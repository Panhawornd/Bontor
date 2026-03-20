import { NextResponse } from 'next/server'
import { prisma } from '@/lib/db'
import { verifyToken } from '@/lib/auth'
import { redis } from '@/lib/redis'
import crypto from 'crypto'

const SCIENCE_GRADE_LIMITS: Record<string, number> = {
  math: 125,
  physics: 75,
  chemistry: 75,
  biology: 75,
  khmer: 75,
  english: 50,
  history: 50,
}

const SOCIAL_SCIENCE_GRADE_LIMITS: Record<string, number> = {
  khmer: 125,
  math: 75,
  geography: 75,
  history: 75,
  moral: 75,
  earth: 50,
  english: 50,
}

type AnalyzeGrade = { subject: string; score: number }

function sameSubjects(required: string[], incoming: string[]) {
  return required.length === incoming.length && required.every((s) => incoming.includes(s))
}

function validateAnalyzePayload(body: unknown):
  | { ok: true; payload: { grades: AnalyzeGrade[]; interest_text: string; career_goals: string } }
  | { ok: false; error: string } {
  if (!body || typeof body !== 'object') {
    return { ok: false, error: 'Invalid request body' }
  }

  const obj = body as Record<string, unknown>
  const interestText = typeof obj.interest_text === 'string' ? obj.interest_text.trim() : ''
  const careerGoals = typeof obj.career_goals === 'string' ? obj.career_goals.trim() : ''

  if (!interestText) {
    return { ok: false, error: 'interest_text is required' }
  }

  const rawGrades = Array.isArray(obj.grades) ? obj.grades : null
  if (!rawGrades || rawGrades.length !== 7) {
    return { ok: false, error: 'All 7 subject grades are required' }
  }

  const parsedGrades: AnalyzeGrade[] = []
  const seen = new Set<string>()
  for (const g of rawGrades) {
    if (!g || typeof g !== 'object') {
      return { ok: false, error: 'Invalid grade format' }
    }

    const grade = g as Record<string, unknown>
    const subject = typeof grade.subject === 'string' ? grade.subject.trim() : ''
    const score = grade.score
    if (!subject || typeof score !== 'number' || !isFinite(score)) {
      return { ok: false, error: 'Each grade must include valid subject and numeric score' }
    }

    if (seen.has(subject)) {
      return { ok: false, error: `Duplicate subject: ${subject}` }
    }
    seen.add(subject)
    parsedGrades.push({ subject, score })
  }

  const incomingSubjects = parsedGrades.map((g) => g.subject)
  const scienceSubjects = Object.keys(SCIENCE_GRADE_LIMITS)
  const socialSubjects = Object.keys(SOCIAL_SCIENCE_GRADE_LIMITS)

  let limits: Record<string, number> | null = null
  if (sameSubjects(scienceSubjects, incomingSubjects)) {
    limits = SCIENCE_GRADE_LIMITS
  } else if (sameSubjects(socialSubjects, incomingSubjects)) {
    limits = SOCIAL_SCIENCE_GRADE_LIMITS
  } else {
    return { ok: false, error: 'Grades must match exactly one valid exam type subject set' }
  }

  for (const g of parsedGrades) {
    const max = limits[g.subject]
    if (typeof max !== 'number') {
      return { ok: false, error: `Unknown subject: ${g.subject}` }
    }
    if (g.score < 0 || g.score > max) {
      return { ok: false, error: `Score for ${g.subject} must be between 0 and ${max}` }
    }
  }

  return {
    ok: true,
    payload: {
      grades: parsedGrades,
      interest_text: interestText.slice(0, 2000),
      career_goals: careerGoals.slice(0, 2000),
    },
  }
}

export async function POST(req: Request) {
  try {
    const body = await req.json()
    const validation = validateAnalyzePayload(body)
    if (!validation.ok) {
      return NextResponse.json({ error: validation.error }, { status: 400 })
    }
    const payload = validation.payload
    const fastapiUrl = process.env.FASTAPI_URL || 'http://localhost:8000'

        // Get user from JWT token
        let user = null
        try {
          const rawCookie = req.headers.get('cookie')
            ?.split(';')
            .find(c => c.trim().startsWith('auth-token='))
          const token = rawCookie?.split('=').slice(1).join('=')
          if (token) {
            const decoded = verifyToken(token)
            if (decoded && typeof decoded === 'object' && 'userId' in decoded) {
              user = await prisma.user.findUnique({
                where: { id: decoded.userId as number }
              })
            }
          }
        } catch (authError) {
          console.error('Auth error:', authError)
        }

    // -------------------------------------------------------------------------
    // REDIS CACHING BLOCK
    // Generate a unique key based on the hashed payload
    // -------------------------------------------------------------------------
    const payloadHash = crypto
      .createHash('md5')
      .update(JSON.stringify(payload))
      .digest('hex')
    const cacheKey = `analyze:cache:${payloadHash}`

    let data = null

    try {
      if (redis.isOpen) {
        const cached = await redis.get(cacheKey)
        if (cached) {
          console.log(`[Redis] Cache hit for ${cacheKey}`)
          data = JSON.parse(cached)
        }
      }
    } catch (cacheError) {
      console.error('[Redis] Error reading from cache:', cacheError)
    }

    // If not in cache, call the ML service
    if (!data) {
      console.log(`[ML Service] Cache miss. Calling ML service at ${fastapiUrl}`)
      // ML service API key for secure service-to-service communication
      const mlApiKey = process.env.ML_API_KEY
      if (!mlApiKey) {
        console.warn('ML_API_KEY is not defined in environment variables')
      }
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 30000)

      const res = await fetch(`${fastapiUrl}/api/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': mlApiKey || '',
        },
        body: JSON.stringify(payload),
        signal: controller.signal,
      })

      clearTimeout(timeoutId)

      if (!res.ok) {
        const text = await res.text()
        return NextResponse.json({ error: 'ML service error', details: text }, { status: 502 })
      }

      data = await res.json()

      // Store in Redis for 24 hours
      try {
        if (redis.isOpen && data) {
          await redis.set(cacheKey, JSON.stringify(data), {
            EX: 86400, // 24 hours in seconds
          })
          console.log(`[Redis] Cached new result for ${cacheKey}`)
        }
      } catch (cacheStoreError) {
        console.error('[Redis] Error saving to cache:', cacheStoreError)
      }
    }

    // Save to database only if user is authenticated
    if (user) {
      try {
        // Save recommendation with metadata (for robust history view)
        const majorsArray = Array.isArray(data.majors) ? [...data.majors] : []
        if (majorsArray.length > 0 && typeof majorsArray[0] === 'object' && majorsArray[0] !== null) {
          majorsArray[0] = {
            ...majorsArray[0],
            _userInterest: payload.interest_text,
            _userGrades: payload.grades
          }
        }

        const recommendation = await prisma.recommendation.create({
          data: {
            user: { connect: { id: user.id } },
            majors: majorsArray,
            jobs: data.careers,
            universities: data.universities,
            skillGaps: data.skill_gaps,
          }
        })

        // Save input using Prisma ORM
        await prisma.input.create({
          data: {
            userId: user.id,
            recommendationId: recommendation.id,
            interestText: payload.interest_text,
            careerGoals: payload.career_goals,
          }
        });

        // Save grades using Prisma ORM
        for (const grade of payload.grades) {
          await prisma.grade.create({
            data: {
              userId: user.id,
              recommendationId: recommendation.id,
              subject: grade.subject,
              score: grade.score,
            }
          });
        }
      } catch (dbError) {
        console.error('Database error:', dbError)
      }
    }

    return NextResponse.json(data)
  } catch (err) {
    console.error('Analyze API error:', err)
    if (err instanceof Error && err.name === 'AbortError') {
      return NextResponse.json({ error: 'Request timeout - ML service took too long to respond' }, { status: 504 })
    }
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 })
  }
}

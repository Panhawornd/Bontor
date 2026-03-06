import { NextResponse } from 'next/server'
import { prisma } from '@/lib/db'
import { verifyToken } from '@/lib/auth'

export async function POST(req: Request) {
  try {
    const body = await req.json()
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

    // ML service API key for secure service-to-service communication
    const mlApiKey = process.env.ML_API_KEY || 'capstone-ml-secret-key-2026'

    // Call ML service with timeout
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 30000) // 30 second timeout
    
    const res = await fetch(`${fastapiUrl}/api/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': mlApiKey,
      },
      body: JSON.stringify(body),
      signal: controller.signal,
    })
    
    clearTimeout(timeoutId)

    if (!res.ok) {
      const text = await res.text()
      return NextResponse.json({ error: 'ML service error', details: text }, { status: 502 })
    }

    const data = await res.json()

    // Save to database only if user is authenticated
    if (user) {
      try {
        // Validate grades before saving
        const grades = Array.isArray(body.grades) ? body.grades.slice(0, 20) : []

        // Save grades
        for (const grade of grades) {
          if (
            grade &&
            typeof grade.subject === 'string' && grade.subject.length <= 100 &&
            typeof grade.score === 'number' && isFinite(grade.score) && grade.score >= 0 && grade.score <= 200
          ) {
            await prisma.grade.create({
              data: {
                userId: user.id,
                subject: grade.subject,
                score: grade.score,
              }
            })
          }
        }

        // Save input
        const interestText = typeof body.interest_text === 'string' ? body.interest_text.slice(0, 2000) : ''
        const careerGoals = typeof body.career_goals === 'string' ? body.career_goals.slice(0, 2000) : ''
        await prisma.input.create({
          data: {
            userId: user.id,
            interestText,
            careerGoals,
          }
        })

        // Save recommendation
        await prisma.recommendation.create({
          data: {
            userId: user.id,
            majors: data.majors,
            jobs: data.careers,
            universities: data.universities,
            skillGaps: data.skill_gaps,
          }
        })

      } catch (dbError) {
        console.error('Database error:', dbError)
        // Continue even if database save fails
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

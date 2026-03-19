import { NextResponse } from 'next/server'
import { prisma } from '@/lib/db'
import { verifyToken } from '@/lib/auth'

export const dynamic = 'force-dynamic'
export const revalidate = 0

const MAX_SCORES: Record<string, number> = {
  math: 125, physics: 75, chemistry: 75, biology: 75,
  english: 50, khmer: 75, history: 50,
  geography: 75, moral: 75, earth: 50,
}

interface AnalysisSubjectGrade {
  subject: string;
  score: number;
}

interface AnalysisMetadata {
  _userInterest?: string;
  _userGrades?: AnalysisSubjectGrade[];
  [key: string]: unknown;
}

function buildSubjectAnalysis(grades: AnalysisSubjectGrade[]) {
  const entries: Record<string, { score: number; normalized: number; strength: string }> = {}
  const normScores: number[] = []

  for (const g of grades) {
    const max = MAX_SCORES[g.subject.toLowerCase()] ?? 100
    const normalized = max > 0 ? (g.score / max) * 100 : 0
    normScores.push(normalized)
    entries[g.subject] = { score: g.score, normalized: Math.round(normalized * 10) / 10, strength: '' }
  }

  if (normScores.length > 0) {
    const mean = normScores.reduce((a, b) => a + b, 0) / normScores.length
    const std = normScores.length > 1
      ? Math.sqrt(normScores.reduce((s, n) => s + (n - mean) ** 2, 0) / normScores.length)
      : 10

    for (const subj of Object.keys(entries)) {
      const n = entries[subj].normalized
      if (n >= mean + std) entries[subj].strength = 'Excellent'
      else if (n >= mean) entries[subj].strength = 'Good'
      else if (n >= mean - std) entries[subj].strength = 'Average'
      else entries[subj].strength = 'Needs Improvement'
    }
  }

  return entries
}

export async function GET(req: Request) {
  try {
    const rawCookie = req.headers.get('cookie')
      ?.split(';')
      .find(c => c.trim().startsWith('auth-token='))
    const token = rawCookie?.split('=').slice(1).join('=')

    if (!token) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const payload = verifyToken(token)
    if (!payload || typeof payload.userId !== 'number') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const userId = payload.userId

    const [recommendations, inputs, allFullGrades] = await Promise.all([
      prisma.recommendation.findMany({
        where: { userId },
        orderBy: { id: 'desc' },
        select: {
          id: true,
          majors: true,
          jobs: true,
          universities: true,
          skillGaps: true,
          createdAt: true,
        },
      }),
      prisma.input.findMany({
        where: { userId },
        orderBy: { id: 'desc' },
        select: { interestText: true, createdAt: true },
      }),
      prisma.$queryRaw`
        SELECT id, subject, score, "created_at" AS "createdAt"
        FROM grades
        WHERE user_id = ${userId}
        ORDER BY id DESC
      ` as Promise<{ id: number, subject: string, score: number, createdAt: Date }[]>
    ])

    const history = recommendations.map((rec, index) => {
      // 1. Try to get metadata embedded in the JSON blob (for new records)
      const majors = (rec.majors as unknown as AnalysisMetadata[]) || []
      const metadataSource = majors[0] || {}
      
      let interestText = metadataSource._userInterest
      let gradeData = metadataSource._userGrades
      
      // 2. Fallback for old records: Match Input by timestamp, but Grades by conservative index (due to schema limits)
      if (!interestText || !gradeData) {
        // Find Input created within 1 minute of this recommendation
        const matchingInput = inputs.find(inp => 
          Math.abs(new Date(inp.createdAt).getTime() - new Date(rec.createdAt).getTime()) < 60000
        )
        interestText = interestText || matchingInput?.interestText || 'Analysis'
        
        // Find Grades using timestamp if metadata is missing
        if (!gradeData) {
          const matchingGrades = allFullGrades.filter(g => 
            Math.abs(new Date(g.createdAt).getTime() - new Date(rec.createdAt).getTime()) < 60000
          )
          
          if (matchingGrades.length > 0) {
            gradeData = matchingGrades.map(g => ({ subject: g.subject, score: Number(g.score) }))
          } else {
            // Ultimate fallback to index (deprecated)
            const startIdx = index * 7
            const gradeChunk = allFullGrades.slice(startIdx, startIdx + 7)
            gradeData = gradeChunk.map(g => ({ subject: g.subject, score: Number(g.score) }))
          }
        }
      }

      const subjectAnalysis = (gradeData && gradeData.length > 0) ? buildSubjectAnalysis(gradeData) : {}

      return {
        id: rec.id,
        interestText,
        majors: rec.majors,
        careers: rec.jobs,
        universities: rec.universities,
        skill_gaps: rec.skillGaps,
        subject_analysis: subjectAnalysis,
        createdAt: rec.createdAt,
      }
    })

    return NextResponse.json({ history })
  } catch (error) {
    console.error('Analysis history error:', error)
    return NextResponse.json({ history: [] })
  }
}

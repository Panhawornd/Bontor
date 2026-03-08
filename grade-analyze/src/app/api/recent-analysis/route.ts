import { NextResponse } from 'next/server'
import { prisma } from '@/lib/db'
import { verifyToken } from '@/lib/auth'

const MAX_SCORES: Record<string, number> = {
  math: 125, physics: 75, chemistry: 75, biology: 75,
  english: 50, khmer: 75, history: 50,
  geography: 75, moral: 75, earth: 50,
}

function buildSubjectAnalysis(grades: { subject: string; score: number }[]) {
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
      return NextResponse.json({ analysis: null })
    }

    const payload = verifyToken(token)
    if (!payload) {
      return NextResponse.json({ analysis: null })
    }

    const recommendation = await prisma.recommendation.findFirst({
      where: { userId: payload.userId },
      orderBy: { createdAt: 'desc' },
      select: {
        id: true,
        majors: true,
        jobs: true,
        universities: true,
        skillGaps: true,
        createdAt: true,
      },
    })

    if (!recommendation) {
      return NextResponse.json({ analysis: null })
    }

    // Get the latest 7 grades for this user to reconstruct subject_analysis
    const grades = await prisma.grade.findMany({
      where: { userId: payload.userId },
      orderBy: { id: 'desc' },
      take: 7,
      select: { subject: true, score: true },
    })

    const gradeData = grades.map(g => ({ subject: g.subject, score: Number(g.score) }))
    const subjectAnalysis = buildSubjectAnalysis(gradeData)

    // Map DB field names to the AnalysisResult shape used by RecommendationDashboard
    const analysis = {
      majors: recommendation.majors,
      careers: recommendation.jobs,
      universities: recommendation.universities,
      skill_gaps: recommendation.skillGaps,
      subject_analysis: subjectAnalysis,
      createdAt: recommendation.createdAt,
    }

    return NextResponse.json({ analysis })
  } catch (error) {
    console.error('Recent analyses error:', error)
    return NextResponse.json({ analysis: null })
  }
}

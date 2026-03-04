import { NextResponse } from 'next/server'
import { prisma } from '@/lib/db'
import { verifyToken } from '@/lib/auth'

export async function GET(req: Request) {
  try {
    const token = req.headers.get('cookie')
      ?.split(';')
      .find(c => c.trim().startsWith('auth-token='))
      ?.split('=')[1]

    if (!token) {
      return NextResponse.json({ analysisCount: 0, requestCount: 0 })
    }

    const payload = verifyToken(token)
    if (!payload) {
      return NextResponse.json({ analysisCount: 0, requestCount: 0 })
    }

    const [analysisCount, requestCount] = await Promise.all([
      prisma.input.count({ where: { userId: payload.userId } }),
      prisma.recommendation.count({ where: { userId: payload.userId } }),
    ])

    return NextResponse.json({ analysisCount, requestCount })
  } catch (error) {
    console.error('Stats error:', error)
    return NextResponse.json({ analysisCount: 0, requestCount: 0 })
  }
}

import { NextResponse } from 'next/server'
import { PrismaClient } from '@prisma/client'
import { verifyToken } from '@/lib/auth'

const prisma = new PrismaClient()

export async function POST(req: Request) {
  try {
    const body = await req.json()
    const fastapiUrl = process.env.FASTAPI_URL || 'http://localhost:8000'

        // Get user from JWT token
        let user = null
        try {
          const token = req.headers.get('cookie')?.split('auth-token=')[1]?.split(';')[0]
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

    // Call ML service with timeout
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 30000) // 30 second timeout
    
    const res = await fetch(`${fastapiUrl}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
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

        // Save grades
        for (const grade of body.grades) {
          await prisma.grade.create({
            data: {
              userId: user.id,
              subject: grade.subject,
              score: grade.score,
            }
          })
        }

        // Save input
        await prisma.input.create({
          data: {
            userId: user.id,
            interestText: body.interest_text,
            careerGoals: body.career_goals,
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

        // Send feedback data to ML service for training dataset
        try {
          const feedbackData = {
            user_id: user.id,
            grades: body.grades,
            interests: body.interest_text,
            career_goals: body.career_goals,
            recommendations: data,
            timestamp: new Date().toISOString()
          }
          
          // Send to ML service (fire and forget)
          fetch(`${fastapiUrl}/feedback`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(feedbackData),
          }).catch(() => {
            // Ignore errors - this is for data collection
          })
        } catch (feedbackError) {
          // Ignore feedback errors
        }

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

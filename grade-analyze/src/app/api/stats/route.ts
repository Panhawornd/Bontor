import { NextResponse } from 'next/server'
import { prisma } from '@/lib/db'
import { verifyToken } from '@/lib/auth'

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
    if (!payload) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    if (typeof payload.userId !== 'number') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const userId = payload.userId
    
    // Count analyses (from input table)
    const analysisCount = await prisma.input.count({ where: { userId } });
    
    // Count total chat sessions
    const chatCount = await prisma.chatSession.count({ where: { userId } });
    
    // Count only user messages across all sessions (user's questions)
    const requestCount = await prisma.chatMessage.count({
      where: {
        role: 'user',
        session: {
          userId: userId
        }
      }
    });

    return NextResponse.json({ analysisCount, chatCount, requestCount })
  } catch (error) {
    console.error('Stats error:', error)
    return NextResponse.json({ analysisCount: 0, requestCount: 0 })
  }
}

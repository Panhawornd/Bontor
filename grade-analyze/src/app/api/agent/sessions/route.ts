import { NextResponse } from 'next/server'
import { prisma } from '@/lib/db'
import { verifyToken } from '@/lib/auth'

// GET: Fetch all chat sessions for the authenticated user
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
    if (!payload || typeof payload !== 'object' || !('userId' in payload)) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const sessions = await prisma.chatSession.findMany({
      where: { userId: payload.userId as number },
      orderBy: { updatedAt: 'desc' },
      include: {
        messages: {
          orderBy: { createdAt: 'asc' },
          select: { role: true, content: true },
        },
      },
    })

    return NextResponse.json({ sessions })
  } catch (error) {
    console.error('Chat sessions fetch error:', error)
    return NextResponse.json({ error: 'Failed to fetch chat sessions' }, { status: 500 })
  }
}

// POST: Create a new chat session
export async function POST(req: Request) {
  try {
    const rawCookie = req.headers.get('cookie')
      ?.split(';')
      .find(c => c.trim().startsWith('auth-token='))
    const token = rawCookie?.split('=').slice(1).join('=')

    if (!token) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const payload = verifyToken(token)
    if (!payload || typeof payload !== 'object' || !('userId' in payload)) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await req.json()
    const { title } = body as { title?: string }

    const session = await prisma.chatSession.create({
      data: {
        userId: payload.userId as number,
        title: title || 'New Chat',
      },
    })

    return NextResponse.json({ session })
  } catch (error) {
    console.error('Chat session create error:', error)
    return NextResponse.json({ error: 'Failed to create chat session' }, { status: 500 })
  }
}

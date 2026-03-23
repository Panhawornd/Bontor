import { NextResponse } from 'next/server'
import { prisma } from '@/lib/db'
import { verifyToken } from '@/lib/auth'

// DELETE: Delete a specific chat session
export async function DELETE(
  req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
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

    const { id } = await params
    const sessionId = parseInt(id)
    if (isNaN(sessionId)) {
      return NextResponse.json({ error: 'Invalid session ID' }, { status: 400 })
    }

    // Verify the session belongs to this user
    const session = await prisma.chatSession.findFirst({
      where: { id: sessionId, userId: payload.userId as number },
    })

    if (!session) {
      return NextResponse.json({ error: 'Session not found' }, { status: 404 })
    }

    // Delete session (messages cascade automatically)
    await prisma.chatSession.delete({
      where: { id: sessionId },
    })

    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('Chat session delete error:', error)
    return NextResponse.json({ error: 'Failed to delete chat session' }, { status: 500 })
  }
}

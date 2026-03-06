import { NextResponse } from 'next/server'
import { prisma } from '@/lib/db'
import { verifyToken } from '@/lib/auth'

export async function GET(req: Request) {
  try {
    const rawCookie = req.headers.get('cookie')
      ?.split(';')
      .find(c => c.trim().startsWith('auth-token='))
    // Use slice(1).join('=') to handle base64 '=' padding in JWT
    const token = rawCookie?.split('=').slice(1).join('=')

    if (!token) {
      return NextResponse.json({ user: null })
    }

    const payload = verifyToken(token)
    if (!payload) {
      return NextResponse.json({ user: null })
    }

    // Return user from JWT payload — no DB roundtrip needed
    const user = { id: payload.userId, email: payload.email, name: payload.name }

    return NextResponse.json(
      { user },
      { headers: { 'Cache-Control': 'private, max-age=30, stale-while-revalidate=60' } }
    )
  } catch (error) {
    console.error('Auth check error:', error)
    return NextResponse.json({ user: null })
  }
}

export async function PATCH(req: Request) {
  try {
    const rawCookiePatch = req.headers.get('cookie')
      ?.split(';')
      .find(c => c.trim().startsWith('auth-token='))
    const token = rawCookiePatch?.split('=').slice(1).join('=')

    if (!token) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const payload = verifyToken(token)
    if (!payload) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { name } = await req.json()
    if (!name || typeof name !== 'string' || name.trim().length < 1 || name.trim().length > 100) {
      return NextResponse.json({ error: 'Name must be 1-100 characters' }, { status: 400 })
    }

    const updated = await prisma.user.update({
      where: { id: payload.userId },
      data: { name: name.trim() },
      select: { id: true, name: true, email: true }
    })

    // Re-issue JWT with updated name so future /api/auth/me calls reflect the change
    const newToken = (await import('@/lib/auth')).generateToken({
      id: updated.id,
      name: updated.name!,
      email: updated.email!
    })
    const patchResponse = NextResponse.json({ user: updated })
    patchResponse.cookies.set('auth-token', newToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 24 * 60 * 60,
      path: '/'
    })
    return patchResponse
  } catch (error) {
    console.error('Update name error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

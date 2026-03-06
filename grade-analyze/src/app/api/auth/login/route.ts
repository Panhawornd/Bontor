import { NextResponse } from 'next/server'
import { prisma } from '@/lib/db'
import { comparePassword, generateToken } from '@/lib/auth'

export async function POST(req: Request) {
  try {
    const body = await req.json()
    const { email, password } = body

    // Input validation
    if (!email || typeof email !== 'string' || !password || typeof password !== 'string') {
      return NextResponse.json({ error: 'Invalid credentials' }, { status: 401 })
    }
    if (password.length > 128) {
      return NextResponse.json({ error: 'Invalid credentials' }, { status: 401 })
    }

    const normalizedEmail = email.trim().toLowerCase()

    // Find user
    const user = await prisma.user.findUnique({
      where: { email: normalizedEmail }
    })

    if (!user || !user.password) {
      return NextResponse.json({ error: 'Invalid credentials' }, { status: 401 })
    }

    // Check password
    const isValidPassword = await comparePassword(password, user.password)
    if (!isValidPassword) {
      return NextResponse.json({ error: 'Invalid credentials' }, { status: 401 })
    }

    // Generate token
    const token = generateToken({
      id: user.id,
      name: user.name!,
      email: user.email!
    })

    // Set cookie
    const response = NextResponse.json({ 
      message: 'Login successful',
      user: { id: user.id, name: user.name, email: user.email }
    })

    response.cookies.set('auth-token', token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 24 * 60 * 60, // 24 hours
      path: '/'
    })

    return response
  } catch (error) {
    console.error('Login error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

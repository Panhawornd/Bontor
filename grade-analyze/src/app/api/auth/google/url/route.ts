import { NextResponse } from 'next/server'

// Generate OAuth URL endpoint
export async function GET() {
  try {
    const clientId = process.env.GOOGLE_CLIENT_ID

    if (!clientId) {
      return NextResponse.json({ error: 'OAuth configuration error' }, { status: 500 })
    }

    const appUrl = process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'
    const redirectUri = `${appUrl}/api/auth/callback/google`
    const scope = 'openid email profile'
    const responseType = 'code'
    // Use cryptographically secure random state for CSRF protection
    const state = crypto.randomUUID()
    const prompt = 'consent'

    const googleUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${encodeURIComponent(scope)}&response_type=${responseType}&state=${state}&prompt=${prompt}`

    // Store state in a short-lived httpOnly cookie for verification on callback
    const response = NextResponse.json({ url: googleUrl })
    response.cookies.set('oauth_state', state, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 60 * 10, // 10 minutes
      path: '/'
    })
    return response
  } catch {
    return NextResponse.json({ error: 'Failed to generate OAuth URL' }, { status: 500 })
  }
}
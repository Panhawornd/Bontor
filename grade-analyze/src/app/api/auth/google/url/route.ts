import { NextResponse } from 'next/server'

// Generate OAuth URL endpoint
export async function GET() {
  try {
    const clientId = process.env.GOOGLE_CLIENT_ID
    const clientSecret = process.env.GOOGLE_CLIENT_SECRET

    if (!clientId || !clientSecret) {
      return NextResponse.json({ error: 'OAuth configuration error' }, { status: 500 })
    }

    const redirectUri = 'http://localhost:3000/api/auth/callback/google'
    const scope = 'openid email profile'
    const responseType = 'code'
    const state = Math.random().toString(36).substring(7) + Date.now().toString()
    const prompt = 'consent' // Force consent screen to appear

    const googleUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${encodeURIComponent(scope)}&response_type=${responseType}&state=${state}&prompt=${prompt}`

    return NextResponse.json({ url: googleUrl })
  } catch (error) {
    return NextResponse.json({ error: 'Failed to generate OAuth URL' }, { status: 500 })
  }
}
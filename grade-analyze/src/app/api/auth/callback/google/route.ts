import { NextRequest, NextResponse } from 'next/server'
import { generateToken } from "@/lib/auth"
import { prisma } from '@/lib/db'

// Helper: redirect to login with an error, always clearing the oauth_state cookie
function errorRedirect(url: URL, errorCode: string): NextResponse {
  const response = NextResponse.redirect(new URL(`/login?error=${errorCode}`, url))
  response.cookies.delete('oauth_state')
  return response
}

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const code = searchParams.get('code')
    const oauthError = searchParams.get('error')
    const state = searchParams.get('state')

    // Handle OAuth errors — never reflect raw OAuth error values into the URL
    if (oauthError) {
      return errorRedirect(new URL(request.url), 'oauth_denied')
    }

    if (!code) {
      return errorRedirect(new URL(request.url), 'no_code')
    }

    // Verify state against the cookie to prevent CSRF attacks
    const expectedState = request.cookies.get('oauth_state')?.value
    if (!state || !expectedState || state !== expectedState) {
      return errorRedirect(new URL(request.url), 'invalid_state')
    }

    // Exchange authorization code for access token
    const clientId = process.env.GOOGLE_CLIENT_ID
    const clientSecret = process.env.GOOGLE_CLIENT_SECRET

    if (!clientId || !clientSecret) {
      return errorRedirect(new URL(request.url), 'config_error')
    }

    const tokenResponse = await fetch('https://oauth2.googleapis.com/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        client_id: clientId,
        client_secret: clientSecret,
        code,
        grant_type: 'authorization_code',
        redirect_uri: `${process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'}/api/auth/callback/google`,
      }),
    })

    const tokenData = await tokenResponse.json()

    if (!tokenResponse.ok) {
      return errorRedirect(new URL(request.url), 'token_exchange_failed')
    }

    // Get user info from Google
    const userResponse = await fetch('https://www.googleapis.com/oauth2/v2/userinfo', {
      headers: {
        'Authorization': `Bearer ${tokenData.access_token}`,
      },
    })

    const googleUser = await userResponse.json()

    if (!userResponse.ok) {
      return errorRedirect(new URL(request.url), 'user_info_failed')
    }

    // Check if user exists in our database
    let user = await prisma.user.findUnique({
      where: { email: googleUser.email }
    })

    if (!user) {
      // Create new user
      user = await prisma.user.create({
        data: {
          name: googleUser.name,
          email: googleUser.email,
          emailVerified: new Date(),
          image: googleUser.picture,
          provider: "google",
          providerId: googleUser.id,
        }
      })
    } else if (!user.provider || user.provider === "credentials") {
      // Update existing user with OAuth info
      user = await prisma.user.update({
        where: { email: googleUser.email },
        data: {
          provider: "google",
          providerId: googleUser.id,
          image: googleUser.picture,
          emailVerified: user.emailVerified || new Date(),
        }
      })
    }

    // Generate our custom JWT token
    const token = generateToken({
      id: user.id,
      name: user.name!,
      email: user.email!
    })

    // Create response with redirect to /Input
    const response = NextResponse.redirect(new URL('/Input', request.url))

    // Set the same auth-token cookie as regular login
    response.cookies.set('auth-token', token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 24 * 60 * 60 // 24 hours
    })

    // Set localStorage flag for instant UI updates
    response.cookies.set('just_logged_in', 'true', {
      httpOnly: false, // Allow client-side access
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 60 // 1 minute
    })
    response.cookies.set('just_logged_out', '', {
      httpOnly: false,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 0
    })
    // Clear the oauth state cookie
    response.cookies.delete('oauth_state')

    return response
  } catch {
    const response = NextResponse.redirect(new URL('/login?error=oauth_callback_failed', request.url))
    response.cookies.delete('oauth_state')
    return response
  }
}
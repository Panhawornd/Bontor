import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

interface JWTPayload {
  userId: number
  email: string
  exp?: number
}

// Verify JWT signature using Web Crypto API (Edge Runtime compatible)
async function verifyToken(token: string): Promise<JWTPayload | null> {
  try {
    const parts = token.split('.')
    if (parts.length !== 3) return null

    const secret = process.env.JWT_SECRET || 'aghd@%ajsakjh'
    const encoder = new TextEncoder()

    const key = await crypto.subtle.importKey(
      'raw',
      encoder.encode(secret),
      { name: 'HMAC', hash: 'SHA-256' },
      false,
      ['verify']
    )

    const signatureInput = encoder.encode(`${parts[0]}.${parts[1]}`)
    const signatureBytes = Uint8Array.from(
      atob(parts[2].replace(/-/g, '+').replace(/_/g, '/')),
      (c) => c.charCodeAt(0)
    )

    const valid = await crypto.subtle.verify('HMAC', key, signatureBytes, signatureInput)
    if (!valid) return null

    const payload = JSON.parse(atob(parts[1].replace(/-/g, '+').replace(/_/g, '/')))

    if (payload.exp && payload.exp < Date.now() / 1000) return null

    return payload as JWTPayload
  } catch {
    return null
  }
}

export async function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token')?.value
  const { pathname } = request.nextUrl

  // Skip middleware for API routes - let them handle auth themselves
  if (pathname.startsWith('/api/')) {
    return NextResponse.next()
  }

  // Routes that authenticated users should not access
  const authOnlyBlockedRoutes = ['/login', '/signup']
  const isAuthOnlyBlockedRoute = authOnlyBlockedRoutes.includes(pathname)

  // If user has valid token and tries to access login/signup, redirect to Input
  if (token && isAuthOnlyBlockedRoute) {
    const payload = await verifyToken(token)
    if (payload) {
      return NextResponse.redirect(new URL('/Input', request.url))
    }
  }

  // Public routes that don't require authentication
  const publicRoutes = ['/login', '/signup', '/landing', '/how-it-works', '/about']
  const isPublicRoute = publicRoutes.includes(pathname)

  if (isPublicRoute) {
    return NextResponse.next()
  }

  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  const payload = await verifyToken(token)
  if (!payload) {
    const response = NextResponse.redirect(new URL('/login', request.url))
    response.cookies.delete('auth-token')
    return response
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - image (public image files)
     * - lottie (public lottie animation files)
     * - logo.svg (logo file)
     * - file.svg, globe.svg, next.svg, vercel.svg, window.svg (public assets)
     */
    '/((?!api|_next/static|_next/image|favicon.ico|icon-with-bg.svg|icon.svg|image|lottie|logo.svg|file.svg|globe.svg|next.svg|vercel.svg|window.svg).*)',
  ],
}

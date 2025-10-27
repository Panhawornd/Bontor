import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

const JWT_SECRET = process.env.JWT_SECRET || 'aghd@%ajsakjh'

interface JWTPayload {
  userId: number
  email: string
}

// Simple JWT verification for Edge Runtime
function verifyToken(token: string): JWTPayload | null {
  try {
    // Split the token
    const parts = token.split('.')
    if (parts.length !== 3) {
      return null
    }

    // Decode the payload (base64url decode)
    const payload = JSON.parse(atob(parts[1].replace(/-/g, '+').replace(/_/g, '/')))
    
    // Check if token is expired
    if (payload.exp && payload.exp < Date.now() / 1000) {
      return null
    }

    return payload as JWTPayload
  } catch (error) {
    return null
  }
}

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token')?.value
  const { pathname } = request.nextUrl

  // Skip middleware for API routes - let them handle auth themselves
  if (pathname.startsWith('/api/')) {
    return NextResponse.next()
  }

  // Public routes that don't require authentication
  const publicRoutes = ['/login', '/signup', '/landing', '/how-it-works', '/about']
  const isPublicRoute = publicRoutes.includes(pathname)

  // If it's a public route, allow access
  if (isPublicRoute) {
    return NextResponse.next()
  }

  // If no token and trying to access protected route, redirect to login
  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // Verify token
  const payload = verifyToken(token)
  if (!payload) {
    // Invalid token, redirect to login
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
    '/((?!api|_next/static|_next/image|favicon.ico|image|lottie|logo.svg|file.svg|globe.svg|next.svg|vercel.svg|window.svg).*)',
  ],
}

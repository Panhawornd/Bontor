"use client";

import { useState, useEffect, Suspense } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { X } from 'lucide-react'
import Button from '@/components/ui/Button'
import Input from '@/components/ui/Input'
import Card from '@/components/ui/Card'
import Link from 'next/link'

function LoginContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [isErrorVisible, setIsErrorVisible] = useState(true)
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  // Handle OAuth errors from URL parameters
  useEffect(() => {
    const error = searchParams.get('error')
    
    if (error) {
      setError('Authentication failed. Please try again.')
      setIsErrorVisible(true)
      
      // Clear URL parameters
      const url = new URL(window.location.href)
      url.searchParams.delete('error')
      url.searchParams.delete('callbackUrl')
      window.history.replaceState({}, '', url.toString())
      
      setTimeout(() => {
        setIsErrorVisible(false)
        setTimeout(() => setError(''), 300)
      }, 5000)
    }
  }, [searchParams])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setIsErrorVisible(true)

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        // Set localStorage flag to indicate successful login
        localStorage.setItem('just_logged_in', 'true')
        localStorage.removeItem('just_logged_out')
        // Use window.location for a hard redirect to ensure cookie is available
        window.location.href = '/Input'
      } else {
        const data = await response.json()
        setError(data.error || 'Login failed')
        setIsErrorVisible(true)
        setTimeout(() => {
          setIsErrorVisible(false)
          setTimeout(() => setError(''), 300)
        }, 5000)
      }
    } catch (err) {
      setError('Something went wrong. Please try again.')
      setIsErrorVisible(true)
      setTimeout(() => {
        setIsErrorVisible(false)
        setTimeout(() => setError(''), 300)
      }, 5000)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ 
      minHeight: '100vh', 
      color: '#ffffff',
      position: 'relative'
    }}>
      {/* Ultravib image background with dark overlay */}
      <div
        style={{ 
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundImage: "url(/image/Ultravib.png)",
          backgroundSize: 'cover',
          backgroundPosition: 'center center',
          backgroundRepeat: 'no-repeat',
          filter: 'brightness(0.9)',
          zIndex: 0,
          pointerEvents: 'none'
        }}
      />
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-transparent backdrop-blur-md min-h-[4rem]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16 relative">
            {/* Logo */}
            <div className="absolute left-3 md:left-0 flex items-center gap-3">
              <button
                onClick={() => {
                  window.location.href = '/landing'
                }}
                className="hover:opacity-80 transition-opacity"
              >
                <img 
                  src="/image/Bontor-logo.png" 
                  alt="Bontor" 
                  className="h-5 md:h-[23px] w-auto"
                />
              </button>
            </div>

            {/* Navigation Links - align with logo and stay at right (hidden on mobile) */}
            <div className="hidden md:flex items-center space-x-8 absolute right-[-10px]">
                <button
                  onClick={() => {
                    window.location.href = '/landing'
                  }}
                  className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
                >
                  Home
                </button>
                <button
                  onClick={() => {
                    window.location.href = '/how-it-works'
                  }}
                  className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
                >
                  How it Works
                </button>
                <button
                  onClick={() => {
                    window.location.href = '/about'
                  }}
                  className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
                >
                  About
                </button>
            </div>

            {/* Mobile Menu Trigger - right */}
            <div className="md:hidden absolute inset-y-0 right-3 flex items-center">
              <button
                onClick={() => setIsMenuOpen(true)}
                className="p-2 rounded-md"
                aria-label="Open menu"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="20"
                  height="20"
                  viewBox="0 0 22 22"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M21 5H3" />
                  <path d="M21 12H9" />
                  <path d="M21 19H7" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Mobile Sidebar Menu (like landing, without footer button) */}
      {isMenuOpen && (
        <div className="fixed inset-0 z-[200] md:hidden">
          <button
            className="absolute inset-0 bg-black/60 backdrop-blur-md"
            aria-label="Close menu"
            onClick={() => setIsMenuOpen(false)}
          />
          <aside
            className="absolute top-0 right-0 h-full w-72 max-w-[80%] text-white border-l border-white/10 shadow-2xl"
            style={{
              backgroundImage:
                "linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url(/image/Ultravib.png)",
              backgroundSize: "cover",
              backgroundPosition: "center",
            }}
          >
            <div className="flex items-center justify-between px-5 py-4 border-b border-white/10">
              <span className="text-base font-semibold tracking-wide uppercase">
                Menu
              </span>
              <button
                onClick={() => setIsMenuOpen(false)}
                className="p-1 text-white/80 hover:text-white transition-colors"
                aria-label="Close menu"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  width="24"
                  height="24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
            </div>
            <div className="flex flex-col gap-6 px-5 py-6 text-sm">
              <button
                onClick={() => { window.location.href = '/landing'; setIsMenuOpen(false); }}
                className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors"
              >
                Home
              </button>
              <button
                onClick={() => { window.location.href = '/how-it-works'; setIsMenuOpen(false); }}
                className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors"
              >
                How it Works
              </button>
              <button
                onClick={() => { window.location.href = '/about'; setIsMenuOpen(false); }}
                className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors"
              >
                About
              </button>
            </div>
          </aside>
        </div>
      )}

      {/* Main Content */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        padding: '16px',
        paddingTop: '80px', // Account for fixed navigation
        position: 'relative',
        zIndex: 10
      }}>
        <div style={{ width: '100%', maxWidth: '400px' }}>
          {/* Login Card */}
          <div className="bg-[#111111] border border-[#1f1f1f] rounded-lg p-8 hover:border-[#2a2a2a] transition-colors">
            {/* Bontor Logo inside the card */}
            <div style={{ textAlign: 'center', marginBottom: '24px' }}>
              <img 
                src="/image/Bontor-logo.png" 
                alt="Bontor" 
                style={{ 
                  height: '28px',
                  width: 'auto',
                  display: 'block',
                  margin: '0 auto'
                }}
              />
            </div>

            {/* Sign in text inside the card */}
            <div style={{ textAlign: 'center', marginBottom: '32px' }}>
              <h2 style={{ 
                fontSize: '15px', 
                fontWeight: '500',
                color: '#cccccc',
                margin: 0
              }}>
                Sign in to your account to continue
              </h2>
            </div>

            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
              {error && (
                <div style={{
                  background: 'rgba(220, 53, 69, 0.1)', 
                  border: '1px solid var(--accent-error)', 
                  borderRadius: '12px', 
                  padding: '20px', 
                  marginBottom: '32px',
                  color: 'var(--accent-error)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px',
                  opacity: isErrorVisible ? 1 : 0,
                  transition: 'opacity 0.3s ease-out'
                }}>
                  <div style={{
                    width: '20px',
                    height: '20px',
                    borderRadius: '50%',
                    background: 'transparent',
                    border: '2px solid #ef4444',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0
                  }}>
                    <X size={12} style={{ color: '#ef4444' }} />
                  </div>
                  <span>{error}</span>
                </div>
              )}

              <div>
                <label style={{ 
                  display: 'block', 
                  marginBottom: '8px', 
                  color: '#ffffff',
                  fontWeight: '500',
                  textAlign: 'left'
                }}>
                  Email Address
                </label>
                <div style={{ display: 'flex', justifyContent: 'center' }}>
                  <input
                    type="email"
                    required
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    placeholder="Enter your email"
                    className="input-field"
                  />
                </div>
            </div>

            <div>
              <label style={{ 
                display: 'block', 
                marginBottom: '8px', 
                color: '#ffffff',
                fontWeight: '500'
              }}>
                Password
              </label>
              <input
                type="password"
                required
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                placeholder="Enter your password"
                className="input-field"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="px-4 py-1.5 bg-gray-800 hover:bg-gray-700 text-white rounded-md transition-colors border border-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
              style={{ width: '100%' }}
            >
              {loading ? (
                <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
                  <svg className="logo-spin" width="20" height="20" viewBox="-30 -30 201 233" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ display: 'block' }}>
                    <g>
                      <path d="M110.464 0C127.032 0.000247877 140.464 13.4316 140.464 30V31.4922H92.9033V58.2891H49.9043V86.3154H0V30C0 13.4315 13.4315 1.61637e-06 30 0H110.464Z" fill="white"/>
                    </g>
                    <g>
                      <path d="M30.5372 172.649C13.9687 172.67 0.453776 159.257 0.350835 142.689L0.341564 141.196L47.9011 141.134L47.7346 114.338L90.7336 114.282L90.5595 86.2549L140.464 86.1897L140.814 142.505C140.917 159.073 127.569 172.522 111 172.544L30.5372 172.649Z" fill="#3B82F6"/>
                    </g>
                  </svg>
                  Signing in...
                </span>
              ) : 'Sign In'}
            </button>

            {/* Divider */}
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              margin: '10px 0',
              gap: '16px'
            }}>
              <div style={{ 
                flex: 1, 
                height: '1px', 
                backgroundColor: '#374151' 
              }}></div>
              <span style={{ 
                color: '#9ca3af', 
                fontSize: '14px',
                fontWeight: '500'
              }}>
                or sign in with
              </span>
              <div style={{ 
                flex: 1, 
                height: '1px', 
                backgroundColor: '#374151' 
              }}></div>
            </div>

            {/* Google OAuth Button */}
            <button
              type="button"
              onClick={async () => {
                try {
                  const response = await fetch('/api/auth/google/url', {
                    method: 'GET',
                  });
                  const data = await response.json();
                  window.location.href = data.url;
                } catch (error) {
                  setError('Failed to start Google authentication');
                  setIsErrorVisible(true);
                  setTimeout(() => {
                    setIsErrorVisible(false);
                    setTimeout(() => setError(''), 300);
                  }, 5000);
                }
              }}
              style={{
                width: '100%',
                padding: '12px 16px',
                border: '1px solid #374151',
                borderRadius: '8px',
                backgroundColor: 'transparent',
                color: '#ffffff',
                fontSize: '14px',
                fontWeight: '500',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '12px',
                transition: 'all 0.2s ease',
                marginBottom: '16px'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = '#1f2937'
                e.currentTarget.style.borderColor = '#4b5563'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'transparent'
                e.currentTarget.style.borderColor = '#374151'
              }}
            >
              <svg width="18" height="18" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              Continue with Google
            </button>

            <div style={{ textAlign: 'center' }}>
              <p style={{ color: '#cccccc' }}>
                Don&apos;t have an account?{' '}
                <Link href="/signup" style={{ 
                  color: '#3b82f6', 
                  textDecoration: 'none',
                  fontWeight: '500'
                }}>
                  Sign up here
                </Link>
              </p>
            </div>
          </form>
        </div>
        </div>
      </div>
    </div>
  )
}

export default function LoginPage() {
  return (
    <Suspense fallback={<div></div>}>
      <LoginContent />
    </Suspense>
  );
}

"use client";

import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { X, User, LogOut, ChevronDown } from 'lucide-react'
import GradeInputForm from '@/components/GradeInputForm'
import RecommendationDashboard from '@/components/RecommendationDashboard'
import { AnalysisResult } from '@/types'

interface GradeAnalysisData {
  grades: Array<{ subject: string; score: number }>
  interest_text: string
  career_goals: string
}

export default function InputPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [user, setUser] = useState<{ name: string; email?: string } | null>(null)
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null)
  const [isErrorVisible, setIsErrorVisible] = useState(true)
  const [showProfileMenu, setShowProfileMenu] = useState(false)
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [isMobileFormOpen, setIsMobileFormOpen] = useState(false)
  const profileMenuRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Check if user is authenticated via cookie
    const checkAuth = async () => {
      try {
        const response = await fetch('/api/auth/me')
        const data = await response.json()
        
        if (data.user) {
          setUser(data.user)
          localStorage.removeItem('just_logged_out')
          // Don't remove just_logged_in here - let it persist
        } else {
          // Also check for cookie directly as fallback
          const cookies = document.cookie
          const hasAuthToken = cookies.includes('auth-token=')
          
          if (hasAuthToken) {
            // Cookie exists but API call failed, retry once
            setTimeout(() => {
              fetch('/api/auth/me')
                .then(res => res.json())
                .then(retryData => {
                  if (retryData.user) {
                    setUser(retryData.user)
                    localStorage.removeItem('just_logged_out')
                    // Don't set just_logged_in here - let it persist
                  } else {
                    router.push('/login')
                  }
                })
                .catch(() => router.push('/login'))
            }, 500)
          } else {
            router.push('/login')
          }
        }
      } catch (error) {
        console.error('Auth check error:', error)
        router.push('/login')
      }
    }
    
    checkAuth()
  }, [router])

  // Close profile menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (profileMenuRef.current && !profileMenuRef.current.contains(event.target as Node)) {
        setShowProfileMenu(false)
      }
    }

    if (showProfileMenu) {
      document.addEventListener('mousedown', handleClickOutside)
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [showProfileMenu])

  const handleSubmit = async (data: GradeAnalysisData) => {
    setLoading(true)
    setError(null)
    setIsErrorVisible(true)
    try {
        const response = await fetch('/api/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        })
      if (!response.ok) {
        const errorText = await response.text()
        console.error('API Error:', errorText)
        throw new Error('Failed to analyze data')
      }
      const result = await response.json()
      setAnalysisResult(result)
      sessionStorage.setItem('analysisResult', JSON.stringify(result))
      setIsMobileFormOpen(false)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      setIsErrorVisible(true)
      setTimeout(() => {
        setIsErrorVisible(false)
        setTimeout(() => setError(null), 300)
      }, 5000)
    } finally {
      setLoading(false)
    }
  }

  if (!user) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        minHeight: '100vh',
        padding: '40px 20px',
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
            filter: 'brightness(0.8)',
            zIndex: 0,
            pointerEvents: 'none'
          }}
        />
        <div style={{ position: 'relative', zIndex: 10 }}>
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '24px'
        }}>
          <svg className="logo-spin" width="80" height="80" viewBox="-30 -30 201 233" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ display: 'block' }}>
            <g>
              <path d="M110.464 0C127.032 0.000247877 140.464 13.4316 140.464 30V31.4922H92.9033V58.2891H49.9043V86.3154H0V30C0 13.4315 13.4315 1.61637e-06 30 0H110.464Z" fill="white"/>
            </g>
            <g>
              <path d="M30.5372 172.649C13.9687 172.67 0.453776 159.257 0.350835 142.689L0.341564 141.196L47.9011 141.134L47.7346 114.338L90.7336 114.282L90.5595 86.2549L140.464 86.1897L140.814 142.505C140.917 159.073 127.569 172.522 111 172.544L30.5372 172.649Z" fill="#3B82F6"/>
            </g>
          </svg>
          <img 
            src="/image/Bontor-logo.png" 
            alt="Bontor" 
            style={{ 
              height: '30px',
              width: 'auto',
              display: 'block'
            }}
          />
         
        </div>
        </div>
      </div>
    )
  }

  const handleLogout = async () => {
    // Clear cookie client-side immediately for instant UI update
    document.cookie = 'auth-token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
    // Set logout flag for instant UI update across pages
    localStorage.setItem('just_logged_out', 'true')
    localStorage.removeItem('just_logged_in') // Clear login flag
    
    await fetch('/api/auth/logout', { method: 'POST' })
    // Use window.location for a hard redirect to ensure cookie is cleared
    window.location.href = '/landing?logout=true'
  }

  return (
    <div style={{ 
      height: '100vh', 
      position: 'relative',
      display: 'flex',
      flexDirection: 'column',
      zIndex: 10
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
          filter: 'brightness(0.8)',
          pointerEvents: 'none'
        }}
      />

      {/* Header */}
      <header className="bg-white/2 backdrop-blur-md" style={{ 
        padding: '16px 0',
        position: 'sticky',
        top: 0,
        zIndex: 100
       }}>  
        
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', position: 'relative' }}>
            {/* Logo */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <button
                onClick={() => setIsMenuOpen(true)}
                className="lg:hidden p-2 hover:bg-gray-800 rounded-md transition-colors"
                style={{ background: 'transparent', border: 'none' }}
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
              <button
                onClick={() => router.push('/landing')}
                className="hover:opacity-80 transition-opacity"
                style={{ background: 'transparent', border: 'none', padding: 0}}
              >
                <img 
                  src="/image/Bontor-logo.png" 
                  alt="Bontor" 
                  className="h-5 md:h-[23px] w-auto"
                />
              </button>
            </div>

            {/* Navigation Links - Centered - Hidden on mobile */}
            <div className="hidden lg:flex items-center space-x-8" style={{ 
              position: 'absolute',
              left: '50%',
              transform: 'translateX(-50%)'
            }}>
              <button
                onClick={() => router.push('/Input')}
                className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
              >
                Analyze
              </button>
              <button
                onClick={() => router.push('/dashboard')}
                className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
              >
                Dashboard
              </button>
              <button
                onClick={() => router.push('/university')}
                className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
              >
                University
              </button>
              <button
                onClick={() => router.push('/agent')}
                className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
              >
                Agent
              </button>
            </div>

            {/* Profile Menu */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px', position: 'relative' }}>
              <div ref={profileMenuRef} style={{ position: 'relative' }}>
                <button
                  onClick={() => setShowProfileMenu(!showProfileMenu)}
                  className="flex items-center gap-2 px-3 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-md transition-colors border border-gray-600"
                  style={{ 
                    fontSize: '14px'
                  }}
                >
                  <User size={16} />
                  <span className="hidden sm:inline">{user?.name}</span>
                  <ChevronDown size={14} style={{ transform: showProfileMenu ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 0.2s' }} />
                </button>

                {/* Dropdown Menu */}
                {showProfileMenu && (
                  <div
                    style={{
                      position: 'absolute',
                      top: '100%',
                      right: 0,
                      marginTop: '8px',
                      background: '#1f2937',
                      border: '1px solid #374151',
                      borderRadius: '8px',
                      minWidth: '160px',
                      boxShadow: '0 5px 10px rgba(0, 0, 0, 0.5)',
                      zIndex: 1000,
                      overflow: 'hidden'
                    }}
                  >
                    <div style={{ padding: '8px 12px', borderBottom: '1px solid #374151' }}>
                      <p style={{ color: '#ffffff', fontSize: '14px', fontWeight: '600', margin: 0 }}>
                        {user?.name}
                      </p>
                      {user?.email && (
                        <p style={{ color: '#9ca3af', fontSize: '12px', margin: '4px 0 0 0' }}>
                          {user.email}
                        </p>
                      )}
                    </div>
                    <button
                      onClick={handleLogout}
                      className="w-full flex items-center gap-3 px-4 py-3 text-white hover:bg-gray-700 transition-colors"
                      style={{
                        fontSize: '14px',
                        background: 'transparent',
                        border: 'none',
                        cursor: 'pointer',
                        textAlign: 'left'
                      }}
                    >
                      <LogOut size={16} />
                      Logout
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Sidebar Menu */}
      {isMenuOpen && (
        <div className="fixed inset-0 z-[200] lg:hidden">
          <button
            className="absolute inset-0 bg-black/60 backdrop-blur-md"
            aria-label="Close menu"
            onClick={() => setIsMenuOpen(false)}
          />
          <aside
            className="absolute top-0 left-0 h-full w-72 max-w-[80%] text-white border-r border-white/10 shadow-2xl overflow-y-auto"
            style={{
              backgroundImage:
                "linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url(/image/Ultravib.png)",
              backgroundSize: "cover",
              backgroundPosition: "center",
            }}
          >
            {/* Header */}
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

            {/* Navigation Links */}
            <div className="flex flex-col gap-6 px-5 py-6 text-sm">
              <button
                onClick={() => {
                  router.push('/Input');
                  setIsMenuOpen(false);
                }}
                className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors"
              >
                Analyze
              </button>
              <button
                onClick={() => {
                  router.push('/dashboard');
                  setIsMenuOpen(false);
                }}
                className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors"
              >
                Dashboard
              </button>
              <button
                onClick={() => {
                  router.push('/university');
                  setIsMenuOpen(false);
                }}
                className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors"
              >
                University
              </button>
              <button
                onClick={() => {
                  router.push('/agent');
                  setIsMenuOpen(false);
                }}
                className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors"
              >
                Agent
              </button>
            </div>

            {/* User Info & Logout */}
            <div className="mt-5 px-5 pb-8">
              <div className="mb-3">
                <p className="text-white font-semibold text-sm">{user?.name}</p>
                {user?.email && (
                  <p className="text-white/60 text-xs mt-1">{user.email}</p>
                )}
              </div>
              <button
                onClick={() => {
                  handleLogout();
                  setIsMenuOpen(false);
                }}
                className="w-full justify-center px-4 py-1.5 bg-gray-800 hover:bg-gray-700 text-white rounded-md transition-colors border border-gray-600"
              >
                Logout
              </button>
            </div>
          </aside>
        </div>
      )}


        {/* Main Content */}
        <main style={{ 
          padding: '0',
          flex: 1,
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column',
          position: 'relative',
          zIndex: 10
        }}>
          {error && (
            <div style={{
              position: 'absolute',
              top: '80px',
              left: '50%',
              transform: 'translateX(-50%)',
              width: '400px',
              maxWidth: '90vw',
              zIndex: 200,
              opacity: isErrorVisible ? 1 : 0,
              transition: 'opacity 0.3s ease-out'
            }}>
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
                position: 'relative'
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
            </div>
          )}

          {/* Mobile: hero with toggleable slide-up form */}
          <div className="lg:hidden relative flex-1 overflow-hidden">
            <div
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                backgroundImage: "url(/image/Ultravib.png)",
                backgroundSize: 'cover',
                backgroundPosition: 'center center',
                backgroundRepeat: 'no-repeat',
                filter: 'brightness(0.8)',
                pointerEvents: 'none'
              }}
            />

            <div className="relative h-full flex flex-col items-center justify-center px-6 text-center" style={{ zIndex: 1 }}>
              {analysisResult ? (
                <div className="w-full space-y-6">
                  <div>
                    <h3 className="text-xl font-bold text-white mb-2">Your AI Recommendations</h3>
                    <p className="text-gray-300 text-sm">Personalized insights based on your profile</p>
                  </div>
                  <RecommendationDashboard data={analysisResult} />
                  <div className="flex gap-3">
                    <button
                      onClick={() => setAnalysisResult(null)}
                      className="flex-1 px-4 py-3 bg-gray-800 hover:bg-gray-700 text-white rounded-md border border-gray-600 transition-colors font-medium"
                    >
                      Edit inputs
                    </button>
                    <button
                      onClick={() => setIsMobileFormOpen(true)}
                      className="flex-1 px-4 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors font-medium"
                    >
                      Refine form
                    </button>
                  </div>
                </div>
              ) : (
                <div className="space-y-6">
                  <div className="w-20 h-20 flex items-center justify-center mx-auto">
                    <svg className="w-18 h-18 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold text-white">Ready for Analysis</h3>
                    <p className="text-gray-300 mt-2 text-sm leading-6">
                      Fill out the form to get your personalized academic insights recommendations.
                    </p>
                  </div>
                  <div className="flex justify-center">
                    <button
                      onClick={() => setIsMobileFormOpen(true)}
                      className="px-5 py-3 bg-gray-800 hover:bg-gray-700 border border-gray-600 text-white rounded-full text-sm font-semibold transition-colors shadow-lg"
                    >
                      Open input form
                    </button>
                  </div>
                </div>
              )}
            </div>

            <div
              className={`absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity duration-300 ${isMobileFormOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'}`}
              onClick={() => setIsMobileFormOpen(false)}
              style={{ zIndex: 50 }}
            />

            <div
              className={`absolute bottom-0 left-0 right-0 mx-auto w-full max-w-2xl bg-[#0b0b0b] border border-[#1f1f1f] rounded-t-3xl shadow-2xl transition-transform duration-300 ease-out ${isMobileFormOpen ? 'translate-y-0' : 'translate-y-[105%]'}`}
              style={{ height: '78vh', zIndex: 60 }}
            >
              <div className="overflow-y-auto px-6 pt-6 pb-8 scrollbar-hide" style={{ height: '78vh', WebkitOverflowScrolling: 'touch' }}>
                <div className="w-12 h-1.5 bg-gray-600 rounded-full mx-auto mb-4" />
                <div className="flex items-center justify-center mb-6">
                  <div className="text-center">
                    <div className="inline-flex items-center gap-2 px-3 py-2 rounded-md bg-[#1a1a1a] border border-[#2a2a2a]">
                      <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                      <span className="text-sm text-gray-400">Academic Profile Analysis</span>
                    </div>
                  </div>
                </div>
                <GradeInputForm onSubmit={handleSubmit} loading={loading} />
              </div>
            </div>
          </div>

          {/* Desktop: two-column stays familiar */}
          <div className="hidden lg:grid lg:grid-cols-2 gap-0" style={{ flex: 1, height: '100%' }}>
            <div 
              className="h-full overflow-y-auto relative"
              style={{
                position: 'relative'
              }}
            >
              <div
                style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  right: 0,
                  bottom: 0,
                  backgroundImage: "url(/image/Ultravib.png)",
                  backgroundSize: 'cover',
                  backgroundPosition: 'center center',
                  backgroundRepeat: 'no-repeat',
                  filter: 'brightness(0.8)',
                  zIndex: 0,
                  pointerEvents: 'none'
                }}
              />
              <div style={{ position: 'relative', zIndex: 10, height: '100%' }}>
              {analysisResult ? (
                <div className="p-8">
                  <div className="mb-6 text-center">
                    <h3 className="text-xl font-bold text-white mb-2">
                      Your AI Recommendations
                    </h3>
                    <p className="text-gray-300">
                      Personalized insights based on your profile
                    </p>
                  </div>
                  <RecommendationDashboard data={analysisResult} />
                </div>
              ) : (
                <div className="flex items-center justify-center h-full p-8">
                  <div className="text-center">
                    <div className="w-20 h-20  flex items-center justify-center mx-auto mb-2 ">
                      <svg className="w-18 h-18 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                    <h3 className="text-xl font-semibold text-white mb-2">
                      Ready for Analysis
                    </h3>
                    <p className="text-gray-200 max-w-sm mt-2">
                      Fill out the form on the right to get your personalized academic insights recommendations.
                    </p>
                  </div>
                </div>
              )}
              </div>
            </div>

            <div className="bg-[#111111] border-l border-[#1f1f1f] min-h-full overflow-y-auto">
              <div className="p-8">
                <div className="mb-8 text-center">
                   <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-md bg-[#1a1a1a] border border-[#2a2a2a] mb-6">
                     <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                       <span className="text-sm text-gray-500">Academic Profile Analysis</span>
                     </div>
                  <p className="text-gray-300">
                    Enter your BacII grades and interests to get personalized recommendations
                  </p>
                </div>
                
                <GradeInputForm onSubmit={handleSubmit} loading={loading} />
              </div>
            </div>
          </div>
        </main>
    </div>
  )
}
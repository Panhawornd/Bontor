"use client";

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { X } from 'lucide-react'
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

  useEffect(() => {
    // Check if user is authenticated via cookie
    const checkAuth = async () => {
      try {
        const response = await fetch('/api/auth/me')
        const data = await response.json()
        
        if (data.user) {
          setUser(data.user)
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

  const handleSubmit = async (data: GradeAnalysisData) => {
    setLoading(true)
    setError(null)
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
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
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
        background: "radial-gradient(ellipse 80% 60% at 50% 50%, #2d3748 0%, #1a202c 30%, #0f1419 60%, #000000 100%)",
        padding: '40px 20px'
      }}>
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
          <h2 style={{
            fontSize: '24px',
            fontWeight: '600',
            margin: 0,
            textAlign: 'center',
            color: 'var(--text-primary)'
          }}>
            Loading Your Profile...
          </h2>
          <p style={{
            fontSize: '16px',
            color: 'var(--text-secondary)',
            margin: 0,
            textAlign: 'center',
            maxWidth: '400px'
          }}>
            Our AI is processing your grades and preferences to provide personalized recommendations.
          </p>
        </div>
      </div>
    )
  }

  const handleLogout = async () => {
    await fetch('/api/auth/logout', { method: 'POST' })
    // Use window.location for a hard redirect to ensure cookie is cleared
    window.location.href = '/landing'
  }

  return (
    <div style={{ 
      height: '100vh', 
      background: "radial-gradient(ellipse 80% 60% at 50% 50%, #2d3748 0%, #1a202c 30%, #0f1419 60%, #000000 100%)",
      position: 'relative',
      display: 'flex',
      flexDirection: 'column'
    }}>

      {/* Header */}
      <header style={{ 
        background: 'transparent',  
        padding: '16px 0',
        position: 'sticky',
        top: 0,
        zIndex: 100,
        backdropFilter: 'blur(20px)'
      }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <img 
                src="/image/Bontor-logo.png" 
                alt="Bontor" 
                style={{ 
                  height: '23px',
                  width: 'auto'
                }}
              />
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
              <span style={{ 
                color: 'var(--text-secondary)',
                fontSize: '14px'
              }}>
                Welcome, {user?.name}!
              </span>
              <button 
                onClick={handleLogout}
                className="px-4 py-1.5 bg-gray-800 hover:bg-gray-700 text-white rounded-md transition-colors border border-gray-600"
                style={{ 
                  fontSize: '14px'
                }}
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>


        {/* Main Content */}
        <main style={{ 
          padding: '0',
          flex: 1,
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column'
        }}>
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
              position: 'absolute',
              top: '20px',
              left: '20px',
              right: '20px',
              zIndex: 10
            }}>
              <div style={{
                width: '20px',
                height: '20px',
                borderRadius: '50%',
                background: 'var(--accent-error)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white'
              }}>
                <X size={12} />
              </div>
              <span>{error}</span>
            </div>
          )}

          {/* Two Column Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-0" style={{ flex: 1, height: '100%' }}>
            {/* Left Column - Recommendations (landing gradient) - Hidden on mobile until analysis */}
            <div 
              className={`min-h-full overflow-y-auto ${analysisResult ? 'block' : 'hidden lg:block'}`}
              style={{
                background: "radial-gradient(ellipse 80% 60% at 50% 50%, #2d3748 0%, #1a202c 30%, #0f1419 60%, #000000 100%)"
              }}
            >
              {analysisResult ? (
                <div className="p-6">
                  <div className="mb-6 text-center">
                    <h3 className="text-xl font-bold text-white mb-2">
                      Your AI Recommendations
                    </h3>
                    <p className="text-gray-300">
                      Personalized insights based on your profile
                    </p>
                  </div>
                  <RecommendationDashboard data={analysisResult} />
                  <button 
                    onClick={() => setAnalysisResult(null)}
                    className="lg:hidden mt-8 w-full px-4 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors font-medium"
                  >
                    Back to Input Form
                  </button>
                </div>
              ) : (
                <div className="flex items-center justify-center h-full p-6">
                  <div className="text-center">
                    <div className="w-20 h-20  flex items-center justify-center mx-auto mb-2 ">
                      <svg className="w-18 h-18 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                    <h3 className="text-xl font-semibold text-white mb-2">
                      Ready for Analysis
                    </h3>
                    <p className="text-gray-300 max-w-sm mt-2">
                      Fill out the form on the right to get your personalized career recommendations and academic insights.
                    </p>
                  </div>
                </div>
              )}
            </div>

            {/* Right Column - Input Form - Hidden on mobile after analysis */}
            <div className={`bg-[#111111] border-l border-[#1f1f1f] min-h-full overflow-y-auto ${analysisResult ? 'hidden lg:block' : 'block'}`}>
              <div className="p-8">
                <div className="mb-8 text-center">
                  <h3 className="text-xl font-bold text-white mb-2">
                    Academic Profile Analysis
                  </h3>
                  <p className="text-gray-300">
                    Enter your grades and interests to get personalized recommendations
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
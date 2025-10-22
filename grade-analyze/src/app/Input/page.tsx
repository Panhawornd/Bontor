"use client";

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { X } from 'lucide-react'
import GradeInputForm from '@/components/GradeInputForm'

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
      sessionStorage.setItem('analysisResult', JSON.stringify(result))
      router.push('/results')
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
        background: 'var(--bg-primary)',
        padding: '40px 20px'
      }}>
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '24px'
        }}>
          <div style={{
            width: '48px',
            height: '48px',
            border: '4px solid rgba(255,255,255,0.1)',
            borderTop: '4px solid #3b82f6',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite'
          }} />
          <h2 style={{
            fontSize: '24px',
            fontWeight: '600',
            margin: 0,
            textAlign: 'center',
            color: 'var(--text-primary)'
          }}>
            Analyzing Your Profile...
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
      minHeight: '100vh', 
      background: 'linear-gradient(135deg, #000000 0%, #0a0a0a 25%, #1a1a1a 50%, #0a0a0a 75%, #000000 100%)',
      position: 'relative'
    }}>
      {/* Animated background */}
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: `
          radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.05) 0%, transparent 50%),
          radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.03) 0%, transparent 50%),
          radial-gradient(circle at 40% 80%, rgba(255, 255, 255, 0.02) 0%, transparent 50%)
        `,
        zIndex: -1
      }} />

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

      {/* Hero Section */}
      <section style={{ 
        padding: '80px 24px',
        textAlign: 'center',
        position: 'relative'
      }}>
        <div style={{ maxWidth: '800px', margin: '0 auto' }}>
          <h2 style={{ 
            fontSize: 'clamp(2rem, 4vw, 3rem)', 
            fontWeight: '700', 
            marginBottom: '24px',
            background: 'var(--gradient-primary)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            lineHeight: 1.5
          }}>
            AI-Powered Career Intelligence
          </h2>
          <p style={{ 
            fontSize: '20px', 
            color: 'var(--text-secondary)', 
            marginBottom: '12px',
            fontWeight: '500'
          }}>
            Cambodian BacII Edition
          </p>
          <p style={{ 
            color: 'var(--text-muted)', 
            fontSize: '18px',
            lineHeight: 1.6,
            maxWidth: '600px',
            margin: '0 auto'
          }}>
            Discover your ideal majors, careers, and universities with advanced AI analysis of your academic profile and interests.
          </p>
        </div>
      </section>

      {/* Main Content */}
      <main style={{ 
        maxWidth: '1200px', 
        margin: '0 auto', 
        padding: '0 24px 80px'
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
          gap: '12px'
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

        <div className="card" style={{
          background: 'var(--bg-secondary)',
          border: '1px solid var(--border-primary)',
          borderRadius: '16px',
          padding: '40px',
          boxShadow: 'var(--shadow-primary)',
          position: 'relative',
          overflow: 'hidden'
        }}>
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: '4px',
            background: 'var(--gradient-primary)'
          }} />
          
          <div style={{ marginBottom: '32px', textAlign: 'center' }}>
            <h3 style={{ 
              fontSize: '24px', 
              fontWeight: '600', 
              marginBottom: '8px',
              color: 'var(--text-primary)'
            }}>
              Analyze Your Academic Profile
            </h3>
            <p style={{ 
              color: 'var(--text-secondary)',
              fontSize: '16px'
            }}>
              Enter your grades and interests to get personalized recommendations
            </p>
          </div>

          <GradeInputForm onSubmit={handleSubmit} loading={loading} />
        </div>
      </main>
    </div>
  )
}
"use client";

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { X } from 'lucide-react'
import RecommendationDashboard from '@/components/RecommendationDashboard'
import { AnalysisResult } from '@/types'

export default function Results() {
  const router = useRouter()
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const storedResult = sessionStorage.getItem('analysisResult')
    
    if (storedResult) {
      try {
        const parsedResult = JSON.parse(storedResult)
        setResult(parsedResult)
      } catch (error) {
        console.error('Error parsing stored result:', error)
        setResult(null)
      }
    } else {
      setResult(null)
    }
    setIsLoading(false)
  }, [router])

  if (isLoading) {
    return (
      <div style={{ 
        minHeight: '100vh', 
        background: "radial-gradient(ellipse 80% 60% at 50% 50%, #2d3748 0%, #1a202c 30%, #0f1419 60%, #000000 100%)",
        color: 'var(--text-primary)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
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
            textAlign: 'center'
          }}>
            Loading Results...
          </h2>
          <p style={{
            fontSize: '16px',
            color: 'var(--text-secondary)',
            margin: 0,
            textAlign: 'center',
            maxWidth: '400px'
          }}>
            Please wait while we load your analysis results.
          </p>
        </div>
      </div>
    )
  }

  if (!result) {
    return (
      <div style={{ 
        minHeight: '100vh', 
        background: 'var(--bg-primary)',
        color: 'var(--text-primary)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '40px 20px',
        position: 'relative'
      }}>
        {/* Animated background */}
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: `
            radial-gradient(ellipse 80% 60% at 50% 50%, #2d3748 0%, #1a202c 30%, #0f1419 60%, #000000 100%)
          `,
          zIndex: -1
        }} />

        <div style={{
          background: 'var(--bg-secondary)',
          border: '1px solid var(--border-primary)',
          borderRadius: '16px',
          padding: '40px',
          textAlign: 'center',
          maxWidth: '500px',
          boxShadow: 'var(--shadow-primary)'
        }}>
          <div style={{
            width: '48px',
            height: '48px',
            borderRadius: '50%',
            background: 'var(--accent-error)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            margin: '0 auto 20px'
          }}>
            <X size={24} />
          </div>
          <h1 style={{ 
            fontSize: '24px', 
            fontWeight: '600',
            marginBottom: '16px',
            color: 'var(--text-primary)'
          }}>
            No Analysis Results Found
          </h1>
          <p style={{ 
            color: 'var(--text-secondary)', 
            marginBottom: '32px',
            lineHeight: 1.6
          }}>
            It looks like the analysis results were not saved properly. Please try analyzing again.
          </p>
            <button 
              onClick={() => router.push('/Input')}
              className="px-4 py-1.5 bg-gray-800 hover:bg-gray-700 text-white rounded-md transition-colors border border-gray-600"
              style={{
                fontSize: '16px',
                fontWeight: '500'
              }}
            >
              Go Back to Analysis
            </button>
        </div>
      </div>
    )
  }

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: "radial-gradient(ellipse 80% 60% at 50% 50%, #2d3748 0%, #1a202c 30%, #0f1419 60%, #000000 100%)",
      color: 'var(--text-primary)',
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
            <button 
              onClick={() => router.push('/Input')} 
              className="px-4 py-1.5 bg-gray-800 hover:bg-gray-700 text-white rounded-md transition-colors border border-gray-600"
              style={{
                fontSize: '14px'
              }}
            >
              Back to Analysis
            </button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section style={{ 
        padding: '60px 24px 40px',
        textAlign: 'center',
        position: 'relative'
      }}>
        <div style={{ maxWidth: '800px', margin: '0 auto' }}>
          <h2 style={{ 
            fontSize: 'clamp(2rem, 4vw, 3rem)', 
            fontWeight: '700', 
            marginBottom: '16px',
            background: 'var(--gradient-primary)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            lineHeight: 1.2
          }}>
            Your AI-Generated Career Path
          </h2>
          <p style={{ 
            color: 'var(--text-secondary)', 
            fontSize: '18px',
            lineHeight: 1.6,
            maxWidth: '600px',
            margin: '0 auto'
          }}>
            Based on your academic profile and interests, here are your personalized recommendations
          </p>
        </div>
      </section>

      {/* Main Content */}
      <main style={{ 
        maxWidth: '1200px', 
        margin: '0 auto', 
        padding: '0 24px 80px'
      }}>
        <RecommendationDashboard data={result} />
      </main>
    </div>
  )
}

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
        color: 'var(--text-primary)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
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
            filter: 'brightness(0.3)',
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
      </div>
    )
  }

  if (!result) {
    return (
      <div style={{ 
        minHeight: '100vh', 
        color: 'var(--text-primary)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
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
            filter: 'brightness(0.3)',
            zIndex: 0,
            pointerEvents: 'none'
          }}
        />

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
      color: 'var(--text-primary)',
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
          filter: 'brightness(0.3)',
          zIndex: 0,
          pointerEvents: 'none'
        }}
      />

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

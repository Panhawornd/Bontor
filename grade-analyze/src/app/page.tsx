"use client";

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function Home() {
  const router = useRouter()

  useEffect(() => {
    // Check if user is authenticated via cookie
    const cookies = document.cookie
    const hasAuthToken = cookies.includes('auth-token=')
    
    if (hasAuthToken) {
      // Redirect authenticated users to input form
      router.push('/Input')
    } else {
      // Redirect non-authenticated users to landing page
      router.push('/landing')
    }
  }, [router])

  // Show loading while redirecting
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
          Loading...
        </h2>
        <p style={{
          fontSize: '16px',
          color: 'var(--text-secondary)',
          margin: 0,
          textAlign: 'center',
          maxWidth: '400px'
        }}>
        </p>
      </div>
    </div>
  )
}

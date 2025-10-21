"use client";

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Button from '@/components/ui/Button'
import Input from '@/components/ui/Input'
import Card from '@/components/ui/Card'
import Link from 'next/link'

export default function Login() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        // Use window.location for a hard redirect to ensure cookie is available
        window.location.href = '/Input'
      } else {
        const data = await response.json()
        setError(data.error || 'Login failed')
      }
    } catch (err) {
      setError('Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: 'linear-gradient(135deg, #000000 0%, #0a0a0a 25%, #1a1a1a 50%, #0a0a0a 75%, #000000 100%)',
      color: '#ffffff'
    }}>
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-transparent backdrop-blur-md min-h-[4rem]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center">
              <button
                onClick={() => {
                  console.log('Logo clicked - navigating to landing')
                  window.location.href = '/landing'
                }}
                className="hover:opacity-80 transition-opacity"
              >
                <img 
                  src="/image/Bontor-logo.png" 
                  alt="Bontor" 
                  style={{ 
                    height: '40px',
                    width: 'auto'
                  }}
                />
              </button>
            </div>

            {/* Navigation Links */}
            <div className="flex items-center space-x-4 md:space-x-8">
                <button
                  onClick={() => {
                    console.log('Home clicked - navigating to landing')
                    console.log('Router object:', router)
                    window.location.href = '/landing'
                  }}
                  className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
                >
                  Home
                </button>
                <button
                  onClick={() => {
                    console.log('How it Works clicked - navigating to how-it-works')
                    window.location.href = '/how-it-works'
                  }}
                  className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
                >
                  How it Works
                </button>
                <button
                  onClick={() => {
                    console.log('About clicked - navigating to about')
                    window.location.href = '/about'
                  }}
                  className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
                >
                  About
                </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        padding: '16px',
        paddingTop: '80px' // Account for fixed navigation
      }}>
        <div style={{ width: '100%', maxWidth: '400px' }}>
          <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <h1 style={{ 
            fontSize: '36px', 
            fontWeight: 'bold', 
            marginBottom: '8px',
            color: '#ffffff'
          }}>
            Welcome Back
          </h1>
          <p style={{ color: '#cccccc' }}>Sign in to your account to continue</p>
        </div>

        <div style={{
          backgroundColor: '#111111',
          border: '1px solid #333333',
          borderRadius: '8px',
          padding: '32px'
        }}>
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            {error && (
              <div style={{
                padding: '16px',
                backgroundColor: '#1a1111',
                border: '1px solid #666666',
                borderRadius: '8px',
                color: '#ffffff',
                fontSize: '14px'
              }}>
                {error}
              </div>
            )}

            <div>
              <label style={{ 
                display: 'block', 
                marginBottom: '8px', 
                color: '#ffffff',
                fontWeight: '500'
              }}>
                Email Address
              </label>
              <input
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                placeholder="Enter your email"
                className="input-field"
              />
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
              {loading ? 'Signing in...' : 'Sign In'}
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

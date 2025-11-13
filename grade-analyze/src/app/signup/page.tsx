"use client";

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Button from '@/components/ui/Button'
import Input from '@/components/ui/Input'
import Card from '@/components/ui/Card'
import Link from 'next/link'

export default function Signup() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [isErrorVisible, setIsErrorVisible] = useState(true)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setIsErrorVisible(true)

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match')
      setIsErrorVisible(true)
      setTimeout(() => {
        setIsErrorVisible(false)
        setTimeout(() => setError(''), 300)
      }, 5000)
      setLoading(false)
      return
    }

    try {
      const response = await fetch('/api/auth/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: formData.name,
          email: formData.email,
          password: formData.password
        }),
      })

      if (response.ok) {
        router.push('/input?message=Account created successfully')
      } else {
        const data = await response.json()
        setError(data.error || 'Signup failed')
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
          filter: 'brightness(0.3)',
          zIndex: 0,
          pointerEvents: 'none'
        }}
      />
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
                    height: '23px',
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
        paddingTop: '80px', // Account for fixed navigation
        position: 'relative',
        zIndex: 10
      }}>
        <div style={{ width: '100%', maxWidth: '400px' }}>
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <h1 style={{ 
            fontSize: '36px', 
            fontWeight: 'bold', 
            marginBottom: '8px',
            color: '#ffffff'
          }}>
            Create Account
          </h1>
          <p style={{ color: '#cccccc' }}>Join us to start your career journey</p>
        </div>

        <div className="bg-[#111111] border border-[#1f1f1f] rounded-lg p-8 hover:border-[#2a2a2a] transition-colors">
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            {error && (
              <div style={{
                padding: '16px',
                backgroundColor: '#1a1111',
                border: '1px solid #666666',
                borderRadius: '8px',
                color: '#ffffff',
                fontSize: '14px',
                opacity: isErrorVisible ? 1 : 0,
                transition: 'opacity 0.3s ease-out'
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
                Full Name
              </label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="Enter your full name"
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
                placeholder="Create a password"
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
                Confirm Password
              </label>
              <input
                type="password"
                required
                value={formData.confirmPassword}
                onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                placeholder="Confirm your password"
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
                  Creating Account...
                </span>
              ) : 'Create Account'}
            </button>

            <div style={{ textAlign: 'center' }}>
              <p style={{ color: '#cccccc' }}>
                Already have an account?{' '}
                <Link href="/login" style={{ 
                  color: '#3b82f6', 
                  textDecoration: 'none',
                  fontWeight: '500'
                }}>
                  Sign in here
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

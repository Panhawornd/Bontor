"use client";

import { useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'
import Button from "@/components/ui/Button";
import Reveal from "@/components/Reveal";
import { Brain, TrendingUp, Target, Shield, CheckCircle2, BarChart3, Globe, Zap, ArrowRight, Award } from "lucide-react";
import Lottie from "lottie-react";
import InfiniteScroll from "@/components/InfiniteScroll";

export default function LandingPage() {
  const router = useRouter()
  const [aiAnimation, setAiAnimation] = useState(null)
  const [bacIIAnimation, setBacIIAnimation] = useState(null)
  const [nextStepAnimation, setNextStepAnimation] = useState(null)
  const [securityAnimation, setSecurityAnimation] = useState(null)
  const [subjectAnalysisAnimation, setSubjectAnalysisAnimation] = useState(null)
  const [recommendationEngineAnimation, setRecommendationEngineAnimation] = useState(null)
  const [skillDevelopmentAnimation, setSkillDevelopmentAnimation] = useState(null)
  const [cambodiaAnimation, setCambodiaAnimation] = useState(null)
  const [hasToken, setHasToken] = useState<boolean | null>(null)

  useEffect(() => {
    // Check if user has auth token cookie
    const cookies = document.cookie
    const hasAuthToken = cookies.includes('auth-token=')
    
    if (hasAuthToken) {
      setHasToken(true)
    } else {
      setHasToken(false)
    }

    // Load Lottie animations
    fetch('/lottie/AI.json')
      .then(res => res.json())
      .then(data => setAiAnimation(data))
      .catch(err => console.error('Failed to load AI animation:', err))

    fetch('/lottie/BacII-student.json')
      .then(res => res.json())
      .then(data => setBacIIAnimation(data))
      .catch(err => console.error('Failed to load BacII animation:', err))

    fetch('/lottie/Next-step.json')
      .then(res => res.json())
      .then(data => setNextStepAnimation(data))
      .catch(err => console.error('Failed to load NextStep animation:', err))

    fetch('/lottie/Security.json')
      .then(res => res.json())
      .then(data => setSecurityAnimation(data))
      .catch(err => console.error('Failed to load Security animation:', err))

    fetch('/lottie/Subject-analysis.json')
      .then(res => res.json())
      .then(data => setSubjectAnalysisAnimation(data))
      .catch(err => console.error('Failed to load Subject-analysis animation:', err))

    fetch('/lottie/Recommendation-engine.json')
      .then(res => res.json())
      .then(data => setRecommendationEngineAnimation(data))
      .catch(err => console.error('Failed to load Recommendation-engine animation:', err))

    fetch('/lottie/Skill-development.json')
      .then(res => res.json())
      .then(data => setSkillDevelopmentAnimation(data))
      .catch(err => console.error('Failed to load Skill-development animation:', err))

    fetch('/lottie/Cambodia.json')
      .then(res => res.json())
      .then(data => setCambodiaAnimation(data))
      .catch(err => console.error('Failed to load Cambodia animation:', err))
  }, [])

  const handleGetStarted = () => {
    router.push('/login')
  }

  return (
    <div className="min-h-screen bg-black relative overflow-hidden">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-transparent backdrop-blur-md min-h-[4rem]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-center h-16 relative">
            {/* Logo */}
            <div className="absolute left-0 flex items-center">
              <button
                onClick={() => router.push('/landing')}
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

            {/* Desktop Navigation - Centered */}
            <div className="hidden md:block">
              <div className="flex items-baseline space-x-8">
                <button
                  onClick={() => router.push('/landing')}
                  className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
                >
                  Home
                </button>
                <button
                  onClick={() => router.push('/how-it-works')}
                  className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
                >
                  How it Works
                </button>
                <button
                  onClick={() => router.push('/about')}
                  className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
                >
                  About
                </button>
              </div>
            </div>

            {/* Get Started/Analyze Button */}
            <div className="absolute right-0 hidden md:block">
              <Button
                onClick={hasToken ? () => router.push('/Input') : handleGetStarted}
                className="px-4 py-1.5 bg-gray-800 hover:bg-gray-700 text-white rounded-md transition-colors border border-gray-600"
              >
                {hasToken ? 'Start Analysis' : 'Get Started'}
              </Button>
            </div>
          </div>
        </div>
      </nav>

      
      
      {/* Subtle Gradient Orbs */}
      <div className="absolute top-0 left-1/4 w-[500px] h-[500px] bg-blue-500/5 rounded-full mix-blend-lighten filter blur-3xl" />
      <div className="absolute top-1/3 right-1/4 w-[500px] h-[500px] bg-blue-400/5 rounded-full mix-blend-lighten filter blur-3xl" />
      
      {/* Hero Section */}
      <section className="relative">
        {/* Background Image - only hero text height */}
        <div
          className="absolute inset-x-0 top-15 bg-cover bg-center bg-no-repeat bg-black"
          style={{ 
            backgroundImage: "url(/image/Herosection.jpg)",
            height: "calc(82vh - 80px)"
          }}
        />
        {/* Dark overlay matched to height */}
        <div
          className="absolute inset-x-0 top-0 bg-black/70"
          style={{ height: "calc(82vh - 80px)" }}
        />
        <div className="max-w-7xl mx-auto px-6 pt-32 pb-24 relative z-10">
          <div className="text-center max-w-5xl mx-auto" style={{ perspective: '1000px' }}>
            <Reveal
              className="inline-flex items-center gap-2 px-3 py-1.5 rounded-md bg-[#1a1a1a] border border-[#2a2a2a] mb-8"
              rootMargin="-100px"
              threshold={0.2}
            >
              <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
              <span className="text-sm text-gray-400">
                AI-Powered Career Guidance for Cambodian Students
              </span>
            </Reveal>
            
            <Reveal rootMargin="-100px" threshold={0.2}>
              <h1
                className="text-6xl md:text-8xl text-white tracking-tight leading-none"
                style={{ marginBottom: '3rem' }}
              >
                Your future starts
                <br />
                <span className="text-white">with insight</span>
              </h1>
            </Reveal>
            
            <Reveal
              className="text-xl md:text-2xl text-gray-500 mb-12 max-w-3xl mx-auto leading-relaxed"
              rootMargin="-100px"
              threshold={0.2}
            >
              Transform your BacII grades into a personalized roadmap. Discover your ideal major, career path, and university powered by AI.
            </Reveal>
            
            <Reveal
              className="flex justify-center items-center"
              rootMargin="-100px"
              threshold={0.2}
            >
              <Button
                onClick={hasToken ? () => router.push('/Input') : handleGetStarted}
                size="lg"
                className="group px-6 py-3 rounded-lg bg-gray-800 hover:bg-gray-700 text-white transition-colors"
              >
                {hasToken ? 'Start Analysis' : 'Get Started'}
                <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
              </Button>
            </Reveal>
          </div>
          
          {/* Hero Visual - Bento Grid */}
          <div className="mt-24 relative" style={{ perspective: '1000px' }}>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 max-w-6xl mx-auto">
              {/* Large Card */}
              <Reveal
                className="md:col-span-2 relative rounded-lg bg-[#111111] border border-[#1f1f1f] p-8 overflow-hidden group hover:border-[#2a2a2a] transition-colors"
                rootMargin="-100px"
                threshold={0.2}
              >
                <div className="relative">
                  <div className="flex items-center gap-3 mb-6">
                    <div className="w-10 h-10 rounded-lg bg-[#1a1a1a] border border-[#2a2a2a] flex items-center justify-center">
                      <Brain className="w-5 h-5 text-blue-500" />
                    </div>
                    <div>
                      <h3 className="text-white">AI Analysis Engine</h3>
                      <p className="text-sm text-gray-500">Personalized recommendations</p>
                    </div>
                  </div>
                  <div className="space-y-3">
                    {[
                      { value: 94, label: 'Recommendation Accuracy' },
                      { value: 92, label: 'User Satisfaction' },
                      { value: 95, label: 'University Match Success' }
                    ].map((item, i) => (
                      <div key={i}>
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-xs text-gray-400">{item.label}</span>
                          <span className="text-sm text-gray-500 w-12 text-right">{item.value}%</span>
                        </div>
                        <div className="flex-1 h-1.5 bg-[#1a1a1a] rounded-full overflow-hidden">
                          <div
                            className="h-full bg-blue-500 progress-bar-smooth"
                            style={{
                              '--target-width': `${item.value}%`,
                              width: '0%',
                              animation: `progressFill 1.2s cubic-bezier(0.4, 0, 0.2, 1) ${0.6+ i * 0.15}s forwards`,
                              transformOrigin: 'left',
                              willChange: 'width'
                            } as React.CSSProperties & { '--target-width': string }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </Reveal>

              {/* Small Card 1 */}
              <Reveal
                className="relative rounded-lg bg-[#111111] border border-[#1f1f1f] p-8 overflow-hidden group hover:border-[#2a2a2a] transition-colors"
                rootMargin="-100px"
                threshold={0.2}
              >
                <div className="relative">
                        <Zap className="w-8 h-8 text-blue-500 mb-4" />
                  <h4 className="text-white" style={{ marginBottom: '1rem' }}>Instant Insights</h4>
                  <p className="text-sm text-gray-500">Real-time analysis in seconds upload your grades and instantly see trends, strengths, and next‑step recommendations. Get subject-level breakdowns, targeted improvement tips, and suggested majors without waiting.</p>
                </div>
              </Reveal>

              {/* Small Card 2 */}
              <Reveal
                className="relative rounded-lg bg-[#111111] border border-[#1f1f1f] p-8 overflow-hidden group hover:border-[#2a2a2a] transition-colors"
                rootMargin="-100px"
                threshold={0.2}
              >
                <div className="relative">
                        <Target className="w-8 h-8 text-blue-500 mb-4" />
                  <h4 className="text-white" style={{ marginBottom: '1rem' }}>92% Accuracy</h4>
                  <p className="text-sm text-gray-500">Average match rate</p>
                </div>
              </Reveal>

              {/* Wide Card */}
              <Reveal
                className="md:col-span-2 relative rounded-lg bg-[#111111] border border-[#1f1f1f] p-8 overflow-hidden group hover:border-[#2a2a2a] transition-colors"
                rootMargin="-100px"
                threshold={0.2}
              >
                <div className="relative h-full flex items-center justify-center">
                  <div className="grid grid-cols-3 gap-25 justify-items-center">
                    {[
                      { name: 'Mathematics', icon: BarChart3 },
                      { name: 'Sciences', icon: Globe },
                      { name: 'Languages', icon: CheckCircle2 }
                    ].map((subject, i) => (
                      <div key={i} className="text-center flex flex-col items-center">
                        <div className="w-14 h-14 rounded-lg bg-[#1a1a1a] border border-[#2a2a2a] flex items-center justify-center mb-3">
                          <subject.icon className="w-6 h-6 text-gray-600" />
                        </div>
                        <p className="text-sm text-gray-500">{subject.name}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </Reveal>
            </div>
          </div>
        </div>
      </section>

      
      

      {/* Dark gradient background from hero to footer */}
      <div
        className="absolute inset-x-0"
        style={{ 
          top: "calc(82vh - 80px)",
          bottom: 0,
          background: "radial-gradient(ellipse 80% 60% at 50% 50%, #2d3748 0%, #1a202c 30%, #0f1419 60%, #000000 100%)"
        }}
      />

      {/* Key Benefits */}
      <section className="py-32 relative">
        <div className="max-w-7xl mx-auto px-6 relative z-10">
          <Reveal className="text-center mb-20">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-md bg-[#1a1a1a] border border-[#2a2a2a] mb-6">
              <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
              <span className="text-sm text-gray-500">Features</span>
            </div>
            <h2 className="text-5xl md:text-6xl text-white" style={{ marginBottom: '2rem' }}>
              Everything you need
            </h2>
            <p className="text-gray-500 text-xl max-w-2xl mx-auto">
              Built specifically for Cambodian BacII students with cutting-edge AI technology
            </p>
          </Reveal>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
            {[
              {
                icon: Brain,
                title: "AI-Powered Insights",
                description: "Personalized majors, careers, and universities tailored to your profile",
                lottie: aiAnimation
              },
              {
                icon: TrendingUp,
                title: "Built for BacII",
                description: "Subject max scores, normalization, and Cambodian educational context",
                lottie: bacIIAnimation
              },
              {
                icon: Target,
                title: "Actionable Next Steps",
                description: "Clear skill gaps and how to improve with specific suggestions",
                lottie: nextStepAnimation
              },
              {
                icon: Shield,
                title: "Private & Secure",
                description: "Your data, your control. All analysis happens locally",
                lottie: securityAnimation
              }
            ].map((benefit, idx) => (
              <Reveal
                key={idx}
                translateY={true}
                delay={idx * 100}
                className="group"
              >
                <div className="relative h-full p-6 rounded-lg bg-[#111111] border border-[#1f1f1f] hover:border-[#2a2a2a] transition-colors overflow-hidden">
                  <div className="relative flex flex-col h-full">
                    <div className="w-10 h-10 rounded-lg bg-[#1a1a1a] border border-[#2a2a2a] flex items-center justify-center mb-4">
                      <benefit.icon className="w-5 h-5 text-blue-500" />
                    </div>
                    <h3 className="text-white" style={{ marginBottom: '1rem' }}>{benefit.title}</h3>
                    <p className="text-gray-500 text-sm leading-relaxed mb-4">{benefit.description}</p>
                    {benefit.lottie && (
                      <div className="mt-auto flex justify-center items-center">
                        <Lottie 
                          animationData={benefit.lottie}
                          loop={true}
                          autoplay={true}
                          style={{ width: '100%', maxWidth: 300, height: 'auto' }}
                        />
                      </div>
                    )}
                  </div>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      

      {/* Three Steps Process */}
      <section className="py-32 relative">
        <div className="max-w-7xl mx-auto px-6 relative">
          <Reveal className="text-center mb-20">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-md bg-[#1a1a1a] border border-[#2a2a2a] mb-6">
              <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
              <span className="text-sm text-gray-500">Simple Process</span>
            </div>
            <h2 className="text-5xl md:text-6xl text-white" style={{ marginBottom: '2rem' }}>
              Three steps to clarity
            </h2>
            <p className="text-gray-500 text-xl max-w-2xl mx-auto">
              From grades to guidance in minutes
            </p>
          </Reveal>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 relative">
            {/* Connecting Line */}
            <div className="hidden md:block absolute top-16 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[rgba(179,179,179,0.3)] to-transparent" />
            
            {[
              {
                step: "01",
                title: "Enter Your Grades",
                description: "Input your BacII exam results and tell us about your interests and goals",
                icon: BarChart3
              },
              {
                step: "02",
                title: "AI Analysis",
                description: "Our AI analyzes your strengths, preferences, and career aspirations",
                icon: Brain
              },
              {
                step: "03",
                title: "Get Recommendations",
                description: "Receive personalized majors, careers, and universities with skill-gap guidance",
                icon: Target
              }
            ].map((step, idx) => (
              <Reveal
                key={idx}
                translateY={true}
                delay={idx * 200}
                className="relative"
              >
                <div className="relative p-6 rounded-lg bg-[#111111] border border-[#1f1f1f] hover:border-[#2a2a2a] transition-colors group">
                  {/* Step Number */}
                  <div className="relative flex items-center justify-center w-12 h-12 mb-6 rounded-lg bg-[#1a1a1a] border border-[#2a2a2a]">
                    <span className="text-lg text-gray-600">
                      {step.step}
                    </span>
                  </div>
                  
                  {/* Icon */}
                  <div className="w-10 h-10 rounded-lg bg-blue-600/10 border border-blue-600/20 flex items-center justify-center mb-6">
                    <step.icon className="w-5 h-5 text-blue-500" />
                  </div>
                  
                  <h3 className="text-white" style={{ marginBottom: '1rem' }}>{step.title}</h3>
                  <p className="text-gray-500 text-sm leading-relaxed">{step.description}</p>
                  {/* Image in bordered container */}
                  <div className="mt-4 h-80 rounded-lg border border-[#2a2a2a] bg-transparent overflow-hidden">
                    <div className="w-full h-full flex items-center justify-center text-gray-500 text-sm">
                      {`Image ${idx + 1}`}
                    </div>
                  </div>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      

      {/* Feature Highlights - Bento Grid */}
      <section className="py-32 relative">
        <div className="max-w-7xl mx-auto px-6">
          <Reveal className="text-center mb-20">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-md bg-[#1a1a1a] border border-[#2a2a2a] mb-6">
              <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
              <span className="text-sm text-gray-500">Comprehensive</span>
            </div>
            <h2 className="text-5xl md:text-6xl text-white" style={{ marginBottom: '2rem' }}>
              Deep analysis, clear results
            </h2>
            <p className="text-gray-500 text-xl max-w-2xl mx-auto">
              Everything you need to make informed decisions about your future
            </p>
          </Reveal>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
            {/* Large Feature 1 */}
            <Reveal
              scale={true}
              delay={100}
              className="md:col-span-2 md:row-span-2 relative p-8 rounded-lg bg-[#111111] border border-[#1f1f1f] hover:border-[#2a2a2a] transition-colors group overflow-hidden"
            >
              <div className="relative h-full flex flex-col">
                <div className="w-12 h-12 rounded-lg bg-[#1a1a1a] border border-[#2a2a2a] flex items-center justify-center mb-6">
                  <BarChart3 className="w-6 h-6 text-blue-500" />
                </div>
                <h3 className="text-white text-xl" style={{ marginBottom: '1rem' }}>Subject Analysis</h3>
                <p className="text-gray-500 text-sm leading-relaxed mb-6">
                  See your strengths across Math, Physics, Chemistry, Biology, Khmer, English, and History with detailed performance breakdowns and insights.
                </p>
                <div className="mt-auto flex flex-col gap-4">
                  <div className="space-y-2">
                    {['Mathematics: Strong', 'Physics: Moderate', 'English: Strong'].map((item, i) => (
                      <div key={i} className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                        <span className="text-sm text-gray-600">{item}</span>
                      </div>
                    ))}
                  </div>
                  {subjectAnalysisAnimation && (
                    <div className="flex items-center justify-center">
                      <Lottie 
                        animationData={subjectAnalysisAnimation}
                        loop={true}
                        autoplay={true}
                        style={{ width: '350px', height: '350px' }}
                      />
                    </div>
                  )}
                </div>
              </div>
            </Reveal>
            
            {/* Small Feature 1 */}
            <Reveal
              scale={true}
              delay={200}
              className="md:col-span-2 relative p-6 rounded-lg bg-[#111111] border border-[#1f1f1f] hover:border-[#2a2a2a] transition-colors group overflow-hidden"
            >
              <div className="relative h-full flex flex-col">
                <div className="w-10 h-10 rounded-lg bg-[#1a1a1a] border border-[#2a2a2a] flex items-center justify-center mb-4">
                  <Award className="w-5 h-5 text-blue-500" />
                </div>
                <h3 className="text-white" style={{ marginBottom: '1rem' }}>Recommendation Engine</h3>
                <p className="text-gray-500 text-sm leading-relaxed mb-4">
                  Get majors, careers, and universities with match scores and detailed breakdowns
                </p>
                {recommendationEngineAnimation && (
                  <div className="mt-auto flex justify-center items-center">
                    <Lottie 
                      animationData={recommendationEngineAnimation}
                      loop={true}
                      autoplay={true}
                      style={{ width: '100%', maxWidth: 150, height: 'auto' }}
                    />
                  </div>
                )}
              </div>
            </Reveal>
            
            {/* Small Feature 2 */}
            <Reveal
              scale={true}
              delay={300}
              className="relative p-6 rounded-lg bg-[#111111] border border-[#1f1f1f] hover:border-[#2a2a2a] transition-colors group overflow-hidden"
            >
              <div className="relative h-full flex flex-col">
                <div className="w-10 h-10 rounded-lg bg-[#1a1a1a] border border-[#2a2a2a] flex items-center justify-center mb-4">
                  <TrendingUp className="w-5 h-5 text-blue-500" />
                </div>
                <h3 className="text-white" style={{ marginBottom: '1rem' }}>Skill Development</h3>
                <p className="text-gray-500 text-sm leading-relaxed mb-4">
                  Current vs target levels with improvement plans
                </p>
                {skillDevelopmentAnimation && (
                  <div className="mt-auto flex justify-center items-center">
                    <Lottie 
                      animationData={skillDevelopmentAnimation}
                      loop={true}
                      autoplay={true}
                      style={{ width: '100%', maxWidth: 220, height: 'auto' }}
                    />
                  </div>
                )}
              </div>
            </Reveal>
            
            {/* Small Feature 3 */}
            <Reveal
              scale={true}
              delay={400}
              className="relative p-6 rounded-lg bg-[#111111] border border-[#1f1f1f] hover:border-[#2a2a2a] transition-colors group overflow-hidden"
            >
              <div className="relative h-full flex flex-col">
                <div className="w-10 h-10 rounded-lg bg-[#1a1a1a] border border-[#2a2a2a] flex items-center justify-center mb-4">
                  <Globe className="w-5 h-5 text-blue-500" />
                </div>
                <h3 className="text-white" style={{ marginBottom: '1rem' }}>Cambodia Focused</h3>
                <p className="text-gray-500 text-sm leading-relaxed mb-4">
                  Specialized recommendations for Cambodian universities
                </p>
                {cambodiaAnimation && (
                  <div className="mt-auto flex justify-center items-center">
                    <Lottie 
                      animationData={cambodiaAnimation}
                      loop={true}
                      autoplay={true}
                      style={{ width: '100%', maxWidth: 150, height: 'auto' }}
                    />
                  </div>
                )}
              </div>
            </Reveal>
          </div>
        </div>
      </section>

      {/* University Showcase Section */}
      <section className="py-32 relative">
        <div className="max-w-7xl mx-auto px-6">
          <Reveal className="text-center mb-20">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-md bg-[#1a1a1a] border border-[#2a2a2a] mb-6">
              <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
              <span className="text-sm text-gray-500">Partner Universities</span>
            </div>
            <h2 className="text-5xl md:text-6xl text-white" style={{ marginBottom: '2rem' }}>
              Top Cambodian Universities
            </h2>
            <p className="text-gray-500 text-xl max-w-2xl mx-auto">
              Based on your recommended major, we match you with the best universities in Cambodia
            </p>
          </Reveal>

          {/* 2 Column Grid Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Left Column - Description */}
            <Reveal
              translateX={-20}
              className="space-y-6"
            >
              <div className="space-y-4">
                <h3 className="text-3xl md:text-4xl text-white font-bold">
                  Your Perfect University Match
                </h3>
                <p className="text-gray-400 text-lg leading-relaxed">
                  Our AI-powered system analyzes your academic performance and career goals to recommend the most suitable universities for your chosen major. All partner institutions are accredited and recognized leaders in their fields.
                </p>
              </div>

              <div className="space-y-4">
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 rounded-lg  bg-[#1a1a1a] border border-[#2a2a2a] flex items-center justify-center flex-shrink-0 mt-1">
                    <CheckCircle2 className="w-5 h-5 text-blue-500" />
                  </div>
                  <div>
                    <h4 className="text-white font-semibold mb-1">Accredited Programs</h4>
                    <p className="text-gray-500 text-sm">All universities offer internationally recognized degrees and certifications</p>
                  </div>
                </div>

                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 rounded-lg  bg-[#1a1a1a] border border-[#2a2a2a] flex items-center justify-center flex-shrink-0 mt-1">
                    <Award className="w-5 h-5 text-blue-500" />
                  </div>
                  <div>
                    <h4 className="text-white font-semibold mb-1">Specialized Excellence</h4>
                    <p className="text-gray-500 text-sm">Each institution excels in specific fields matching your interests</p>
                  </div>
                </div>

                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 rounded-lg  bg-[#1a1a1a] border border-[#2a2a2a] flex items-center justify-center flex-shrink-0 mt-1">
                    <Target className="w-5 h-5 text-blue-500" />
                  </div>
                  <div>
                    <h4 className="text-white font-semibold mb-1">Career-Focused</h4>
                    <p className="text-gray-500 text-sm">Strong industry connections and high graduate employment rates</p>
                  </div>
                </div>
              </div>
            </Reveal>

            {/* Right Column - Infinite Scroll */}
            <Reveal
              translateX={20}
              className="relative mt-6"
            >
              <InfiniteScroll
                items={[
                  { content: <div className="text-white text-xs p-2">Cambodia Academy of Digital Technology (CADT)</div> },
                  { content: <div className="text-white text-xs p-2">Royal University of Phnom Penh (RUPP)</div> },
                  { content: <div className="text-white text-xs p-2">Institute of Technology of Cambodia (ITC)</div> },
                  { content: <div className="text-white text-xs p-2">Phnom Penh International University (PPIU)</div> },
                  { content: <div className="text-white text-xs p-2">Western University</div> },
                  { content: <div className="text-white text-xs p-2">Royal University of Law and Economics (RULE)</div> },
                  { content: <div className="text-white text-xs p-2">Build Bright University (BBU)</div> },
                  { content: <div className="text-white text-xs p-2">University of Cambodia (UC)</div> },
                  { content: <div className="text-white text-xs p-2">American University of Phnom Penh (AUPP)</div> },
                  { content: <div className="text-white text-xs p-2">National University of Management (NUM)</div> },
                  { content: <div className="text-white text-xs p-2">Royal University of Fine Arts (RUFA)</div> },
                  { content: <div className="text-white text-xs p-2">University of Health Sciences (UHS)</div> },
                  { content: <div className="text-white text-xs p-2">Paññāsāstra University of Cambodia (PUC)</div> },
                  { content: <div className="text-white text-xs p-2">Paragon International University</div> },
                  { content: <div className="text-white text-xs p-2">University of Puthisastra (UP)</div> },
                  { content: <div className="text-white text-xs p-2">National Polytechnic Institute of Cambodia (NPIC)</div> },
                ]}
                isTilted={true}
                tiltDirection="right"
                autoplay={true}
                autoplaySpeed={0.6}
                autoplayDirection="down"
                pauseOnHover={true}
                itemMinHeight={80}
                width="100%"
                maxHeight="600px"
              />
            </Reveal>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-32 relative">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <Reveal translateY={true}>
            <h2 className="text-5xl md:text-6xl text-white" style={{ marginBottom: '2rem' }}>
              Ready to discover your path?
            </h2>
            <p className="text-xl text-gray-500 mb-12 max-w-2xl mx-auto">
              Join thousands of Cambodian students who have found clarity in their academic journey
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Button
                onClick={hasToken ? () => router.push('/Input') : handleGetStarted}
                size="lg"
                className="group px-8 py-3 rounded-lg bg-gray-800 hover:bg-gray-700 text-white transition-colors border border-gray-600"
              >
                {hasToken ? 'Start Analysis' : 'Start Free Analysis'}
                <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
              </Button>
            </div>
          </Reveal>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-16 border-t border-[#1f1f1f] relative z-20">
        <div className="max-w-7xl mx-auto px-6">
          
          
          <div className="flex flex-col md:flex-row justify-between items-center pt-8 border-[#1f1f1f]">
            <div className="flex items-center gap-2 mb-4 md:mb-0">
              <img 
                src="/image/Bontor-logo.png" 
                alt="Bontor" 
                style={{ 
                  height: '24px',
                  width: 'auto'
                }}
              />
            </div>
            <p className="text-gray-600 text-sm">
              © 2025 Bontor Smart BacII Grade & Career Analyzer. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
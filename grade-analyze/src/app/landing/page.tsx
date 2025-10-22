"use client";

import { useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'
import Button from "@/components/ui/Button";
import { Brain, TrendingUp, Target, Shield, CheckCircle2, BarChart3, Globe, Zap, ArrowRight, Award } from "lucide-react";
import { motion } from "framer-motion";

export default function LandingPage() {
  const router = useRouter()
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
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center max-w-5xl mx-auto"
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5 }}
              className="inline-flex items-center gap-2 px-3 py-1.5 rounded-md bg-[#1a1a1a] border border-[#2a2a2a] mb-8"
            >
              <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
              <span className="text-sm text-gray-400">
                AI-Powered Career Guidance for Cambodian Students
              </span>
            </motion.div>
            
            <h1 className="text-6xl md:text-8xl text-white tracking-tight leading-none" style={{ marginBottom: '3rem' }}>
              Your future starts
              <br />
              <span className="text-white">
                with insight
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-500 mb-12 max-w-3xl mx-auto leading-relaxed">
              Transform your BacII grades into a personalized roadmap. Discover your ideal major, career path, and university powered by AI.
            </p>
            
            <div className="flex justify-center items-center">
              <Button
                onClick={hasToken ? () => router.push('/Input') : handleGetStarted}
                size="lg"
                className="group px-6 py-3 rounded-lg bg-gray-800 hover:bg-gray-700 text-white transition-colors"
              >
                {hasToken ? 'Start Analysis' : 'Get Started'}
                <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
              </Button>
            </div>
          </motion.div>
          
          {/* Hero Visual - Bento Grid */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="mt-24 relative"
          >
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 max-w-6xl mx-auto">
              {/* Large Card */}
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: 0.4 }}
                className="md:col-span-2 relative rounded-lg bg-[#111111] border border-[#1f1f1f] p-8 overflow-hidden group hover:border-[#2a2a2a] transition-colors"
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
                    {[85, 92, 78].map((value, i) => (
                      <div key={i} className="flex items-center gap-3">
                        <div className="flex-1 h-1.5 bg-[#1a1a1a] rounded-full overflow-hidden">
                          <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${value}%` }}
                            transition={{ duration: 1, delay: 0.5 + i * 0.1 }}
                            className="h-full bg-blue-500"
                          />
                        </div>
                        <span className="text-sm text-gray-500 w-12">{value}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>

              {/* Small Card 1 */}
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: 0.5 }}
                className="relative rounded-lg bg-[#111111] border border-[#1f1f1f] p-8 overflow-hidden group hover:border-[#2a2a2a] transition-colors"
              >
                <div className="relative">
                        <Zap className="w-8 h-8 text-blue-500 mb-4" />
                  <h4 className="text-white" style={{ marginBottom: '1rem' }}>Instant Insights</h4>
                  <p className="text-sm text-gray-500">Real-time analysis in seconds</p>
                </div>
              </motion.div>

              {/* Small Card 2 */}
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: 0.6 }}
                className="relative rounded-lg bg-[#111111] border border-[#1f1f1f] p-8 overflow-hidden group hover:border-[#2a2a2a] transition-colors"
              >
                <div className="relative">
                        <Target className="w-8 h-8 text-blue-500 mb-4" />
                  <h4 className="text-white" style={{ marginBottom: '1rem' }}>92% Accuracy</h4>
                  <p className="text-sm text-gray-500">Average match rate</p>
                </div>
              </motion.div>

              {/* Wide Card */}
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: 0.7 }}
                className="md:col-span-2 relative rounded-lg bg-[#111111] border border-[#1f1f1f] p-8 overflow-hidden group hover:border-[#2a2a2a] transition-colors"
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
              </motion.div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Simple Divider */}
      <div className="relative h-16 flex items-center justify-center z-20">
        <div className="w-64 h-px bg-gradient-to-r from-transparent via-gray-400/60 to-transparent shadow-[0_0_8px_rgba(156,163,175,0.3)]" />
      </div>
      

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
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-20"
          >
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
          </motion.div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
            {[
              {
                icon: Brain,
                title: "AI-Powered Insights",
                description: "Personalized majors, careers, and universities tailored to your profile"
              },
              {
                icon: TrendingUp,
                title: "Built for BacII",
                description: "Subject max scores, normalization, and Cambodian educational context"
              },
              {
                icon: Target,
                title: "Actionable Next Steps",
                description: "Clear skill gaps and how to improve with specific suggestions"
              },
              {
                icon: Shield,
                title: "Private & Secure",
                description: "Your data, your control. All analysis happens locally"
              }
            ].map((benefit, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
                className="group"
              >
                <div className="relative h-full p-6 rounded-lg bg-[#111111] border border-[#1f1f1f] hover:border-[#2a2a2a] transition-colors overflow-hidden">
                  <div className="relative">
                    <div className="w-10 h-10 rounded-lg bg-[#1a1a1a] border border-[#2a2a2a] flex items-center justify-center mb-4">
                      <benefit.icon className="w-5 h-5 text-blue-500" />
                    </div>
                    <h3 className="text-white" style={{ marginBottom: '1rem' }}>{benefit.title}</h3>
                    <p className="text-gray-500 text-sm leading-relaxed">{benefit.description}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Simple Divider */}
      <div className="relative h-16 flex items-center justify-center">
        <div className="w-64 h-px bg-gradient-to-r from-transparent via-gray-400/60 to-transparent shadow-[0_0_8px_rgba(156,163,175,0.3)]" />
      </div>

      {/* Three Steps Process */}
      <section className="py-32 relative">
        <div className="max-w-7xl mx-auto px-6 relative">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-20"
          >
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
          </motion.div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 relative">
            {/* Connecting Line */}
            <div className="hidden md:block absolute top-16 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[#2a2a2a] to-transparent" />
            
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
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.2 }}
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
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Simple Divider */}
      <div className="relative h-15 flex items-center justify-center">
        <div className="w-64 h-px bg-gradient-to-r from-transparent via-gray-400/60 to-transparent shadow-[0_0_8px_rgba(156,163,175,0.3)]" />
      </div>

      {/* Feature Highlights - Bento Grid */}
      <section className="py-32 relative">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-20"
          >
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
          </motion.div>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
            {/* Large Feature 1 */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
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
                <div className="mt-auto space-y-2">
                  {['Mathematics: Strong', 'Physics: Moderate', 'English: Strong'].map((item, i) => (
                    <div key={i} className="flex items-center gap-2">
                      <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                      <span className="text-sm text-gray-600">{item}</span>
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>
            
            {/* Small Feature 1 */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
              className="md:col-span-2 relative p-6 rounded-lg bg-[#111111] border border-[#1f1f1f] hover:border-[#2a2a2a] transition-colors group overflow-hidden"
            >
              <div className="relative">
                <div className="w-10 h-10 rounded-lg bg-[#1a1a1a] border border-[#2a2a2a] flex items-center justify-center mb-4">
                  <Award className="w-5 h-5 text-blue-500" />
                </div>
                <h3 className="text-white" style={{ marginBottom: '1rem' }}>Recommendation Engine</h3>
                <p className="text-gray-500 text-sm leading-relaxed">
                  Get majors, careers, and universities with match scores and detailed breakdowns
                </p>
              </div>
            </motion.div>
            
            {/* Small Feature 2 */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.3 }}
              className="relative p-6 rounded-lg bg-[#111111] border border-[#1f1f1f] hover:border-[#2a2a2a] transition-colors group overflow-hidden"
            >
              <div className="relative">
                <div className="w-10 h-10 rounded-lg bg-[#1a1a1a] border border-[#2a2a2a] flex items-center justify-center mb-4">
                  <TrendingUp className="w-5 h-5 text-blue-500" />
                </div>
                <h3 className="text-white" style={{ marginBottom: '1rem' }}>Skill Development</h3>
                <p className="text-gray-500 text-sm leading-relaxed">
                  Current vs target levels with improvement plans
                </p>
              </div>
            </motion.div>
            
            {/* Small Feature 3 */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.4 }}
              className="relative p-6 rounded-lg bg-[#111111] border border-[#1f1f1f] hover:border-[#2a2a2a] transition-colors group overflow-hidden"
            >
              <div className="relative">
                <div className="w-10 h-10 rounded-lg bg-[#1a1a1a] border border-[#2a2a2a] flex items-center justify-center mb-4">
                  <Globe className="w-5 h-5 text-blue-500" />
                </div>
                <h3 className="text-white" style={{ marginBottom: '1rem' }}>Cambodia Focused</h3>
                <p className="text-gray-500 text-sm leading-relaxed">
                  Specialized recommendations for Cambodian universities
                </p>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-32 relative">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
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
          </motion.div>
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
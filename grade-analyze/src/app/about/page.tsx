"use client";

import { useRouter } from 'next/navigation';
import { useState, useEffect, useLayoutEffect } from 'react';
import Button from "@/components/ui/Button";
import { motion } from "framer-motion";
import { Brain, Code, Database, Monitor } from "lucide-react";
import dynamic from 'next/dynamic';

const Lanyard = dynamic(() => import('@/components/Lanyard'), { ssr: false });

export default function AboutPage() {
  const router = useRouter();
  const [hasToken, setHasToken] = useState<boolean | null>(null);

  useLayoutEffect(() => {
    // Scroll to top immediately before browser paints
    if (typeof window !== 'undefined') {
      window.scrollTo(0, 0);
    }
  }, []);

  useEffect(() => {
    const cookies = document.cookie;
    const hasAuthToken = cookies.includes('auth-token=');
    setHasToken(hasAuthToken);
  }, []);

  const teamMembers = [
    {
      name: "Phan Panhawornd",
      role: "Fullstack Developer, Project Manager & ML Trainer",
      icon: Code,
      alignment: "left",
      description: `Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.`
    },
    {
      name: "Deng Rithypanha",
      role: "Backend Developer & ML Trainer",
      icon: Database,
      alignment: "right",
      description: `Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.`
    },
    {
      name: "Soy Dychheny",
      role: "Frontend Developer & ML Trainer",
      icon: Monitor,
      alignment: "left",
      description: `Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.`
    },
    {
      name: "Pin Rathana",
      role: "Frontend Developer & ML Trainer",
      icon: Monitor,
      alignment: "right",
      description: `Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.`
    },
    {
      name: "Chorn Sothea",
      role: "Backend Developer & ML Trainer",
      icon: Database,
      alignment: "left",
      description: `Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.`
    },
    {
      name: "Choeun Rane",
      role: "Frontend Developer & ML Trainer",
      icon: Monitor,
      alignment: "right",
      description: `Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.`
    }
  ];

  const handleGetStarted = () => {
    router.push('/login');
  };

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

      {/* Dark gradient background */}
      <div
        className="absolute inset-x-0"
        style={{ 
          top: 0,
          bottom: 0,
          background: "radial-gradient(ellipse 80% 60% at 50% 50%, #2d3748 0%, #1a202c 30%, #0f1419 60%, #000000 100%)"
        }}
      />

      {/* Our Story Section */}
      <section className="pt-32 pb-24 relative z-10">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-10"
          >
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-md bg-[#1a1a1a] border border-[#2a2a2a] mb-6">
              <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
              <span className="text-sm text-gray-500">Our Story</span>
            </div>
            <h2 className="text-5xl md:text-6xl text-white mb-8">
              Who We Are
            </h2>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="max-w-4xl mx-auto relative z-10 text-center"
          >
            <div className="space-y-1 text-gray-400 text-lg leading-relaxed text-center">
              <p>
                We are students at <span className="text-white font-semibold">Cambodia Academy of Digital Technology</span>. Our vision is to help students who have just finished taking the BacII exam find their suitable major, career, and university.
              </p>
              <p>
                When we were in that situation, we knew it was a new experience to find a major and university to study. That challenge inspired us to create this platform to make the path clearer for future students.
              </p>
              <p className="text-gray-300">
                Through AI-powered analysis and comprehensive guidance, we aim to bridge the gap between academic achievement and career decisions, helping every student make informed choices about their future.
              </p>
            </div>
          </motion.div>
        </div>
      </section>

      {/*True After BacII Story*/}
      <section className="py-32 relative z-10">
        <div>
          
        </div>


        
      </section>


      {/* Our Team Section - Zigzag Design */}
      <section className="py-32 relative z-10">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-20"
          >
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-md bg-[#1a1a1a] border border-[#2a2a2a] mb-6">
              <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
              <span className="text-sm text-gray-500">Our Team</span>
            </div>
            <h2 className="text-5xl md:text-6xl text-white" style={{ marginBottom: '2rem' }}>
              Meet the Developers
            </h2>
            <p className="text-gray-500 text-xl max-w-2xl mx-auto">
              A passionate team of students building the future of career guidance
            </p>
          </motion.div>

          <div className="space-y-12">
            {teamMembers.map((member, idx) => {
              // Simple alternating: even index = image left, odd index = image right
              const imageOnLeft = idx % 2 === 0;
              
              return (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, x: imageOnLeft ? -50 : 50 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6, delay: idx * 0.1 }}
                  className={`flex flex-col md:flex-row items-center ${imageOnLeft ? 'md:flex-row gap-8' : 'md:flex-row-reverse gap-6'}`}
                >
                  {/* Profile Image Placeholder with Name and Role Below */}
                  <div className="flex-shrink-0 flex flex-col items-center" style={{ width: '320px' }}>
                    <div className="w-80 rounded-lg border border-[#2a2a2a] overflow-hidden flex flex-col items-center" style={{ width: '320px', backgroundColor: '#111111' }}>
                      <div className="w-full h-72 rounded-lg overflow-hidden mb-[-4px] relative" style={{ width: '288px', height: '288px', marginTop: '4px', backgroundColor: 'transparent' }}>
                        <Lanyard 
                          position={[0, 0, 11]} 
                          gravity={[0, -40, 0]} 
                          fov={42}
                        />
                      </div>
                      <div className="text-center pb-6 px-4">
                        <h3 className="text-xl md:text-2xl text-white font-semibold mb-2 whitespace-nowrap">
                          {member.name}
                        </h3>
                        <p className="text-gray-400 text-sm leading-relaxed">
                          {member.role}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Description Content */}
                  <div className="flex-1 text-left max-w-2xl">
                    <p className="text-gray-400 text-lg leading-relaxed">
                      {member.description.split('\n').map((line, lineIdx) => (
                        <span key={lineIdx}>
                          {line}
                          {lineIdx < member.description.split('\n').length - 1 && <br />}
                        </span>
                      ))}
                    </p>
                  </div>
                </motion.div>
              );
            })}
          </div>
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

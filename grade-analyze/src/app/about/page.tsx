"use client";

import { useRouter } from 'next/navigation';
import { useState, useEffect, useLayoutEffect, useRef } from 'react';
import Button from "@/components/ui/Button";
import Reveal from "@/components/Reveal";
import { Code, Database, Monitor, Target, Lightbulb, Heart, Globe } from "lucide-react";
import dynamic from 'next/dynamic';
import Lottie, { LottieRefCurrentProps } from "lottie-react";
import StarBorder from "@/components/ui/StarBorder";

const Lanyard = dynamic(() => import('@/components/Lanyard'), { ssr: false });

export default function AboutPage() {
  const router = useRouter();
  const [hasToken, setHasToken] = useState<boolean | null>(null);
  const [confusionAnimation, setConfusionAnimation] = useState<any>(null);
  const lottieRef = useRef<LottieRefCurrentProps>(null);

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

    // Load confusion Lottie animation
    fetch('/lottie/confusion.json')
      .then(res => res.json())
      .then(data => {
        setConfusionAnimation(data);
      })
      .catch(err => console.error('Error loading confusion animation:', err));
  }, []);

  const teamMembers = [
    {
      name: "Phan Panhawornd",
      role: "Fullstack Developer, Project Manager & ML Trainer",
      icon: Code,
      alignment: "left",
      description: `Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.`,
      hasCustomImage: true,
      imagePath: "/image/Panhawornd.png"
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
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/2 backdrop-blur-md min-h-[4rem]">
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
                  className="h-5 md:h-[23px] w-auto"
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
      <div className="absolute top-0 left-1/4 w-[500px] h-[500px] bg-blue-500/5 rounded-full mix-blend-lighten filter blur-3xl" style={{ willChange: 'auto', transform: 'translateZ(0)' }} />
      <div className="absolute top-1/3 right-1/4 w-[500px] h-[500px] bg-blue-400/5 rounded-full mix-blend-lighten filter blur-3xl" style={{ willChange: 'auto', transform: 'translateZ(0)' }} />

      {/* Ultravib image background with dark overlay */}
      <div
        className="fixed inset-x-0"
        style={{ 
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

      {/* Our Story Section */}
      <section className="pt-32 pb-24 relative z-10" data-section="our-story">
        <div className="max-w-7xl mx-auto px-6">
          <Reveal
            className="text-center mb-10"
            rootMargin="-50px"
            threshold={0.2}
          >
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-md bg-[#1a1a1a] border border-[#2a2a2a] mb-6">
              <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
              <span className="text-sm text-gray-500">Our Story</span>
            </div>
            <h2 className="text-5xl md:text-6xl text-white mb-8">
              Who We Are
            </h2>
          </Reveal>

          <Reveal
            className="max-w-4xl mx-auto relative z-10 text-center"
            delay={100}
            rootMargin="-50px"
            threshold={0.2}
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
          </Reveal>
        </div>
      </section>

      {/* After BacII Story */}
      <section className="py-32 relative z-10" data-section="after-bacii">
        <div className="max-w-7xl mx-auto px-6">
          {/* Section Header */}
          <Reveal
            className="text-center mb-10"
            rootMargin="-50px"
            threshold={0.2}
          >
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-md bg-[#1a1a1a] border border-[#2a2a2a] mb-6">
              <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
              <span className="text-sm text-gray-500">Our Journey</span>
            </div>
            <h2 className="text-5xl md:text-6xl text-white mb-8">
              After BacII
            </h2>
          </Reveal>

          <div className="space-y-8">
            {/* Main content */}
            <Reveal
              className="text-center max-w-4xl mx-auto"
              delay={100}
              rootMargin="-50px"
            >
              <p className="text-gray-400 text-lg leading-relaxed mb-6">
                Finishing the BacII exam is one of the biggest milestones in a student's life but it also comes with uncertainty. Many students feel lost, unsure of what major to choose, which university to apply to, or what career path fits them best.
              </p>
              <p className="text-gray-300 text-lg leading-relaxed font-medium mb-6">
                We've been there too. After completing our BacII exams, we faced the same questions:
              </p>
            </Reveal>

            {/* Questions with image */}
            <Reveal
              className="flex flex-col md:flex-row items-center justify-center gap-6 max-w-5xl mx-auto"
              translateY={true}
              rootMargin="-50px"
            >
              {/* Confusion Lottie animation on the left */}
              <div className="flex-shrink-0 flex items-center justify-center">
                {confusionAnimation && (
                  <Lottie
                    lottieRef={lottieRef}
                    animationData={confusionAnimation}
                    loop={false}
                    autoplay={true}
                    style={{ width: '100%', maxWidth: '400px', height: 'auto' }}
                    onEnterFrame={(evt: any) => {
                      // Stop at 70% of total frames (before it ends)
                      if (confusionAnimation && evt && evt.currentFrame !== undefined) {
                        const totalFrames = confusionAnimation.op || 181;
                        const stopFrame = Math.floor(totalFrames * 0.7);
                        if (evt.currentFrame >= stopFrame && lottieRef.current) {
                          lottieRef.current.stop();
                        }
                      }
                    }}
                  />
                )}
              </div>

              {/* Questions as bullet points on the right */}
              <div className="flex-1 flex items-center justify-center">
                <ul className="space-y-4 text-left">
                  <li className="flex items-start gap-3">
                    <span className="text-blue-500 mt-1.5">•</span>
                    <p className="text-gray-300 text-lg leading-relaxed">
                      What should I study next?
                    </p>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="text-blue-500 mt-1.5">•</span>
                    <p className="text-gray-300 text-lg leading-relaxed">
                      Which major will match my interests and abilities?
                    </p>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="text-blue-500 mt-1.5">•</span>
                    <p className="text-gray-300 text-lg leading-relaxed">
                      What if I make the wrong choice?
                    </p>
                  </li>
                </ul>
              </div>
            </Reveal>

            {/* Closing content */}
            <Reveal
              className="text-center max-w-4xl mx-auto mt-12"
              rootMargin="-50px"
            >
              <p className="text-gray-400 text-lg leading-relaxed mb-6">
                That period of confusion and exploration inspired us to take action. Instead of letting others go through the same struggle alone, we created Bontor a platform built by students, for students.
              </p>
              <p className="text-gray-300 text-lg leading-relaxed font-medium">
                Bontor exists to guide BacII graduates toward the future that fits them best. We use AI technology and personalized insights to turn uncertainty into clarity helping students discover the major, university, and career path that truly suits them.
              </p>
            </Reveal>
          </div>
        </div>
      </section>

      {/* Our Values */}
      <section className="py-32 relative z-10" data-section="our-values">
        <div className="max-w-7xl mx-auto px-6">
          {/* Section Header */}
          <Reveal
            className="text-center mb-16"
            rootMargin="-50px"
            threshold={0.2}
          >
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-md bg-[#1a1a1a] border border-[#2a2a2a] mb-6">
              <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
              <span className="text-sm text-gray-500">Our Foundation</span>
            </div>
            <h2 className="text-5xl md:text-6xl text-white mb-4">
              Our Values
            </h2>
          </Reveal>

          {/* Values Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <Reveal
              delay={0}
              rootMargin="-50px"
              threshold={0.2}
            >
              <StarBorder
                color="#3b82f6"
                className="w-full"
              >
                <div className="flex flex-col justify-center items-center text-center p-6 min-h-[280px]">
                  <div className="mb-4">
                    <Target className="w-12 h-12 text-blue-500 mx-auto" />
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-3">
                    Purpose-Driven
                  </h3>
                  <p className="text-gray-400 text-sm leading-relaxed mt-4">
                    Every student&apos;s dream matters. We empower students to pursue their goals.
                  </p>
                </div>
              </StarBorder>
            </Reveal>

            <Reveal
              delay={100}
              rootMargin="-50px"
              threshold={0.2}
            >
              <StarBorder
                color="#3b82f6"
                className="w-full"
              >
                <div className="flex flex-col justify-center items-center text-center p-6 min-h-[280px]">
                  <div className="mb-4">
                    <Lightbulb className="w-12 h-12 text-blue-500 mx-auto" />
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-3">
                    Innovation
                  </h3>
                  <p className="text-gray-400 text-sm leading-relaxed mt-4">
                    We use technology to make guidance smarter and more accessible.
                  </p>
                </div>
              </StarBorder>
            </Reveal>

            <Reveal
              delay={200}
              rootMargin="-50px"
              threshold={0.2}
            >
              <StarBorder
                color="#3b82f6"
                className="w-full"
              >
                <div className="flex flex-col justify-center items-center text-center p-6 min-h-[280px]">
                  <div className="mb-4">
                    <Heart className="w-12 h-12 text-blue-500 mx-auto" />
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-3">
                    Empathy
                  </h3>
                  <p className="text-gray-400 text-sm leading-relaxed mt-4">
                    We understand because we&apos;ve been there. We know the challenges students face.
                  </p>
                </div>
              </StarBorder>
            </Reveal>

            <Reveal
              delay={300}
              rootMargin="-50px"
              threshold={0.2}
            >
              <StarBorder
                color="#3b82f6"
                className="w-full"
              >
                <div className="flex flex-col justify-center items-center text-center p-6 min-h-[280px]">
                  <div className="mb-4">
                    <Globe className="w-12 h-12 text-blue-500 mx-auto" />
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-3">
                    Impact
                  </h3>
                  <p className="text-gray-400 text-sm leading-relaxed mt-4">
                    We aim to improve educational choices and career readiness for students nationwide.
                  </p>
                </div>
              </StarBorder>
            </Reveal>
          </div>
        </div>
      </section>

      {/* Our Team Section - Zigzag Design */}
      <section className="py-32 relative z-10">
        <div className="max-w-7xl mx-auto px-6">
          <Reveal
            className="text-center mb-20"
            threshold={0.2}
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
          </Reveal>

          <div className="space-y-12">
            {teamMembers.map((member, idx) => {
              // Simple alternating: even index = image left, odd index = image right
              const imageOnLeft = idx % 2 === 0;
              
              return (
                <MemberCard 
                  key={idx}
                  member={member}
                  idx={idx}
                  imageOnLeft={imageOnLeft}
                />
              );
            })}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-16 border-t relative z-20 footer-container border-white/10">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center pt-2 gap-8 footer-content">
            {/* Logo and Description */}
            <div className="flex flex-col footer-logo-section">
              <div className="flex items-center gap-2 mb-4 footer-logo">
              <img 
                src="/image/Bontor-logo.png" 
                alt="Bontor" 
                style={{ 
                  height: '24px',
                  width: 'auto'
                }}
              />
            </div>
              <p className="text-gray-500 text-sm leading-relaxed max-w-xs footer-description">
                AI-powered career guidance platform designed specifically for Cambodian BacII students. Transform your grades into personalized major and university recommendations.
              </p>
            </div>

            {/* Quick Links and Copyright */}
            <div className="flex flex-col gap-4 footer-links-section">
              <div className="flex flex-row md:flex-row gap-20 footer-links">
                <div className="flex flex-col">
                  <h3 className="text-white font-semibold mb-3">Quick Links</h3>
                  <ul className="space-y-2 mt-2">
                    <li>
                      <button
                        onClick={() => router.push('/landing')}
                        className="text-gray-500 hover:text-blue-500 transition-colors text-sm"
                      >
                        Home
                      </button>
                    </li>
                    <li>
                      <button
                        onClick={() => router.push('/how-it-works')}
                        className="text-gray-500 hover:text-blue-500 transition-colors text-sm"
                      >
                        How it Works
                      </button>
                    </li>
                    <li>
                      <button
                        onClick={() => router.push('/about')}
                        className="text-gray-500 hover:text-blue-500 transition-colors text-sm"
                      >
                        About
                      </button>
                    </li>
                  </ul>
                </div>
                <div className="flex flex-col">
                  <h3 className="text-white font-semibold mb-3">Account</h3>
                  <ul className="space-y-2 mt-2">
                    <li>
                      <button
                        onClick={() => router.push('/login')}
                        className="text-gray-500 hover:text-blue-500 transition-colors text-sm"
                      >
                        Login
                      </button>
                    </li>
                    <li>
                      <button
                        onClick={() => router.push('/signup')}
                        className="text-gray-500 hover:text-blue-500 transition-colors text-sm"
                      >
                        Register
                      </button>
                    </li>
                  </ul>
                </div>
              </div>
              <div className="pt-4 border-t border-white/10 footer-copyright">
            <p className="text-gray-600 text-sm">
              © 2025 Bontor Smart BacII Grade & Career Analyzer. All rights reserved.
            </p>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

type TeamMember = {
  name: string;
  role: string;
  icon: typeof Code;
  alignment: string;
  description: string;
  hasCustomImage?: boolean;
  imagePath?: string;
};

function MemberCard({ member, idx, imageOnLeft }: { member: TeamMember; idx: number; imageOnLeft: boolean }) {
  const [isHovered, setIsHovered] = useState(false);
  
  return (
    <Reveal
      className={`flex flex-col md:flex-row items-center ${imageOnLeft ? 'md:flex-row gap-8' : 'md:flex-row-reverse gap-6'}`}
      translateX={imageOnLeft ? -50 : 50}
      threshold={0.2}
    >
      {/* Profile Image Placeholder with Name and Role Below */}
      <div 
        className="flex-shrink-0 flex flex-col items-center group" 
        style={{ width: '320px' }}
      >
                    <div className="w-80 rounded-lg border border-[#2a2a2a] overflow-hidden flex flex-col items-center" style={{ width: '320px', backgroundColor: '#111111' }}>
                      <div 
                        className="w-full h-72 rounded-lg overflow-hidden mb-[-4px] relative group/card" 
                        style={{ width: '288px', height: '288px', marginTop: '4px', backgroundColor: 'transparent' }}
                      >
                        <Lanyard 
                          position={[0, 0, 11]} 
                          gravity={[0, -40, 0]} 
                          fov={42}
                          onHoverChange={setIsHovered}
                        />
                        {member.hasCustomImage && member.imagePath && (
                          <div
                            className="absolute overflow-hidden"
                            style={{ 
                              zIndex: 10, 
                              pointerEvents: 'none',
                              top: '67px',
                              left: '56px',
                              width: '180px',
                              height: '180px',
                              // Card center is at 144px, 144px in 288x288 container
                              // Image top-left is at 56px, 66px, so card center relative to image is (144-56, 144-66) = (88px, 78px)
                              // As percentage: (88/180 * 100, 78/180 * 100) = (48.89%, 43.33%)
                              transformOrigin: '48.89% 43.33%',
                              transform: isHovered ? 'perspective(1000px) rotateY(5.73deg) scale(1.05)' : 'perspective(1000px) rotateY(0deg) scale(1)',
                              transition: 'transform 0.15s ease-out',
                              transformStyle: 'preserve-3d',
                              willChange: 'transform',
                              // Card radius: 0.3 units / 4 units width = 7.5% of width
                              // Image container: 180px, so radius = 180px * 0.075 = 13.5px ≈ 0.84375rem
                              borderRadius: '0.84375rem',
                              clipPath: 'inset(0 round 0.84375rem)'
                            }}
                          >
                            <img 
                              src={member.imagePath}
                              alt={member.name}
                              className="w-full h-full object-contain"
                              style={{ 
                                borderRadius: '0.84375rem',
                                transform: 'translateZ(0)',
                                display: 'block'
                              }}
                            />
                          </div>
                        )}
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
          {member.description.split('\n').map((line: string, lineIdx: number) => (
            <span key={lineIdx}>
              {line}
              {lineIdx < member.description.split('\n').length - 1 && <br />}
            </span>
          ))}
        </p>
      </div>
    </Reveal>
  );
}

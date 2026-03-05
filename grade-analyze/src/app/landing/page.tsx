"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useState, useEffect, Suspense } from "react";
import Image from "next/image";
import Button from "@/components/ui/Button";
import Reveal from "@/components/Reveal";
import {
  Brain,
  TrendingUp,
  Target,
  Shield,
  CheckCircle2,
  BarChart3,
  Globe,
  Microscope,
  Zap,
  ArrowRight,
  Award,
} from "lucide-react";
import Lottie from "lottie-react";
import aiAnimationData from "@/lib/lottie/AI.json";
import bacIIAnimationData from "@/lib/lottie/BacII-student.json";
import nextStepAnimationData from "@/lib/lottie/Next-step.json";
import securityAnimationData from "@/lib/lottie/Security.json";
import subjectAnalysisAnimationData from "@/lib/lottie/Subject-analysis.json";
import recommendationEngineAnimationData from "@/lib/lottie/Recommendation-engine.json";
import skillDevelopmentAnimationData from "@/lib/lottie/Skill-development.json";
import cambodiaAnimationData from "@/lib/lottie/Cambodia.json";
import InfiniteScroll from "@/components/InfiniteScroll";

function LandingPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [hasToken, setHasToken] = useState(false); // Always false on SSR to avoid hydration mismatch
  const [authLoading, setAuthLoading] = useState(false);
  const [grades, setGrades] = useState<Record<string, string>>({});
  const [interestText, setInterestText] = useState("");
  const [careerGoals, setCareerGoals] = useState("");
  const [isAnalysisCardRevealed, setIsAnalysisCardRevealed] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isMobileFormOpen, setIsMobileFormOpen] = useState(false);


  // Validate form - check if all required fields are filled
  const isFormValid = () => {
    const SUBJECTS = [
      { id: "math", maxScore: 125 },
      { id: "physics", maxScore: 75 },
      { id: "chemistry", maxScore: 75 },
      { id: "biology", maxScore: 75 },
      { id: "khmer", maxScore: 75 },
      { id: "english", maxScore: 50 },
      { id: "history", maxScore: 50 },
    ];

    // Check all subjects have valid scores
    const allGradesValid = SUBJECTS.every((subj) => {
      const val = grades[subj.id]?.trim();
      if (!val) return false;
      const num = parseFloat(val);
      return !isNaN(num) && num >= 0 && num <= subj.maxScore;
    });

    // Check interests text is filled
    const interestsValid = interestText.trim().length > 0;

    return allGradesValid && interestsValid;
  };

  useEffect(() => {
    const justLoggedOut = localStorage.getItem('just_logged_out') === 'true';
    const justLoggedIn = localStorage.getItem('just_logged_in') === 'true';
    
    if (justLoggedOut) {
      setHasToken(false);
      setAuthLoading(false);
      localStorage.removeItem('just_logged_in'); // Clear login flag on logout
      return;
    }
    
    if (justLoggedIn) {
      setHasToken(true);
    }

    // Check if user is authenticated via API
    const checkAuth = async () => {
      try {
        const response = await fetch('/api/auth/me');
        const data = await response.json();
        
        if (data.user) {
          setHasToken(true);
          localStorage.setItem('just_logged_in', 'true'); // Set flag for future page visits
        } else {
          setHasToken(false);
          localStorage.removeItem('just_logged_in'); // Clear flag if not authenticated
        }
      } catch (error) {
        setHasToken(false);
        localStorage.removeItem('just_logged_in'); // Clear flag on error
      } finally {
        setAuthLoading(false);
      }
    };

    checkAuth();
  }, []);

  const handleGetStarted = () => {
    router.push("/login");
  };

  return (
    <div className="min-h-screen bg-black relative overflow-hidden">
      {/* Ultravib image background with dark overlay - covers from Cards section to bottom */}
      <div
        className="fixed inset-x-0"
        style={{
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundImage: "url(/image/Ultravib.png)",
          backgroundSize: "cover",
          backgroundPosition: "center center",
          backgroundRepeat: "no-repeat",
          filter: "brightness(0.9)",
          zIndex: 0,
          pointerEvents: "none",
        }}
      />
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/2 backdrop-blur-md min-h-[4rem]">
        <div className="max-w-7xl 2xl:max-w-none mx-auto px-4 sm:px-6 lg:px-8 2xl:px-24">
          <div className="flex items-center justify-center h-16 relative">
            {/* Logo */}
            <div className="absolute left-3 md:left-0 flex items-center">
              <button
                onClick={() => router.push("/landing")}
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
                  onClick={() => router.push("/landing")}
                  className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
                >
                  Home
                </button>
                <button
                  onClick={() => router.push("/how-it-works")}
                  className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
                >
                  How it Works
                </button>
                <button
                  onClick={() => router.push("/about")}
                  className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
                >
                  About
                </button>
              </div>
            </div>

            {/* Get Started/Analyze Button */}
            <div className="absolute right-0 hidden md:block">
              <Button
                onClick={
                  hasToken ? () => router.push("/dashboard") : handleGetStarted
                }
                disabled={authLoading}
                className="px-4 py-1.5 bg-gray-800 hover:bg-gray-700 text-white rounded-md transition-colors border border-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {hasToken ? "Go Dashboard" : "Get Started"}
              </Button>
            </div>
            {/* Mobile Menu trigger */}
            <div className="absolute inset-y-0 right-3 left-3 md:hidden flex items-center justify-end">
              <button
                type="button"
                className="flex items-center justify-end text-white text-sm tracking-wide uppercase text-right w-auto"
                aria-label="Open menu"
                onClick={() => setIsMenuOpen(true)}
              >
                <span className="w-5 h-5 flex items-center justify-center">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 22 22"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="lucide lucide-text-align-end-icon lucide-text-align-end"
                  >
                    <path d="M21 5H3" />
                    <path d="M21 12H9" />
                    <path d="M21 19H7" />
                  </svg>
                </span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      {isMenuOpen && (
        <div className="fixed inset-0 z-50 md:hidden">
          <button
            className="absolute inset-0 bg-black/60 backdrop-blur-md"
            aria-label="Close menu"
            onClick={() => setIsMenuOpen(false)}
          />
          <aside
            className="absolute top-0 right-0 h-full w-72 max-w-[80%] text-white border-l border-white/10 shadow-2xl"
            style={{
              backgroundImage:
                "linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url(/image/Ultravib.png)",
              backgroundSize: "cover",
              backgroundPosition: "center",
            }}
          >
            <div className="flex items-center justify-between px-5 py-4 border-b border-white/10">
              <span className="text-base font-semibold tracking-wide uppercase">
                Menu
              </span>
              <button
                onClick={() => setIsMenuOpen(false)}
                className="p-1 text-white/80 hover:text-white transition-colors"
                aria-label="Close menu"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  width="24"
                  height="24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
            </div>
            <div className="flex flex-col gap-6 px-5 py-6 text-sm">
              <button
                onClick={() => {
                  router.push("/landing");
                  setIsMenuOpen(false);
                }}
                className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors"
              >
                Home
              </button>
              <button
                onClick={() => {
                  router.push("/how-it-works");
                  setIsMenuOpen(false);
                }}
                className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors"
              >
                How it Works
              </button>
              <button
                onClick={() => {
                  router.push("/about");
                  setIsMenuOpen(false);
                }}
                className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors"
              >
                About
              </button>
            </div>
            <div className="mt-5 px-5 pb-8">
              <Button
                onClick={() => {
                  if (hasToken) {
                    router.push("/dashboard");
                  } else {
                    handleGetStarted();
                  }
                  setIsMenuOpen(false);
                }}
                disabled={authLoading}
                className="w-full justify-center px-4 py-1.5 bg-gray-800 hover:bg-gray-700 text-white rounded-md transition-colors border border-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {hasToken ? "Go Dashboard" : "Get Started"}
              </Button>
            </div>
          </aside>
        </div>
      )}

      

      {/* Hero Section */}
      <section className="relative hero-section-wrapper">
        {/* Background Image Container - Content is positioned within this */}
        <div
          className="absolute inset-x-0 hero-bg-image hero-image-container"
          style={{
            top: "4rem",
            overflow: "hidden",
            zIndex: 1,
          }}
        >
          {/* Background Image */}
          <div
            className="absolute inset-0 bg-cover bg-center bg-no-repeat bg-black"
            style={{
              backgroundImage: "url(/image/Herosection.jpg)",
            }}
          />

          {/* Dark overlay */}
          <div className="absolute inset-0 bg-black/60 hero-bg-overlay" />

          {/* Content positioned within the image container */}
          <div className="absolute inset-0 flex items-center justify-center hero-content-wrapper">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full relative z-10">
              <div
                className="text-center max-w-5xl mx-auto"
                style={{ perspective: "1000px" }}
              >
                <Reveal
                  className="inline-flex items-center gap-2 px-3 py-1.5 sm:px-4 sm:py-2 rounded-md bg-[#1a1a1a] border border-[#2a2a2a] mb-6 sm:mb-8"
                  rootMargin="-100px"
                  threshold={0.2}
                >
                  <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                  <span className="text-xs sm:text-sm text-gray-400">
                    AI-Powered Career Guidance for Cambodian Students
                  </span>
                </Reveal>

                <Reveal rootMargin="-100px" threshold={0.2}>
                  <h1 className="hero-title">
                    Your future starts
                    <br />
                    <span className="text-white">with insight</span>
                  </h1>
                </Reveal>

                <Reveal
                  className="hero-description-text"
                  rootMargin="-100px"
                  threshold={0.2}
                >
                  Transform your BacII grades into a personalized roadmap.
                  Discover your ideal major, career path, and university powered
                  by AI.
                </Reveal>

                <Reveal
                  className="flex justify-center items-center mt-8 sm:mt-10 md:mt-12"
                  rootMargin="-100px"
                  threshold={0.2}
                >
                  <Button
                    onClick={
                      hasToken ? () => router.push("/dashboard") : handleGetStarted
                    }
                    size="lg"
                    disabled={authLoading}
                    className="group hero-cta-button rounded-lg bg-gray-800 hover:bg-gray-700 text-white transition-colors border border-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {hasToken ? "Go Dashboard" : "Get Started"}
                    {!authLoading && <ArrowRight className="hero-cta-icon ml-2 group-hover:translate-x-1 transition-transform" />}
                  </Button>
                </Reveal>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Cards and Input Section */}
      <section className="relative py-24">
        <div className="max-w-7xl mx-auto px-6 relative z-10">
          {/* Hero Visual - Bento Grid */}
          <div
            className="mt-[-6rem] relative"
            style={{ perspective: "1000px" }}
          >
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 max-w-6xl mx-auto">
              {/* Large Card */}
              <Reveal
                className="md:col-span-2 relative rounded-lg bg-[#111111] border border-[#1f1f1f] p-8 overflow-hidden group hover:border-[#2a2a2a] transition-colors"
                rootMargin="-100px"
                threshold={0.2}
                onReveal={() => {
                  // Wait for reveal animation to complete (0.6s) before starting progress bars
                  setTimeout(() => {
                    setIsAnalysisCardRevealed(true);
                  }, 600);
                }}
              >
                <div className="relative">
                  <div className="flex items-center gap-3 mb-6">
                    <div className="w-10 h-10 rounded-lg bg-[#1a1a1a] border border-[#2a2a2a] flex items-center justify-center">
                      <Brain className="w-5 h-5 text-blue-500" />
                    </div>
                    <div>
                      <h3 className="text-white">AI Analysis Engine</h3>
                      <p className="text-sm text-gray-500">
                        Personalized recommendations
                      </p>
                    </div>
                  </div>
                  <div className="space-y-3">
                    {[
                      { value: 94, label: "Recommendation Accuracy" },
                      { value: 92, label: "User Satisfaction" },
                      { value: 95, label: "University Match Success" },
                    ].map((item, i) => (
                      <div key={i}>
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-xs text-gray-400">
                            {item.label}
                          </span>
                          <span className="text-sm text-gray-500 w-12 text-right">
                            {item.value}%
                          </span>
                        </div>
                        <div className="flex-1 h-1.5 bg-[#1a1a1a] rounded-full overflow-hidden">
                          <div
                            className="h-full bg-blue-500 progress-bar-smooth"
                            style={
                              {
                                "--target-width": `${item.value}%`,
                                width: "0%",
                                animation: isAnalysisCardRevealed
                                  ? `progressFill 1.2s cubic-bezier(0.4, 0, 0.2, 1) ${
                                      i * 0.15
                                    }s forwards`
                                  : "none",
                                transformOrigin: "left",
                                willChange: "width",
                              } as React.CSSProperties & {
                                "--target-width": string;
                              }
                            }
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
                  <h4 className="text-white" style={{ marginBottom: "1rem" }}>
                    Instant Insights
                  </h4>
                  <p className="text-sm text-gray-500">
                    Real-time analysis in seconds upload your grades and
                    instantly see trends, strengths, and next‑step
                    recommendations. Get subject-level breakdowns, targeted
                    improvement tips, and suggested majors without waiting.
                  </p>
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
                  <h4 className="text-white" style={{ marginBottom: "1rem" }}>
                    92% Accuracy
                  </h4>
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
                      { name: "Mathematics", icon: BarChart3 },
                      { name: "Sciences", icon: Microscope },
                      { name: "Languages", icon: Globe },
                    ].map((subject, i) => (
                      <div
                        key={i}
                        className="text-center flex flex-col items-center"
                      >
                        <div className="w-14 h-14 rounded-lg bg-[#1a1a1a] border border-[#2a2a2a] flex items-center justify-center mb-3">
                          <subject.icon className="w-6 h-6 text-gray-600" />
                        </div>
                        <p className="text-sm text-gray-500 subject-category-name">
                          {subject.name}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              </Reveal>
            </div>
          </div>

          {/* Interactive Input Section - Small Compact Version */}
          <Reveal className="mt-10 mb-8" rootMargin="-100px" threshold={0.2}>
            <div className="max-w-4xl mx-auto">
              <div className="mb-10 text-center mt-10">
                <p className="text-gray-300 text-lg">
                  Fill out the form below to see how it works
                </p>
              </div>
              <div className="rounded-lg border border-[#1f1f1f] bg-[#111111] overflow-hidden hover:border-[#2a2a2a] transition-colors">
                {/* Desktop Two Column Layout */}
                <div className="hidden lg:grid lg:grid-cols-2 gap-0">
                  {/* Left Column - Ready for Analysis */}
                  <div className="min-h-full overflow-y-auto relative">
                    {/* Background layer with filter */}
                    <div
                      className="absolute inset-0 bg-cover bg-center bg-no-repeat"
                      style={{
                        backgroundImage: "url(/image/Ultravib.png)",
                        backgroundSize: "cover",
                        backgroundPosition: "center",
                        backgroundRepeat: "no-repeat",
                        filter: "brightness(0.9)",
                        zIndex: 0,
                      }}
                    />
                    {/* Content layer */}
                    <div className="flex items-center justify-center h-full p-4 relative z-10">
                      <div className="text-center">
                        <div className="w-10 h-10 flex items-center justify-center mx-auto mb-2">
                          <svg
                            className="w-8 h-8 text-blue-400"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                            />
                          </svg>
                        </div>
                        <h3 className="text-base font-semibold text-white mb-1">
                          Ready for Analysis
                        </h3>
                        <p className="text-gray-200 text-xs max-w-[200px] mt-1">
                          Fill out the form on the right to get your personalized academic insights recommendations.
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Right Column - Input Form */}
                  <div className="bg-[#111111] border-l border-[#1f1f1f] min-h-full overflow-y-auto">
                    <div className="p-4">
                      <div className="mb-4 text-center">
                        <div className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md bg-[#1a1a1a] border border-[#2a2a2a] mb-3">
                          <div className="w-1 h-1 rounded-full bg-blue-500" />
                          <span className="text-[10px] text-gray-500">
                            Academic Profile Analysis
                          </span>
                        </div>
                        <p className="text-gray-300 text-xs">
                          Enter your BacII grades and interests
                        </p>
                      </div>

                      <form
                        onSubmit={(e) => {
                          e.preventDefault();
                          router.push("/login");
                        }}
                        style={{ width: "100%" }}
                      >
                        <div
                          style={{
                            display: "flex",
                            flexDirection: "column",
                            gap: "12px",
                          }}
                        >
                          {/* Grades Section */}
                          <div>
                            <div className="grid-2-col">
                              {[
                                {
                                  id: "math",
                                  name: "Mathematics",
                                  category: "Science",
                                  maxScore: 125,
                                },
                                {
                                  id: "physics",
                                  name: "Physics",
                                  category: "Science",
                                  maxScore: 75,
                                },
                                {
                                  id: "chemistry",
                                  name: "Chemistry",
                                  category: "Science",
                                  maxScore: 75,
                                },
                                {
                                  id: "biology",
                                  name: "Biology",
                                  category: "Science",
                                  maxScore: 75,
                                },
                                {
                                  id: "khmer",
                                  name: "Khmer Literature",
                                  category: "Language",
                                  maxScore: 75,
                                },
                                {
                                  id: "english",
                                  name: "English",
                                  category: "Language",
                                  maxScore: 50,
                                },
                                {
                                  id: "history",
                                  name: "History",
                                  category: "Social Studies",
                                  maxScore: 50,
                                },
                              ].map((subject) => (
                                <div
                                  key={subject.id}
                                  style={{
                                    padding: "8px",
                                    transition: "all 0.2s ease",
                                  }}
                                >
                                  <label
                                    style={{
                                      fontSize: "10px",
                                      fontWeight: "500",
                                      marginBottom: "4px",
                                      color: "#ffffff",
                                      display: "block",
                                    }}
                                  >
                                    {subject.name}
                                    <span
                                      style={{
                                        color: "#9ca3af",
                                        fontSize: "9px",
                                        fontWeight: "400",
                                        marginLeft: "4px",
                                      }}
                                    >
                                      ({subject.category}) - Max:{" "}
                                      {subject.maxScore}
                                    </span>
                                  </label>
                                  <input
                                    type="text"
                                    inputMode="numeric"
                                    pattern="[0-9]*"
                                    placeholder={`0-${subject.maxScore}`}
                                    className="input-field"
                                    value={grades[subject.id] || ""}
                                    onChange={(e) =>
                                      setGrades((prev) => ({
                                        ...prev,
                                        [subject.id]: e.target.value,
                                      }))
                                    }
                                    style={{
                                      margin: 0,
                                      fontSize: "11px",
                                      padding: "6px 8px",
                                    }}
                                  />
                                </div>
                              ))}
                            </div>
                          </div>

                          {/* Interests Section */}
                          <div>
                            <h4
                              style={{
                                fontSize: "13px",
                                fontWeight: "600",
                                marginBottom: "4px",
                                color: "#ffffff",
                              }}
                            >
                              Your Interests & Strengths
                            </h4>
                            <p
                              style={{
                                color: "#9ca3af",
                                fontSize: "10px",
                                marginBottom: "6px",
                              }}
                            >
                              Describe your interests, hobbies, and skills...
                            </p>
                            <textarea
                              className="input-field"
                              style={{
                                minHeight: "50px",
                                resize: "vertical",
                                fontFamily: "inherit",
                                lineHeight: "1.4",
                                fontSize: "11px",
                                padding: "6px 8px",
                              }}
                              placeholder="I love programming and building apps..."
                              value={interestText}
                              onChange={(e) => setInterestText(e.target.value)}
                              required
                            />
                          </div>

                          {/* Career Goals Section */}
                          <div>
                            <h4
                              style={{
                                fontSize: "13px",
                                fontWeight: "600",
                                marginBottom: "4px",
                                color: "#ffffff",
                              }}
                            >
                              Career Goals (Optional)
                            </h4>
                            <p
                              style={{
                                color: "#9ca3af",
                                fontSize: "10px",
                                marginBottom: "6px",
                              }}
                            >
                              What kind of career are you interested in?
                            </p>
                            <textarea
                              className="input-field"
                              style={{
                                minHeight: "45px",
                                resize: "vertical",
                                fontFamily: "inherit",
                                lineHeight: "1.4",
                                fontSize: "11px",
                                padding: "6px 8px",
                              }}
                              placeholder="I want to become a software engineer..."
                              value={careerGoals}
                              onChange={(e) => setCareerGoals(e.target.value)}
                            />
                          </div>

                          {/* Submit Button */}
                          <div style={{ paddingTop: "8px" }}>
                            <button
                              type="submit"
                              disabled={!isFormValid()}
                              className="px-4 py-1.5 text-white rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                              style={{
                                width: "100%",
                                backgroundColor: isFormValid()
                                  ? "#1d4ed8"
                                  : "#1f2937",
                                borderWidth: "1px",
                                borderStyle: "solid",
                                borderColor: isFormValid()
                                  ? "#1d4ed8"
                                  : "#374151",
                                padding: "8px 12px",
                                fontSize: "12px",
                                fontWeight: "500",
                              }}
                              onMouseEnter={(e) => {
                                if (isFormValid()) {
                                  e.currentTarget.style.backgroundColor =
                                    "#1e40af";
                                  e.currentTarget.style.borderColor = "#1e40af";
                                }
                              }}
                              onMouseLeave={(e) => {
                                if (isFormValid()) {
                                  e.currentTarget.style.backgroundColor =
                                    "#1d4ed8";
                                  e.currentTarget.style.borderColor = "#1d4ed8";
                                }
                              }}
                            >
                              Analyze My Results
                            </button>
                          </div>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>

                {/* Mobile: Hero with slide-up form button */}
                <div className="lg:hidden relative overflow-hidden" style={{ minHeight: '500px', height: '70vh', maxHeight: '700px' }}>
                  <div
                    className="absolute inset-0 bg-cover bg-center bg-no-repeat"
                    style={{
                      backgroundImage: "url(/image/Ultravib.png)",
                      backgroundSize: "cover",
                      backgroundPosition: "center",
                      backgroundRepeat: "no-repeat",
                      filter: "brightness(0.9)",
                      zIndex: 0,
                    }}
                  />
                  <div className="relative flex flex-col items-center justify-center px-6 text-center" style={{ minHeight: '500px', height: '70vh', maxHeight: '700px', zIndex: 1 }}>
                    <div className="w-10 h-10 flex items-center justify-center mx-auto mb-2">
                      <svg
                        className="w-8 h-8 text-blue-400"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                      </svg>
                    </div>
                    <h3 className="text-base font-semibold text-white mb-1">
                      Ready for Analysis
                    </h3>
                    <p className="text-gray-300 text-xs max-w-[250px] mt-1 mb-4">
                     Fill out the form to get your personalized academic insights recommendations.
                    </p>
                    <button
                      onClick={() => setIsMobileFormOpen(true)}
                      className="px-4 py-2 bg-gray-800 hover:bg-gray-700 border border-gray-600 text-white rounded-full text-sm font-semibold transition-colors shadow-lg"
                    >
                      Open input form
                    </button>
                  </div>

                  {/* Backdrop */}
                  <div
                    className={`absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity duration-300 ${
                      isMobileFormOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'
                    }`}
                    onClick={() => setIsMobileFormOpen(false)}
                    style={{ zIndex: 50 }}
                  />

                  {/* Mobile bottom sheet form */}
                  <div
                    className={`absolute bottom-0 left-0 right-0 bg-[#0b0b0b] border border-[#1f1f1f] rounded-t-3xl shadow-2xl transition-transform duration-300 ease-out ${
                      isMobileFormOpen ? 'translate-y-0' : 'translate-y-full'
                    }`}
                    style={{ height: '85%', zIndex: 60 }}
                  >
                    <div className="h-full overflow-y-auto px-6 pt-6 pb-8 scrollbar-hide" style={{ WebkitOverflowScrolling: 'touch' }}>
                      <div className="w-12 h-1.5 bg-gray-600 rounded-full mx-auto mb-4" />
                      <div className="flex items-center justify-center mb-6">
                        <div className="text-center">
                          <div className="inline-flex items-center gap-2 px-3 py-2 rounded-md bg-[#1a1a1a] border border-[#2a2a2a]">
                            <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                            <span className="text-sm text-gray-400">Academic Profile Analysis</span>
                          </div>
                        </div>
                      </div>

                      <form
                        onSubmit={(e) => {
                          e.preventDefault();
                          router.push("/login");
                        }}
                        style={{ width: "100%" }}
                      >
                        <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
                          {/* Grades Section */}
                          <div>
                            <div className="grid grid-cols-2 gap-4">
                              {[
                                { id: "math", name: "Mathematics", category: "Science", maxScore: 125 },
                                { id: "physics", name: "Physics", category: "Science", maxScore: 75 },
                                { id: "chemistry", name: "Chemistry", category: "Science", maxScore: 75 },
                                { id: "biology", name: "Biology", category: "Science", maxScore: 75 },
                                { id: "khmer", name: "Khmer Literature", category: "Language", maxScore: 75 },
                                { id: "english", name: "English", category: "Language", maxScore: 50 },
                                { id: "history", name: "History", category: "Social Studies", maxScore: 50 },
                              ].map((subject) => (
                                <div key={subject.id} style={{ transition: "all 0.2s ease" }}>
                                  <label
                                    style={{
                                      fontSize: "13px",
                                      fontWeight: "500",
                                      marginBottom: "6px",
                                      color: "#ffffff",
                                      display: "block",
                                    }}
                                  >
                                    {subject.name}
                                    <span
                                      style={{
                                        color: "#9ca3af",
                                        fontSize: "11px",
                                        fontWeight: "400",
                                        marginLeft: "4px",
                                      }}
                                    >
                                      (Max: {subject.maxScore})
                                    </span>
                                  </label>
                                  <input
                                    type="text"
                                    inputMode="numeric"
                                    pattern="[0-9]*"
                                    placeholder={`0-${subject.maxScore}`}
                                    className="input-field"
                                    value={grades[subject.id] || ""}
                                    onChange={(e) =>
                                      setGrades((prev) => ({
                                        ...prev,
                                        [subject.id]: e.target.value,
                                      }))
                                    }
                                    style={{ margin: 0, fontSize: "14px", padding: "10px 12px" }}
                                  />
                                </div>
                              ))}
                            </div>
                          </div>

                          {/* Interests Section */}
                          <div>
                            <h4 style={{ fontSize: "15px", fontWeight: "600", marginBottom: "8px", color: "#ffffff" }}>
                              Your Interests & Strengths
                            </h4>
                            <p style={{ color: "#9ca3af", fontSize: "13px", marginBottom: "8px" }}>
                              Describe your interests, hobbies, and skills...
                            </p>
                            <textarea
                              className="input-field"
                              style={{
                                minHeight: "80px",
                                resize: "vertical",
                                fontFamily: "inherit",
                                lineHeight: "1.5",
                                fontSize: "14px",
                                padding: "10px 12px",
                              }}
                              placeholder="I love programming and building apps..."
                              value={interestText}
                              onChange={(e) => setInterestText(e.target.value)}
                              required
                            />
                          </div>

                          {/* Career Goals Section */}
                          <div>
                            <h4 style={{ fontSize: "15px", fontWeight: "600", marginBottom: "8px", color: "#ffffff" }}>
                              Career Goals (Optional)
                            </h4>
                            <p style={{ color: "#9ca3af", fontSize: "13px", marginBottom: "8px" }}>
                              What kind of career are you interested in?
                            </p>
                            <textarea
                              className="input-field"
                              style={{
                                minHeight: "70px",
                                resize: "vertical",
                                fontFamily: "inherit",
                                lineHeight: "1.5",
                                fontSize: "14px",
                                padding: "10px 12px",
                              }}
                              placeholder="I want to become a software engineer..."
                              value={careerGoals}
                              onChange={(e) => setCareerGoals(e.target.value)}
                            />
                          </div>

                          {/* Submit Button */}
                          <div style={{ paddingTop: "8px" }}>
                            <button
                              type="submit"
                              disabled={!isFormValid()}
                              className="px-4 py-3 text-white rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                              style={{
                                width: "100%",
                                backgroundColor: isFormValid() ? "#1d4ed8" : "#1f2937",
                                borderWidth: "1px",
                                borderStyle: "solid",
                                borderColor: isFormValid() ? "#1d4ed8" : "#374151",
                                fontSize: "15px",
                                fontWeight: "600",
                              }}
                              onMouseEnter={(e) => {
                                if (isFormValid()) {
                                  e.currentTarget.style.backgroundColor =
                                    "#1e40af";
                                  e.currentTarget.style.borderColor = "#1e40af";
                                }
                              }}
                              onMouseLeave={(e) => {
                                if (isFormValid()) {
                                  e.currentTarget.style.backgroundColor =
                                    "#1d4ed8";
                                  e.currentTarget.style.borderColor = "#1d4ed8";
                                }
                              }}
                            >
                              
                              Analyze My Results
                            </button>
                          </div>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      {/* Key Benefits */}
      <section className="py-32 relative">
        <div className="max-w-7xl mx-auto px-6 relative z-10">
          <Reveal className="text-center mb-20">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-md bg-[#1a1a1a] border border-[#2a2a2a] mb-6">
              <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
              <span className="text-sm text-gray-500">Features</span>
            </div>
            <h2
              className="text-5xl md:text-6xl text-white"
              style={{ marginBottom: "2rem" }}
            >
              Everything you need
            </h2>
            <p className="text-gray-200 text-xl max-w-2xl mx-auto">
              Built specifically for Cambodian BacII students with cutting-edge
              AI technology
            </p>
          </Reveal>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
            {[
              {
                icon: Brain,
                title: "AI-Powered Insights",
                description:
                  "Personalized majors, careers, and universities tailored to your profile",
                lottie: aiAnimationData,
              },
              {
                icon: TrendingUp,
                title: "Built for BacII",
                description:
                  "Subject max scores, normalization, and Cambodian educational context",
                lottie: bacIIAnimationData,
              },
              {
                icon: Target,
                title: "Actionable Next Steps",
                description:
                  "Clear skill gaps and how to improve with specific suggestions",
                lottie: nextStepAnimationData,
              },
              {
                icon: Shield,
                title: "Private & Secure",
                description:
                  "Your data, your control. All analysis happens locally",
                lottie: securityAnimationData,
              },
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
                    <h3 className="text-white" style={{ marginBottom: "1rem" }}>
                      {benefit.title}
                    </h3>
                    <p className="text-gray-500 text-sm leading-relaxed mb-4">
                      {benefit.description}
                    </p>
                    {benefit.lottie && (
                      <div className="mt-auto flex justify-center items-center">
                        <Lottie
                          animationData={benefit.lottie}
                          loop
                          autoplay
                          className="w-full max-w-[200px] sm:max-w-[240px] md:max-w-[300px] h-auto"
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
            <h2
              className="text-5xl md:text-6xl text-white"
              style={{ marginBottom: "2rem" }}
            >
              Three steps to clarity
            </h2>
            <p className="text-gray-200 text-xl max-w-2xl mx-auto">
              From grades to guidance in minutes
            </p>
          </Reveal>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 relative">
            {/* Connecting Line */}
            <div className="hidden lg:block absolute top-16 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[rgba(179,179,179,0.3)] to-transparent" />

            {[
              {
                step: "01",
                title: "Enter Your Grades",
                description:
                  "Input your BacII exam results and tell us about your interests and goals",
                icon: BarChart3,
                image: "enter-grade.png",
              },
              {
                step: "02",
                title: "AI Analysis",
                description:
                  "Our AI analyzes your strengths, preferences, and career aspirations",
                icon: Brain,
                image: "analysis.png",
              },
              {
                step: "03",
                title: "Get Recommendations",
                description:
                  "Receive personalized majors, careers, and universities with skill-gap guidance",
                icon: Target,
                image: "recommendation.png",
              },
            ].map((step, idx) => (
              <Reveal
                key={idx}
                translateY={true}
                delay={idx * 200}
                className="relative"
              >
                <div className="relative p-6 rounded-lg bg-[#111111] border border-[#1f1f1f] hover:border-[#2a2a2a] transition-colors group h-full">
                  {/* Step Number */}
                  <div className="relative flex items-center justify-center w-12 h-12 mb-6 rounded-lg bg-[#1a1a1a] border border-[#2a2a2a]">
                    <span className="text-lg text-gray-600">{step.step}</span>
                  </div>

                  {/* Icon */}
                  <div className="w-10 h-10 rounded-lg bg-blue-600/10 border border-blue-600/20 flex items-center justify-center mb-6">
                    <step.icon className="w-5 h-5 text-blue-500" />
                  </div>

                  <h3 className="text-white" style={{ marginBottom: "1rem" }}>
                    {step.title}
                  </h3>
                  <p className="text-gray-500 text-sm leading-relaxed">
                    {step.description}
                  </p>
                  {/* Image in bordered container */}
                  <div className="mt-8 rounded-lg bg-transparent overflow-hidden relative">
                    <Image
                      src={`/image/${step.image}`}
                      alt={step.title}
                      width={800}
                      height={640}
                      quality={100}
                      className="w-full h-auto object-contain rounded-lg"
                    />
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
            <h2
              className="text-5xl md:text-6xl text-white"
              style={{ marginBottom: "2rem" }}
            >
              Deep analysis, clear results
            </h2>
            <p className="text-gray-200 text-xl max-w-2xl mx-auto">
              Everything you need to make informed decisions about your future
            </p>
          </Reveal>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
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
                <h3
                  className="text-white text-xl"
                  style={{ marginBottom: "1rem" }}
                >
                  Subject Analysis
                </h3>
                <p className="text-gray-500 text-sm leading-relaxed mb-6">
                  See your strengths across Math, Physics, Chemistry, Biology,
                  Khmer, English, and History with detailed performance
                  breakdowns and insights.
                </p>
                <div className="mt-auto flex flex-col gap-4">
                  <div className="flex gap-4">
                    <div className="flex-1 flex flex-col gap-2">
                      <div className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                        <span className="text-sm text-gray-600">Mathematics: Strong</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                        <span className="text-sm text-gray-600">Physics: Moderate</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                        <span className="text-sm text-gray-600">Khmer Literature: Strong</span>
                      </div>
                    </div>
                    <div className="flex-1 flex flex-col gap-2">
                      <div className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                        <span className="text-sm text-gray-600">Chemistry: Moderate</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                        <span className="text-sm text-gray-600">Biology: Moderate</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                        <span className="text-sm text-gray-600">English: Strong</span>
                      </div>
                    </div>
                    <div className="flex-1 flex flex-col gap-2">
                      <div className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                        <span className="text-sm text-gray-600">History: Moderate</span>
                      </div>
                    </div>
                  </div>
                  {subjectAnalysisAnimationData && (
                    <div className="flex items-center justify-center subject-analysis-lottie-container">
                      <Lottie
                        animationData={subjectAnalysisAnimationData}
                        loop={true}
                        autoplay={true}
                        style={{ width: "100%", maxWidth: 350, height: "auto" }}
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
                <h3 className="text-white" style={{ marginBottom: "1rem" }}>
                  Recommendation Engine
                </h3>
                <p className="text-gray-500 text-sm leading-relaxed mb-4">
                  Get majors, careers, and universities with match scores and
                  detailed breakdowns
                </p>
                {recommendationEngineAnimationData && (
                  <div className="mt-auto flex justify-center items-center">
                    <Lottie
                      animationData={recommendationEngineAnimationData}
                      loop={true}
                      autoplay={true}
                      style={{ width: "100%", maxWidth: 150, height: "auto" }}
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
                <h3 className="text-white" style={{ marginBottom: "1rem" }}>
                  Skill Development
                </h3>
                <p className="text-gray-500 text-sm leading-relaxed mb-4">
                  Current vs target levels with improvement plans
                </p>
                {skillDevelopmentAnimationData && (
                  <div className="mt-auto flex justify-center items-center">
                    <Lottie
                      animationData={skillDevelopmentAnimationData}
                      loop={true}
                      autoplay={true}
                      style={{ width: "100%", maxWidth: 220, height: "auto" }}
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
                <h3 className="text-white" style={{ marginBottom: "1rem" }}>
                  Cambodia Focused
                </h3>
                <p className="text-gray-500 text-sm leading-relaxed mb-4">
                  Specialized recommendations for Cambodian universities
                </p>
                {cambodiaAnimationData && (
                  <div className="mt-auto flex justify-center items-center">
                    <Lottie
                      animationData={cambodiaAnimationData}
                      loop={true}
                      autoplay={true}
                      style={{ width: "100%", maxWidth: 150, height: "auto" }}
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
              <span className="text-sm text-gray-500">
                Partner Universities
              </span>
            </div>
            <h2
              className="text-5xl md:text-6xl text-white"
              style={{ marginBottom: "2rem" }}
            >
              Top Cambodian Universities
            </h2>
            <p className="text-gray-200 text-xl max-w-2xl mx-auto">
              Based on your recommended major, we match you with the best
              universities in Cambodia
            </p>
          </Reveal>

          {/* 2 Column Grid Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Left Column - Description */}
            <Reveal translateX={-20} className="space-y-6">
              <div className="space-y-4">
                <h3 className="text-3xl md:text-4xl text-white font-bold">
                  Your Perfect University Match
                </h3>
                <p className="text-gray-400 text-lg leading-relaxed">
                  Our AI-powered system analyzes your academic performance and
                  career goals to recommend the most suitable universities for
                  your chosen major. All partner institutions are accredited and
                  recognized leaders in their fields.
                </p>
              </div>

              <div className="space-y-4">
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 rounded-lg  bg-[#1a1a1a] border border-[#2a2a2a] flex items-center justify-center flex-shrink-0 mt-1">
                    <CheckCircle2 className="w-5 h-5 text-blue-500" />
                  </div>
                  <div>
                    <h4 className="text-white font-semibold mb-1">
                      Accredited Programs
                    </h4>
                    <p className="text-gray-400 text-sm">
                      All universities offer internationally recognized degrees
                      and certifications
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 rounded-lg  bg-[#1a1a1a] border border-[#2a2a2a] flex items-center justify-center flex-shrink-0 mt-1">
                    <Award className="w-5 h-5 text-blue-500" />
                  </div>
                  <div>
                    <h4 className="text-white font-semibold mb-1">
                      Specialized Excellence
                    </h4>
                    <p className="text-gray-400 text-sm">
                      Each institution excels in specific fields matching your
                      interests
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 rounded-lg  bg-[#1a1a1a] border border-[#2a2a2a] flex items-center justify-center flex-shrink-0 mt-1">
                    <Target className="w-5 h-5 text-blue-500" />
                  </div>
                  <div>
                    <h4 className="text-white font-semibold mb-1">
                      Career-Focused
                    </h4>
                    <p className="text-gray-400 text-sm">
                      Strong industry connections and high graduate employment
                      rates
                    </p>
                  </div>
                </div>
              </div>
            </Reveal>

            {/* Right Column - Infinite Scroll */}
            <Reveal translateX={20} className="relative mt-6">
              <InfiniteScroll
                items={[
                  {
                    content: (
                      <div className="text-white text-xs p-2">
                        Cambodia Academy of Digital Technology (CADT)
                      </div>
                    ),
                  },
                  {
                    content: (
                      <div className="text-white text-xs p-2">
                        Royal University of Phnom Penh (RUPP)
                      </div>
                    ),
                  },
                  {
                    content: (
                      <div className="text-white text-xs p-2">
                        Institute of Technology of Cambodia (ITC)
                      </div>
                    ),
                  },
                  {
                    content: (
                      <div className="text-white text-xs p-2">
                        Phnom Penh International University (PPIU)
                      </div>
                    ),
                  },
                  {
                    content: (
                      <div className="text-white text-xs p-2">
                        Western University
                      </div>
                    ),
                  },
                  {
                    content: (
                      <div className="text-white text-xs p-2">
                        Royal University of Law and Economics (RULE)
                      </div>
                    ),
                  },
                  {
                    content: (
                      <div className="text-white text-xs p-2">
                        Build Bright University (BBU)
                      </div>
                    ),
                  },
                  {
                    content: (
                      <div className="text-white text-xs p-2">
                        University of Cambodia (UC)
                      </div>
                    ),
                  },
                  {
                    content: (
                      <div className="text-white text-xs p-2">
                        American University of Phnom Penh (AUPP)
                      </div>
                    ),
                  },
                  {
                    content: (
                      <div className="text-white text-xs p-2">
                        National University of Management (NUM)
                      </div>
                    ),
                  },
                  {
                    content: (
                      <div className="text-white text-xs p-2">
                        Royal University of Fine Arts (RUFA)
                      </div>
                    ),
                  },
                  {
                    content: (
                      <div className="text-white text-xs p-2">
                        University of Health Sciences (UHS)
                      </div>
                    ),
                  },
                  {
                    content: (
                      <div className="text-white text-xs p-2">
                        Paññāsāstra University of Cambodia (PUC)
                      </div>
                    ),
                  },
                  {
                    content: (
                      <div className="text-white text-xs p-2">
                        Paragon International University
                      </div>
                    ),
                  },
                  {
                    content: (
                      <div className="text-white text-xs p-2">
                        University of Puthisastra (UP)
                      </div>
                    ),
                  },
                  {
                    content: (
                      <div className="text-white text-xs p-2">
                        National Polytechnic Institute of Cambodia (NPIC)
                      </div>
                    ),
                  },
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
            <h2
              className="text-5xl md:text-6xl text-white"
              style={{ marginBottom: "2rem" }}
            >
              Ready to discover your path?
            </h2>
            <p className="text-xl text-gray-200 mb-12 max-w-2xl mx-auto">
              Join thousands of Cambodian students who have found clarity in
              their academic journey
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Button
                onClick={
                  hasToken ? () => router.push("/dashboard") : handleGetStarted
                }
                size="lg"
                disabled={authLoading}
                className="group px-8 py-3 rounded-lg bg-gray-800 hover:bg-gray-700 text-white transition-colors border border-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {hasToken ? "Go Dashboard" : "Get Started"}
                {!authLoading && <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />}
              </Button>
            </div>
          </Reveal>
        </div>
      </section>

      {/* Footer */}
      <footer
        className="py-16 border-t relative z-20 footer-container border-white/10"
        >
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center pt-2 gap-8 footer-content">
            {/* Logo and Description */}
            <div className="flex flex-col footer-logo-section">
              <div className="flex items-center gap-2 mb-4 footer-logo">
                <img
                  src="/image/Bontor-logo.png"
                  alt="Bontor"
                  style={{
                    height: "24px",
                    width: "auto",
                  }}
                />
              </div>
              <p className="text-gray-300 text-sm leading-relaxed max-w-xs footer-description">
                AI-powered career guidance platform designed specifically for
                Cambodian BacII students. Transform your grades into
                personalized major and university recommendations.
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
                        onClick={() => router.push("/landing")}
                        className="text-gray-300 hover:text-blue-500 transition-colors text-sm"
                      >
                        Home
                      </button>
                    </li>
                    <li>
                      <button
                        onClick={() => router.push("/how-it-works")}
                        className="text-gray-300 hover:text-blue-500 transition-colors text-sm"
                      >
                        How it Works
                      </button>
                    </li>
                    <li>
                      <button
                        onClick={() => router.push("/about")}
                        className="text-gray-300 hover:text-blue-500 transition-colors text-sm"
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
                        onClick={() => router.push("/login")}
                        className="text-gray-300 hover:text-blue-500 transition-colors text-sm"
                      >
                        Login
                      </button>
                    </li>
                    <li>
                      <button
                        onClick={() => router.push("/signup")}
                        className="text-gray-300 hover:text-blue-500 transition-colors text-sm"
                      >
                        Register
                      </button>
                    </li>
                  </ul>
                </div>
              </div>
              <div className="pt-4 border-t border-white/10 footer-copyright">
                <p className="text-gray-300 text-sm">
                  © {new Date().getFullYear()} Bontor Smart BacII Grade & Career Analyzer. All rights
                  reserved.
                </p>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default function LandingPage() {
  return (
    <Suspense fallback={<div></div>}>
      <LandingPageContent />
    </Suspense>
  );
}
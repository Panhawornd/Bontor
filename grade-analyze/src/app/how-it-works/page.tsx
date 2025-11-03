"use client";

import React, { useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import Button from "@/components/ui/Button";
import { FileSpreadsheet, SlidersHorizontal, Sparkles, MessageSquare } from "lucide-react";

const steps = [
  {
    id: "step-1",
    title: "Enter Your Grades",
    description:
      "Input your BacII subject grades. We securely process your data to prepare a detailed analysis.",
    icon: FileSpreadsheet,
  },
  {
    id: "step-2",
    title: "Enter Preferences",
    description:
      "Tell us your interests, strengths, and goals. We factor these into your recommended majors and paths.",
    icon: SlidersHorizontal,
  },
  {
    id: "step-3",
    title: "Get Recommendations",
    description:
      "Receive AI-powered matches: suggested majors, universities, and skills to focus on—instantly.",
    icon: Sparkles,
  },
  {
    id: "step-4",
    title: "Chat with the Agent",
    description:
      "Ask follow-up questions and learn what skills to build next to prepare for your chosen major.",
    icon: MessageSquare,
  },
];

export default function HowItWorksPage() {
  const router = useRouter();
  const sectionRefs = useRef<Record<string, HTMLElement | null>>({});
  const [activeIndex, setActiveIndex] = useState(0);
  const [hasToken, setHasToken] = useState<boolean | null>(null);
  const [metrics, setMetrics] = useState<number[]>([]);
  const [progressPct, setProgressPct] = useState<number>(0);

  useEffect(() => {
    const cookies = document.cookie;
    const hasAuthToken = cookies.includes("auth-token=");
    setHasToken(hasAuthToken);
  }, []);

  const ids = useMemo(() => steps.map((s) => s.id), []);

  // Helper: compute real-time progress based on scroll position
  const computeProgress = () => {
    if (ids.length === 0) return;
    const first = sectionRefs.current[ids[0]];
    const last = sectionRefs.current[ids[ids.length - 1]];
    if (!first || !last) return;

    const startY = first.offsetTop;
    const endY = last.offsetTop + last.offsetHeight;

    // Use a point slightly below the top to match timeline perception
    const indicatorY = window.scrollY + window.innerHeight * 0.3;
    const span = Math.max(1, endY - startY);
    const raw = (indicatorY - startY) / span;
    const clamped = Math.min(1, Math.max(0, raw));
    setProgressPct(clamped * 100);
  };

  // Measure right-side section heights and mirror to left timeline items
  useEffect(() => {
    const measure = () => {
      const values = ids.map((id, idx) => {
        const el = sectionRefs.current[id];
        if (!el) return 0;
        const rect = el.getBoundingClientRect();
        const gap = idx < ids.length - 1 ? 96 : 0;
        return Math.max(120, Math.round(rect.height + gap));
      });
      setMetrics(values);
      // Also recompute progress after measurement
      computeProgress();
    };

    measure();
    const ro = new ResizeObserver(measure);
    ids.forEach((id) => {
      const el = sectionRefs.current[id];
      if (el) ro.observe(el);
    });
    window.addEventListener("resize", measure);
    return () => {
      ro.disconnect();
      window.removeEventListener("resize", measure);
    };
  }, [ids]);

  // Real-time progress on scroll using rAF
  useEffect(() => {
    let ticking = false;
    const onScroll = () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          computeProgress();
          ticking = false;
        });
        ticking = true;
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    // initial compute
    computeProgress();
    return () => window.removeEventListener('scroll', onScroll);
  }, [ids]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        const intersecting = entries.filter((e) => e.isIntersecting);
        if (intersecting.length > 0) {
          const sorted = intersecting.sort((a, b) => {
            if (Math.abs(b.intersectionRatio - a.intersectionRatio) > 0.1) {
              return b.intersectionRatio - a.intersectionRatio;
            }
            return a.boundingClientRect.top - b.boundingClientRect.top;
          });
          const activeEntry = sorted[0];
          const idx = ids.indexOf(activeEntry.target.id);
          if (idx !== -1) setActiveIndex(idx);
        }
      },
      {
        root: null,
        rootMargin: "-30% 0px -50% 0px",
        threshold: [0, 0.1, 0.25, 0.5, 0.75, 1],
      }
    );

    ids.forEach((id) => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, [ids]);

  const totalHeight = metrics.reduce((a, b) => a + b, 0) || 1;

  return (
    <div className="min-h-screen bg-black relative overflow-hidden">
      {/* Navigation (same as landing) */}
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
                onClick={hasToken ? () => router.push('/Input') : () => router.push('/login')}
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
      
      {/* Dark gradient background from hero to footer */}
      <div
        className="absolute inset-x-0"
        style={{
          top: 0,
          bottom: 0,
          background: "radial-gradient(ellipse 80% 60% at 50% 50%, #2d3748 0%, #1a202c 30%, #0f1419 60%, #000000 100%)"
        }}
      />

      {/* Content wrapper */}
    <div className="relative z-10 text-white">
      <main className="mx-auto max-w-7xl px-6 pt-28 pb-32 md:pb-40">

        {/* Page Header */}
        <div className="max-w-5xl mx-auto text-center mb-14">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-md bg-[#1a1a1a] border border-[#2a2a2a] mb-6">
            <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
            <span className="text-sm text-gray-500">Features</span>
          </div>
          <h2 className="text-5xl md:text-6xl text-white" style={{ marginBottom: '2rem' }}>
            How it works
          </h2>
          <p className="text-gray-500 text-xl max-w-2xl mx-auto">
            Built specifically for Cambodian BacII students with cutting-edge AI technology
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-[220px_1fr] gap-10 md:gap-14 py-12 md:py-20">
          {/* Left timeline rail */}
          <aside className="relative md:sticky md:top-24">
            {/* Wrapper matches content height to align dots */}
            <div className="relative hidden md:block" style={{ height: totalHeight ? `${totalHeight}px` : undefined }}>
              {/* Rail */}
              <div className="absolute left-[22px] top-0 bottom-0">
                <div className="h-full w-0.5 bg-gray-800/70 rounded" />
                {/* Progress */}
                <div
                  className="absolute left-0 top-0 w-0.5 bg-blue-500 rounded transition-all duration-700 ease-out"
                  style={{ height: `${progressPct}%` }}
                />
              </div>

              {/* Dots + labels */}
              <ul className="space-y-0">
                {steps.map((step, idx) => {
                  const Icon = step.icon;
                  const active = idx === activeIndex;
                  const completed = idx < activeIndex;
                  const itemHeight = metrics[idx] || 0;
                  return (
                    <li
                      key={step.id}
                      className="flex items-start gap-4"
                      style={{ height: itemHeight ? `${itemHeight}px` : undefined }}
                    >
                      <div className="relative z-10" style={{ marginTop: '2px' }}>
                        <span
                          className={
                            "block h-3.5 w-3.5 rounded-full border transition-all duration-300 " +
                            (active
                              ? "bg-blue-500 border-blue-400 scale-125"
                              : completed
                              ? "bg-blue-500 border-blue-400"
                              : "bg-gray-900 border-gray-700")
                          }
                        />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 text-sm transition-colors mb-1">
                          <Icon className={"h-4 w-4 " + (active || completed ? "text-blue-400" : "text-gray-600")} />
                          <span className={active || completed ? "text-blue-400" : "text-gray-400"}>Step {idx + 1}</span>
                        </div>
                        <button
                          onClick={() => {
                            const el = sectionRefs.current[step.id];
                            if (el) {
                              const headerOffset = 120;
                              const elementPosition = el.getBoundingClientRect().top;
                              const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                              window.scrollTo({ top: offsetPosition, behavior: "smooth" });
                            }
                          }}
                          className={`text-left text-base font-medium transition-colors ${
                            active
                              ? "text-white"
                              : completed
                              ? "text-white/90 hover:text-white"
                              : "text-white/70 hover:text-white/90"
                          }`}
                        >
                          {step.title}
                        </button>
                      </div>
                    </li>
                  );
                })}
              </ul>
            </div>
          </aside>

          {/* Right content */}
          <section>
            {steps.map((step, idx) => {
              const Icon = step.icon;
              const isActive = idx === activeIndex;
              return (
                <article
                  key={step.id}
                  id={step.id}
                  ref={(el) => {
                    sectionRefs.current[step.id] = el;
                  }}
                  className="scroll-mt-28 mb-24 last:mb-0"
                >
                  <div
                    className={
                      "rounded-2xl border transition-colors " +
                      (isActive 
                        ? "border-blue-500/40 bg-[#111111]" 
                        : "border-[#1f1f1f] bg-[#111111] hover:border-[#2a2a2a]")
                    }
                  >
                    <div className="p-6 md:p-8">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
                        {/* Left side - Content */}
                        <div>
                          <div className="flex items-center gap-3 mb-3">
                            <Icon className={"h-5 w-5 " + (isActive ? "text-blue-400" : "text-gray-500")} />
                            <h3 className="text-lg md:text-xl font-semibold">{step.title}</h3>
                          </div>
                          <p className="text-gray-400 leading-relaxed text-sm md:text-base">
                            {step.description}
                          </p>
                        </div>

                        {/* Right side - Video placeholder */}
                        <div className="rounded-lg border border-[#2a2a2a] bg-black/40 overflow-hidden">
                          <div className="w-full aspect-video flex items-center justify-center">
                            <span className="text-gray-600 text-sm">Video placeholder</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </article>
              );
            })}
          </section>
        </div>
      </main>

    </div>

      {/* Footer (same style as landing) */}
      <footer className="py-16 border-t border-[#1f1f1f] relative z-10 text-white">
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
'use client';

import { useEffect, useRef } from 'react';

interface RevealProps {
  children: React.ReactNode;
  className?: string;
  rootMargin?: string;
  threshold?: number;
  once?: boolean;
  delay?: number;
  translateY?: boolean;
  translateX?: number;
  scale?: boolean;
  style?: React.CSSProperties;
  immediatelyVisible?: boolean;
}

export default function Reveal({
  children,
  className = '',
  rootMargin = '-50px',
  threshold = 0.1,
  once = true,
  delay = 0,
  translateY = false,
  translateX = 0,
  scale = false,
  style = {},
  immediatelyVisible = false
}: RevealProps) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    // If immediately visible, trigger animation right away
    if (immediatelyVisible) {
      const applyAnimation = () => {
        element.classList.add('reveal-visible');
      };
      if (delay > 0) {
        setTimeout(applyAnimation, delay);
      } else {
        applyAnimation();
      }
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            // Apply delay via setTimeout if specified
            const applyAnimation = () => {
              element.classList.add('reveal-visible');
              if (once) {
                observer.unobserve(element);
              }
            };

            if (delay > 0) {
              setTimeout(applyAnimation, delay);
            } else {
              applyAnimation();
            }
          } else if (!once) {
            element.classList.remove('reveal-visible');
          }
        });
      },
      {
        root: null,
        rootMargin,
        threshold
      }
    );

    observer.observe(element);

    return () => {
      observer.disconnect();
    };
  }, [rootMargin, threshold, once, delay, immediatelyVisible]);

  // Set initial transform based on props
  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    if (translateY) {
      element.style.setProperty('--translate-y', '15px');
    } else if (translateX !== 0) {
      // Reduce horizontal translation for smoother effect
      const reducedX = Math.abs(translateX) > 20 ? (translateX > 0 ? 15 : -15) : translateX;
      element.style.setProperty('--translate-x', `${reducedX}px`);
    }
    if (scale) {
      element.style.setProperty('--scale', '0.9');
    }
  }, [translateY, translateX, scale]);

  return (
    <div
      ref={ref}
      className={`reveal ${className}`}
      style={{
        willChange: translateY || translateX !== 0 || scale ? 'opacity, transform' : 'opacity',
        ...style
      }}
    >
      {children}
    </div>
  );
}


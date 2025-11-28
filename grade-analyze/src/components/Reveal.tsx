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
  onReveal?: () => void;
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
  immediatelyVisible = false,
  onReveal
}: RevealProps) {
  const ref = useRef<HTMLDivElement>(null);
  const observerRef = useRef<IntersectionObserver | null>(null);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    // If immediately visible, trigger animation right away
    if (immediatelyVisible) {
      const applyAnimation = () => {
        element.classList.add('reveal-visible');
        if (onReveal) {
          onReveal();
        }
      };
      if (delay > 0) {
        setTimeout(applyAnimation, delay);
      } else {
        applyAnimation();
      }
      return;
    }

    // Check if element is already visible in viewport on mount
    const checkInitialVisibility = () => {
      const rect = element.getBoundingClientRect();
      const windowHeight = window.innerHeight || document.documentElement.clientHeight;
      const windowWidth = window.innerWidth || document.documentElement.clientWidth;
      
      // Simple check: element is visible if any part of it is in the viewport
      // This is more lenient than IntersectionObserver with negative rootMargin
      // We want elements that are already on screen to reveal immediately
      const isVisible = 
        rect.bottom > 0 &&
        rect.top < windowHeight &&
        rect.right > 0 &&
        rect.left < windowWidth;
      
      if (isVisible) {
        const applyAnimation = () => {
          element.classList.add('reveal-visible');
          if (onReveal) {
            onReveal();
          }
        };
        if (delay > 0) {
          setTimeout(applyAnimation, delay);
        } else {
          applyAnimation();
        }
        return true; // Element was already visible
      }
      return false; // Element not visible yet
    };

    // Check initial visibility after layout is complete
    // Use requestAnimationFrame to ensure DOM is fully rendered
    const setupObserver = () => {
      observerRef.current = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              // Apply delay via setTimeout if specified
              const applyAnimation = () => {
                element.classList.add('reveal-visible');
                if (onReveal) {
                  onReveal();
                }
                if (once && observerRef.current) {
                  observerRef.current.unobserve(element);
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

      observerRef.current.observe(element);
    };

    // Check visibility after next frame to ensure layout is complete
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        const wasVisible = checkInitialVisibility();
        
        // If not already visible, set up observer
        if (!wasVisible) {
          setupObserver();
        }
      });
    });
    
    // Return cleanup function
    return () => {
      if (observerRef.current) {
        observerRef.current.disconnect();
        observerRef.current = null;
      }
    };
  }, [rootMargin, threshold, once, delay, immediatelyVisible, onReveal]);

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


"use client";

import { useEffect, useRef } from "react";
import { createPortal } from "react-dom";
import { X } from "lucide-react";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
  title?: string;
}

export default function Modal({
  isOpen,
  onClose,
  children,
  title,
}: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener("keydown", handleEscape);
      // Prevent layout shift by adding padding when scrollbar is hidden
      const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
      document.body.style.overflow = "hidden";
      document.body.style.paddingRight = `${scrollbarWidth}px`;
    }

    return () => {
      document.removeEventListener("keydown", handleEscape);
      document.body.style.overflow = "unset";
      document.body.style.paddingRight = "0px";
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const modalContent = (
    <div
      className="fixed inset-0 z-[9999] flex items-center justify-center p-4 animate-fadeIn"
      onClick={(e) => {
        if (e.target === e.currentTarget) {
          onClose();
        }
      }}
    >
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/70 backdrop-blur-sm z-[1]" />

      {/* Modal */}
      <div
        ref={modalRef}
        className="relative bg-[#111111] border border-[#1f1f1f] rounded-2xl shadow-2xl w-4xl max-h-[90vh] overflow-y-auto animate-scaleIn z-[2] modal-scroll" /* max-w-md md:max-w-3xl lg:max-w-5xl xl-max-w-6xl */
        onClick={(e) => e.stopPropagation()}
      >
        {/* Always-visible close button (top-right) */}
        <button
          onClick={onClose}
          className="absolute top-3 right-3 p-2 rounded-lg transition-colors z-20"
          aria-label="Close modal"
        >
          <X className="w-6 h-6 text-white hover:text-gray-300" />
        </button>

        {/* Header */}
        {title && (
          <div className="sticky top-0 bg-[#111111]/95 backdrop-blur-sm border-b border-[#1f1f1f] px-6 py-4 flex items-center justify-between z-10">
            <h2 className="text-2xl font-bold text-white">{title}</h2>
            <button
              onClick={onClose}
              className="p-2 rounded-lg transition-colors"
              aria-label="Close modal"
            >
              <X className="w-6 h-6 text-white hover:text-gray-300" />
            </button>
          </div>
        )}

        {/* Content */}
        <div className="p-6">{children}</div>
      </div>

      <style jsx global>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }

        @keyframes scaleIn {
          from {
            opacity: 0;
            transform: scale(0.95);
          }
          to {
            opacity: 1;
            transform: scale(1);
          }
        }

        .animate-fadeIn {
          animation: fadeIn 0.2s ease-out;
        }

        .animate-scaleIn {
          animation: scaleIn 0.3s ease-out;
        }

        /* Modal scrollbar styling (hidden but scrollable) */
        .modal-scroll {
          scrollbar-width: none; /* Firefox: hide scrollbar */
        }
        .modal-scroll::-webkit-scrollbar {
          width: 0; /* Chrome, Safari: hide scrollbar */
          height: 0;
        }
      `}</style>
    </div>
  );

  return typeof document !== "undefined"
    ? createPortal(modalContent, document.body)
    : null;
}

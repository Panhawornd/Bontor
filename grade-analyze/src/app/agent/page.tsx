"use client";

import { useRouter } from 'next/navigation';
import Button from "@/components/ui/Button";
import { Bot, ArrowLeft } from "lucide-react";

export default function AgentPage() {
  const router = useRouter();

  return (
    <div className="min-h-screen text-white flex flex-col items-center justify-center p-6 relative">
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
          filter: 'brightness(0.5)',
          zIndex: 0,
          pointerEvents: 'none'
        }}
      />
      <div className="relative z-10 text-center">
        <Bot className="w-24 h-24 text-blue-500 mx-auto mb-8 animate-bounce" />
        <h1 className="text-5xl font-bold mb-4">Agent</h1>
        <p className="text-xl text-gray-400 mb-8">This page is coming soon! We&apos;re working hard to bring you an AI-powered assistant for career guidance.</p>
        <Button
          onClick={() => router.push('/Input')}
          className="px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-md transition-colors flex items-center justify-center mx-auto"
        >
          <ArrowLeft className="w-5 h-5 mr-2" /> Back
        </Button>
      </div>
    </div>
  );
}


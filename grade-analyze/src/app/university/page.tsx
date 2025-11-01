"use client";

import { useRouter } from 'next/navigation';
import Button from "@/components/ui/Button";
import { GraduationCap, ArrowLeft } from "lucide-react";

export default function UniversityPage() {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center p-6">
      <div className="text-center">
        <GraduationCap className="w-24 h-24 text-blue-500 mx-auto mb-8 animate-bounce" />
        <h1 className="text-5xl font-bold mb-4">University</h1>
        <p className="text-xl text-gray-400 mb-8">This page is coming soon! We&apos;re working hard to bring you comprehensive university information and comparisons.</p>
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


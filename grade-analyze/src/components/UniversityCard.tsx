"use client";

import Image from "next/image";
import { useState } from "react";
import {
  MapPin,
  GraduationCap,
  FileText,
  Award,
  Globe,
  Eye,
  Search,
} from "lucide-react";
import UniversityDetailModal from "./UniversityDetailModal";

export interface University {
  id: number;
  name: string;
  country: string;
  city: string | null;
  availablePrograms: string[];
  minGrade: number | null;
  entranceExam: boolean | null;
  scholarshipAvailable: boolean | null;
  scholarshipDetail: string | null;
  locationMaps: string | null;
  tuitionFee: string | null;
  imageUrl?: string | null;
}

interface UniversityCardProps {
  university: University;
}

export default function UniversityCard({ university }: UniversityCardProps) {
  const [showAllPrograms, setShowAllPrograms] = useState(false);
  const [imageError, setImageError] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const imageSrc =
    !imageError && university.imageUrl
      ? university.imageUrl
      : "/image/Bontor-logo.png";

  const displayedPrograms = showAllPrograms
    ? university.availablePrograms
    : university.availablePrograms.slice(0, 5);

  return (
    <div
      className="bg-[#111111] border border-[#1f1f1f] rounded-xl transition-colors hover:border-[#2a2a2a] flex flex-col h-full overflow-hidden"
    >
      <div className="relative w-full h-56 bg-gray-900">
        <Image
          src={imageSrc}
          alt={`Bontor logo for ${university.name}`}
          fill
          sizes="(min-width: 1024px) 380px, (min-width: 768px) 45vw, 100vw"
          className="object-cover transition-transform duration-500 hover:scale-105"
          priority={false}
          onError={() => setImageError(true)}
        />
      </div>

      <div className="p-6 flex flex-col flex-grow">
      <div className="mb-4">
        <h3 className="text-xl font-bold text-white mb-2">{university.name}</h3>
        <div className="pt-2 flex items-center gap-2 text-gray-400 mb-2 text-sm overflow-hidden">
          <MapPin className="w-4 h-4 flex-shrink-0" />
          <span className="truncate flex-shrink">{university.city || "Unknown City"}</span>
          <span className="text-gray-600 flex-shrink-0">•</span>
          <span className="truncate flex-shrink">{university.country}</span>
          <span className="text-gray-600 flex-shrink-0">•</span>
          <span className="flex-shrink-0 whitespace-nowrap">Entrance Exam</span>
        </div>
      </div>

      <div className="mb-4 flex-grow">
        <h4 className="text-sm font-semibold text-gray-300 mb-3">
          Available Programs
        </h4>
        <div className="pt-2 text-sm text-gray-400">
          {university.availablePrograms.slice(0, 2).join(", ")}
          {university.availablePrograms.length > 2 && "..."}
        </div>
      </div>

      <div className="border-t border-gray-700 pt-4">
        {/* View Details Button */}
        <button
          onClick={() => setIsModalOpen(true)}
          className="w-full px-4 py-1.5 bg-gray-800 hover:bg-gray-700 text-white rounded-md transition-colors border border-gray-600 flex items-center justify-center gap-2"
        >
          View Details
        </button>
      </div>
      </div>

      {/* University Detail Modal */}
      <UniversityDetailModal
        university={university}
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </div>
  );
}

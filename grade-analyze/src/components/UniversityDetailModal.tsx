"use client";

import Image from "next/image";
import { useState } from "react";
import {
  MapPin,
  GraduationCap,
  FileText,
  Award,
  Globe,
  BookOpen,
  CheckCircle,
  DollarSign,
  Users,
  Building,
  Calendar,
  TrendingUp,
  Mail,
  Phone,
  ExternalLink,
  Clock,
  BadgeCheck,
  Lightbulb,
  Info,
} from "lucide-react";
import { University } from "./UniversityCard";
import Modal from "./ui/Modal";

interface UniversityDetailModalProps {
  university: University;
  isOpen: boolean;
  onClose: () => void;
}

export default function UniversityDetailModal({
  university,
  isOpen,
  onClose,
}: UniversityDetailModalProps) {
  const [imageError, setImageError] = useState(false);
  const imageSrc =
    !imageError && university.imageUrl
      ? university.imageUrl
      : "/image/Bontor-logo.png";

  // Convert Google Maps link to embed URL
  const getEmbedUrl = (mapsLink: string) => {
    try {
      // Extract coordinates from the URL
      const coordMatch = mapsLink.match(/@(-?\d+\.\d+),(-?\d+\.\d+)/);
      if (coordMatch) {
        const lat = coordMatch[1];
        const lng = coordMatch[2];
        return `https://maps.google.com/maps?q=${lat},${lng}&hl=en&z=16&output=embed`;
      }
      
      // Fallback: use university name as search query
      const query = encodeURIComponent(university.name + " " + (university.city || ""));
      return `https://maps.google.com/maps?q=${query}&hl=en&z=16&output=embed`;
    } catch {
      return "";
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <div className="space-y-8">
        {/* University Image with overlaid title, full-width cover */}
        <div className="relative w-[calc(100%+3rem)] h-80 -translate-x-6 -mt-6 rounded-t-2xl overflow-hidden bg-[#111111]">
          <Image
            src={imageSrc}
            alt={university.name}
            fill
            sizes="(min-width: 1024px) 896px, 90vw"
            className="object-cover object-center brightness-75"
            priority
            onError={() => setImageError(true)}
          />
          {/* Darkening overlay - bottom to top gradient */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/30 to-black/10" />
          {/* Title overlay */}
          <div className="absolute inset-x-0 bottom-0 px-6 py-4 bg-gradient-to-t from-black/50 to-transparent">
            <h2 className="text-2xl md:text-4xl font-bold text-white">
              {university.name}
            </h2>
          </div>
        </div>

        {/* Location & Country */}
        <div className="flex items-center gap-6 max-[430px]:gap-3 text-gray-300 pt-2">
          <div className="flex items-center gap-2 max-[430px]:gap-1.5">
            <MapPin className="w-5 h-5 max-[430px]:w-4 max-[430px]:h-4 text-blue-500" />
            <span className="text-lg max-[430px]:text-sm">{university.city || "Unknown City"}</span>
          </div>
          <span className="text-gray-600 max-[430px]:text-sm">•</span>
          <div className="flex items-center gap-2 max-[430px]:gap-1.5">
            <Image 
              src="/image/kh-flag.jpg" 
              alt="Cambodia Flag" 
              width={20} 
              height={20} 
              className="max-[430px]:w-4 max-[430px]:h-4"
            />
            <span className="text-lg max-[430px]:text-sm">{university.country}</span>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-2">
          <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-4">
            <div className="flex items-center gap-2 mb-1">
              <BookOpen className="w-5 h-5 text-blue-500" />
              <span className="text-xs text-gray-400">Programs</span>
            </div>
            <p className="text-xl font-bold text-white">
              {university.availablePrograms?.length || 0}
            </p>
          </div>

          <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-4">
            <div className="flex items-center gap-2 mb-1">
              <TrendingUp className="w-5 h-5 text-green-500" />
              <span className="text-xs text-gray-400">Min Grade</span>
            </div>
            <p className="text-xl font-bold text-white">
              {university.minGrade ? `${university.minGrade}%` : "N/A"}
            </p>
          </div>

          <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-4">
            <div className="flex items-center gap-2 mb-1">
              <FileText className="w-5 h-5 text-green-500" />
              <span className="text-xs text-gray-400">Entrance Exam</span>
            </div>
            <p className="text-xl max-[430px]:text-base font-bold text-white">
              {university.entranceExam ? "Required" : "No"}
            </p>
          </div>

          <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-4">
            <div className="flex items-center gap-2 mb-1">
              <Award className="w-5 h-5 text-yellow-500" />
              <span className="text-xs text-gray-400">Scholarships</span>
            </div>
            <p className="text-xl max-[430px]:text-base font-bold text-white">
              {university.scholarshipAvailable ? "Available" : "N/A"}
            </p>
          </div>
        </div>

        {/* Programs Section */}
        <div className="bg-[#111111] border border-[#1f1f1f] rounded-lg p-6 mt-2">
          <h3 className="text-xl font-bold text-white pb-6 flex items-center gap-3">
            <BookOpen className="w-6 h-6 text-blue-500" />
            Available Programs ({university.availablePrograms?.length || 0})
          </h3>
          <div className="space-y-3 pt-2">
            {university.availablePrograms?.map((program, idx) => (
              <div
                key={idx}
                className="flex items-center gap-3 bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-4"
              >
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span className="text-gray-200">{program}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Additional Information Section */}
        {(university.locationMaps || university.tuitionFee || university.scholarshipDetail) && (
          <div className="bg-[#111111] border border-[#1f1f1f] rounded-lg p-6 pt-4 mt-2">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

              {/* Google Maps Location */}
              {university.locationMaps && (
                <div className="md:col-span-2">
                  <h4 className="text-sm font-semibold text-white pb-4 ">
                    Campus Location
                  </h4>
                  <div className="w-full h-64 bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg overflow-hidden mb-3">
                    <iframe
                      src={getEmbedUrl(university.locationMaps)}
                      width="100%"
                      height="100%"
                      style={{ border: 0 }}
                      allowFullScreen
                      loading="lazy"
                      referrerPolicy="no-referrer-when-downgrade"
                      className="rounded-lg"
                    />
                  </div>
                  <a
                    href={university.locationMaps}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 bg-gray-700/50 hover:bg-gray-700 rounded-lg p-4 transition-colors group"
                  >
                    <MapPin className="w-5 h-5 text-blue-500" />
                    <span className="text-sm text-gray-300 group-hover:text-white">
                      View on Google Maps
                    </span>
                    <ExternalLink className="w-4 h-4 text-gray-400 ml-auto" />
                  </a>
                </div>
              )}

              {/* Tuition Fee */}
              {university.tuitionFee && (
                <div>
                  <h4 className="text-sm font-semibold text-gray-400 mb-3">
                    Tuition Fee
                  </h4>
                  <div className="flex items-center gap-2 text-gray-300">
                    <DollarSign className="w-4 h-4 text-blue-400" />
                    <span className="text-sm">
                      {university.tuitionFee}
                    </span>
                  </div>
                </div>
              )}

              {/* Scholarship Detail */}
              {university.scholarshipDetail && (
                <div className="md:col-span-2">
                  <h4 className="text-sm font-semibold text-white mb-3">
                    Scholarship Details
                  </h4>
                  <p className="py-2 text-gray-300 text-sm">
                    {university.scholarshipDetail}
                  </p>
                </div>
              )}

            </div>
          </div>
        )}

        {/* Action Button */}
        <div className="pt-6">
          <button
            onClick={onClose}
            className="w-full px-6 py-3 bg-gray-800 hover:bg-gray-700 text-white rounded-md transition-colors border border-gray-600 font-semibold"
          >
            Close
          </button>
        </div>
      </div>
    </Modal>
  );
}

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
      const query = encodeURIComponent(university.name);
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
        <div className="flex items-center gap-6 text-gray-300 pt-2">
          <div className="flex items-center gap-2">
            <MapPin className="w-5 h-5 text-blue-500" />
            <span className="text-lg">{university.location}</span>
          </div>
          <span className="text-gray-600">•</span>
          <div className="flex items-center gap-2">
            <Image 
              src="/image/kh-flag.jpg" 
              alt="Cambodia Flag" 
              width={20} 
              height={20} 
            />
            <span className="text-lg">{university.country}</span>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-2">
          <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-4">
            <div className="flex items-center gap-2 mb-1">
              <BookOpen className="w-5 h-5 text-blue-500" />
              <span className="text-xs text-gray-400">Programs</span>
            </div>
            <p className="text-2xl font-bold text-white">
              {university.programs.length}
            </p>
          </div>

          <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-4">
            <div className="flex items-center gap-2 mb-1">
              <TrendingUp className="w-5 h-5 text-green-500" />
              <span className="text-xs text-gray-400">Min Grade</span>
            </div>
            <p className="text-lg font-bold text-white">
              {university.requirements.min_grade}%
            </p>
          </div>

          <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-4">
            <div className="flex items-center gap-2 mb-1">
              <FileText className="w-5 h-5 text-green-500" />
              <span className="text-xs text-gray-400">Entrance Exam</span>
            </div>
            <p className="text-lg font-bold text-white">
              {university.requirements.entrance_exam?.required ? "Required" : "No"}
            </p>
          </div>

          <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-4">
            <div className="flex items-center gap-2 mb-1">
              <Award className="w-5 h-5 text-yellow-500" />
              <span className="text-xs text-gray-400">Scholarships</span>
            </div>
            <p className="text-lg font-bold text-white">
              {university.scholarships?.available ? "Available" : "N/A"}
            </p>
          </div>
        </div>

        {/* Programs Section */}
        <div className="bg-[#111111] border border-[#1f1f1f] rounded-lg p-6 mt-2">
          <h3 className="text-xl font-bold text-white pb-6 flex items-center gap-3">
            <BookOpen className="w-6 h-6 text-blue-500" />
            Available Programs ({university.programs.length})
          </h3>
          <div className="space-y-3 pt-2">
            {university.programs.map((program, idx) => (
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
        {university.additional_info && (
          <div className="bg-[#111111] border border-[#1f1f1f] rounded-lg p-6 pt-4 mt-2">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* International Program */}
              {university.additional_info.international_program !==
                undefined && (
                <div className="md:col-span-2">
                  <div className="flex items-center gap-3 bg-blue-500/10 rounded-lg p-4 border border-blue-500/30">
                    <Globe className="w-5 h-5 text-blue-400" />
                    <div>
                      <p className="text-sm font-semibold text-white">
                        International Program:{" "}
                        {university.additional_info.international_program
                          ? "Available"
                          : "Not Available"}
                      </p>
                      {university.additional_info.international_program && (
                        <p className="text-xs text-gray-400 mt-1">
                          Offers programs taught in English for international
                          students
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* Google Maps Location */}
              {university.additional_info.google_maps_link && (
                <div className="md:col-span-2">
                  <h4 className="text-sm font-semibold text-white pb-4 ">
                    Campus Location
                  </h4>
                  {/* Embedded Google Map */}
                  <div className="w-full h-64 bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg overflow-hidden mb-3">
                    <iframe
                      src={getEmbedUrl(university.additional_info.google_maps_link)}
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
                    href={university.additional_info.google_maps_link}
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

              {/* Contact Information */}
              {(university.additional_info.website ||
                university.additional_info.email ||
                university.additional_info.phone) && (
                <div className="md:col-span-2">
                  <h4 className="text-sm font-semibold text-gray-400 mb-4">
                    Contact Information
                  </h4>
                  <div className="space-y-3">
                    {university.additional_info.website && (
                      <a
                        href={university.additional_info.website}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-2 text-blue-400 hover:text-blue-300 transition-colors"
                      >
                        <Globe className="w-4 h-4" />
                        <span className="text-sm">
                          {university.additional_info.website}
                        </span>
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    )}
                    {university.additional_info.email && (
                      <a
                        href={`mailto:${university.additional_info.email}`}
                        className="flex items-center gap-2 text-gray-300 hover:text-white transition-colors"
                      >
                        <Mail className="w-4 h-4 text-blue-400" />
                        <span className="text-sm">
                          {university.additional_info.email}
                        </span>
                      </a>
                    )}
                    {university.additional_info.phone && (
                      <div className="flex items-center gap-2 text-gray-300">
                        <Phone className="w-4 h-4 text-blue-400" />
                        <span className="text-sm">
                          {university.additional_info.phone}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Academic Information */}
              {university.additional_info.application_deadline && (
                <div>
                  <h4 className="text-sm font-semibold text-gray-400 mb-3">
                    Application Deadline
                  </h4>
                  <div className="flex items-center gap-2 text-gray-300">
                    <Calendar className="w-4 h-4 text-blue-400" />
                    <span className="text-sm">
                      {university.additional_info.application_deadline}
                    </span>
                  </div>
                </div>
              )}

              {university.additional_info.duration && (
                <div>
                  <h4 className="text-sm font-semibold text-gray-400 mb-3">
                    Program Duration
                  </h4>
                  <div className="flex items-center gap-2 text-gray-300">
                    <Clock className="w-4 h-4 text-blue-400" />
                    <span className="text-sm">
                      {university.additional_info.duration}
                    </span>
                  </div>
                </div>
              )}

              {university.additional_info.tuition_fee && (
                <div>
                  <h4 className="text-sm font-semibold text-gray-400 mb-3">
                    Tuition Fee
                  </h4>
                  <div className="flex items-center gap-2 text-gray-300">
                    <DollarSign className="w-4 h-4 text-blue-400" />
                    <span className="text-sm">
                      {university.additional_info.tuition_fee}
                    </span>
                  </div>
                </div>
              )}

              {/* Accreditation */}
              {university.additional_info.accreditation &&
                university.additional_info.accreditation.length > 0 && (
                  <div className="md:col-span-2">
                    <h4 className="text-sm font-semibold text-gray-400 mb-3">
                      Accreditation
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {university.additional_info.accreditation.map(
                        (acc, idx) => (
                          <span
                            key={idx}
                            className="flex items-center gap-1 bg-blue-500/10 text-blue-400 px-3 py-1 rounded-full text-sm border border-blue-500/30"
                          >
                            <BadgeCheck className="w-3 h-3" />
                            {acc}
                          </span>
                        )
                      )}
                    </div>
                  </div>
                )}

              {/* Facilities */}
              {university.additional_info.facilities &&
                university.additional_info.facilities.length > 0 && (
                  <div className="md:col-span-2">
                    <h4 className="text-sm font-semibold text-gray-400 mb-3">
                      Campus Facilities
                    </h4>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                      {university.additional_info.facilities.map(
                        (facility, idx) => (
                          <div
                            key={idx}
                            className="flex items-center gap-2 text-gray-300 text-sm"
                          >
                            <Lightbulb className="w-3 h-3 text-blue-400" />
                            <span>{facility}</span>
                          </div>
                        )
                      )}
                    </div>
                  </div>
                )}

              {/* Student Life */}
              {university.additional_info.student_life && (
                <div className="md:col-span-2">
                  <h4 className="text-sm font-semibold text-gray-400 mb-3">
                    Student Life
                  </h4>
                  <p className="text-gray-300 text-sm">
                    {university.additional_info.student_life}
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

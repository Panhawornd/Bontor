"use client";

import Image from "next/image";
import { useState } from "react";
import { MapPin, GraduationCap, FileText, Award, Globe } from "lucide-react";

export interface University {
  name: string;
  country: string;
  location: string;
  programs: string[];
  imageUrl?: string;
  requirements: {
    min_grade: number;
    preferred_subjects: string[];
    entrance_exam?: {
      required: boolean;
      description?: string;
    };
    english_proficiency?: {
      toefl?: {
        required: boolean;
        min_score?: number;
      };
      ielts?: {
        required: boolean;
        min_score?: number;
      };
    };
  };
  scholarships?: {
    available: boolean;
    description?: string;
    types?: string[];
  };
}

interface UniversityCardProps {
  university: University;
}

export default function UniversityCard({ university }: UniversityCardProps) {
  const [showAllPrograms, setShowAllPrograms] = useState(false);
  const [imageError, setImageError] = useState(false);
  const imageSrc =
    !imageError && university.imageUrl
      ? university.imageUrl
      : "/image/Bontor-logo.png";

  const displayedPrograms = showAllPrograms
    ? university.programs
    : university.programs.slice(0, 5);

  return (
    <div
      className="bg-gray-800 border border-gray-700 rounded-xl p-6 transition-all duration-300 hover:border-blue-500 hover:shadow-lg hover:shadow-blue-500/20"
      style={{
        background: "var(--bg-tertiary)",
        border: "1px solid var(--border-primary)",
      }}
    >
      <div className="relative mb-4">
        <div className="relative w-full h-56 rounded-lg overflow-hidden border border-gray-700 bg-gray-900">
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
      </div>

      <div className="mb-4">
        <h3 className="text-xl font-bold text-white mb-2">{university.name}</h3>
        <div className="flex flex-wrap items-center gap-2 text-gray-400 mb-2">
          <div className="flex items-center gap-2">
            <MapPin className="w-4 h-4" />
            <span className="text-sm">{university.location}</span>
            <span className="text-gray-600">•</span>
            <span className="text-sm">{university.country}</span>
          </div>

          {/* Entrance Exam - only if required */}
          {university.requirements.entrance_exam?.required && (
            <>
              <span className="text-gray-600">•</span>
              <div className="flex items-center gap-1">
                <FileText className="w-3 h-3 text-blue-500" />
                <span className="text-xs text-red-400">Entrance Exam</span>
              </div>
            </>
          )}

          {/* English Proficiency - only if required */}
          {university.requirements.english_proficiency &&
            (university.requirements.english_proficiency.toefl?.required ||
              university.requirements.english_proficiency.ielts?.required) && (
              <>
                <span className="text-gray-600">•</span>
                <div className="flex items-center gap-1">
                  <Globe className="w-3 h-3 text-blue-500" />
                  <span className="text-xs">
                    {university.requirements.english_proficiency.toefl
                      ?.required &&
                      `TOEFL${
                        university.requirements.english_proficiency.toefl
                          .min_score
                          ? ` ${university.requirements.english_proficiency.toefl.min_score}`
                          : ""
                      }`}
                    {university.requirements.english_proficiency.toefl
                      ?.required &&
                      university.requirements.english_proficiency.ielts
                        ?.required &&
                      " / "}
                    {university.requirements.english_proficiency.ielts
                      ?.required &&
                      `IELTS${
                        university.requirements.english_proficiency.ielts
                          .min_score
                          ? ` ${university.requirements.english_proficiency.ielts.min_score}`
                          : ""
                      }`}
                  </span>
                </div>
              </>
            )}

          {/* Scholarships - only if available */}
          {university.scholarships?.available && (
            <>
              <span className="text-gray-600">•</span>
              <div className="flex items-center gap-1">
                <Award className="w-3 h-3 text-yellow-500" />
                <span className="text-xs text-yellow-400">Scholarships</span>
              </div>
            </>
          )}
        </div>
      </div>

      <div className="mb-4">
        <div className="flex items-center gap-2 mb-3">
          <GraduationCap className="w-5 h-5 text-blue-500" />
          <h4 className="text-sm font-semibold text-gray-300">
            Available Programs ({university.programs.length})
          </h4>
        </div>
        <div className="flex flex-wrap gap-2 mb-2">
          {displayedPrograms.map((program, index) => (
            <span
              key={index}
              className="text-xs bg-gray-700 text-gray-300 px-3 py-1 rounded-full"
            >
              {program}
            </span>
          ))}
        </div>
        {university.programs.length > 5 && (
          <button
            onClick={() => setShowAllPrograms(!showAllPrograms)}
            className="text-sm text-blue-500 hover:text-blue-400 transition-colors"
          >
            {showAllPrograms
              ? "Show less"
              : `Show ${university.programs.length - 5} more programs`}
          </button>
        )}
      </div>

      <div className="border-t border-gray-700 pt-4">
        <div className="flex flex-col gap-2 text-sm">
          <div className="flex items-center justify-between">
            <span className="text-gray-400">Minimum Grade:</span>
            <span className="text-white font-semibold">
              {university.requirements.min_grade}%
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-400">Preferred Subjects:</span>
            <span className="text-white">
              {university.requirements.preferred_subjects
                .map((s) => s.charAt(0).toUpperCase() + s.slice(1))
                .join(", ")}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

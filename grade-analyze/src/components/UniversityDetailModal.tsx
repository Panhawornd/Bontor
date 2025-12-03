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

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={university.name}>
      <div className="space-y-6">
        {/* University Image */}
        <div className="relative w-full h-72 rounded-xl overflow-hidden border border-gray-700 bg-gray-800">
          <Image
            src={imageSrc}
            alt={university.name}
            fill
            sizes="(min-width: 1024px) 896px, 90vw"
            className="object-cover"
            priority
            onError={() => setImageError(true)}
          />
        </div>

        {/* Location & Country */}
        <div className="flex items-center gap-4 text-gray-300">
          <div className="flex items-center gap-2">
            <MapPin className="w-5 h-5 text-blue-500" />
            <span className="text-lg">{university.location}</span>
          </div>
          <span className="text-gray-600">•</span>
          <div className="flex items-center gap-2">
            <Building className="w-5 h-5 text-blue-500" />
            <span className="text-lg">{university.country}</span>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-1">
              <GraduationCap className="w-5 h-5 text-blue-500" />
              <span className="text-xs text-gray-400">Programs</span>
            </div>
            <p className="text-2xl font-bold text-white">
              {university.programs.length}
            </p>
          </div>

          <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-1">
              <TrendingUp className="w-5 h-5 text-green-500" />
              <span className="text-xs text-gray-400">Min Grade</span>
            </div>
            <p className="text-2xl font-bold text-white">
              {university.requirements.min_grade}%
            </p>
          </div>

          <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-1">
              <FileText className="w-5 h-5 text-green-500" />
              <span className="text-xs text-gray-400">Entrance Exam</span>
            </div>
            <p className="text-lg font-bold text-green-500">
              {university.requirements.entrance_exam?.required ? "Yes" : "No"}
            </p>
          </div>

          <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-1">
              <Award className="w-5 h-5 text-yellow-500" />
              <span className="text-xs text-gray-400">Scholarships</span>
            </div>
            <p className="text-lg font-bold text-yellow-500">
              {university.scholarships?.available ? "Available" : "N/A"}
            </p>
          </div>
        </div>

        {/* Requirements Section */}
        <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <CheckCircle className="w-6 h-6 text-blue-500" />
            Admission Requirements
          </h3>

          <div className="space-y-4">
            {/* Minimum Grade */}
            <div>
              <h4 className="text-sm font-semibold text-gray-400 mb-2">
                Minimum Grade Requirement
              </h4>
              <p className="text-white">
                {university.requirements.min_grade}% or higher
              </p>
            </div>

            {/* Preferred Subjects */}
            <div>
              <h4 className="text-sm font-semibold text-gray-400 mb-2">
                Preferred Subjects
              </h4>
              <div className="flex flex-wrap gap-2">
                {university.requirements.preferred_subjects.map(
                  (subject, idx) => (
                    <span
                      key={idx}
                      className="bg-blue-500/20 text-blue-400 px-3 py-1 rounded-full text-sm border border-blue-500/30"
                    >
                      {subject.charAt(0).toUpperCase() + subject.slice(1)}
                    </span>
                  )
                )}
              </div>
            </div>

            {/* Entrance Exam */}
            {university.requirements.entrance_exam?.required && (
              <div>
                <h4 className="text-sm font-semibold text-gray-400 mb-2">
                  Entrance Exam
                </h4>
                <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4">
                  <div className="flex items-start gap-3">
                    <FileText className="w-5 h-5 text-green-400 mt-0.5" />
                    <div className="flex-1 space-y-3">
                      <p className="text-green-400 font-semibold">Required</p>

                      {university.requirements.entrance_exam.description && (
                        <div>
                          <p className="text-gray-300 text-sm">
                            {university.requirements.entrance_exam.description}
                          </p>
                        </div>
                      )}

                      {university.requirements.entrance_exam.subjects &&
                        university.requirements.entrance_exam.subjects.length >
                          0 && (
                          <div>
                            <p className="text-xs text-gray-400 mb-1">
                              Exam Subjects:
                            </p>
                            <div className="flex flex-wrap gap-1">
                              {university.requirements.entrance_exam.subjects.map(
                                (subject, idx) => (
                                  <span
                                    key={idx}
                                    className="text-xs bg-green-500/20 text-green-300 px-2 py-1 rounded"
                                  >
                                    {subject}
                                  </span>
                                )
                              )}
                            </div>
                          </div>
                        )}

                      {university.requirements.entrance_exam.schedule && (
                        <div className="flex items-center gap-2">
                          <Calendar className="w-4 h-4 text-green-400" />
                          <span className="text-sm text-gray-300">
                            {university.requirements.entrance_exam.schedule}
                          </span>
                        </div>
                      )}

                      {university.requirements.entrance_exam.fee && (
                        <div className="flex items-center gap-2">
                          <DollarSign className="w-4 h-4 text-green-400" />
                          <span className="text-sm text-gray-300">
                            Exam Fee:{" "}
                            {university.requirements.entrance_exam.fee}
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* English Proficiency */}
            {university.requirements.english_proficiency &&
              (university.requirements.english_proficiency.toefl?.required ||
                university.requirements.english_proficiency.ielts
                  ?.required) && (
                <div>
                  <h4 className="text-sm font-semibold text-gray-400 mb-2">
                    English Proficiency
                  </h4>
                  <div className="space-y-2">
                    {university.requirements.english_proficiency.toefl
                      ?.required && (
                      <div className="flex items-center gap-3 bg-gray-700/50 rounded-lg p-3">
                        <Globe className="w-5 h-5 text-blue-400" />
                        <div>
                          <p className="text-white font-semibold">TOEFL</p>
                          {university.requirements.english_proficiency.toefl
                            .min_score && (
                            <p className="text-gray-400 text-sm">
                              Minimum Score:{" "}
                              {
                                university.requirements.english_proficiency
                                  .toefl.min_score
                              }
                            </p>
                          )}
                        </div>
                      </div>
                    )}
                    {university.requirements.english_proficiency.ielts
                      ?.required && (
                      <div className="flex items-center gap-3 bg-gray-700/50 rounded-lg p-3">
                        <Globe className="w-5 h-5 text-blue-400" />
                        <div>
                          <p className="text-white font-semibold">IELTS</p>
                          {university.requirements.english_proficiency.ielts
                            .min_score && (
                            <p className="text-gray-400 text-sm">
                              Minimum Score:{" "}
                              {
                                university.requirements.english_proficiency
                                  .ielts.min_score
                              }
                            </p>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}
          </div>
        </div>

        {/* Programs Section */}
        <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <BookOpen className="w-6 h-6 text-blue-500" />
            Available Programs ({university.programs.length})
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {university.programs.map((program, idx) => (
              <div
                key={idx}
                className="flex items-center gap-3 bg-gray-700/50 rounded-lg p-3 hover:bg-gray-700 transition-colors"
              >
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span className="text-gray-200">{program}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Scholarships Section */}
        {university.scholarships?.available && (
          <div className="bg-gradient-to-br from-yellow-500/10 to-orange-500/10 border border-yellow-500/30 rounded-lg p-6">
            <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <Award className="w-6 h-6 text-yellow-500" />
              Scholarship Opportunities
            </h3>

            <div className="space-y-4">
              {university.scholarships.description && (
                <p className="text-gray-300">
                  {university.scholarships.description}
                </p>
              )}

              {university.scholarships.types &&
                university.scholarships.types.length > 0 && (
                  <div>
                    <h4 className="text-sm font-semibold text-gray-400 mb-3">
                      Available Scholarship Types
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      {university.scholarships.types.map((type, idx) => (
                        <div
                          key={idx}
                          className="flex items-center gap-2 bg-yellow-500/10 rounded-lg p-3"
                        >
                          <DollarSign className="w-4 h-4 text-yellow-400" />
                          <span className="text-yellow-100">{type}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

              {university.scholarships.coverage &&
                university.scholarships.coverage.length > 0 && (
                  <div>
                    <h4 className="text-sm font-semibold text-gray-400 mb-2">
                      Scholarship Coverage
                    </h4>
                    <ul className="space-y-1">
                      {university.scholarships.coverage.map((item, idx) => (
                        <li
                          key={idx}
                          className="flex items-start gap-2 text-gray-300 text-sm"
                        >
                          <CheckCircle className="w-4 h-4 text-yellow-400 mt-0.5 flex-shrink-0" />
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

              {university.scholarships.application_deadline && (
                <div className="flex items-center gap-2 bg-yellow-500/10 rounded-lg p-3">
                  <Calendar className="w-4 h-4 text-yellow-400" />
                  <div>
                    <p className="text-xs text-gray-400">
                      Application Deadline
                    </p>
                    <p className="text-yellow-100 font-semibold">
                      {university.scholarships.application_deadline}
                    </p>
                  </div>
                </div>
              )}

              {university.scholarships.how_to_apply && (
                <div>
                  <h4 className="text-sm font-semibold text-gray-400 mb-2">
                    How to Apply
                  </h4>
                  <p className="text-gray-300 text-sm">
                    {university.scholarships.how_to_apply}
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Additional Information Section */}
        {university.additional_info && (
          <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
            <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <Info className="w-6 h-6 text-blue-500" />
              Additional Information
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* International Program */}
              {university.additional_info.international_program !==
                undefined && (
                <div className="md:col-span-2">
                  <div className="flex items-center gap-2 bg-blue-500/10 rounded-lg p-3 border border-blue-500/30">
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
                  <h4 className="text-sm font-semibold text-gray-400 mb-2">
                    Campus Location
                  </h4>
                  <a
                    href={university.additional_info.google_maps_link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 bg-gray-700/50 hover:bg-gray-700 rounded-lg p-3 transition-colors group"
                  >
                    <MapPin className="w-5 h-5 text-blue-400" />
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
                  <h4 className="text-sm font-semibold text-gray-400 mb-3">
                    Contact Information
                  </h4>
                  <div className="space-y-2">
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
                  <h4 className="text-sm font-semibold text-gray-400 mb-2">
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
                  <h4 className="text-sm font-semibold text-gray-400 mb-2">
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
                  <h4 className="text-sm font-semibold text-gray-400 mb-2">
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
                    <h4 className="text-sm font-semibold text-gray-400 mb-2">
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
                    <h4 className="text-sm font-semibold text-gray-400 mb-2">
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
                  <h4 className="text-sm font-semibold text-gray-400 mb-2">
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

        {/* Action Buttons */}
        <div className="flex gap-4 pt-4">
          <button
            onClick={onClose}
            className="flex-1 px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors font-semibold"
          >
            Close
          </button>
          <button
            onClick={() => {
              window.open(
                `https://www.google.com/search?q=${encodeURIComponent(
                  university.name
                )}`,
                "_blank"
              );
            }}
            className="flex-1 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors font-semibold flex items-center justify-center gap-2"
          >
            <Globe className="w-5 h-5" />
            Learn More
          </button>
        </div>
      </div>
    </Modal>
  );
}

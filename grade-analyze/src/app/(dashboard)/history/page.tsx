"use client";

import React from 'react';
import { useDashboard } from '../layout';
import RecommendationDashboard from '../../../components/RecommendationDashboard';
import { AnalysisResult } from '../../../types';
import { Clock, Calendar } from 'lucide-react';

export default function HistoryPage() {
  const { analysisHistory, selectedHistoryId } = useDashboard();

  // Find the selected analysis
  const selectedItem = analysisHistory.find((item) => item.id === selectedHistoryId) ?? null;

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  // No item selected
  if (!selectedItem) {
    return (
      <div className="px-2 lg:px-20">
        <div className="p-8 text-center">
          <Clock size={65} className="text-blue-500 mx-auto mb-4" />
          <p className="text-gray-200 text-lg">
            Select an analysis from the History sidebar to view its recommendations.
          </p>
        </div>
      </div>
    );
  }

  // Build AnalysisResult shape for RecommendationDashboard
  const analysisData: AnalysisResult = {
    majors: selectedItem.majors as AnalysisResult['majors'],
    careers: selectedItem.careers as AnalysisResult['careers'],
    universities: selectedItem.universities as AnalysisResult['universities'],
    skill_gaps: selectedItem.skill_gaps as AnalysisResult['skill_gaps'],
    subject_analysis: (selectedItem.subject_analysis as AnalysisResult['subject_analysis']) || ({} as AnalysisResult['subject_analysis']),
  };

  return (
    <div className="px-2 lg:px-20">
      {/* Date header */}
      <div className="flex items-center justify-center sm:justify-center md:justify-start lg:justify-start mb-1 sm:mb-1 md:mb-6 lg:mb-6">
        <span className="text-xs text-gray-400 flex items-center gap-1.5 bg-[#1a1a1a] border border-[#2a2a2a] px-3 py-1.5 rounded-full">
          <Calendar className='text-blue-500' size={12} /> {formatDate(selectedItem.createdAt)}
        </span>
      </div>

      {/* Recommendation Dashboard */}
      <div className="rec-dashboard-responsive">
        <RecommendationDashboard data={analysisData} />
      </div>
    </div>
  );
}

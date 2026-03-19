"use client";

import React from 'react';
import {
  TrendingUp,
  MessageSquare,
  Send,
} from 'lucide-react';
import RecommendationDashboard from '../../../components/RecommendationDashboard';
import { useDashboard } from '../layout';

export default function DashboardOverviewComponent() {
  const { analysisCount, chatCount, requestCount, recentAnalysis } = useDashboard();

  return (
    <div>
      {/* Stats cards */}
      <div className="grid grid-cols-2 lg:grid-cols-3 gap-4 mb-8 px-2 lg:px-20">
        {/* Analysis */}
        <div className="bg-[#111111] border border-[#2a2a2a] rounded-xl p-3 lg:p-5">
          <div className="flex items-center gap-1.5 lg:gap-2 mb-2 lg:mb-3">
            <div className="p-1 lg:p-1.5">
              <TrendingUp size={18} className="text-green-400"/>
            </div>
            <p className="text-xs lg:text-lg text-white tracking-wide leading-tight">Analysis <span className="text-xs lg:text-sm text-gray-400">(Total)</span></p>
          </div>
          <p className="text-xl lg:text-3xl font-bold text-white ml-1">{analysisCount}</p>
        </div>

        {/* Chats */}
        <div className="bg-[#111111] border border-[#2a2a2a] rounded-xl p-3 lg:p-5">
          <div className="flex items-center gap-1.5 lg:gap-2 mb-2 lg:mb-3">
            <div className="p-1 lg:p-1.5">
              <MessageSquare size={18} className="text-blue-400" />
            </div>
            <p className="text-xs lg:text-lg text-white tracking-wide leading-tight">Chats <span className="text-xs lg:text-sm text-gray-400">(Total)</span></p>
          </div>
          <p className="text-xl lg:text-3xl font-bold text-white ml-1">{chatCount}</p>
        </div>

        {/* Requests */}
        <div className="col-span-2 lg:col-span-1 bg-[#111111] border border-[#2a2a2a] rounded-xl p-3 lg:p-5">
          <div className="flex items-center gap-1.5 lg:gap-2 mb-2 lg:mb-3">
            <div className="p-1 lg:p-1.5">
              <Send size={18} className="text-blue-400" />
            </div>
            <p className="text-xs lg:text-lg text-white tracking-wide leading-tight">Requests <span className="text-xs lg:text-sm text-gray-400">(Total)</span></p>
          </div>
          <p className="text-xl lg:text-3xl font-bold text-white ml-1">{requestCount}</p>
        </div>
      </div>

      {/* Recent Analysis */}
      <div className="px-2 lg:px-20 mt-4">
        <div className="flex items-center justify-center mb-1 sm:mb-3 md:mb-6">
          <div className="inline-flex items-center gap-2 px-3 py-2 rounded-md bg-[#1a1a1a] border border-[#2a2a2a]">
            <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
            <span className="text-sm text-gray-400">Recent Analysis</span>
          </div>
        </div>
        {recentAnalysis ? (
          <div className="rec-dashboard-responsive">
            <RecommendationDashboard data={recentAnalysis} />
          </div>
        ) : (
          <div className="bg-[#111111] border border-[#2a2a2a] rounded-xl p-6 text-center">
            <p className="text-gray-400 text-sm">No analysis yet. Go to the Analyze page to get started.</p>
          </div>
        )}
      </div>
    </div>
  );
}

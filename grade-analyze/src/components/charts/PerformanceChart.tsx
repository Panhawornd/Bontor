"use client";

import { Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

interface PerformanceChartProps {
  subjects: Record<string, { score: number; normalized: number; strength: string }>
}

export default function PerformanceChart({ subjects }: PerformanceChartProps) {
  const subjectEntries = Object.entries(subjects)

  const data = {
    labels: subjectEntries.map(([name]) => name.charAt(0).toUpperCase() + name.slice(1)),
    datasets: [
      {
        label: 'Normalized Score',
        data: subjectEntries.map(([, d]) => d.normalized * 100),
        backgroundColor: 'rgba(59, 130, 246, 0.8)',
        borderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 1,
      },
    ],
  }

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: { legend: { display: false } },
    scales: {
      y: { beginAtZero: true, max: 100 },
    },
  }

  return (
    <div className="h-64">
      <Bar data={data} options={options} />
    </div>
  )
}

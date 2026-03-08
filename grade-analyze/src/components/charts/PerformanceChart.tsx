"use client";

import { useState, useEffect } from 'react'
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

const SUBJECT_ORDER = ['math', 'physics', 'chemistry', 'biology', 'khmer', 'english', 'history', 'geography', 'moral', 'earth']

interface PerformanceChartProps {
  subjects: Record<string, { score: number; normalized: number; strength: string }>
}

export default function PerformanceChart({ subjects }: PerformanceChartProps) {
  const [isMobile, setIsMobile] = useState(false)

  useEffect(() => {
    const check = () => setIsMobile(window.innerWidth < 768)
    check()
    window.addEventListener('resize', check)
    return () => window.removeEventListener('resize', check)
  }, [])

  const subjectEntries = Object.entries(subjects).sort(([a], [b]) => {
    const ia = SUBJECT_ORDER.indexOf(a.toLowerCase())
    const ib = SUBJECT_ORDER.indexOf(b.toLowerCase())
    return (ia === -1 ? 999 : ia) - (ib === -1 ? 999 : ib)
  })

  const data = {
    labels: subjectEntries.map(([name]) => name.charAt(0).toUpperCase() + name.slice(1)),
    datasets: [
      {
        label: 'Normalized Score',
        data: subjectEntries.map(([, d]) => d.normalized),
        backgroundColor: 'rgba(59, 130, 246, 0.8)',
        borderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 1,
      },
    ],
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: {
      x: {
        ticks: {
          font: { size: isMobile ? 9 : 12 },
          maxRotation: isMobile ? 45 : 0,
          minRotation: isMobile ? 45 : 0,
        },
      },
      y: { 
        beginAtZero: true, 
        max: 100,
        ticks: {
          font: { size: isMobile ? 9 : 12 },
        },
      },
    },
  }

  return (
    <div style={{ width: '100%', height: '100%' }}>
      <Bar data={data} options={options} />
    </div>
  )
}

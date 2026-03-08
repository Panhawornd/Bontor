"use client";

import { useState, useEffect } from 'react'
import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend, Filler)

interface SkillRadarChartProps {
  skillGaps: Array<{ skill: string; current_level: number; required_level: number }>
}

export default function SkillRadarChart({ skillGaps }: SkillRadarChartProps) {
  const [isMobile, setIsMobile] = useState(false)

  useEffect(() => {
    const check = () => setIsMobile(window.innerWidth < 768)
    check()
    window.addEventListener('resize', check)
    return () => window.removeEventListener('resize', check)
  }, [])
  const data = {
    labels: skillGaps.map(gap => gap.skill),
    datasets: [
      {
        label: 'Current Level',
        data: skillGaps.map(gap => gap.current_level),
        borderColor: 'rgba(59, 130, 246, 0.8)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        borderWidth: 3,
        pointBackgroundColor: 'rgba(59, 130, 246, 1)',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2,
        pointRadius: 6,
        fill: true,
        tension: 0.4,
      },
      {
        label: 'Required Level',
        data: skillGaps.map(gap => gap.required_level),
        borderColor: 'rgba(34, 197, 94, 0.8)',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        borderWidth: 3,
        pointBackgroundColor: 'rgba(34, 197, 94, 1)',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2,
        pointRadius: 6,
        fill: true,
        tension: 0.4,
      },
    ],
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { 
      legend: { 
        display: false
      }
    },
    scales: {
      x: {
        display: true,
        grid: {
          display: false
        },
        ticks: {
          maxRotation: isMobile ? 45 : 0,
          minRotation: isMobile ? 45 : 0,
          padding: 5,
          font: { size: isMobile ? 9 : 12 },
          callback: function(value: string | number, index: number): string {
            const labels = skillGaps.map(gap => gap.skill);
            const label: string = labels[index] || '';
            
            const totalSkills = skillGaps.length;
            let maxLength: number;
            
            if (isMobile) {
              maxLength = totalSkills <= 3 ? 10 : totalSkills <= 5 ? 7 : 5;
            } else if (totalSkills <= 3) {
              maxLength = 15;
            } else if (totalSkills <= 5) {
              maxLength = 12;
            } else {
              maxLength = 8;
            }
            
            return label.length > maxLength ? label.substring(0, maxLength) + '...' : label;
          }
        }
      },
      y: { 
        beginAtZero: true, 
        max: 10,
        grid: {
          display: true,
          color: 'rgba(255, 255, 255, 0.1)'
        },
        ticks: {
          stepSize: 2,
          padding: 10
        }
      } 
    },
    layout: {
      padding: {
        left: 0,
        right: 0,
        top: 10,
        bottom: 20
      }
    }
  }

  return (
    <div style={{
      width: '100%',
      height: '100%',
      minHeight: '250px'
    }}>
      <Line data={data} options={options} />
    </div>
  )
}
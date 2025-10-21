"use client";

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
          maxRotation: 0,
          minRotation: 0,
          padding: 5,
          callback: function(value: string | number, index: number): string {
            const labels = skillGaps.map(gap => gap.skill);
            const label: string = labels[index] || '';
            
            // Calculate dynamic character limit based on number of skills
            const totalSkills = skillGaps.length;
            let maxLength: number;
            
            if (totalSkills <= 3) {
              maxLength = 15; // More space for fewer skills
            } else if (totalSkills <= 5) {
              maxLength = 12; // Medium space
            } else {
              maxLength = 8; // Less space for many skills
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
      height: '256px',
      width: '100%'
    }}>
      <Line data={data} options={options} />
    </div>
  )
}
"use client";

import { useState } from 'react'

interface GradeAnalysisData {
  grades: Array<{ subject: string; score: number }>
  interest_text: string
  career_goals: string
}

interface GradeInputFormProps {
  onSubmit: (data: GradeAnalysisData) => void
  loading: boolean
}

const SUBJECTS = [
  { id: 'math', name: 'Mathematics', category: 'Science', maxScore: 125 },
  { id: 'physics', name: 'Physics', category: 'Science', maxScore: 75 },
  { id: 'chemistry', name: 'Chemistry', category: 'Science', maxScore: 75 },
  { id: 'biology', name: 'Biology', category: 'Science', maxScore: 75 },
  { id: 'khmer', name: 'Khmer Literature', category: 'Language', maxScore: 75 },
  { id: 'english', name: 'English', category: 'Language', maxScore: 50 },
  { id: 'history', name: 'History', category: 'Social Studies', maxScore: 50 },
]

export default function GradeInputForm({ onSubmit, loading }: GradeInputFormProps) {
  const [grades, setGrades] = useState<Record<string, string>>({})
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [interestText, setInterestText] = useState('')
  const [careerGoals, setCareerGoals] = useState('')

  const validateGrade = (subject: string, value: string): string => {
    const subjDef = SUBJECTS.find(s => s.id === subject)
    const maxScore = subjDef?.maxScore ?? 100
    const s = (value || '').trim().toUpperCase()
    const LETTER_MAP: Record<string, number> = { A: 95, B: 85, C: 75, D: 65, E: 55 }
    if (!s) return ''
    const asNumber = LETTER_MAP[s] ?? parseFloat(s)
    if (isNaN(asNumber)) return 'Enter A–E or a valid number'
    if (asNumber < 0 || asNumber > maxScore) return `Must be between 0 and ${maxScore}`
    return ''
  }

  const handleGradeChange = (subject: string, value: string) => {
    setGrades(prev => ({ ...prev, [subject]: value }))
    const err = validateGrade(subject, value)
    setErrors(prev => ({ ...prev, [subject]: err }))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    // Validate and normalize inputs: allow A-E letters or numbers within each subject's max
    const normalizedGrades = Object.entries(grades).map(([subject, score]) => {
      const subjDef = SUBJECTS.find(s => s.id === subject)
      const maxScore = subjDef?.maxScore ?? 100
      const s = (score || '').trim().toUpperCase()
      const LETTER_MAP: Record<string, number> = { A: 95, B: 85, C: 75, D: 65, E: 55 }
      const asNumber = LETTER_MAP[s] ?? parseFloat(s)
      const value = isNaN(asNumber) ? 0 : asNumber
      const clamped = Math.min(Math.max(value, 0), maxScore)
      return { subject, score: clamped }
    })

    const formData = {
      grades: normalizedGrades,
      interest_text: interestText,
      career_goals: careerGoals,
    }

    onSubmit(formData)
  }

  const isFormValid = Object.entries(grades).every(([id, val]) => {
    const subj = SUBJECTS.find(s => s.id === id)
    if (!subj) return false
    const s = (val || '').trim().toUpperCase()
    const LETTER_MAP: Record<string, number> = { A: 95, B: 85, C: 75, D: 65, E: 55 }
    const asNumber = LETTER_MAP[s] ?? parseFloat(s)
    if (isNaN(asNumber)) return false
    return asNumber >= 0 && asNumber <= subj.maxScore
  }) && interestText.trim().length > 0

  return (
    <form onSubmit={handleSubmit} style={{ width: '100%' }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
        {/* Grades Section */}
        <div>
          <div style={{ marginBottom: '24px' }}>
            <h4 style={{ 
              fontSize: '20px', 
              fontWeight: '600', 
              marginBottom: '8px',
              color: 'var(--text-primary)'
            }}>
              BacII Exam Results
            </h4>
            <p style={{ 
              color: 'var(--text-secondary)', 
              fontSize: '14px',
              margin: 0
            }}>
              Enter your grades (A, B, C, D, E, or percentage 0-{Math.max(...SUBJECTS.map(s => s.maxScore))})
            </p>
          </div>
          
          <div className="grid-2-col">
            {SUBJECTS.map(subject => (
              <div key={subject.id} style={{
                padding: '20px',
                transition: 'all 0.2s ease'
              }}>
                <label style={{ 
                  fontSize: '14px', 
                  fontWeight: '500', 
                  marginBottom: '8px',
                  color: 'var(--text-primary)',
                  display: 'block'
                }}>
                  {subject.name}
                  <span style={{ 
                    color: 'var(--text-muted)', 
                    fontSize: '12px',
                    fontWeight: '400',
                    marginLeft: '8px'
                  }}>
                    ({subject.category}) - Max: {subject.maxScore}
                  </span>
                </label>
                <input
                  type="text"
                  placeholder={`Ex, A or ${subject.maxScore}`}
                  className="input-field"
                  value={grades[subject.id] || ''}
                  onChange={(e) => handleGradeChange(subject.id, e.target.value)}
                  style={{ margin: 0 }}
                />
              {errors[subject.id] && (
                <div style={{ marginTop: '6px', fontSize: '12px', color: 'var(--error, #ef4444)' }}>
                  {errors[subject.id]}
                </div>
              )}
              </div>
            ))}
          </div>
        </div>

        {/* Interests Section */}
        <div>
          <h4 style={{ 
            fontSize: '20px', 
            fontWeight: '600', 
            marginBottom: '8px',
            color: 'var(--text-primary)'
          }}>
            Your Interests & Strengths
          </h4>
          <p style={{ 
            color: 'var(--text-secondary)', 
            fontSize: '14px',
            marginBottom: '16px'
          }}>
            Describe your interests, hobbies, skills, and what you enjoy doing. Be as detailed as possible!
          </p>
          <textarea
            className="input-field"
            style={{ 
              minHeight: '120px', 
              resize: 'vertical',
              fontFamily: 'inherit',
              lineHeight: '1.5'
            }}
            placeholder="I love programming and building apps. I enjoy working with data and solving complex problems. I'm also interested in artificial intelligence and machine learning..."
            value={interestText}
            onChange={(e) => setInterestText(e.target.value)}
            required
          />
        </div>

        {/* Career Goals Section */}
        <div>
          <h4 style={{ 
            fontSize: '20px', 
            fontWeight: '600', 
            marginBottom: '8px',
            color: 'var(--text-primary)'
          }}>
            Career Goals (Optional)
          </h4>
          <p style={{ 
            color: 'var(--text-secondary)', 
            fontSize: '14px',
            marginBottom: '16px'
          }}>
            What kind of career are you interested in? This helps us provide more targeted recommendations.
          </p>
          <textarea
            className="input-field"
            style={{ 
              minHeight: '100px', 
              resize: 'vertical',
              fontFamily: 'inherit',
              lineHeight: '1.5'
            }}
            placeholder="I want to become a software engineer and work for a tech company. I'm also interested in starting my own business..."
            value={careerGoals}
            onChange={(e) => setCareerGoals(e.target.value)}
          />
        </div>


        {/* Submit Button */}
        <div style={{ paddingTop: '16px' }}>
          <button 
            type="submit" 
            disabled={!isFormValid || loading} 
            className="px-4 py-1.5 text-white rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            style={{ 
              width: '100%',
              backgroundColor: isFormValid ? '#1d4ed8' : '#1f2937',
              borderWidth: '1px',
              borderStyle: 'solid',
              borderColor: isFormValid ? '#1d4ed8' : '#374151'
            }}
            onMouseEnter={(e) => {
              if (isFormValid && !loading) {
                e.currentTarget.style.backgroundColor = '#1e40af'
                e.currentTarget.style.borderColor = '#1e40af'
              }
            }}
            onMouseLeave={(e) => {
              if (isFormValid && !loading) {
                e.currentTarget.style.backgroundColor = '#1d4ed8'
                e.currentTarget.style.borderColor = '#1d4ed8'
              }
            }}
          >
            {loading ? (
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
                <div style={{
                  width: '16px',
                  height: '16px',
                  border: '2px solid rgba(255,255,255,0.3)',
                  borderTop: '2px solid white',
                  borderRadius: '50%',
                  animation: 'spin 1s linear infinite'
                }} />
                Analyzing Your Profile...
              </div>
            ) : (
              'Analyze My Results'
            )}
          </button>
        </div>
      </div>

      <style jsx>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </form>
  )
}

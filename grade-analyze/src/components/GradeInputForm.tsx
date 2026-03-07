"use client";

import { useState, useEffect, useRef } from 'react'

interface GradeAnalysisData {
  grades: Array<{ subject: string; score: number }>
  interest_text: string
  career_goals: string
}

interface GradeInputFormProps {
  onSubmit: (data: GradeAnalysisData) => void
  loading: boolean
  initialData?: {
    grades: Record<string, string>
    interestText: string
    careerGoals: string
    examType: 'science' | 'social-science'
  }
  onFormChange?: (data: {
    grades: Record<string, string>
    interestText: string
    careerGoals: string
    examType: 'science' | 'social-science'
  }) => void
}

type ExamType = 'science' | 'social-science'

const SCIENCE_SUBJECTS = [
  { id: 'math', name: 'Mathematics', category: 'Science', maxScore: 125 },
  { id: 'physics', name: 'Physics', category: 'Science', maxScore: 75 },
  { id: 'chemistry', name: 'Chemistry', category: 'Science', maxScore: 75 },
  { id: 'biology', name: 'Biology', category: 'Science', maxScore: 75 },
  { id: 'khmer', name: 'Khmer Literature', category: 'Language', maxScore: 75 },
  { id: 'english', name: 'English', category: 'Language', maxScore: 50 },
  { id: 'history', name: 'History', category: 'Social Studies', maxScore: 50 },
]

const SOCIAL_SCIENCE_SUBJECTS = [
  { id: 'khmer', name: 'Khmer Literature', category: 'Language', maxScore: 125 },
  { id: 'math', name: 'Mathematics', category: 'Science', maxScore: 75 },
  { id: 'geography', name: 'Geography', category: 'Social Studies', maxScore: 75 },
  { id: 'history', name: 'History', category: 'Social Studies', maxScore: 75 },
  { id: 'moral', name: 'Moral Education', category: 'Social Studies', maxScore: 75 },
  { id: 'earth', name: 'Earth', category: 'Science', maxScore: 50 },
  { id: 'english', name: 'English', category: 'Language', maxScore: 50 },
]

export default function GradeInputForm({ onSubmit, loading, initialData, onFormChange }: GradeInputFormProps) {
  const [examType, setExamType] = useState<ExamType>(initialData?.examType || 'science')
  const [grades, setGrades] = useState<Record<string, string>>(initialData?.grades || {})
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [interestText, setInterestText] = useState(initialData?.interestText || '')
  const [careerGoals, setCareerGoals] = useState(initialData?.careerGoals || '')
  
  // Ref to track initial mount
  const isInitialMount = useRef(true)

  // Notify parent of form changes (skip initial mount)
  useEffect(() => {
    if (isInitialMount.current) {
      isInitialMount.current = false
      return
    }
    onFormChange?.({ grades, interestText, careerGoals, examType })
  }, [grades, interestText, careerGoals, examType, onFormChange])

  const SUBJECTS = examType === 'science' ? SCIENCE_SUBJECTS : SOCIAL_SCIENCE_SUBJECTS

  const interestPlaceholder = examType === 'social-science'
    ? 'I enjoy debating, understanding legal systems, justice, public policy, and human rights...'
    : 'I love programming and building apps. I enjoy working with data and solving complex problems...'

  const careerPlaceholder = examType === 'social-science'
    ? 'I want to study law and become a lawyer, or work in public policy/legal advocacy...'
    : 'I want to become a software engineer and work for a tech company...'

  const handleExamTypeChange = (newType: ExamType) => {
    if (newType !== examType) {
      setExamType(newType)
      setGrades({})
      setErrors({})
    }
  }

  const validateGrade = (subject: string, value: string): string => {
    const subjDef = SUBJECTS.find(s => s.id === subject)
    const maxScore = subjDef?.maxScore ?? 100
    const s = (value || '').trim()
    if (!s) return ''
    const asNumber = parseFloat(s)
    if (isNaN(asNumber)) return 'Enter a valid number'
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

    const nextErrors: Record<string, string> = {}
    const normalizedGrades = SUBJECTS.map((subject) => {
      const raw = (grades[subject.id] || '').trim()
      if (!raw) {
        nextErrors[subject.id] = `Required (0-${subject.maxScore})`
        return { subject: subject.id, score: 0 }
      }

      const asNumber = parseFloat(raw)
      if (isNaN(asNumber) || asNumber < 0 || asNumber > subject.maxScore) {
        nextErrors[subject.id] = `Must be between 0 and ${subject.maxScore}`
      }

      const value = isNaN(asNumber) ? 0 : asNumber
      const clamped = Math.min(Math.max(value, 0), subject.maxScore)
      return { subject: subject.id, score: clamped }
    })

    setErrors(nextErrors)

    if (Object.keys(nextErrors).length > 0 || interestText.trim().length === 0) {
      return
    }

    const formData = {
      grades: normalizedGrades,
      interest_text: interestText,
      career_goals: careerGoals,
    }

    onSubmit(formData)
  }

  const isFormValid = SUBJECTS.every((subject) => {
    const s = (grades[subject.id] || '').trim()
    const asNumber = parseFloat(s)
    if (!s || isNaN(asNumber)) return false
    return asNumber >= 0 && asNumber <= subject.maxScore
  }) && interestText.trim().length > 0

  return (
    <form onSubmit={handleSubmit} style={{ width: '100%' }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
        {/* Exam Type Toggle */}
        <div style={{ marginBottom: '8px' }}>
          <div style={{ 
            display: 'flex', 
            gap: '12px',
            backgroundColor: '#1a1a1a',
            padding: '4px',
            borderRadius: '8px',
            border: '1px solid #2a2a2a'
          }}>
            <button
              type="button"
              onClick={() => handleExamTypeChange('science')}
              style={{
                flex: 1,
                padding: '10px 16px',
                borderRadius: '6px',
                fontSize: '14px',
                fontWeight: '500',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                backgroundColor: examType === 'science' ? '#1f2937' : 'transparent',
                color: examType === 'science' ? '#ffffff' : 'var(--text-secondary)',
                border: 'none',
                outline: 'none'
              }}
            >
              Science
            </button>
            <button
              type="button"
              onClick={() => handleExamTypeChange('social-science')}
              style={{
                flex: 1,
                padding: '10px 16px',
                borderRadius: '6px',
                fontSize: '14px',
                fontWeight: '500',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                backgroundColor: examType === 'social-science' ? '#1f2937' : 'transparent',
                color: examType === 'social-science' ? '#ffffff' : 'var(--text-secondary)',
                border: 'none',
                outline: 'none'
              }}
            >
              Social Science
            </button>
          </div>
        </div>

        {/* Grades Section */}
        <div>
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
                  inputMode="numeric"
                  pattern="[0-9]*"
                  placeholder={`Enter score (0-${subject.maxScore})`}
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
            placeholder={interestPlaceholder}
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
            placeholder={careerPlaceholder}
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
              <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
                <svg className="logo-spin" width="24" height="24" viewBox="-30 -30 201 233" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ display: 'block' }}>
                  <g>
                    <path d="M110.464 0C127.032 0.000247877 140.464 13.4316 140.464 30V31.4922H92.9033V58.2891H49.9043V86.3154H0V30C0 13.4315 13.4315 1.61637e-06 30 0H110.464Z" fill="white"/>
                  </g>
                  <g>
                    <path d="M30.5372 172.649C13.9687 172.67 0.453776 159.257 0.350835 142.689L0.341564 141.196L47.9011 141.134L47.7346 114.338L90.7336 114.282L90.5595 86.2549L140.464 86.1897L140.814 142.505C140.917 159.073 127.569 172.522 111 172.544L30.5372 172.649Z" fill="#3B82F6"/>
                  </g>
                </svg>
                Analyzing Your Profile...
              </span>
            ) : (
              'Analyze My Results'
            )}
          </button>
        </div>
      </div>

    </form>
  )
}
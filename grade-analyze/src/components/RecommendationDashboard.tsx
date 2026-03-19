import PerformanceChart from './charts/PerformanceChart'
import SkillRadarChart from './charts/SkillRadarChart'

interface RecommendationDashboardProps {
  data: {
    majors: Array<{ name: string; score: number; description: string; source?: string }>
    careers: Array<{ title: string; match_score: number; description: string }>
    universities: Array<{ name: string; country: string; programs: string[] }>
    skill_gaps: Array<{ skill: string; current_level: number; required_level: number; suggestions: string[] }>
    subject_analysis: Record<string, { score: number; normalized: number; strength: string }>
  }
}

export default function RecommendationDashboard({ data }: RecommendationDashboardProps) {
  return (
    <div className="rec-dashboard-container" style={{ 
      display: 'flex', 
      flexDirection: 'column', 
      gap: '24px',
      maxWidth: '1400px',
      margin: '0 auto',
      padding: '0'
    }}>
      {/* Charts Section */}
      <div className="rec-charts-grid" style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 500px), 1fr))', 
        gap: '20px',
        alignItems: 'start'
      }}>
        <div className="rec-chart-card" style={{
          background: 'var(--bg-secondary)',
          border: '1px solid var(--border-primary)',
          borderRadius: '12px',
          padding: '24px',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
          height: '380px',
          display: 'flex',
          flexDirection: 'column'
        }}>
          <h3 className="rec-section-title" style={{ 
            fontSize: '22px', 
            fontWeight: '700', 
            marginBottom: '20px',
            color: 'var(--text-primary)',
            textAlign: 'center',
            borderBottom: '2px solid var(--accent-primary)',
            paddingBottom: '10px'
          }}>
            Subject Performance
          </h3>
          <div style={{ flex: 1 }}>
            <PerformanceChart subjects={data.subject_analysis} />
          </div>
        </div>
        
        <div className="rec-chart-card rec-skill-chart" style={{
          background: 'var(--bg-secondary)',
          border: '1px solid var(--border-primary)',
          borderRadius: '12px',
          padding: '24px',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
          height: '380px',
          display: 'flex',
          flexDirection: 'column'
        }}>
          <h3 className="rec-section-title" style={{ 
            fontSize: '22px', 
            fontWeight: '700', 
            marginBottom: '8px',
            color: 'var(--text-primary)',
            textAlign: 'center',
            borderBottom: '2px solid var(--accent-primary)',
            paddingBottom: '10px'
          }}>
            Skills Analysis
          </h3>
          
          {/* Custom Legend */}
          <div style={{
            display: 'flex',
            justifyContent: 'center',
            gap: '30px',
            marginTop: '10px',
            marginBottom: '0px',
            
          }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}>
              <div style={{
                width: '20px',
                height: '3px',
                backgroundColor: 'rgba(59, 130, 246, 0.8)',
                borderRadius: '2px'
              }}></div>
              <span className="rec-legend-label" style={{
                fontSize: '12px',
                color: 'var(--text-primary)',
                fontWeight: '500'
              }}>Current Level</span>
            </div>
            
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}>
              <div style={{
                width: '20px',
                height: '3px',
                backgroundColor: 'rgba(34, 197, 94, 0.8)',
                borderRadius: '2px'
              }}></div>
              <span className="rec-legend-label" style={{
                fontSize: '12px',
                color: 'var(--text-primary)',
                fontWeight: '500'
              }}>Required Level</span>
            </div>
          </div>
          
          <div style={{ flex: 1, paddingTop: '12px' }}>
            <SkillRadarChart skillGaps={data.skill_gaps} />
          </div>
        </div>
      </div>

      {/* Majors Section */}
      <div className="rec-section-card" style={{
        background: 'var(--bg-secondary)',
        border: '1px solid var(--border-primary)',
        borderRadius: '12px',
        padding: '32px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
      }}>
        <h3 className="rec-section-title" style={{ 
          fontSize: '22px', 
          fontWeight: '700', 
          marginBottom: '28px',
          color: 'var(--text-primary)',
          textAlign: 'center',
          borderBottom: '2px solid var(--accent-primary)',
          paddingBottom: '16px'
        }}>
          Recommended Academic Majors
        </h3>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {data.majors.map((major, index) => (
            <div 
              key={index}
              className="rec-major-card"
              style={{
                background: 'var(--bg-tertiary)',
                border: '1px solid var(--border-primary)',
                borderRadius: '12px',
                padding: '24px',
                transition: 'all 0.2s ease',
                position: 'relative',
                overflow: 'hidden'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = '#6b7280'
                e.currentTarget.style.backgroundColor = '#374151'
                e.currentTarget.style.boxShadow = 'var(--shadow-secondary)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = 'var(--border-primary)'
                e.currentTarget.style.backgroundColor = 'var(--bg-tertiary)'
                e.currentTarget.style.boxShadow = 'none'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                <h3 style={{ 
                  fontSize: '18px', 
                  fontWeight: '600', 
                  color: 'var(--accent-primary)',
                  margin: 0
                }}>
                  {index + 1}. {major.name}
                </h3>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexShrink: 0 }}>
                  <span className="rec-match-badge" style={{
                    fontSize: '12px',
                    background: 'rgba(59, 130, 246, 0.1)',
                    color: '#ffffff',
                    padding: '5px 10px',
                    borderRadius: '20px',
                    border: '1px solid rgba(59, 130, 246, 0.3)',
                    fontWeight: '500'
                  }}>
                    {(major.score * 100).toFixed(0)}% Match
                  </span>
                </div>
              </div>
              
              <p style={{ 
                color: 'var(--text-secondary)', 
                fontSize: '14px',
                lineHeight: 1.6,
                margin: 0
              }}>
                {major.description}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Careers Section */}
      <div className="rec-section-card" style={{
        background: 'var(--bg-secondary)',
        border: '1px solid var(--border-primary)',
        borderRadius: '12px',
        padding: '32px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
      }}>
        <h3 className="rec-section-title" style={{ 
          fontSize: '22px', 
          fontWeight: '700', 
          marginBottom: '28px',
          color: 'var(--text-primary)',
          textAlign: 'center',
          borderBottom: '2px solid var(--accent-primary)',
          paddingBottom: '16px'
        }}>
          Suggested Career Paths
        </h3>
        
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 300px), 1fr))', 
          gap: '16px' 
        }}>
          {data.careers.map((career, index) => (
            <div 
              key={index}
              className="rec-career-card"
              style={{
                background: 'var(--bg-tertiary)',
                border: '1px solid var(--border-primary)',
                borderRadius: '12px',
                padding: '20px',
                transition: 'all 0.2s ease'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = '#6b7280'
                e.currentTarget.style.backgroundColor = '#374151'
                e.currentTarget.style.boxShadow = 'var(--shadow-secondary)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = 'var(--border-primary)'
                e.currentTarget.style.backgroundColor = 'var(--bg-tertiary)'
                e.currentTarget.style.boxShadow = 'none'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                <h3 style={{ 
                  fontSize: '16px', 
                  fontWeight: '600', 
                  color: 'var(--text-primary)',
                  margin: 0
                }}>
                  {career.title}
                </h3>
                <span className="rec-match-badge" style={{
                  fontSize: '11px',
                  background: 'rgba(59, 130, 246, 0.1)',
                  color: '#ffffff',
                  padding: '4px 8px',
                  borderRadius: '12px',
                  border: '1px solid rgba(59, 130, 246, 0.3)'
                }}>
                  {(career.match_score * 100).toFixed(0)}%
                </span>
              </div>
              <p style={{ 
                color: 'var(--text-secondary)', 
                fontSize: '14px',
                lineHeight: 1.5,
                margin: 0
              }}>
                {career.description}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Universities Section */}
      <div className="rec-section-card" style={{
        background: 'var(--bg-secondary)',
        border: '1px solid var(--border-primary)',
        borderRadius: '12px',
        padding: '32px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
      }}>
        <h3 className="rec-section-title" style={{ 
          fontSize: '22px', 
          fontWeight: '700', 
          marginBottom: '28px',
          color: 'var(--text-primary)',
          textAlign: 'center',
          borderBottom: '2px solid var(--accent-primary)',
          paddingBottom: '16px'
        }}>
          Recommended Universities
        </h3>
        
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 280px), 1fr))', 
          gap: '16px' 
        }}>
          {data.universities.map((uni, index) => (
            <div 
              key={index}
              className="rec-university-card"
              style={{
                background: 'var(--bg-tertiary)',
                border: '1px solid var(--border-primary)',
                borderRadius: '12px',
                padding: '20px',
                transition: 'all 0.2s ease'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = '#6b7280'
                e.currentTarget.style.backgroundColor = '#374151'
                e.currentTarget.style.boxShadow = 'var(--shadow-secondary)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = 'var(--border-primary)'
                e.currentTarget.style.backgroundColor = 'var(--bg-tertiary)'
                e.currentTarget.style.boxShadow = 'none'
              }}
            >
              <h3 style={{ 
                fontSize: '16px', 
                fontWeight: '600', 
                color: 'var(--text-primary)',
                marginBottom: '8px'
              }}>
                {uni.name}
              </h3>
              <p style={{ 
                fontSize: '14px', 
                color: 'var(--text-secondary)', 
                marginBottom: '16px' 
              }}>
                {uni.country}
              </p>
              <div>
                <p className="rec-section-p" style={{ 
                  fontSize: '12px', 
                  color: 'var(--text-muted)', 
                  marginBottom: '8px',
                  fontWeight: '500'
                }}>
                  Available Programs:
                </p>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                  {uni.programs.slice(0, 3).map((program, pIndex) => (
                    <p key={pIndex} style={{ 
                      fontSize: '12px', 
                      color: 'var(--text-secondary)',
                      margin: 0,
                      display: 'flex',
                      alignItems: 'center',
                      gap: '6px'
                    }}>
                      <span style={{ color: 'rgba(59, 130, 246, 1)' }}>•</span>
                      {program}
                    </p>
                  ))}
                  {uni.programs.length > 3 && (
                    <p style={{ 
                      fontSize: '12px', 
                      color: 'var(--accent-primary)',
                      margin: 0,
                      fontWeight: '500'
                    }}>
                      +{uni.programs.length - 3} more programs
                    </p>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Skills Section */}
      <div className="card rec-section-card" style={{
        background: 'var(--bg-secondary)',
        border: '1px solid var(--border-primary)',
        borderRadius: '16px',
        padding: '32px',
        boxShadow: 'var(--shadow-primary)',
        position: 'relative',
        overflow: 'hidden'
      }}>
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: '4px',
          background: 'var(--gradient-primary)'
        }} />
        
        <h2 className="rec-section-title" style={{ 
          fontSize: '22px', 
          fontWeight: '600', 
          marginBottom: '24px',
          color: 'var(--text-primary)'
        }}>
          Skills to Develop
        </h2>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {data.skill_gaps.map((gap, index) => (
            <div 
              key={index}
              className="rec-skill-card"
              style={{
                background: 'var(--bg-tertiary)',
                border: '1px solid var(--border-primary)',
                borderRadius: '16px',
                padding: '24px',
                transition: 'all 0.2s ease'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = '#6b7280'
                e.currentTarget.style.backgroundColor = '#374151'
                e.currentTarget.style.boxShadow = 'var(--shadow-secondary)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = 'var(--border-primary)'
                e.currentTarget.style.backgroundColor = 'var(--bg-tertiary)'
                e.currentTarget.style.boxShadow = 'none'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                <h3 style={{ 
                  fontSize: '18px', 
                  fontWeight: '600', 
                  color: 'var(--text-primary)',
                  margin: 0
                }}>
                  {gap.skill}
                </h3>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <span className="rec-level-badge" style={{
                    fontSize: '12px',
                    background: 'rgba(59, 130, 246, 0.1)',
                    color: '#ffffff',
                    padding: '6px 12px',
                    borderRadius: '16px',
                    border: '1px solid rgba(59, 130, 246, 0.3)',
                    fontWeight: '500'
                  }}>
                    Current: {gap.current_level}/10
                  </span>
                  <span className="rec-level-badge" style={{
                    fontSize: '12px',
                    background: 'rgba(40, 167, 69, 0.1)',
                    color: 'var(--accent-success)',
                    padding: '6px 12px',
                    borderRadius: '16px',
                    border: '1px solid rgba(40, 167, 69, 0.3)',
                    fontWeight: '500'
                  }}>
                    Target: {gap.required_level}/10
                  </span>
                </div>
              </div>
              
              <div style={{ 
                width: '100%', 
                background: 'var(--bg-primary)', 
                borderRadius: '8px', 
                height: '12px', 
                marginBottom: '16px', 
                overflow: 'hidden', 
                border: '1px solid var(--border-primary)' 
              }}>
                <div 
                  style={{ 
                    height: '12px', 
                    borderRadius: '8px', 
                    transition: 'all 0.7s ease-out', 
                    position: 'relative',
                    width: `${Math.min((gap.current_level / gap.required_level) * 100, 100)}%`,
                    background: 'var(--gradient-primary)'
                  }} 
                />
              </div>
              
              <div>
                <p style={{ 
                  fontSize: '14px', 
                  color: 'var(--text-muted)', 
                  marginBottom: '12px', 
                  fontWeight: '500' 
                }}>
                  Improvement Suggestions:
                </p>
                <div style={{ 
                  display: 'grid', 
                  gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 250px), 1fr))', 
                  gap: '8px' 
                }}>
                  {gap.suggestions.map((suggestion, sIndex) => (
                    <div key={sIndex} style={{ 
                      display: 'flex', 
                      alignItems: 'flex-start', 
                      gap: '8px',
                      fontSize: '14px',
                      color: 'var(--text-secondary)',
                    }}>
                        <span style={{ 
                          color: 'rgba(59, 130, 246, 1)', 
                          marginTop: '-1px',
                          fontWeight: 'bold',
                        }}>
                          •
                        </span>
                      <span>{suggestion}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}


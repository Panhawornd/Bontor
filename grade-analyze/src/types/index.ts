export interface AnalysisResult {
  majors: Array<{ name: string; score: number; description: string }>;
  careers: Array<{ title: string; match_score: number; description: string }>;
  universities: Array<{ name: string; country: string; programs: string[] }>;
  skill_gaps: Array<{ skill: string; current_level: number; required_level: number; suggestions: string[] }>;
  subject_analysis: Record<string, { score: number; normalized: number; strength: string }>;
}

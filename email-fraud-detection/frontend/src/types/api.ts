export interface User {
  id: number
  email: string
  full_name?: string
  role: 'admin' | 'analyst' | 'user'
  is_active: boolean
  created_at: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
  expires_at: string
}

export interface AnalysisResult {
  id: number
  user_id: number
  email_subject?: string
  email_from?: string
  email_to?: string
  fraud_score: number
  labels: Record<string, boolean>
  details: Record<string, unknown>
  created_at: string
}

export interface AnalysisSummary {
  total_analyses: number
  average_score: number
  phishing_pct: number
  spam_pct: number
  spoofing_pct: number
  bec_pct: number
}

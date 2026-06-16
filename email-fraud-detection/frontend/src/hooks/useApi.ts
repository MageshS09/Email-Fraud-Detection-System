const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

function getToken() {
  return localStorage.getItem('auth_token')
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken()
  const headers = new Headers(options.headers as HeadersInit)
  headers.set('Content-Type', 'application/json')
  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    const payload = await response.json().catch(() => null)
    throw new Error(payload?.detail || response.statusText)
  }

  return response.json() as Promise<T>
}

export function useApi() {
  return {
    login: async (email: string, password: string) => request('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }),
    register: async (email: string, password: string, full_name?: string) => request('/auth/register', { method: 'POST', body: JSON.stringify({ email, password, full_name }) }),
    fetchSummary: async () => request<import('../types/api').AnalysisSummary>('/analysis/summary'),
    fetchHistory: async () => request<import('../types/api').AnalysisResult[]>('/analysis/history'),
    analyzeText: async (email_raw: string) => request<import('../types/api').AnalysisResult>('/analysis/', { method: 'POST', body: JSON.stringify({ email_raw, source: 'paste' }) }),
  }
}

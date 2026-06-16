import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useApi } from '../hooks/useApi'
import { AnalysisResult } from '../types/api'

export default function AnalysisPage() {
  const [rawEmail, setRawEmail] = useState('')
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const api = useApi()
  const navigate = useNavigate()

  const handleAnalyze = async (event: React.FormEvent) => {
    event.preventDefault()
    setLoading(true)
    setError('')
    try {
      const response = await api.analyzeText(rawEmail)
      setResult(response)
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto mt-12 max-w-5xl px-4 sm:px-6 lg:px-8">
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:justify-between sm:items-center">
        <div>
          <h1 className="text-3xl font-bold">Analyze Email</h1>
          <p className="text-slate-600">Paste the email content or upload an .eml file from your inbox.</p>
        </div>
        <div className="flex gap-3">
          <Link to="/" className="rounded-2xl border border-slate-200 px-5 py-3 text-slate-700 hover:bg-slate-100">Back to dashboard</Link>
          <button onClick={() => { localStorage.removeItem('auth_token'); navigate('/login') }} className="rounded-2xl bg-slate-900 px-5 py-3 text-white hover:bg-slate-800">Sign out</button>
        </div>
      </div>

      <form onSubmit={handleAnalyze} className="space-y-6 rounded-3xl bg-white p-6 shadow-sm">
        <label className="block">
          <span className="text-sm font-medium">Email text or raw .eml contents</span>
          <textarea
            value={rawEmail}
            onChange={(event) => setRawEmail(event.target.value)}
            rows={12}
            className="mt-2 w-full rounded-3xl border p-4 text-slate-900 focus:outline-none focus:ring-2 focus:ring-sky-500"
            required
          />
        </label>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <button type="submit" disabled={loading} className="rounded-2xl bg-sky-600 px-6 py-3 text-white hover:bg-sky-700 disabled:cursor-not-allowed disabled:bg-slate-400">
          {loading ? 'Analyzing…' : 'Upload and analyze'}
        </button>
      </form>

      {result && (
        <div className="mt-8 rounded-3xl bg-white p-6 shadow-sm">
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <h2 className="text-xl font-semibold">Result</h2>
              <p className="text-slate-600">Fraud score: {result.fraud_score}</p>
            </div>
            <div className="space-y-3">
              {Object.entries(result.labels).map(([label, value]) => (
                <div key={label} className="flex items-center justify-between rounded-2xl bg-slate-50 p-4">
                  <span className="capitalize">{label.replace('_', ' ')}</span>
                  <span className={value ? 'text-emerald-600' : 'text-slate-500'}>{value ? 'Detected' : 'Clear'}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="mt-6 rounded-3xl bg-slate-50 p-4">
            <h3 className="text-lg font-semibold">Analysis details</h3>
            <pre className="mt-3 max-h-72 overflow-auto whitespace-pre-wrap text-sm text-slate-700">{JSON.stringify(result.details, null, 2)}</pre>
          </div>
        </div>
      )}
    </div>
  )
}

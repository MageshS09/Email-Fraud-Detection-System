import { useEffect, useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useApi } from '../hooks/useApi'
import { AnalysisResult } from '../types/api'

export default function HistoryPage() {
  const [history, setHistory] = useState<AnalysisResult[]>([])
  const [error, setError] = useState('')
  const api = useApi()
  const navigate = useNavigate()

  useEffect(() => {
    api.fetchHistory()
      .then(setHistory)
      .catch((err) => setError((err as Error).message))
  }, [api])

  return (
    <div className="mx-auto mt-12 max-w-6xl px-4 sm:px-6 lg:px-8">
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:justify-between sm:items-center">
        <div>
          <h1 className="text-3xl font-bold">Analysis history</h1>
          <p className="text-slate-600">Review your recent reports and risk details.</p>
        </div>
        <div className="flex gap-3">
          <Link to="/" className="rounded-2xl border border-slate-200 px-5 py-3 text-slate-700 hover:bg-slate-100">Dashboard</Link>
          <button onClick={() => { localStorage.removeItem('auth_token'); navigate('/login') }} className="rounded-2xl bg-slate-900 px-5 py-3 text-white hover:bg-slate-800">Sign out</button>
        </div>
      </div>

      {error ? (
        <p className="rounded-3xl bg-red-50 p-4 text-red-700">{error}</p>
      ) : (
        <div className="space-y-4">
          {history.map((item) => (
            <div key={item.id} className="rounded-3xl bg-white p-6 shadow-sm">
              <div className="flex flex-col gap-2 sm:flex-row sm:justify-between sm:items-center">
                <div>
                  <h2 className="text-lg font-semibold">{item.email_subject || 'Untitled email'}</h2>
                  <p className="text-sm text-slate-500">From: {item.email_from || 'unknown'} · To: {item.email_to || 'unknown'}</p>
                </div>
                <span className="rounded-full bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700">Score: {item.fraud_score}</span>
              </div>
              <div className="mt-4 grid gap-3 sm:grid-cols-2">
                {Object.entries(item.labels).map(([label, value]) => (
                  <div key={label} className="rounded-2xl bg-slate-50 p-4">
                    <span className="font-medium capitalize">{label.replace('_', ' ')}</span>
                    <p className={value ? 'text-emerald-600' : 'text-slate-500'}>{value ? 'Detected' : 'Clear'}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

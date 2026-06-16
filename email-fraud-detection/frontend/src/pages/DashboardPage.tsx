import { useEffect, useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useApi } from '../hooks/useApi'
import { AnalysisSummary } from '../types/api'

export default function DashboardPage() {
  const [summary, setSummary] = useState<AnalysisSummary | null>(null)
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const api = useApi()

  useEffect(() => {
    api.fetchSummary()
      .then(setSummary)
      .catch((err) => setError((err as Error).message))
  }, [api])

  return (
    <div className="mx-auto mt-12 max-w-6xl px-4 sm:px-6 lg:px-8">
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-slate-600">Overview of your email fraud analysis activity.</p>
        </div>
        <div className="flex gap-3">
          <Link to="/analysis" className="rounded-2xl bg-sky-600 px-5 py-3 text-white hover:bg-sky-700">
            Analyze email
          </Link>
          <button onClick={() => { localStorage.removeItem('auth_token'); navigate('/login') }} className="rounded-2xl border border-slate-200 px-5 py-3 text-slate-700 hover:bg-slate-100">
            Sign out
          </button>
        </div>
      </div>

      {error && <p className="mb-4 rounded-2xl bg-red-100 p-4 text-red-700">{error}</p>}

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <div className="rounded-3xl bg-white p-6 shadow-sm">
          <h2 className="text-sm text-slate-500">Total analyses</h2>
          <p className="mt-3 text-3xl font-semibold">{summary?.total_analyses ?? '—'}</p>
        </div>
        <div className="rounded-3xl bg-white p-6 shadow-sm">
          <h2 className="text-sm text-slate-500">Average fraud score</h2>
          <p className="mt-3 text-3xl font-semibold">{summary?.average_score.toFixed(1) ?? '—'}</p>
        </div>
        <div className="rounded-3xl bg-white p-6 shadow-sm">
          <h2 className="text-sm text-slate-500">Phishing rate</h2>
          <p className="mt-3 text-3xl font-semibold">{summary?.phishing_pct.toFixed(1) ?? '—'}%</p>
        </div>
        <div className="rounded-3xl bg-white p-6 shadow-sm">
          <h2 className="text-sm text-slate-500">Spam rate</h2>
          <p className="mt-3 text-3xl font-semibold">{summary?.spam_pct.toFixed(1) ?? '—'}%</p>
        </div>
      </div>

      <div className="mt-8 rounded-3xl bg-white p-6 shadow-sm">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold">Quick links</h2>
            <p className="text-slate-500">Upload or paste email content for immediate analysis.</p>
          </div>
          <Link to="/history" className="text-sky-600 hover:text-sky-700">View history</Link>
        </div>
      </div>
    </div>
  )
}

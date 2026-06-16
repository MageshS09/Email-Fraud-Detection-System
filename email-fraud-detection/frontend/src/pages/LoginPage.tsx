import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useApi } from '../hooks/useApi'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const api = useApi()

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    setError('')
    try {
      const response = await api.login(email, password)
      localStorage.setItem('auth_token', response.access_token)
      navigate('/')
    } catch (err) {
      setError((err as Error).message)
    }
  }

  return (
    <div className="mx-auto mt-20 max-w-md rounded-3xl bg-white p-8 shadow-xl">
      <h1 className="mb-6 text-3xl font-semibold">Email Fraud Detection</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <label className="block">
          <span className="text-sm font-medium">Email</span>
          <input
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            className="mt-1 w-full rounded-xl border px-4 py-3 text-slate-900 focus:outline-none focus:ring-2 focus:ring-sky-500"
            required
          />
        </label>
        <label className="block">
          <span className="text-sm font-medium">Password</span>
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            className="mt-1 w-full rounded-xl border px-4 py-3 text-slate-900 focus:outline-none focus:ring-2 focus:ring-sky-500"
            required
          />
        </label>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <button type="submit" className="w-full rounded-2xl bg-sky-600 px-4 py-3 text-white transition hover:bg-sky-700">
          Sign in
        </button>
      </form>
      <p className="mt-4 text-sm text-slate-600">
        New user? <Link to="/register" className="text-sky-600">Create an account</Link>
      </p>
    </div>
  )
}

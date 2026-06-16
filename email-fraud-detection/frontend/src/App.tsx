import { Routes, Route, Navigate } from 'react-router-dom'
import DashboardPage from './pages/DashboardPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import AnalysisPage from './pages/AnalysisPage'
import HistoryPage from './pages/HistoryPage'

function App() {
  const token = localStorage.getItem('auth_token')

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route
          path="/"
          element={token ? <DashboardPage /> : <Navigate to="/login" replace />}
        />
        <Route
          path="/analysis"
          element={token ? <AnalysisPage /> : <Navigate to="/login" replace />}
        />
        <Route
          path="/history"
          element={token ? <HistoryPage /> : <Navigate to="/login" replace />}
        />
      </Routes>
    </div>
  )
}

export default App

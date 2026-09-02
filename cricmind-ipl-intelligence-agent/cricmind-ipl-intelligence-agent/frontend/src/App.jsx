import { Routes, Route, NavLink } from 'react-router-dom'
import Dashboard from './pages/Dashboard.jsx'
import AiAnalyst from './pages/AiAnalyst.jsx'
import Teams from './pages/Teams.jsx'
import Predictions from './pages/Predictions.jsx'

function NavItem({ to, label }) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        `px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
          isActive ? 'bg-cricmind-accent text-white' : 'text-slate-300 hover:bg-slate-800'
        }`
      }
    >
      {label}
    </NavLink>
  )
}

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-slate-800 bg-cricmind-dark/80 backdrop-blur sticky top-0 z-10">
        <div className="max-w-6xl mx-auto flex items-center justify-between px-6 py-3">
          <div className="flex items-center gap-2">
            <span className="text-2xl">🏏</span>
            <span className="font-bold text-lg tracking-tight">CricMind</span>
            <span className="text-xs text-slate-400 hidden sm:inline">IPL Intelligence Agent</span>
          </div>
          <nav className="flex gap-2">
            <NavItem to="/" label="Dashboard" />
            <NavItem to="/analyst" label="AI Analyst" />
            <NavItem to="/teams" label="Teams" />
            <NavItem to="/predictions" label="Predictions" />
          </nav>
        </div>
      </header>

      <main className="flex-1 max-w-6xl mx-auto w-full px-6 py-8">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/analyst" element={<AiAnalyst />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/predictions" element={<Predictions />} />
        </Routes>
      </main>

      <footer className="border-t border-slate-800 py-4 text-center text-xs text-slate-500">
        CricMind — built with React, Spring Boot, Python/LangGraph & PostgreSQL/pgvector
      </footer>
    </div>
  )
}

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
          isActive ? 'bg-[#e8f0ff] text-[#1e5acb]' : 'text-[#647089] hover:bg-[#f1f4f9] hover:text-[#172033]'
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
      <header className="border-b border-[#e3e8f0] bg-white/90 backdrop-blur sticky top-0 z-10">
        <div className="max-w-6xl mx-auto flex items-center justify-between px-6 py-4">
          <div className="flex items-center gap-2">
            <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#172033] text-lg text-white">C</span>
            <span className="font-display font-bold text-lg tracking-tight text-[#172033]">CricMind</span>
            <span className="text-xs text-[#8a95a8] hidden sm:inline">IPL Intelligence Agent</span>
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

      <footer className="border-t border-[#e3e8f0] py-5 text-center text-xs text-[#8a95a8]">
        CricMind — built with React, Spring Boot, Python/LangGraph & PostgreSQL/pgvector
      </footer>
    </div>
  )
}

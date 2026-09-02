import { useEffect, useState } from 'react'
import { getTeams } from '../api/client'

export default function Teams() {
  const [teams, setTeams] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    getTeams().then(setTeams).catch(() => setError('Could not load teams from backend.'))
  }, [])

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Teams</h1>
      {error && <p className="text-amber-400 text-sm mb-4">{error}</p>}
      <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
        {teams.map((t) => (
          <div key={t.id} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <h3 className="font-semibold">{t.name}</h3>
            <p className="text-slate-400 text-sm">{t.shortCode} · {t.homeVenue}</p>
          </div>
        ))}
        {teams.length === 0 && !error && <p className="text-slate-500">Loading…</p>}
      </div>
    </div>
  )
}

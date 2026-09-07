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
      <p className="eyebrow mb-2">Competition directory</p>
      <h1 className="text-3xl font-bold mb-4">Teams</h1>
      {error && <p className="text-[#a36e13] text-sm mb-4">{error}</p>}
      <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
        {teams.map((t) => (
          <div key={t.id} className="surface p-4 hover:-translate-y-0.5 transition-transform">
            <h3 className="font-semibold">{t.name}</h3>
            <p className="text-[#647089] text-sm">{t.shortCode} · {t.homeVenue}</p>
          </div>
        ))}
        {teams.length === 0 && !error && <p className="text-[#8a95a8]">Loading...</p>}
      </div>
    </div>
  )
}

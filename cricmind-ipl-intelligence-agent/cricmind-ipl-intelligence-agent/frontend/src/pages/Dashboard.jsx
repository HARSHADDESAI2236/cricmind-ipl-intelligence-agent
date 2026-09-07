import { useEffect, useState } from 'react'
import { getStandings, getMatches } from '../api/client'

export default function Dashboard() {
  const [standings, setStandings] = useState([])
  const [matches, setMatches] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    Promise.all([getStandings(), getMatches()])
      .then(([s, m]) => {
        setStandings(s.standings || s)
        setMatches(m)
      })
      .catch(() => setError('Could not reach the backend API yet — start the backend + AI service to see live data.'))
  }, [])

  return (
    <div className="space-y-8">
      <section>
        <p className="eyebrow mb-2">Season overview</p>
        <h1 className="text-3xl font-bold mb-1 text-[#172033]">Dashboard</h1>
        <p className="text-[#647089] text-sm">Live standings, fixtures, and quick AI insights.</p>
      </section>

      {error && (
        <div className="bg-[#fff8e8] border border-[#f3d28a] text-[#8b6414] rounded-lg px-4 py-3 text-sm">
          {error}
        </div>
      )}

      <section className="grid md:grid-cols-2 gap-6">
        <div className="surface p-5">
          <div className="flex items-center justify-between mb-4"><h2 className="font-semibold">Points Table</h2><span className="text-xs font-semibold text-[#8a95a8]">IPL 2026</span></div>
          <table className="w-full text-sm">
            <thead className="text-[#8a95a8] text-left text-xs uppercase tracking-wider">
              <tr>
                <th className="pb-2">Team</th><th className="pb-2">P</th><th className="pb-2">W</th><th className="pb-2">L</th><th className="pb-2">Pts</th><th className="pb-2">NRR</th>
              </tr>
            </thead>
            <tbody>
              {standings.map((row) => (
                <tr key={row.team} className="border-t border-[#edf0f5]">
                  <td className="py-2 font-medium">{row.team}</td>
                  <td>{row.played}</td>
                  <td>{row.won}</td>
                  <td>{row.lost}</td>
                  <td>{row.points}</td>
                  <td>{row.nrr}</td>
                </tr>
              ))}
              {standings.length === 0 && !error && (
                <tr><td colSpan="6" className="py-4 text-[#8a95a8]">Loading...</td></tr>
              )}
            </tbody>
          </table>
        </div>

        <div className="surface p-5">
          <div className="flex items-center justify-between mb-4"><h2 className="font-semibold">Upcoming Matches</h2><span className="text-xs font-semibold text-[#1e5acb]">View schedule</span></div>
          <ul className="space-y-3 text-sm">
            {(matches.upcoming_matches || matches || []).map((m) => (
              <li key={m.id} className="flex justify-between border-b border-[#edf0f5] pb-3">
                <span>{m.team1} vs {m.team2}</span>
                <span className="text-[#8a95a8]">{m.date}</span>
              </li>
            ))}
            {(!matches.upcoming_matches && matches.length === undefined) && (
              <li className="text-[#8a95a8]">Loading...</li>
            )}
          </ul>
        </div>
      </section>
    </div>
  )
}

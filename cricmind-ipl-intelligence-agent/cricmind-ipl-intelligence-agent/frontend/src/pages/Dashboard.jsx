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
        <h1 className="text-2xl font-bold mb-1">Dashboard</h1>
        <p className="text-slate-400 text-sm">Live standings, fixtures, and quick AI insights.</p>
      </section>

      {error && (
        <div className="bg-amber-900/30 border border-amber-700 text-amber-300 rounded-lg px-4 py-3 text-sm">
          {error}
        </div>
      )}

      <section className="grid md:grid-cols-2 gap-6">
        <div className="bg-slate-900 rounded-xl border border-slate-800 p-5">
          <h2 className="font-semibold mb-3">Points Table</h2>
          <table className="w-full text-sm">
            <thead className="text-slate-400 text-left">
              <tr>
                <th className="pb-2">Team</th><th className="pb-2">P</th><th className="pb-2">W</th><th className="pb-2">L</th><th className="pb-2">Pts</th><th className="pb-2">NRR</th>
              </tr>
            </thead>
            <tbody>
              {standings.map((row) => (
                <tr key={row.team} className="border-t border-slate-800">
                  <td className="py-2 font-medium">{row.team}</td>
                  <td>{row.played}</td>
                  <td>{row.won}</td>
                  <td>{row.lost}</td>
                  <td>{row.points}</td>
                  <td>{row.nrr}</td>
                </tr>
              ))}
              {standings.length === 0 && !error && (
                <tr><td colSpan="6" className="py-4 text-slate-500">Loading…</td></tr>
              )}
            </tbody>
          </table>
        </div>

        <div className="bg-slate-900 rounded-xl border border-slate-800 p-5">
          <h2 className="font-semibold mb-3">Upcoming Matches</h2>
          <ul className="space-y-3 text-sm">
            {(matches.upcoming_matches || matches || []).map((m) => (
              <li key={m.id} className="flex justify-between border-b border-slate-800 pb-2">
                <span>{m.team1} vs {m.team2}</span>
                <span className="text-slate-400">{m.date}</span>
              </li>
            ))}
            {(!matches.upcoming_matches && matches.length === undefined) && (
              <li className="text-slate-500">Loading…</li>
            )}
          </ul>
        </div>
      </section>
    </div>
  )
}

import { useState } from 'react'
import { predictMatch } from '../api/client'

const TEAM_CODES = ['RCB', 'GT', 'MI', 'CSK', 'KKR']

export default function Predictions() {
  const [team1, setTeam1] = useState('RCB')
  const [team2, setTeam2] = useState('GT')
  const [venue, setVenue] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const run = async () => {
    setLoading(true)
    try {
      const res = await predictMatch({ team1, team2, venue })
      setResult(res)
    } catch {
      setResult({ error: 'Prediction service unavailable.' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <p className="eyebrow mb-2">Machine learning</p>
      <h1 className="text-3xl font-bold mb-1">Match Predictions</h1>
      <p className="text-[#647089] text-sm mb-6">Run the ML pipeline for a hypothetical or upcoming matchup.</p>

      <div className="surface p-5 max-w-xl space-y-4">
        <div className="flex gap-4">
          <select className="flex-1 bg-[#f7f9fc] border border-[#d8dfeb] rounded-lg px-3 py-2 text-sm" value={team1} onChange={(e) => setTeam1(e.target.value)}>
            {TEAM_CODES.map((t) => <option key={t}>{t}</option>)}
          </select>
          <span className="self-center text-[#8a95a8]">vs</span>
          <select className="flex-1 bg-[#f7f9fc] border border-[#d8dfeb] rounded-lg px-3 py-2 text-sm" value={team2} onChange={(e) => setTeam2(e.target.value)}>
            {TEAM_CODES.map((t) => <option key={t}>{t}</option>)}
          </select>
        </div>
        <input
          className="w-full bg-[#f7f9fc] border border-[#d8dfeb] rounded-lg px-3 py-2 text-sm"
          placeholder="Venue (optional)"
          value={venue}
          onChange={(e) => setVenue(e.target.value)}
        />
        <button onClick={run} disabled={loading} className="bg-[#f06b32] hover:bg-[#d95822] text-white px-5 py-2 rounded-lg text-sm font-semibold w-full">
          {loading ? 'Predicting…' : 'Predict Winner'}
        </button>
      </div>

      {result && !result.error && (
        <div className="mt-6 surface p-5 max-w-xl">
          <p className="text-lg font-semibold">
            Predicted winner: <span className="text-[#1e5acb]">{result.predicted_winner}</span> ({result.win_probability}%)
          </p>
          <p className="text-sm text-slate-400 mt-1">
            {result.team1}: {result.team1_win_probability}% · {result.team2}: {result.team2_win_probability}%
          </p>
          {result.key_factors?.length > 0 && (
            <ul className="mt-3 text-sm list-disc list-inside text-[#46536b]">
              {result.key_factors.map((f, i) => <li key={i}>{f}</li>)}
            </ul>
          )}
          <p className="mt-3 text-xs text-[#8a95a8]">{result.disclaimer}</p>
        </div>
      )}
      {result?.error && <p className="mt-4 text-[#a36e13] text-sm">{result.error}</p>}
    </div>
  )
}

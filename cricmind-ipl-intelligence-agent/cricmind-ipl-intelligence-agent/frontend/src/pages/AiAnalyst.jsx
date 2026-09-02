import { useState, useRef, useEffect } from 'react'
import { sendChatMessage } from '../api/client'

export default function AiAnalyst() {
  const [messages, setMessages] = useState([
    { role: 'agent', content: "Ask me anything about IPL teams, players, stats, or match predictions." },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const send = async () => {
    if (!input.trim() || loading) return
    const userMsg = { role: 'user', content: input }
    setMessages((m) => [...m, userMsg])
    setInput('')
    setLoading(true)
    try {
      const res = await sendChatMessage(userMsg.content)
      setMessages((m) => [...m, {
        role: 'agent',
        content: res.answer,
        toolsUsed: res.toolsUsed,
        confidence: res.confidence,
      }])
    } catch (e) {
      setMessages((m) => [...m, { role: 'agent', content: 'Sorry, I could not reach the AI service. Is it running?' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-[70vh]">
      <h1 className="text-2xl font-bold mb-4">AI Analyst</h1>
      <div className="flex-1 overflow-y-auto space-y-4 bg-slate-900 border border-slate-800 rounded-xl p-5">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-lg px-4 py-2 text-sm ${
              m.role === 'user' ? 'bg-cricmind-primary text-white' : 'bg-slate-800 text-slate-100'
            }`}>
              <p>{m.content}</p>
              {m.toolsUsed?.length > 0 && (
                <p className="mt-2 text-xs text-slate-400">
                  tools used: {m.toolsUsed.join(', ')} · confidence {(m.confidence * 100).toFixed(0)}%
                </p>
              )}
            </div>
          </div>
        ))}
        {loading && <p className="text-slate-500 text-sm">CricMind is thinking…</p>}
        <div ref={bottomRef} />
      </div>
      <div className="flex gap-2 mt-4">
        <input
          className="flex-1 bg-slate-900 border border-slate-800 rounded-lg px-4 py-2 text-sm outline-none focus:border-cricmind-accent"
          placeholder="e.g. Why is RCB likely to win against GT?"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && send()}
        />
        <button
          onClick={send}
          className="bg-cricmind-accent hover:opacity-90 text-white px-5 py-2 rounded-lg text-sm font-medium"
        >
          Send
        </button>
      </div>
    </div>
  )
}

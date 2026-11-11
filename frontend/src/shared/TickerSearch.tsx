import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

interface TickerSearchProps {
  large?: boolean
  autoFocus?: boolean
}

// Type a ticker, press Enter — works from anywhere.
function TickerSearch({ large = false, autoFocus = false }: TickerSearchProps) {
  const navigate = useNavigate()
  const [ticker, setTicker] = useState('')

  function submit(e: React.FormEvent) {
    e.preventDefault()
    const t = ticker.trim().toUpperCase()
    if (!t) return
    navigate(`/company/${t}`)
    setTicker('')
  }

  return (
    <form onSubmit={submit} className={large ? 'w-full max-w-md' : 'w-full'}>
      <input
        value={ticker}
        onChange={(e) => setTicker(e.target.value.toUpperCase().replace(/[^A-Z0-9.-]/g, ''))}
        placeholder={large ? 'Enter a ticker' : 'Ticker'}
        autoFocus={autoFocus}
        className={`w-full border border-secondary-ice bg-primary text-slate-800 placeholder:text-slate-400 focus:border-secondary focus:ring-2 focus:ring-secondary/40 focus:outline-none ${
          large ? 'rounded-2xl px-6 py-4 text-center text-2xl shadow-lg shadow-secondary/10' : 'rounded-lg px-3 py-1.5 text-sm'
        }`}
      />
    </form>
  )
}

export default TickerSearch

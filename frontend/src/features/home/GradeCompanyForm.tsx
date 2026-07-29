import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Button from '../../shared/Button'
import TextInput from '../../shared/TextInput'
import Select from '../../shared/Select'
import { defaultRange, isValidRange, yearOptions } from '../../constants/yearRange'

function GradeCompanyForm() {
  const navigate = useNavigate()
  const [ticker, setTicker] = useState('')
  const initial = defaultRange()
  const [start, setStart] = useState(initial.start)
  const [end, setEnd] = useState(initial.end)
  const years = yearOptions()
  const valid = ticker.trim().length > 0 && isValidRange(start, end)

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!valid) return
    navigate(`/company/${ticker.trim().toUpperCase()}?start=${start}&end=${end}`)
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="flex w-full max-w-xl flex-col gap-3 rounded-2xl border border-secondary-ice bg-white/70 p-6 shadow-lg shadow-secondary/20 backdrop-blur"
    >
      <div className="flex flex-col gap-3 sm:flex-row">
        <TextInput
          value={ticker}
          onChange={(value) => setTicker(value.toUpperCase())}
          placeholder="AAPL"
        />
        <div className="shrink-0">
          <Button type="submit" disabled={!valid}>
            Grade Company
          </Button>
        </div>
      </div>
      <div className="flex items-center gap-3">
        <Select value={String(start)} onChange={(v) => setStart(Number(v))} options={years.map((y) => ({ value: String(y), label: String(y) }))} />
        <span className="text-slate-400">to</span>
        <Select value={String(end)} onChange={(v) => setEnd(Number(v))} options={years.map((y) => ({ value: String(y), label: String(y) }))} />
      </div>
      {!isValidRange(start, end) && (
        <p className="text-xs text-rose-600">Year range must span at most 6 years, start ≤ end.</p>
      )}
    </form>
  )
}

export default GradeCompanyForm

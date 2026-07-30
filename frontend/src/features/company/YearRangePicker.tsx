import { useState } from 'react'
import Select from '../../shared/Select'
import { yearOptions, isValidRange } from '../../constants/yearRange'
import type { YearRange } from '../../constants/yearRange'

interface YearRangePickerProps {
  range: YearRange
  onChange: (range: YearRange) => void
}

function YearRangePicker({ range, onChange }: YearRangePickerProps) {
  const [start, setStart] = useState(range.start)
  const [end, setEnd] = useState(range.end)
  const years = yearOptions()
  const valid = isValidRange(start, end)

  function update(nextStart: number, nextEnd: number) {
    setStart(nextStart)
    setEnd(nextEnd)
    if (isValidRange(nextStart, nextEnd)) onChange({ start: nextStart, end: nextEnd })
  }

  return (
    <div className="flex flex-wrap items-end gap-3">
      <div>
        <label className="mb-1 block text-xs text-slate-500">From</label>
        <Select value={String(start)} onChange={(v) => update(Number(v), end)} options={years.map((y) => ({ value: String(y), label: String(y) }))} />
      </div>
      <div>
        <label className="mb-1 block text-xs text-slate-500">To</label>
        <Select value={String(end)} onChange={(v) => update(start, Number(v))} options={years.map((y) => ({ value: String(y), label: String(y) }))} />
      </div>
      {!valid && <p className="text-xs text-rose-600">Range must be 1–6 years, start ≤ end.</p>}
    </div>
  )
}

export default YearRangePicker

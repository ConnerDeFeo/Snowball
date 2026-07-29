import { useState } from 'react'
import Select from '../../shared/Select'
import Button from '../../shared/Button'
import { yearOptions, isValidRange } from '../../constants/yearRange'
import type { YearRange } from '../../constants/yearRange'

interface YearRangePickerProps {
  range: YearRange
  onApply: (range: YearRange) => void
}

function YearRangePicker({ range, onApply }: YearRangePickerProps) {
  const [start, setStart] = useState(range.start)
  const [end, setEnd] = useState(range.end)
  const years = yearOptions()
  const valid = isValidRange(start, end)

  return (
    <div className="flex flex-wrap items-end gap-3">
      <div>
        <label className="mb-1 block text-xs text-slate-500">From</label>
        <Select value={String(start)} onChange={(v) => setStart(Number(v))} options={years.map((y) => ({ value: String(y), label: String(y) }))} />
      </div>
      <div>
        <label className="mb-1 block text-xs text-slate-500">To</label>
        <Select value={String(end)} onChange={(v) => setEnd(Number(v))} options={years.map((y) => ({ value: String(y), label: String(y) }))} />
      </div>
      <Button variant="ghost" onClick={() => onApply({ start, end })} disabled={!valid}>
        Apply
      </Button>
      {!valid && <p className="text-xs text-rose-600">Range must be 1–6 years, start ≤ end.</p>}
    </div>
  )
}

export default YearRangePicker

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
  const options = yearOptions().map((y) => ({ value: String(y), label: String(y) }))
  const valid = isValidRange(start, end)

  function update(nextStart: number, nextEnd: number) {
    setStart(nextStart)
    setEnd(nextEnd)
    if (isValidRange(nextStart, nextEnd)) onChange({ start: nextStart, end: nextEnd })
  }

  return (
    <div className="flex items-center gap-1.5">
      <div className="w-20">
        <Select compact value={String(start)} onChange={(v) => update(Number(v), end)} options={options} />
      </div>
      <span className="text-slate-400">–</span>
      <div className="w-20">
        <Select compact value={String(end)} onChange={(v) => update(start, Number(v))} options={options} />
      </div>
      {!valid && <p className="ml-2 text-xs text-rose-600">1–6 years, start ≤ end</p>}
    </div>
  )
}

export default YearRangePicker

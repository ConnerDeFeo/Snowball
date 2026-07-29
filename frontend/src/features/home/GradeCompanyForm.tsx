import { useState } from 'react'
import Button from '../../shared/Button'
import TextInput from '../../shared/TextInput'

function GradeCompanyForm() {
  const [ticker, setTicker] = useState('')

  return (
    <form
      onSubmit={(e) => e.preventDefault()}
      className="flex w-full max-w-xl flex-col gap-3 rounded-2xl border border-secondary-ice bg-white/70 p-6 shadow-lg shadow-secondary/20 backdrop-blur sm:flex-row"
    >
      <TextInput
        value={ticker}
        onChange={(value) => setTicker(value.toUpperCase())}
        placeholder="AAPL"
      />
      <div className="shrink-0">
        <Button type="submit">Grade Company</Button>
      </div>
    </form>
  )
}

export default GradeCompanyForm

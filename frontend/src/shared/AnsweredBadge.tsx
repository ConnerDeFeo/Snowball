import { answeredClasses } from '../constants/evidenceStyles'

interface AnsweredBadgeProps {
  answered: number
  total: number
}

function AnsweredBadge({ answered, total }: AnsweredBadgeProps) {
  return (
    <span className={`inline-block rounded-full px-3 py-1 text-sm font-semibold ${answeredClasses(answered, total)}`}>
      {answered}/{total} answered
    </span>
  )
}

export default AnsweredBadge

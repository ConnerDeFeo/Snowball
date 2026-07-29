import { Link } from 'react-router-dom'
import Button from './Button'

function Header() {
  return (
    <header className="flex items-center justify-between border-b border-secondary-ice px-6 py-4">
      <Link to="/" className="flex items-center gap-2 text-xl font-bold text-slate-800">
        <span className="text-secondary-deep">❄</span>
        Snowball
      </Link>
      <Link to="/rubric">
        <Button variant="ghost">Edit Rubric</Button>
      </Link>
    </header>
  )
}

export default Header

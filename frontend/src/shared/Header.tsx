import Button from './Button'

function Header() {
  return (
    <header className="flex items-center justify-between border-b border-secondary-ice px-6 py-4">
      <div className="flex items-center gap-2 text-xl font-bold text-slate-800">
        <span className="text-secondary-deep">❄</span>
        Snowball
      </div>
      <Button variant="ghost">Edit Rubric</Button>
    </header>
  )
}

export default Header

interface ButtonProps {
  children: React.ReactNode
  variant?: 'primary' | 'ghost'
  type?: 'button' | 'submit'
  onClick?: () => void
}

const styles = {
  primary:
    'bg-secondary text-white shadow-md shadow-secondary/40 hover:bg-secondary-deep',
  ghost:
    'border border-secondary text-secondary-deep hover:bg-secondary-ice',
}

function Button({ children, variant = 'primary', type = 'button', onClick }: ButtonProps) {
  return (
    <button
      type={type}
      onClick={onClick}
      className={`cursor-pointer rounded-lg px-5 py-2.5 font-semibold transition-colors ${styles[variant]}`}
    >
      {children}
    </button>
  )
}

export default Button

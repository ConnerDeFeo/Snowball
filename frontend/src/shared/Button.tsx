interface ButtonProps {
  children: React.ReactNode
  variant?: 'primary' | 'ghost'
  type?: 'button' | 'submit'
  onClick?: () => void
  disabled?: boolean
}

const styles = {
  primary:
    'bg-secondary text-white shadow-md shadow-secondary/40 hover:bg-secondary-deep',
  ghost:
    'border border-secondary text-secondary-deep hover:bg-secondary-ice',
}

function Button({ children, variant = 'primary', type = 'button', onClick, disabled }: ButtonProps) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`cursor-pointer rounded-lg px-5 py-2.5 font-semibold transition-colors disabled:cursor-not-allowed disabled:opacity-50 ${styles[variant]}`}
    >
      {children}
    </button>
  )
}

export default Button

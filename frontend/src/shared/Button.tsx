interface ButtonProps {
  children: React.ReactNode
  variant?: 'primary' | 'ghost' | 'subtle'
  size?: 'md' | 'sm'
  type?: 'button' | 'submit'
  onClick?: () => void
  disabled?: boolean
  title?: string
}

const styles = {
  primary: 'bg-secondary text-white hover:bg-secondary-deep',
  ghost: 'border border-secondary text-secondary-deep hover:bg-secondary-ice',
  subtle: 'text-secondary-deep hover:bg-secondary-ice',
}

const sizes = {
  md: 'px-5 py-2.5',
  sm: 'px-3 py-1.5 text-sm',
}

function Button({ children, variant = 'primary', size = 'md', type = 'button', onClick, disabled, title }: ButtonProps) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      title={title}
      className={`cursor-pointer rounded-lg font-semibold transition-colors disabled:cursor-not-allowed disabled:opacity-50 ${sizes[size]} ${styles[variant]}`}
    >
      {children}
    </button>
  )
}

export default Button

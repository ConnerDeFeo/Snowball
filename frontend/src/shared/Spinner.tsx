interface SpinnerProps {
  className?: string
}

function Spinner({ className = 'h-4 w-4' }: SpinnerProps) {
  return (
    <span
      className={`inline-block animate-spin rounded-full border-2 border-secondary-ice border-t-secondary-deep ${className}`}
    />
  )
}

export default Spinner

interface CardProps {
  children: React.ReactNode
  className?: string
}

function Card({ children, className = '' }: CardProps) {
  return (
    <div
      className={`rounded-2xl border border-secondary-ice bg-white/70 p-6 shadow-lg shadow-secondary/20 backdrop-blur ${className}`}
    >
      {children}
    </div>
  )
}

export default Card

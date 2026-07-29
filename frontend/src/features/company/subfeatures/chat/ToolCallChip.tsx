import type { ToolCall } from '../../../../hooks/useChat'

function ToolCallChip({ tool, args }: ToolCall) {
  const detail = Object.values(args).filter(Boolean).join(' · ')
  return (
    <span className="inline-block rounded-full border border-secondary-ice bg-secondary-ice/50 px-2.5 py-1 text-xs text-slate-500">
      {tool}
      {detail ? ` · ${detail}` : ''}
    </span>
  )
}

export default ToolCallChip

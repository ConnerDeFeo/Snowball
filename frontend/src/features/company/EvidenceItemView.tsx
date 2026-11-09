import { statusClasses } from '../../constants/evidenceStyles'
import type { EvidenceItem } from '../../services/types/EvidenceTypes'

interface EvidenceItemViewProps {
  item: EvidenceItem
}

function EvidenceItemView({ item }: EvidenceItemViewProps) {
  return (
    <div className="rounded-lg bg-secondary-ice/30 p-3">
      <p className="text-sm font-semibold text-slate-800">
        {item.year}
        {item.quarter ? ` ${item.quarter}` : ''}
      </p>

      {item.findings.length === 0 && <p className="mt-1 text-sm text-slate-500">Nothing relevant found.</p>}

      <ul className="mt-1 flex flex-col gap-2">
        {item.findings.map((finding, i) => (
          <li key={i}>
            <div className="flex flex-wrap items-center gap-2 text-sm">
              <span className="font-medium text-slate-700">{finding.field}:</span>
              <span className="text-slate-600">{finding.value}</span>
              <span className={`rounded-full px-2 py-0.5 text-xs ${statusClasses(finding.status)}`}>
                {finding.status.replaceAll('_', ' ')}
              </span>
            </div>
            {finding.snippet && (
              <blockquote className="mt-1 border-l-2 border-secondary pl-3 text-sm italic text-slate-500">
                {finding.snippet}
              </blockquote>
            )}
          </li>
        ))}
      </ul>

      {item.notable_anomalies && (
        <p className="mt-2 text-xs text-amber-700">Anomaly: {item.notable_anomalies}</p>
      )}
    </div>
  )
}

export default EvidenceItemView

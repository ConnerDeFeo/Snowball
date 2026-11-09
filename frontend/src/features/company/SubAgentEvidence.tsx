import EvidenceItemView from './EvidenceItemView'
import { displaySection } from '../../constants/categories'
import type { Section } from '../../enums/Sections'
import type { EvidenceSubAgent } from '../../services/types/EvidenceTypes'

interface SubAgentEvidenceProps {
  subAgent: EvidenceSubAgent
}

function SubAgentEvidence({ subAgent }: SubAgentEvidenceProps) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
        {subAgent.form} · {displaySection(subAgent.section as Section)}
      </p>
      {subAgent.evidence.length === 0 ? (
        <p className="mt-2 text-sm text-slate-500">Not run yet.</p>
      ) : (
        <div className="mt-2 flex flex-col gap-3">
          {subAgent.evidence.map((item) => (
            <EvidenceItemView key={`${item.year}-${item.quarter}`} item={item} />
          ))}
        </div>
      )}
    </div>
  )
}

export default SubAgentEvidence

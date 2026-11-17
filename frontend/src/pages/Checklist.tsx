import AppShell from '../shared/layout/AppShell';
import EditorControls from '../features/sidebar/EditorControls';
import ChecklistEditor from '../features/checklist/ChecklistEditor';

// Standalone editor, for when no company is open (e.g. coming from Home).
function Checklist() {
  return (
    <AppShell controls={<EditorControls />}>
      <ChecklistEditor />
    </AppShell>
  )
}

export default Checklist

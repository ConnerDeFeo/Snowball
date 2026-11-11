import Markdown from '../../../../shared/Markdown'
import { useSmoothText } from '../../../../hooks/useSmoothText'

interface StreamingTextProps {
  text: string
  streaming: boolean
}

function StreamingText({ text, streaming }: StreamingTextProps) {
  return <Markdown>{useSmoothText(text, streaming)}</Markdown>
}

export default StreamingText

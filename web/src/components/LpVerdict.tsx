import { AlertTriangleIcon, CheckCircle2Icon, InfoIcon, ScaleIcon } from 'lucide-react'

import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import type { ConclusionTone, Verdict } from '@/lib/lpConclusion'
import { cn } from '@/lib/utils'

const TONE: Record<ConclusionTone, { icon: typeof InfoIcon; className: string }> = {
  tie: { icon: ScaleIcon, className: 'border-brand/40 bg-brand/5' },
  good: { icon: CheckCircle2Icon, className: 'border-brand/40 bg-brand/5' },
  bad: { icon: AlertTriangleIcon, className: 'border-warning/40 bg-warning/10' },
  neutral: { icon: InfoIcon, className: '' }
}

/**
 * Avisos e conclusão curta de uma comparação do LP com o RuFaS, para o topo dos resultados.
 * Os avisos dizem quando o resultado diz pouco ou quando algo ficou fora; a conclusão resume o que a comparação mostrou.
 */
export default function LpVerdict({ verdict, className }: { verdict: Verdict; className?: string }) {
  const { conclusion, notices } = verdict
  const tone = conclusion ? TONE[conclusion.tone] : null

  if (!conclusion && notices.length === 0) return null

  return (
    <div className={cn('space-y-3', className)}>
      {notices.length > 0 && (
        <Alert className='border-warning/40 bg-warning/10'>
          <AlertTriangleIcon />
          <AlertTitle>{notices.length > 1 ? 'Avisos' : 'Aviso'}</AlertTitle>
          <AlertDescription>
            <ul className={notices.length > 1 ? 'list-disc space-y-1 pl-4' : undefined}>
              {notices.map(text => (
                <li key={text} className={notices.length > 1 ? undefined : 'list-none'}>
                  {text}
                </li>
              ))}
            </ul>
          </AlertDescription>
        </Alert>
      )}
      {conclusion && tone && (
        <Alert className={tone.className} role='status'>
          <tone.icon />
          <AlertTitle>Conclusão: {conclusion.title}</AlertTitle>
          <AlertDescription>{conclusion.text}</AlertDescription>
        </Alert>
      )}
    </div>
  )
}

import { AlertTriangleIcon, CheckCircle2Icon, MinusCircleIcon, XCircleIcon } from 'lucide-react'

import { Badge } from '@/components/ui/badge'
import { cn } from '@/lib/utils'
import type { ConstraintStatus, ModuleDietResult } from '@/lib/types'

// O estado sempre aparece em texto e em ícone: a cor sozinha não basta (FSD, B.2).
const CONSTRAINT: Record<ConstraintStatus, { label: string; icon: typeof CheckCircle2Icon; className?: string }> = {
  ok: { label: 'Atende', icon: CheckCircle2Icon },
  no_limite: { label: 'No limite', icon: AlertTriangleIcon, className: 'border-warning/50 bg-warning/10 text-foreground' },
  violada: { label: 'Violada', icon: XCircleIcon, className: 'bg-destructive/10 text-destructive' },
  indisponivel: { label: 'Indisponível', icon: MinusCircleIcon, className: 'text-muted-foreground' }
}

export function ConstraintBadge({ status }: { status: ConstraintStatus }) {
  const { label, icon: Icon, className } = CONSTRAINT[status]

  return (
    <Badge variant={status === 'ok' ? 'secondary' : 'outline'} className={cn(className)}>
      <Icon aria-hidden /> {label}
    </Badge>
  )
}

export type DietState = 'viavel' | 'inviavel' | 'incompleta'

/** Viável, inviável ou incompleta (alguma restrição sem dados, como a energia do NASEM sem metano e N urinário). */
export function dietState(diet: ModuleDietResult): DietState {
  if (!diet.feasible) return 'inviavel'

  return diet.incomplete ? 'incompleta' : 'viavel'
}

const DIET: Record<DietState, { label: string; icon: typeof CheckCircle2Icon; className?: string }> = {
  viavel: { label: 'Viável', icon: CheckCircle2Icon },
  inviavel: { label: 'Inviável', icon: XCircleIcon, className: 'bg-destructive/10 text-destructive' },
  incompleta: {
    label: 'Viável, incompleta',
    icon: AlertTriangleIcon,
    className: 'border-warning/50 bg-warning/10 text-foreground'
  }
}

export function DietBadge({ diet }: { diet: ModuleDietResult }) {
  const state = dietState(diet)
  const { label, icon: Icon, className } = DIET[state]

  return (
    <Badge variant={state === 'viavel' ? 'secondary' : 'outline'} className={cn(className)}>
      <Icon aria-hidden /> {label}
    </Badge>
  )
}

import { AlertTriangleIcon, CheckCircle2Icon, XCircleIcon } from 'lucide-react'

import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { cn } from '@/lib/utils'
import type { CheckStatus, RationCheck } from '@/lib/types'

// O estado sempre aparece em texto e em ícone: a cor sozinha não basta (FSD, A.4.1).
const STATUS: Record<CheckStatus, { label: string; icon: typeof CheckCircle2Icon; className?: string }> = {
  ok: { label: 'Ok', icon: CheckCircle2Icon },
  warn: { label: 'Atenção', icon: AlertTriangleIcon, className: 'border-warning/50 bg-warning/10 text-foreground' },
  alert: { label: 'Alerta', icon: XCircleIcon, className: 'bg-destructive/10 text-destructive' }
}

function StatusBadge({ status }: { status: CheckStatus }) {
  const { label, icon: Icon, className } = STATUS[status]

  return (
    <Badge variant={status === 'ok' ? 'secondary' : 'outline'} className={cn(className)}>
      <Icon aria-hidden /> {label}
    </Badge>
  )
}

const plural = (n: number, one: string, many: string) => `${n} ${n === 1 ? one : many}`

/** Resumo do título: "5 verificações: 1 em alerta, 1 em atenção, 3 ok". */
export function checksSummary(checks: RationCheck[]) {
  const count = (status: CheckStatus) => checks.filter(c => c.status === status).length

  return `${plural(checks.length, 'verificação', 'verificações')}: ${count('alert')} em alerta, ${count('warn')} em atenção, ${count('ok')} ok`
}

/** Aviso no topo dos resultados quando há verificação em alerta ou em atenção. */
export function ChecksAlert({ checks }: { checks: RationCheck[] }) {
  const alerts = checks.filter(c => c.status === 'alert').length
  const warns = checks.filter(c => c.status === 'warn').length

  if (alerts === 0 && warns === 0) return null

  return (
    <Alert variant={alerts > 0 ? 'destructive' : 'default'}>
      <AlertTriangleIcon />
      <AlertTitle>
        {alerts > 0
          ? `A ração tem ${plural(alerts, 'verificação', 'verificações')} em alerta.`
          : `A ração tem ${plural(warns, 'verificação', 'verificações')} em atenção.`}
      </AlertTitle>
      <AlertDescription>Veja o cartão Verificações. Elas só informam: não alteram a margem nem o custo.</AlertDescription>
    </Alert>
  )
}

export default function ChecksCard({ checks }: { checks: RationCheck[] }) {
  const table51 = checks.find(c => c.id === 'V3')

  return (
    <Card>
      <CardHeader>
        <CardTitle>Verificações</CardTitle>
        <CardDescription>
          {checksSummary(checks)}. A ração obtida é conferida contra o que o NRC e o NASEM consideram plausível; os limiares
          ainda estão em avaliação com o professor.
        </CardDescription>
      </CardHeader>
      <CardContent className='space-y-3'>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className='w-32'>Estado</TableHead>
              <TableHead className='min-w-48'>Verificação</TableHead>
              <TableHead className='min-w-56'>Valor obtido</TableHead>
              <TableHead className='min-w-56'>Limite</TableHead>
              <TableHead className='min-w-64'>Dica</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {checks.map(check => (
              <TableRow key={check.id}>
                <TableCell>
                  <StatusBadge status={check.status} />
                </TableCell>
                <TableCell className='text-sm leading-snug'>
                  <span className='text-muted-foreground mr-1.5 text-xs'>{check.id}</span>
                  {check.label}
                </TableCell>
                <TableCell className='text-sm tabular-nums'>{check.value}</TableCell>
                <TableCell className='text-muted-foreground text-sm'>{check.limit}</TableCell>
                <TableCell className='text-muted-foreground text-xs'>{check.detail}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        {table51 && (
          <p className='text-muted-foreground text-xs'>
            V3 segue a Tabela 5-1 do NASEM (p. 70) e vale para dieta em TMR, com forragem de tamanho de partícula adequado e
            milho moído seco como fonte predominante de amido.
          </p>
        )}
      </CardContent>
    </Card>
  )
}

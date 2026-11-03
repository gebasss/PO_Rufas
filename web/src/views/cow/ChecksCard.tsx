import { AlertTriangleIcon, CheckCircle2Icon, XCircleIcon } from 'lucide-react'

import { Bullet, type BulletBand } from '@/components/charts'
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

/** Escala e faixas (ok, atenção, alerta) de cada verificação que tem um número só; V5 e as demais ficam sem barra. */
const BULLETS: Record<string, { min: number; max: number; bands: BulletBand[]; pick: (metrics: Record<string, number>) => number | undefined }> = {
  V1: { min: -10, max: 40, bands: [{ to: 12, tone: 'ok' }, { to: 24, tone: 'warn' }, { to: 40, tone: 'alert' }], pick: m => m.mean_excess_pct },
  V2: {
    min: 20,
    max: 50,
    bands: [{ to: 25, tone: 'alert' }, { to: 25.5, tone: 'warn' }, { to: 44.5, tone: 'ok' }, { to: 45, tone: 'warn' }, { to: 50, tone: 'alert' }],
    pick: m => m.ndf
  },
  V3: { min: 10, max: 30, bands: [{ to: 15, tone: 'alert' }, { to: 19, tone: 'warn' }, { to: 30, tone: 'ok' }], pick: m => m.forage_ndf },
  V4: { min: 0, max: 10, bands: [{ to: 5, tone: 'ok' }, { to: 7, tone: 'warn' }, { to: 10, tone: 'alert' }], pick: m => m.fat }
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
                <TableCell className='min-w-56 text-sm leading-snug whitespace-normal'>
                  <span className='text-muted-foreground mr-1.5 text-xs'>{check.id}</span>
                  {check.label}
                  {(() => {
                    const bullet = BULLETS[check.id]
                    const value = bullet?.pick(check.metrics)

                    return bullet && value !== undefined ? (
                      <div className='mt-2.5 mr-2'>
                        <Bullet value={value} min={bullet.min} max={bullet.max} bands={bullet.bands} />
                      </div>
                    ) : null
                  })()}
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

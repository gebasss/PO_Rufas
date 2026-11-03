'use client'

import { useMemo } from 'react'

import { AlertTriangleIcon, CheckCircle2Icon, DownloadIcon, ScaleIcon, XCircleIcon } from 'lucide-react'

import { KpiCard, NumberInput } from '@/components/shared'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { nf, signedPct } from '@/lib/format'
import { cn } from '@/lib/utils'
import type { ComparisonDiet, ComparisonProbe, ComparisonRow, ModuleComparison } from '@/lib/types'

import { ConstraintBadge } from './StatusBadge'

const digits = (value: number) => (Math.abs(value) < 1 ? 3 : 2)
const fmt = (value: number | null | undefined) => (value == null ? '—' : nf(value, digits(value)))

/** Escala 0,95 → "−5%": o rótulo da coluna de erro daquela sondagem. */
const scaleLabel = (scale: number) => `${scale < 1 ? '−' : '+'}${nf(Math.abs(scale - 1) * 100, 0)}%`

function Verdict({ ok, yes, no }: { ok: boolean; yes: string; no: string }) {
  return ok ? (
    <Badge variant='secondary'>
      <CheckCircle2Icon aria-hidden /> {yes}
    </Badge>
  ) : (
    <Badge variant='outline' className='border-warning/50 bg-warning/10 text-foreground'>
      <AlertTriangleIcon aria-hidden /> {no}
    </Badge>
  )
}

const probeAt = (probes: ComparisonProbe[] | undefined, scale: number) => probes?.find(p => p.scale === scale)

function downloadCsv(report: ModuleComparison) {
  // BOM para o Excel reconhecer os acentos.
  const url = URL.createObjectURL(new Blob(['﻿', report.csv], { type: 'text/csv;charset=utf-8' }))
  const link = document.createElement('a')

  link.href = url
  link.download = 'comparacao-linear-rufas.csv'
  link.click()
  URL.revokeObjectURL(url)
}

function ComparisonTable({ diet, scales, tolerance }: { diet: ComparisonDiet; scales: number[]; tolerance: number }) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead className='min-w-56'>Restrição</TableHead>
          <TableHead className='text-right'>Exigência</TableHead>
          <TableHead className='text-right'>Oferta linear</TableHead>
          <TableHead className='text-right'>Oferta no RuFaS</TableHead>
          <TableHead className='text-right'>Folga linear</TableHead>
          <TableHead className='text-right'>Folga no RuFaS</TableHead>
          <TableHead className='text-right'>Erro no ponto</TableHead>
          {scales.map(scale => (
            <TableHead key={scale} className='text-right'>
              Erro a {scaleLabel(scale)}
            </TableHead>
          ))}
          <TableHead className='text-right'>Maior erro</TableHead>
          <TableHead>Tolerância ({nf(tolerance, 1)}%)</TableHead>
          <TableHead>Estado (RuFaS)</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {diet.constraints.map((row: ComparisonRow) => {
          const unavailable = row.status_linear === 'indisponivel'

          return (
            <TableRow key={row.id}>
              <TableCell>
                <span className='block text-sm leading-snug'>{row.label}</span>
                <span className='text-muted-foreground block text-xs'>
                  {row.unit} · classe {row.kind}
                </span>
                {row.note && <span className='text-muted-foreground mt-0.5 block text-xs'>{row.note}</span>}
              </TableCell>
              <TableCell className='text-right tabular-nums'>{fmt(row.requirement)}</TableCell>
              <TableCell className='text-right tabular-nums'>{fmt(row.supply_linear)}</TableCell>
              <TableCell className='text-right tabular-nums'>{fmt(row.supply_original)}</TableCell>
              <TableCell className='text-right tabular-nums'>{fmt(row.slack_linear)}</TableCell>
              <TableCell className='text-right tabular-nums'>{fmt(row.slack_original)}</TableCell>
              <TableCell className='text-right tabular-nums'>{signedPct(row.point_error_pct)}</TableCell>
              {scales.map(scale => (
                <TableCell key={scale} className='text-right tabular-nums'>
                  {signedPct(probeAt(row.probes, scale)?.error_pct)}
                </TableCell>
              ))}
              <TableCell
                className={cn('text-right tabular-nums', row.within_tolerance === false && 'text-warning-text font-medium')}
              >
                {row.max_error_pct == null ? '—' : `${nf(row.max_error_pct, 2)}%`}
              </TableCell>
              <TableCell>
                {unavailable ? '—' : <Verdict ok={row.within_tolerance === true} yes='Dentro' no='Fora' />}
              </TableCell>
              <TableCell>
                {row.status_original ? <ConstraintBadge status={row.status_original} /> : <ConstraintBadge status='indisponivel' />}
              </TableCell>
            </TableRow>
          )
        })}
      </TableBody>
    </Table>
  )
}

interface Props {
  report: ModuleComparison | null
  /** A comparação mostrada não corresponde mais às entradas ou à tolerância atuais. */
  stale: boolean
  running: boolean
  error: string | null
  blockers: string[]
  tolerance: number
  selected: string | null
  onTolerance: (value: number) => void
  onSelect: (name: string) => void
  onCompare: () => void
}

export default function CompareCard({
  report,
  stale,
  running,
  error,
  blockers,
  tolerance,
  selected,
  onTolerance,
  onSelect,
  onCompare
}: Props) {
  const detail = useMemo(
    () => report?.diets.find(d => d.name === selected) ?? report?.diets[0] ?? null,
    [report, selected]
  )
  const invalidTolerance = !Number.isFinite(tolerance) || tolerance < 0

  return (
    <Card>
      <CardHeader>
        <CardTitle>Comparação com o RuFaS</CardTitle>
        <CardDescription>
          Para a mesma vaca e a mesma dieta, a oferta e a folga de cada restrição do modelo linear são conferidas com as
          funções originais do RuFaS: no ponto da dieta (onde devem coincidir) e com as quantidades de −5% a +5%. O erro é
          medido em % da oferta do RuFaS.
        </CardDescription>
      </CardHeader>
      <CardContent className='space-y-6'>
        <div className='space-y-2'>
          <div className='flex flex-wrap items-end gap-3'>
            <div className='flex flex-col justify-end gap-1.5'>
              <Label htmlFor='compare-tolerance'>Tolerância do erro (%)</Label>
              <NumberInput id='compare-tolerance' className='w-32' step={0.1} min={0} value={tolerance} onChange={onTolerance} />
            </div>
            <Button onClick={onCompare} disabled={running || blockers.length > 0 || invalidTolerance}>
              <ScaleIcon /> {running ? 'Comparando…' : 'Comparar com o RuFaS'}
            </Button>
            {report && (
              <Button variant='outline' onClick={() => downloadCsv(report)}>
                <DownloadIcon /> Baixar CSV
              </Button>
            )}
          </div>
          {invalidTolerance && <p className='text-muted-foreground text-sm'>Informe uma tolerância maior ou igual a zero.</p>}
          {report && stale && (
            <p className='text-muted-foreground text-sm' role='status'>
              As entradas ou a tolerância mudaram desde a última comparação. Clique em Comparar com o RuFaS para atualizar.
            </p>
          )}
        </div>

        {error && (
          <Alert variant='destructive'>
            <AlertTriangleIcon />
            <AlertTitle>Não foi possível comparar</AlertTitle>
            <AlertDescription>{error.split('\n')[0]}</AlertDescription>
          </Alert>
        )}

        {report && detail && (
          <div className={cn('space-y-6 transition-opacity', (running || stale) && 'opacity-60')}>
            <div className='grid grid-cols-2 gap-3 lg:grid-cols-4'>
              <KpiCard
                label='Maior erro'
                value={`${nf(report.summary.max_error_pct, 2)}%`}
                hint={report.summary.worst ? `${report.summary.worst.diet}: ${report.summary.worst.label}` : undefined}
              />
              <KpiCard
                label='Restrições acima da tolerância'
                value={`${report.summary.n_above_tolerance} de ${report.summary.n_compared}`}
                hint={`em ${report.summary.n_diets_above_tolerance} de ${report.summary.n_diets} dietas`}
              />
              <KpiCard
                label='Igualdade no ponto'
                value={report.summary.identity_ok ? 'Confere' : 'Diverge'}
                hint='oferta linear = oferta do RuFaS na dieta'
              />
              <KpiCard
                label='Mesmo estado a ±5%'
                value={report.summary.same_state_in_probes ? 'Confere' : 'Diverge'}
                hint='viável ou violada, nos dois modelos'
              />
            </div>

            {report.warnings.length > 0 && (
              <Alert>
                <AlertTriangleIcon />
                <AlertTitle>Avisos</AlertTitle>
                <AlertDescription>
                  <ul className='list-disc space-y-1 pl-4'>
                    {report.warnings.map(warning => (
                      <li key={warning}>{warning}</li>
                    ))}
                  </ul>
                </AlertDescription>
              </Alert>
            )}

            <div className='space-y-2'>
              <h3 className='text-muted-foreground text-xs font-medium tracking-wider uppercase'>Erro por dieta</h3>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Dieta</TableHead>
                    <TableHead className='text-right'>Maior erro</TableHead>
                    <TableHead>Restrição de maior erro</TableHead>
                    <TableHead className='text-right'>Acima da tolerância</TableHead>
                    <TableHead>Igualdade no ponto</TableHead>
                    <TableHead>Tolerância</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {report.diets.map(diet => (
                    <TableRow key={diet.name} data-state={diet.name === detail.name ? 'selected' : undefined}>
                      <TableCell>
                        <button
                          type='button'
                          aria-pressed={diet.name === detail.name}
                          className='focus-visible:ring-ring/50 rounded text-left font-medium underline-offset-4 outline-none hover:underline focus-visible:ring-3'
                          onClick={() => onSelect(diet.name)}
                        >
                          {diet.name}
                        </button>
                      </TableCell>
                      <TableCell className='text-right tabular-nums'>{nf(diet.max_error_pct, 2)}%</TableCell>
                      <TableCell className='text-muted-foreground text-xs'>{diet.worst_constraint?.label ?? '—'}</TableCell>
                      <TableCell className='text-right tabular-nums'>
                        {diet.n_above_tolerance} de {diet.n_compared}
                      </TableCell>
                      <TableCell>
                        {diet.identity_ok ? (
                          <Badge variant='secondary'>
                            <CheckCircle2Icon aria-hidden /> Confere
                          </Badge>
                        ) : (
                          <Badge variant='outline' className='bg-destructive/10 text-destructive'>
                            <XCircleIcon aria-hidden /> Diverge
                          </Badge>
                        )}
                      </TableCell>
                      <TableCell>
                        <Verdict ok={diet.within_tolerance} yes='Dentro' no='Fora' />
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>

            <div className='space-y-3'>
              <h3 className='text-muted-foreground text-xs font-medium tracking-wider uppercase'>
                Detalhe por restrição: {detail.name}
              </h3>
              <ComparisonTable diet={detail} scales={report.scales} tolerance={report.tolerance_pct} />
              <p className='text-muted-foreground text-xs'>
                <strong>Erro</strong>: (oferta linear − oferta do RuFaS) / oferta do RuFaS, com sinal. As classes L e E são
                exatas: o erro é 0 e não há sondagem. Na classe A os coeficientes ficam congelados na dieta e as quantidades
                são escaladas. <strong>Estado (RuFaS)</strong>: situação pela folga calculada com as funções originais. A
                tolerância de 1% ainda está em avaliação com o professor.
              </p>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

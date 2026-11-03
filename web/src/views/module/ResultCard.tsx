'use client'

import { useMemo } from 'react'

import { AlertTriangleIcon, CheckCircle2Icon, PlayIcon } from 'lucide-react'

import { KpiCard } from '@/components/shared'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { nf, signedPct, usd } from '@/lib/format'
import { cn } from '@/lib/utils'
import type { ModuleConstraint, ModuleDietResult, ModuleEvaluation } from '@/lib/types'

import { ConstraintBadge, DietBadge } from './StatusBadge'

/** Acima disso o erro de linearização é destacado (critério do FSD B.9-2, ainda em avaliação com o professor). */
const ERROR_ALERT_PCT = 1

const CLASS_HINT: Record<string, string> = {
  L: 'Exata: a oferta é linear nas quantidades.',
  E: 'Razão (FDN, gordura): exata na forma Σ(aᵢ−c)xᵢ.',
  A: 'Aproximada: coeficientes congelados na dieta avaliada.'
}

const digits = (value: number) => (Math.abs(value) < 1 ? 3 : 2)
const fmt = (value: number | null | undefined) => (value == null ? '—' : nf(value, digits(value)))

interface Props {
  result: ModuleEvaluation | null
  /** O resultado mostrado não corresponde mais às entradas atuais. */
  stale: boolean
  evaluating: boolean
  error: string | null
  blockers: string[]
  selected: string | null
  /** Custo da dieta ótima (LP), quando calculada para as entradas atuais: vira a referência final do ranking. */
  optimalCost: number | null
  onSelect: (name: string) => void
  onEvaluate: () => void
}

function Requirement({ row }: { row: ModuleConstraint }) {
  if (row.requirement === null) return <>—</>

  return (
    <>
      <span aria-hidden className='text-muted-foreground'>
        {row.sense === 'ge' ? '≥' : '≤'}{' '}
      </span>
      <span className='sr-only'>{row.sense === 'ge' ? 'no mínimo ' : 'no máximo '}</span>
      {fmt(row.requirement)}
    </>
  )
}

export function ConstraintTable({ diet }: { diet: ModuleDietResult }) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead className='min-w-56'>Restrição</TableHead>
          <TableHead className='text-right'>Exigência</TableHead>
          <TableHead className='text-right'>Oferta linear</TableHead>
          <TableHead className='text-right'>Oferta no RuFaS</TableHead>
          <TableHead className='text-right'>Erro</TableHead>
          <TableHead className='text-right'>Folga</TableHead>
          <TableHead>Estado</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {diet.constraints.map(row => {
          const bigError = row.error_pct != null && row.error_pct > ERROR_ALERT_PCT

          return (
            <TableRow key={row.id}>
              <TableCell>
                <span className='block text-sm leading-snug'>{row.label}</span>
                <span className='text-muted-foreground block text-xs'>
                  {row.unit} ·{' '}
                  <abbr title={CLASS_HINT[row.kind]} className='underline decoration-dotted'>
                    classe {row.kind}
                  </abbr>
                </span>
                {row.note && <span className='text-muted-foreground mt-0.5 block text-xs'>{row.note}</span>}
              </TableCell>
              <TableCell className='text-right tabular-nums'>
                <Requirement row={row} />
              </TableCell>
              <TableCell className='text-right tabular-nums'>{fmt(row.supply_linear)}</TableCell>
              <TableCell className='text-right tabular-nums'>{fmt(row.supply_nonlinear)}</TableCell>
              <TableCell
                className={cn('text-right tabular-nums', bigError && 'text-warning-text font-medium')}
                title={bigError ? `Acima de ${ERROR_ALERT_PCT}% da oferta original` : undefined}
              >
                {row.error_pct == null ? '—' : `${nf(row.error_pct, 2)}%`}
                {bigError && <span className='sr-only'> (acima de {ERROR_ALERT_PCT}%)</span>}
              </TableCell>
              <TableCell className='text-right tabular-nums'>{fmt(row.slack)}</TableCell>
              <TableCell>
                <ConstraintBadge status={row.status} />
              </TableCell>
            </TableRow>
          )
        })}
      </TableBody>
    </Table>
  )
}

export default function ResultCard({
  result,
  stale,
  evaluating,
  error,
  blockers,
  selected,
  optimalCost,
  onSelect,
  onEvaluate
}: Props) {
  const ranked = useMemo(
    // O back-end ordena da menos para a mais recomendada; na tela a posição 1 é a mais recomendada.
    () => (result ? [...result.ranking].reverse().map(name => result.diets.find(d => d.name === name)!) : []),
    [result]
  )
  const detail = ranked.find(d => d.name === selected) ?? ranked[0] ?? null
  const warnings = result ? [...new Set([...result.requirement_warnings, ...result.warnings])] : []
  const labelOf = (diet: ModuleDietResult, id: string) => diet.constraints.find(c => c.id === id)?.label ?? id

  return (
    <Card>
      <CardHeader>
        <CardTitle>Resultado</CardTitle>
        <CardDescription>
          Cada dieta é verificada contra as exigências da vaca e ordenada: as viáveis do menor para o maior custo. A
          “melhor entre as informadas” não é a dieta ótima; a ótima é a fase seguinte do projeto.
        </CardDescription>
      </CardHeader>
      <CardContent className='space-y-6'>
        <div className='space-y-2'>
          <Button onClick={onEvaluate} disabled={evaluating || blockers.length > 0}>
            <PlayIcon /> {evaluating ? 'Avaliando…' : 'Avaliar dietas'}
          </Button>
          {blockers.length > 0 && (
            <ul className='text-muted-foreground list-disc space-y-0.5 pl-4 text-sm'>
              {blockers.map(blocker => (
                <li key={blocker}>{blocker}</li>
              ))}
            </ul>
          )}
          {stale && blockers.length === 0 && (
            <p className='text-muted-foreground text-sm' role='status'>
              As entradas mudaram desde a última avaliação. Clique em Avaliar dietas para atualizar o resultado.
            </p>
          )}
        </div>

        {error && (
          <Alert variant='destructive'>
            <AlertTriangleIcon />
            <AlertTitle>Não foi possível avaliar</AlertTitle>
            <AlertDescription>{error.split('\n')[0]}</AlertDescription>
          </Alert>
        )}

        {!result ? (
          !error && (
            <p className='text-muted-foreground text-sm'>
              Informe a vaca, monte as dietas e clique em Avaliar dietas.
            </p>
          )
        ) : (
          <div className={cn('space-y-6 transition-opacity', (evaluating || stale) && 'opacity-60')}>
            {warnings.length > 0 && (
              <Alert>
                <AlertTriangleIcon />
                <AlertTitle>Avisos</AlertTitle>
                <AlertDescription>
                  <ul className='list-disc space-y-1 pl-4'>
                    {warnings.map(warning => (
                      <li key={warning}>{warning}</li>
                    ))}
                  </ul>
                </AlertDescription>
              </Alert>
            )}

            <div className='space-y-2'>
              <h3 className='text-muted-foreground text-xs font-medium tracking-wider uppercase'>Ranking</h3>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className='w-16'>Posição</TableHead>
                    <TableHead>Dieta</TableHead>
                    <TableHead>Estado</TableHead>
                    <TableHead className='text-right'>Custo (US$/dia)</TableHead>
                    <TableHead className='text-right'>Custo (US$/kg MS)</TableHead>
                    {optimalCost !== null && (
                      <TableHead className='text-right' title='(custo da dieta − custo da dieta ótima) / custo da dieta ótima'>
                        Desvio do ótimo
                      </TableHead>
                    )}
                    <TableHead className='text-right' title='Soma das faltas normalizadas das restrições violadas'>
                      Violação
                    </TableHead>
                    <TableHead>Restrições violadas</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {ranked.map((diet, index) => {
                    const active = diet.name === detail?.name

                    return (
                      <TableRow key={diet.name} data-state={active ? 'selected' : undefined}>
                        <TableCell className='tabular-nums'>{index + 1}º</TableCell>
                        <TableCell>
                          <button
                            type='button'
                            aria-pressed={active}
                            className='focus-visible:ring-ring/50 rounded text-left font-medium underline-offset-4 outline-none hover:underline focus-visible:ring-3'
                            onClick={() => onSelect(diet.name)}
                          >
                            {diet.name}
                          </button>
                          {diet.name === result.best && (
                            <Badge className='ml-2' variant='default'>
                              Melhor entre as informadas
                            </Badge>
                          )}
                        </TableCell>
                        <TableCell>
                          <DietBadge diet={diet} />
                        </TableCell>
                        <TableCell className='text-right tabular-nums'>{usd(diet.cost, 2)}</TableCell>
                        <TableCell className='text-right tabular-nums'>{usd(diet.cost_per_kg, 3)}</TableCell>
                        {optimalCost !== null && (
                          <TableCell className='text-right tabular-nums'>
                            {signedPct(((diet.cost - optimalCost) / optimalCost) * 100, 1)}
                          </TableCell>
                        )}
                        <TableCell className='text-right tabular-nums'>{diet.violation > 0 ? nf(diet.violation, 3) : '—'}</TableCell>
                        <TableCell className='text-muted-foreground text-xs'>
                          {diet.violated.length ? diet.violated.map(id => labelOf(diet, id)).join(' · ') : '—'}
                        </TableCell>
                      </TableRow>
                    )
                  })}
                  {optimalCost !== null && (
                    <TableRow className='bg-muted/40'>
                      <TableCell>Ref.</TableCell>
                      <TableCell className='font-medium'>Dieta ótima (sugerida)</TableCell>
                      <TableCell>
                        <Badge variant='secondary'>
                          <CheckCircle2Icon aria-hidden /> Viável
                        </Badge>
                      </TableCell>
                      <TableCell className='text-right tabular-nums'>{usd(optimalCost, 2)}</TableCell>
                      <TableCell />
                      <TableCell className='text-right tabular-nums'>0,0%</TableCell>
                      <TableCell />
                      <TableCell />
                    </TableRow>
                  )}
                </TableBody>
              </Table>
              {optimalCost !== null && (
                <p className='text-muted-foreground text-xs'>
                  O desvio é em relação à dieta ótima do cartão abaixo, que usa as exigências da vaca sem ração anterior; as
                  dietas acima usam as exigências calculadas com a própria dieta, então pequenas diferenças são esperadas.
                </p>
              )}
              {result.best === null && (
                <p className='text-muted-foreground text-xs'>Nenhuma das dietas informadas atende a todas as restrições.</p>
              )}
            </div>

            {detail && (
              <div className='space-y-4'>
                <h3 className='text-muted-foreground text-xs font-medium tracking-wider uppercase'>
                  Detalhe por restrição: {detail.name}
                </h3>

                <div className='grid grid-cols-2 gap-3 lg:grid-cols-4'>
                  <KpiCard label='Consumo de MS' value={`${nf(detail.intake.dry_matter, 2)} kg/dia`} />
                  <KpiCard
                    label='TDN da dieta'
                    value={detail.intake.tdn_percentage === null ? '—' : `${nf(detail.intake.tdn_percentage, 1)}%`}
                  />
                  <KpiCard
                    label='Concentrado na dieta'
                    value={
                      detail.intake.concentrate_percentage === null ? '—' : `${nf(detail.intake.concentrate_percentage, 1)}%`
                    }
                  />
                  <KpiCard
                    label='Desconto de ingestão (NRC)'
                    value={detail.intake.intake_discount === null ? '—' : nf(detail.intake.intake_discount, 3)}
                    hint={detail.intake.intake_discount === null ? 'só existe no padrão NRC' : '1 = sem desconto'}
                  />
                </div>

                <ConstraintTable diet={detail} />

                <p className='text-muted-foreground text-xs'>
                  <strong>Erro</strong>: maior desvio, com as quantidades variando de −5% a +5%, entre a oferta linear (coeficientes
                  congelados na dieta) e a oferta do RuFaS, em % da oferta do RuFaS. Nas classes L e E é 0. Valores acima de{' '}
                  {ERROR_ALERT_PCT}% aparecem em destaque. <strong>Folga</strong>: oferta − exigência (ou o inverso nos tetos);
                  negativa = violada. “No limite” = folga de até 0,5% da exigência.
                </p>

                {detail.warnings.length > 0 && (
                  <ul className='text-muted-foreground list-disc space-y-0.5 pl-4 text-xs'>
                    {detail.warnings
                      .filter(warning => !warnings.includes(warning))
                      .map(warning => (
                        <li key={warning}>{warning}</li>
                      ))}
                  </ul>
                )}
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  )
}

'use client'

import { useMemo } from 'react'

import { AlertTriangleIcon, CheckCircle2Icon, ListOrderedIcon, TrophyIcon } from 'lucide-react'

import { DivergingBars, StatusGrid, ToneBars, type CellStatus, type ToneDatum } from '@/components/charts'
import ChartCard from '@/components/ChartCard'
import { Segmented } from '@/components/Segmented'
import { KpiCard } from '@/components/shared'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { nf, shortName, signedPct, usd } from '@/lib/format'
import type { ModuleConstraint, ModuleDietResult, ModuleEvaluation } from '@/lib/types'
import { cn } from '@/lib/utils'

import { ConstraintBadge, DietBadge } from './StatusBadge'

/** Acima disso o erro de linearização é destacado (critério do FSD B.9-2, ainda em avaliação com o professor). */
const ERROR_ALERT_PCT = 1
/** Acima disso o eixo da folga corta a barra (o rótulo continua mostrando o valor real). */
export const SLACK_CLIP = 150

const CLASS_HINT: Record<string, string> = {
  L: 'Exata: a oferta é linear nas quantidades.',
  E: 'Razão (FDN, gordura): exata na forma Σ(aᵢ−c)xᵢ.',
  A: 'Aproximada: coeficientes congelados na dieta avaliada.'
}

const digits = (value: number) => (Math.abs(value) < 1 ? 3 : 2)
const fmt = (value: number | null | undefined) => (value == null ? '—' : nf(value, digits(value)))
const isLimit = (id: string) => id.startsWith('limit_')

/** Da mais para a menos recomendada (o back-end devolve o contrário). */
export function rankedDiets(result: ModuleEvaluation): ModuleDietResult[] {
  return [...result.ranking].reverse().map(name => result.diets.find(d => d.name === name)!)
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

/** Avisos da avaliação (exigências e cálculo), sem repetição. */
export function EvaluationWarnings({ result }: { result: ModuleEvaluation }) {
  const warnings = [...new Set([...result.requirement_warnings, ...result.warnings])]

  if (warnings.length === 0) return null

  return (
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
  )
}

interface ViewProps {
  result: ModuleEvaluation
  selected: string | null
  onSelect: (name: string) => void
}

/** Ranking das dietas: indicadores, custo por dieta (barras) e o detalhe da dieta escolhida. */
export function RankingView({ result, selected, onSelect, optimalCost }: ViewProps & { optimalCost: number | null }) {
  const ranked = useMemo(() => rankedDiets(result), [result])
  const detail = ranked.find(d => d.name === selected) ?? ranked[0] ?? null
  const best = ranked.find(d => d.name === result.best) ?? null
  const feasible = ranked.filter(d => d.feasible).length
  const labelOf = (diet: ModuleDietResult, id: string) => diet.constraints.find(c => c.id === id)?.label ?? id

  const bars: ToneDatum[] = ranked.map(diet => ({
    name: shortName(diet.name, 24),
    value: diet.cost,
    tone: diet.name === result.best ? 'best' : diet.feasible ? 'ok' : 'bad'
  }))
  const deviation = best && optimalCost ? ((best.cost - optimalCost) / optimalCost) * 100 : undefined

  const rankingTable = (
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
                <TableCell className='text-right tabular-nums'>{signedPct(((diet.cost - optimalCost) / optimalCost) * 100, 1)}</TableCell>
              )}
              <TableCell className='text-right tabular-nums'>{diet.violation > 0 ? nf(diet.violation, 3) : '—'}</TableCell>
              <TableCell className='text-muted-foreground text-xs whitespace-normal'>
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
  )

  return (
    <>
      <div className='grid gap-3 sm:grid-cols-2 2xl:grid-cols-4'>
        <KpiCard
          tone={best ? 'primary' : 'warning'}
          icon={TrophyIcon}
          label='Melhor entre as informadas'
          value={best ? best.name : 'Nenhuma viável'}
          hint={best ? `${usd(best.cost, 2)}/dia` : 'Nenhuma atende a todas as restrições'}
        />
        <KpiCard icon={ListOrderedIcon} color='info' label='Dietas viáveis' value={`${feasible} de ${ranked.length}`} />
        <KpiCard
          label='Menor custo entre as viáveis'
          color='violet'
          icon={TrophyIcon}
          value={best ? `${usd(best.cost, 2)}/dia` : '—'}
          delta={deviation}
          better='down'
          hint={deviation !== undefined ? 'vs. dieta ótima' : undefined}
        />
        <KpiCard
          label='Dieta ótima (LP)'
          color='warning'
          icon={CheckCircle2Icon}
          value={optimalCost !== null ? `${usd(optimalCost, 2)}/dia` : '—'}
          hint={optimalCost === null ? 'calcule na aba Dieta ótima' : undefined}
        />
      </div>

      <EvaluationWarnings result={result} />

      <ChartCard
        title='Custo por dieta'
        description={
          <>
            US$ por vaca por dia, da mais para a menos recomendada. Verde vivo: a melhor viável; verde apagado: as outras viáveis; vermelho:
            inviáveis{optimalCost !== null ? '; a linha tracejada é a dieta ótima' : ''}.
          </>
        }
        chart={
          <ToneBars
            data={bars}
            format={value => usd(value, 2)}
            height={Math.max(200, bars.length * 48 + 40)}
            reference={optimalCost ?? undefined}
            referenceLabel={optimalCost !== null ? 'Ótima (LP)' : undefined}
          />
        }
        table={rankingTable}
        footer={
          <>
            {result.best === null && <p className='text-muted-foreground text-xs'>Nenhuma das dietas informadas atende a todas as restrições.</p>}
            {optimalCost !== null && (
              <p className='text-muted-foreground text-xs'>
                O desvio é em relação à dieta ótima da aba Dieta ótima, que usa as exigências da vaca sem ração anterior; as dietas aqui usam as exigências
                calculadas com a própria dieta, então pequenas diferenças são esperadas.
              </p>
            )}
          </>
        }
      />

      {detail && (
        <Card>
          <CardHeader>
            <CardTitle>Dieta {detail.name}</CardTitle>
            <CardDescription>
              <span className='flex flex-wrap items-center gap-2'>
                Escolha a dieta para ver o consumo e o desconto de ingestão.
                <Segmented
                  label='Dieta em detalhe'
                  value={detail.name}
                  options={ranked.map(d => ({ value: d.name, label: d.name }))}
                  onChange={onSelect}
                />
              </span>
            </CardDescription>
          </CardHeader>
          <CardContent className='space-y-4'>
            <div className='grid grid-cols-2 gap-3 lg:grid-cols-4'>
              <KpiCard label='Consumo de MS' value={`${nf(detail.intake.dry_matter, 2)} kg/dia`} />
              <KpiCard label='TDN da dieta' value={detail.intake.tdn_percentage === null ? '—' : `${nf(detail.intake.tdn_percentage, 1)}%`} />
              <KpiCard
                label='Concentrado na dieta'
                value={detail.intake.concentrate_percentage === null ? '—' : `${nf(detail.intake.concentrate_percentage, 1)}%`}
              />
              <KpiCard
                label='Desconto de ingestão (NRC)'
                value={detail.intake.intake_discount === null ? '—' : nf(detail.intake.intake_discount, 3)}
                hint={detail.intake.intake_discount === null ? 'só existe no padrão NRC' : '1 = sem desconto'}
              />
            </div>
            {detail.warnings.length > 0 && (
              <ul className='text-muted-foreground list-disc space-y-0.5 pl-4 text-xs'>
                {detail.warnings.map(warning => (
                  <li key={warning}>{warning}</li>
                ))}
              </ul>
            )}
          </CardContent>
        </Card>
      )}
    </>
  )
}

const CELL: Record<string, CellStatus> = { ok: 'ok', no_limite: 'no_limite', violada: 'violada', indisponivel: 'indisponivel' }

/** Restrições: mapa de estados (dieta × restrição), folga da dieta escolhida em % da exigência e a tabela completa. */
export function ConstraintsView({ result, selected, onSelect }: ViewProps) {
  const ranked = useMemo(() => rankedDiets(result), [result])
  const detail = ranked.find(d => d.name === selected) ?? ranked[0] ?? null

  // os limites por alimento são dados do usuário e ficam na tabela; o mapa mostra as restrições nutricionais
  const columns = (ranked[0]?.constraints ?? []).filter(c => !isLimit(c.id)).map(c => ({ id: c.id, label: c.label }))
  const rows = ranked.map(diet => ({
    label: diet.name,
    cells: columns.map(column => CELL[diet.constraints.find(c => c.id === column.id)?.status ?? 'indisponivel'])
  }))

  const slack = (detail?.constraints ?? [])
    .filter(c => !isLimit(c.id) && c.slack != null && c.requirement)
    .map(c => {
      const pct = ((c.slack as number) / Math.abs(c.requirement as number)) * 100

      return { name: shortName(c.label, 26), value: pct, bar: Math.min(Math.max(pct, -100), SLACK_CLIP) }
    })

  return (
    <>
      <ChartCard
        title='Mapa de restrições'
        description='Cada linha é uma dieta (da mais para a menos recomendada) e cada coluna, uma restrição nutricional. ✓ atende, ! no limite (folga de até 0,5%), ✕ violada, – indisponível.'
        chart={<StatusGrid columns={columns} rows={rows} />}
        table={detail ? <ConstraintTable diet={detail} /> : undefined}
      />

      {detail && (
        <ChartCard
          title='Folga da dieta escolhida'
          description={
            <span className='flex flex-wrap items-center gap-2'>
              Folga em % da exigência (oferta − exigência; nos tetos, o inverso). Verde: atende; vermelho: viola.
              <Segmented label='Dieta em detalhe' value={detail.name} options={ranked.map(d => ({ value: d.name, label: d.name }))} onChange={onSelect} />
            </span>
          }
          chart={
            slack.length > 0 ? (
              <DivergingBars data={slack} format={value => signedPct(value, 0)} domain={[-100, SLACK_CLIP]} height={Math.max(220, slack.length * 40 + 30)} />
            ) : (
              <p className='text-muted-foreground py-8 text-center text-sm'>Sem restrições calculadas para esta dieta.</p>
            )
          }
          table={<ConstraintTable diet={detail} />}
          footer={
            <p className='text-muted-foreground text-xs'>
              <strong>Erro</strong>: maior desvio, com as quantidades variando de −5% a +5%, entre a oferta linear (coeficientes congelados na dieta) e a
              oferta do RuFaS, em % da oferta do RuFaS; nas classes L e E é 0. <strong>Folga</strong> negativa = violada.
            </p>
          }
        />
      )}
    </>
  )
}

'use client'

import { useCallback, useEffect, useMemo, useState } from 'react'

import { AlertTriangleIcon, BeakerIcon, GridIcon, ListIcon, PlusIcon, ScaleIcon, Trash2Icon, TrendingDownIcon, TrendingUpIcon, WalletIcon, WheatIcon } from 'lucide-react'
import { toast } from 'sonner'

import { Bullet, HeatMap, HighlightBars, ShareBars, type BulletBand } from '@/components/charts'
import ChartCard from '@/components/ChartCard'
import { EmptyState, ResultsSkeleton } from '@/components/EmptyState'
import ExportButtons from '@/components/ExportButtons'
import RunButton, { type RunState } from '@/components/RunButton'
import { finite, heat, KpiCard, NumberInput } from '@/components/shared'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Tabs, TabsList, TabsPanel, TabsTab } from '@/components/ui/tabs'
import { api } from '@/lib/api'
import { nf, usd } from '@/lib/format'
import { cn } from '@/lib/utils'
import { useApp } from '@/providers/AppProvider'

interface ToyFactor {
  target: string
  low: number
  high: number
  n: number
}

const DEFAULT_FACTORS: ToyFactor[] = [
  { target: 'cost:Arroz', low: 1, high: 2, n: 3 },
  { target: 'cost:Milho', low: 1.8, high: 2.6, n: 3 }
]

/** Cores das faixas do custo por alimento (sem o vermelho, reservado ao que falha). */
const SHARE_COLORS = ['var(--chart-1)', 'var(--chart-3)', 'var(--chart-5)', 'var(--chart-2)', 'var(--chart-6)', 'var(--chart-7)', 'var(--chart-8)']
const SHARE_OTHER = 'color-mix(in oklch, var(--muted-foreground) 55%, transparent)'
/** Um máximo a partir daqui é tratado como "sem teto" (o back-end recebe 1e9 quando o campo fica vazio). */
const OPEN_MAX = 1e6

const messageOf = (error: unknown, fallback: string) => (error instanceof Error ? error.message : fallback).split('\n')[0]
const showResults = () => document.getElementById('resultados-quadro')?.scrollIntoView({ behavior: 'smooth', block: 'start' })

function targetLabel(target: string) {
  const [kind, name] = target.split(':')

  return `${{ cost: 'Custo', min: 'Mínimo', max: 'Máximo' }[kind] ?? kind} · ${name}`
}

/** Faixas do bullet de um nutriente: fora do intervalo [mínimo, máximo] é alerta, dentro é ok. */
function boundScale(total: number, min: number, max: number) {
  const open = !Number.isFinite(max) || max >= OPEN_MAX
  const top = Math.max(total, min, open ? 0 : max) * 1.3 || 1
  const bands: BulletBand[] = [
    ...(min > 0 ? [{ to: min, tone: 'alert' as const }] : []),
    { to: open ? top : max, tone: 'ok' as const },
    ...(open ? [] : [{ to: top, tone: 'alert' as const }])
  ]

  return { top, bands }
}

export default function ToyView() {
  const {
    connection,
    toyFoods,
    setToyFoods,
    toyBounds,
    setToyBounds,
    toyResult,
    setToyResult,
    toySens,
    setToySens,
    toyKey,
    setToyKey,
    toySensKey,
    setToySensKey
  } = useApp()
  const [solving, setSolving] = useState(false)
  const [solveError, setSolveError] = useState<string | null>(null)
  const [generating, setGenerating] = useState(false)
  const [sensError, setSensError] = useState<string | null>(null)
  const [factors, setFactors] = useState<ToyFactor[]>(DEFAULT_FACTORS)

  const problem = useMemo(
    () => ({
      foods: toyFoods.map(f => ({
        name: f.name,
        cost: finite(f.cost),
        nutrients: { Carboidrato: finite(f.carb), Proteína: finite(f.prot) }
      })),
      bounds: Object.fromEntries(
        toyBounds.map(b => [b.name, { min: finite(b.min), max: Number.isFinite(b.max) ? b.max : 1e9 }])
      )
    }),
    [toyFoods, toyBounds]
  )
  const problemKey = JSON.stringify(problem)
  const sensBody = useMemo(
    () => ({
      problem,
      factors: factors.map(f => ({ ...f, low: finite(f.low), high: finite(f.high), n: Math.max(2, finite(f.n, 2)) }))
    }),
    [problem, factors]
  )
  const sensBodyKey = JSON.stringify(sensBody)
  const stale = toyResult !== null && toyKey !== problemKey
  const sensStale = toySens !== null && toySensKey !== sensBodyKey

  const solve = useCallback(async () => {
    setSolving(true)
    setSolveError(null)

    try {
      setToyResult(await api.toy(problem))
      setToyKey(JSON.stringify(problem))
    } catch (error) {
      setSolveError(messageOf(error, 'Falha ao resolver'))
      toast.error(messageOf(error, 'Falha ao resolver'))
    } finally {
      setSolving(false)
    }
  }, [problem, setToyResult, setToyKey])

  // Resolve o problema do quadro automaticamente na primeira visita.
  useEffect(() => {
    if (connection === 'online' && !toyResult) void solve()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [connection])

  const targets = useMemo(
    () => [
      ...toyFoods.map(f => `cost:${f.name}`),
      ...toyBounds.flatMap(b => [`min:${b.name}`, `max:${b.name}`])
    ],
    [toyFoods, toyBounds]
  )
  const targetItems = targets.map(t => ({ value: t, label: targetLabel(t) }))

  const generate = async () => {
    if (factors[0].target === factors[1].target) {
      toast.error('Escolha dois fatores diferentes.')

      return
    }

    setGenerating(true)
    setSensError(null)

    try {
      setToySens(await api.toySensitivity(sensBody))
      setToySensKey(sensBodyKey)
    } catch (error) {
      setSensError(messageOf(error, 'Falha ao gerar cenários'))
      toast.error(messageOf(error, 'Falha ao gerar cenários'))
    } finally {
      setGenerating(false)
    }
  }

  const updateFood = (index: number, patch: Partial<(typeof toyFoods)[number]>) =>
    setToyFoods(toyFoods.map((f, i) => (i === index ? { ...f, ...patch } : f)))

  const updateBound = (index: number, patch: Partial<(typeof toyBounds)[number]>) =>
    setToyBounds(toyBounds.map((b, i) => (i === index ? { ...b, ...patch } : b)))

  const updateFactor = (index: number, patch: Partial<ToyFactor>) =>
    setFactors(factors.map((f, i) => (i === index ? { ...f, ...patch } : f)))

  const runState: RunState = solving ? 'running' : solveError ? 'error' : toyResult && !stale ? 'done' : 'idle'
  const amountOf = (name: string) => toyResult?.amounts[name] ?? 0

  // ---- solução
  const used = toyResult?.feasible ? toyFoods.filter(f => amountOf(f.name) > 1e-6).length : 0
  const mainFood = toyFoods.reduce((a, f) => (amountOf(f.name) > amountOf(a) ? f.name : a), toyFoods[0]?.name ?? '')
  const activeCount = toyResult?.feasible
    ? toyBounds.filter(b => {
        const total = toyResult.nutrient_totals[b.name]

        return Math.abs(total - b.min) < 1e-6 || Math.abs(total - b.max) < 1e-6
      }).length
    : 0
  const costShare = toyFoods
    .map((food, index) => ({ name: food.name, value: amountOf(food.name) * finite(food.cost), color: SHARE_COLORS[index] ?? SHARE_OTHER }))
    .filter(part => part.value > 1e-9)

  const foodTable = toyResult && (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Alimento</TableHead>
          <TableHead className='text-right'>Quantidade</TableHead>
          <TableHead className='text-right'>Custo</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {toyFoods.map(food => (
          <TableRow key={food.name}>
            <TableCell>{food.name}</TableCell>
            <TableCell className='text-right tabular-nums'>{nf(amountOf(food.name), 3)} kg</TableCell>
            <TableCell className='text-right tabular-nums'>{usd(amountOf(food.name) * finite(food.cost), 2)}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )

  const nutrientTable = toyResult && (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Nutriente</TableHead>
          <TableHead className='text-right'>Total</TableHead>
          <TableHead className='text-right'>Faixa</TableHead>
          <TableHead>Restrição</TableHead>
          <TableHead className='text-right'>Preço-sombra</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {toyBounds.map(bound => {
          const total = toyResult.nutrient_totals[bound.name]
          const atMin = Math.abs(total - bound.min) < 1e-6
          const atMax = Math.abs(total - bound.max) < 1e-6
          const shadow = toyResult.shadow_prices[`${bound.name}_min`]

          return (
            <TableRow key={bound.name}>
              <TableCell>{bound.name}</TableCell>
              <TableCell className='text-right tabular-nums'>{nf(total, 3)} kg</TableCell>
              <TableCell className='text-right tabular-nums'>
                {nf(bound.min, 2)} – {bound.max >= OPEN_MAX ? '∞' : nf(bound.max, 2)}
              </TableCell>
              <TableCell>
                {atMin || atMax ? (
                  <Badge variant='secondary'>{atMin ? 'mínimo ativo' : 'máximo ativo'}</Badge>
                ) : (
                  <span className='text-muted-foreground text-xs'>folga</span>
                )}
              </TableCell>
              <TableCell className='text-right tabular-nums'>{shadow ? `${usd(shadow, 2)}/kg` : '—'}</TableCell>
            </TableRow>
          )
        })}
      </TableBody>
    </Table>
  )

  // ---- cenários
  const valid = toySens?.rows.filter(r => r.Res !== null) ?? []
  const costs = valid.map(r => r.Res as number)
  const [sensMin, sensMax] = [Math.min(...costs), Math.max(...costs)]
  const bestRow = valid.find(r => r.Res === sensMin)
  const worstRow = valid.find(r => r.Res === sensMax)
  const failed = (toySens?.rows.length ?? 0) - valid.length
  const factorColumns = toySens?.columns.filter(c => c !== 'Res') ?? []
  const grid = (() => {
    if (!toySens || factorColumns.length !== 2) return null

    const [rowKey, colKey] = factorColumns
    const unique = (key: string) => [...new Set(toySens.rows.map(r => r[key] as number))].sort((a, b) => a - b)
    const ys = unique(rowKey)
    const xs = unique(colKey)
    const at = (y: number, x: number) => toySens.rows.find(r => r[rowKey] === y && r[colKey] === x)?.Res ?? null

    return { rowKey, colKey, xs, ys, values: ys.map(y => xs.map(x => at(y, x))) }
  })()

  const scenarioTable = toySens && (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead />
          {toySens.columns.map(c => (
            <TableHead key={c} className='text-right'>
              {c === 'Res' ? 'Res (US$/dia)' : targetLabel(c)}
            </TableHead>
          ))}
          <TableHead>Dieta ótima</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {toySens.rows.map(row => (
          <TableRow key={row.cenario}>
            <TableCell className='font-medium'>{row.cenario}</TableCell>
            {toySens.columns.map(c =>
              c === 'Res' ? (
                <TableCell
                  key={c}
                  className='text-right font-semibold tabular-nums'
                  style={row.Res === null ? undefined : heat(row.Res, sensMin, sensMax, true)}
                >
                  {row.Res === null ? <span className='text-destructive'>inviável</span> : nf(row.Res, 2)}
                </TableCell>
              ) : (
                <TableCell key={c} className='text-right tabular-nums'>
                  {nf(row[c] as number, 2)}
                </TableCell>
              )
            )}
            <TableCell className='text-muted-foreground text-xs'>
              {Object.entries(row.amounts)
                .map(([name, kg]) => `${name} ${nf(kg, 2)} kg`)
                .join(' · ')}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )

  return (
    <div className='space-y-6'>
      <Card>
        <CardHeader>
          <CardTitle>Problema</CardTitle>
          <CardDescription>Minimizar Σ custo × quantidade, com mín ≤ Σ nutriente × quantidade ≤ máx para cada nutriente.</CardDescription>
        </CardHeader>
        <CardContent className='space-y-6'>
          <div className='grid gap-6 xl:grid-cols-[3fr_2fr]'>
            <div className='space-y-2'>
              <h3 className='text-muted-foreground text-xs font-medium tracking-wider uppercase'>Alimentos</h3>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Alimento</TableHead>
                    <TableHead className='text-right'>Custo (US$/kg)</TableHead>
                    <TableHead className='text-right'>Carboidrato (kg/kg)</TableHead>
                    <TableHead className='text-right'>Proteína (kg/kg)</TableHead>
                    <TableHead className='w-10' />
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {toyFoods.map((food, i) => (
                    <TableRow key={i}>
                      <TableCell>
                        <Input
                          className='h-8 min-w-24'
                          value={food.name}
                          aria-label='Nome do alimento'
                          onChange={e => updateFood(i, { name: e.target.value })}
                        />
                      </TableCell>
                      <TableCell>
                        <NumberInput value={food.cost} onChange={v => updateFood(i, { cost: v })} aria-label='Custo' />
                      </TableCell>
                      <TableCell>
                        <NumberInput value={food.carb} onChange={v => updateFood(i, { carb: v })} aria-label='Carboidrato' />
                      </TableCell>
                      <TableCell>
                        <NumberInput value={food.prot} onChange={v => updateFood(i, { prot: v })} aria-label='Proteína' />
                      </TableCell>
                      <TableCell>
                        {toyFoods.length > 2 && (
                          <Button
                            variant='ghost'
                            size='icon-sm'
                            aria-label={`Remover ${food.name}`}
                            onClick={() => setToyFoods(toyFoods.filter((_, k) => k !== i))}
                          >
                            <Trash2Icon />
                          </Button>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
              <Button
                variant='outline'
                size='sm'
                onClick={() => setToyFoods([...toyFoods, { name: `Alimento ${toyFoods.length + 1}`, cost: 1, carb: 0.5, prot: 0.1 }])}
              >
                <PlusIcon /> Alimento
              </Button>
            </div>

            <div className='space-y-2'>
              <h3 className='text-muted-foreground text-xs font-medium tracking-wider uppercase'>Nutrientes</h3>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Nutriente</TableHead>
                    <TableHead className='text-right'>Mínimo (kg)</TableHead>
                    <TableHead className='text-right'>Máximo (kg)</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {toyBounds.map((bound, i) => (
                    <TableRow key={bound.name}>
                      <TableCell className='font-medium'>{bound.name}</TableCell>
                      <TableCell>
                        <NumberInput value={bound.min} step={0.1} onChange={v => updateBound(i, { min: v })} aria-label={`Mínimo de ${bound.name}`} />
                      </TableCell>
                      <TableCell>
                        <NumberInput value={bound.max} step={0.1} onChange={v => updateBound(i, { max: v })} aria-label={`Máximo de ${bound.name}`} />
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </div>

          <div className='space-y-2'>
            <div className='sm:max-w-72'>
              <RunButton state={runState} label='Resolver' error={solveError} disabled={connection !== 'online'} onRun={solve} onView={showResults} />
            </div>
            {toyResult && stale && !solving && (
              <p className='text-muted-foreground text-sm' role='status'>
                O problema mudou desde a última solução. Clique em Resolver para atualizar.
              </p>
            )}
            {connection !== 'online' && <p className='text-muted-foreground text-sm'>O servidor local não está respondendo.</p>}
          </div>
        </CardContent>
      </Card>

      <div id='resultados-quadro' className='min-w-0 scroll-mt-24'>
        <Tabs defaultValue='solution'>
          <div className='flex flex-wrap items-center justify-between gap-3'>
            <TabsList>
              <TabsTab value='solution'>
                <ScaleIcon /> Solução ótima
              </TabsTab>
              <TabsTab value='scenarios'>
                <GridIcon /> Cenários
              </TabsTab>
            </TabsList>
          </div>

          <TabsPanel value='solution'>
            {!toyResult ? (
              solving ? (
                <ResultsSkeleton />
              ) : (
                <EmptyState
                  icon={ScaleIcon}
                  title='Nenhuma solução ainda'
                  steps={['Confira os alimentos, os custos e as faixas de cada nutriente.', 'Clique em Resolver: o programa linear devolve a dieta de menor custo.']}
                />
              )
            ) : !toyResult.feasible ? (
              <Alert variant='destructive'>
                <AlertTriangleIcon />
                <AlertTitle>Sem solução viável</AlertTitle>
                <AlertDescription>Os limites mínimo e máximo são incompatíveis com os alimentos disponíveis. Afrouxe um limite ou inclua outro alimento.</AlertDescription>
              </Alert>
            ) : (
              <div className={cn('space-y-6 transition-opacity', (stale || solving) && 'opacity-60')}>
                <div className='grid gap-3 sm:grid-cols-2 2xl:grid-cols-4'>
                  <KpiCard tone='primary' icon={WalletIcon} label='Custo mínimo por dia' value={usd(toyResult.cost, 2)} />
                  <KpiCard icon={WheatIcon} color='info' label='Alimentos usados' value={String(used)} hint={`de ${toyFoods.length} disponíveis`} />
                  <KpiCard icon={BeakerIcon} color='violet' label='Restrições ativas' value={String(activeCount)} hint={`de ${toyBounds.length} nutrientes`} />
                  <KpiCard icon={ScaleIcon} color='warning' label='Maior quantidade' value={mainFood} hint={`${nf(amountOf(mainFood), 2)} kg por dia`} />
                </div>

                <ChartCard
                  title='Quantidade de cada alimento'
                  description='kg por dia na dieta ótima; o alimento de maior quantidade em verde vivo.'
                  chart={
                    <HighlightBars
                      data={toyFoods.map(f => ({ name: f.name, value: amountOf(f.name) }))}
                      highlight={mainFood}
                      format={value => nf(value, 2)}
                      axisFormat={value => nf(value, 0)}
                      height={240}
                    />
                  }
                  table={foodTable}
                />

                <ChartCard
                  title='Para onde vai o custo'
                  description='Participação de cada alimento no custo mínimo por dia.'
                  chart={costShare.length > 0 ? <ShareBars rows={[{ label: `Custo total ${usd(toyResult.cost, 2)}`, parts: costShare }]} /> : <p className='text-muted-foreground py-8 text-center text-sm'>Dieta sem custo.</p>}
                  table={foodTable}
                />

                <ChartCard
                  title='Nutrientes na faixa'
                  description='O total de cada nutriente contra a faixa exigida: verde é o intervalo permitido, vermelho fica fora. O traço branco é o total da dieta ótima.'
                  chart={
                    <ul className='space-y-4'>
                      {toyBounds.map(bound => {
                        const total = toyResult.nutrient_totals[bound.name]
                        const { top, bands } = boundScale(total, bound.min, bound.max)

                        return (
                          <li key={bound.name} className='grid grid-cols-[7rem_1fr_auto] items-center gap-3 text-sm'>
                            <span className='font-medium'>{bound.name}</span>
                            <Bullet value={total} min={0} max={top} bands={bands} />
                            <span className='text-muted-foreground text-xs tabular-nums'>
                              {nf(total, 2)} kg · faixa {nf(bound.min, 2)} – {bound.max >= OPEN_MAX ? '∞' : nf(bound.max, 2)}
                            </span>
                          </li>
                        )
                      })}
                    </ul>
                  }
                  table={nutrientTable}
                  footer={<p className='text-muted-foreground text-xs'>Preço-sombra (na tabela): quanto o custo ótimo aumenta se o mínimo do nutriente subir 1 kg.</p>}
                />
              </div>
            )}
          </TabsPanel>

          <TabsPanel value='scenarios'>
            <div className='space-y-6'>
              <Card>
                <CardHeader>
                  <CardTitle>Cenários e sensibilidade</CardTitle>
                  <CardDescription>
                    Como no quadro: cada cenário S<sub>i</sub> é uma linha com os parâmetros e o resultado <strong>Res</strong> (custo ótimo da dieta).
                  </CardDescription>
                </CardHeader>
                <CardContent className='space-y-4'>
                  <div className='grid gap-4 md:grid-cols-2'>
                    {factors.map((factor, i) => (
                      <div key={i} className='grid grid-cols-[1fr_5rem_5rem_4.5rem] items-end gap-2'>
                        <div className='space-y-1.5'>
                          <Label>Fator {i + 1}</Label>
                          <Select value={factor.target} items={targetItems} onValueChange={value => value && updateFactor(i, { target: value })}>
                            <SelectTrigger className='w-full'>
                              <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                              {targetItems.map(item => (
                                <SelectItem key={item.value} value={item.value}>
                                  {item.label}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </div>
                        <div className='space-y-1.5'>
                          <Label>De</Label>
                          <NumberInput className='h-9' step={0.1} value={factor.low} onChange={v => updateFactor(i, { low: v })} />
                        </div>
                        <div className='space-y-1.5'>
                          <Label>Até</Label>
                          <NumberInput className='h-9' step={0.1} value={factor.high} onChange={v => updateFactor(i, { high: v })} />
                        </div>
                        <div className='space-y-1.5'>
                          <Label>Níveis</Label>
                          <NumberInput className='h-9' step={1} min={2} value={factor.n} onChange={v => updateFactor(i, { n: v })} />
                        </div>
                      </div>
                    ))}
                  </div>

                  <div className='flex flex-wrap items-center gap-3'>
                    <Button onClick={generate} disabled={generating || connection !== 'online'}>
                      <ListIcon /> {generating ? 'Gerando…' : 'Gerar cenários'}
                    </Button>
                    {toySens && <ExportButtons screen='toy' data={toySens} csvOnly />}
                  </div>
                  {toySens && sensStale && !generating && (
                    <p className='text-muted-foreground text-sm' role='status'>
                      O problema ou os fatores mudaram desde estes cenários. Clique em Gerar cenários para atualizá-los.
                    </p>
                  )}
                  {sensError && (
                    <Alert variant='destructive'>
                      <AlertTriangleIcon />
                      <AlertTitle>Não foi possível gerar os cenários</AlertTitle>
                      <AlertDescription>{sensError}</AlertDescription>
                    </Alert>
                  )}
                </CardContent>
              </Card>

              {!toySens ? (
                generating ? (
                  <ResultsSkeleton />
                ) : (
                  <EmptyState
                    icon={GridIcon}
                    title='Nenhum cenário ainda'
                    steps={['Escolha dois fatores (custo, mínimo ou máximo) e a faixa de cada um.', 'Clique em Gerar cenários: cada combinação é resolvida e vira uma linha Sᵢ.']}
                  />
                )
              ) : (
                <div className={cn('space-y-6 transition-opacity', (sensStale || generating) && 'opacity-60')}>
                  {bestRow && worstRow && (
                    <div className='grid gap-3 sm:grid-cols-2 2xl:grid-cols-4'>
                      <KpiCard tone='primary' icon={TrendingDownIcon} label={`Menor custo (${bestRow.cenario})`} value={usd(sensMin, 2)} hint='por vaca e por dia' />
                      <KpiCard icon={TrendingUpIcon} color='destructive' label={`Maior custo (${worstRow.cenario})`} value={usd(sensMax, 2)} />
                      <KpiCard icon={ScaleIcon} color='info' label='Amplitude' value={usd(sensMax - sensMin, 2)} hint={`${nf(sensMin > 0 ? ((sensMax - sensMin) / sensMin) * 100 : 0, 0)}% acima do menor`} />
                      <KpiCard
                        icon={GridIcon}
                        color={failed ? 'warning' : 'violet'}
                        tone={failed ? 'warning' : 'default'}
                        label='Cenários resolvidos'
                        value={`${valid.length} de ${toySens.rows.length}`}
                        hint={failed ? `${failed} sem solução viável` : undefined}
                      />
                    </div>
                  )}

                  <ChartCard
                    title='Custo ótimo por cenário'
                    description='Res de cada cenário em US$ por dia; o cenário de menor custo em verde vivo. Cenários sem solução viável não aparecem no gráfico.'
                    chart={
                      valid.length > 0 ? (
                        <HighlightBars
                          data={valid.map(r => ({ name: r.cenario, value: r.Res }))}
                          highlight={bestRow?.cenario}
                          format={value => nf(value, 2)}
                          axisFormat={value => nf(value, 1)}
                          height={260}
                        />
                      ) : (
                        <p className='text-muted-foreground py-8 text-center text-sm'>Nenhum cenário com solução viável.</p>
                      )
                    }
                    table={scenarioTable}
                  />

                  {grid && (
                    <ChartCard
                      title='Mapa dos dois fatores'
                      description='O custo ótimo em cada combinação: quanto mais verde, mais barato; o contorno marca o menor custo.'
                      chart={
                        <HeatMap
                          xLabels={grid.xs.map(v => nf(v, 2))}
                          yLabels={grid.ys.map(v => nf(v, 2))}
                          values={grid.values}
                          format={value => usd(value, 2)}
                          xTitle={targetLabel(grid.colKey)}
                          yTitle={targetLabel(grid.rowKey)}
                        />
                      }
                      table={scenarioTable}
                    />
                  )}
                </div>
              )}
            </div>
          </TabsPanel>
        </Tabs>
      </div>
    </div>
  )
}

'use client'

import { useCallback, useEffect, useMemo, useState } from 'react'

import { PlayIcon, PlusIcon, Trash2Icon } from 'lucide-react'
import { toast } from 'sonner'
import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from 'recharts'

import { finite, heat, KpiCard, NumberInput, PageHeader } from '@/components/shared'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { ChartContainer, ChartTooltip, ChartTooltipContent, type ChartConfig } from '@/components/ui/chart'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { api } from '@/lib/api'
import { nf, usd } from '@/lib/format'
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

const chartConfig = { kg: { label: 'kg por dia', color: 'var(--chart-1)' } } satisfies ChartConfig

function targetLabel(target: string) {
  const [kind, name] = target.split(':')

  return `${{ cost: 'Custo', min: 'Mínimo', max: 'Máximo' }[kind] ?? kind} · ${name}`
}

export default function ToyView() {
  const { connection, toyFoods, setToyFoods, toyBounds, setToyBounds, toyResult, setToyResult, toySens, setToySens } =
    useApp()
  const [solving, setSolving] = useState(false)
  const [generating, setGenerating] = useState(false)
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

  const solve = useCallback(async () => {
    setSolving(true)

    try {
      setToyResult(await api.toy(problem))
    } catch (error) {
      toast.error(error instanceof Error ? error.message : 'Falha ao resolver')
    } finally {
      setSolving(false)
    }
  }, [problem, setToyResult])

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

    try {
      setToySens(
        await api.toySensitivity({
          problem,
          factors: factors.map(f => ({ ...f, low: finite(f.low), high: finite(f.high), n: Math.max(2, finite(f.n, 2)) }))
        })
      )
    } catch (error) {
      toast.error(error instanceof Error ? error.message : 'Falha ao gerar cenários')
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

  const sensValues = toySens?.rows.map(r => r.Res).filter((v): v is number => v !== null) ?? []
  const [sensMin, sensMax] = [Math.min(...sensValues), Math.max(...sensValues)]

  return (
    <>
      <PageHeader
        title='Exercício do quadro'
        description='Dieta de custo mínimo respeitando o mínimo e o máximo diário de cada nutriente. É a modelagem de Pesquisa Operacional que dá base ao restante do sistema.'
      />

      <div className='grid gap-6 xl:grid-cols-2'>
        <Card>
          <CardHeader>
            <CardTitle>Problema</CardTitle>
            <CardDescription>
              Minimizar Σ custo × quantidade, com mín ≤ Σ nutriente × quantidade ≤ máx para cada nutriente.
            </CardDescription>
          </CardHeader>
          <CardContent className='space-y-6'>
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
                onClick={() =>
                  setToyFoods([...toyFoods, { name: `Alimento ${toyFoods.length + 1}`, cost: 1, carb: 0.5, prot: 0.1 }])
                }
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

            <Button onClick={solve} disabled={solving || connection !== 'online'}>
              <PlayIcon /> {solving ? 'Resolvendo…' : 'Resolver'}
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Solução ótima</CardTitle>
            <CardDescription>Resolvida por programação linear (HiGHS, via SciPy).</CardDescription>
          </CardHeader>
          <CardContent className='space-y-6'>
            {!toyResult ? (
              <p className='text-muted-foreground text-sm'>Clique em “Resolver”.</p>
            ) : !toyResult.feasible ? (
              <div className='border-destructive/40 bg-destructive/5 text-destructive rounded-lg border p-4 text-sm'>
                <strong>Sem solução viável.</strong> Os limites mínimo e máximo são incompatíveis com os alimentos
                disponíveis.
              </div>
            ) : (
              <>
                <div className='grid gap-3 sm:grid-cols-2'>
                  <KpiCard tone='primary' label='Custo mínimo por dia' value={usd(toyResult.cost, 2)} />
                  <KpiCard
                    label='Alimentos usados'
                    value={String(Object.values(toyResult.amounts).filter(v => v > 1e-6).length)}
                    hint={`de ${toyFoods.length} disponíveis`}
                  />
                </div>

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
                        <TableCell className='text-right tabular-nums'>{nf(toyResult.amounts[food.name], 3)} kg</TableCell>
                        <TableCell className='text-right tabular-nums'>
                          {usd((toyResult.amounts[food.name] ?? 0) * finite(food.cost), 2)}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>

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
                            {nf(bound.min, 2)} – {nf(bound.max, 2)}
                          </TableCell>
                          <TableCell>
                            {atMin || atMax ? (
                              <Badge variant='secondary'>{atMin ? 'mínimo ativo' : 'máximo ativo'}</Badge>
                            ) : (
                              <span className='text-muted-foreground text-xs'>folga</span>
                            )}
                          </TableCell>
                          <TableCell className='text-right tabular-nums'>
                            {shadow ? `${usd(shadow, 2)}/kg` : '—'}
                          </TableCell>
                        </TableRow>
                      )
                    })}
                  </TableBody>
                </Table>
                <p className='text-muted-foreground text-xs'>
                  Preço-sombra: quanto o custo ótimo aumenta se o mínimo do nutriente subir 1 kg.
                </p>

                <ChartContainer config={chartConfig} className='aspect-auto h-52 w-full'>
                  <BarChart data={toyFoods.map(f => ({ name: f.name, kg: toyResult.amounts[f.name] ?? 0 }))}>
                    <CartesianGrid vertical={false} />
                    <XAxis dataKey='name' tickLine={false} axisLine={false} />
                    <YAxis tickLine={false} axisLine={false} width={36} />
                    <ChartTooltip content={<ChartTooltipContent />} />
                    <Bar dataKey='kg' fill='var(--color-kg)' radius={4} />
                  </BarChart>
                </ChartContainer>
              </>
            )}
          </CardContent>
        </Card>
      </div>

      <Card className='mt-6'>
        <CardHeader>
          <CardTitle>Cenários e sensibilidade</CardTitle>
          <CardDescription>
            Como no quadro: cada cenário S<sub>i</sub> é uma linha com os parâmetros e o resultado{' '}
            <strong>Res</strong> (custo ótimo da dieta).
          </CardDescription>
        </CardHeader>
        <CardContent className='space-y-4'>
          <div className='grid gap-4 md:grid-cols-2'>
            {factors.map((factor, i) => (
              <div key={i} className='grid grid-cols-[1fr_5rem_5rem_4.5rem] items-end gap-2'>
                <div className='space-y-1.5'>
                  <Label>Fator {i + 1}</Label>
                  <Select
                    value={factor.target}
                    items={targetItems}
                    onValueChange={value => value && updateFactor(i, { target: value })}
                  >
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

          <Button onClick={generate} disabled={generating || connection !== 'online'}>
            {generating ? 'Gerando…' : 'Gerar cenários'}
          </Button>

          {toySens && (
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
          )}
        </CardContent>
      </Card>
    </>
  )
}

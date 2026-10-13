'use client'

import { useMemo, useState } from 'react'

import Link from 'next/link'

import { PlayIcon, SlidersHorizontalIcon } from 'lucide-react'
import { toast } from 'sonner'
import { Bar, BarChart, CartesianGrid, Cell, XAxis, YAxis } from 'recharts'

import { feedTitle } from '@/components/FeedPicker'
import { finite, heat, JobProgress, NumberInput, PageHeader } from '@/components/shared'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Checkbox } from '@/components/ui/checkbox'
import { ChartContainer, ChartTooltip, ChartTooltipContent, type ChartConfig } from '@/components/ui/chart'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { runJob } from '@/lib/api'
import { nf, shortName, usd } from '@/lib/format'
import type { SensFactor, SensResult } from '@/lib/types'
import { useApp } from '@/providers/AppProvider'
import { simulationBody } from '@/views/CowView'

const METHODS = [
  { value: 'grid', label: 'Grade (todas as combinações)' },
  { value: 'latin', label: 'Hipercubo latino' }
]
const MILK = 'milk_price'
const SECONDS_PER_SIMULATION = 17

interface FactorState {
  on: boolean
  low: number
  high: number
}

const effectsConfig = { spearman: { label: 'Spearman', color: 'var(--chart-1)' } } satisfies ChartConfig
const marginConfig = { margem: { label: 'Margem (US$)', color: 'var(--chart-1)' } } satisfies ChartConfig

export default function SensitivityView() {
  const { connection, selected, feedById, params, sens, setSens } = useApp()
  const [overrides, setOverrides] = useState<Record<string, FactorState>>({})
  const [method, setMethod] = useState('grid')
  const [levels, setLevels] = useState(3)
  const [running, setRunning] = useState(false)
  const [progress, setProgress] = useState({ done: 0, total: 0, status: 'queued' })

  const rows = useMemo(() => {
    const list = Object.entries(selected).map(([id, s]) => ({
      key: id,
      label: feedById[Number(id)] ? feedTitle(feedById[Number(id)]) : id,
      defaults: { on: ['138', '44'].includes(id), low: +(s.price * 0.5).toFixed(3), high: +(s.price * 1.5).toFixed(3) }
    }))

    list.push({
      key: MILK,
      label: 'Preço do leite (US$/kg)',
      defaults: { on: true, low: +(finite(params.milkPrice, 0.45) * 0.8).toFixed(3), high: +(finite(params.milkPrice, 0.45) * 1.2).toFixed(3) }
    })

    return list
  }, [selected, feedById, params.milkPrice])

  const stateOf = (key: string, defaults: FactorState) => overrides[key] ?? defaults
  const patch = (key: string, defaults: FactorState, change: Partial<FactorState>) =>
    setOverrides(prev => ({ ...prev, [key]: { ...(prev[key] ?? defaults), ...change } }))

  const factors: SensFactor[] = rows
    .filter(r => stateOf(r.key, r.defaults).on)
    .map(r => ({ key: r.key, label: r.label, low: finite(stateOf(r.key, r.defaults).low), high: finite(stateOf(r.key, r.defaults).high) }))

  const n = Math.max(2, Math.min(12, finite(levels, 2)))
  const feedFactors = factors.filter(f => f.key !== MILK).length
  const points = factors.length ? (method === 'grid' ? n ** factors.length : n) : 0
  const sims = factors.length ? (method === 'grid' ? n ** feedFactors : n) : 0

  const run = async () => {
    setRunning(true)
    setProgress({ done: 0, total: 0, status: 'queued' })

    try {
      const result = await runJob<SensResult>(
        'sensitivity',
        { ...simulationBody(selected, params), factors, method, n },
        (done, total, status) => setProgress({ done, total, status })
      )

      setSens(result)
      toast.success('Análise concluída.')
    } catch (error) {
      toast.error(error instanceof Error ? error.message.split('\n')[0] : 'Falha na análise')
    } finally {
      setRunning(false)
    }
  }

  return (
    <>
      <PageHeader
        title='Sensibilidade (RuFaS)'
        description='Varia preços de alimentos e do leite, roda o RuFaS para cada combinação e mostra como a margem reage. Cada combinação de preços de alimentos exige uma simulação; o preço do leite só recalcula a receita.'
      />

      <div className='grid items-start gap-6 xl:grid-cols-[23rem_minmax(0,1fr)]'>
        <Card>
          <CardHeader>
            <CardTitle>Fatores</CardTitle>
            <CardDescription>
              Usa os alimentos escolhidos na aba{' '}
              <Link href='/vaca' className='text-primary underline-offset-4 hover:underline'>
                Vaca leiteira
              </Link>
              . Marque o que variar e informe a faixa.
            </CardDescription>
          </CardHeader>
          <CardContent className='space-y-5'>
            <div className='space-y-2'>
              <div className='text-muted-foreground grid grid-cols-[1.25rem_1fr_4.5rem_4.5rem] gap-2 text-[11px]'>
                <span />
                <span>Fator</span>
                <span className='text-right'>De</span>
                <span className='text-right'>Até</span>
              </div>
              {rows.map(r => {
                const s = stateOf(r.key, r.defaults)

                return (
                  <div key={r.key} className='grid grid-cols-[1.25rem_1fr_4.5rem_4.5rem] items-center gap-2'>
                    <Checkbox checked={s.on} aria-label={`Variar ${r.label}`} onCheckedChange={v => patch(r.key, r.defaults, { on: !!v })} />
                    <span className='text-xs leading-snug' title={r.label}>
                      {r.label}
                    </span>
                    <NumberInput className='h-7 px-1.5 text-xs' value={s.low} onChange={v => patch(r.key, r.defaults, { low: v })} aria-label={`${r.label}, mínimo`} />
                    <NumberInput className='h-7 px-1.5 text-xs' value={s.high} onChange={v => patch(r.key, r.defaults, { high: v })} aria-label={`${r.label}, máximo`} />
                  </div>
                )
              })}
            </div>

            <div className='grid grid-cols-2 gap-3'>
              <div className='space-y-1.5'>
                <Label>Método</Label>
                <Select value={method} items={METHODS} onValueChange={v => v && setMethod(v)}>
                  <SelectTrigger className='w-full'>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {METHODS.map(m => (
                      <SelectItem key={m.value} value={m.value}>
                        {m.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className='space-y-1.5'>
                <Label>Níveis / amostras</Label>
                <NumberInput className='h-9' step={1} min={2} value={levels} onChange={setLevels} aria-label='Níveis ou amostras' />
              </div>
            </div>

            <p className='text-muted-foreground text-xs' aria-live='polite'>
              {factors.length
                ? `${points} cenários, até ${sims} simulações do RuFaS (cerca de ${Math.max(1, Math.ceil((sims * SECONDS_PER_SIMULATION) / 60))} min).`
                : 'Marque ao menos um fator.'}
            </p>

            <Button className='w-full' onClick={run} disabled={running || !factors.length || connection !== 'online' || Object.keys(selected).length < 3}>
              <PlayIcon /> {running ? 'Rodando…' : 'Rodar sensibilidade'}
            </Button>
            {running && <JobProgress {...progress} />}
          </CardContent>
        </Card>

        {sens ? (
          <SensResults result={sens} />
        ) : (
          <Card>
            <CardContent className='text-muted-foreground flex flex-col items-center gap-3 py-16 text-center text-sm'>
              <SlidersHorizontalIcon className='size-10 opacity-40' />
              <p className='max-w-sm text-balance'>Defina os fatores e rode a análise.</p>
            </CardContent>
          </Card>
        )}
      </div>
    </>
  )
}

function SensResults({ result }: { result: SensResult }) {
  const names = useMemo(() => Object.fromEntries(result.feeds.map(f => [String(f.id), shortName(f.label, 22)])), [result.feeds])
  const valid = result.rows.map(r => r.Res).filter((v): v is number => v !== null)
  const [min, max] = [Math.min(...valid), Math.max(...valid)]
  const factorColumns = result.columns.filter(c => c !== 'Res')

  const effects = result.effects
    .filter(e => e.spearman !== null)
    .map(e => ({ fator: shortName(e.fator, 26), spearman: e.spearman as number }))
  const marginData = result.rows.filter(r => r.Res !== null).map(r => ({ cenario: r.cenario, margem: r.Res as number }))

  return (
    <div className='min-w-0 space-y-6'>
      <Card>
        <CardHeader>
          <CardTitle>Tabela de cenários</CardTitle>
          <CardDescription>
            Cada linha é um cenário S<sub>i</sub>; <strong>Res</strong> é a margem sobre o custo de alimentação.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead />
                {factorColumns.map(c => (
                  <TableHead key={c} className='text-right'>
                    {shortName(c, 24)}
                  </TableHead>
                ))}
                <TableHead className='text-right'>Res (US$)</TableHead>
                <TableHead className='text-right'>US$/vaca/dia</TableHead>
                <TableHead className='text-right'>Leite perdido</TableHead>
                <TableHead>Ração (kg MS/vaca/dia)</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {result.rows.map(row => (
                <TableRow key={row.cenario}>
                  <TableCell className='font-medium'>{row.cenario}</TableCell>
                  {factorColumns.map(c => (
                    <TableCell key={c} className='text-right tabular-nums'>
                      {nf(row[c] as number, 3)}
                    </TableCell>
                  ))}
                  <TableCell
                    className='text-right font-semibold tabular-nums'
                    style={row.Res === null ? undefined : heat(row.Res, min, max)}
                    title={row.erro}
                  >
                    {row.Res === null ? <span className='text-destructive'>falhou</span> : usd(row.Res)}
                  </TableCell>
                  <TableCell className='text-right tabular-nums'>{row.custo_vaca_dia !== undefined ? nf(row.custo_vaca_dia, 2) : '—'}</TableCell>
                  <TableCell className='text-right tabular-nums'>
                    {(row.reducao_leite ?? 0) > 0.005 ? <span className='text-warning-text'>−{nf(row.reducao_leite, 2)}</span> : '—'}
                  </TableCell>
                  <TableCell className='text-muted-foreground max-w-80 text-xs'>
                    {row.ration
                      ? Object.entries(row.ration)
                          .sort((a, b) => b[1] - a[1])
                          .slice(0, 4)
                          .map(([id, kg]) => `${names[id] ?? id} ${nf(kg, 1)}`)
                          .join(' · ')
                      : row.erro}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      <div className='grid gap-6 2xl:grid-cols-2'>
        <Card>
          <CardHeader>
            <CardTitle>Efeito sobre a margem</CardTitle>
            <CardDescription>Correlação de Spearman entre cada fator e a margem (−1 a +1).</CardDescription>
          </CardHeader>
          <CardContent>
            <ChartContainer config={effectsConfig} className='aspect-auto h-56 w-full'>
              <BarChart data={effects} layout='vertical' margin={{ left: 8 }}>
                <CartesianGrid horizontal={false} />
                <XAxis type='number' domain={[-1, 1]} tickLine={false} axisLine={false} />
                <YAxis type='category' dataKey='fator' tickLine={false} axisLine={false} width={150} fontSize={11} />
                <ChartTooltip content={<ChartTooltipContent />} />
                <Bar dataKey='spearman' radius={4}>
                  {effects.map(e => (
                    <Cell key={e.fator} fill={e.spearman >= 0 ? 'var(--chart-1)' : 'var(--chart-4)'} />
                  ))}
                </Bar>
              </BarChart>
            </ChartContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Margem por cenário</CardTitle>
            <CardDescription>US$ sobre o custo de alimentação.</CardDescription>
          </CardHeader>
          <CardContent>
            <ChartContainer config={marginConfig} className='aspect-auto h-56 w-full'>
              <BarChart data={marginData}>
                <CartesianGrid vertical={false} />
                <XAxis dataKey='cenario' tickLine={false} axisLine={false} />
                <YAxis tickLine={false} axisLine={false} width={56} />
                <ChartTooltip content={<ChartTooltipContent />} />
                <Bar dataKey='margem' fill='var(--color-margem)' radius={4} />
              </BarChart>
            </ChartContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

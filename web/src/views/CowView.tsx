'use client'

import { useMemo, useState } from 'react'

import { PlayIcon, WheatIcon } from 'lucide-react'
import { toast } from 'sonner'
import { Bar, BarChart, CartesianGrid, Line, LineChart, XAxis, YAxis } from 'recharts'

import FeedPicker from '@/components/FeedPicker'
import { finite, JobProgress, KpiCard, NumberInput, PageHeader } from '@/components/shared'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import {
  ChartContainer,
  ChartLegend,
  ChartLegendContent,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig
} from '@/components/ui/chart'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Table, TableBody, TableCell, TableFooter, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { runJob } from '@/lib/api'
import { nf, shortName, usd } from '@/lib/format'
import type { SimResult } from '@/lib/types'
import { useApp } from '@/providers/AppProvider'

const YEARS = [
  { value: '1', label: '1 ano' },
  { value: '2', label: '2 anos' }
]

const seriesColor = (index: number) => `var(--chart-${(index % 8) + 1})`

export function simulationBody(
  selected: ReturnType<typeof useApp>['selected'],
  params: ReturnType<typeof useApp>['params']
) {
  const prices: Record<string, number> = {}
  const limits: Record<string, [number, number]> = {}

  for (const [id, s] of Object.entries(selected)) {
    prices[id] = finite(s.price, 0.3)
    limits[id] = [finite(s.min), finite(s.max, 100)]
  }

  return {
    feeds: Object.keys(selected).map(Number),
    prices,
    limits,
    milk_price: finite(params.milkPrice, 0.45),
    years: params.years,
    max_milk_reduction: finite(params.maxReduction, 5)
  }
}

export default function CowView() {
  const { connection, selected, params, setParams, sim, setSim } = useApp()
  const [running, setRunning] = useState(false)
  const [progress, setProgress] = useState({ done: 0, total: 0, status: 'queued' })

  const run = async () => {
    if (Object.keys(selected).length < 3) {
      toast.error('Selecione pelo menos 3 alimentos (um volumoso, um concentrado e um mineral).')

      return
    }

    setRunning(true)
    setProgress({ done: 0, total: 0, status: 'queued' })

    try {
      const result = await runJob<SimResult>('simulate', simulationBody(selected, params), (done, total, status) =>
        setProgress({ done, total, status })
      )

      setSim(result)
      toast.success('Simulação concluída.')
    } catch (error) {
      toast.error(error instanceof Error ? error.message.split('\n')[0] : 'Falha na simulação')
    } finally {
      setRunning(false)
    }
  }

  return (
    <>
      <PageHeader
        title='Vaca leiteira (RuFaS)'
        description='Escolha os alimentos, informe preços e limites e simule com o RuFaS (padrão NRC 2001). O otimizador do RuFaS formula a ração de custo mínimo e o sistema calcula custo, leite e margem.'
      />

      <div className='grid items-start gap-6 xl:grid-cols-[23rem_minmax(0,1fr)]'>
        <Card>
          <CardHeader>
            <CardTitle>Cenário</CardTitle>
            <CardDescription>Preços em US$/kg de matéria seca; limites em kg de MS por vaca por dia.</CardDescription>
          </CardHeader>
          <CardContent className='space-y-5'>
            <div className='grid grid-cols-2 gap-3'>
              <div className='space-y-1.5'>
                <Label>Preço do leite (US$/kg)</Label>
                <NumberInput
                  className='h-9'
                  value={params.milkPrice}
                  onChange={v => setParams({ milkPrice: v })}
                  aria-label='Preço do leite em dólares por quilo'
                />
              </div>
              <div className='space-y-1.5'>
                <Label>Período simulado</Label>
                <Select
                  value={String(params.years)}
                  items={YEARS}
                  onValueChange={v => v && setParams({ years: Number(v) })}
                >
                  <SelectTrigger className='w-full'>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {YEARS.map(y => (
                      <SelectItem key={y.value} value={y.value}>
                        {y.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className='space-y-1.5'>
              <Label>Redução máxima de leite tolerada (kg/vaca/dia)</Label>
              <NumberInput
                className='h-9'
                step={0.25}
                min={0}
                value={params.maxReduction}
                onChange={v => setParams({ maxReduction: v })}
                aria-label='Redução máxima de leite'
              />
              <p className='text-muted-foreground text-xs'>
                Se a ração não atende às exigências, o RuFaS reduz o leite (0,25 kg por tentativa) até este limite; acima
                dele a simulação aborta.
              </p>
            </div>

            <FeedPicker />

            <Button className='w-full' onClick={run} disabled={running || connection !== 'online'}>
              <PlayIcon /> {running ? 'Simulando…' : 'Simular com o RuFaS'}
            </Button>
            {running && <JobProgress {...progress} />}
          </CardContent>
        </Card>

        {sim ? (
          <Results sim={sim} />
        ) : (
          <Card>
            <CardContent className='text-muted-foreground flex flex-col items-center gap-3 py-16 text-center text-sm'>
              <WheatIcon className='size-10 opacity-40' />
              <p className='max-w-sm text-balance'>
                Escolha os alimentos e clique em “Simular com o RuFaS”. Cada simulação leva de 30 a 60 segundos.
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </>
  )
}

function Results({ sim }: { sim: SimResult }) {
  const s = sim.summary
  const feedIds = useMemo(
    () =>
      sim.feeds
        .map(f => f.id)
        .filter(id => sim.intervals.ration.some(r => (r[String(id)] ?? 0) > 1e-3))
        // o ingrediente principal fica com a cor primária
        .sort((a, b) => (sim.average_ration[String(b)] ?? 0) - (sim.average_ration[String(a)] ?? 0)),
    [sim]
  )
  const labelById = useMemo(() => Object.fromEntries(sim.feeds.map(f => [f.id, f.label])), [sim])
  const priceById = useMemo(() => Object.fromEntries(sim.feeds.map(f => [f.id, f.price ?? 0])), [sim])

  const avgCows = sim.daily.milking_cows.reduce((a, b) => a + b, 0) / Math.max(sim.daily.milking_cows.length, 1)
  const milkPerCow = s.leite_kg / (avgCows * Math.max(sim.daily.day.length, 1))

  const rationConfig = Object.fromEntries(
    feedIds.map((id, i) => [`f${id}`, { label: shortName(labelById[id], 30), color: seriesColor(i) }])
  ) satisfies ChartConfig
  const rationData = sim.intervals.day.map((day, i) => ({
    day: `dia ${day}`,
    ...Object.fromEntries(feedIds.map(id => [`f${id}`, sim.intervals.ration[i][String(id)] ?? 0]))
  }))

  const requirementData = sim.intervals.day.map((day, i) => ({
    day: `dia ${day}`,
    nel: sim.intervals.requirements[i]?.NEl_requirement,
    dmi: sim.intervals.requirements[i]?.DMIest_requirement,
    mp: sim.intervals.requirements[i]?.MP_requirement
  }))
  const requirementConfig = {
    nel: { label: 'NEL exigida (Mcal/dia)', color: 'var(--chart-1)' },
    dmi: { label: 'DMI estimado (kg/dia)', color: 'var(--chart-2)' },
    mp: { label: 'Proteína metabolizável (g/dia)', color: 'var(--chart-3)' }
  } satisfies ChartConfig

  const milkData = sim.daily.day.map((day, i) => ({
    day,
    milk: sim.daily.milk_kg[i],
    cows: sim.daily.milking_cows[i]
  }))
  const milkConfig = {
    milk: { label: 'Leite do rebanho (kg/dia)', color: 'var(--chart-1)' },
    cows: { label: 'Vacas em lactação', color: 'var(--chart-4)' }
  } satisfies ChartConfig

  const total = Object.values(sim.average_ration).reduce((a, b) => a + b, 0)
  const tableRows = Object.entries(sim.average_ration)
    .filter(([, kg]) => kg > 1e-3)
    .sort((a, b) => b[1] - a[1])

  return (
    <div className='min-w-0 space-y-6'>
      <div className='grid gap-3 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4'>
        <KpiCard tone='primary' label='Margem sobre custo de alimentação' value={usd(s.margem)} />
        <KpiCard label='Receita do leite' value={usd(s.receita)} />
        <KpiCard label='Custo de alimentação (rebanho)' value={usd(s.custo_alimentacao)} />
        <KpiCard label='Custo da ração, vaca em lactação' value={`${usd(s.custo_vaca_dia, 2)}/dia`} />
        <KpiCard label='Leite por vaca' value={`${nf(milkPerCow, 1)} kg/dia`} />
        <KpiCard label='Leite total' value={`${nf(s.leite_kg / 1000, 0)} t`} />
        {s.reducao_leite > 0.005 && (
          <KpiCard
            tone='warning'
            label='Leite perdido por ração insuficiente'
            value={`−${nf(s.reducao_leite, 2)} kg/vaca/dia`}
            hint='O RuFaS reduziu o leite para fechar a ração.'
          />
        )}
      </div>

      {s.reducao_leite > 0.005 && (
        <Alert>
          <AlertTitle>A ração não atendeu a todas as exigências</AlertTitle>
          <AlertDescription>
            Para continuar a simulação, o RuFaS reduziu a produção de leite em média {nf(s.reducao_leite, 2)} kg por
            vaca por dia (limite configurado: {nf(s.max_reducao, 2)}). Revise os alimentos, os preços e os limites.
          </AlertDescription>
        </Alert>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Ração das vacas em lactação</CardTitle>
          <CardDescription>
            kg de matéria seca por vaca por dia, a cada 30 dias de simulação (formulada pelo otimizador do RuFaS).
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ChartContainer config={rationConfig} className='aspect-auto h-80 w-full'>
            <BarChart data={rationData}>
              <CartesianGrid vertical={false} />
              <XAxis dataKey='day' tickLine={false} axisLine={false} interval={0} fontSize={11} />
              <YAxis tickLine={false} axisLine={false} width={36} />
              <ChartTooltip content={<ChartTooltipContent />} />
              <ChartLegend content={<ChartLegendContent />} />
              {feedIds.map(id => (
                <Bar key={id} dataKey={`f${id}`} stackId='ration' fill={`var(--color-f${id})`} />
              ))}
            </BarChart>
          </ChartContainer>
        </CardContent>
      </Card>

      <div className='grid gap-6 2xl:grid-cols-2'>
        <Card>
          <CardHeader>
            <CardTitle>Composição média</CardTitle>
            <CardDescription>Média dos intervalos de 30 dias.</CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Alimento</TableHead>
                  <TableHead className='text-right'>kg MS/dia</TableHead>
                  <TableHead className='text-right'>% MS</TableHead>
                  <TableHead className='text-right'>US$/dia</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {tableRows.map(([id, kg]) => (
                  <TableRow key={id}>
                    <TableCell className='max-w-56 truncate' title={labelById[Number(id)]}>
                      <span
                        className='mr-2 inline-block size-2.5 rounded-sm align-middle'
                        style={{ backgroundColor: seriesColor(Math.max(feedIds.indexOf(Number(id)), 0)) }}
                      />
                      {shortName(labelById[Number(id)] ?? id, 34)}
                    </TableCell>
                    <TableCell className='text-right tabular-nums'>{nf(kg, 2)}</TableCell>
                    <TableCell className='text-right tabular-nums'>{nf((100 * kg) / total, 1)}%</TableCell>
                    <TableCell className='text-right tabular-nums'>{nf(kg * (priceById[Number(id)] ?? 0), 2)}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
              <TableFooter>
                <TableRow>
                  <TableCell className='font-semibold'>Total</TableCell>
                  <TableCell className='text-right font-semibold tabular-nums'>{nf(total, 2)}</TableCell>
                  <TableCell className='text-right tabular-nums'>100%</TableCell>
                  <TableCell className='text-right font-semibold tabular-nums'>{nf(s.custo_vaca_dia, 2)}</TableCell>
                </TableRow>
              </TableFooter>
            </Table>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Exigências (NRC 2001)</CardTitle>
            <CardDescription>Energia e consumo (eixo esquerdo) e proteína metabolizável (direito).</CardDescription>
          </CardHeader>
          <CardContent>
            <ChartContainer config={requirementConfig} className='aspect-auto h-72 w-full'>
              <LineChart data={requirementData}>
                <CartesianGrid vertical={false} />
                <XAxis dataKey='day' tickLine={false} axisLine={false} interval={1} fontSize={11} />
                <YAxis yAxisId='left' tickLine={false} axisLine={false} width={36} domain={['auto', 'auto']} />
                <YAxis
                  yAxisId='right'
                  orientation='right'
                  tickLine={false}
                  axisLine={false}
                  width={44}
                  domain={['auto', 'auto']}
                />
                <ChartTooltip content={<ChartTooltipContent />} />
                <ChartLegend content={<ChartLegendContent />} />
                <Line yAxisId='left' dataKey='nel' stroke='var(--color-nel)' strokeWidth={2} dot={false} />
                <Line yAxisId='left' dataKey='dmi' stroke='var(--color-dmi)' strokeWidth={2} dot={false} />
                <Line yAxisId='right' dataKey='mp' stroke='var(--color-mp)' strokeWidth={2} dot={false} />
              </LineChart>
            </ChartContainer>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Leite do rebanho</CardTitle>
          <CardDescription>Produção diária e número de vacas em lactação.</CardDescription>
        </CardHeader>
        <CardContent>
          <ChartContainer config={milkConfig} className='aspect-auto h-64 w-full'>
            <LineChart data={milkData}>
              <CartesianGrid vertical={false} />
              <XAxis dataKey='day' tickLine={false} axisLine={false} minTickGap={32} />
              <YAxis yAxisId='left' tickLine={false} axisLine={false} width={44} domain={['auto', 'auto']} />
              <YAxis
                yAxisId='right'
                orientation='right'
                tickLine={false}
                axisLine={false}
                width={36}
                domain={['auto', 'auto']}
              />
              <ChartTooltip content={<ChartTooltipContent />} />
              <ChartLegend content={<ChartLegendContent />} />
              <Line yAxisId='left' dataKey='milk' stroke='var(--color-milk)' strokeWidth={2} dot={false} />
              <Line
                yAxisId='right'
                dataKey='cows'
                stroke='var(--color-cows)'
                strokeWidth={1.5}
                strokeDasharray='4 3'
                dot={false}
              />
            </LineChart>
          </ChartContainer>
        </CardContent>
      </Card>
    </div>
  )
}

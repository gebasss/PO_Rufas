'use client'

import { useMemo } from 'react'

import { CoinsIcon, DropletsIcon, GaugeIcon, MilkIcon, TrendingUpIcon, WalletIcon, WheatIcon } from 'lucide-react'
import { CartesianGrid, Line, LineChart, XAxis, YAxis } from 'recharts'

import { DivergingBars, HighlightBars, SeriesLegend, TimeSeries } from '@/components/charts'
import ChartCard from '@/components/ChartCard'
import ExportButtons from '@/components/ExportButtons'
import { KpiCard } from '@/components/shared'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import {
  ChartContainer,
  ChartLegend,
  ChartLegendContent,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig
} from '@/components/ui/chart'
import { Tabs, TabsList, TabsPanel, TabsTab } from '@/components/ui/tabs'
import { Table, TableBody, TableCell, TableFooter, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { nf, shortName, signedPct, usd } from '@/lib/format'
import type { SimResult } from '@/lib/types'
import BalanceCard, { BalanceTable } from '@/views/cow/BalanceCard'
import ChecksCard, { ChecksAlert } from '@/views/cow/ChecksCard'

const seriesColor = (index: number) => `var(--chart-${(index % 8) + 1})`

/** Acima disso o eixo do balanço corta a barra (o rótulo continua mostrando o valor real). */
const BALANCE_CLIP = 150

export default function Results({ sim, stale = false }: { sim: SimResult; stale?: boolean }) {
  const s = sim.summary
  const labelById = useMemo(() => Object.fromEntries(sim.feeds.map(f => [f.id, f.label])), [sim])
  const priceById = useMemo(() => Object.fromEntries(sim.feeds.map(f => [f.id, f.price ?? 0])), [sim])
  const feedIds = useMemo(
    () =>
      sim.feeds
        .map(f => f.id)
        .filter(id => sim.intervals.ration.some(r => (r[String(id)] ?? 0) > 1e-3))
        .sort((a, b) => (sim.average_ration[String(b)] ?? 0) - (sim.average_ration[String(a)] ?? 0)),
    [sim]
  )

  const avgCows = sim.daily.milking_cows.reduce((a, b) => a + b, 0) / Math.max(sim.daily.milking_cows.length, 1)
  const milkPerCow = s.leite_kg / (avgCows * Math.max(sim.daily.day.length, 1))
  // Séries da própria simulação para os mini gráficos dos cartões (a cada 5 dias, para ficarem leves).
  const trends = useMemo(() => {
    const every = (values: number[], step = 5) => values.filter((_, i) => i % step === 0 && Number.isFinite(values[i]))
    const { milk_kg: milk, milking_cows: cows } = sim.daily

    return {
      milk: every(milk),
      revenue: every(milk.map(kg => kg * s.milk_price)),
      milkPerCow: every(milk.map((kg, i) => kg / Math.max(cows[i], 1))),
      cowCost: sim.intervals.cost_per_cow_day,
      herdCost: sim.intervals.cost_per_cow_day.map((cost, i) => cost * (sim.intervals.cows[i] ?? 0))
    }
  }, [sim, s.milk_price])

  const total = Object.values(sim.average_ration).reduce((a, b) => a + b, 0)
  const rationRows = Object.entries(sim.average_ration)
    .filter(([, kg]) => kg > 1e-3)
    .sort((a, b) => b[1] - a[1])
  const rationBars = rationRows.slice(0, 8).map(([id, kg]) => ({ name: shortName(labelById[Number(id)] ?? id, 26), value: kg }))

  const balanceBars = (sim.balance ?? [])
    .filter(row => row.kind === 'surplus' && row.margin_pct != null)
    .map(row => ({
      name: shortName(row.label, 24),
      value: row.margin_pct as number,
      bar: Math.min(Math.max(row.margin_pct as number, -100), BALANCE_CLIP)
    }))

  const milkData = sim.daily.day.map((day, i) => ({ day, milk: sim.daily.milk_kg[i], cows: sim.daily.milking_cows[i] }))
  const costData = sim.intervals.day.map((day, i) => ({ day: `dia ${day}`, cost: sim.intervals.cost_per_cow_day[i] }))
  const rationSeries = feedIds.map((id, i) => ({
    key: `f${id}`,
    label: shortName(labelById[id] ?? String(id), 30),
    color: seriesColor(i)
  }))
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

  const compositionTable = (
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
        {rationRows.map(([id, kg]) => (
          <TableRow key={id}>
            <TableCell className='max-w-56 truncate' title={labelById[Number(id)]}>
              <span
                className='mr-2 inline-block size-2.5 rounded-full align-middle'
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
  )

  const costTable = (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Intervalo</TableHead>
          <TableHead className='text-right'>Custo (US$/vaca/dia)</TableHead>
          <TableHead className='text-right'>Vacas</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {costData.map((row, i) => (
          <TableRow key={row.day}>
            <TableCell>{row.day}</TableCell>
            <TableCell className='text-right tabular-nums'>{nf(row.cost, 2)}</TableCell>
            <TableCell className='text-right tabular-nums'>{nf(sim.intervals.cows[i] ?? 0, 0)}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )

  const rationTimeTable = (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Intervalo</TableHead>
          {rationSeries.map(item => (
            <TableHead key={item.key} className='text-right'>
              {shortName(item.label, 14)}
            </TableHead>
          ))}
        </TableRow>
      </TableHeader>
      <TableBody>
        {rationData.map(row => (
          <TableRow key={row.day}>
            <TableCell>{row.day}</TableCell>
            {rationSeries.map(item => (
              <TableCell key={item.key} className='text-right tabular-nums'>
                {nf(Number(row[item.key as keyof typeof row]), 1)}
              </TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )

  return (
    <div id='resultados' className='min-w-0 scroll-mt-24'>
      <Tabs defaultValue='overview'>
        <div className='flex flex-wrap items-center justify-between gap-3'>
          <TabsList>
            <TabsTab value='overview'>
              <GaugeIcon /> Visão geral
            </TabsTab>
            <TabsTab value='ration'>
              <WheatIcon /> Ração
            </TabsTab>
            <TabsTab value='nutrition'>
              <DropletsIcon /> Nutrição
            </TabsTab>
          </TabsList>
          <ExportButtons screen='simulation' data={sim} meta={{ standard: 'NRC 2001' }} />
        </div>

        <div className={stale ? 'space-y-6 opacity-60 transition-opacity' : 'space-y-6 transition-opacity'}>
          {stale && (
            <p className='text-muted-foreground text-sm' role='status'>
              Os parâmetros mudaram desde esta simulação. Clique em Executar para atualizar os resultados.
            </p>
          )}

          <TabsPanel value='overview'>
            <div className='grid gap-3 sm:grid-cols-2 2xl:grid-cols-3'>
              <KpiCard tone='primary' icon={TrendingUpIcon} label='Margem sobre custo de alimentação' value={usd(s.margem)} />
              <KpiCard icon={WalletIcon} color='info' label='Receita do leite' value={usd(s.receita)} trend={trends.revenue} />
              <KpiCard icon={WheatIcon} color='violet' label='Custo de alimentação (rebanho)' value={usd(s.custo_alimentacao)} trend={trends.herdCost} />
              <KpiCard icon={CoinsIcon} color='warning' label='Custo da ração, vaca em lactação' value={`${usd(s.custo_vaca_dia, 2)}/dia`} trend={trends.cowCost} />
              <KpiCard icon={MilkIcon} color='info' label='Leite por vaca' value={`${nf(milkPerCow, 1)} kg/dia`} trend={trends.milkPerCow} />
              <KpiCard icon={DropletsIcon} label='Leite total' value={`${nf(s.leite_kg / 1000, 0)} t`} trend={trends.milk} />
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
            {sim.checks && sim.checks.length > 0 && <ChecksAlert checks={sim.checks} />}

            <div className='grid gap-6 2xl:grid-cols-2'>
              <ChartCard
                title='Ração média'
                description='kg de matéria seca por vaca por dia; o ingrediente principal em verde vivo.'
                chart={<HighlightBars layout='vertical' data={rationBars} highlight={rationBars[0]?.name} format={value => nf(value, 1)} height={Math.max(220, rationBars.length * 40 + 30)} />}
                table={compositionTable}
              />
              {balanceBars.length > 0 && (
                <ChartCard
                  title='Balanço nutricional'
                  description={`Oferta em relação à exigência (%); barras limitadas a +${BALANCE_CLIP}%, o rótulo mostra o valor real.`}
                  chart={<DivergingBars data={balanceBars} format={value => signedPct(value, 0)} domain={[-100, BALANCE_CLIP]} height={Math.max(220, balanceBars.length * 44 + 30)} />}
                  table={<BalanceTable rows={sim.balance ?? []} />}
                />
              )}
            </div>

            <ChartCard
              title='Leite do rebanho'
              description='Produção diária (área) e vacas em lactação (linha tracejada, eixo direito).'
              chart={
                <>
                  <TimeSeries
                    data={milkData}
                    xKey='day'
                    series={[
                      { key: 'milk', label: 'Leite do rebanho (kg/dia)', color: 'var(--chart-1)' },
                      { key: 'cows', label: 'Vacas em lactação', color: 'var(--chart-3)', kind: 'line', axis: 'right', dashed: true }
                    ]}
                    format={value => nf(value, 0)}
                    height={260}
                  />
                  <SeriesLegend
                    series={[
                      { label: 'Leite do rebanho (kg/dia)', color: 'var(--chart-1)' },
                      { label: 'Vacas em lactação', color: 'var(--chart-3)' }
                    ]}
                  />
                </>
              }
            />

            <ChartCard
              title='Custo da ração por vaca'
              description='US$ por vaca em lactação por dia, a cada intervalo de 30 dias.'
              chart={
                <TimeSeries
                  data={costData}
                  xKey='day'
                  series={[{ key: 'cost', label: 'Custo (US$/vaca/dia)', color: 'var(--chart-2)' }]}
                  format={value => nf(value, 2)}
                  height={220}
                />
              }
              table={costTable}
            />
          </TabsPanel>

          <TabsPanel value='ration'>
            <ChartCard
              title='Ração ao longo do tempo'
              description='kg de matéria seca por vaca por dia, a cada 30 dias de simulação (formulada pelo otimizador do RuFaS).'
              chart={
                <>
                  <TimeSeries data={rationData} xKey='day' series={rationSeries} stacked format={value => nf(value, 0)} height={300} />
                  <SeriesLegend series={rationSeries} />
                </>
              }
              table={rationTimeTable}
            />
            <Card>
              <CardHeader>
                <CardTitle>Composição média</CardTitle>
                <CardDescription>Média dos intervalos de 30 dias.</CardDescription>
              </CardHeader>
              <CardContent>{compositionTable}</CardContent>
            </Card>
          </TabsPanel>

          <TabsPanel value='nutrition'>
            {sim.checks && sim.checks.length > 0 && <ChecksCard checks={sim.checks} />}
            {sim.balance && sim.balance.length > 0 && <BalanceCard rows={sim.balance} />}
            <ChartCard
              title='Exigências (NRC 2001)'
              description='Energia e consumo (eixo esquerdo) e proteína metabolizável (direito).'
              chart={
                <ChartContainer config={requirementConfig} className='aspect-auto h-72 w-full'>
                  <LineChart data={requirementData}>
                    <CartesianGrid vertical={false} />
                    <XAxis dataKey='day' tickLine={false} axisLine={false} interval={1} fontSize={11} />
                    <YAxis yAxisId='left' tickLine={false} axisLine={false} width={36} domain={['auto', 'auto']} />
                    <YAxis yAxisId='right' orientation='right' tickLine={false} axisLine={false} width={44} domain={['auto', 'auto']} />
                    <ChartTooltip content={<ChartTooltipContent />} />
                    <ChartLegend content={<ChartLegendContent />} />
                    <Line yAxisId='left' dataKey='nel' stroke='var(--color-nel)' strokeWidth={2} dot={false} />
                    <Line yAxisId='left' dataKey='dmi' stroke='var(--color-dmi)' strokeWidth={2} dot={false} />
                    <Line yAxisId='right' dataKey='mp' stroke='var(--color-mp)' strokeWidth={2} dot={false} />
                  </LineChart>
                </ChartContainer>
              }
            />
          </TabsPanel>
        </div>
      </Tabs>
    </div>
  )
}

'use client'

import { useMemo } from 'react'

import { CoinsIcon, DropletsIcon, GaugeIcon, MilkIcon, StarIcon, TrendingUpIcon, WalletIcon, WheatIcon } from 'lucide-react'

import { DivergingBars, HighlightBars, SeriesLegend, TimeSeries, type SeriesSpec } from '@/components/charts'
import ChartCard from '@/components/ChartCard'
import ExportButtons from '@/components/ExportButtons'
import { KpiCard } from '@/components/shared'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsList, TabsPanel, TabsTab } from '@/components/ui/tabs'
import { Table, TableBody, TableCell, TableFooter, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { nf, shortName, signedPct, usd } from '@/lib/format'
import { shortDate } from '@/lib/history'
import type { RunMeta, SimResult } from '@/lib/types'
import BalanceCard, { BalanceTable } from '@/views/cow/BalanceCard'
import ChecksCard, { ChecksAlert } from '@/views/cow/ChecksCard'

const seriesColor = (index: number) => `var(--chart-${(index % 8) + 1})`

/** O gráfico empilhado mostra no máximo este número de faixas; os alimentos menores se somam em "Outros". */
const MAX_RATION_BANDS = 8
const OTHERS_COLOR = 'var(--chart-dim)'

/** Acima disso o eixo do balanço corta a barra (o rótulo continua mostrando o valor real). */
const BALANCE_CLIP = 150

interface Props {
  sim: SimResult
  stale?: boolean
  /** Cenário-base das simulações (D3): os indicadores mostram a variação em relação a ele. */
  base?: RunMeta | null
  /** Marca a execução desta tela como o cenário-base. */
  onSetBase?: () => void
}

/** Totais do rebanho: só se comparam com o cenário-base quando os dois têm o mesmo número de vacas. */
const HERD_TOTALS = new Set(['margem', 'receita', 'custo_alimentacao', 'leite_kg'])

export default function Results({ sim, stale = false, base = null, onSetBase }: Props) {
  const s = sim.summary
  const isBase = base !== null && base.id === sim.run_id
  const herdSize = Number(s.cow_num ?? 100)
  const baseHerd = Number(base?.summary.cow_num ?? 100)
  const sameHerd = herdSize === baseHerd
  /** Variação percentual em relação ao cenário-base (nada se não há base, se esta é a base ou se o valor não existe). */
  const delta = (key: string, current: number) => {
    const reference = base && !isBase && (sameHerd || !HERD_TOTALS.has(key)) ? base.summary[key] : null

    return typeof reference === 'number' && reference !== 0 ? ((current - reference) / Math.abs(reference)) * 100 : undefined
  }
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
  // Tabela: todos os alimentos. Gráfico: até 8 faixas (as de maior consumo médio) e o resto somado em "Outros".
  const rationSeries = feedIds.map((id, i) => ({
    key: `f${id}`,
    label: shortName(labelById[id] ?? String(id), 30),
    color: seriesColor(i)
  }))
  const grouped = feedIds.length > MAX_RATION_BANDS
  const bandIds = grouped ? feedIds.slice(0, MAX_RATION_BANDS - 1) : feedIds
  const otherIds = grouped ? feedIds.slice(MAX_RATION_BANDS - 1) : []
  const bandSeries: SeriesSpec[] = [
    ...rationSeries.slice(0, bandIds.length),
    ...(grouped ? [{ key: 'others', label: `Outros (${otherIds.length} alimentos)`, color: OTHERS_COLOR }] : [])
  ]
  const rationData = sim.intervals.day.map((day, i) => ({
    day: `dia ${day}`,
    ...Object.fromEntries(feedIds.map(id => [`f${id}`, sim.intervals.ration[i][String(id)] ?? 0])),
    others: otherIds.reduce((sum, id) => sum + (sim.intervals.ration[i][String(id)] ?? 0), 0)
  }))
  /** Cor do alimento no gráfico e na tabela de composição (cinza para os que entram em "Outros"). */
  const colorOf = (id: number) => (otherIds.includes(id) ? OTHERS_COLOR : seriesColor(Math.max(feedIds.indexOf(id), 0)))

  const requirementData = sim.intervals.day.map((day, i) => ({
    day: `dia ${day}`,
    nel: sim.intervals.requirements[i]?.NEl_requirement,
    dmi: sim.intervals.requirements[i]?.DMIest_requirement,
    mp: sim.intervals.requirements[i]?.MP_requirement
  }))
  const requirementSeries: SeriesSpec[] = [
    { key: 'nel', label: 'NEL exigida (Mcal/dia)', color: 'var(--chart-1)', kind: 'line' },
    { key: 'dmi', label: 'DMI estimado (kg/dia)', color: 'var(--chart-3)', kind: 'line' },
    { key: 'mp', label: 'Proteína metabolizável (g/dia)', color: 'var(--chart-5)', kind: 'line', axis: 'right' }
  ]
  const requirementTable = (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Dia</TableHead>
          {requirementSeries.map(item => (
            <TableHead key={item.key} className='text-right'>
              {item.label}
            </TableHead>
          ))}
        </TableRow>
      </TableHeader>
      <TableBody>
        {requirementData.map(row => (
          <TableRow key={row.day}>
            <TableCell>{row.day}</TableCell>
            <TableCell className='text-right tabular-nums'>{nf(row.nel, 1)}</TableCell>
            <TableCell className='text-right tabular-nums'>{nf(row.dmi, 1)}</TableCell>
            <TableCell className='text-right tabular-nums'>{nf(row.mp, 0)}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )

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
                style={{ backgroundColor: colorOf(Number(id)) }}
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

        {sim.run_id && (
          <div className='text-muted-foreground flex flex-wrap items-center gap-x-3 gap-y-2 text-sm'>
            {onSetBase && !isBase && (
              <Button variant='outline' size='sm' onClick={onSetBase}>
                <StarIcon /> Definir como cenário-base
              </Button>
            )}
            <span>
              {isBase
                ? 'Esta simulação é o cenário-base.'
                : base
                  ? `Variações em relação ao cenário-base: ${base.title} (${shortDate(base.created)}).${sameHerd ? '' : ` O base tem ${baseHerd} vacas e esta simulação, ${herdSize}: os totais do rebanho não são comparados.`}`
                  : 'Sem cenário-base: marque uma simulação com a estrela para ver as variações dos indicadores.'}
            </span>
          </div>
        )}

        <div className={stale ? 'space-y-6 opacity-60 transition-opacity' : 'space-y-6 transition-opacity'}>
          {stale && (
            <p className='text-muted-foreground text-sm' role='status'>
              Os parâmetros mudaram desde esta simulação. Clique em Executar para atualizar os resultados.
            </p>
          )}

          <TabsPanel value='overview'>
            <div className='grid gap-3 sm:grid-cols-2 2xl:grid-cols-3'>
              <KpiCard tone='primary' icon={TrendingUpIcon} label='Margem sobre custo de alimentação' value={usd(s.margem)} delta={delta('margem', s.margem)} />
              <KpiCard icon={WalletIcon} color='info' label='Receita do leite' value={usd(s.receita)} delta={delta('receita', s.receita)} trend={trends.revenue} />
              <KpiCard icon={WheatIcon} color='violet' label='Custo de alimentação (rebanho)' value={usd(s.custo_alimentacao)} delta={delta('custo_alimentacao', s.custo_alimentacao)} better='down' trend={trends.herdCost} />
              <KpiCard icon={CoinsIcon} color='warning' label='Custo da ração, vaca em lactação' value={`${usd(s.custo_vaca_dia, 2)}/dia`} delta={delta('custo_vaca_dia', s.custo_vaca_dia)} better='down' trend={trends.cowCost} />
              <KpiCard icon={MilkIcon} color='info' label='Leite por vaca' value={`${nf(milkPerCow, 1)} kg/dia`} trend={trends.milkPerCow} />
              <KpiCard icon={DropletsIcon} label='Leite total' value={`${nf(s.leite_kg / 1000, 0)} t`} delta={delta('leite_kg', s.leite_kg)} trend={trends.milk} />
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
              description='kg de matéria seca por vaca por dia, a cada 30 dias de simulação (formulada pelo otimizador do RuFaS). Cada faixa é um alimento e sua espessura é a quantidade; a linha de cima é o consumo total.'
              chart={
                <>
                  <TimeSeries
                    data={rationData}
                    xKey='day'
                    series={bandSeries}
                    stacked
                    format={value => nf(value, 0)}
                    tooltipFormat={value => nf(value, 2)}
                    totalLabel='Total da ração'
                    height={300}
                  />
                  <SeriesLegend series={bandSeries} />
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
                <>
                  <TimeSeries
                    data={requirementData}
                    xKey='day'
                    series={requirementSeries}
                    format={value => nf(value, 0)}
                    rightFormat={value => nf(value, 0)}
                    height={288}
                  />
                  <SeriesLegend series={requirementSeries} />
                </>
              }
              table={requirementTable}
            />
          </TabsPanel>
        </div>
      </Tabs>
    </div>
  )
}

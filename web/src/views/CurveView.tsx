'use client'

import { useEffect, useMemo, useState } from 'react'

import { CalendarClockIcon, MilkIcon } from 'lucide-react'

import { SeriesLegend, TimeSeries, type SeriesSpec } from '@/components/charts'
import ChartCard from '@/components/ChartCard'
import { EmptyState, ResultsSkeleton } from '@/components/EmptyState'
import { finite, KpiCard, NumberInput, PageHeader, type AccentColor } from '@/components/shared'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { api } from '@/lib/api'
import { nf } from '@/lib/format'
import type { LactationInfo, Wood } from '@/lib/types'
import { useApp } from '@/providers/AppProvider'

const PARITY_LABEL: Record<string, string> = { '1': '1ª lactação', '2': '2ª lactação', '3': '3ª ou mais' }
/** Uma cor por paridade; o âmbar e o vermelho ficam para a secagem e o parto. */
const PARITY_COLOR = ['var(--chart-1)', 'var(--chart-3)', 'var(--chart-5)']
const PARITY_ACCENT: AccentColor[] = ['brand', 'info', 'violet']
const LACTATION_DAYS = 305
const TABLE_STEP = 30

const woodYield = (day: number, p: Wood) => p.l * Math.pow(day, p.m) * Math.exp(-p.n * day)
const parityName = (p: string) => PARITY_LABEL[p] ?? `paridade ${p}`

export default function CurveView() {
  const { sim, connection } = useApp()
  const [reference, setReference] = useState<LactationInfo | null>(null)
  const [pev, setPev] = useState(60)
  const [gestation, setGestation] = useState(270)
  const [dry, setDry] = useState(60)

  useEffect(() => {
    if (connection === 'online') api.lactation().then(setReference).catch(() => undefined)
  }, [connection])

  const fromRufas = !!sim?.lactation.wood_from_rufas
  const wood = (sim?.lactation.wood ?? reference?.wood) as Record<string, Wood> | undefined

  const pevDays = Math.round(finite(pev))
  const calving = pevDays + Math.round(finite(gestation))
  const dryDay = calving - Math.round(finite(dry))
  const maxDay = Math.max(330, calving + 15)

  const parities = useMemo(() => Object.keys(wood ?? {}), [wood])
  const series: SeriesSpec[] = parities.map((p, i) => ({ key: `p${p}`, label: parityName(p), color: PARITY_COLOR[i % 3], kind: 'line' }))
  const data = useMemo(() => {
    if (!wood) return []

    return Array.from({ length: maxDay }, (_, i): Record<string, number> => {
      const day = i + 1

      return { day, ...Object.fromEntries(parities.map(p => [`p${p}`, woodYield(day, wood[p])])) }
    })
  }, [wood, parities, maxDay])
  // produção acumulada ao longo dos 305 dias de lactação (o que o produtor vende)
  const cumulative = useMemo(() => {
    const totals = Object.fromEntries(parities.map(p => [`p${p}`, 0]))

    return data.slice(0, LACTATION_DAYS).map((row): Record<string, number> => {
      for (const p of parities) totals[`p${p}`] += row[`p${p}`]

      return { day: row.day, ...totals }
    })
  }, [data, parities])

  const facts = useMemo(() => {
    if (!wood) return []

    return parities.map(p => {
      let peak = { day: 1, kg: 0 }
      let total = 0

      for (let d = 1; d <= LACTATION_DAYS; d++) {
        const y = woodYield(d, wood[p])

        total += y
        if (y > peak.kg) peak = { day: d, kg: y }
      }

      return { parity: p, peak, total }
    })
  }, [wood, parities])

  const markers = [
    { x: pevDays, label: `PEV ${pevDays} d`, color: 'var(--brand)' },
    { x: dryDay, label: `secagem ${dryDay} d`, color: 'var(--chart-2)' },
    { x: calving, label: `parto ${calving} d`, color: 'var(--chart-4)' }
  ].filter(marker => marker.x >= 1 && marker.x <= maxDay)
  const bands = pevDays < calving ? [{ x1: Math.max(pevDays, 1), x2: Math.min(calving, maxDay), color: 'var(--brand)' }] : []

  const tableDays = [...new Set([1, ...Array.from({ length: Math.floor(maxDay / TABLE_STEP) }, (_, i) => (i + 1) * TABLE_STEP), ...facts.map(f => f.peak.day)])]
    .filter(day => day <= maxDay)
    .sort((a, b) => a - b)
  const curveTable = (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Dia em lactação</TableHead>
          {parities.map(p => (
            <TableHead key={p} className='text-right'>
              {parityName(p)} (kg/dia)
            </TableHead>
          ))}
        </TableRow>
      </TableHeader>
      <TableBody>
        {tableDays.map(day => (
          <TableRow key={day}>
            <TableCell className='tabular-nums'>
              {day}
              {facts.some(f => f.peak.day === day) && <span className='text-muted-foreground text-xs'> · pico</span>}
            </TableCell>
            {parities.map(p => (
              <TableCell key={p} className='text-right tabular-nums'>
                {nf(woodYield(day, wood![p]), 1)}
              </TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
  const totalTable = (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Paridade</TableHead>
          <TableHead className='text-right'>Pico (kg/dia)</TableHead>
          <TableHead className='text-right'>Dia do pico</TableHead>
          <TableHead className='text-right'>Total em {LACTATION_DAYS} dias (t)</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {facts.map(f => (
          <TableRow key={f.parity}>
            <TableCell>{parityName(f.parity)}</TableCell>
            <TableCell className='text-right tabular-nums'>{nf(f.peak.kg, 1)}</TableCell>
            <TableCell className='text-right tabular-nums'>{f.peak.day}</TableCell>
            <TableCell className='text-right tabular-nums'>{nf(f.total / 1000, 2)}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )

  return (
    <div className='space-y-6'>
      <PageHeader
        title='Curva de lactação'
        description='Curva de Wood por paridade, y(t) = l · t^m · e^(−n·t). Depois do PEV a vaca pode ser inseminada; se emprenhar logo, o parto seguinte ocorre cerca de PEV + gestação dias depois do parto atual.'
        actions={
          <Badge variant='outline' className={fromRufas ? 'text-brand border-brand/40' : undefined}>
            {fromRufas ? 'parâmetros calibrados pela simulação RuFaS' : 'parâmetros de referência'}
          </Badge>
        }
      />

      <Card>
        <CardHeader>
          <CardTitle>Ciclo reprodutivo</CardTitle>
          <CardDescription>
            {fromRufas
              ? 'Usando os parâmetros (l, m, n) da última simulação do RuFaS.'
              : 'Rode uma simulação na aba Vaca leiteira para usar os parâmetros calibrados pelo RuFaS.'}
          </CardDescription>
        </CardHeader>
        <CardContent className='space-y-3'>
          <div className='grid gap-4 sm:grid-cols-3'>
            <div className='space-y-1.5'>
              <Label>PEV (dias)</Label>
              <NumberInput className='h-9' step={1} min={0} value={pev} onChange={setPev} aria-label='PEV em dias' />
            </div>
            <div className='space-y-1.5'>
              <Label>Gestação (dias)</Label>
              <NumberInput className='h-9' step={1} min={200} value={gestation} onChange={setGestation} aria-label='Gestação em dias' />
            </div>
            <div className='space-y-1.5'>
              <Label>Secagem antes do parto (dias)</Label>
              <NumberInput className='h-9' step={1} min={0} value={dry} onChange={setDry} aria-label='Dias de secagem' />
            </div>
          </div>
          <p className='text-muted-foreground flex items-center gap-2 text-sm' aria-live='polite'>
            <CalendarClockIcon className='size-4 shrink-0' aria-hidden />
            Parto seguinte no dia {calving}; a vaca é seca no dia {dryDay}, depois de {Math.max(dryDay, 0)} dias de lactação.
          </p>
        </CardContent>
      </Card>

      {!wood ? (
        connection === 'online' ? (
          <ResultsSkeleton />
        ) : (
          <EmptyState
            icon={MilkIcon}
            title='Sem parâmetros da curva'
            steps={['O servidor local não está respondendo, então os parâmetros de referência não foram carregados.', 'Inicie o servidor e recarregue a página, ou rode uma simulação na aba Vaca leiteira.']}
          />
        )
      ) : (
        <>
          <div className='grid gap-3 sm:grid-cols-2 2xl:grid-cols-3'>
            {facts.map((f, i) => (
              <KpiCard
                key={f.parity}
                icon={MilkIcon}
                color={PARITY_ACCENT[i % 3]}
                label={parityName(f.parity)}
                value={`${nf(f.peak.kg, 1)} kg`}
                hint={`pico no dia ${f.peak.day} · ${nf(f.total / 1000, 1)} t em ${LACTATION_DAYS} dias`}
                trend={data.filter((_, k) => k % 5 === 0).map(row => row[`p${f.parity}`])}
              />
            ))}
          </div>

          <ChartCard
            title='Produção de leite por dia em lactação'
            description='kg por vaca por dia. A faixa verde é a gestação do PEV até o parto; as linhas tracejadas marcam o PEV, a secagem e o parto.'
            chart={
              <>
                <TimeSeries data={data} xKey='day' series={series} markers={markers} bands={bands} format={value => nf(value, 0)} height={360} />
                <SeriesLegend series={series} />
              </>
            }
            table={curveTable}
          />

          <ChartCard
            title={`Produção acumulada em ${LACTATION_DAYS} dias`}
            description='Soma da produção diária desde o parto, por paridade, em kg por vaca.'
            chart={
              <>
                <TimeSeries data={cumulative} xKey='day' series={series} format={value => nf(value, 0)} height={260} />
                <SeriesLegend series={series} />
              </>
            }
            table={totalTable}
          />
        </>
      )}
    </div>
  )
}

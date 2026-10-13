'use client'

import { useEffect, useMemo, useState } from 'react'

import { CartesianGrid, Line, LineChart, ReferenceArea, ReferenceLine, XAxis, YAxis } from 'recharts'

import { finite, KpiCard, NumberInput, PageHeader } from '@/components/shared'
import { Badge } from '@/components/ui/badge'
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
import { api } from '@/lib/api'
import { nf } from '@/lib/format'
import type { LactationInfo, Wood } from '@/lib/types'
import { useApp } from '@/providers/AppProvider'

const PARITY_LABEL: Record<string, string> = { '1': '1ª lactação', '2': '2ª lactação', '3': '3ª ou mais' }

const woodYield = (day: number, p: Wood) => p.l * Math.pow(day, p.m) * Math.exp(-p.n * day)

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

  const pevDays = finite(pev)
  const calving = pevDays + finite(gestation)
  const dryDay = calving - finite(dry)
  const maxDay = Math.max(330, calving + 15)

  const parities = useMemo(() => Object.keys(wood ?? {}), [wood])
  const data = useMemo(() => {
    if (!wood) return []

    return Array.from({ length: maxDay }, (_, i) => {
      const day = i + 1

      return { day, ...Object.fromEntries(parities.map(p => [`p${p}`, woodYield(day, wood[p])])) }
    })
  }, [wood, parities, maxDay])

  const config = Object.fromEntries(
    parities.map((p, i) => [`p${p}`, { label: PARITY_LABEL[p] ?? `paridade ${p}`, color: `var(--chart-${[1, 2, 3][i % 3]})` }])
  ) satisfies ChartConfig

  const facts = useMemo(() => {
    if (!wood) return []

    return parities.map(p => {
      let peak = { day: 1, kg: 0 }
      let total = 0

      for (let d = 1; d <= 305; d++) {
        const y = woodYield(d, wood[p])

        total += y
        if (y > peak.kg) peak = { day: d, kg: y }
      }

      return { parity: p, peak, total }
    })
  }, [wood, parities])

  return (
    <>
      <PageHeader
        title='Curva de lactação'
        description='Curva de Wood por paridade, y(t) = l · t^m · e^(−n·t). Depois do PEV a vaca pode ser inseminada; se emprenhar logo, o parto seguinte ocorre cerca de PEV + gestação dias depois do parto atual.'
        actions={
          <Badge variant='outline' className={fromRufas ? 'text-primary border-primary/40' : undefined}>
            {fromRufas ? 'parâmetros calibrados pela simulação RuFaS' : 'parâmetros de referência'}
          </Badge>
        }
      />

      <Card>
        <CardHeader>
          <CardTitle>Produção de leite por dia em lactação</CardTitle>
          <CardDescription>
            {fromRufas
              ? 'Usando os parâmetros (l, m, n) da última simulação do RuFaS.'
              : 'Rode uma simulação na aba Vaca leiteira para usar os parâmetros calibrados pelo RuFaS.'}
          </CardDescription>
        </CardHeader>
        <CardContent className='space-y-6'>
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

          <ChartContainer config={config} className='aspect-auto h-96 w-full'>
            <LineChart data={data} margin={{ top: 24, right: 16, left: 0, bottom: 0 }}>
              <CartesianGrid vertical={false} />
              <XAxis
                dataKey='day'
                type='number'
                domain={[0, maxDay]}
                tickLine={false}
                axisLine={false}
                label={{ value: 'dias em lactação', position: 'insideBottom', offset: -2, fontSize: 12 }}
              />
              <YAxis
                tickLine={false}
                axisLine={false}
                width={40}
                label={{ value: 'kg/vaca/dia', angle: -90, position: 'insideLeft', fontSize: 12 }}
              />
              <ChartTooltip content={<ChartTooltipContent labelFormatter={v => `dia ${v}`} />} />
              <ChartLegend content={<ChartLegendContent />} />
              <ReferenceArea
                x1={pevDays}
                x2={Math.min(calving, maxDay)}
                fill='var(--primary)'
                fillOpacity={0.07}
                label={{ value: `gestação ${nf(finite(gestation), 0)} d`, position: 'insideBottom', fontSize: 12, fill: 'var(--primary)' }}
              />
              <ReferenceLine x={pevDays} stroke='var(--primary)' strokeDasharray='5 4' label={{ value: `PEV (${nf(pevDays, 0)} d)`, position: 'top', fontSize: 12, fill: 'var(--primary)' }} />
              <ReferenceLine x={dryDay} stroke='var(--chart-2)' strokeDasharray='5 4' label={{ value: `secagem (${nf(dryDay, 0)} d)`, position: 'top', fontSize: 12, fill: 'var(--chart-2)' }} />
              <ReferenceLine x={calving} stroke='var(--chart-4)' strokeDasharray='5 4' label={{ value: `parto (${nf(calving, 0)} d)`, position: 'top', fontSize: 12, fill: 'var(--chart-4)' }} />
              {parities.map(p => (
                <Line key={p} dataKey={`p${p}`} stroke={`var(--color-p${p})`} strokeWidth={2.5} dot={false} />
              ))}
            </LineChart>
          </ChartContainer>

          <div className='grid gap-3 sm:grid-cols-3'>
            {facts.map(f => (
              <KpiCard
                key={f.parity}
                label={PARITY_LABEL[f.parity] ?? `paridade ${f.parity}`}
                value={`${nf(f.peak.kg, 1)} kg`}
                hint={`pico no dia ${f.peak.day} · ${nf(f.total / 1000, 1)} t em 305 dias`}
              />
            ))}
          </div>
        </CardContent>
      </Card>
    </>
  )
}

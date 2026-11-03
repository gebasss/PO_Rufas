'use client'

import { useId } from 'react'

import { Area, AreaChart, Bar, BarChart, CartesianGrid, Cell, LabelList, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

import { cn } from '@/lib/utils'

/** Cores dos gráficos: tudo apagado, só o dado de interesse em verde vivo (FSD de design, seção "Gráficos"). */
export const CHART = {
  vivid: 'var(--chart-1)',
  dim: 'var(--chart-dim)',
  grid: 'color-mix(in oklch, var(--foreground) 8%, transparent)',
  tick: 'var(--muted-foreground)'
} as const

const AXIS = { tickLine: false, axisLine: false, fontSize: 12, stroke: CHART.tick } as const

/** Balão de valores no estilo dos cartões (fundo do popover, borda sutil, cantos arredondados). */
export function ChartTip({
  active,
  payload,
  label,
  format
}: {
  active?: boolean
  payload?: { value?: number | string; name?: string; payload?: { name?: string } }[]
  label?: string | number
  format?: (value: number) => string
}) {
  if (!active || !payload?.length) return null

  return (
    <div className='bg-popover text-popover-foreground border-border rounded-xl border px-3 py-2 text-xs'>
      <p className='text-muted-foreground mb-0.5'>{label ?? payload[0].payload?.name}</p>
      {payload.map((item, index) => (
        <p key={index} className='font-semibold tabular-nums'>
          {typeof item.value === 'number' && format ? format(item.value) : item.value}
        </p>
      ))}
    </div>
  )
}

/** Mini gráfico de tendência (sem eixos) para dentro de um cartão de KPI. */
export function Sparkline({ values, color = CHART.vivid, className }: { values: number[]; color?: string; className?: string }) {
  const id = useId().replace(/:/g, '')
  const data = values.map((value, index) => ({ index, value }))

  if (values.length < 2) return null

  return (
    <div className={cn('h-10 w-24 shrink-0', className)} aria-hidden>
      <ResponsiveContainer width='100%' height='100%'>
        <AreaChart data={data} margin={{ top: 2, right: 0, bottom: 2, left: 0 }}>
          <defs>
            <linearGradient id={id} x1='0' y1='0' x2='0' y2='1'>
              <stop offset='0%' stopColor={color} stopOpacity={0.35} />
              <stop offset='100%' stopColor={color} stopOpacity={0} />
            </linearGradient>
          </defs>
          <Area type='monotone' dataKey='value' stroke={color} strokeWidth={2} fill={`url(#${id})`} dot={false} isAnimationActive={false} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}

export interface BarDatum {
  name: string
  value: number | null
}

/**
 * Barras com um destaque: todas em verde apagado e só a de interesse em verde vivo, com o valor sobre a barra.
 * `highlight` é o `name` da barra (ou uma função); `reference` desenha uma linha tracejada (por exemplo, o cenário-base).
 */
export function HighlightBars({
  data,
  highlight,
  format = value => String(value),
  axisFormat,
  layout = 'horizontal',
  height = 260,
  reference,
  referenceLabel,
  className
}: {
  data: BarDatum[]
  highlight?: string | ((datum: BarDatum) => boolean)
  format?: (value: number) => string
  /** Formato dos números do eixo (mais curto que o dos rótulos, que levam a unidade); padrão: o mesmo de `format`. */
  axisFormat?: (value: number) => string
  /** `horizontal`: barras em pé (categorias no eixo X); `vertical`: barras deitadas (categorias no eixo Y). */
  layout?: 'horizontal' | 'vertical'
  height?: number
  reference?: number
  referenceLabel?: string
  className?: string
}) {
  const isHighlight = (datum: BarDatum) => (typeof highlight === 'function' ? highlight(datum) : datum.name === highlight)
  const vertical = layout === 'vertical'

  return (
    <div className={cn('w-full', className)} style={{ height }}>
      <ResponsiveContainer width='100%' height='100%'>
        <BarChart data={data} layout={vertical ? 'vertical' : 'horizontal'} margin={{ top: 22, right: vertical ? 56 : 8, bottom: 4, left: vertical ? 8 : 0 }}>
          <CartesianGrid stroke={CHART.grid} vertical={vertical} horizontal={!vertical} />
          {vertical ? (
            <>
              <XAxis type='number' {...AXIS} hide />
              <YAxis type='category' dataKey='name' width={150} {...AXIS} />
            </>
          ) : (
            <>
              <XAxis dataKey='name' {...AXIS} />
              <YAxis {...AXIS} width={64} tickFormatter={value => (axisFormat ?? format)(Number(value))} />
            </>
          )}
          <Tooltip cursor={{ fill: CHART.grid }} content={<ChartTip format={format} />} />
          {reference !== undefined && (
            <ReferenceLine
              {...(vertical ? { x: reference } : { y: reference })}
              stroke={CHART.tick}
              strokeDasharray='5 4'
              label={referenceLabel ? { value: referenceLabel, fill: CHART.tick, fontSize: 11, position: 'insideTopRight' } : undefined}
            />
          )}
          <Bar dataKey='value' radius={vertical ? [0, 8, 8, 0] : [8, 8, 0, 0]} maxBarSize={44} isAnimationActive={false}>
            {data.map(datum => (
              <Cell key={datum.name} fill={isHighlight(datum) ? CHART.vivid : CHART.dim} />
            ))}
            <LabelList
              dataKey='value'
              position={vertical ? 'right' : 'top'}
              fontSize={12}
              fill='var(--foreground)'
              formatter={(value: unknown) => (typeof value === 'number' ? format(value) : '')}
            />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

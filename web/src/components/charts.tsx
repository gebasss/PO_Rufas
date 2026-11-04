'use client'

import { useId } from 'react'

import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ComposedChart,
  LabelList,
  Line,
  ReferenceArea,
  ReferenceLine,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis
} from 'recharts'

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

export interface DivergingDatum {
  name: string
  /** Valor real (mostrado no rótulo e no balão). */
  value: number
  /** Valor desenhado, já limitado ao eixo, quando um dado extremo esmagaria os demais. */
  bar?: number
}

/**
 * Barras divergentes a partir do zero: verde para o que sobra ou atende e vermelho para o que falta.
 * Use `domain` para limitar o eixo; o rótulo sempre mostra o valor real.
 */
export function DivergingBars({
  data,
  format = value => String(value),
  domain,
  height = 260,
  className
}: {
  data: DivergingDatum[]
  format?: (value: number) => string
  domain?: [number, number]
  height?: number
  className?: string
}) {
  const rows = data.map(d => ({ ...d, bar: d.bar ?? d.value, text: format(d.value) }))

  return (
    <div className={cn('w-full', className)} style={{ height }}>
      <ResponsiveContainer width='100%' height='100%'>
        <BarChart data={rows} layout='vertical' margin={{ top: 8, right: 72, bottom: 4, left: 8 }}>
          <CartesianGrid stroke={CHART.grid} horizontal={false} />
          <XAxis type='number' domain={domain ?? ['auto', 'auto']} {...AXIS} hide />
          <YAxis type='category' dataKey='name' width={150} {...AXIS} />
          <Tooltip cursor={{ fill: CHART.grid }} content={<ChartTip format={format} />} />
          <ReferenceLine x={0} stroke={CHART.tick} />
          <Bar dataKey='bar' radius={6} maxBarSize={26} isAnimationActive={false}>
            {rows.map(row => (
              <Cell key={row.name} fill={row.value >= 0 ? CHART.vivid : 'var(--chart-4)'} />
            ))}
            <LabelList dataKey='text' position='right' fontSize={12} fill='var(--foreground)' />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export interface SeriesSpec {
  key: string
  label: string
  color: string
  /** `area` (padrão) ou `line`; com `stacked`, todas as áreas se empilham. */
  kind?: 'area' | 'line'
  axis?: 'left' | 'right'
  dashed?: boolean
}

/** Legenda das séries (pontos coloridos e nomes), fora do gráfico para quebrar em várias linhas. */
export function SeriesLegend({ series, className }: { series: Pick<SeriesSpec, 'label' | 'color'>[]; className?: string }) {
  return (
    <ul className={cn('text-muted-foreground flex flex-wrap gap-x-4 gap-y-1.5 text-xs', className)}>
      {series.map(item => (
        <li key={item.label} className='flex items-center gap-1.5'>
          <span className='size-2.5 rounded-full' style={{ backgroundColor: item.color }} aria-hidden />
          {item.label}
        </li>
      ))}
    </ul>
  )
}

function SeriesTip({
  active,
  payload,
  label,
  series,
  format
}: {
  active?: boolean
  payload?: { dataKey?: string; value?: number }[]
  label?: string | number
  series: SeriesSpec[]
  format?: (value: number) => string
}) {
  if (!active || !payload?.length) return null

  return (
    <div className='bg-popover text-popover-foreground border-border rounded-xl border px-3 py-2 text-xs'>
      <p className='text-muted-foreground mb-1'>{label}</p>
      {payload.map(item => {
        const spec = series.find(s => s.key === item.dataKey)

        return (
          <p key={item.dataKey} className='flex items-center gap-2 tabular-nums'>
            <span className='size-2 rounded-full' style={{ backgroundColor: spec?.color }} aria-hidden />
            <span className='text-muted-foreground'>{spec?.label}</span>
            <span className='ml-auto pl-3 font-semibold'>{typeof item.value === 'number' && format ? format(item.value) : item.value}</span>
          </p>
        )
      })}
    </div>
  )
}

/** Séries ao longo do tempo: áreas suaves (podem empilhar) e linhas, com eixo direito opcional. */
export function TimeSeries({
  data,
  xKey,
  series,
  stacked = false,
  format,
  rightFormat,
  markers,
  bands,
  height = 260,
  className
}: {
  data: Record<string, number | string | null | undefined>[]
  xKey: string
  series: SeriesSpec[]
  stacked?: boolean
  format?: (value: number) => string
  rightFormat?: (value: number) => string
  /** Linhas verticais tracejadas em valores do eixo X (marcos como PEV e parto); valores fora dos dados são ignorados. */
  markers?: { x: number; label: string; color: string }[]
  /** Faixas verticais suaves entre dois valores do eixo X (por exemplo, a gestação). */
  bands?: { x1: number; x2: number; label?: string; color: string }[]
  height?: number
  className?: string
}) {
  const id = useId().replace(/:/g, '')
  const hasRight = series.some(s => s.axis === 'right')

  return (
    <div className={cn('w-full', className)} style={{ height }}>
      <ResponsiveContainer width='100%' height='100%'>
        <ComposedChart data={data} margin={{ top: markers?.length ? 24 : 8, right: markers?.length ? 28 : hasRight ? 0 : 8, bottom: 0, left: 0 }}>
          <defs>
            {series.map(s => (
              <linearGradient key={s.key} id={`${id}-${s.key}`} x1='0' y1='0' x2='0' y2='1'>
                <stop offset='0%' stopColor={s.color} stopOpacity={stacked ? 0.55 : 0.3} />
                <stop offset='100%' stopColor={s.color} stopOpacity={stacked ? 0.25 : 0} />
              </linearGradient>
            ))}
          </defs>
          <CartesianGrid stroke={CHART.grid} vertical={false} />
          <XAxis dataKey={xKey} {...AXIS} minTickGap={28} />
          <YAxis yAxisId='left' {...AXIS} width={52} domain={stacked ? [0, 'auto'] : ['auto', 'auto']} tickFormatter={value => (format ?? String)(Number(value))} />
          {hasRight && (
            <YAxis yAxisId='right' orientation='right' {...AXIS} width={48} domain={['auto', 'auto']} tickFormatter={value => (rightFormat ?? String)(Number(value))} />
          )}
          <Tooltip cursor={{ stroke: CHART.tick, strokeDasharray: '3 3' }} content={<SeriesTip series={series} format={format} />} />
          {bands?.map(band => (
            <ReferenceArea key={`${band.x1}-${band.x2}`} yAxisId='left' x1={band.x1} x2={band.x2} fill={band.color} fillOpacity={0.08} ifOverflow='hidden' />
          ))}
          {markers?.map(marker => (
            <ReferenceLine
              key={marker.label}
              yAxisId='left'
              x={marker.x}
              stroke={marker.color}
              strokeDasharray='5 4'
              ifOverflow='hidden'
              label={{ value: marker.label, position: 'top', fontSize: 11, fill: marker.color }}
            />
          ))}
          {series.map(s =>
            s.kind === 'line' ? (
              <Line
                key={s.key}
                yAxisId={s.axis ?? 'left'}
                type='monotone'
                dataKey={s.key}
                stroke={s.color}
                strokeWidth={s.dashed ? 1.5 : 2}
                strokeDasharray={s.dashed ? '4 3' : undefined}
                dot={false}
                isAnimationActive={false}
              />
            ) : (
              <Area
                key={s.key}
                yAxisId={s.axis ?? 'left'}
                type='monotone'
                dataKey={s.key}
                stackId={stacked ? 'stack' : undefined}
                stroke={s.color}
                strokeWidth={stacked ? 1 : 2}
                fill={`url(#${id}-${s.key})`}
                dot={false}
                isAnimationActive={false}
              />
            )
          )}
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  )
}

export interface BulletBand {
  /** Limite superior da faixa, na unidade do valor. */
  to: number
  tone: 'ok' | 'warn' | 'alert'
}

const BAND_COLOR = { ok: 'bg-brand/25', warn: 'bg-warning/30', alert: 'bg-destructive/30' } as const

/** Valor sobre faixas ok, atenção e alerta (bullet chart). A cor nunca é o único canal: o valor sempre vem em texto ao lado. */
export function Bullet({
  value,
  min,
  max,
  bands,
  className
}: {
  value: number
  min: number
  max: number
  bands: BulletBand[]
  className?: string
}) {
  const span = max - min
  const pct = (v: number) => Math.min(Math.max(((v - min) / span) * 100, 0), 100)
  let from = min

  return (
    <div
      className={cn('relative h-2.5 w-full min-w-28 overflow-visible rounded-full', className)}
      role='img'
      aria-label={`Valor ${value.toFixed(1)} na escala de ${min} a ${max}`}
    >
      <div className='absolute inset-0 flex overflow-hidden rounded-full'>
        {bands.map(band => {
          const width = pct(band.to) - pct(from)

          from = band.to

          return <span key={`${band.tone}-${band.to}`} className={BAND_COLOR[band.tone]} style={{ width: `${width}%` }} />
        })}
      </div>
      <span
        className='bg-foreground absolute top-1/2 h-4 w-1 -translate-x-1/2 -translate-y-1/2 rounded-full'
        style={{ left: `${pct(value)}%` }}
      />
    </div>
  )
}

export interface ScatterDatum {
  name: string
  x: number
  y: number
}

/** Dispersão (um ponto por cenário): todos apagados e só o de interesse em verde vivo; o balão mostra o nome e os dois valores. */
export function ScatterPlot({
  data,
  highlight,
  xFormat = value => String(value),
  yFormat = value => String(value),
  yAxisFormat,
  xLabel,
  xInteger,
  referenceY,
  referenceLabel,
  height = 260,
  className
}: {
  data: ScatterDatum[]
  highlight?: string
  xFormat?: (value: number) => string
  yFormat?: (value: number) => string
  /** Formato mais curto para os números do eixo vertical; padrão: o de `yFormat`. */
  yAxisFormat?: (value: number) => string
  xLabel?: string
  /** O eixo horizontal só tem números inteiros (sementes, índices). */
  xInteger?: boolean
  /** Linha tracejada horizontal (por exemplo, o custo do LP contra os pontos do RuFaS). */
  referenceY?: number
  referenceLabel?: string
  height?: number
  className?: string
}) {
  return (
    <div className={cn('w-full', className)} style={{ height }}>
      <ResponsiveContainer width='100%' height='100%'>
        <ScatterChart margin={{ top: 12, right: 16, bottom: xLabel ? 18 : 4, left: 0 }}>
          <CartesianGrid stroke={CHART.grid} />
          <XAxis
            type='number'
            dataKey='x'
            domain={['auto', 'auto']}
            allowDecimals={!xInteger}
            {...AXIS}
            tickFormatter={value => xFormat(Number(value))}
            label={xLabel ? { value: xLabel, position: 'insideBottom', offset: -10, fill: CHART.tick, fontSize: 11 } : undefined}
          />
          <YAxis type='number' dataKey='y' domain={['auto', 'auto']} {...AXIS} width={56} tickFormatter={value => (yAxisFormat ?? yFormat)(Number(value))} />
          <Tooltip
            cursor={{ strokeDasharray: '3 3', stroke: CHART.tick }}
            content={({ active, payload }) => {
              const point = payload?.[0]?.payload as ScatterDatum | undefined

              if (!active || !point) return null

              return (
                <div className='bg-popover text-popover-foreground border-border rounded-xl border px-3 py-2 text-xs'>
                  <p className='mb-0.5 font-semibold'>{point.name}</p>
                  <p className='text-muted-foreground tabular-nums'>
                    {xLabel ?? 'x'}: {xFormat(point.x)}
                  </p>
                  <p className='font-semibold tabular-nums'>{yFormat(point.y)}</p>
                </div>
              )
            }}
          />
          {referenceY !== undefined && (
            <ReferenceLine y={referenceY} ifOverflow='extendDomain' stroke={CHART.vivid} strokeDasharray='5 4' label={referenceLabel ? { value: referenceLabel, fill: CHART.vivid, fontSize: 11, position: 'insideTopRight' } : undefined} />
          )}
          <Scatter
            data={data}
            isAnimationActive={false}
            shape={(props: { cx?: number; cy?: number; payload?: ScatterDatum }) => (
              <circle
                cx={props.cx}
                cy={props.cy}
                r={props.payload?.name === highlight ? 8 : 5.5}
                fill={props.payload?.name === highlight ? CHART.vivid : CHART.dim}
                stroke='var(--card)'
                strokeWidth={1.5}
              />
            )}
          />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  )
}

export type Tone = 'best' | 'ok' | 'bad' | 'muted'

export interface ToneDatum {
  name: string
  value: number | null
  tone: Tone
}

const TONE_FILL: Record<Tone, string> = {
  best: CHART.vivid,
  ok: CHART.dim,
  bad: 'var(--chart-4)',
  muted: 'color-mix(in oklch, var(--muted-foreground) 35%, transparent)'
}

/**
 * Barras em que cada uma tem o seu tom: `best` (verde vivo, o destaque), `ok` (verde apagado), `bad` (vermelho, o que
 * falha) e `muted` (cinza). `reference` desenha uma linha tracejada no eixo do valor (a dieta ótima, a tolerância).
 */
export function ToneBars({
  data,
  format = value => String(value),
  layout = 'vertical',
  height = 260,
  reference,
  referenceLabel,
  className
}: {
  data: ToneDatum[]
  format?: (value: number) => string
  /** `vertical`: barras deitadas (nomes no eixo Y, o padrão); `horizontal`: barras em pé. */
  layout?: 'horizontal' | 'vertical'
  height?: number
  reference?: number
  referenceLabel?: string
  className?: string
}) {
  const vertical = layout === 'vertical'

  return (
    <div className={cn('w-full', className)} style={{ height }}>
      <ResponsiveContainer width='100%' height='100%'>
        <BarChart data={data} layout={vertical ? 'vertical' : 'horizontal'} margin={{ top: 22, right: vertical ? 64 : 8, bottom: 4, left: vertical ? 8 : 0 }}>
          <CartesianGrid stroke={CHART.grid} vertical={vertical} horizontal={!vertical} />
          {vertical ? (
            <>
              <XAxis type='number' domain={[0, 'auto']} {...AXIS} hide />
              <YAxis type='category' dataKey='name' width={150} {...AXIS} />
            </>
          ) : (
            <>
              <XAxis dataKey='name' {...AXIS} />
              <YAxis {...AXIS} width={52} tickFormatter={value => format(Number(value))} />
            </>
          )}
          <Tooltip cursor={{ fill: CHART.grid }} content={<ChartTip format={format} />} />
          {reference !== undefined && (
            <ReferenceLine
              {...(vertical ? { x: reference } : { y: reference })}
              ifOverflow='extendDomain'
              stroke={CHART.tick}
              strokeDasharray='5 4'
              label={referenceLabel ? { value: referenceLabel, fill: CHART.tick, fontSize: 11, position: vertical ? 'top' : 'insideTopRight' } : undefined}
            />
          )}
          <Bar dataKey='value' radius={vertical ? [0, 8, 8, 0] : [8, 8, 0, 0]} maxBarSize={36} isAnimationActive={false}>
            {data.map(datum => (
              <Cell key={datum.name} fill={TONE_FILL[datum.tone]} />
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

export type CellStatus = 'ok' | 'no_limite' | 'violada' | 'indisponivel'

const CELL_STYLE: Record<CellStatus, { className: string; mark: string; label: string }> = {
  ok: { className: 'bg-brand/20 text-brand', mark: '✓', label: 'atende' },
  no_limite: { className: 'bg-warning/25 text-warning-text', mark: '!', label: 'no limite' },
  violada: { className: 'bg-destructive/25 text-destructive', mark: '✕', label: 'violada' },
  indisponivel: { className: 'bg-muted text-muted-foreground', mark: '–', label: 'indisponível' }
}

/** Mapa de estados (linhas × colunas): cada célula tem cor, símbolo e rótulo para leitores de tela, nunca só a cor. */
export function StatusGrid({
  columns,
  rows,
  className
}: {
  columns: { id: string; label: string }[]
  rows: { label: string; cells: CellStatus[] }[]
  className?: string
}) {
  return (
    <div className={cn('overflow-x-auto', className)}>
      <table className='border-separate border-spacing-1 text-xs'>
        <thead>
          <tr>
            <th className='sticky left-0 z-10 min-w-36 bg-[var(--card)]' />
            {columns.map(column => (
              <th key={column.id} className='h-44 align-bottom' title={column.label}>
                <span className='text-muted-foreground inline-block max-h-44 overflow-hidden text-left font-medium whitespace-nowrap [writing-mode:vertical-rl] rotate-180'>
                  {column.label}
                </span>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map(row => (
            <tr key={row.label}>
              <th className='sticky left-0 z-10 max-w-44 truncate bg-[var(--card)] pr-3 text-left text-sm font-medium'>{row.label}</th>
              {row.cells.map((status, index) => (
                <td key={columns[index].id} className='p-0'>
                  <span
                    className={cn('flex size-8 items-center justify-center rounded-lg text-sm font-semibold', CELL_STYLE[status].className)}
                    title={`${row.label}: ${columns[index].label}, ${CELL_STYLE[status].label}`}
                  >
                    <span aria-hidden>{CELL_STYLE[status].mark}</span>
                    <span className='sr-only'>{CELL_STYLE[status].label}</span>
                  </span>
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export interface SharePart {
  name: string
  value: number
  color: string
}

/** Barras empilhadas a 100% (composição de uma ração por linha), com legenda; o percentual vai na faixa quando ela cabe. */
export function ShareBars({
  rows,
  className
}: {
  rows: { label: string; parts: SharePart[] }[]
  className?: string
}) {
  const legend = new Map<string, string>()

  for (const row of rows) for (const part of row.parts) legend.set(part.name, part.color)

  return (
    <div className={cn('space-y-4', className)}>
      {rows.map(row => {
        const total = row.parts.reduce((sum, part) => sum + part.value, 0) || 1

        return (
          <div key={row.label} className='space-y-1.5'>
            <p className='text-sm font-medium'>{row.label}</p>
            <div className='flex h-9 w-full overflow-hidden rounded-xl' role='img' aria-label={`Composição de ${row.label}: ${row.parts.map(p => `${p.name} ${((100 * p.value) / total).toFixed(0)}%`).join(', ')}`}>
              {row.parts.map(part => {
                const share = (100 * part.value) / total

                return (
                  <span
                    key={part.name}
                    className='flex items-center justify-center overflow-hidden text-[11px] font-semibold text-black/80'
                    style={{ width: `${share}%`, backgroundColor: part.color }}
                    title={`${part.name}: ${share.toFixed(1)}%`}
                  >
                    {share >= 7 ? `${share.toFixed(0)}%` : ''}
                  </span>
                )
              })}
            </div>
          </div>
        )
      })}
      <SeriesLegend series={[...legend].map(([label, color]) => ({ label, color }))} />
    </div>
  )
}

/**
 * Mapa de calor de duas dimensões (por exemplo, dois fatores do quadro): cada célula mostra o valor em texto, o tom
 * esmeralda cresce com o quanto o valor é melhor (`better`) e a melhor célula ganha um contorno. `null` = sem solução.
 */
export function HeatMap({
  xLabels,
  yLabels,
  values,
  format = value => String(value),
  better = 'low',
  xTitle,
  yTitle,
  className
}: {
  xLabels: string[]
  yLabels: string[]
  /** `values[linha][coluna]`: a linha segue `yLabels` e a coluna, `xLabels`. */
  values: (number | null)[][]
  format?: (value: number) => string
  better?: 'low' | 'high'
  xTitle?: string
  yTitle?: string
  className?: string
}) {
  const flat = values.flat().filter((v): v is number => v !== null)
  const min = Math.min(...flat)
  const max = Math.max(...flat)
  const best = better === 'low' ? min : max
  const share = (value: number) => {
    const t = max === min ? 1 : (value - min) / (max - min)

    return Math.round(10 + 40 * (better === 'low' ? 1 - t : t))
  }

  return (
    <div className={cn('overflow-x-auto', className)}>
      <table className='border-separate border-spacing-1 text-sm'>
        <thead>
          <tr>
            <th className='text-muted-foreground pr-2 text-left text-xs font-normal'>{yTitle && xTitle ? `${yTitle} ↓ · ${xTitle} →` : ''}</th>
            {xLabels.map(label => (
              <th key={label} className='text-muted-foreground px-1 text-center text-xs font-medium tabular-nums'>
                {label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {yLabels.map((yLabel, row) => (
            <tr key={yLabel}>
              <th className='text-muted-foreground pr-2 text-right text-xs font-medium tabular-nums'>{yLabel}</th>
              {xLabels.map((xLabel, col) => {
                const value = values[row]?.[col] ?? null

                return (
                  <td
                    key={xLabel}
                    title={`${yTitle ?? 'linha'} ${yLabel}, ${xTitle ?? 'coluna'} ${xLabel}: ${value === null ? 'sem solução' : format(value)}`}
                    className={cn(
                      'h-12 min-w-20 rounded-lg px-2 text-center font-semibold tabular-nums',
                      value === null && 'bg-destructive/15 text-destructive text-xs font-medium',
                      value !== null && value === best && 'ring-brand ring-2'
                    )}
                    style={value === null ? undefined : { backgroundColor: `color-mix(in oklch, var(--brand) ${share(value)}%, transparent)` }}
                  >
                    {value === null ? 'inviável' : format(value)}
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

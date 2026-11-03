'use client'

import type { ReactNode } from 'react'

import { ArrowDownRightIcon, ArrowUpRightIcon, type LucideIcon } from 'lucide-react'

import { Sparkline } from '@/components/charts'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Progress } from '@/components/ui/progress'
import { signedPct } from '@/lib/format'
import { cn } from '@/lib/utils'

export function PageHeader({ title, description, actions }: { title: string; description: string; actions?: ReactNode }) {
  return (
    <div className='mb-6 flex flex-wrap items-end justify-between gap-3'>
      <div className='min-w-0'>
        <h1 className='text-2xl font-bold tracking-tight sm:text-3xl'>{title}</h1>
        <p className='text-muted-foreground mt-1 max-w-3xl text-sm text-balance'>{description}</p>
      </div>
      {actions}
    </div>
  )
}

export type AccentColor = 'brand' | 'info' | 'violet' | 'destructive' | 'warning'

const ACCENT: Record<AccentColor, { tile: string; stroke: string }> = {
  brand: { tile: 'bg-brand/12 text-brand', stroke: 'var(--chart-1)' },
  info: { tile: 'bg-info/12 text-info', stroke: 'var(--chart-3)' },
  violet: { tile: 'bg-violet/12 text-violet', stroke: 'var(--chart-5)' },
  destructive: { tile: 'bg-destructive/12 text-destructive', stroke: 'var(--chart-4)' },
  warning: { tile: 'bg-warning/12 text-warning-text', stroke: 'var(--chart-2)' }
}

/** Ícone dentro de um quadrado com fundo translúcido da própria cor (12%). */
export function IconTile({ icon: Icon, color = 'brand', className }: { icon: LucideIcon; color?: AccentColor; className?: string }) {
  return (
    <span className={cn('flex size-10 shrink-0 items-center justify-center rounded-xl', ACCENT[color].tile, className)} aria-hidden>
      <Icon className='size-5' />
    </span>
  )
}

/** Variação em pill: verde quando melhora e vermelho quando piora (`better` diz se subir é bom ou ruim). */
export function DeltaPill({ value, better = 'up', digits = 1 }: { value: number; better?: 'up' | 'down'; digits?: number }) {
  const flat = Math.abs(value) < 0.5 * 10 ** -digits
  const good = flat ? null : (value > 0) === (better === 'up')
  const Icon = value > 0 ? ArrowUpRightIcon : ArrowDownRightIcon

  return (
    <span
      className={cn(
        'inline-flex h-6 items-center gap-0.5 rounded-full px-2 text-xs font-medium tabular-nums',
        flat ? 'bg-muted text-muted-foreground' : good ? 'bg-brand/12 text-brand' : 'bg-destructive/12 text-destructive'
      )}
    >
      {!flat && <Icon className='size-3' aria-hidden />}
      {signedPct(value, digits)}
    </span>
  )
}

export function KpiCard({
  label,
  value,
  hint,
  tone = 'default',
  icon,
  color = 'brand',
  delta,
  better = 'up',
  trend
}: {
  label: string
  value: string
  hint?: string
  tone?: 'default' | 'primary' | 'warning'
  /** Ícone no quadrado translúcido; sem ele o cartão fica só com texto. */
  icon?: LucideIcon
  color?: AccentColor
  /** Variação em % em relação ao cenário-base (mostrada em pill). */
  delta?: number
  better?: 'up' | 'down'
  /** Série do mini gráfico de tendência. */
  trend?: number[]
}) {
  const accent = tone === 'warning' ? 'warning' : color

  return (
    <Card size='sm' className={cn(tone === 'primary' && 'border-brand/40 bg-brand/5', tone === 'warning' && 'border-warning/40 bg-warning/10')}>
      <CardContent className='space-y-3'>
        <div className='flex items-start gap-3'>
        {icon ? <IconTile icon={icon} color={accent} /> : null}
        <div className='min-w-0 flex-1 space-y-1'>
          <p className='text-muted-foreground text-xs'>{label}</p>
          <p className={cn('text-2xl leading-8 font-extrabold tracking-tight tabular-nums', tone === 'primary' && 'text-brand')}>{value}</p>
          {delta !== undefined || hint ? (
            <div className='flex flex-wrap items-center gap-x-2 gap-y-1'>
              {delta !== undefined ? <DeltaPill value={delta} better={better} /> : null}
              {hint ? <p className='text-muted-foreground text-xs'>{hint}</p> : null}
            </div>
          ) : null}
        </div>
        </div>
        {trend && trend.length > 1 ? <Sparkline values={trend} color={ACCENT[accent].stroke} className='h-9 w-full' /> : null}
      </CardContent>
    </Card>
  )
}

export function JobProgress({ done, total, status }: { done: number; total: number; status: string }) {
  const label =
    status === 'queued'
      ? 'Na fila…'
      : total
        ? `${done} de ${total} simulações do RuFaS concluídas`
        : 'Simulando no RuFaS…'

  return (
    <div className='space-y-1.5' role='status' aria-live='polite'>
      <Progress value={total ? (100 * done) / total : null} />
      <p className='text-muted-foreground text-xs'>{label}</p>
    </div>
  )
}

/** Campo numérico controlado. Vazio vira NaN (o chamador decide o que fazer ao enviar). */
export function NumberInput({
  value,
  onChange,
  step = 0.01,
  min,
  className,
  ...rest
}: {
  value: number
  onChange: (value: number) => void
  step?: number
  min?: number
  className?: string
  'aria-label'?: string
  title?: string
  placeholder?: string
  id?: string
}) {
  return (
    <Input
      type='number'
      inputMode='decimal'
      step={step}
      min={min}
      value={Number.isFinite(value) ? value : ''}
      onChange={e => onChange(e.target.value === '' ? Number.NaN : Number(e.target.value))}
      className={cn('h-8 text-right tabular-nums', className)}
      {...rest}
    />
  )
}

/** Troca valores não numéricos por um padrão antes de enviar à API. */
export const finite = (value: number, fallback = 0) => (Number.isFinite(value) ? value : fallback)

/** Cor de fundo proporcional ao valor (do menor ao maior), usada nas tabelas de cenários. */
export function heat(value: number, min: number, max: number, invert = false) {
  const t = max === min ? 1 : (value - min) / (max - min)
  // Teto de 40%: acima disso o texto perde contraste (WCAG 4,5:1) no tema escuro.
  const share = Math.round(8 + 32 * (invert ? 1 - t : t))

  return { backgroundColor: `color-mix(in oklch, var(--brand) ${share}%, transparent)` }
}

'use client'

import type { ReactNode } from 'react'

import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Progress } from '@/components/ui/progress'
import { cn } from '@/lib/utils'

export function PageHeader({ title, description, actions }: { title: string; description: string; actions?: ReactNode }) {
  return (
    <div className='mb-6 flex flex-wrap items-end justify-between gap-3'>
      <div className='min-w-0'>
        <h1 className='text-2xl font-semibold tracking-tight'>{title}</h1>
        <p className='text-muted-foreground mt-1 max-w-3xl text-sm text-balance'>{description}</p>
      </div>
      {actions}
    </div>
  )
}

export function KpiCard({
  label,
  value,
  hint,
  tone = 'default'
}: {
  label: string
  value: string
  hint?: string
  tone?: 'default' | 'primary' | 'warning'
}) {
  return (
    <Card
      size='sm'
      className={cn(
        tone === 'primary' && 'bg-primary/5 ring-primary/30',
        tone === 'warning' && 'bg-warning/10 ring-warning/40'
      )}
    >
      <CardContent className='space-y-1'>
        <p className='text-muted-foreground text-xs'>{label}</p>
        <p className={cn('text-2xl font-semibold tracking-tight tabular-nums', tone === 'primary' && 'text-primary')}>
          {value}
        </p>
        {hint ? <p className='text-muted-foreground text-xs'>{hint}</p> : null}
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

  return { backgroundColor: `color-mix(in oklch, var(--primary) ${share}%, transparent)` }
}

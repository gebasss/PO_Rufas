'use client'

import { useState, type ReactNode } from 'react'

import { BarChart3Icon, TableIcon } from 'lucide-react'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { cn } from '@/lib/utils'

/**
 * Cartão de gráfico com a opção "ver como tabela": o mesmo dado em tabela, para conferir números e por acessibilidade.
 * Sem `table`, o cartão só mostra o gráfico.
 */
export default function ChartCard({
  title,
  description,
  chart,
  table,
  footer,
  className
}: {
  title: string
  description?: ReactNode
  chart: ReactNode
  table?: ReactNode
  footer?: ReactNode
  className?: string
}) {
  const [view, setView] = useState<'chart' | 'table'>('chart')

  return (
    <Card className={className}>
      <CardHeader className='grid-cols-[1fr_auto]'>
        <div className='min-w-0 space-y-1'>
          <CardTitle>{title}</CardTitle>
          {description ? <CardDescription>{description}</CardDescription> : null}
        </div>
        {table ? (
          <div role='radiogroup' aria-label={`Formato de ${title}`} className='bg-muted/60 border-border inline-flex rounded-full border p-0.5'>
            {(
              [
                ['chart', BarChart3Icon, 'Gráfico'],
                ['table', TableIcon, 'Tabela']
              ] as const
            ).map(([value, Icon, label]) => (
              <button
                key={value}
                type='button'
                role='radio'
                aria-checked={view === value}
                aria-label={`Ver como ${label.toLowerCase()}`}
                title={`Ver como ${label.toLowerCase()}`}
                onClick={() => setView(value)}
                className={cn(
                  'text-muted-foreground flex size-8 items-center justify-center rounded-full transition-colors',
                  view === value && 'bg-card text-foreground border-border border'
                )}
              >
                <Icon className='size-4' />
              </button>
            ))}
          </div>
        ) : null}
      </CardHeader>
      <CardContent className='space-y-3'>
        {view === 'table' && table ? table : chart}
        {footer}
      </CardContent>
    </Card>
  )
}

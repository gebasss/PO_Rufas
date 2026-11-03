import type { ReactNode } from 'react'

import type { LucideIcon } from 'lucide-react'

import { IconTile } from '@/components/shared'
import { Card, CardContent } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'

/** Estado vazio: ícone, uma frase e os próximos passos (o fluxo configurar → executar → analisar). */
export function EmptyState({
  icon,
  title,
  steps,
  children
}: {
  icon: LucideIcon
  title: string
  steps?: string[]
  children?: ReactNode
}) {
  return (
    <Card>
      <CardContent className='flex flex-col items-center gap-4 py-14 text-center'>
        <IconTile icon={icon} className='size-14 rounded-2xl [&_svg]:size-7' />
        <div className='space-y-1.5'>
          <p className='text-lg font-semibold tracking-tight'>{title}</p>
          {steps?.length ? (
            <ol className='text-muted-foreground mx-auto max-w-md space-y-1 text-left text-sm'>
              {steps.map((step, index) => (
                <li key={step} className='flex gap-2.5'>
                  <span className='bg-muted text-foreground flex size-5 shrink-0 items-center justify-center rounded-full text-[11px] font-semibold'>
                    {index + 1}
                  </span>
                  {step}
                </li>
              ))}
            </ol>
          ) : null}
        </div>
        {children}
      </CardContent>
    </Card>
  )
}

/** Esqueleto dos resultados: mantém o formato dos cartões enquanto a simulação roda. */
export function ResultsSkeleton() {
  return (
    <div className='space-y-6' aria-busy='true' aria-label='Carregando os resultados'>
      <div className='grid gap-3 sm:grid-cols-2 xl:grid-cols-3'>
        {Array.from({ length: 6 }, (_, index) => (
          <Skeleton key={index} className='h-28 rounded-[1.25rem]' />
        ))}
      </div>
      <div className='grid gap-6 2xl:grid-cols-2'>
        <Skeleton className='h-80 rounded-[1.25rem]' />
        <Skeleton className='h-80 rounded-[1.25rem]' />
      </div>
    </div>
  )
}

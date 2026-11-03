'use client'

import { AlertTriangleIcon, CheckIcon, LoaderCircleIcon, PlayIcon, RotateCcwIcon } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

export type RunState = 'idle' | 'running' | 'done' | 'error'

interface Props {
  state: RunState
  /** Progresso da tarefa (`total` 0 = na fila ou sem estimativa). */
  progress?: { done: number; total: number }
  /** Texto do botão no estado pronto, por exemplo "Executar simulação". */
  label: string
  /** Rótulo do progresso, por exemplo "simulações do RuFaS". */
  unit?: string
  error?: string | null
  disabled?: boolean
  onRun: () => void
  /** No estado concluído o botão principal leva aos resultados. */
  onView?: () => void
}

/**
 * Botão Executar com os quatro estados do fluxo: pronto (claro), executando (barra de progresso no próprio botão),
 * concluído (esmeralda, leva aos resultados) e erro (vermelho, tentar de novo).
 */
export default function RunButton({ state, progress, label, unit = 'passos', error, disabled, onRun, onView }: Props) {
  const percent = progress && progress.total > 0 ? Math.round((100 * progress.done) / progress.total) : null

  return (
    <div className='space-y-2'>
      {state === 'running' ? (
        <div
          className='bg-muted border-border relative flex h-12 w-full items-center justify-center gap-2 overflow-hidden rounded-xl border text-sm font-medium'
          role='status'
          aria-live='polite'
        >
          <span
            className='bg-brand/25 absolute inset-y-0 left-0 transition-[width] duration-500'
            style={{ width: `${percent ?? 8}%` }}
            aria-hidden
          />
          <LoaderCircleIcon className='relative size-4 animate-spin' />
          <span className='relative'>
            {percent === null ? 'Na fila…' : `Executando… ${progress?.done} de ${progress?.total} ${unit}`}
          </span>
        </div>
      ) : state === 'done' ? (
        <div className='flex gap-2'>
          <Button variant='brand' size='lg' className='h-12 flex-1' onClick={onView ?? onRun}>
            <CheckIcon /> Concluído · ver resultados
          </Button>
          <Button variant='outline' size='icon-lg' className='h-12 w-12' onClick={onRun} disabled={disabled} aria-label='Executar de novo' title='Executar de novo'>
            <RotateCcwIcon />
          </Button>
        </div>
      ) : state === 'error' ? (
        <Button
          variant='outline'
          size='lg'
          className={cn('border-destructive/50 text-destructive hover:bg-destructive/10 h-12 w-full')}
          onClick={onRun}
          disabled={disabled}
        >
          <AlertTriangleIcon /> Tentar de novo
        </Button>
      ) : (
        <Button size='lg' className='h-12 w-full text-[15px] font-semibold' onClick={onRun} disabled={disabled}>
          <PlayIcon /> {label}
        </Button>
      )}
      {state === 'error' && error ? (
        <p className='text-destructive text-xs' role='alert'>
          {error}
        </p>
      ) : null}
    </div>
  )
}

'use client'

import { Button } from '@/components/ui/button'

/** Escolha entre poucas opções mutuamente exclusivas (grupo de rádio feito com botões). */
export function Segmented<T extends string>({
  value,
  options,
  onChange,
  label,
  disabled
}: {
  value: T
  options: { value: T; label: string; hint?: string }[]
  onChange: (value: T) => void
  label: string
  disabled?: boolean
}) {
  return (
    <div role='radiogroup' aria-label={label} className='inline-flex flex-wrap gap-1.5'>
      {options.map(option => {
        const active = option.value === value

        return (
          <Button
            key={option.value}
            type='button'
            role='radio'
            aria-checked={active}
            variant={active ? 'default' : 'outline'}
            size='sm'
            disabled={disabled}
            onClick={() => onChange(option.value)}
          >
            {option.label}
            {option.hint ? <span className='text-xs opacity-70'>({option.hint})</span> : null}
          </Button>
        )
      })}
    </div>
  )
}

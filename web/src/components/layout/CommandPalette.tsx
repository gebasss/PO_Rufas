'use client'

import { useEffect, useMemo, useState } from 'react'

import { useRouter } from 'next/navigation'

import { CornerDownLeftIcon, MoonStarIcon, SearchIcon } from 'lucide-react'
import { useTheme } from 'next-themes'

import { allNavLinks } from '@/components/layout/nav'
import { Dialog, DialogContent, DialogTitle } from '@/components/ui/dialog'
import { cn } from '@/lib/utils'

interface Command {
  id: string
  label: string
  hint: string
  icon: React.ComponentType<{ className?: string }>
  run: () => void
}

const normalize = (text: string) =>
  text
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()

/** Rótulo curto do atalho (⌘K no Mac, Ctrl K nos demais). */
export const shortcutLabel = () =>
  typeof navigator !== 'undefined' && /mac|iphone|ipad/i.test(navigator.platform) ? '⌘K' : 'Ctrl K'

/** Paleta de comandos: ir a uma tela ou trocar o tema, com busca e teclado (↑ ↓ Enter). */
export default function CommandPalette({
  open,
  onOpenChange
}: {
  open: boolean
  onOpenChange: (open: boolean) => void
}) {
  const router = useRouter()
  const { setTheme, resolvedTheme } = useTheme()
  const [query, setQuery] = useState('')
  const [active, setActive] = useState(0)

  const commands: Command[] = useMemo(
    () => [
      ...allNavLinks.map(link => ({
        id: link.href,
        label: link.label,
        hint: link.description,
        icon: link.icon,
        run: () => router.push(link.href)
      })),
      {
        id: 'theme',
        label: resolvedTheme === 'dark' ? 'Usar tema claro' : 'Usar tema escuro',
        hint: 'Alterna entre os temas claro e escuro.',
        icon: MoonStarIcon,
        run: () => setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')
      }
    ],
    [router, resolvedTheme, setTheme]
  )
  const shown = useMemo(() => {
    const q = normalize(query.trim())

    return commands.filter(c => !q || normalize(`${c.label} ${c.hint}`).includes(q))
  }, [commands, query])

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault()
        onOpenChange(!open)
      }
    }

    window.addEventListener('keydown', onKey)

    return () => window.removeEventListener('keydown', onKey)
  }, [open, onOpenChange])

  useEffect(() => {
    if (open) {
      setQuery('')
      setActive(0)
    }
  }, [open])

  const choose = (command: Command | undefined) => {
    if (!command) return

    onOpenChange(false)
    command.run()
  }

  const onKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'ArrowDown') {
      event.preventDefault()
      setActive(i => (shown.length ? (i + 1) % shown.length : 0))
    } else if (event.key === 'ArrowUp') {
      event.preventDefault()
      setActive(i => (shown.length ? (i - 1 + shown.length) % shown.length : 0))
    } else if (event.key === 'Enter') {
      event.preventDefault()
      choose(shown[active])
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogTitle>Paleta de comandos</DialogTitle>
        <div className='border-border flex items-center gap-3 border-b px-4'>
          <SearchIcon className='text-muted-foreground size-4 shrink-0' />
          <input
            autoFocus
            value={query}
            onChange={event => {
              setQuery(event.target.value)
              setActive(0)
            }}
            onKeyDown={onKeyDown}
            placeholder='Ir para uma tela ou executar um comando…'
            aria-label='Buscar comando'
            className='placeholder:text-muted-foreground h-14 w-full bg-transparent text-sm outline-none'
          />
        </div>
        <ul role='listbox' aria-label='Comandos' className='max-h-80 overflow-y-auto p-2'>
          {shown.length === 0 && (
            <li className='text-muted-foreground px-3 py-6 text-center text-sm'>Nada encontrado.</li>
          )}
          {shown.map((command, index) => (
            <li
              key={command.id}
              role='option'
              aria-selected={index === active}
              onMouseEnter={() => setActive(index)}
              onClick={() => choose(command)}
              className={cn('flex cursor-pointer items-center gap-3 rounded-xl px-3 py-2.5', index === active && 'bg-muted')}
            >
              <span className='bg-brand/12 text-brand flex size-9 shrink-0 items-center justify-center rounded-xl'>
                <command.icon className='size-4' />
              </span>
              <span className='min-w-0 flex-1'>
                <span className='block truncate text-sm font-medium'>{command.label}</span>
                <span className='text-muted-foreground block truncate text-xs'>{command.hint}</span>
              </span>
              {index === active && <CornerDownLeftIcon className='text-muted-foreground size-4 shrink-0' />}
            </li>
          ))}
        </ul>
      </DialogContent>
    </Dialog>
  )
}

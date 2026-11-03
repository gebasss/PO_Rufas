'use client'

import { useEffect, useState } from 'react'

import { usePathname } from 'next/navigation'

import { SearchIcon } from 'lucide-react'

import CommandPalette, { shortcutLabel } from '@/components/layout/CommandPalette'
import ModeToggle from '@/components/layout/ModeToggle'
import { findNav } from '@/components/layout/nav'
import TasksMenu from '@/components/layout/TasksMenu'
import { SidebarTrigger } from '@/components/ui/sidebar'
import { cn } from '@/lib/utils'
import { useApp } from '@/providers/AppProvider'

const connectionLabel = {
  connecting: 'Conectando…',
  online: 'Conectado',
  offline: 'Sem conexão'
} as const

/** Barra superior flutuante em pílula: sidebar, tela atual, busca ⌘K, tarefas, tema e conexão. */
const Header = () => {
  const pathname = usePathname()
  const { connection, feeds } = useApp()
  const page = findNav(pathname)
  const [paletteOpen, setPaletteOpen] = useState(false)
  const [shortcut, setShortcut] = useState('⌘K')

  useEffect(() => setShortcut(shortcutLabel()), [])

  return (
    <>
      <header className='sticky top-3 z-40 px-3 sm:px-6'>
        <div className='bg-card/80 border-border mx-auto flex max-w-360 items-center gap-1.5 rounded-full border px-2 py-1.5 backdrop-blur-xl'>
          <SidebarTrigger className='rounded-full [&_svg]:size-5!' />
          <p className='ml-1 min-w-0 truncate text-sm font-semibold sm:text-base'>{page?.label ?? 'Dieta Ótima'}</p>

          <div className='ml-auto flex items-center gap-1.5'>
            <button
              type='button'
              onClick={() => setPaletteOpen(true)}
              className='text-muted-foreground hover:text-foreground border-input hidden h-9 min-w-56 items-center gap-2 rounded-full border px-3.5 text-sm transition-colors md:flex'
              aria-label='Buscar ou ir para uma tela'
            >
              <SearchIcon className='size-4' />
              <span className='flex-1 text-left'>Buscar…</span>
              <kbd className='bg-muted rounded-md px-1.5 py-0.5 text-[11px] font-medium'>{shortcut}</kbd>
            </button>
            <button
              type='button'
              onClick={() => setPaletteOpen(true)}
              className='text-muted-foreground hover:text-foreground flex size-10 items-center justify-center rounded-full md:hidden'
              aria-label='Buscar ou ir para uma tela'
            >
              <SearchIcon className='size-5' />
            </button>
            <TasksMenu />
            <ModeToggle />
            <span
              className={cn(
                'hidden h-9 items-center gap-2 rounded-full border px-3 text-xs font-medium sm:flex',
                connection === 'offline' ? 'border-destructive/40 text-destructive' : 'border-input text-muted-foreground'
              )}
              role='status'
            >
              <span
                className={cn(
                  'size-2 rounded-full',
                  connection === 'online' ? 'bg-brand' : connection === 'offline' ? 'bg-destructive' : 'animate-pulse bg-amber-400'
                )}
              />
              {connectionLabel[connection]}
              {connection === 'online' && <span className='hidden lg:inline'>· {feeds.length} alimentos NRC</span>}
            </span>
          </div>
        </div>
      </header>
      <CommandPalette open={paletteOpen} onOpenChange={setPaletteOpen} />
    </>
  )
}

export default Header

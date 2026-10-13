'use client'

import { usePathname } from 'next/navigation'

import ModeToggle from '@/components/layout/ModeToggle'
import { findNav } from '@/components/layout/nav'
import { Badge } from '@/components/ui/badge'
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator
} from '@/components/ui/breadcrumb'
import { Separator } from '@/components/ui/separator'
import { SidebarTrigger } from '@/components/ui/sidebar'
import { useApp } from '@/providers/AppProvider'

const connectionLabel = {
  connecting: 'conectando…',
  online: 'conectado',
  offline: 'sem conexão com o servidor'
} as const

const Header = () => {
  const pathname = usePathname()
  const { connection, feeds } = useApp()
  const page = findNav(pathname)

  return (
    <header className='bg-card sticky top-0 z-50 border-b'>
      <div className='mx-auto flex max-w-360 items-center justify-between gap-6 px-4 py-2 sm:px-6'>
        <div className='flex items-center gap-4'>
          <SidebarTrigger className='[&_svg]:size-5!' />
          <Separator orientation='vertical' className='hidden h-4! data-vertical:self-center sm:block' />
          <Breadcrumb className='hidden sm:block'>
            <BreadcrumbList>
              <BreadcrumbItem>Dieta Ótima</BreadcrumbItem>
              <BreadcrumbSeparator />
              <BreadcrumbItem>
                <BreadcrumbPage>{page?.label ?? 'Página'}</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        </div>
        <div className='flex items-center gap-2'>
          <Badge
            variant={connection === 'offline' ? 'destructive' : 'outline'}
            className={connection === 'online' ? 'text-primary border-primary/40' : undefined}
          >
            {connectionLabel[connection]}
            {connection === 'online' ? ` · ${feeds.length} alimentos NRC` : ''}
          </Badge>
          <ModeToggle />
        </div>
      </div>
    </header>
  )
}

export default Header

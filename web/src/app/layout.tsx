import type { ReactNode } from 'react'

import type { Metadata } from 'next'

import { GeistMono } from 'geist/font/mono'
import { GeistSans } from 'geist/font/sans'

import AppShell from '@/components/layout/AppShell'
import { ThemeProvider } from '@/components/ThemeProvider'
import { SidebarProvider } from '@/components/ui/sidebar'
import { TooltipProvider } from '@/components/ui/tooltip'
import { cn } from '@/lib/utils'
import { AppProvider } from '@/providers/AppProvider'

import './globals.css'

export const metadata: Metadata = {
  title: 'Dieta Ótima com RuFaS',
  description:
    'Otimização da dieta de vacas leiteiras com o simulador RuFaS: custo mínimo, sensibilidade a preços e curva de lactação.'
}

const RootLayout = ({ children }: Readonly<{ children: ReactNode }>) => {
  return (
    <html
      lang='pt-BR'
      className={cn(GeistSans.variable, GeistMono.variable, 'flex min-h-full w-full antialiased')}
      suppressHydrationWarning
    >
      <body className='flex min-h-full w-full flex-auto flex-col font-sans'>
        <ThemeProvider attribute='class' defaultTheme='system' enableSystem>
          <TooltipProvider>
            <SidebarProvider defaultOpen>
              <AppProvider>
                <AppShell>{children}</AppShell>
              </AppProvider>
            </SidebarProvider>
          </TooltipProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}

export default RootLayout

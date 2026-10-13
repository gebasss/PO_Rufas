'use client'

import type { ReactNode } from 'react'

import AppSidebar from '@/components/layout/AppSidebar'
import Footer from '@/components/layout/Footer'
import Header from '@/components/layout/Header'
import { SidebarInset } from '@/components/ui/sidebar'
import { Toaster } from '@/components/ui/sonner'

const AppShell = ({ children }: { children: ReactNode }) => {
  return (
    <div className='flex h-full w-full min-w-0'>
      <AppSidebar />
      <SidebarInset className='flex flex-1 flex-col'>
        <Header />
        <main className='mx-auto size-full max-w-360 flex-1 px-4 py-6 sm:px-6'>{children}</main>
        <Toaster />
        <Footer />
      </SidebarInset>
    </div>
  )
}

export default AppShell

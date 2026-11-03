'use client'

import * as React from 'react'

import { Tabs as TabsPrimitive } from '@base-ui/react/tabs'

import { cn } from '@/lib/utils'

function Tabs({ className, ...props }: TabsPrimitive.Root.Props) {
  return <TabsPrimitive.Root data-slot='tabs' className={cn('flex flex-col gap-6', className)} {...props} />
}

/** Lista de abas em pílula: a aba ativa ganha o fundo do cartão e uma borda sutil. */
function TabsList({ className, ...props }: TabsPrimitive.List.Props) {
  return (
    <TabsPrimitive.List
      data-slot='tabs-list'
      className={cn(
        'bg-muted/60 border-border inline-flex w-fit max-w-full items-center gap-1 overflow-x-auto rounded-full border p-1',
        className
      )}
      {...props}
    />
  )
}

function TabsTab({ className, ...props }: TabsPrimitive.Tab.Props) {
  return (
    <TabsPrimitive.Tab
      data-slot='tabs-tab'
      className={cn(
        'text-muted-foreground hover:text-foreground focus-visible:ring-ring/40 data-active:bg-card data-active:text-foreground data-active:border-border inline-flex h-9 shrink-0 items-center justify-center gap-1.5 rounded-full border border-transparent px-4 text-sm font-medium whitespace-nowrap transition-colors outline-none focus-visible:ring-3 [&_svg]:size-4',
        className
      )}
      {...props}
    />
  )
}

function TabsPanel({ className, ...props }: TabsPrimitive.Panel.Props) {
  return <TabsPrimitive.Panel data-slot='tabs-panel' className={cn('flex flex-col gap-6 outline-none', className)} {...props} />
}

export { Tabs, TabsList, TabsTab, TabsPanel }

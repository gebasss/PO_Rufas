'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

import { WheatIcon } from 'lucide-react'

import { navGroups, normalizePath } from '@/components/layout/nav'
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar
} from '@/components/ui/sidebar'

const AppSidebar = () => {
  const pathname = normalizePath(usePathname())
  const { isMobile, setOpenMobile } = useSidebar()

  return (
    <Sidebar collapsible='icon' variant='sidebar'>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              size='lg'
              className='gap-2.5 bg-transparent!'
              render={<Link href='/' />}
              onClick={() => isMobile && setOpenMobile(false)}
            >
              <span className='bg-primary text-primary-foreground flex size-8 shrink-0 items-center justify-center rounded-lg'>
                <WheatIcon className='size-5' />
              </span>
              <div className='flex flex-col items-start leading-tight'>
                <span className='text-base font-semibold text-nowrap'>Dieta Ótima</span>
                <span className='text-sidebar-foreground/60 text-xs text-nowrap'>com RuFaS</span>
              </div>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>

      <SidebarContent>
        {navGroups.map(group => (
          <SidebarGroup key={group.label}>
            <SidebarGroupLabel className='text-sidebar-foreground/50 tracking-wider uppercase'>
              {group.label}
            </SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {group.items.map(item => (
                  <SidebarMenuItem key={item.href}>
                    <SidebarMenuButton
                      tooltip={item.label}
                      isActive={pathname === item.href}
                      className='data-active:bg-primary/10!'
                      render={<Link href={item.href} />}
                      onClick={() => isMobile && setOpenMobile(false)}
                    >
                      <item.icon />
                      <span className='min-w-0 flex-1 truncate'>{item.label}</span>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        ))}
      </SidebarContent>

      <SidebarFooter>
        <p className='text-sidebar-foreground/60 px-2 text-xs group-data-[collapsible=icon]:hidden'>
          RuFaS v1.0.6 · NRC 2001
        </p>
      </SidebarFooter>
    </Sidebar>
  )
}

export default AppSidebar

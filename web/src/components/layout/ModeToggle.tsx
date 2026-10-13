'use client'

import { MoonStarIcon, SunIcon } from 'lucide-react'
import { useTheme } from 'next-themes'

import { Button } from '@/components/ui/button'

const ModeToggle = () => {
  const { setTheme, resolvedTheme } = useTheme()

  return (
    <Button
      variant='ghost'
      size='icon'
      className='relative'
      onClick={() => setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')}
    >
      <MoonStarIcon className='scale-100 dark:scale-0' />
      <SunIcon className='absolute scale-0 dark:scale-100' />
      <span className='sr-only'>Alternar tema claro e escuro</span>
    </Button>
  )
}

export default ModeToggle

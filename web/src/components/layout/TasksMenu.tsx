'use client'

import { ActivityIcon } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { Progress } from '@/components/ui/progress'
import { useApp } from '@/providers/AppProvider'

/** Tarefas em segundo plano: aparece um ponto esmeralda no ícone enquanto alguma roda. */
export default function TasksMenu() {
  const { tasks } = useApp()

  return (
    <Popover>
      <PopoverTrigger
        render={<Button variant='ghost' size='icon' className='relative rounded-full' aria-label='Tarefas em andamento' />}
      >
        <ActivityIcon />
        {tasks.length > 0 && (
          <span className='bg-brand ring-card absolute top-2 right-2 size-2 animate-pulse rounded-full ring-2' />
        )}
      </PopoverTrigger>
      <PopoverContent>
        <p className='mb-3 text-sm font-semibold'>Tarefas</p>
        {tasks.length === 0 ? (
          <p className='text-muted-foreground text-sm'>
            Nenhuma tarefa em andamento. Simulações e otimizações aparecem aqui enquanto rodam.
          </p>
        ) : (
          <ul className='space-y-3'>
            {tasks.map(task => (
              <li key={task.id} className='space-y-1.5'>
                <div className='flex items-center justify-between gap-2 text-sm'>
                  <span className='truncate'>{task.label}</span>
                  <span className='text-muted-foreground text-xs tabular-nums'>
                    {task.total ? `${task.done}/${task.total}` : 'na fila'}
                  </span>
                </div>
                <Progress value={task.total ? (100 * task.done) / task.total : null} />
              </li>
            ))}
          </ul>
        )}
      </PopoverContent>
    </Popover>
  )
}

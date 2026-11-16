'use client'

import { useState } from 'react'

import { toast } from 'sonner'

import { Button } from '@/components/ui/button'
import { Dialog, DialogContent, DialogTitle } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { api } from '@/lib/api'
import type { RunMeta } from '@/lib/types'

export const MAX_NAME = 80
export const MAX_NOTE = 500

interface Props {
  run: Pick<RunMeta, 'id' | 'title' | 'name' | 'note'> | null
  onClose: () => void
  onSaved: () => void
}

function Form({ run, onClose, onSaved }: Props & { run: NonNullable<Props['run']> }) {
  const [name, setName] = useState(run.name ?? '')
  const [note, setNote] = useState(run.note ?? '')
  const [saving, setSaving] = useState(false)

  const save = async () => {
    setSaving(true)

    try {
      await api.updateHistory(run.id, { name, note })
      toast.success('Nome e nota salvos.')
      onSaved()
      onClose()
    } catch (e) {
      toast.error(e instanceof Error ? e.message.split('\n')[0] : 'Falha ao salvar')
      setSaving(false)
    }
  }

  return (
    <form
      className='space-y-4 p-5'
      onSubmit={event => {
        event.preventDefault()
        void save()
      }}
    >
      <div>
        <h2 className='text-base font-semibold'>Nome e nota da execução</h2>
        <p className='text-muted-foreground mt-1 text-xs'>{run.title}</p>
      </div>
      <label className='block space-y-1.5 text-sm'>
        <span className='font-medium'>Nome</span>
        <Input value={name} maxLength={MAX_NAME} autoFocus placeholder='Ex.: Farelo de soja mais caro' onChange={event => setName(event.target.value)} />
        <span className='text-muted-foreground block text-xs'>Aparece no lugar do título automático. Deixe em branco para voltar a ele.</span>
      </label>
      <label className='block space-y-1.5 text-sm'>
        <span className='font-medium'>Nota</span>
        <textarea
          value={note}
          maxLength={MAX_NOTE}
          rows={4}
          placeholder='O que você testou, por que, o que concluiu…'
          onChange={event => setNote(event.target.value)}
          className='border-input bg-background placeholder:text-muted-foreground focus-visible:ring-ring/30 focus-visible:border-ring w-full resize-y rounded-xl border px-3 py-2 text-sm outline-none focus-visible:ring-3'
        />
        <span className='text-muted-foreground block text-right text-xs tabular-nums'>
          {note.length} de {MAX_NOTE}
        </span>
      </label>
      <div className='flex justify-end gap-2'>
        <Button type='button' variant='outline' onClick={onClose}>
          Cancelar
        </Button>
        <Button type='submit' disabled={saving}>
          Salvar
        </Button>
      </div>
    </form>
  )
}

/** Janela para dar um nome e escrever uma nota numa execução. */
export default function RunNameDialog({ run, onClose, onSaved }: Props) {
  return (
    <Dialog open={run !== null} onOpenChange={open => !open && onClose()}>
      <DialogContent>
        <DialogTitle>Nome e nota da execução</DialogTitle>
        {run && <Form key={run.id} run={run} onClose={onClose} onSaved={onSaved} />}
      </DialogContent>
    </Dialog>
  )
}

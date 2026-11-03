'use client'

import { useRef, useState } from 'react'

import { FolderOpenIcon, SaveIcon } from 'lucide-react'
import { toast } from 'sonner'

import { Button } from '@/components/ui/button'
import { api } from '@/lib/api'
import { downloadText } from '@/lib/download'
import type { ScenarioKind } from '@/lib/types'

const KIND_LABEL: Record<ScenarioKind, string> = { cow: 'Vaca leiteira', module: 'Avaliar dietas' }

interface Props<T> {
  kind: ScenarioKind
  /** Entradas da tela, como o back-end as espera (sem resultados). */
  getData: () => unknown
  /** Recebe o cenário já validado pelo back-end e o aplica à tela. */
  onLoad: (data: T) => void
}

/** Salva as entradas da tela em um arquivo JSON e as restaura de um arquivo salvo antes (RF-21). */
export default function ScenarioFile<T>({ kind, getData, onLoad }: Props<T>) {
  const input = useRef<HTMLInputElement>(null)
  const [busy, setBusy] = useState(false)

  const fail = (error: unknown, fallback: string) =>
    toast.error(error instanceof Error ? error.message.split('\n')[0] : fallback)

  const save = async () => {
    setBusy(true)

    try {
      const file = await api.saveScenario(kind, getData())

      downloadText(file.filename, file.content, file.mime)
      toast.success(`Cenário salvo em ${file.filename}.`)
    } catch (error) {
      fail(error, 'Falha ao salvar o cenário')
    } finally {
      setBusy(false)
    }
  }

  const open = async (file: File) => {
    setBusy(true)

    try {
      const loaded = await api.loadScenario<T>(await file.text())

      if (loaded.kind !== kind) {
        throw new Error(`Este arquivo é um cenário de ${KIND_LABEL[loaded.kind]}; abra-o na tela correspondente.`)
      }

      onLoad(loaded.data)
      toast.success(`Cenário aberto: ${file.name}.`)

      for (const warning of loaded.warnings) toast.warning(warning)
    } catch (error) {
      fail(error, 'Falha ao abrir o cenário')
    } finally {
      setBusy(false)

      if (input.current) input.current.value = ''
    }
  }

  return (
    <div className='flex flex-wrap items-center gap-2'>
      <Button variant='outline' size='sm' disabled={busy} onClick={save}>
        <SaveIcon /> Salvar cenário
      </Button>
      <Button variant='outline' size='sm' disabled={busy} onClick={() => input.current?.click()}>
        <FolderOpenIcon /> Abrir cenário
      </Button>
      <input
        ref={input}
        type='file'
        accept='.json,application/json'
        className='sr-only'
        aria-label='Arquivo de cenário'
        tabIndex={-1}
        onChange={e => {
          const file = e.target.files?.[0]

          if (file) void open(file)
        }}
      />
    </div>
  )
}

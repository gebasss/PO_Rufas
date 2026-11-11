'use client'

import { useState } from 'react'

import { DownloadIcon, FileTextIcon } from 'lucide-react'
import { toast } from 'sonner'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { api } from '@/lib/api'
import { downloadText } from '@/lib/download'

type Screen = 'simulation' | 'sensitivity' | 'module'

interface Props {
  screen: Screen
  /** O resultado que está na tela, como veio da API. */
  data: unknown
  /** Dados da tela que o resultado não traz (limites, nomes de alimentos, padrão, dieta ótima). */
  meta?: Record<string, unknown>
}

/** Baixa o CSV da tabela e o relatório (HTML imprimível) do resultado da tela (RF-20). */
export default function ExportButtons({ screen, data, meta }: Props) {
  const [busy, setBusy] = useState<'csv' | 'report' | null>(null)
  const [note, setNote] = useState('')

  const download = async (format: 'csv' | 'report') => {
    setBusy(format)

    try {
      const file = await api.exportFile(format, screen, data, { ...meta, note })

      downloadText(file.filename, file.content, file.mime)
    } catch (error) {
      toast.error(error instanceof Error ? error.message.split('\n')[0] : 'Falha ao exportar')
    } finally {
      setBusy(null)
    }
  }

  return (
    <div className='flex flex-wrap items-center gap-2'>
      <Button variant='outline' size='sm' disabled={busy !== null} onClick={() => download('csv')}>
        <DownloadIcon /> {busy === 'csv' ? 'Gerando…' : 'Baixar CSV'}
      </Button>
      <Button variant='outline' size='sm' disabled={busy !== null} onClick={() => download('report')}>
        <FileTextIcon /> {busy === 'report' ? 'Gerando…' : 'Baixar relatório'}
      </Button>
      <Input
        value={note}
        onChange={e => setNote(e.target.value)}
        placeholder='Observação para o relatório (opcional)'
        aria-label='Observação para o relatório'
        className='h-8 w-72 max-w-full'
        maxLength={2000}
      />
    </div>
  )
}

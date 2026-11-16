'use client'

import { useCallback, useEffect, useState } from 'react'

import { HardDriveIcon } from 'lucide-react'
import { toast } from 'sonner'

import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { api } from '@/lib/api'
import { bytesLabel } from '@/lib/history'
import type { HistoryStorage } from '@/lib/types'

/** Espaço em disco das pastas de simulação (`runs/web_*`) e o botão que as apaga. O histórico não é tocado. */
export default function StoragePanel() {
  const [storage, setStorage] = useState<HistoryStorage | null>(null)
  const [busy, setBusy] = useState(false)
  const [version, setVersion] = useState(0)

  useEffect(() => {
    let cancelled = false

    api
      .historyStorage()
      .then(value => !cancelled && setStorage(value))
      .catch(() => !cancelled && setStorage(null))

    return () => {
      cancelled = true
    }
  }, [version])

  const clean = useCallback(async () => {
    if (!storage) return

    const ok = window.confirm(
      `Apagar ${storage.folders} pastas de simulação (${bytesLabel(storage.folders_bytes)})?\n\n` +
        'São as entradas, os logs e as saídas brutas do RuFaS em runs/web_*. As execuções do histórico e os resultados guardados continuam ' +
        'abertos, e rodar o mesmo cenário de novo reaproveita o resultado guardado. Isso não pode ser desfeito.'
    )

    if (!ok) return

    setBusy(true)

    try {
      const result = await api.cleanHistoryFolders()

      toast.success(
        `${result.removed} pastas apagadas, ${bytesLabel(result.freed_bytes)} liberados.` +
          (result.failed ? ` ${result.failed} não puderam ser apagadas (em uso).` : '')
      )
      setVersion(n => n + 1)
    } catch (e) {
      toast.error(e instanceof Error ? e.message.split('\n')[0] : 'Falha ao limpar os arquivos')
    } finally {
      setBusy(false)
    }
  }, [storage])

  if (!storage) return null

  return (
    <Card>
      <CardContent className='flex flex-wrap items-center justify-between gap-3'>
        <div className='flex min-w-0 items-start gap-3'>
          <HardDriveIcon className='text-muted-foreground mt-0.5 size-5 shrink-0' aria-hidden />
          <div className='min-w-0 text-sm'>
            <p className='font-medium'>
              {storage.folders === 0
                ? 'Nenhuma pasta de simulação guardada'
                : `${storage.folders} pastas de simulação ocupam ${bytesLabel(storage.folders_bytes)}`}
            </p>
            <p className='text-muted-foreground'>
              Cada simulação deixa uma pasta em runs/ com as saídas brutas do RuFaS; elas não são necessárias para abrir as execuções
              (o histórico ocupa só {bytesLabel(storage.history_bytes)}).
            </p>
          </div>
        </div>
        <Button variant='outline' size='sm' disabled={busy || storage.folders === 0} onClick={clean}>
          Limpar arquivos antigos
        </Button>
      </CardContent>
    </Card>
  )
}

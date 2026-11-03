'use client'

import { useRef, useState } from 'react'

import { DownloadIcon, UploadIcon } from 'lucide-react'

import { NumberInput } from '@/components/shared'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { api } from '@/lib/api'
import { nf } from '@/lib/format'
import type { NutrientStandard, PriceImportResult } from '@/lib/types'

/** Modelo de arquivo: o preço de cada alimento por id do RuFaS, em US$/kg MS ou convertido (reais, saca, matéria natural). */
const TEMPLATE = `id,preco,moeda,cambio,unidade_kg,base,fonte
50,0.09,USD,,1,MS,preço já em US$ por kg de MS
44,70,BRL,5.0,60,MN,saca de 60 kg em reais na matéria natural
`

function downloadTemplate() {
  const url = URL.createObjectURL(new Blob(['﻿', TEMPLATE], { type: 'text/csv;charset=utf-8' }))
  const link = document.createElement('a')

  link.href = url
  link.download = 'modelo-precos.csv'
  link.click()
  URL.revokeObjectURL(url)
}

interface Props {
  standard: NutrientStandard
  /** Alimentos da tela; só o preço deles muda. Os demais do arquivo aparecem como "fora da seleção". */
  selectedIds: number[]
  onApply: (prices: Record<number, number>) => void
}

/** Importa preços de um arquivo CSV (RF-22) e mostra o que foi aplicado e o que não pôde ser lido. */
export default function PriceImport({ standard, selectedIds, onApply }: Props) {
  const input = useRef<HTMLInputElement>(null)
  const [fx, setFx] = useState(Number.NaN)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [report, setReport] = useState<{ file: string; result: PriceImportResult; applied: number } | null>(null)

  const load = async (file: File) => {
    setBusy(true)
    setError(null)

    try {
      const result = await api.importPrices(standard, await file.text(), Number.isFinite(fx) ? fx : null)
      const chosen = new Set(selectedIds)
      const prices = Object.fromEntries(result.items.filter(i => chosen.has(i.id)).map(i => [i.id, i.price]))

      onApply(prices)
      setReport({ file: file.name, result, applied: Object.keys(prices).length })
    } catch (e) {
      setReport(null)
      setError((e instanceof Error ? e.message : 'Falha ao importar os preços').split('\n')[0])
    } finally {
      setBusy(false)

      if (input.current) input.current.value = ''
    }
  }

  const outside = report?.result.items.filter(i => !selectedIds.includes(i.id)) ?? []

  return (
    <div className='space-y-3'>
      <div className='flex flex-wrap items-end gap-2'>
        <Button variant='outline' size='sm' disabled={busy} onClick={() => input.current?.click()}>
          <UploadIcon /> {busy ? 'Importando…' : 'Importar preços (CSV)'}
        </Button>
        <input
          ref={input}
          type='file'
          accept='.csv,.txt,text/csv,text/plain'
          className='sr-only'
          aria-label='Arquivo CSV de preços'
          tabIndex={-1}
          onChange={e => {
            const file = e.target.files?.[0]

            if (file) void load(file)
          }}
        />
        <div className='flex flex-col gap-1'>
          <Label htmlFor='price-import-fx' className='text-xs'>
            Câmbio (R$ por US$)
          </Label>
          <NumberInput id='price-import-fx' className='h-8 w-28' step={0.01} min={0} value={fx} onChange={setFx} placeholder='se houver reais' />
        </div>
        <Button variant='ghost' size='sm' onClick={downloadTemplate}>
          <DownloadIcon /> Modelo
        </Button>
      </div>
      <p className='text-muted-foreground text-xs'>
        Colunas: <code>id</code> do RuFaS (ou <code>alimento</code>) e <code>preco</code>; opcionais <code>moeda</code> (USD ou BRL),{' '}
        <code>cambio</code>, <code>unidade_kg</code> (kg por saca ou tonelada) e <code>base</code> (MS ou MN). Tudo vira US$ por kg de MS.
      </p>

      {error && (
        <Alert variant='destructive'>
          <AlertTitle>Não foi possível importar</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {report && (
        <Alert>
          <AlertTitle>
            {report.file}: {report.applied} preço{report.applied === 1 ? '' : 's'} aplicado{report.applied === 1 ? '' : 's'}
          </AlertTitle>
          <AlertDescription>
            <div className='space-y-2'>
              <p>
                {report.result.items.length} linha{report.result.items.length === 1 ? '' : 's'} lida{report.result.items.length === 1 ? '' : 's'}
                {outside.length > 0 && `, ${outside.length} de alimento fora da seleção (não aplicad${outside.length === 1 ? 'a' : 'as'})`}
                {report.result.problems.length > 0 && `, ${report.result.problems.length} sem leitura`}.
              </p>
              {report.result.items.length > 0 && (
                <details>
                  <summary className='cursor-pointer'>Conferir a conversão</summary>
                  <ul className='mt-1 list-disc space-y-0.5 pl-4 text-xs'>
                    {report.result.items.map(item => (
                      <li key={item.id}>
                        {item.name} (id {item.id}): {item.original} → US$ {nf(item.price, 4)}/kg MS
                        {!selectedIds.includes(item.id) && ' · fora da seleção'}
                      </li>
                    ))}
                  </ul>
                </details>
              )}
              {report.result.problems.length > 0 && (
                <details open>
                  <summary className='cursor-pointer'>Linhas sem correspondência ou inválidas</summary>
                  <ul className='mt-1 list-disc space-y-0.5 pl-4 text-xs'>
                    {report.result.problems.map(problem => (
                      <li key={`${problem.line}-${problem.reason}`}>
                        Linha {problem.line} ({problem.text}): {problem.reason}
                      </li>
                    ))}
                  </ul>
                </details>
              )}
              {report.result.warnings.length > 0 && (
                <ul className='list-disc space-y-0.5 pl-4 text-xs'>
                  {report.result.warnings.map(warning => (
                    <li key={warning}>{warning}</li>
                  ))}
                </ul>
              )}
            </div>
          </AlertDescription>
        </Alert>
      )}
    </div>
  )
}

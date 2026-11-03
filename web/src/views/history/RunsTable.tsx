'use client'

import { useCallback, useEffect, useState } from 'react'

import { CheckCircle2Icon, ChevronLeftIcon, ChevronRightIcon, CopyIcon, DownloadIcon, EyeIcon, HistoryIcon, SearchIcon, StarIcon, Trash2Icon, XCircleIcon } from 'lucide-react'
import { toast } from 'sonner'

import { EmptyState } from '@/components/EmptyState'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Skeleton } from '@/components/ui/skeleton'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { api } from '@/lib/api'
import { KIND_LABEL, shortDate, summaryLine } from '@/lib/history'
import type { RunKind, RunMeta, RunPage } from '@/lib/types'
import { cn } from '@/lib/utils'

const KIND_STYLE: Record<RunKind, string> = {
  simulation: 'bg-brand/12 text-brand',
  sensitivity: 'bg-info/12 text-info',
  evaluation: 'bg-violet/12 text-violet',
  optimization: 'bg-warning/12 text-warning-text'
}

const KIND_ITEMS = [
  { value: 'all', label: 'Todos os tipos' },
  ...(Object.entries(KIND_LABEL) as [RunKind, string][]).map(([value, label]) => ({ value, label }))
]
const STATUS_ITEMS = [
  { value: 'all', label: 'Todos os estados' },
  { value: 'done', label: 'Concluídas' },
  { value: 'error', label: 'Com falha' }
]
const PAGE_SIZES = [10, 25, 50].map(n => ({ value: String(n), label: `${n} por página` }))

export function KindPill({ kind }: { kind: RunKind }) {
  return (
    <Badge variant='outline' className={cn('border-transparent', KIND_STYLE[kind])}>
      {KIND_LABEL[kind]}
    </Badge>
  )
}

export function StatusPill({ status }: { status: RunMeta['status'] }) {
  return status === 'done' ? (
    <Badge variant='secondary'>
      <CheckCircle2Icon aria-hidden /> Concluída
    </Badge>
  ) : (
    <Badge variant='destructive'>
      <XCircleIcon aria-hidden /> Falhou
    </Badge>
  )
}

interface Props {
  onView: (id: string) => void
  onDuplicate: (id: string) => void
  onExport: (id: string) => void
}

/** Tabela de execuções: busca, filtros, linhas por página, estrela do cenário-base, ações e paginação. */
export default function RunsTable({ onView, onDuplicate, onExport }: Props) {
  const [query, setQuery] = useState('')
  const [applied, setApplied] = useState('')
  const [kind, setKind] = useState('all')
  const [status, setStatus] = useState('all')
  const [perPage, setPerPage] = useState(10)
  const [page, setPage] = useState(1)
  const [data, setData] = useState<RunPage | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [reload, setReload] = useState(0)

  useEffect(() => {
    const timer = setTimeout(() => {
      setApplied(query.trim())
      setPage(1)
    }, 300)

    return () => clearTimeout(timer)
  }, [query])

  useEffect(() => {
    let cancelled = false

    api
      .history({ kind: kind === 'all' ? '' : (kind as RunKind), status: status === 'all' ? '' : status, q: applied, page, perPage })
      .then(result => {
        if (cancelled) return

        setData(result)
        setError(null)

        // a página sumiu (por exemplo, depois de excluir a última linha dela): volta para a última que existe
        if (result.items.length === 0 && result.total > 0 && page > result.pages) setPage(result.pages)
      })
      .catch(e => !cancelled && setError(e instanceof Error ? e.message.split('\n')[0] : 'Falha ao carregar o histórico'))

    return () => {
      cancelled = true
    }
  }, [kind, status, applied, page, perPage, reload])

  const toggleBase = useCallback(async (run: RunMeta) => {
    try {
      await api.setHistoryBase(run.id, !run.is_base)
      setReload(n => n + 1)
    } catch (e) {
      toast.error(e instanceof Error ? e.message.split('\n')[0] : 'Falha ao marcar o cenário-base')
    }
  }, [])

  const remove = useCallback(async (run: RunMeta) => {
    if (!window.confirm(`Excluir "${run.title}" (${shortDate(run.created)})? Isso não pode ser desfeito.`)) return

    try {
      await api.deleteHistory(run.id)
      toast.success('Execução excluída.')
      setReload(n => n + 1)
    } catch (e) {
      toast.error(e instanceof Error ? e.message.split('\n')[0] : 'Falha ao excluir')
    }
  }, [])

  const filtered = kind !== 'all' || status !== 'all' || applied !== ''

  if (error) return <p className='text-destructive text-sm' role='alert'>{error}</p>

  if (data && data.total === 0 && !filtered) {
    return (
      <EmptyState
        icon={HistoryIcon}
        title='Nenhuma execução ainda'
        steps={[
          'Rode uma simulação, uma análise de sensibilidade, uma avaliação de dietas ou a dieta ótima.',
          'Cada execução fica guardada aqui, com os parâmetros e o resultado.',
          'Marque uma simulação com a estrela para usá-la como cenário-base nos indicadores.'
        ]}
      />
    )
  }

  const first = data && data.total > 0 ? (data.page - 1) * data.per_page + 1 : 0
  const last = data ? Math.min(data.page * data.per_page, data.total) : 0

  return (
    <Card>
      <CardContent className='space-y-4'>
        <div className='flex flex-wrap items-center gap-2'>
          <div className='relative min-w-56 flex-1'>
            <SearchIcon className='text-muted-foreground pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2' />
            <Input
              type='search'
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder='Buscar por título, tipo, dieta ou código…'
              aria-label='Buscar execuções'
              className='pl-9'
            />
          </div>
          <Select value={kind} items={KIND_ITEMS} onValueChange={v => v && (setKind(v), setPage(1))}>
            <SelectTrigger className='w-48' aria-label='Filtrar por tipo'>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {KIND_ITEMS.map(item => (
                <SelectItem key={item.value} value={item.value}>
                  {item.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Select value={status} items={STATUS_ITEMS} onValueChange={v => v && (setStatus(v), setPage(1))}>
            <SelectTrigger className='w-44' aria-label='Filtrar por estado'>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {STATUS_ITEMS.map(item => (
                <SelectItem key={item.value} value={item.value}>
                  {item.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {!data ? (
          <div className='space-y-2' aria-busy='true'>
            {Array.from({ length: 5 }, (_, i) => (
              <Skeleton key={i} className='h-12 rounded-xl' />
            ))}
          </div>
        ) : data.items.length === 0 ? (
          <p className='text-muted-foreground py-10 text-center text-sm'>Nenhuma execução com esses filtros.</p>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className='w-10'>
                  <span className='sr-only'>Cenário-base</span>
                </TableHead>
                <TableHead className='min-w-56'>Execução</TableHead>
                <TableHead>Tipo</TableHead>
                <TableHead className='min-w-64'>Resultado</TableHead>
                <TableHead>Data</TableHead>
                <TableHead>Estado</TableHead>
                <TableHead className='text-right'>Ações</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {data.items.map(run => (
                <TableRow key={run.id}>
                  <TableCell>
                    <Button
                      variant='ghost'
                      size='icon-sm'
                      disabled={run.status !== 'done'}
                      aria-pressed={run.is_base}
                      aria-label={run.is_base ? 'Cenário-base: clique para desmarcar' : 'Marcar como cenário-base'}
                      title={run.is_base ? 'Cenário-base (clique para desmarcar)' : 'Marcar como cenário-base'}
                      onClick={() => toggleBase(run)}
                    >
                      <StarIcon className={cn(run.is_base && 'fill-warning text-warning')} />
                    </Button>
                  </TableCell>
                  <TableCell className='whitespace-normal'>
                    <button type='button' className='text-left font-medium underline-offset-4 hover:underline' onClick={() => onView(run.id)}>
                      {run.title}
                    </button>
                    <span className='text-muted-foreground block text-xs'>{run.id}</span>
                  </TableCell>
                  <TableCell>
                    <KindPill kind={run.kind} />
                  </TableCell>
                  <TableCell className='text-muted-foreground max-w-80 text-sm whitespace-normal'>{summaryLine(run)}</TableCell>
                  <TableCell className='text-muted-foreground tabular-nums'>{shortDate(run.created)}</TableCell>
                  <TableCell>
                    <StatusPill status={run.status} />
                  </TableCell>
                  <TableCell>
                    <div className='flex justify-end gap-0.5'>
                      <Button variant='ghost' size='icon-sm' aria-label='Ver detalhe' title='Ver detalhe' onClick={() => onView(run.id)}>
                        <EyeIcon />
                      </Button>
                      <Button variant='ghost' size='icon-sm' aria-label='Duplicar: abrir os parâmetros na tela' title='Duplicar: abrir os parâmetros na tela' onClick={() => onDuplicate(run.id)}>
                        <CopyIcon />
                      </Button>
                      <Button variant='ghost' size='icon-sm' aria-label='Exportar a execução (JSON)' title='Exportar a execução (JSON)' onClick={() => onExport(run.id)}>
                        <DownloadIcon />
                      </Button>
                      <Button variant='ghost' size='icon-sm' aria-label='Excluir' title='Excluir' className='hover:text-destructive' onClick={() => remove(run)}>
                        <Trash2Icon />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}

        {data && data.total > 0 && (
          <div className='flex flex-wrap items-center justify-between gap-3 text-sm'>
            <p className='text-muted-foreground'>
              Mostrando {first}–{last} de {data.total}
            </p>
            <div className='flex items-center gap-2'>
              <Select value={String(perPage)} items={PAGE_SIZES} onValueChange={v => v && (setPerPage(Number(v)), setPage(1))}>
                <SelectTrigger className='w-36' aria-label='Linhas por página'>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {PAGE_SIZES.map(item => (
                    <SelectItem key={item.value} value={item.value}>
                      {item.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Button variant='outline' size='icon' aria-label='Página anterior' disabled={data.page <= 1} onClick={() => setPage(data.page - 1)}>
                <ChevronLeftIcon />
              </Button>
              <span className='text-muted-foreground min-w-20 text-center tabular-nums'>
                {data.page} de {data.pages}
              </span>
              <Button variant='outline' size='icon' aria-label='Próxima página' disabled={data.page >= data.pages} onClick={() => setPage(data.page + 1)}>
                <ChevronRightIcon />
              </Button>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

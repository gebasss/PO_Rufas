'use client'

import { useEffect, useState, type ReactNode } from 'react'

import { ArrowLeftIcon, CopyIcon, DownloadIcon, StarIcon, Trash2Icon } from 'lucide-react'
import { toast } from 'sonner'

import { KpiCard } from '@/components/shared'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { api } from '@/lib/api'
import { KIND_LABEL, shortDate } from '@/lib/history'
import { nf, shortName, signedPct, usd } from '@/lib/format'
import type { ModuleEvaluation, ModuleOptimization, RunFull, SensResult, SimResult } from '@/lib/types'
import { cn } from '@/lib/utils'
import { useApp } from '@/providers/AppProvider'
import Results from '@/views/cow/Results'
import { KindPill, StatusPill } from '@/views/history/RunsTable'
import SensResults from '@/views/sensitivity/Results'

type Params = Record<string, unknown>

function KeyValue({ items }: { items: [string, ReactNode][] }) {
  return (
    <dl className='divide-border divide-y text-sm'>
      {items.map(([label, value]) => (
        <div key={label} className='flex items-start justify-between gap-4 py-2.5 first:pt-0 last:pb-0'>
          <dt className='text-muted-foreground'>{label}</dt>
          <dd className='text-right font-medium tabular-nums'>{value}</dd>
        </div>
      ))}
    </dl>
  )
}

const METHOD_LABEL: Record<string, string> = { grid: 'Grade (todas as combinações)', latin: 'Hipercubo latino' }

/** Parâmetros usados na execução, em listas legíveis (o JSON completo está na exportação). */
function ParamsCard({ run }: { run: RunFull }) {
  const { feedById } = useApp()
  const params = run.params as Params
  const prices = (params.prices ?? {}) as Record<string, number>
  const limits = (params.limits ?? {}) as Record<string, [number, number]>
  const ids = ((params.feeds ?? params.feed_ids ?? Object.keys(prices)) as (string | number)[]).map(String)
  const factors = (params.factors ?? []) as { key: string; label: string; low: number; high: number }[]
  const cow = Object.entries((params.cow ?? {}) as Record<string, unknown>)
  const override = Object.entries((params.requirements_override ?? {}) as Record<string, number>)
  const diets = (params.diets ?? []) as { name: string; amounts: Record<string, number> }[]
  const isModule = run.kind === 'evaluation' || run.kind === 'optimization'
  const nameOf = (id: string) => shortName(feedById[Number(id)]?.name ?? `Alimento ${id}`, 28)

  const general: [string, ReactNode][] = isModule
    ? [
        ['Padrão', String(params.standard ?? '—')],
        ['Categoria', String(params.category ?? '—')],
        ['Tipo de animal', String(params.animal_type ?? '—')],
        ...(run.kind === 'optimization'
          ? ([
              ['Resolução da busca', String(params.resolution ?? 'normal')],
              ['Execuções do RuFaS', String(params.seeds ?? 5)]
            ] as [string, ReactNode][])
          : [])
      ]
    : [
        ['Preço do leite', `${usd(Number(params.milk_price ?? 0), 3)}/kg`],
        ['Período', `${params.years ?? 1} ano${Number(params.years) > 1 ? 's' : ''}`],
        ['Vacas no rebanho', String(params.cow_num ?? 100)],
        ['Redução máxima de leite', `${nf(Number(params.max_milk_reduction ?? 0), 2)} kg/vaca/dia`],
        ...(run.kind === 'sensitivity'
          ? ([
              ['Método', METHOD_LABEL[String(params.method)] ?? String(params.method)],
              ['Níveis ou amostras', String(params.n ?? '—')]
            ] as [string, ReactNode][])
          : [])
      ]

  return (
    <div className='space-y-6'>
      <Card>
        <CardHeader>
          <CardTitle>Parâmetros usados</CardTitle>
          <CardDescription>Execução de {shortDate(run.created)}.</CardDescription>
        </CardHeader>
        <CardContent className='space-y-5'>
          <KeyValue items={general} />
          {factors.length > 0 && (
            <div className='space-y-2'>
              <h3 className='text-muted-foreground text-xs font-medium tracking-wider uppercase'>Fatores variados</h3>
              <KeyValue items={factors.map(f => [shortName(f.label, 30), `${nf(f.low, 3)} a ${nf(f.high, 3)}`])} />
            </div>
          )}
          {override.length > 0 && (
            <div className='space-y-2'>
              <h3 className='text-muted-foreground text-xs font-medium tracking-wider uppercase'>Exigências sobrescritas</h3>
              <KeyValue items={override.map(([key, value]) => [key, nf(value, 2)])} />
            </div>
          )}
          {cow.length > 0 && (
            <details>
              <summary className='text-muted-foreground cursor-pointer text-xs font-medium tracking-wider uppercase'>Vaca ({cow.length} campos)</summary>
              <div className='mt-2'>
                <KeyValue items={cow.map(([key, value]) => [key, String(value)])} />
              </div>
            </details>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Alimentos</CardTitle>
          <CardDescription>
            {ids.length} alimentos; preço em US$/kg de MS e limites em kg de MS por dia.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Alimento</TableHead>
                <TableHead className='text-right'>Preço</TableHead>
                <TableHead className='text-right'>Mín.</TableHead>
                <TableHead className='text-right'>Máx.</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {ids.map(id => (
                <TableRow key={id}>
                  <TableCell className='max-w-44 truncate'>{nameOf(id)}</TableCell>
                  <TableCell className='text-right tabular-nums'>{nf(prices[id], 3)}</TableCell>
                  <TableCell className='text-right tabular-nums'>{nf(limits[id]?.[0], 1)}</TableCell>
                  <TableCell className='text-right tabular-nums'>{nf(limits[id]?.[1], 1)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          {run.kind === 'evaluation' && diets.length > 0 && (
            <div className='mt-5 space-y-2'>
              <h3 className='text-muted-foreground text-xs font-medium tracking-wider uppercase'>Dietas avaliadas</h3>
              <KeyValue items={diets.map(d => [d.name, `${Object.keys(d.amounts).length} alimentos`])} />
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

function EvaluationResult({ result }: { result: ModuleEvaluation }) {
  const ranked = [...result.ranking].reverse().map(name => result.diets.find(d => d.name === name)!)
  const best = result.diets.find(d => d.name === result.best)

  return (
    <div className='space-y-6'>
      <div className='grid gap-3 sm:grid-cols-2'>
        <KpiCard tone='primary' label='Melhor entre as informadas' value={best ? best.name : 'Nenhuma viável'} hint={best ? `${usd(best.cost, 2)}/dia` : undefined} />
        <KpiCard label='Dietas viáveis' value={`${result.diets.filter(d => d.feasible).length} de ${result.diets.length}`} />
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Ranking</CardTitle>
          <CardDescription>Da mais para a menos recomendada.</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Posição</TableHead>
                <TableHead>Dieta</TableHead>
                <TableHead>Estado</TableHead>
                <TableHead className='text-right'>Custo (US$/dia)</TableHead>
                <TableHead className='text-right'>Violação</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {ranked.map((diet, index) => (
                <TableRow key={diet.name}>
                  <TableCell className='tabular-nums'>{index + 1}º</TableCell>
                  <TableCell className='font-medium'>{diet.name}</TableCell>
                  <TableCell>{diet.feasible ? (diet.incomplete ? 'Viável, incompleta' : 'Viável') : 'Inviável'}</TableCell>
                  <TableCell className='text-right tabular-nums'>{nf(diet.cost, 2)}</TableCell>
                  <TableCell className='text-right tabular-nums'>{diet.violation > 0 ? nf(diet.violation, 3) : '—'}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}

function OptimizationResult({ result }: { result: ModuleOptimization }) {
  const { feedById } = useApp()
  const diet = result.diet

  if (!diet) {
    return (
      <Alert>
        <AlertTitle>Sem dieta viável</AlertTitle>
        <AlertDescription>{result.message}</AlertDescription>
      </Alert>
    )
  }

  const rows = Object.entries(diet.amounts).sort((a, b) => b[1] - a[1])

  return (
    <div className='space-y-6'>
      <div className='grid gap-3 sm:grid-cols-2 xl:grid-cols-4'>
        <KpiCard tone='primary' label='Custo' value={`${usd(diet.cost, 2)}/dia`} />
        <KpiCard label='Consumo de MS' value={`${nf(diet.scalars.dmi, 2)} kg/dia`} />
        <KpiCard label='TDN · concentrado' value={`${nf(diet.scalars.tdn_percentage, 1)}% · ${nf(diet.scalars.concentrate_percentage, 1)}%`} />
        <KpiCard
          label='Em relação ao RuFaS'
          value={result.rufas?.lp_gap_pct != null ? signedPct(result.rufas.lp_gap_pct, 3) : '—'}
          hint={result.rufas?.cost_min != null ? `melhor do RuFaS ${usd(result.rufas.cost_min, 4)}` : 'sem execuções do RuFaS'}
        />
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Ração</CardTitle>
          <CardDescription>{diet.verified ? 'Confere com as restrições originais do RuFaS.' : 'Viola alguma restrição original do RuFaS.'}</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Alimento</TableHead>
                <TableHead className='text-right'>kg MS/dia</TableHead>
                <TableHead className='text-right'>% da dieta</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {rows.map(([id, kg]) => (
                <TableRow key={id}>
                  <TableCell>{shortName(feedById[Number(id)]?.name ?? `Alimento ${id}`, 40)}</TableCell>
                  <TableCell className='text-right tabular-nums'>{nf(kg, 2)}</TableCell>
                  <TableCell className='text-right tabular-nums'>{nf((100 * kg) / diet.scalars.dmi, 1)}%</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}

interface Props {
  id: string
  onBack: () => void
  onDuplicate: (id: string) => void
  onExport: (id: string) => void
  onDeleted: () => void
}

/** Tela de detalhe de uma execução: parâmetros usados e resultados lado a lado. */
export default function RunDetail({ id, onBack, onDuplicate, onExport, onDeleted }: Props) {
  const [run, setRun] = useState<RunFull | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [reload, setReload] = useState(0)

  useEffect(() => {
    let cancelled = false

    api
      .historyRun(id)
      .then(value => !cancelled && (setRun(value), setError(null)))
      .catch(e => !cancelled && setError(e instanceof Error ? e.message.split('\n')[0] : 'Falha ao carregar a execução'))

    return () => {
      cancelled = true
    }
  }, [id, reload])

  const toggleBase = async () => {
    if (!run) return

    try {
      await api.setHistoryBase(run.id, !run.is_base)
      setReload(n => n + 1)
    } catch (e) {
      toast.error(e instanceof Error ? e.message.split('\n')[0] : 'Falha ao marcar o cenário-base')
    }
  }

  const remove = async () => {
    if (!run || !window.confirm(`Excluir "${run.title}"? Isso não pode ser desfeito.`)) return

    try {
      await api.deleteHistory(run.id)
      toast.success('Execução excluída.')
      onDeleted()
    } catch (e) {
      toast.error(e instanceof Error ? e.message.split('\n')[0] : 'Falha ao excluir')
    }
  }

  if (error)
    return (
      <div className='space-y-4'>
        <Button variant='outline' size='sm' onClick={onBack}>
          <ArrowLeftIcon /> Voltar às execuções
        </Button>
        <Alert variant='destructive'>
          <AlertTitle>Não foi possível abrir a execução</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      </div>
    )

  if (!run)
    return (
      <div className='space-y-4' aria-busy='true'>
        <Skeleton className='h-10 w-72 rounded-xl' />
        <div className='grid gap-6 xl:grid-cols-[24rem_minmax(0,1fr)]'>
          <Skeleton className='h-96 rounded-[1.25rem]' />
          <Skeleton className='h-96 rounded-[1.25rem]' />
        </div>
      </div>
    )

  return (
    <div className='space-y-6'>
      <div className='flex flex-wrap items-center justify-between gap-3'>
        <div className='flex min-w-0 items-center gap-3'>
          <Button variant='outline' size='icon' aria-label='Voltar às execuções' onClick={onBack}>
            <ArrowLeftIcon />
          </Button>
          <div className='min-w-0'>
            <div className='flex flex-wrap items-center gap-2'>
              <h2 className='truncate text-xl font-bold tracking-tight'>{run.title}</h2>
              <KindPill kind={run.kind} />
              <StatusPill status={run.status} />
            </div>
            <p className='text-muted-foreground text-xs'>
              {KIND_LABEL[run.kind]} · {shortDate(run.created)} · {run.id}
            </p>
          </div>
        </div>
        <div className='flex flex-wrap items-center gap-2'>
          <Button variant='outline' size='sm' disabled={run.status !== 'done'} aria-pressed={run.is_base} onClick={toggleBase}>
            <StarIcon className={cn(run.is_base && 'fill-warning text-warning')} /> {run.is_base ? 'Cenário-base' : 'Marcar como base'}
          </Button>
          <Button variant='outline' size='sm' onClick={() => onDuplicate(run.id)}>
            <CopyIcon /> Duplicar
          </Button>
          <Button variant='outline' size='sm' onClick={() => onExport(run.id)}>
            <DownloadIcon /> Exportar
          </Button>
          <Button variant='outline' size='sm' className='hover:text-destructive' onClick={remove}>
            <Trash2Icon /> Excluir
          </Button>
        </div>
      </div>

      <div className='grid items-start gap-6 xl:grid-cols-[24rem_minmax(0,1fr)]'>
        <ParamsCard run={run} />
        <div className='min-w-0'>
          {run.status === 'error' || run.result === null ? (
            <Alert variant='destructive'>
              <AlertTitle>A execução falhou</AlertTitle>
              <AlertDescription>{run.error ?? 'Sem detalhes do erro.'}</AlertDescription>
            </Alert>
          ) : run.kind === 'simulation' ? (
            <Results sim={run.result as SimResult} />
          ) : run.kind === 'sensitivity' ? (
            <SensResults result={run.result as SensResult} years={Number((run.params as Record<string, unknown>).years) || undefined} />
          ) : run.kind === 'evaluation' ? (
            <EvaluationResult result={run.result as ModuleEvaluation} />
          ) : (
            <OptimizationResult result={run.result as ModuleOptimization} />
          )}
        </div>
      </div>
    </div>
  )
}

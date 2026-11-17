'use client'

import { useRef, useState } from 'react'

import { CoinsIcon, InfoIcon, ScaleIcon, TrendingDownIcon, WalletIcon } from 'lucide-react'
import { toast } from 'sonner'

import { SeriesLegend, TimeSeries } from '@/components/charts'
import ChartCard from '@/components/ChartCard'
import RunButton, { type RunState } from '@/components/RunButton'
import { KpiCard } from '@/components/shared'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Table, TableBody, TableCell, TableFooter, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { cancelJob, JobCancelledError, runJob } from '@/lib/api'
import { nf, shortName, usd } from '@/lib/format'
import type { LpRationResult, LpRationVariant, SimResult } from '@/lib/types'
import { useApp } from '@/providers/AppProvider'

const COLORS = { slsqp: 'var(--chart-2)', same: 'var(--chart-1)', free: 'var(--chart-3)' }

const messageOf = (error: unknown) => (error instanceof Error ? error.message : 'Falha na comparação').split('\n')[0]

/** Variação percentual do custo do LP em relação ao do RuFaS (negativa = o LP é mais barato). */
const change = (variant: LpRationVariant, slsqp: number) => (slsqp ? (variant.cost_per_cow_day / slsqp - 1) * 100 : 0)

interface Props {
  sim: SimResult
  /** Parâmetros (serializados) da simulação mostrada; é com eles que o servidor acha a simulação no cache. */
  simKey: string | null
  stale: boolean
}

/** Compara a ração do RuFaS (SLSQP) com a do LP nas mesmas exigências de cada intervalo da simulação (FSD, A.14). */
export default function LinearRationCard({ sim, simKey, stale }: Props) {
  const { connection, lp, setLp, trackTask } = useApp()
  const [running, setRunning] = useState(false)
  const [progress, setProgress] = useState({ done: 0, total: 0 })
  const [error, setError] = useState<string | null>(null)
  const [cancelling, setCancelling] = useState(false)
  const jobId = useRef<string | null>(null)

  const result: LpRationResult | null = lp?.result ?? null
  const outdated = lp !== null && lp.key !== simKey
  const state: RunState = running ? 'running' : error ? 'error' : result && !outdated ? 'done' : 'idle'

  const run = async () => {
    if (!simKey) return

    setRunning(true)
    setCancelling(false)
    setError(null)
    setProgress({ done: 0, total: 0 })

    const task = trackTask('Ração linear × RuFaS')

    try {
      const data = await runJob<LpRationResult>(
        'lp-ration',
        JSON.parse(simKey),
        (done, total) => {
          setProgress({ done, total })
          task.update(done, total)
        },
        { onStart: id => (jobId.current = id) }
      )

      setLp({ key: simKey, result: data })
      toast.success('Comparação concluída.')
    } catch (e) {
      if (e instanceof JobCancelledError) {
        toast.info('Comparação cancelada.')
      } else {
        setError(messageOf(e))
        toast.error(messageOf(e))
      }
    } finally {
      task.end()
      jobId.current = null
      setCancelling(false)
      setRunning(false)
    }
  }

  const cancel = () => {
    if (!jobId.current) return

    setCancelling(true)
    cancelJob(jobId.current).catch(e => {
      setCancelling(false)
      toast.error(messageOf(e))
    })
  }

  const summary = result?.summary
  const same = summary?.lp_same
  const free = summary?.lp_free
  const slsqp = summary?.slsqp_cost_per_cow_day ?? 0
  const nameOf = (id: string) => shortName(result?.feeds.find(f => String(f.id) === id)?.label ?? sim.feeds.find(f => String(f.id) === id)?.label ?? `Alimento ${id}`, 30)
  const usable = (result?.intervals ?? []).filter(row => row.lp_same && row.lp_free)

  const costData = usable.map(row => ({
    day: row.day,
    slsqp: row.slsqp.cost,
    same: row.lp_same?.cost ?? null,
    free: row.lp_free?.cost ?? null
  }))

  const feedIds = result ? [...new Set([...result.feed_ids.map(String)])] : []
  const compositionRows = feedIds
    .map(id => ({
      id,
      slsqp: summary?.slsqp_mean_amounts?.[id] ?? 0,
      same: same?.mean_amounts[id] ?? 0,
      free: free?.mean_amounts[id] ?? 0
    }))
    .filter(row => row.slsqp > 0.005 || row.same > 0.005 || row.free > 0.005)
    .sort((a, b) => b.slsqp + b.same + b.free - (a.slsqp + a.same + a.free))

  return (
    <div className='space-y-6'>
      <Card>
        <CardHeader>
          <CardTitle>Ração linear × ração do RuFaS</CardTitle>
          <CardDescription>
            A cada intervalo de 30 dias o RuFaS formula a ração do lote com um otimizador não linear (SLSQP). Aqui a
            programação linear resolve o mesmo problema, com as mesmas exigências, alimentos, preços e limites da simulação, e as
            duas rações são comparadas.
          </CardDescription>
        </CardHeader>
        <CardContent className='space-y-4'>
          <RunButton
            state={state}
            progress={progress}
            label='Comparar com a ração linear'
            unit='etapas'
            error={error}
            disabled={connection !== 'online' || !simKey || stale}
            onRun={run}
            onCancel={cancel}
            cancelling={cancelling}
          />
          <p className='text-muted-foreground text-xs'>
            {stale
              ? 'Os parâmetros mudaram desde a simulação: simule de novo para comparar.'
              : 'Não roda uma nova simulação: usa as exigências e a ração desta. Leva cerca de 11 segundos por intervalo (2 a 3 minutos em 1 ano).'}
          </p>
        </CardContent>
      </Card>

      {result && summary && summary.intervals_used > 0 && same && free ? (
        <div className={outdated || stale ? 'space-y-6 opacity-60 transition-opacity' : 'space-y-6 transition-opacity'}>
          {outdated && (
            <p className='text-muted-foreground text-sm' role='status'>
              Esta comparação é de outra simulação. Clique em Comparar para atualizar.
            </p>
          )}

          <div className='grid gap-3 sm:grid-cols-2 2xl:grid-cols-3'>
            <KpiCard
              icon={CoinsIcon}
              color='warning'
              label='Ração do RuFaS (SLSQP)'
              value={`${usd(slsqp, 2)}/dia`}
              hint={`por vaca, ${nf(summary.slsqp_dmi, 1)} kg de MS`}
            />
            <KpiCard
              tone='primary'
              icon={ScaleIcon}
              label='Ração linear, mesmo consumo'
              value={`${usd(same.cost_per_cow_day, 2)}/dia`}
              delta={change(same, slsqp)}
              better='down'
              hint={`${nf(same.dmi, 1)} kg de MS`}
            />
            <KpiCard
              icon={TrendingDownIcon}
              color='info'
              label='Ração linear, consumo livre'
              value={`${usd(free.cost_per_cow_day, 2)}/dia`}
              delta={change(free, slsqp)}
              better='down'
              hint={`${nf(free.dmi, 1)} kg de MS`}
            />
            <KpiCard
              tone='primary'
              icon={WalletIcon}
              label='Diferença do rebanho, mesmo consumo'
              value={usd(same.herd_saving)}
              hint={`RuFaS menos linear, em ${nf(summary.days, 0)} dias e ${nf(summary.mean_cows, 0)} vacas em lactação; positivo = o linear custa menos`}
            />
            <KpiCard
              icon={WalletIcon}
              color='info'
              label='Diferença do rebanho, consumo livre'
              value={usd(free.herd_saving)}
              hint='o consumo pode subir até o limite do RuFaS'
            />
          </div>

          {result.warnings.length > 0 && (
            <Alert>
              <InfoIcon />
              <AlertTitle>Atenção</AlertTitle>
              <AlertDescription>
                <ul className='list-disc pl-4'>
                  {result.warnings.map(text => (
                    <li key={text}>{text}</li>
                  ))}
                </ul>
              </AlertDescription>
            </Alert>
          )}

          <ChartCard
            title='Custo da ração por intervalo'
            description='US$ por vaca em lactação por dia, a cada intervalo de 30 dias, com as mesmas exigências.'
            chart={
              <>
                <TimeSeries
                  data={costData}
                  xKey='day'
                  series={[
                    { key: 'slsqp', label: 'RuFaS (SLSQP)', color: COLORS.slsqp, kind: 'line' },
                    { key: 'same', label: 'Linear, mesmo consumo', color: COLORS.same, kind: 'line' },
                    { key: 'free', label: 'Linear, consumo livre', color: COLORS.free, kind: 'line', dashed: true }
                  ]}
                  format={value => nf(value, 2)}
                  height={240}
                />
                <SeriesLegend
                  series={[
                    { label: 'RuFaS (SLSQP)', color: COLORS.slsqp },
                    { label: 'Linear, mesmo consumo', color: COLORS.same },
                    { label: 'Linear, consumo livre', color: COLORS.free }
                  ]}
                />
              </>
            }
            table={
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Dia</TableHead>
                    <TableHead className='text-right'>RuFaS</TableHead>
                    <TableHead className='text-right'>Linear, mesmo consumo</TableHead>
                    <TableHead className='text-right'>Linear, consumo livre</TableHead>
                    <TableHead className='text-right'>Restrições do RuFaS</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {usable.map(row => (
                    <TableRow key={row.day}>
                      <TableCell>{row.day}</TableCell>
                      <TableCell className='text-right tabular-nums'>{nf(row.slsqp.cost, 2)}</TableCell>
                      <TableCell className='text-right tabular-nums'>{nf(row.lp_same?.cost, 2)}</TableCell>
                      <TableCell className='text-right tabular-nums'>{nf(row.lp_free?.cost, 2)}</TableCell>
                      <TableCell className='text-right'>{row.lp_same?.verified && row.lp_free?.verified ? 'atendidas' : 'conferir'}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            }
          />

          <Card>
            <CardHeader>
              <CardTitle>Ração média</CardTitle>
              <CardDescription>kg de matéria seca por vaca por dia, média ponderada pelos dias de cada intervalo.</CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Alimento</TableHead>
                    <TableHead className='text-right'>RuFaS</TableHead>
                    <TableHead className='text-right'>Linear, mesmo consumo</TableHead>
                    <TableHead className='text-right'>Linear, consumo livre</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {compositionRows.map(row => (
                    <TableRow key={row.id}>
                      <TableCell>{nameOf(row.id)}</TableCell>
                      <TableCell className='text-right tabular-nums'>{nf(row.slsqp, 2)}</TableCell>
                      <TableCell className='text-right tabular-nums'>{nf(row.same, 2)}</TableCell>
                      <TableCell className='text-right tabular-nums'>{nf(row.free, 2)}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
                <TableFooter>
                  <TableRow>
                    <TableCell>Consumo total</TableCell>
                    <TableCell className='text-right tabular-nums'>{nf(summary.slsqp_dmi, 2)}</TableCell>
                    <TableCell className='text-right tabular-nums'>{nf(same.dmi, 2)}</TableCell>
                    <TableCell className='text-right tabular-nums'>{nf(free.dmi, 2)}</TableCell>
                  </TableRow>
                </TableFooter>
              </Table>
            </CardContent>
          </Card>

          <Alert>
            <InfoIcon />
            <AlertTitle>Como ler esta comparação</AlertTitle>
            <AlertDescription>
              <ul className='list-disc space-y-1 pl-4'>
                <li>
                  As exigências são as que o RuFaS usou em cada intervalo, e cada ração do LP atende a todas as restrições
                  originais do RuFaS ({same.all_verified && free.all_verified ? 'conferido em todos os intervalos' : 'há intervalos a conferir'}).
                </li>
                <li>
                  <strong>Mesmo consumo</strong> é a comparação mais conservadora: o LP come o mesmo que o SLSQP escolheu. No
                  <strong> consumo livre</strong> o LP também pode usar a folga de até +30% sobre o consumo estimado que o RuFaS
                  permite, o que baixa mais o custo; se as vacas não comerem tanto, vale o mesmo consumo.
                </li>
                <li>
                  <strong>O esperado é um empate.</strong> O SLSQP do RuFaS já chega perto do ótimo da ração: no total as
                  diferenças são de centésimos de ponto percentual, com intervalos em que o linear custa um pouco menos e outros
                  em que custa um pouco mais. O que o linear acrescenta não é um custo menor, e sim um resultado que não
                  depende do ponto inicial aleatório do SLSQP e os preços-sombra (aba Ruminante Singular).
                </li>
                <li>
                  O leite não é simulado de novo: o RuFaS só reduz o leite quando a ração não atende, e as rações do LP atendem. O
                  custo é o da ração formulada (preço × quantidade), como no indicador da aba Visão geral.
                </li>
                <li>Só vale para o padrão NRC 2001 e para as vacas em lactação.</li>
              </ul>
            </AlertDescription>
          </Alert>
        </div>
      ) : result ? (
        <Alert variant='destructive'>
          <InfoIcon />
          <AlertTitle>Sem comparação</AlertTitle>
          <AlertDescription>O LP não achou ração viável nos intervalos desta simulação.</AlertDescription>
        </Alert>
      ) : null}
    </div>
  )
}

'use client'

import { useRef, useState } from 'react'

import { CoinsIcon, InfoIcon, ScaleIcon, TrendingDownIcon, TrendingUpIcon } from 'lucide-react'
import { toast } from 'sonner'

import { DivergingBars } from '@/components/charts'
import ChartCard from '@/components/ChartCard'
import RunButton, { type RunState } from '@/components/RunButton'
import { KpiCard } from '@/components/shared'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { cancelJob, JobCancelledError, runJob } from '@/lib/api'
import { nf, shortName, signedPct, usd } from '@/lib/format'
import type { SensLpResult } from '@/lib/types'
import { useApp } from '@/providers/AppProvider'

const messageOf = (error: unknown) => (error instanceof Error ? error.message : 'Falha na comparação').split('\n')[0]

/** Eixo do gráfico: ±1% (as diferenças medidas ficam em centésimos de ponto percentual; o rótulo mostra o valor real). */
const DOMAIN: [number, number] = [-1, 1]

/** Economia do LP em % (positiva = o linear custa menos): é o contrário da diferença `diff_pct` do servidor, e o verde do gráfico vira "melhor". */
const saving = (diffPct: number | undefined) => -(diffPct ?? 0)

interface Props {
  /** Corpo (serializado) da análise mostrada; é com ele que o servidor refaz os cenários e acha as simulações no cache. */
  sensKey: string | null
  stale: boolean
}

/** Compara a ração do RuFaS (SLSQP) com a do LP em cada cenário da análise de sensibilidade (FSD, A.15). */
export default function SensLinearRationCard({ sensKey, stale }: Props) {
  const { connection, sensLp, setSensLp, trackTask } = useApp()
  const [running, setRunning] = useState(false)
  const [progress, setProgress] = useState({ done: 0, total: 0 })
  const [error, setError] = useState<string | null>(null)
  const [cancelling, setCancelling] = useState(false)
  const jobId = useRef<string | null>(null)

  const result: SensLpResult | null = sensLp?.result ?? null
  const outdated = sensLp !== null && sensLp.key !== sensKey
  const state: RunState = running ? 'running' : error ? 'error' : result && !outdated ? 'done' : 'idle'

  const run = async () => {
    if (!sensKey) return

    setRunning(true)
    setCancelling(false)
    setError(null)
    setProgress({ done: 0, total: 0 })

    const task = trackTask('Ração linear × RuFaS (sensibilidade)')

    try {
      const data = await runJob<SensLpResult>(
        'sens-lp-ration',
        JSON.parse(sensKey),
        (done, total) => {
          setProgress({ done, total })
          task.update(done, total)
        },
        { onStart: id => (jobId.current = id) }
      )

      setSensLp({ key: sensKey, result: data })
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
  const compared = (result?.rows ?? []).filter(row => row.intervals_used)
  const label = (row: SensLpResult['rows'][number]) =>
    row.cenarios.length > 1 ? `${row.cenarios[0]} a ${row.cenarios[row.cenarios.length - 1]}` : row.cenarios[0]
  const bars = compared.map(row => ({ name: label(row), value: saving(row.diff_pct) }))
  const priceNames = result?.rows[0] ? Object.keys(result.rows[0].precos) : []

  return (
    <div className='space-y-6'>
      <Card>
        <CardHeader>
          <CardTitle>Ração linear × ração do RuFaS em cada cenário</CardTitle>
          <CardDescription>
            Para cada simulação da análise, a programação linear resolve a ração de menor custo com as mesmas exigências que o RuFaS usou
            e compara com a ração do SLSQP. Mostra se o empate medido na tela Vaca leiteira se mantém quando os preços mudam.
          </CardDescription>
        </CardHeader>
        <CardContent className='space-y-4'>
          <RunButton
            state={state}
            progress={progress}
            label='Comparar com a ração linear'
            unit='cenários'
            error={error}
            disabled={connection !== 'online' || !sensKey || stale}
            onRun={run}
            onCancel={cancel}
            cancelling={cancelling}
          />
          <p className='text-muted-foreground text-xs'>
            {stale
              ? 'Os fatores ou os parâmetros mudaram desde a análise: execute-a de novo para comparar.'
              : 'Não roda novas simulações: usa as da análise. Compara 4 intervalos por simulação, com o mesmo consumo do RuFaS. Leva de 20 a 45 segundos por simulação.'}
          </p>
        </CardContent>
      </Card>

      {result && summary && summary.compared > 0 ? (
        <div className={outdated || stale ? 'space-y-6 opacity-60 transition-opacity' : 'space-y-6 transition-opacity'}>
          {outdated && (
            <p className='text-muted-foreground text-sm' role='status'>
              Esta comparação é de outra análise. Clique em Comparar para atualizar.
            </p>
          )}

          <div className='grid gap-3 sm:grid-cols-2 2xl:grid-cols-3'>
            <KpiCard
              tone='primary'
              icon={ScaleIcon}
              label='Economia média do LP'
              value={signedPct(saving(summary.mean_diff_pct), 3)}
              hint={`no custo da ração, em ${summary.compared} simulações; positiva = o linear custa menos`}
            />
            <KpiCard
              icon={TrendingDownIcon}
              color='info'
              label='Melhor caso do LP'
              value={signedPct(saving(summary.min_diff_pct), 3)}
              hint='economia na simulação em que o linear foi mais barato'
            />
            <KpiCard
              icon={TrendingUpIcon}
              color='warning'
              label='Pior caso do LP'
              value={signedPct(saving(summary.max_diff_pct), 3)}
              hint='na simulação em que o linear foi mais caro (negativa = custou mais)'
            />
            <KpiCard
              icon={CoinsIcon}
              color='violet'
              label='Empates'
              value={`${summary.tie} de ${summary.compared}`}
              hint={`diferença de até ${nf(summary.tie_pct, 1)}%; LP mais barato em ${summary.lp_cheaper} e mais caro em ${summary.lp_dearer}`}
            />
          </div>

          {(summary.failed > 0 || !summary.all_verified) && (
            <Alert>
              <InfoIcon />
              <AlertTitle>Atenção</AlertTitle>
              <AlertDescription>
                <ul className='list-disc pl-4'>
                  {summary.failed > 0 && <li>{summary.failed} simulação(ões) do RuFaS falharam e ficaram fora da comparação.</li>}
                  {!summary.all_verified && <li>Alguma ração do LP não atendeu a uma restrição original do RuFaS: confira a tabela.</li>}
                </ul>
              </AlertDescription>
            </Alert>
          )}

          <ChartCard
            title='Economia do LP no custo da ração, por simulação'
            description='Quanto o custo da ração do linear fica abaixo do RuFaS (%), por vaca por dia; positiva = o linear custa menos. Eixo de −1% a +1%.'
            chart={<DivergingBars data={bars} format={value => signedPct(value, 3)} domain={DOMAIN} height={Math.max(220, bars.length * 40 + 30)} />}
            table={
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Cenários</TableHead>
                    {priceNames.map(name => (
                      <TableHead key={name} className='text-right'>
                        {shortName(name, 18)}
                      </TableHead>
                    ))}
                    <TableHead className='text-right'>RuFaS (US$/vaca/dia)</TableHead>
                    <TableHead className='text-right'>Linear (US$/vaca/dia)</TableHead>
                    <TableHead className='text-right'>Economia do LP</TableHead>
                    <TableHead className='text-right'>Restrições do RuFaS</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {result.rows.map(row => (
                    <TableRow key={row.cenarios.join('-')}>
                      <TableCell>{label(row)}</TableCell>
                      {priceNames.map(name => (
                        <TableCell key={name} className='text-right tabular-nums'>
                          {nf(row.precos[name], 3)}
                        </TableCell>
                      ))}
                      {row.intervals_used ? (
                        <>
                          <TableCell className='text-right tabular-nums'>{usd(row.slsqp_cost, 3)}</TableCell>
                          <TableCell className='text-right tabular-nums'>{usd(row.lp_cost, 3)}</TableCell>
                          <TableCell className='text-right tabular-nums'>{signedPct(saving(row.diff_pct), 3)}</TableCell>
                          <TableCell className='text-right'>{row.verified ? 'atendidas' : 'conferir'}</TableCell>
                        </>
                      ) : (
                        <TableCell colSpan={4} className='text-destructive text-right'>
                          {row.erro ? 'falhou' : 'sem ração viável no LP'}
                        </TableCell>
                      )}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            }
          />

          <Alert>
            <InfoIcon />
            <AlertTitle>Como ler esta comparação</AlertTitle>
            <AlertDescription>
              <ul className='list-disc space-y-1 pl-4'>
                <li>
                  Cada linha é uma simulação da análise (uma combinação de preços de alimentos); cenários que só diferem no preço do leite
                  compartilham a simulação. O custo é o da ração formulada (preço × quantidade), em média de {result.sample} intervalos
                  igualmente espaçados, ponderada pelos dias.
                </li>
                <li>
                  <strong>O esperado é um empate</strong>, mesmo com preços muito diferentes: o SLSQP do RuFaS já chega perto do ótimo da
                  ração. O que o linear acrescenta é um resultado que não depende do ponto inicial aleatório e os preços-sombra.
                </li>
                <li>O LP usa o mesmo consumo que o RuFaS escolheu e atende às restrições originais do RuFaS (coluna da tabela). O leite não é simulado de novo.</li>
                <li>Só vale para o padrão NRC 2001.</li>
              </ul>
            </AlertDescription>
          </Alert>
        </div>
      ) : result ? (
        <Alert variant='destructive'>
          <InfoIcon />
          <AlertTitle>Sem comparação</AlertTitle>
          <AlertDescription>Nenhuma simulação da análise teve ração viável no LP.</AlertDescription>
        </Alert>
      ) : null}
    </div>
  )
}

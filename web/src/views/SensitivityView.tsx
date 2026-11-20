'use client'

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import Link from 'next/link'

import { AlertTriangleIcon, SlidersHorizontalIcon } from 'lucide-react'
import { toast } from 'sonner'

import { EmptyState, ResultsSkeleton } from '@/components/EmptyState'
import { feedTitle } from '@/components/FeedPicker'
import RunButton, { type RunState } from '@/components/RunButton'
import { finite, NumberInput, PageHeader } from '@/components/shared'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Checkbox } from '@/components/ui/checkbox'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { api, cancelJob, JobCancelledError, runJob } from '@/lib/api'
import { DEFAULT_HERD, herdProblem, secondsPerSimulation } from '@/lib/herd'
import { DEFAULT_SENS_LIMITS, maxLevels, sensitivityPlan, sensitivityProblem } from '@/lib/sensitivity'
import type { RunMeta, SensFactor, SensFactorState as FactorState, SensResult } from '@/lib/types'
import { useApp } from '@/providers/AppProvider'
import { COW_STANDARD, standardName } from '@/views/module/model'
import { simulationBody } from '@/views/CowView'
import SensLinearRationCard from '@/views/sensitivity/LinearRationCard'
import SensResults from '@/views/sensitivity/Results'

const METHODS = [
  { value: 'grid', label: 'Grade (todas as combinações)' },
  { value: 'latin', label: 'Hipercubo latino' }
]
const MILK = 'milk_price'

const messageOf = (error: unknown) => (error instanceof Error ? error.message : 'Falha na análise').split('\n')[0]
const showResults = () => document.getElementById('resultados')?.scrollIntoView({ behavior: 'smooth', block: 'start' })

export default function SensitivityView() {
  const { connection, defaults, selected, feedById, params, sim, sens, setSens, sensKey, setSensKey, sensSetup, setSensSetup, trackTask } = useApp()
  const limits = defaults?.sensitivity ?? DEFAULT_SENS_LIMITS
  const { overrides, method, levels } = sensSetup
  const setOverrides = (change: (previous: Record<string, FactorState>) => Record<string, FactorState>) =>
    setSensSetup(s => ({ ...s, overrides: change(s.overrides) }))
  const setMethod = (value: string) => setSensSetup(s => ({ ...s, method: value }))
  const setLevels = (value: number) => setSensSetup(s => ({ ...s, levels: value }))
  const [running, setRunning] = useState(false)
  const [progress, setProgress] = useState({ done: 0, total: 0, status: 'queued' })
  const [error, setError] = useState<string | null>(null)
  const [base, setBase] = useState<RunMeta | null>(null)
  const [cancelling, setCancelling] = useState(false)
  const jobId = useRef<string | null>(null)

  // simulação-base (D3): linha de referência dos gráficos e delta da melhor margem
  const loadBase = useCallback(() => {
    api
      .historyBase('simulation')
      .then(setBase)
      .catch(() => setBase(null))
  }, [])

  useEffect(() => {
    if (connection === 'online') loadBase()
  }, [connection, loadBase])

  // Fatores ligados de início: os dois alimentos que mais pesam no custo (kg da última simulação × preço); sem simulação,
  // os dois de maior preço. O usuário muda isso à vontade.
  const heaviest = useMemo(() => {
    const weights = Object.entries(selected).map(([id, s]) => ({ id, weight: (sim ? (sim.average_ration[id] ?? 0) : 1) * s.price }))

    return new Set(weights.sort((a, b) => b.weight - a.weight).slice(0, 2).map(w => w.id))
  }, [selected, sim])

  const rows = useMemo(() => {
    const list = Object.entries(selected).map(([id, s]) => ({
      key: id,
      label: feedById[Number(id)] ? feedTitle(feedById[Number(id)]) : id,
      defaults: { on: heaviest.has(id), low: +(s.price * 0.5).toFixed(3), high: +(s.price * 1.5).toFixed(3) }
    }))

    list.push({
      key: MILK,
      label: 'Preço do leite (US$/kg)',
      defaults: { on: true, low: +(finite(params.milkPrice, 0.45) * 0.8).toFixed(3), high: +(finite(params.milkPrice, 0.45) * 1.2).toFixed(3) }
    })

    return list
  }, [selected, feedById, params.milkPrice, heaviest])

  const stateOf = (key: string, defaults: FactorState) => overrides[key] ?? defaults
  const patch = (key: string, defaults: FactorState, change: Partial<FactorState>) =>
    setOverrides(prev => ({ ...prev, [key]: { ...(prev[key] ?? defaults), ...change } }))

  const factors: SensFactor[] = rows
    .filter(r => stateOf(r.key, r.defaults).on)
    .map(r => ({ key: r.key, label: r.label, low: finite(stateOf(r.key, r.defaults).low), high: finite(stateOf(r.key, r.defaults).high) }))

  const top = maxLevels(method, limits)
  const levelsProblem =
    Number.isInteger(levels) && levels >= limits.min_levels && levels <= top
      ? null
      : `Use um número inteiro de ${limits.min_levels} a ${top} ${method === 'grid' ? 'níveis' : 'amostras'}.`
  const n = Math.max(limits.min_levels, Math.min(top, Math.round(finite(levels, limits.min_levels))))
  const feedFactors = factors.filter(f => f.key !== MILK).length
  const plan = sensitivityPlan(feedFactors, factors.length, method, n)
  const sizeProblem = levelsProblem ? null : sensitivityProblem(plan, limits)

  const body = useMemo(
    () => ({ ...simulationBody(selected, params), factors, method, n }),
    // `factors` é derivado de `rows`, `overrides`; a chave serializada abaixo cobre a identidade
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [selected, params, JSON.stringify(factors), method, n]
  )
  const bodyKey = JSON.stringify(body)
  const stale = sens !== null && sensKey !== null && sensKey !== bodyKey
  const state: RunState = running ? 'running' : error ? 'error' : sens && !stale ? 'done' : 'idle'
  const herdError = herdProblem(params.cowNum, defaults?.herd ?? DEFAULT_HERD)
  const blocked = !factors.length || connection !== 'online' || Object.keys(selected).length < 3 || herdError !== null || levelsProblem !== null || sizeProblem !== null

  const run = async () => {
    setRunning(true)
    setCancelling(false)
    setError(null)
    setProgress({ done: 0, total: 0, status: 'queued' })

    const task = trackTask('Análise de sensibilidade')

    try {
      const result = await runJob<SensResult>(
        'sensitivity',
        body,
        (done, total, status) => {
          setProgress({ done, total, status })
          task.update(done, total)
        },
        { onStart: id => (jobId.current = id) }
      )

      setSens(result)
      setSensKey(bodyKey)
      toast.success('Análise concluída.')
    } catch (e) {
      if (e instanceof JobCancelledError) {
        toast.info('Análise cancelada.')
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

  const runButton = (
    <div className='space-y-2'>
      {sizeProblem ? (
        <p className='text-destructive text-xs' role='alert'>
          {sizeProblem}
        </p>
      ) : levelsProblem ? (
        <p className='text-muted-foreground text-xs'>Corrija o número de níveis para ver a estimativa.</p>
      ) : (
        <p className='text-muted-foreground text-xs' aria-live='polite'>
          {factors.length
            ? `${plan.scenarios} cenários, até ${plan.simulations} simulações do RuFaS (cerca de ${Math.max(1, Math.ceil((plan.simulations * secondsPerSimulation(params.cowNum)) / 60))} min).`
            : 'Marque ao menos um fator.'}{' '}
          Rebanho de {params.cowNum} vacas e padrão {standardName(COW_STANDARD)}, como na tela Vaca leiteira.
        </p>
      )}
      {herdError && (
        <p className='text-destructive text-xs' role='alert'>
          {herdError} Ajuste na tela Vaca leiteira.
        </p>
      )}
      <RunButton
        state={state}
        progress={progress}
        label='Executar sensibilidade'
        unit='simulações do RuFaS'
        error={error}
        disabled={blocked}
        onRun={run}
        onView={showResults}
        onCancel={cancel}
        cancelling={cancelling}
      />
    </div>
  )

  return (
    <>
      <PageHeader
        title='Sensibilidade (RuFaS)'
        description='Varia preços de alimentos e do leite, roda o RuFaS para cada combinação e mostra como a margem reage. Cada combinação de preços de alimentos exige uma simulação; o preço do leite só recalcula a receita.'
      />

      <div className='grid items-start gap-6 max-xl:pb-32 xl:grid-cols-[24rem_minmax(0,1fr)]'>
        <Card className='xl:sticky xl:top-24 xl:max-h-[calc(100dvh-7rem)]'>
          <CardHeader>
            <CardTitle>Fatores</CardTitle>
            <CardDescription>
              Usa os alimentos escolhidos na aba{' '}
              <Link href='/vaca' className='text-brand underline-offset-4 hover:underline'>
                Vaca leiteira
              </Link>
              . Marque o que variar e informe a faixa.
            </CardDescription>
          </CardHeader>
          <CardContent className='min-h-0 flex-1 space-y-5 overflow-y-auto'>
            <div className='space-y-2'>
              <div className='text-muted-foreground grid grid-cols-[1.25rem_1fr_4.5rem_4.5rem] gap-2 text-[11px]'>
                <span />
                <span>Fator</span>
                <span className='text-right'>De</span>
                <span className='text-right'>Até</span>
              </div>
              {rows.map(r => {
                const s = stateOf(r.key, r.defaults)

                return (
                  <div key={r.key} className='grid grid-cols-[1.25rem_1fr_4.5rem_4.5rem] items-center gap-2'>
                    <Checkbox checked={s.on} aria-label={`Variar ${r.label}`} onCheckedChange={v => patch(r.key, r.defaults, { on: !!v })} />
                    <span className='text-xs leading-snug' title={r.label}>
                      {r.label}
                    </span>
                    <NumberInput className='h-8 px-1.5 text-xs' value={s.low} onChange={v => patch(r.key, r.defaults, { low: v })} aria-label={`${r.label}, mínimo`} />
                    <NumberInput className='h-8 px-1.5 text-xs' value={s.high} onChange={v => patch(r.key, r.defaults, { high: v })} aria-label={`${r.label}, máximo`} />
                  </div>
                )
              })}
            </div>

            <div className='grid grid-cols-2 gap-3'>
              <div className='space-y-1.5'>
                <Label>Método</Label>
                <Select value={method} items={METHODS} onValueChange={v => v && setMethod(v)}>
                  <SelectTrigger className='w-full'>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {METHODS.map(m => (
                      <SelectItem key={m.value} value={m.value}>
                        {m.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className='space-y-1.5'>
                <Label>Níveis / amostras</Label>
                <NumberInput
                  step={1}
                  min={limits.min_levels}
                  value={levels}
                  onChange={setLevels}
                  aria-label='Níveis ou amostras'
                  aria-invalid={levelsProblem !== null}
                  aria-describedby='sens-levels-hint'
                />
                <p id='sens-levels-hint' className={levelsProblem ? 'text-destructive text-xs' : 'text-muted-foreground text-xs'} role={levelsProblem ? 'alert' : undefined}>
                  {levelsProblem ?? `De ${limits.min_levels} a ${top}.`}
                </p>
              </div>
            </div>
          </CardContent>
          <CardFooter className='border-t pt-(--card-spacing) max-xl:hidden'>
            <div className='w-full'>{runButton}</div>
          </CardFooter>
        </Card>

        <div className='min-w-0 space-y-6'>
          {state === 'error' && (
            <Alert variant='destructive'>
              <AlertTriangleIcon />
              <AlertTitle>A análise não terminou</AlertTitle>
              <AlertDescription>{error} Confira os alimentos, as faixas dos fatores e a conexão com o servidor.</AlertDescription>
            </Alert>
          )}

          {sens ? (
            <div id='resultados' className='scroll-mt-24'>
              <SensResults result={sens} stale={stale} base={base} years={params.years} cowNum={params.cowNum} linear={<SensLinearRationCard sensKey={sensKey} stale={stale} />} />
            </div>
          ) : running ? (
            <ResultsSkeleton />
          ) : (
            <EmptyState
              icon={SlidersHorizontalIcon}
              title='Nenhuma análise ainda'
              steps={[
                'Marque os fatores que vão variar (preços dos alimentos e do leite) e informe a faixa de cada um.',
                'Escolha o método e os níveis, e clique em Executar sensibilidade: cada simulação leva cerca de 17 segundos com 100 vacas (um pouco mais com rebanhos maiores).',
                'Veja o cenário ótimo, a distribuição das margens e o efeito de cada fator, e exporte o relatório.'
              ]}
            />
          )}
        </div>
      </div>

      <div className='bg-card/90 border-border fixed inset-x-3 bottom-3 z-30 rounded-2xl border p-2 backdrop-blur-xl xl:hidden'>{runButton}</div>
    </>
  )
}

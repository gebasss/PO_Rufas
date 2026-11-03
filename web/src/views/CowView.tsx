'use client'

import { useCallback, useEffect, useMemo, useState } from 'react'

import { AlertTriangleIcon, MilkIcon } from 'lucide-react'
import { toast } from 'sonner'

import { EmptyState, ResultsSkeleton } from '@/components/EmptyState'
import FeedPicker from '@/components/FeedPicker'
import RunButton, { type RunState } from '@/components/RunButton'
import ScenarioFile from '@/components/ScenarioFile'
import { finite, NumberInput, PageHeader } from '@/components/shared'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { api, runJob } from '@/lib/api'
import type { CowScenario, RunMeta, SimResult } from '@/lib/types'
import { useApp } from '@/providers/AppProvider'
import Results from '@/views/cow/Results'

const YEARS = [
  { value: '1', label: '1 ano' },
  { value: '2', label: '2 anos' }
]

export function simulationBody(
  selected: ReturnType<typeof useApp>['selected'],
  params: ReturnType<typeof useApp>['params']
) {
  const prices: Record<string, number> = {}
  const limits: Record<string, [number, number]> = {}

  for (const [id, s] of Object.entries(selected)) {
    prices[id] = finite(s.price, 0.3)
    limits[id] = [finite(s.min), finite(s.max, 100)]
  }

  return {
    feeds: Object.keys(selected).map(Number),
    prices,
    limits,
    milk_price: finite(params.milkPrice, 0.45),
    years: params.years,
    max_milk_reduction: finite(params.maxReduction, 5)
  }
}

const messageOf = (error: unknown) => (error instanceof Error ? error.message : 'Falha na simulação').split('\n')[0]
const showResults = () => document.getElementById('resultados')?.scrollIntoView({ behavior: 'smooth', block: 'start' })

export default function CowView() {
  const { connection, selected, params, setParams, sim, setSim, simKey, setSimKey, cowScenario, loadCowScenario, trackTask } =
    useApp()
  const [running, setRunning] = useState(false)
  const [progress, setProgress] = useState({ done: 0, total: 0, status: 'queued' })
  const [error, setError] = useState<string | null>(null)
  const [base, setBase] = useState<RunMeta | null>(null)

  // cenário-base das simulações (D3): referência dos deltas dos indicadores
  const loadBase = useCallback(() => {
    api
      .historyBase('simulation')
      .then(setBase)
      .catch(() => setBase(null))
  }, [])

  useEffect(() => {
    if (connection === 'online') loadBase()
  }, [connection, loadBase])

  const markBase = async () => {
    if (!sim?.run_id) return

    try {
      await api.setHistoryBase(sim.run_id, true)
      toast.success('Cenário-base definido.')
      loadBase()
    } catch (e) {
      toast.error(messageOf(e))
    }
  }

  const bodyKey = useMemo(() => JSON.stringify(simulationBody(selected, params)), [selected, params])
  const stale = sim !== null && simKey !== null && simKey !== bodyKey
  const state: RunState = running ? 'running' : error ? 'error' : sim && !stale ? 'done' : 'idle'

  const run = async () => {
    if (Object.keys(selected).length < 3) {
      toast.error('Selecione pelo menos 3 alimentos (um volumoso, um concentrado e um mineral).')

      return
    }

    setRunning(true)
    setError(null)
    setProgress({ done: 0, total: 0, status: 'queued' })

    const task = trackTask('Simulação do RuFaS')

    try {
      const result = await runJob<SimResult>('simulate', simulationBody(selected, params), (done, total, status) => {
        setProgress({ done, total, status })
        task.update(done, total)
      })

      setSim(result)
      setSimKey(bodyKey)
      toast.success('Simulação concluída.')
    } catch (e) {
      setError(messageOf(e))
      toast.error(messageOf(e))
    } finally {
      task.end()
      setRunning(false)
    }
  }

  const runButton = (
    <RunButton
      state={state}
      progress={progress}
      label='Executar simulação'
      unit='simulações do RuFaS'
      error={error}
      disabled={connection !== 'online'}
      onRun={run}
      onView={showResults}
    />
  )

  return (
    <>
      <PageHeader
        title='Vaca leiteira (RuFaS)'
        description='Escolha os alimentos, informe preços e limites e simule com o RuFaS (padrão NRC 2001). O otimizador do RuFaS formula a ração de custo mínimo e o sistema calcula custo, leite e margem.'
      />

      <div className='grid items-start gap-6 max-xl:pb-20 xl:grid-cols-[24rem_minmax(0,1fr)]'>
        <Card className='xl:sticky xl:top-24 xl:max-h-[calc(100dvh-7rem)]'>
          <CardHeader>
            <CardTitle>Parâmetros</CardTitle>
            <CardDescription>Preços em US$/kg de matéria seca; limites em kg de MS por vaca por dia.</CardDescription>
          </CardHeader>
          <CardContent className='min-h-0 flex-1 space-y-5 overflow-y-auto'>
            <div className='grid grid-cols-2 gap-3'>
              <div className='space-y-1.5'>
                <Label>Preço do leite (US$/kg)</Label>
                <NumberInput
                  value={params.milkPrice}
                  onChange={v => setParams({ milkPrice: v })}
                  aria-label='Preço do leite em dólares por quilo'
                />
              </div>
              <div className='space-y-1.5'>
                <Label>Período simulado</Label>
                <Select
                  value={String(params.years)}
                  items={YEARS}
                  onValueChange={v => v && setParams({ years: Number(v) })}
                >
                  <SelectTrigger className='w-full'>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {YEARS.map(y => (
                      <SelectItem key={y.value} value={y.value}>
                        {y.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className='space-y-1.5'>
              <Label>Redução máxima de leite tolerada (kg/vaca/dia)</Label>
              <NumberInput
                step={0.25}
                min={0}
                value={params.maxReduction}
                onChange={v => setParams({ maxReduction: v })}
                aria-label='Redução máxima de leite'
              />
              <p className='text-muted-foreground text-xs'>
                Se a ração não atende às exigências, o RuFaS reduz o leite (0,25 kg por tentativa) até este limite; acima
                dele a simulação aborta.
              </p>
            </div>

            <ScenarioFile<CowScenario> kind='cow' getData={cowScenario} onLoad={loadCowScenario} />

            <FeedPicker />
          </CardContent>
          <CardFooter className='border-t pt-(--card-spacing) max-xl:hidden'>
            <div className='w-full'>{runButton}</div>
          </CardFooter>
        </Card>

        <div className='min-w-0 space-y-6'>
          {state === 'error' && (
            <Alert variant='destructive'>
              <AlertTriangleIcon />
              <AlertTitle>A simulação não terminou</AlertTitle>
              <AlertDescription>{error} Confira os alimentos, os limites e a conexão com o servidor.</AlertDescription>
            </Alert>
          )}

          {sim ? (
            <Results sim={sim} stale={stale} base={base} onSetBase={markBase} />
          ) : running ? (
            <ResultsSkeleton />
          ) : (
            <EmptyState
              icon={MilkIcon}
              title='Nenhuma simulação ainda'
              steps={[
                'Escolha os alimentos (ou use o Conjunto base) e ajuste preços e limites.',
                'Clique em Executar simulação: cada uma leva de 30 a 60 segundos.',
                'Analise os indicadores, a ração e a nutrição, e exporte o relatório.'
              ]}
            />
          )}
        </div>
      </div>

      <div className='bg-card/90 border-border fixed inset-x-3 bottom-3 z-30 rounded-2xl border p-2 backdrop-blur-xl xl:hidden'>
        {runButton}
      </div>
    </>
  )
}

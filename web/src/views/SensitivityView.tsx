'use client'

import { useCallback, useEffect, useMemo, useState } from 'react'

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
import { api, runJob } from '@/lib/api'
import type { RunMeta, SensFactor, SensFactorState as FactorState, SensResult } from '@/lib/types'
import { useApp } from '@/providers/AppProvider'
import { simulationBody } from '@/views/CowView'
import SensResults from '@/views/sensitivity/Results'

const METHODS = [
  { value: 'grid', label: 'Grade (todas as combinações)' },
  { value: 'latin', label: 'Hipercubo latino' }
]
const MILK = 'milk_price'
const SECONDS_PER_SIMULATION = 17

const messageOf = (error: unknown) => (error instanceof Error ? error.message : 'Falha na análise').split('\n')[0]
const showResults = () => document.getElementById('resultados')?.scrollIntoView({ behavior: 'smooth', block: 'start' })

export default function SensitivityView() {
  const { connection, selected, feedById, params, sens, setSens, sensKey, setSensKey, sensSetup, setSensSetup, trackTask } = useApp()
  const { overrides, method, levels } = sensSetup
  const setOverrides = (change: (previous: Record<string, FactorState>) => Record<string, FactorState>) =>
    setSensSetup(s => ({ ...s, overrides: change(s.overrides) }))
  const setMethod = (value: string) => setSensSetup(s => ({ ...s, method: value }))
  const setLevels = (value: number) => setSensSetup(s => ({ ...s, levels: value }))
  const [running, setRunning] = useState(false)
  const [progress, setProgress] = useState({ done: 0, total: 0, status: 'queued' })
  const [error, setError] = useState<string | null>(null)
  const [base, setBase] = useState<RunMeta | null>(null)

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

  const rows = useMemo(() => {
    const list = Object.entries(selected).map(([id, s]) => ({
      key: id,
      label: feedById[Number(id)] ? feedTitle(feedById[Number(id)]) : id,
      defaults: { on: ['138', '44'].includes(id), low: +(s.price * 0.5).toFixed(3), high: +(s.price * 1.5).toFixed(3) }
    }))

    list.push({
      key: MILK,
      label: 'Preço do leite (US$/kg)',
      defaults: { on: true, low: +(finite(params.milkPrice, 0.45) * 0.8).toFixed(3), high: +(finite(params.milkPrice, 0.45) * 1.2).toFixed(3) }
    })

    return list
  }, [selected, feedById, params.milkPrice])

  const stateOf = (key: string, defaults: FactorState) => overrides[key] ?? defaults
  const patch = (key: string, defaults: FactorState, change: Partial<FactorState>) =>
    setOverrides(prev => ({ ...prev, [key]: { ...(prev[key] ?? defaults), ...change } }))

  const factors: SensFactor[] = rows
    .filter(r => stateOf(r.key, r.defaults).on)
    .map(r => ({ key: r.key, label: r.label, low: finite(stateOf(r.key, r.defaults).low), high: finite(stateOf(r.key, r.defaults).high) }))

  const n = Math.max(2, Math.min(12, finite(levels, 2)))
  const feedFactors = factors.filter(f => f.key !== MILK).length
  const points = factors.length ? (method === 'grid' ? n ** factors.length : n) : 0
  const sims = factors.length ? (method === 'grid' ? n ** feedFactors : n) : 0

  const body = useMemo(
    () => ({ ...simulationBody(selected, params), factors, method, n }),
    // `factors` é derivado de `rows`, `overrides`; a chave serializada abaixo cobre a identidade
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [selected, params, JSON.stringify(factors), method, n]
  )
  const bodyKey = JSON.stringify(body)
  const stale = sens !== null && sensKey !== null && sensKey !== bodyKey
  const state: RunState = running ? 'running' : error ? 'error' : sens && !stale ? 'done' : 'idle'
  const blocked = !factors.length || connection !== 'online' || Object.keys(selected).length < 3

  const run = async () => {
    setRunning(true)
    setError(null)
    setProgress({ done: 0, total: 0, status: 'queued' })

    const task = trackTask('Análise de sensibilidade')

    try {
      const result = await runJob<SensResult>('sensitivity', body, (done, total, status) => {
        setProgress({ done, total, status })
        task.update(done, total)
      })

      setSens(result)
      setSensKey(bodyKey)
      toast.success('Análise concluída.')
    } catch (e) {
      setError(messageOf(e))
      toast.error(messageOf(e))
    } finally {
      task.end()
      setRunning(false)
    }
  }

  const runButton = (
    <div className='space-y-2'>
      <p className='text-muted-foreground text-xs' aria-live='polite'>
        {factors.length
          ? `${points} cenários, até ${sims} simulações do RuFaS (cerca de ${Math.max(1, Math.ceil((sims * SECONDS_PER_SIMULATION) / 60))} min).`
          : 'Marque ao menos um fator.'}
      </p>
      <RunButton
        state={state}
        progress={progress}
        label='Executar sensibilidade'
        unit='simulações do RuFaS'
        error={error}
        disabled={blocked}
        onRun={run}
        onView={showResults}
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
                <NumberInput step={1} min={2} value={levels} onChange={setLevels} aria-label='Níveis ou amostras' />
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
              <SensResults result={sens} stale={stale} base={base} years={params.years} />
            </div>
          ) : running ? (
            <ResultsSkeleton />
          ) : (
            <EmptyState
              icon={SlidersHorizontalIcon}
              title='Nenhuma análise ainda'
              steps={[
                'Marque os fatores que vão variar (preços dos alimentos e do leite) e informe a faixa de cada um.',
                'Escolha o método e os níveis, e clique em Executar sensibilidade: cada simulação leva cerca de 17 segundos.',
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

'use client'

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import { JobCancelledError, api, cancelJob, runJob } from '@/lib/api'
import type {
  ModuleCategory,
  ModuleDefaults,
  ModuleOptimization,
  ModuleRequirements,
  NutrientStandard,
  OptimizationResolution
} from '@/lib/types'
import { useApp } from '@/providers/AppProvider'

import CompareCard from './module/CompareCard'
import CowCard from './module/CowCard'
import DietsCard from './module/DietsCard'
import OptimalCard from './module/OptimalCard'
import {
  ANIMAL_TYPES,
  MAX_DIETS,
  SAMPLE_COWS,
  cowPayload,
  cowProblems,
  dietProblems,
  evaluateBody,
  exampleDiets,
  initialSetting,
  optimizeBody,
  optimizeProblems,
  standardName,
  type ModuleState
} from './module/model'
import PricesCard from './module/PricesCard'
import ResultCard from './module/ResultCard'
import { useFeedLibrary } from './module/useFeedLibrary'

const REQUIREMENTS_DELAY_MS = 400

/** Mensagem curta de um erro da API (a primeira linha). */
const messageOf = (error: unknown, fallback: string) =>
  (error instanceof Error ? error.message : fallback).split('\n')[0]

export default function ModuleView() {
  const { connection, defaults: appDefaults, moduleState: state, setModuleState: setState } = useApp()
  const online = connection === 'online'
  const { feeds, byId, error: libraryError } = useFeedLibrary(state.standard, online)

  const [defaults, setDefaults] = useState<ModuleDefaults | null>(null)
  const [defaultsError, setDefaultsError] = useState<string | null>(null)
  const [requirements, setRequirements] = useState<ModuleRequirements | null>(null)
  const [requirementsLoading, setRequirementsLoading] = useState(false)
  const [requirementsError, setRequirementsError] = useState<string | null>(null)
  const [evaluating, setEvaluating] = useState(false)
  const [evaluateError, setEvaluateError] = useState<string | null>(null)
  const [selected, setSelected] = useState<string | null>(null)
  const [comparing, setComparing] = useState(false)
  const [compareError, setCompareError] = useState<string | null>(null)
  const [comparedDiet, setComparedDiet] = useState<string | null>(null)
  const [optimizing, setOptimizing] = useState(false)
  const [optimizeProgress, setOptimizeProgress] = useState<{ done: number; total: number } | null>(null)
  const [optimizeError, setOptimizeError] = useState<string | null>(null)
  const optimizeJob = useRef<string | null>(null)
  const [notice, setNotice] = useState<string | null>(null)
  // Nomes dos alimentos já vistos em qualquer biblioteca, para citá-los no aviso de remoção ao trocar de padrão.
  const names = useRef<Record<number, string>>({})

  const patch = useCallback((change: Partial<ModuleState>) => setState(s => ({ ...s, ...change })), [setState])

  // ---- campos da vaca e restrições do padrão, categoria e tipo de animal
  useEffect(() => {
    if (!online) return

    let cancelled = false

    setDefaults(null)
    setDefaultsError(null)
    api
      .moduleDefaults(state.standard, state.category, state.animalType)
      .then(value => !cancelled && setDefaults(value))
      .catch(e => !cancelled && setDefaultsError(messageOf(e, 'Falha ao carregar os campos da vaca')))

    return () => {
      cancelled = true
    }
  }, [online, state.standard, state.category, state.animalType])

  const cowProblemList = useMemo(() => (defaults ? cowProblems(defaults.fields, state.cow) : []), [defaults, state.cow])
  const cowKey = useMemo(
    () => (defaults ? JSON.stringify(cowPayload(defaults.fields, state.cow)) : ''),
    [defaults, state.cow]
  )

  // ---- exigências calculadas (sem sobrescritas: elas só mudam o que é usado na avaliação)
  useEffect(() => {
    if (!online || !defaults || cowProblemList.length > 0) {
      setRequirements(null)
      setRequirementsError(null)

      return
    }

    let cancelled = false
    const timer = setTimeout(() => {
      setRequirementsLoading(true)
      api
        .moduleRequirements({
          standard: state.standard,
          category: state.category,
          animal_type: state.animalType,
          cow: JSON.parse(cowKey)
        })
        .then(value => {
          if (cancelled) return

          setRequirements(value)
          setRequirementsError(null)
        })
        .catch(e => !cancelled && setRequirementsError(messageOf(e, 'Falha ao calcular as exigências')))
        .finally(() => !cancelled && setRequirementsLoading(false))
    }, REQUIREMENTS_DELAY_MS)

    return () => {
      cancelled = true
      clearTimeout(timer)
    }
    // `cowKey` representa o conteúdo de `state.cow`; os demais campos identificam o cálculo.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [online, defaults, cowKey, cowProblemList.length, state.standard, state.category, state.animalType])

  // ---- biblioteca do padrão: guarda os nomes e remove das dietas o que não existe nela
  useEffect(() => {
    if (!feeds) return

    for (const feed of feeds) names.current[feed.id] = feed.name

    const missing = state.feedIds.filter(id => !byId[id])

    if (missing.length === 0) return

    setState(s => ({
      ...s,
      feedIds: s.feedIds.filter(id => byId[id]),
      feedSettings: Object.fromEntries(Object.entries(s.feedSettings).filter(([id]) => byId[Number(id)])),
      diets: s.diets.map(diet => ({
        ...diet,
        amounts: Object.fromEntries(Object.entries(diet.amounts).filter(([id]) => byId[Number(id)]))
      })),
      result: null,
      resultKey: null
    }))
    setNotice(
      `Removidos por não existirem no padrão ${standardName(state.standard)}: ${missing
        .map(id => names.current[id] ?? id)
        .join(', ')}.`
    )
  }, [feeds, byId, state.feedIds, state.standard, setState])

  // ---- o que mudou desde a última avaliação
  const library = byId
  const body = useMemo(
    () => (defaults ? evaluateBody(state, defaults.fields, library) : null),
    [state, defaults, library]
  )
  const bodyKey = body ? JSON.stringify(body) : null
  const stale = state.result !== null && state.resultKey !== bodyKey
  const compareBody = useMemo(() => (body ? { ...body, tolerance_pct: state.tolerance } : null), [body, state.tolerance])
  const compareKey = compareBody ? JSON.stringify(compareBody) : null
  const compareStale = state.comparison !== null && state.comparisonKey !== compareKey
  const optimizePayload = useMemo(
    () => (defaults ? optimizeBody(state, defaults.fields, library) : null),
    [state, defaults, library]
  )
  const optimizeKey = optimizePayload ? JSON.stringify(optimizePayload) : null
  const optimalStale = state.optimal !== null && state.optimalKey !== optimizeKey

  const blockers = useMemo(() => {
    if (!online) return ['O servidor local não está respondendo.']
    if (!defaults || !feeds) return ['Carregando os dados do padrão…']

    return [...cowProblemList, ...dietProblems(state, library)]
  }, [online, defaults, feeds, cowProblemList, state, library])

  const optimizeBlockers = useMemo(() => {
    if (!online) return ['O servidor local não está respondendo.']
    if (!defaults || !feeds) return ['Carregando os dados do padrão…']

    return [...cowProblemList, ...optimizeProblems(state, library)]
  }, [online, defaults, feeds, cowProblemList, state, library])

  // ---- ações
  const changeStandard = (standard: NutrientStandard) => {
    setNotice(null)
    patch({ standard, result: null, resultKey: null })
  }

  // Trocar de categoria ou de tipo de animal muda os campos da vaca: volta ao exemplo do novo tipo.
  const resetCow = (category: ModuleCategory, animalType: string) =>
    patch({ category, animalType, cow: { ...SAMPLE_COWS[animalType] }, override: {}, result: null, resultKey: null })

  const changeCategory = (category: ModuleCategory) => resetCow(category, ANIMAL_TYPES[category][0].value)
  const changeAnimalType = (animalType: string) => resetCow(state.category, animalType)

  const setCow = (key: string, value: number | string) => setState(s => ({ ...s, cow: { ...s.cow, [key]: value } }))

  const setOverride = (key: string, value: number | undefined) =>
    setState(s => {
      const { [key]: _removed, ...rest } = s.override

      return { ...s, override: value === undefined ? rest : { ...rest, [key]: value } }
    })

  const addFeeds = (ids: number[]) =>
    setState(s => {
      const fresh = ids.filter(id => byId[id] && !s.feedIds.includes(id))

      return {
        ...s,
        feedIds: [...s.feedIds, ...fresh],
        feedSettings: {
          ...s.feedSettings,
          ...Object.fromEntries(fresh.map(id => [id, initialSetting(byId[id], appDefaults)]))
        }
      }
    })

  const removeFeed = (id: number) =>
    setState(s => ({
      ...s,
      feedIds: s.feedIds.filter(f => f !== id),
      feedSettings: Object.fromEntries(Object.entries(s.feedSettings).filter(([key]) => Number(key) !== id)),
      diets: s.diets.map(diet => ({
        ...diet,
        amounts: Object.fromEntries(Object.entries(diet.amounts).filter(([key]) => Number(key) !== id))
      }))
    }))

  const setAmount = (uid: number, id: number, value: number) =>
    setState(s => ({
      ...s,
      diets: s.diets.map(diet => (diet.uid === uid ? { ...diet, amounts: { ...diet.amounts, [id]: value } } : diet))
    }))

  const setName = (uid: number, name: string) =>
    setState(s => ({ ...s, diets: s.diets.map(diet => (diet.uid === uid ? { ...diet, name } : diet)) }))

  const addDiet = () =>
    setState(s => {
      let n = s.diets.length + 1

      while (s.diets.some(d => d.name === `Dieta ${n}`)) n += 1

      return { ...s, diets: [...s.diets, { uid: s.nextUid, name: `Dieta ${n}`, amounts: {} }], nextUid: s.nextUid + 1 }
    })

  const removeDiet = (uid: number) => setState(s => ({ ...s, diets: s.diets.filter(d => d.uid !== uid) }))

  const loadExamples = () => {
    const total = requirements?.calculated.dry_matter ?? 25
    const room = MAX_DIETS - state.diets.length
    const taken = new Set(state.diets.map(d => d.name))

    // As dietas de exemplo somam o consumo estimado da vaca; os alimentos ausentes no padrão ficam de fora.
    const added = exampleDiets(total, state.nextUid)
      .slice(0, Math.max(room, 0))
      .map(diet => ({
        ...diet,
        name: taken.has(diet.name) ? `${diet.name} (exemplo)` : diet.name,
        amounts: Object.fromEntries(Object.entries(diet.amounts).filter(([id]) => byId[Number(id)]))
      }))
    const ids = [...new Set(added.flatMap(diet => Object.keys(diet.amounts).map(Number)))]

    addFeeds(ids)
    setState(s => ({ ...s, diets: [...s.diets, ...added], nextUid: s.nextUid + added.length }))
  }

  const evaluate = async () => {
    if (!body || blockers.length > 0) return

    setEvaluating(true)
    setEvaluateError(null)

    try {
      const result = await api.moduleEvaluate(body)

      patch({ result, resultKey: bodyKey })
      setSelected(result.best ?? result.ranking[result.ranking.length - 1] ?? null)
    } catch (e) {
      setEvaluateError(messageOf(e, 'Falha ao avaliar as dietas'))
    } finally {
      setEvaluating(false)
    }
  }

  const compare = async () => {
    if (!compareBody || blockers.length > 0) return

    setComparing(true)
    setCompareError(null)

    try {
      const comparison = await api.moduleCompare(compareBody)

      patch({ comparison, comparisonKey: compareKey })
      setComparedDiet(comparison.summary.worst?.diet ?? comparison.diets[0]?.name ?? null)
    } catch (e) {
      setCompareError(messageOf(e, 'Falha ao comparar com o RuFaS'))
    } finally {
      setComparing(false)
    }
  }

  const optimize = async () => {
    if (!optimizePayload || optimizeBlockers.length > 0) return

    setOptimizing(true)
    setOptimizeError(null)
    setOptimizeProgress(null)

    try {
      const optimal = await runJob<ModuleOptimization>(
        'optimize',
        optimizePayload,
        (done, total) => setOptimizeProgress({ done, total }),
        { onStart: id => (optimizeJob.current = id), intervalMs: 700 }
      )

      patch({ optimal, optimalKey: optimizeKey })
    } catch (e) {
      if (!(e instanceof JobCancelledError)) setOptimizeError(messageOf(e, 'Falha ao calcular a dieta ótima'))
    } finally {
      optimizeJob.current = null
      setOptimizing(false)
    }
  }

  const cancelOptimize = () => {
    if (optimizeJob.current) cancelJob(optimizeJob.current).catch(() => undefined)
  }

  return (
    <div className='space-y-6'>
      <CowCard
        state={state}
        defaults={defaults}
        defaultsError={defaultsError}
        requirements={requirements}
        requirementsLoading={requirementsLoading}
        requirementsError={requirementsError}
        problems={cowProblemList}
        onStandard={changeStandard}
        onCategory={changeCategory}
        onAnimalType={changeAnimalType}
        onCow={setCow}
        onOverride={setOverride}
      />
      <DietsCard
        state={state}
        library={library}
        feeds={feeds}
        libraryError={libraryError}
        notice={notice}
        estimatedIntake={requirements?.calculated.dry_matter ?? null}
        onAddFeed={id => addFeeds([id])}
        onRemoveFeed={removeFeed}
        onAmount={setAmount}
        onName={setName}
        onAddDiet={addDiet}
        onRemoveDiet={removeDiet}
        onExamples={loadExamples}
      />
      <PricesCard
        state={state}
        library={library}
        onPrices={prices =>
          setState(s => ({
            ...s,
            feedSettings: Object.fromEntries(
              Object.entries(s.feedSettings).map(([id, setting]) => [id, id in prices ? { ...setting, price: prices[Number(id)] } : setting])
            )
          }))
        }
        onSetting={(id, field, value) =>
          setState(s => ({ ...s, feedSettings: { ...s.feedSettings, [id]: { ...s.feedSettings[id], [field]: value } } }))
        }
      />
      <ResultCard
        result={state.result}
        stale={stale}
        evaluating={evaluating}
        error={evaluateError}
        blockers={blockers}
        selected={selected}
        optimalCost={state.optimal?.diet && !optimalStale ? state.optimal.diet.cost : null}
        onSelect={setSelected}
        onEvaluate={evaluate}
      />
      <OptimalCard
        library={library}
        result={state.optimal}
        stale={optimalStale}
        running={optimizing}
        progress={optimizeProgress}
        error={optimizeError}
        blockers={optimizeBlockers}
        resolution={state.resolution}
        seeds={state.seeds}
        onResolution={(resolution: OptimizationResolution) => patch({ resolution })}
        onSeeds={seeds => patch({ seeds })}
        onRun={optimize}
        onCancel={cancelOptimize}
      />
      {state.result && (
        <CompareCard
          report={state.comparison}
          stale={compareStale}
          running={comparing}
          error={compareError}
          blockers={blockers}
          tolerance={state.tolerance}
          selected={comparedDiet}
          onTolerance={tolerance => patch({ tolerance })}
          onSelect={setComparedDiet}
          onCompare={compare}
        />
      )}
    </div>
  )
}

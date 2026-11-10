'use client'

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type Dispatch,
  type ReactNode,
  type SetStateAction
} from 'react'

import { api } from '@/lib/api'
import type {
  Defaults,
  CowScenario,
  Feed,
  Selected,
  SensResult,
  SensSetup,
  SimParams,
  SimResult,
  ToyBound,
  ToyFood,
  ToyResult,
  ToySens
} from '@/lib/types'
import { initialModuleState, type ModuleState } from '@/views/module/model'

/** Conjunto validado de alimentos: volumosos, concentrados e minerais da biblioteca NRC. */
export const PRESET_BASE = [50, 110, 44, 167, 138, 230, 23]
export const PRESET_WIDE = [50, 51, 110, 104, 95, 44, 47, 138, 167, 164, 169, 58, 193, 194, 24, 1, 230, 23]

const FALLBACK_PRICE: Record<string, number> = { Forage: 0.12, Conc: 0.35, Mineral: 0.15 }
const STORAGE_KEY = 'dietopt.v1'

type Connection = 'connecting' | 'online' | 'offline'

interface AppContextValue {
  connection: Connection
  feeds: Feed[]
  feedById: Record<number, Feed>
  defaults: Defaults | null

  selected: Selected
  toggleFeed: (id: number) => void
  setFeedField: (id: number, field: 'price' | 'min' | 'max', value: number) => void
  /** Troca o preço (US$/kg MS) dos alimentos selecionados que aparecem em `prices`. */
  applyPrices: (prices: Record<number, number>) => void
  applyPreset: (ids: number[]) => void

  params: SimParams
  setParams: (patch: Partial<SimParams>) => void

  sim: SimResult | null
  setSim: (value: SimResult | null) => void
  /** Parâmetros (serializados) com que `sim` foi calculada; diferente dos atuais = resultado desatualizado. */
  simKey: string | null
  setSimKey: (value: string | null) => void
  sens: SensResult | null
  setSens: (value: SensResult | null) => void
  /** Parâmetros (serializados) com que `sens` foi calculada; diferente dos atuais = análise desatualizada. */
  sensKey: string | null
  setSensKey: (value: string | null) => void
  /** Fatores, método e níveis da sensibilidade; ficam aqui para sobreviver à navegação e irem no cenário salvo. */
  sensSetup: SensSetup
  setSensSetup: Dispatch<SetStateAction<SensSetup>>
  /** Entradas da tela Vaca leiteira (e da sensibilidade) para salvar em arquivo. */
  cowScenario: () => unknown
  /** Aplica um cenário aberto de arquivo: troca alimentos, parâmetros e fatores e descarta os resultados. */
  loadCowScenario: (scenario: CowScenario) => void

  toyFoods: ToyFood[]
  setToyFoods: (value: ToyFood[]) => void
  toyBounds: ToyBound[]
  setToyBounds: (value: ToyBound[]) => void
  toyResult: ToyResult | null
  setToyResult: (value: ToyResult | null) => void
  toySens: ToySens | null
  setToySens: (value: ToySens | null) => void
  /** Chaves (problema e fatores) com que o resultado e os cenários do quadro foram calculados; servem para detectar o que ficou desatualizado. */
  toyKey: string | null
  setToyKey: (value: string | null) => void
  toySensKey: string | null
  setToySensKey: (value: string | null) => void

  tasks: AppTask[]
  trackTask: (label: string) => TaskHandle

  /** Tela 1: exercício simples ou avaliação de dietas de uma vaca real. */
  exerciseMode: ExerciseMode
  setExerciseMode: (value: ExerciseMode) => void
  /** Estado da avaliação de dietas; fica aqui para sobreviver à navegação entre telas (memória da página). */
  moduleState: ModuleState
  setModuleState: Dispatch<SetStateAction<ModuleState>>
}

export type ExerciseMode = 'simple' | 'module'

/** Tarefa em andamento (simulação, sensibilidade, dieta ótima), mostrada no menu Tarefas do cabeçalho. */
export interface AppTask {
  id: number
  label: string
  done: number
  total: number
}

/** Controle de uma tarefa registrada: atualize o progresso e encerre no `finally`. */
export interface TaskHandle {
  update: (done: number, total: number) => void
  end: () => void
}

const AppContext = createContext<AppContextValue | null>(null)

const INITIAL_PARAMS: SimParams = { milkPrice: 0.45, years: 1, maxReduction: 5, cowNum: 100 }
const INITIAL_SENS: SensSetup = { overrides: {}, method: 'grid', levels: 3 }

const INITIAL_TOY_FOODS: ToyFood[] = [
  { name: 'Arroz', cost: 1.5, carb: 0.77, prot: 0.08 },
  { name: 'Milho', cost: 2.23, carb: 0.66, prot: 0.14 }
]
const INITIAL_TOY_BOUNDS: ToyBound[] = [
  { name: 'Carboidrato', min: 6, max: 9.5 },
  { name: 'Proteína', min: 0.9, max: 1.6 }
]

function priceOf(feed: Feed, defaults: Defaults | null) {
  return defaults?.prices[String(feed.id)] ?? feed.default_price ?? FALLBACK_PRICE[feed.kind] ?? 0.3
}

export function AppProvider({ children }: { children: ReactNode }) {
  const [connection, setConnection] = useState<Connection>('connecting')
  const [feeds, setFeeds] = useState<Feed[]>([])
  const [defaults, setDefaults] = useState<Defaults | null>(null)
  const [selected, setSelected] = useState<Selected>({})
  const [params, setParamsState] = useState<SimParams>(INITIAL_PARAMS)
  const [sim, setSim] = useState<SimResult | null>(null)
  const [simKey, setSimKey] = useState<string | null>(null)
  const [sens, setSens] = useState<SensResult | null>(null)
  const [sensKey, setSensKey] = useState<string | null>(null)
  const [sensSetup, setSensSetup] = useState<SensSetup>(INITIAL_SENS)
  const [toyFoods, setToyFoods] = useState<ToyFood[]>(INITIAL_TOY_FOODS)
  const [toyBounds, setToyBounds] = useState<ToyBound[]>(INITIAL_TOY_BOUNDS)
  const [toyResult, setToyResult] = useState<ToyResult | null>(null)
  const [toySens, setToySens] = useState<ToySens | null>(null)
  const [toyKey, setToyKey] = useState<string | null>(null)
  const [toySensKey, setToySensKey] = useState<string | null>(null)
  const [exerciseMode, setExerciseMode] = useState<ExerciseMode>('simple')
  const [moduleState, setModuleState] = useState<ModuleState>(initialModuleState)
  const [tasks, setTasks] = useState<AppTask[]>([])

  const feedById = useMemo(() => Object.fromEntries(feeds.map(f => [f.id, f])) as Record<number, Feed>, [feeds])

  const buildSelection = useCallback(
    (ids: number[], library: Feed[], defs: Defaults | null): Selected => {
      const byId = Object.fromEntries(library.map(f => [f.id, f])) as Record<number, Feed>

      return Object.fromEntries(
        ids
          .filter(id => byId[id])
          .map(id => [id, { price: priceOf(byId[id], defs), min: 0, max: byId[id].default_max }])
      )
    },
    []
  )

  // Carrega a biblioteca e restaura a última configuração (localStorage, quando disponível).
  useEffect(() => {
    let cancelled = false

    Promise.all([api.feeds(), api.defaults()])
      .then(([library, defs]) => {
        if (cancelled) return

        setFeeds(library)
        setDefaults(defs)
        setParamsState(p => ({ ...p, milkPrice: defs.milk_price }))

        let restored: Selected | null = null

        try {
          const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null') as {
            selected?: Selected
            params?: SimParams
          } | null

          if (saved?.selected && Object.keys(saved.selected).length) restored = saved.selected
          // o que foi salvo antes do RF-13 não tem o número de vacas: completa com o padrão
          if (saved?.params) setParamsState({ ...INITIAL_PARAMS, ...saved.params })
        } catch {
          // sem localStorage: segue com os valores padrão
        }

        setSelected(restored ?? buildSelection(PRESET_BASE, library, defs))
        setConnection('online')
      })
      .catch(() => !cancelled && setConnection('offline'))

    return () => {
      cancelled = true
    }
  }, [buildSelection])

  useEffect(() => {
    if (connection !== 'online') return

    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ selected, params }))
    } catch {
      // ignora
    }
  }, [selected, params, connection])

  const toggleFeed = useCallback(
    (id: number) =>
      setSelected(prev => {
        if (prev[id]) {
          const { [id]: _removed, ...rest } = prev

          return rest
        }

        const feed = feedById[id]

        return feed ? { ...prev, [id]: { price: priceOf(feed, defaults), min: 0, max: feed.default_max } } : prev
      }),
    [feedById, defaults]
  )

  const setFeedField = useCallback(
    (id: number, field: 'price' | 'min' | 'max', value: number) =>
      setSelected(prev => (prev[id] ? { ...prev, [id]: { ...prev[id], [field]: value } } : prev)),
    []
  )

  const applyPrices = useCallback(
    (prices: Record<number, number>) =>
      setSelected(prev =>
        Object.fromEntries(
          Object.entries(prev).map(([id, feed]) => [id, id in prices ? { ...feed, price: prices[Number(id)] } : feed])
        )
      ),
    []
  )

  const applyPreset = useCallback(
    (ids: number[]) => setSelected(buildSelection(ids, feeds, defaults)),
    [buildSelection, feeds, defaults]
  )

  const cowScenario = useCallback(
    () => ({
      standard: 'NRC',
      params,
      feeds: Object.entries(selected).map(([id, feed]) => ({ id: Number(id), ...feed })),
      sensitivity: { method: sensSetup.method, levels: sensSetup.levels, factors: sensSetup.overrides }
    }),
    [params, selected, sensSetup]
  )

  const loadCowScenario = useCallback((scenario: CowScenario) => {
    setSelected(Object.fromEntries(scenario.feeds.map(({ id, ...feed }) => [id, feed])))
    setParamsState(scenario.params)
    setSensSetup(
      scenario.sensitivity
        ? { overrides: scenario.sensitivity.factors, method: scenario.sensitivity.method, levels: scenario.sensitivity.levels }
        : INITIAL_SENS
    )
    setSim(null)
    setSimKey(null)
    setSens(null)
    setSensKey(null)
  }, [])

  const trackTask = useCallback((label: string): TaskHandle => {
    const id = Date.now() + Math.random()

    setTasks(prev => [...prev, { id, label, done: 0, total: 0 }])

    return {
      update: (done, total) => setTasks(prev => prev.map(t => (t.id === id ? { ...t, done, total } : t))),
      end: () => setTasks(prev => prev.filter(t => t.id !== id))
    }
  }, [])

  const setParams = useCallback((patch: Partial<SimParams>) => setParamsState(p => ({ ...p, ...patch })), [])

  const value: AppContextValue = {
    connection,
    feeds,
    feedById,
    defaults,
    selected,
    toggleFeed,
    setFeedField,
    applyPrices,
    applyPreset,
    params,
    setParams,
    sim,
    setSim,
    simKey,
    setSimKey,
    sens,
    setSens,
    sensKey,
    setSensKey,
    sensSetup,
    setSensSetup,
    cowScenario,
    loadCowScenario,
    toyFoods,
    setToyFoods,
    toyBounds,
    setToyBounds,
    toyResult,
    setToyResult,
    toySens,
    setToySens,
    toyKey,
    setToyKey,
    toySensKey,
    setToySensKey,
    tasks,
    trackTask,
    exerciseMode,
    setExerciseMode,
    moduleState,
    setModuleState
  }

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

export function useApp() {
  const ctx = useContext(AppContext)

  if (!ctx) throw new Error('useApp deve ser usado dentro de <AppProvider>')

  return ctx
}

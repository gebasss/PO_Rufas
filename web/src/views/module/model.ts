// Estado e funções puras da tela "Avaliar dietas (vaca real)" (FSD, Anexo B). Nada aqui depende de React.

import type {
  Defaults,
  Feed,
  ModuleCategory,
  ModuleEvaluation,
  ModuleField,
  NutrientStandard,
  Selected
} from '@/lib/types'

/** Máximo de dietas por avaliação (o mesmo limite do back-end, `MAX_DIETS`). */
export const MAX_DIETS = 10

export const STANDARDS: { value: NutrientStandard; label: string; hint: string }[] = [
  { value: 'NASEM', label: 'NASEM 2021', hint: 'principal' },
  { value: 'NRC', label: 'NRC 2001', hint: 'apoio' }
]

export const CATEGORIES: { value: ModuleCategory; label: string }[] = [
  { value: 'LAC_COW', label: 'Vaca em lactação' },
  { value: 'CLOSE_UP', label: 'Vaca seca e novilha pré-parto' },
  { value: 'GROWING', label: 'Novilha em crescimento' }
]

/** Tipos de animal de cada categoria; o primeiro é o padrão (espelha `CATEGORY_ANIMAL_TYPES` do back-end). */
export const ANIMAL_TYPES: Record<ModuleCategory, { value: string; label: string }[]> = {
  LAC_COW: [{ value: 'LAC_COW', label: 'Vaca em lactação' }],
  CLOSE_UP: [
    { value: 'DRY_COW', label: 'Vaca seca' },
    { value: 'HEIFER_III', label: 'Novilha pré-parto' }
  ],
  GROWING: [
    { value: 'HEIFER_II', label: 'Novilha II' },
    { value: 'HEIFER_I', label: 'Novilha I' }
  ]
}

export const HOUSING_LABELS: Record<string, string> = { Barn: 'Confinamento (Barn)', Grazing: 'Pasto (Grazing)' }

/** Valor de um campo da vaca: número (`NaN` = vazio) ou texto (alojamento). */
export type CowValues = Record<string, number | string>

/** Vacas de exemplo, só para a tela abrir preenchida. Os valores são ilustrativos: o usuário deve trocá-los. */
export const SAMPLE_COWS: Record<string, CowValues> = {
  LAC_COW: {
    body_weight: 650, mature_body_weight: 700, parity: 2, days_in_milk: 100, day_of_pregnancy: 60,
    body_condition_score_5: 3, calving_interval: 400, milk_production: 40, milk_fat: 3.7,
    milk_true_protein: 3.1, milk_lactose: 4.85, housing: 'Barn', distance: 100
  },
  DRY_COW: {
    body_weight: 740, mature_body_weight: 740, parity: 2, day_of_pregnancy: 250, calving_interval: 400,
    housing: 'Barn', distance: 100
  },
  HEIFER_III: {
    body_weight: 600, mature_body_weight: 700, parity: 0, day_of_pregnancy: 250, average_daily_gain_heifer: 0.8,
    body_condition_score_5: 3, days_born: 700, housing: 'Barn', distance: 100
  },
  HEIFER_II: {
    body_weight: 450, mature_body_weight: 700, parity: 0, day_of_pregnancy: 100, average_daily_gain_heifer: 0.8,
    body_condition_score_5: 3, days_born: 500, housing: 'Barn', distance: 100
  },
  HEIFER_I: {
    body_weight: 250, mature_body_weight: 700, parity: 0, average_daily_gain_heifer: 0.8,
    body_condition_score_5: 3, days_born: 250, housing: 'Barn', distance: 100
  }
}

/** Dietas de exemplo, em fração do consumo total, com alimentos que existem nos dois padrões. */
export const EXAMPLE_DIETS: { name: string; shares: Record<number, number> }[] = [
  { name: 'Silagem e concentrado', shares: { 50: 0.364, 110: 0.596, 44: 0.019, 167: 0.019, 230: 0.018, 23: 0.001 } },
  { name: 'Mais concentrado', shares: { 50: 0.298, 110: 0.331, 44: 0.265, 167: 0.099, 230: 0.007 } },
  { name: 'Só volumoso', shares: { 50: 0.5, 110: 0.5 } }
]

export interface ModuleDiet {
  /** Identificador estável (a chave do React), distinto do nome editável. */
  uid: number
  name: string
  /** kg de MS por dia, por id de alimento; ausente vale 0. */
  amounts: Record<number, number>
}

export interface ModuleState {
  standard: NutrientStandard
  category: ModuleCategory
  animalType: string
  cow: CowValues
  /** Exigências sobrescritas pelo usuário (só as chaves preenchidas). */
  override: Record<string, number>
  /** Alimentos da tabela, na ordem das linhas. */
  feedIds: number[]
  /** Preço (US$/kg MS) e limites (kg MS/dia) de cada alimento da tabela. */
  feedSettings: Selected
  diets: ModuleDiet[]
  nextUid: number
  result: ModuleEvaluation | null
  /** Requisição que gerou `result`; diferente da atual = resultado desatualizado. */
  resultKey: string | null
}

export function initialModuleState(): ModuleState {
  return {
    standard: 'NASEM',
    category: 'LAC_COW',
    animalType: 'LAC_COW',
    cow: { ...SAMPLE_COWS.LAC_COW },
    override: {},
    feedIds: [],
    feedSettings: {},
    diets: [],
    nextUid: 1,
    result: null,
    resultKey: null
  }
}

export const standardName = (standard: NutrientStandard) => (standard === 'NASEM' ? 'NASEM 2021' : 'NRC 2001')

const FALLBACK_PRICE: Record<string, number> = { Forage: 0.12, Conc: 0.35, Mineral: 0.15 }

/** Preço inicial de um alimento (US$/kg MS): o do cenário padrão, o da biblioteca ou um valor por tipo. */
export function initialSetting(feed: Feed, defaults: Defaults | null) {
  return {
    price: defaults?.prices[String(feed.id)] ?? feed.default_price ?? FALLBACK_PRICE[feed.kind] ?? 0.3,
    min: 0,
    max: feed.default_max
  }
}

export const hasValue = (value: number | string | undefined) =>
  typeof value === 'string' ? value.trim() !== '' : value !== undefined && Number.isFinite(value)

/** Campos da vaca que entram na requisição: os que o padrão e o tipo de animal usam e que foram preenchidos. */
export function cowPayload(fields: ModuleField[], cow: CowValues) {
  const body: Record<string, number | string> = {}

  for (const field of fields) {
    const value = cow[field.key]

    if (hasValue(value)) body[field.key] = value
  }

  return body
}

/** Problemas dos campos da vaca (obrigatório vazio, fora da faixa, inteiro). */
export function cowProblems(fields: ModuleField[], cow: CowValues) {
  const problems: string[] = []

  for (const field of fields) {
    const value = cow[field.key]

    if (!hasValue(value)) {
      if (field.required) problems.push(`${field.label}: informe um valor.`)

      continue
    }

    if (typeof value !== 'number') continue

    if (field.integer && !Number.isInteger(value)) problems.push(`${field.label}: use um número inteiro.`)
    else if ((field.min !== null && value < field.min) || (field.max !== null && value > field.max))
      problems.push(`${field.label}: fora da faixa de ${field.min ?? '…'} a ${field.max ?? '…'} ${field.unit}.`)
  }

  return problems
}

/** Alimentos com quantidade positiva em alguma dieta. */
export function usedFeedIds(state: ModuleState) {
  return state.feedIds.filter(id => state.diets.some(d => (d.amounts[id] ?? 0) > 0))
}

/** Problemas das dietas, dos preços e dos limites (B.4 e B.5). */
export function dietProblems(state: ModuleState, library: Record<number, Feed>) {
  const problems: string[] = []
  const names = new Set<string>()

  if (state.diets.length === 0) problems.push('Monte ao menos uma dieta.')

  for (const diet of state.diets) {
    const name = diet.name.trim()
    const total = state.feedIds.reduce((sum, id) => sum + Math.max(diet.amounts[id] ?? 0, 0), 0)

    if (!name) problems.push('Toda dieta precisa de um nome.')
    else if (names.has(name)) problems.push(`Nome repetido: ${name}.`)

    names.add(name)

    if (total <= 0) problems.push(`${name || 'Dieta sem nome'}: informe quantidades maiores que zero.`)
  }

  for (const id of usedFeedIds(state)) {
    const setting = state.feedSettings[id]
    const label = library[id]?.name ?? String(id)

    if (!setting || !Number.isFinite(setting.price) || setting.price < 0) problems.push(`${label}: informe o preço.`)
    else if (Number.isFinite(setting.min) && Number.isFinite(setting.max) && setting.min > setting.max)
      problems.push(`${label}: o mínimo é maior que o máximo.`)
  }

  return problems
}

/** Corpo de `POST /api/module/evaluate` (FSD, B.7). */
export function evaluateBody(state: ModuleState, fields: ModuleField[], library: Record<number, Feed>) {
  const used = usedFeedIds(state)
  const prices: Record<string, number> = {}
  const limits: Record<string, [number, number]> = {}

  for (const id of used) {
    const setting = state.feedSettings[id]

    prices[id] = setting.price
    limits[id] = [
      Number.isFinite(setting.min) ? setting.min : 0,
      Number.isFinite(setting.max) ? setting.max : (library[id]?.default_max ?? 100)
    ]
  }

  return {
    standard: state.standard,
    category: state.category,
    animal_type: state.animalType,
    cow: cowPayload(fields, state.cow),
    requirements_override: state.override,
    diets: state.diets.map(diet => ({
      name: diet.name.trim(),
      amounts: Object.fromEntries(
        used.filter(id => (diet.amounts[id] ?? 0) > 0).map(id => [id, diet.amounts[id]])
      )
    })),
    prices,
    limits
  }
}

/** Dietas de exemplo escaladas para somarem `totalKg` de MS por dia. */
export function exampleDiets(totalKg: number, firstUid: number): ModuleDiet[] {
  return EXAMPLE_DIETS.map((example, index) => ({
    uid: firstUid + index,
    name: example.name,
    amounts: Object.fromEntries(
      Object.entries(example.shares).map(([id, share]) => [Number(id), Math.round(share * totalKg * 100) / 100])
    )
  }))
}

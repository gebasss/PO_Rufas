// Contratos da API Python (backend/dietopt/server.py)

export interface Feed {
  id: number
  name: string
  description: string
  kind: string
  category: string
  dm: number
  cp: number
  ndf: number
  ee: number
  tdn: number
  calcium: number
  phosphorus: number
  default_price: number | null
  nel: number
  default_max: number
}

export interface Defaults {
  milk_price: number
  prices: Record<string, number>
}

/** Alimento escolhido para a ração: preço (US$/kg MS) e limites (kg MS/vaca/dia). */
export interface SelectedFeed {
  price: number
  min: number
  max: number
}
export type Selected = Record<number, SelectedFeed>

export interface SimParams {
  milkPrice: number
  years: number
  maxReduction: number
}

// ---- Exercício do quadro (PL)
export interface ToyFood {
  name: string
  cost: number
  carb: number
  prot: number
}
export interface ToyBound {
  name: string
  min: number
  max: number
}
export interface ToyResult {
  feasible: boolean
  status: string
  cost: number | null
  amounts: Record<string, number>
  nutrient_totals: Record<string, number>
  shadow_prices: Record<string, number>
  reduced_costs: Record<string, number>
}
export interface ToySensRow {
  cenario: string
  Res: number | null
  amounts: Record<string, number>
  [column: string]: string | number | null | Record<string, number>
}
export interface ToySens {
  columns: string[]
  rows: ToySensRow[]
}

// ---- Curva de lactação
export interface Wood {
  l: number
  m: number
  n: number
}
export interface LactationInfo {
  curves: Record<string, number[]>
  wood: Record<string, Wood>
  wood_from_rufas?: boolean
  milestones: { pev: number; proximo_parto: number; secagem: number }
}

// ---- Simulação do RuFaS
export interface SimSummary {
  cenario: string
  ok: boolean
  leite_kg: number
  receita: number
  custo_alimentacao: number
  custo_vaca_dia: number
  margem: number
  segundos: number
  milk_price: number
  reducao_leite: number
  max_reducao: number
}
export interface Requirement {
  NEl_requirement: number | null
  NEmaint_requirement: number | null
  MP_requirement: number | null
  Ca_requirement: number | null
  P_req: number | null
  DMIest_requirement: number | null
  avg_BW: number | null
}
export interface SimResult {
  summary: SimSummary
  feeds: { id: number; label: string; price: number | null }[]
  daily: { day: number[]; milk_kg: number[]; milking_cows: number[]; avg_dim: number[] }
  intervals: {
    day: number[]
    ration: Record<string, number>[]
    cows: number[]
    requirements: Requirement[]
    cost_per_cow_day: number[]
  }
  lactation: LactationInfo
  average_ration: Record<string, number>
}

// ---- Sensibilidade
export interface SensRow {
  cenario: string
  Res: number | null
  leite_kg?: number
  receita?: number
  custo_alimentacao?: number
  custo_vaca_dia?: number
  reducao_leite?: number
  ration?: Record<string, number>
  erro?: string
  [column: string]: string | number | null | undefined | Record<string, number>
}
export interface SensResult {
  columns: string[]
  rows: SensRow[]
  effects: { fator: string; spearman: number | null }[]
  feeds: { id: number; label: string }[]
}
export interface SensFactor {
  key: string
  label: string
  low: number
  high: number
}

export interface Job<T> {
  id: string
  kind: string
  status: 'queued' | 'running' | 'done' | 'error'
  done: number
  total: number
  error: string
  result?: T
}

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
  /** Só no padrão NRC (Eq. 2-3); no NASEM a energia depende da dieta e vão `starch` e `de_base`. */
  nel?: number
  starch?: number
  de_base?: number
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

// ---- Avaliar dietas (vaca real): contratos de /api/module/* (FSD, Anexo B.7)
export type NutrientStandard = 'NASEM' | 'NRC'
export type ModuleCategory = 'LAC_COW' | 'CLOSE_UP' | 'GROWING'

export interface ModuleField {
  key: string
  label: string
  unit: string
  required: boolean
  min: number | null
  max: number | null
  integer: boolean
  choices: string[]
  /** "vaca"; "dieta" (na avaliação vem da própria dieta); "lote" (metano e N urinário, só no NASEM). */
  group: 'vaca' | 'dieta' | 'lote'
}
export interface ModuleRequirementField {
  key: string
  label: string
  unit: string
}
export interface ModuleDefaults {
  standard: NutrientStandard
  category: ModuleCategory
  label: string
  animal_type: string
  animal_types: string[]
  fields: ModuleField[]
  diet_defaults: Record<string, number>
  requirement_fields: ModuleRequirementField[]
  constraints: { id: string; label: string; rufas_name: string; kind: string }[]
}
export interface ModuleRequirements {
  requirements: Record<string, number | null>
  calculated: Record<string, number | null>
  overridden: string[]
  warnings: string[]
}

export type ConstraintStatus = 'ok' | 'no_limite' | 'violada' | 'indisponivel'
export interface ModuleConstraint {
  id: string
  label: string
  unit: string
  /** Classe de linearização: L (exata), E (razão, exata) ou A (aproximada, escalares congelados). */
  kind: 'L' | 'E' | 'A'
  sense: 'ge' | 'le'
  requirement: number | null
  /** Ausentes (junto com `error_pct` e `slack`) quando o estado é `indisponivel`; `note` diz o que falta. */
  supply_linear?: number | null
  supply_nonlinear?: number | null
  error_pct?: number | null
  slack?: number | null
  status: ConstraintStatus
  note?: string
}
export interface ModuleDietResult {
  name: string
  cost: number
  cost_per_kg: number | null
  feasible: boolean
  violation: number
  violated: string[]
  incomplete: boolean
  intake: Record<string, number | null>
  requirements: Record<string, number | null>
  constraints: ModuleConstraint[]
  warnings: string[]
}
export interface ModuleEvaluation {
  standard: NutrientStandard
  category: ModuleCategory
  animal_type: string
  requirements: Record<string, number | null>
  requirement_warnings: string[]
  diets: ModuleDietResult[]
  /** Nomes das dietas, da menos para a mais recomendada. */
  ranking: string[]
  best: string | null
  warnings: string[]
}

// ---- Comparação do modelo linear com o RuFaS (FSD, Anexo B.8; POST /api/module/compare)
export interface ComparisonProbe {
  /** Fator aplicado às quantidades da dieta (0,95 = −5%). */
  scale: number
  supply_linear: number
  supply_original: number
  slack_linear: number
  slack_original: number
  /** Com sinal, em % da oferta original. */
  error_pct: number
  same_state: boolean
}
/** Restrição sem cálculo (`status_linear: 'indisponivel'`) traz só `note`; as demais, todos os números. */
export interface ComparisonRow {
  id: string
  label: string
  unit: string
  kind: 'L' | 'E' | 'A'
  sense: 'ge' | 'le'
  requirement: number | null
  status_linear: ConstraintStatus
  note?: string
  supply_linear?: number
  supply_original?: number
  slack_linear?: number
  slack_original?: number
  point_error_pct?: number
  probes?: ComparisonProbe[]
  max_error_pct?: number
  within_tolerance?: boolean
  identity_ok?: boolean
  status_original?: ConstraintStatus
  same_state_in_probes?: boolean
}
export interface ComparisonDiet {
  name: string
  feasible: boolean
  incomplete: boolean
  n_compared: number
  n_unavailable: number
  max_error_pct: number
  worst_constraint: { id: string; label: string } | null
  n_above_tolerance: number
  within_tolerance: boolean
  identity_ok: boolean
  same_state_in_probes: boolean
  constraints: ComparisonRow[]
}
export interface ModuleComparison {
  standard: NutrientStandard
  category: ModuleCategory
  animal_type: string
  tolerance_pct: number
  scales: number[]
  diets: ComparisonDiet[]
  summary: {
    n_diets: number
    n_compared: number
    max_error_pct: number
    worst: { diet: string; id: string; label: string } | null
    n_above_tolerance: number
    n_diets_above_tolerance: number
    identity_ok: boolean
    same_state_in_probes: boolean
  }
  warnings: string[]
  /** Mesma tabela em CSV (uma linha por dieta e restrição). */
  csv: string
}

// ---- Dieta ótima e comparação com o SLSQP do RuFaS (FSD, Anexo B.8, fase 2; job `optimize`)
export type OptimizationResolution = 'rapida' | 'normal' | 'fina'
export interface RufasRun {
  seed: number
  success: boolean
  cost: number
  amounts: Record<string, number>
  iterations: number
  seconds: number
  /** Viável nas restrições originais, com as exigências da otimização. */
  feasible: boolean
  violated: string[]
}
export interface RufasComparison {
  runs: RufasRun[]
  n_runs: number
  n_success: number
  cost_min: number | null
  cost_median: number | null
  cost_max: number | null
  best_seed: number | null
  /** Variação do custo do LP em relação ao melhor do RuFaS, em %; negativa = o LP é mais barato. */
  lp_gap_pct: number | null
}
export interface OptimalDiet {
  amounts: Record<string, number>
  cost: number
  cost_per_kg: number
  scalars: { dmi: number; tdn_percentage: number; concentrate_percentage: number; total_starch_kg?: number }
  regime: 'sem_desconto' | 'com_desconto'
  energy_branch: string | null
  /** A dieta atende a todas as restrições originais do RuFaS. */
  verified: boolean
  evaluation: ModuleDietResult
}
export interface ModuleOptimization {
  standard: NutrientStandard
  category: ModuleCategory
  animal_type: string
  status: 'ok' | 'infeasible'
  message?: string
  requirements: Record<string, number | null>
  feed_ids: number[]
  resolution: OptimizationResolution
  search: { points: number; feasible_points: number; seconds: number }
  warnings: string[]
  diet?: OptimalDiet
  /** Variação do custo por unidade da exigência (ou do limite), com os escalares globais fixos. */
  shadow_prices?: { id: string; label: string; value: number }[]
  rufas?: RufasComparison
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
  NEa_requirement?: number | null
  NEg_requirement?: number | null
  NEpreg_requirement?: number | null
  MP_requirement: number | null
  Ca_requirement: number | null
  P_req: number | null
  P_req_process?: number | null
  DMIest_requirement: number | null
  avg_BW: number | null
}

/** Verificação de consistência da ração (RF-27; FSD, A.4): só informa, não altera margem nem custo. */
export type CheckStatus = 'ok' | 'warn' | 'alert'
export interface RationCheck {
  id: string
  label: string
  status: CheckStatus
  value: string
  limit: string
  detail: string
  metrics: Record<string, number>
}
/** Linha do balanço nutricional (RF-19), calculado pelo próprio RuFaS a cada intervalo e resumido. */
export interface BalanceRow {
  id: string
  label: string
  unit: string
  /** `surplus`: oferta − exigência; `range`: 0 dentro da faixa; `floor`: % − mínimo; `ceiling`: máximo − %. */
  kind: 'surplus' | 'range' | 'floor' | 'ceiling'
  requirement: number | null
  supply?: number
  margin_pct?: number | null
  /** Média dos intervalos e a pior (mais desfavorável). */
  difference: number
  worst_difference: number
  status: 'ok' | 'deficit' | 'fora'
  note: string
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
  checks?: RationCheck[]
  checks_summary?: Record<CheckStatus, number>
  balance?: BalanceRow[]
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
  status: 'queued' | 'running' | 'done' | 'error' | 'cancelled'
  done: number
  total: number
  error: string
  result?: T
}

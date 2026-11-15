/** Tamanho e limites da análise de sensibilidade (espelham `backend/dietopt/sensitivity.py`). */
import type { SensitivityLimits } from '@/lib/types'

/** Usados enquanto o servidor não respondeu; os valores oficiais vêm de `/api/defaults`. */
export const DEFAULT_SENS_LIMITS: SensitivityLimits = { min_levels: 2, max_levels: 12, max_samples: 100, max_simulations: 100 }

export interface SensPlan {
  scenarios: number
  simulations: number
}

/** Cenários e simulações do RuFaS: o preço do leite só recalcula a receita, sem simulação nova. */
export function sensitivityPlan(feedFactors: number, factors: number, method: string, n: number): SensPlan {
  if (factors === 0) return { scenarios: 0, simulations: 0 }

  if (method === 'grid') return { scenarios: n ** factors, simulations: n ** feedFactors }

  return { scenarios: n, simulations: feedFactors > 0 ? n : 1 }
}

/** Maior número de níveis (grade) ou de amostras (hipercubo latino) que a tela aceita. */
export const maxLevels = (method: string, limits: SensitivityLimits) => (method === 'grid' ? limits.max_levels : limits.max_samples)

/** Mensagem quando a análise passa do limite de simulações; `null` se cabe. */
export function sensitivityProblem(plan: SensPlan, limits: SensitivityLimits): string | null {
  return plan.simulations > limits.max_simulations
    ? `Esta análise exigiria ${plan.simulations.toLocaleString('pt-BR')} simulações do RuFaS; o limite é ${limits.max_simulations}. Reduza os níveis ou os fatores.`
    : null
}

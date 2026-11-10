import type { HerdLimits } from '@/lib/types'

/** Limites usados enquanto o servidor não respondeu (os mesmos de `backend/dietopt/herd.py`). */
export const DEFAULT_HERD: HerdLimits = { default: 100, min: 60, max: 500, warn: 250 }

/** Segundos de uma simulação de 1 ano com o rebanho padrão (a estimativa que a interface já usava). */
const BASE_SECONDS = 17
/**
 * O tempo cresce devagar com o rebanho: medido em 03/11/2026 (1 ano, NRC), 100 vacas levaram 27 s, 200 vacas 37 s e 500 vacas
 * 57 s, ou seja, cerca de 20 s fixos mais 0,075 s por vaca. A memória vai de 0,7 GB (100 vacas) a 1,0 GB (500 vacas).
 */
const FIXED_SECONDS = 19.5
const SECONDS_PER_COW = 0.075
const BASE_MEMORY_MB = 610
const MEMORY_MB_PER_COW = 0.7

/** Por que o número de vacas não vale (ou `null` se vale). */
export function herdProblem(cows: number, limits: HerdLimits): string | null {
  if (!Number.isFinite(cows) || !Number.isInteger(cows)) return 'Informe o número de vacas como um número inteiro.'
  if (cows < limits.min || cows > limits.max) return `O número de vacas deve ficar entre ${limits.min} e ${limits.max}.`

  return null
}

/** Segundos estimados de uma simulação, relativos ao rebanho padrão (100 vacas = 17 s). */
export const secondsPerSimulation = (cows: number) => (BASE_SECONDS * (FIXED_SECONDS + SECONDS_PER_COW * cows)) / (FIXED_SECONDS + SECONDS_PER_COW * 100)

/** Memória estimada de uma simulação, em GB. */
export const memoryGb = (cows: number) => (BASE_MEMORY_MB + MEMORY_MB_PER_COW * cows) / 1024

/** Aviso de tempo e memória para rebanhos grandes (acima de `limits.warn`); `null` para os demais. */
export function herdNote(cows: number, limits: HerdLimits): string | null {
  if (cows <= limits.warn) return null

  const seconds = Math.round(secondsPerSimulation(cows))

  return `Rebanho grande: cada simulação leva cerca de ${seconds} s e ocupa cerca de ${memoryGb(cows).toLocaleString('pt-BR', { maximumFractionDigits: 1 })} GB de memória. Na sensibilidade, duas simulações rodam ao mesmo tempo e o tempo total cresce com o número de cenários.`
}

/**
 * Ciclo reprodutivo da tela Curva de lactação: PEV, gestação e dias de secagem, com limites e marcos.
 * Os limites são só para a tela não aceitar valores sem sentido (não vêm da literatura nem do RuFaS).
 */
export interface CycleInput {
  pev: number
  gestation: number
  dry: number
}

export interface CycleRange {
  min: number
  max: number
}

export const CYCLE_RANGES = {
  pev: { min: 0, max: 200 },
  gestation: { min: 200, max: 300 },
  dry: { min: 0, max: 120 }
} as const satisfies Record<keyof CycleInput, CycleRange>

export type CycleProblems = Partial<Record<keyof CycleInput, string>>

const LABEL: Record<keyof CycleInput, string> = { pev: 'O PEV', gestation: 'A gestação', dry: 'A secagem' }

/** Mensagem de cada campo fora do limite (inteiros entre `min` e `max`); objeto vazio se está tudo certo. */
export function cycleProblems(input: CycleInput): CycleProblems {
  const problems: CycleProblems = {}

  for (const key of Object.keys(CYCLE_RANGES) as (keyof CycleInput)[]) {
    const { min, max } = CYCLE_RANGES[key]
    const value = input[key]

    if (!Number.isFinite(value)) problems[key] = `${LABEL[key]} precisa de um número de dias.`
    else if (!Number.isInteger(value)) problems[key] = `${LABEL[key]} deve ser um número inteiro de dias.`
    else if (value < min || value > max) problems[key] = `${LABEL[key]} vai de ${min} a ${max} dias.`
  }

  return problems
}

export interface Cycle {
  /** Dia em lactação do fim do PEV. */
  pev: number
  /** Dia em lactação do parto seguinte (PEV + gestação). */
  calving: number
  /** Dia em lactação em que a vaca é seca (parto seguinte − dias de secagem). */
  dryDay: number
}

/** Marcos do ciclo, ou `null` se algum campo tem problema. Com os limites acima, a secagem sempre cai depois do dia 80. */
export function cycleMarks(input: CycleInput): Cycle | null {
  if (Object.keys(cycleProblems(input)).length > 0) return null

  const calving = input.pev + input.gestation

  return { pev: input.pev, calving, dryDay: calving - input.dry }
}

/**
 * Escala "bonita" para o eixo de um gráfico: degraus de 1, 2 ou 5 vezes uma potência de 10 (0, 10, 20, 30...), no
 * lugar dos degraus arbitrários que o Recharts escolhe sozinho (como 0, 9, 18, 27, 36).
 */
export interface NiceScale {
  domain: [number, number]
  ticks: number[]
}

/** No máximo este número de intervalos entre os traços do eixo (6 intervalos = 7 traços). */
const MAX_INTERVALS = 6

/** Menor degrau {1, 2, 5} × 10^k que cobre o intervalo com poucos traços. */
function niceStep(span: number) {
  const exponent = Math.floor(Math.log10(span / MAX_INTERVALS))

  for (let e = exponent; e <= exponent + 2; e += 1) {
    for (const mantissa of [1, 2, 5]) {
      const step = mantissa * 10 ** e

      if (span / step <= MAX_INTERVALS) return step
    }
  }

  return span
}

/** Arredonda sem deixar o erro de ponto flutuante aparecer (0.30000000000000004 vira 0.3). */
const clean = (value: number, step: number) => {
  const digits = Math.max(0, -Math.floor(Math.log10(step)) + 1)

  return Number(value.toFixed(digits))
}

/**
 * Domínio e traços do eixo para os valores `min` e `max` dos dados. Com `fromZero`, o eixo começa em zero (áreas
 * empilhadas); sem ele, o eixo acompanha a faixa dos dados. Devolve `null` quando não há valores válidos.
 */
export function niceScale(min: number, max: number, fromZero = false): NiceScale | null {
  if (!Number.isFinite(min) || !Number.isFinite(max)) return null

  let low = fromZero ? Math.min(0, min) : min
  let high = fromZero ? Math.max(0, max) : max

  if (high === low) {
    const pad = Math.abs(high) * 0.1 || 1

    low -= pad
    high += pad
  }

  const step = niceStep(high - low)
  const start = clean(Math.floor(low / step) * step, step)
  const end = clean(Math.ceil(high / step) * step, step)
  const ticks: number[] = []

  for (let value = start; value <= end + step / 2; value += step) ticks.push(clean(value, step))

  return { domain: [start, end], ticks }
}

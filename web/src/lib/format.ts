const cache = new Map<string, Intl.NumberFormat>()

function formatter(digits: number) {
  let f = cache.get(String(digits))

  if (!f) {
    f = new Intl.NumberFormat('pt-BR', { minimumFractionDigits: digits, maximumFractionDigits: digits })
    cache.set(String(digits), f)
  }

  return f
}

export const nf = (value: number | null | undefined, digits = 2) =>
  value === null || value === undefined || Number.isNaN(value) ? '—' : formatter(digits).format(value)

/** Variação em % com sinal ("+1,2%", "-0,3%"); abaixo de meio passo da última casa vale zero (evita "-0,00%"). */
export const signedPct = (value: number | null | undefined, digits = 2) =>
  value === null || value === undefined || Number.isNaN(value)
    ? '—'
    : Math.abs(value) < 0.5 * 10 ** -digits
      ? `${formatter(digits).format(0)}%`
      : `${value > 0 ? '+' : ''}${formatter(digits).format(value)}%`

export const usd = (value: number | null | undefined, digits = 0) =>
  value === null || value === undefined || Number.isNaN(value) ? '—' : `US$ ${formatter(digits).format(value)}`

/** Nome curto de um alimento para legendas e tabelas. */
export function shortName(label: string, max = 34) {
  const text = label.replace(/\s+/g, ' ').trim()

  return text.length > max ? `${text.slice(0, max - 1)}…` : text
}

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

export const usd = (value: number | null | undefined, digits = 0) =>
  value === null || value === undefined || Number.isNaN(value) ? '—' : `US$ ${formatter(digits).format(value)}`

/** Nome curto de um alimento para legendas e tabelas. */
export function shortName(label: string, max = 34) {
  const text = label.replace(/\s+/g, ' ').trim()

  return text.length > max ? `${text.slice(0, max - 1)}…` : text
}

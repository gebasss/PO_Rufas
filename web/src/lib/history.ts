import { nf, signedPct, usd } from '@/lib/format'
import type { CowScenario, ModuleScenario, RunKind, RunMeta, SensSetup } from '@/lib/types'

export const KIND_LABEL: Record<RunKind, string> = {
  simulation: 'Simulação',
  sensitivity: 'Sensibilidade',
  evaluation: 'Avaliação de dietas',
  optimization: 'Dieta ótima'
}

/** Tela em que cada tipo de execução pode ser reaberta ("duplicar"). */
export const KIND_PAGE: Record<RunKind, string> = {
  simulation: '/vaca',
  sensitivity: '/sensibilidade',
  evaluation: '/',
  optimization: '/'
}

const num = (value: unknown) => (typeof value === 'number' ? value : null)

/** Uma linha com o resultado principal da execução, para a tabela. */
export function summaryLine(run: RunMeta): string {
  const s = run.summary

  if (run.status === 'error') return run.error ?? 'Falhou'

  switch (run.kind) {
    case 'simulation':
      return `Margem ${usd(num(s.margem), 0)} · ${nf((num(s.leite_kg) ?? 0) / 1000, 0)} t de leite`
    case 'sensitivity':
      return `Margem de ${usd(num(s.worst), 0)} a ${usd(num(s.best), 0)} em ${s.n_ok} de ${s.n_scenarios} cenários`
    case 'evaluation':
      return s.best ? `Melhor: ${s.best} (${usd(num(s.best_cost), 2)}/dia)` : `Nenhuma das ${s.n_diets} dietas é viável`
    case 'optimization':
      return s.status === 'ok'
        ? `${usd(num(s.cost), 2)}/dia${s.gap_pct != null ? ` · ${signedPct(num(s.gap_pct), 2)} do RuFaS` : ''}`
        : 'Sem dieta viável'
  }
}

/** Data curta (dd/mm hh:mm) de um ISO local sem fuso. */
export function shortDate(iso: string) {
  const [date, time] = iso.split('T')
  const [, month, day] = date.split('-')

  return `${day}/${month} ${time.slice(0, 5)}`
}

type Params = Record<string, unknown>

const feedsOf = (params: Params): { id: number; price: number; min: number; max: number }[] => {
  const prices = (params.prices ?? {}) as Record<string, number>
  const limits = (params.limits ?? {}) as Record<string, [number, number]>
  const ids = ((params.feeds ?? params.feed_ids ?? Object.keys(prices)) as (string | number)[]).map(Number)

  return ids.map(id => ({ id, price: prices[id] ?? 0, min: limits[id]?.[0] ?? 0, max: limits[id]?.[1] ?? 100 }))
}

/** Cenário da tela Vaca leiteira a partir dos parâmetros de uma simulação ou de uma sensibilidade. */
export function cowScenarioOf(params: Params): CowScenario {
  const feeds = feedsOf(params)
  const factors = (params.factors ?? []) as { key: string; low: number; high: number }[]
  const base: CowScenario = {
    standard: 'NRC',
    params: {
      milkPrice: Number(params.milk_price ?? 0.45),
      years: Number(params.years ?? 1),
      maxReduction: Number(params.max_milk_reduction ?? 5),
      cowNum: Number(params.cow_num ?? 100)
    },
    feeds
  }

  if (!factors.length) return base

  const on = new Map(factors.map(f => [f.key, f]))
  const overrides: SensSetup['overrides'] = {}

  for (const feed of feeds) {
    const factor = on.get(String(feed.id))

    overrides[feed.id] = { on: !!factor, low: factor?.low ?? +(feed.price * 0.5).toFixed(3), high: factor?.high ?? +(feed.price * 1.5).toFixed(3) }
  }

  const milk = on.get('milk_price')

  overrides.milk_price = {
    on: !!milk,
    low: milk?.low ?? +(base.params.milkPrice * 0.8).toFixed(3),
    high: milk?.high ?? +(base.params.milkPrice * 1.2).toFixed(3)
  }

  return { ...base, sensitivity: { method: String(params.method ?? 'grid'), levels: Number(params.n ?? 3), factors: overrides } }
}

/** Cenário da tela Avaliar dietas a partir dos parâmetros de uma avaliação de dietas ou de uma dieta ótima. */
export function moduleScenarioOf(params: Params): ModuleScenario {
  return {
    standard: (params.standard as ModuleScenario['standard']) ?? 'NASEM',
    category: params.category as ModuleScenario['category'],
    animalType: String(params.animal_type ?? ''),
    cow: (params.cow ?? {}) as ModuleScenario['cow'],
    override: (params.requirements_override ?? {}) as ModuleScenario['override'],
    feeds: feedsOf(params),
    diets: ((params.diets ?? []) as ModuleScenario['diets']).map(d => ({ name: d.name, amounts: d.amounts })),
    tolerance: 1,
    resolution: (params.resolution as ModuleScenario['resolution']) ?? 'normal',
    seeds: Number(params.seeds ?? 5)
  }
}

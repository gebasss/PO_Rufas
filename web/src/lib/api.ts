import type {
  Defaults,
  Feed,
  Job,
  LactationInfo,
  ModuleComparison,
  ModuleDefaults,
  ModuleEvaluation,
  ModuleRequirements,
  NutrientStandard,
  ToyResult,
  ToySens
} from '@/lib/types'

async function request<T>(path: string, body?: unknown): Promise<T> {
  const res = await fetch(
    path,
    body === undefined
      ? undefined
      : { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }
  )
  const data = await res.json()

  if (!res.ok) throw new Error((data as { error?: string }).error ?? res.statusText)

  return data as T
}

export const api = {
  feeds: (standard: NutrientStandard = 'NRC') => request<Feed[]>(`/api/feeds?standard=${standard}`),
  defaults: () => request<Defaults>('/api/defaults'),
  lactation: () => request<LactationInfo>('/api/lactation'),
  toy: (body: unknown) => request<ToyResult>('/api/toy', body),
  toySensitivity: (body: unknown) => request<ToySens>('/api/toy/sensitivity', body),
  moduleDefaults: (standard: NutrientStandard, category: string, animalType: string) =>
    request<ModuleDefaults>(
      `/api/module/defaults?standard=${standard}&category=${category}&animal_type=${animalType}`
    ),
  moduleRequirements: (body: unknown) => request<ModuleRequirements>('/api/module/requirements', body),
  moduleEvaluate: (body: unknown) => request<ModuleEvaluation>('/api/module/evaluate', body),
  moduleCompare: (body: unknown) => request<ModuleComparison>('/api/module/compare', body)
}

const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

/** Dispara um job do RuFaS e consulta o andamento até terminar. */
export async function runJob<T>(
  kind: 'simulate' | 'sensitivity' | 'optimize',
  body: unknown,
  onProgress: (done: number, total: number, status: Job<T>['status']) => void,
  options: { onStart?: (jobId: string) => void; intervalMs?: number } = {}
): Promise<T> {
  const job = await request<Job<T>>(`/api/jobs/${kind}`, body)

  options.onStart?.(job.id)

  for (;;) {
    const current = await request<Job<T>>(`/api/jobs/${job.id}`)

    onProgress(current.done, current.total, current.status)

    if (current.status === 'done') return current.result as T
    if (current.status === 'cancelled') throw new JobCancelledError()
    if (current.status === 'error') throw new Error(current.error)

    await sleep(options.intervalMs ?? 1500)
  }
}

/** O job terminou porque o usuário o cancelou (não é uma falha). */
export class JobCancelledError extends Error {
  constructor() {
    super('Cancelado')
  }
}

/** Pede o cancelamento de um job; ele para na próxima verificação. */
export const cancelJob = (jobId: string) => request<Job<unknown>>(`/api/jobs/${jobId}/cancel`, {})

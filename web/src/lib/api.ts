import type { Defaults, Feed, Job, LactationInfo, ToyResult, ToySens } from '@/lib/types'

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
  feeds: () => request<Feed[]>('/api/feeds'),
  defaults: () => request<Defaults>('/api/defaults'),
  lactation: () => request<LactationInfo>('/api/lactation'),
  toy: (body: unknown) => request<ToyResult>('/api/toy', body),
  toySensitivity: (body: unknown) => request<ToySens>('/api/toy/sensitivity', body)
}

const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

/** Dispara um job do RuFaS e consulta o andamento até terminar. */
export async function runJob<T>(
  kind: 'simulate' | 'sensitivity',
  body: unknown,
  onProgress: (done: number, total: number, status: Job<T>['status']) => void
): Promise<T> {
  const job = await request<Job<T>>(`/api/jobs/${kind}`, body)

  for (;;) {
    const current = await request<Job<T>>(`/api/jobs/${job.id}`)

    onProgress(current.done, current.total, current.status)

    if (current.status === 'done') return current.result as T
    if (current.status === 'error') throw new Error(current.error)

    await sleep(1500)
  }
}

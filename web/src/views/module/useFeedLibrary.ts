'use client'

import { useEffect, useMemo, useState } from 'react'

import { api } from '@/lib/api'
import type { Feed, NutrientStandard } from '@/lib/types'

// A biblioteca de cada padrão só muda com o código; guardá-la evita pedir de novo a cada troca de padrão ou de tela.
const cache = new Map<NutrientStandard, Feed[]>()

/** Biblioteca de alimentos do padrão (`GET /api/feeds?standard=`). */
export function useFeedLibrary(standard: NutrientStandard, enabled: boolean) {
  const [version, setVersion] = useState(0)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!enabled || cache.has(standard)) return

    let cancelled = false

    api
      .feeds(standard)
      .then(feeds => {
        cache.set(standard, feeds)

        if (!cancelled) {
          setError(null)
          setVersion(v => v + 1)
        }
      })
      .catch(e => !cancelled && setError(e instanceof Error ? e.message : 'Falha ao carregar os alimentos'))

    return () => {
      cancelled = true
    }
  }, [standard, enabled])

  const feeds = cache.get(standard) ?? null
  // `version` entra só para a memoização reagir à chegada da biblioteca.
  const byId = useMemo(
    () => Object.fromEntries((feeds ?? []).map(f => [f.id, f])) as Record<number, Feed>,
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [feeds, version]
  )

  return { feeds, byId, loading: feeds === null && error === null, error }
}

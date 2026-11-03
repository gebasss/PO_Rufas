import { Suspense } from 'react'

import HistoryView from '@/views/HistoryView'

// `useSearchParams` (o `?id=` do detalhe) exige um limite de Suspense na exportação estática.
export default function Page() {
  return (
    <Suspense>
      <HistoryView />
    </Suspense>
  )
}

'use client'

import { useCallback } from 'react'

import { useRouter, useSearchParams } from 'next/navigation'

import { toast } from 'sonner'

import { PageHeader } from '@/components/shared'
import { api } from '@/lib/api'
import { downloadText } from '@/lib/download'
import { cowScenarioOf, KIND_PAGE, moduleScenarioOf } from '@/lib/history'
import { useApp } from '@/providers/AppProvider'
import RunDetail from '@/views/history/RunDetail'
import RunsTable from '@/views/history/RunsTable'
import { moduleStateFromScenario } from '@/views/module/model'

const message = (error: unknown, fallback: string) => (error instanceof Error ? error.message : fallback).split('\n')[0]

/** Execuções: a tabela do histórico e, com `?id=`, o detalhe de uma execução. */
export default function HistoryView() {
  const router = useRouter()
  const id = useSearchParams().get('id')
  const { loadCowScenario, setModuleState, setExerciseMode } = useApp()

  const open = useCallback((runId: string) => router.push(`/execucoes/?id=${runId}`), [router])
  const back = useCallback(() => router.push('/execucoes/'), [router])

  // "Duplicar": abre os parâmetros da execução na tela de origem, para editar e executar de novo.
  const duplicate = useCallback(
    async (runId: string) => {
      try {
        const run = await api.historyRun(runId)

        if (run.kind === 'simulation' || run.kind === 'sensitivity') {
          loadCowScenario(cowScenarioOf(run.params))
        } else {
          setModuleState(moduleStateFromScenario(moduleScenarioOf(run.params)))
          setExerciseMode('module')
        }

        toast.success('Parâmetros abertos na tela. Ajuste o que quiser e execute de novo.')
        router.push(KIND_PAGE[run.kind])
      } catch (error) {
        toast.error(message(error, 'Falha ao duplicar a execução'))
      }
    },
    [loadCowScenario, router, setExerciseMode, setModuleState]
  )

  const exportRun = useCallback(async (runId: string) => {
    try {
      const run = await api.historyRun(runId)

      downloadText(`execucao-${runId}.json`, `${JSON.stringify(run, null, 2)}\n`, 'application/json;charset=utf-8')
    } catch (error) {
      toast.error(message(error, 'Falha ao exportar a execução'))
    }
  }, [])

  return (
    <>
      <PageHeader
        title='Execuções'
        description='O histórico de simulações, análises de sensibilidade, avaliações de dietas e dietas ótimas, guardado no servidor. Marque uma simulação com a estrela para usá-la como cenário-base dos indicadores.'
      />
      {id ? (
        <RunDetail id={id} onBack={back} onDuplicate={duplicate} onExport={exportRun} onDeleted={back} />
      ) : (
        <RunsTable onView={open} onDuplicate={duplicate} onExport={exportRun} />
      )}
    </>
  )
}

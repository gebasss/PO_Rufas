'use client'

import { Segmented } from '@/components/Segmented'
import { PageHeader } from '@/components/shared'
import { useApp, type ExerciseMode } from '@/providers/AppProvider'

import ModuleView from './ModuleView'
import ToyView from './ToyView'

const MODES: { value: ExerciseMode; label: string }[] = [
  { value: 'simple', label: 'Exercício simples' },
  { value: 'module', label: 'Avaliar dietas (vaca real)' }
]

const DESCRIPTIONS: Record<ExerciseMode, string> = {
  simple:
    'Dieta de custo mínimo respeitando o mínimo e o máximo diário de cada nutriente. É a modelagem de Pesquisa Operacional que dá base ao restante do sistema.',
  module:
    'Compara dietas já montadas para uma vaca real: exigências do NASEM (ou do NRC), restrições lineares calculadas pelas equações do RuFaS, custo em dólares e ranking das dietas.'
}

export default function ExerciseView() {
  const { exerciseMode, setExerciseMode } = useApp()

  return (
    <>
      <PageHeader
        title='Exercício do quadro'
        description={DESCRIPTIONS[exerciseMode]}
        actions={<Segmented label='Tipo de exercício' value={exerciseMode} options={MODES} onChange={setExerciseMode} />}
      />
      {exerciseMode === 'simple' ? <ToyView /> : <ModuleView />}
    </>
  )
}

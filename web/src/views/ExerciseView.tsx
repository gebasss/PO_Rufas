'use client'

import { PageHeader } from '@/components/shared'

import ModuleView from './ModuleView'

export default function ExerciseView() {
  return (
    <>
      <PageHeader
        title='Exercício do quadro'
        description='Compara dietas já montadas para uma vaca real: exigências do NASEM (ou do NRC), restrições lineares calculadas pelas equações do RuFaS, custo em dólares e ranking das dietas.'
      />
      <ModuleView />
    </>
  )
}

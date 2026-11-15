import type { ReactNode } from 'react'

import { PageHeader } from '@/components/shared'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

function Section({ title, description, className, children }: { title: string; description?: string; className?: string; children: ReactNode }) {
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        {description ? <CardDescription>{description}</CardDescription> : null}
      </CardHeader>
      <CardContent>
        <ul className='text-muted-foreground list-disc space-y-2 pl-5 text-sm'>{children}</ul>
      </CardContent>
    </Card>
  )
}

const Strong = ({ children }: { children: ReactNode }) => <strong className='text-foreground'>{children}</strong>

export default function AboutView() {
  return (
    <>
      <PageHeader
        title='Premissas e limites'
        description='O que o modelo assume, o que ele não faz e como ler os resultados. Leia antes de usar os números numa decisão real.'
      />

      <div className='grid gap-6 xl:grid-cols-2'>
        <Section title='Como o sistema funciona' description='Do cenário à margem.'>
          <li>
            O <Strong>Ruminante Singular</Strong> avalia dietas já montadas para uma vaca real, com as exigências do{' '}
            <Strong>NASEM (2021)</Strong> ou da <Strong>NRC (2001)</Strong>, e sugere a de menor custo por programação linear,
            comparando-a com o RuFaS.
          </li>
          <li>
            Na <Strong>Vaca leiteira</Strong> você escolhe alimentos, preços e limites e o sistema roda o <Strong>RuFaS</Strong>,
            um simulador de fazenda leiteira, com a NRC (2001). O otimizador do RuFaS formula a ração de{' '}
            <Strong>custo mínimo</Strong> das vacas em lactação, respeitando o preço e os limites de cada alimento.
          </li>
          <li>
            A <Strong>margem</Strong> é a receita do leite menos o custo da alimentação do rebanho no período.
          </li>
          <li>
            Na <Strong>Sensibilidade</Strong>, cada combinação de preços de alimentos vira uma simulação (no máximo 100 por
            análise, com botão Cancelar). O preço do leite só recalcula a receita. A <Strong>Curva de lactação</Strong> mostra a
            curva de Wood e os marcos do ciclo, sem influenciar o custo nem a margem.
          </li>
          <li>
            Tudo roda no seu computador. As execuções ficam em <code>runs/</code> (tela Execuções); você pode salvar o cenário em
            arquivo e exportar tabelas (CSV) e relatórios.
          </li>
        </Section>

        <Section title='O que o modelo assume'>
          <li>
            O leite vem da <Strong>curva de Wood</Strong> calibrada pelo RuFaS. A dieta não prevê um leite próprio.
          </li>
          <li>
            No RuFaS v1.0.6 o leite só cai quando a ração <Strong>não atende às exigências</Strong> (0,25 kg por
            tentativa, até o limite configurado). Por isso a margem varia sobretudo com o custo da dieta.
          </li>
          <li>
            Os limites de inclusão são em <Strong>kg de matéria seca por vaca por dia</Strong>. Para o otimizador não usar
            mineral como enchimento, há tetos padrão: <Strong>0,6 kg</Strong> para minerais, <Strong>0,9 kg</Strong> para gorduras
            (extrato etéreo de 80% ou mais) e <Strong>1 kg</Strong> para alimentos com 60% ou mais de proteína bruta (farinhas de
            carne, peixe, sangue e penas, glúten de milho e, no NASEM, ureia). Você pode alterar qualquer um.
          </li>
          <li>
            A biblioteca NRC do RuFaS só traz <Strong>farelo de arroz</Strong>, não o arroz em grão.
          </li>
          <li>
            Simulação de 1 ou 2 anos, 100 vacas por padrão (de 60 a 500; exemplo freestall do RuFaS) e semente aleatória
            fixa, para resultados reproduzíveis. O RuFaS forma <Strong>uma única ração</Strong> para o grupo de vacas em lactação,
            sem separar por fase da lactação.
          </li>
        </Section>

        <Section title='Como ler os resultados' description='O essencial; o guia de uso (docs/GUIA_RUMINANTE_SINGULAR.docx) detalha cada botão.' className='xl:col-span-2'>
          <li>
            <Strong>Ruminante Singular, cada restrição:</Strong> <Strong>Atende</Strong>; <Strong>No limite</Strong> (folga de até
            0,5% da exigência); <Strong>Violada</Strong>; ou <Strong>Indisponível</Strong> (falta um dado). A dieta é{' '}
            <Strong>Viável</Strong> (todas atendidas), <Strong>Inviável</Strong> ou <Strong>Viável incompleta</Strong> (alguma
            restrição sem dado, como a energia do NASEM sem metano e nitrogênio urinário). A melhor é a viável de menor custo.
          </li>
          <li>
            <Strong>Restrições aproximadas:</Strong> as que não são lineares são calculadas no ponto da dieta e têm erro; a aba
            Linearização mostra quanto, testando 5% a menos e a mais.
          </li>
          <li>
            <Strong>Dieta ótima:</Strong> é a sugestão do otimizador linear do sistema, comparada com a do RuFaS. Ela pode usar
            até 30% a mais de consumo do que o estimado: confira o consumo antes de adotar.
          </li>
          <li>
            <Strong>Vaca leiteira:</Strong> a <Strong>margem</Strong> é o indicador principal. <Strong>Leite perdido</Strong> quer
            dizer que o RuFaS reduziu o leite porque a ração não atendeu às exigências. As verificações{' '}
            <Strong>V1 a V5</Strong> (consumo acima do estimado, FDN, FDN de forragem e amido, gordura, leite perdido) só avisam:
            não alteram custo nem margem. O balanço mostra a oferta contra a exigência (Atende, Déficit ou Fora da faixa).
          </li>
          <li>
            <Strong>Sensibilidade:</Strong> &quot;quanto a margem muda&quot; (em US$) é o <Strong>tamanho</Strong> do efeito de um
            fator; a correlação de Spearman mostra só a <Strong>direção</Strong>. O preço do leite costuma dominar, porque o leite
            simulado quase não muda com a dieta.
          </li>
        </Section>

        <Section title='O que ele não faz'>
          <li>
            <Strong>Os preços iniciais são ilustrativos</Strong>, não cotações. Troque pelos seus.
          </li>
          <li>
            Não substitui um software de formulação nem a revisão de um nutricionista. Os resultados ainda não foram comparados
            com uma referência profissional.
          </li>
          <li>
            A simulação das telas Vaca leiteira e Sensibilidade usa só o padrão <Strong>NRC (2001)</Strong>; o NASEM (2021) está no
            Ruminante Singular.
          </li>
          <li>
            No Ruminante Singular, a energia do NASEM exige <Strong>metano entérico</Strong> e <Strong>nitrogênio urinário</Strong>
            ; sem eles a restrição fica indisponível. A vaca é avaliada em um único dia, com o consumo estimado pela equação do
            padrão escolhido.
          </li>
          <li>
            O otimizador do RuFaS pode não convergir para certos preços. Nesse caso o cenário aparece como{' '}
            <Strong>falhou</Strong> ou com <Strong>leite perdido</Strong>, nunca como um resultado válido.
          </li>
          <li>
            Cada simulação leva cerca de 20 segundos com 100 vacas (mais em rebanhos grandes) e usa cerca de 1,2 GB de memória.
            Abaixo de 60 vacas o RuFaS falha.
          </li>
          <li>
            Ainda estão em avaliação com o professor os limiares das verificações V1 a V5, a tolerância das restrições e a leitura
            de <Strong>PEV + gestação</Strong> na curva de lactação.
          </li>
        </Section>

        <Section title='Créditos e licenças'>
          <li>
            Simulador: <Strong>RuFaS</Strong> v1.0.6 (Ruminant Farm Systems), licença GPLv3, usado sem modificações.
          </li>
          <li>Exigências e composição dos alimentos: NRC, Nutrient Requirements of Dairy Cattle (2001).</li>
          <li>
            Exigências e restrições do Ruminante Singular: National Academies of Sciences, Engineering, and Medicine,{' '}
            <em>Nutrient Requirements of Dairy Cattle</em>, 8ª ed. revisada, 2021. Washington, DC: The National Academies Press.
            doi:10.17226/25806.
          </li>
          <li>
            Interface adaptada do template <Strong>AdminCN</Strong> (shadcn/studio), licença MIT, com componentes shadcn/ui,
            Tailwind CSS e Recharts. O aviso de copyright do template está em <code>web/LICENSE-TEMPLATE.md</code>.
          </li>
        </Section>
      </div>
    </>
  )
}

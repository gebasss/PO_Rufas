import type { ReactNode } from 'react'

import { PageHeader } from '@/components/shared'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

function Section({ title, description, children }: { title: string; description?: string; children: ReactNode }) {
  return (
    <Card>
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
            Você escolhe alimentos, preços e limites. O sistema monta as entradas e roda o <Strong>RuFaS</Strong>, um
            simulador de fazenda leiteira, com as exigências da <Strong>NRC (2001)</Strong>.
          </li>
          <li>
            O otimizador do RuFaS formula a ração de <Strong>custo mínimo</Strong> das vacas em lactação, usando o preço
            e os limites de cada alimento.
          </li>
          <li>
            A <Strong>margem</Strong> é a receita do leite menos o custo da alimentação do rebanho no período.
          </li>
          <li>
            Na sensibilidade, cada combinação de preços de alimentos vira uma simulação. O preço do leite só recalcula a
            receita.
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
            Os limites de inclusão são em <Strong>kg de matéria seca por vaca por dia</Strong>. Minerais, gorduras e
            farinhas proteicas animais têm teto padrão, para o otimizador não usar mineral como enchimento.
          </li>
          <li>
            A NRC 2001 só traz <Strong>farelo de arroz</Strong>; o “arroz” do exercício vira farelo de arroz.
          </li>
          <li>
            Simulação de 1 ou 2 anos, 100 vacas (exemplo freestall do RuFaS) e semente aleatória fixa, para resultados
            reproduzíveis.
          </li>
        </Section>

        <Section title='O que ele não faz'>
          <li>
            <Strong>Os preços iniciais são ilustrativos</Strong>, não cotações. Troque pelos seus.
          </li>
          <li>Não substitui um software de formulação nem a revisão de um nutricionista.</li>
          <li>Não mostra, ainda, o balanço de oferta e exigência de cada nutriente da ração obtida.</li>
          <li>Não exporta tabelas nem relatórios, e não usa o padrão NASEM (2021).</li>
          <li>
            O otimizador do RuFaS pode não convergir para certos preços. Nesse caso o cenário aparece como{' '}
            <Strong>falhou</Strong> ou com <Strong>leite perdido</Strong>, nunca como um resultado válido.
          </li>
        </Section>

        <Section title='Créditos e licenças'>
          <li>
            Simulador: <Strong>RuFaS</Strong> v1.0.6 (Ruminant Farm Systems), licença GPLv3, usado sem modificações.
          </li>
          <li>Exigências e composição dos alimentos: NRC, Nutrient Requirements of Dairy Cattle (2001).</li>
          <li>
            Interface adaptada do template <Strong>AdminCN</Strong> (shadcn/studio), licença MIT, com componentes shadcn/ui,
            Tailwind CSS e Recharts. O aviso de copyright do template está em <code>web/LICENSE-TEMPLATE.md</code>.
          </li>
        </Section>
      </div>
    </>
  )
}

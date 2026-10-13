import { CalculatorIcon, InfoIcon, MilkIcon, SlidersHorizontalIcon, TrendingUpIcon, type LucideIcon } from 'lucide-react'

export interface NavLink {
  label: string
  title: string
  description: string
  href: string
  icon: LucideIcon
}

export interface NavGroup {
  label: string
  items: NavLink[]
}

export const navGroups: NavGroup[] = [
  {
    label: 'Análise',
    items: [
      {
        label: 'Exercício do quadro',
        title: 'Exercício do quadro',
        description: 'Dieta de custo mínimo por programação linear, com preços-sombra e cenários.',
        href: '/',
        icon: CalculatorIcon
      },
      {
        label: 'Vaca leiteira',
        title: 'Vaca leiteira (RuFaS)',
        description: 'Simulação com o RuFaS, padrão NRC 2001: ração, custo, leite e margem.',
        href: '/vaca',
        icon: MilkIcon
      },
      {
        label: 'Curva de lactação',
        title: 'Curva de lactação',
        description: 'Curva de Wood por paridade, com PEV, gestação e secagem.',
        href: '/curva',
        icon: TrendingUpIcon
      },
      {
        label: 'Sensibilidade',
        title: 'Sensibilidade (RuFaS)',
        description: 'Cenários de preços de alimentos e do leite, com o efeito de cada fator.',
        href: '/sensibilidade',
        icon: SlidersHorizontalIcon
      }
    ]
  },
  {
    label: 'Projeto',
    items: [
      {
        label: 'Premissas e limites',
        title: 'Premissas e limites',
        description: 'O que o modelo assume, o que ele não faz e como ler os resultados.',
        href: '/sobre',
        icon: InfoIcon
      }
    ]
  }
]

export const allNavLinks = navGroups.flatMap(g => g.items)

/** Remove a barra final (o export estático usa trailingSlash). */
export const normalizePath = (pathname: string) => (pathname.length > 1 ? pathname.replace(/\/+$/, '') : pathname)

export const findNav = (pathname: string) => allNavLinks.find(l => l.href === normalizePath(pathname))

import type { LpRationResult, ModuleComparison, ModuleOptimization, SensLpResult } from '@/lib/types'

import { nf, usd } from './format'

/** Diferença (em %) abaixo da qual os dois custos contam como iguais (a mesma do servidor: `tie_pct`). */
export const TIE_PCT = 0.1

export type ConclusionTone = 'tie' | 'good' | 'bad' | 'neutral'

/** Conclusão curta que aparece no topo dos resultados de uma comparação do LP com o RuFaS. */
export interface Conclusion {
  tone: ConclusionTone
  title: string
  text: string
}

/** Conclusão e avisos de uma comparação; os avisos dizem quando o resultado diz pouco ou quando algo ficou fora. */
export interface Verdict {
  conclusion: Conclusion | null
  notices: string[]
}

const pct = (value: number, digits = 2) => `${nf(Math.abs(value), digits)}%`

/** Aba "Ração linear" da Vaca leiteira (FSD, A.14). */
export function cowVerdict(result: LpRationResult, milkLoss = 0): Verdict {
  const notices: string[] = []
  const { summary } = result
  const same = summary.lp_same
  const free = summary.lp_free

  if (milkLoss > 0) {
    notices.push(
      `Esta simulação perdeu leite (${nf(milkLoss, 2)} kg por vaca por dia): o RuFaS reduziu a produção porque a ração não atendia. A comparação usa as exigências já reduzidas.`
    )
  }

  if (summary.intervals_used < result.intervals.length) {
    const out = result.intervals.length - summary.intervals_used

    notices.push(`${out} de ${result.intervals.length} intervalos ${out === 1 ? 'ficou' : 'ficaram'} fora: o LP não achou ração viável ${out === 1 ? 'nele' : 'neles'}.`)
  }

  if (same && free && (!same.all_verified || !free.all_verified)) {
    notices.push('Alguma ração do LP não atendeu a uma restrição original do RuFaS: confira a coluna "Restrições do RuFaS" da tabela.')
  }

  if (!same || !free || summary.intervals_used === 0) return { conclusion: null, notices }

  const s = same.saving_pct
  const herd = `US$ ${nf(Math.abs(same.herd_saving), 0)} no rebanho, em ${nf(summary.days, 0)} dias`

  if (Math.abs(s) <= TIE_PCT) {
    return {
      notices,
      conclusion: {
        tone: 'tie',
        title: 'empate',
        text: `Com o mesmo consumo, a ração linear custou ${pct(s, 3)} ${s >= 0 ? 'menos' : 'mais'} que a do RuFaS (${herd}). O otimizador do RuFaS já chega perto do ótimo da ração; o método linear dá o mesmo custo, com uma resposta que não depende do ponto inicial aleatório.`
      }
    }
  }

  if (s > 0) {
    return {
      notices,
      conclusion: {
        tone: 'good',
        title: 'o método linear foi mais barato',
        text: `Com o mesmo consumo, a ração linear custou ${pct(s)} menos que a do RuFaS (${herd}); com o consumo livre, ${pct(free.saving_pct)} ${free.saving_pct >= 0 ? 'menos' : 'mais'}. O SLSQP do RuFaS parou acima do ótimo em alguns intervalos.`
      }
    }
  }

  return {
    notices,
    conclusion: {
      tone: 'bad',
      title: 'o RuFaS foi mais barato',
      text: `A ração linear custou ${pct(s)} mais que a do RuFaS com o mesmo consumo. A busca do LP é heurística e pode parar um pouco acima do ótimo; neste cenário o RuFaS levou vantagem.`
    }
  }
}

/** Aba "Ração linear" da Sensibilidade (FSD, A.15). */
export function sensVerdict(result: SensLpResult): Verdict {
  const notices: string[] = []
  const { summary } = result
  const compared = result.rows.filter(row => row.intervals_used)

  if (summary.failed > 0) {
    notices.push(`${summary.failed} simulação(ões) do RuFaS falharam e ficaram fora da comparação.`)
  }

  if (compared.length > 0 && !summary.all_verified) {
    notices.push('Alguma ração do LP não atendeu a uma restrição original do RuFaS: confira a tabela.')
  }

  if (compared.length === 0) return { conclusion: null, notices }

  // Quantos custos diferentes o RuFaS teve: se os fatores não mudam a ração, todas as simulações custam o mesmo.
  const distinct = new Set(compared.map(row => (row.slsqp_cost ?? 0).toFixed(4))).size

  if (compared.length > 1 && distinct === 1) {
    notices.unshift(
      `Os fatores escolhidos não mudaram a ração: as ${compared.length} simulações têm o mesmo custo (${usd(compared[0].slsqp_cost, 3)} por vaca por dia). Os alimentos variados provavelmente não entram na ração, então a comparação vale por uma só. Varie preços de alimentos que a ração usa.`
    )

    return {
      notices,
      conclusion: {
        tone: 'neutral',
        title: 'sem informação nova',
        text: 'O RuFaS e o método linear deram a mesma ração em todas as simulações, mas como a ração não mudou com os preços, isso equivale a um único caso. Para testar se o empate se mantém quando os preços mudam, varie alimentos que a ração realmente usa.'
      }
    }
  }

  if (compared.length > 2 && distinct < compared.length / 2) {
    notices.push(
      `Só ${distinct} custos diferentes em ${compared.length} simulações: parte dos fatores não altera a ração, e a comparação tem menos casos distintos do que parece.`
    )
  }

  const best = -summary.min_diff_pct // economia do LP no melhor caso
  const worst = summary.max_diff_pct // quanto o LP custou a mais no pior caso
  const n = summary.compared

  if (summary.lp_cheaper === 0 && summary.lp_dearer === 0) {
    return {
      notices,
      conclusion: {
        tone: 'tie',
        title: 'empate',
        text: `Em todas as ${n} simulações o método linear ficou a menos de ${nf(summary.tie_pct, 1)}% do RuFaS (diferença média de ${pct(summary.mean_diff_pct, 3)}). Mesmo com os preços mudando, o RuFaS já chega perto do ótimo da ração e o método linear o reproduz.`
      }
    }
  }

  if (summary.lp_dearer === 0) {
    return {
      notices,
      conclusion: {
        tone: 'good',
        title: 'o método linear nunca foi pior',
        text: `O linear nunca custou mais que ${pct(Math.max(worst, 0), 3)} além do RuFaS e custou menos em ${summary.lp_cheaper} de ${n} simulações (até ${pct(best)}); nas outras ${summary.tie} empatou. É um ganho pequeno, onde o SLSQP do RuFaS parou acima do ótimo.`
      }
    }
  }

  if (summary.lp_cheaper === 0) {
    return {
      notices,
      conclusion: {
        tone: 'bad',
        title: 'o RuFaS foi mais barato',
        text: `Em ${summary.lp_dearer} de ${n} simulações o método linear custou mais que o RuFaS (até ${pct(worst)}). A busca do LP é heurística: aumente a resolução da busca ou compare de novo.`
      }
    }
  }

  return {
    notices,
    conclusion: {
      tone: 'neutral',
      title: 'resultado misto',
      text: `O método linear custou menos em ${summary.lp_cheaper} simulações (até ${pct(best)}) e mais em ${summary.lp_dearer} (até ${pct(worst)}); ${summary.tie} empataram. Em média, ${nf(Math.abs(summary.mean_diff_pct), 3)}% ${summary.mean_diff_pct <= 0 ? 'a favor' : 'contra'} do método linear.`
    }
  }
}

/** Cartão "Dieta ótima" do Ruminante Singular: o LP contra o SLSQP do RuFaS em várias sementes (FSD, B.11). */
export function optimalVerdict(result: ModuleOptimization): Verdict {
  const notices: string[] = []
  const diet = result.diet
  const rufas = result.rufas

  if (!diet) return { conclusion: null, notices }

  if (!rufas) {
    notices.push('Nenhuma execução do RuFaS foi pedida (0 sementes): não há o que comparar. Aumente o número de execuções do RuFaS para comparar o LP com o SLSQP.')

    return { conclusion: null, notices }
  }

  if (rufas.cost_min == null) {
    notices.push(`Nenhuma das ${rufas.n_runs} execuções do RuFaS ficou viável: o SLSQP não achou dieta, e a comparação de custo não existe.`)

    return {
      notices,
      conclusion: {
        tone: 'good',
        title: 'só o método linear achou dieta',
        text: 'O LP achou uma dieta que atende às restrições originais do RuFaS; o SLSQP, nas sementes testadas, não convergiu para nenhuma viável.'
      }
    }
  }

  if (rufas.n_success < rufas.n_runs) {
    notices.push(
      `${rufas.n_runs - rufas.n_success} de ${rufas.n_runs} execuções do RuFaS não ficaram viáveis: o SLSQP depende do ponto inicial aleatório.`
    )
  }

  if (!diet.verified) {
    notices.push('A dieta do LP viola uma restrição original do RuFaS por uma diferença numérica: confira o selo acima.')
  }

  const gap = rufas.lp_gap_pct ?? 0
  const spread = diet.cost > 0 && rufas.cost_max != null ? ((rufas.cost_max - diet.cost) / diet.cost) * 100 : 0
  const spreadText =
    spread > TIE_PCT ? ` A pior execução do RuFaS custou ${pct(spread)} além do LP: o SLSQP depende do ponto inicial, o LP não.` : ''

  if (Math.abs(gap) <= TIE_PCT) {
    return {
      notices,
      conclusion: {
        tone: 'tie',
        title: 'empate',
        text: `O LP e o melhor SLSQP do RuFaS chegaram ao mesmo custo (diferença de ${pct(gap, 3)}).${spreadText}`
      }
    }
  }

  if (gap < 0) {
    return {
      notices,
      conclusion: {
        tone: 'good',
        title: 'o método linear foi mais barato',
        text: `O LP custou ${pct(gap)} menos que a melhor das ${rufas.n_runs} execuções do RuFaS: o SLSQP parou em um ótimo local.${spreadText}`
      }
    }
  }

  return {
    notices,
    conclusion: {
      tone: 'bad',
      title: 'o RuFaS achou custo menor',
      text: `A melhor execução do RuFaS custou ${pct(gap)} menos que o LP. A busca do LP é heurística: aumente a resolução (rápida, normal ou fina) para aproximá-la do ótimo.${spreadText}`
    }
  }
}

/** Aba "Linearização": as restrições lineares contra as originais do RuFaS (FSD, B.8). */
export function linearizationVerdict(report: ModuleComparison): Verdict {
  const notices: string[] = []
  const s = report.summary

  if (!s.identity_ok) {
    notices.push('A oferta linear não coincide com a do RuFaS no ponto da dieta. Isso indica um defeito no modelo, não só a aproximação fora do ponto.')
  }

  if (!s.same_state_in_probes) {
    notices.push('Em alguma sonda de ±5% uma restrição é viável em um modelo e violada no outro.')
  }

  if (s.n_compared === 0) return { conclusion: null, notices }

  if (s.identity_ok && s.n_above_tolerance === 0) {
    return {
      notices,
      conclusion: {
        tone: 'tie',
        title: 'a linearização reproduz o RuFaS',
        text: `No ponto da dieta a oferta linear é igual à do RuFaS e, com as quantidades de −5% a +5%, o maior erro é de ${nf(s.max_error_pct, 2)}%, dentro da tolerância de ${nf(report.tolerance_pct, 2)}%.`
      }
    }
  }

  return {
    notices,
    conclusion: {
      tone: s.identity_ok ? 'neutral' : 'bad',
      title: s.identity_ok ? 'linearização aproximada fora do ponto' : 'a linearização diverge do RuFaS',
      text: `${s.n_above_tolerance} de ${s.n_compared} restrições passaram da tolerância de ${nf(report.tolerance_pct, 2)}% (em ${s.n_diets_above_tolerance} de ${s.n_diets} dietas); o maior erro é ${nf(s.max_error_pct, 2)}%${s.worst ? ` (${s.worst.diet}: ${s.worst.label})` : ''}. A linearização é exata no ponto e o erro cresce com a distância dele.`
    }
  }
}

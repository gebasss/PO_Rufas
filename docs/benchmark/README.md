# Benchmark LP × SLSQP do RuFaS (v3)

Pergunta: **o custo mínimo que o LP acha é equivalente ao melhor custo que o SLSQP do RuFaS acha?**
O LP é o método de parametrização da dieta ótima (`docs/CONCLUSOES_PREVIAS.txt`, seção 7); o SLSQP é o otimizador não linear do próprio RuFaS, que parte de um ponto inicial aleatório.

## Pastas

| Caminho | O que é |
|---|---|
| `v3/RELATORIO.txt` | O relatório legível (comece por aqui). |
| `v3/resumo.json` | As mesmas medidas, em formato de máquina. |
| `v3/resultados.jsonl` | Um caso por linha (custo do LP, custo e estado de cada semente do SLSQP, tempos). |
| `historico/v1`, `historico/v2` | Desenhos anteriores, guardados só para rastrear a história (ver abaixo). Não são mais produzidos. |

## Desenho do v3 (definido antes de rodar)

- **Padrão:** NASEM 2021, o único que as telas usam. O metano entérico e o nitrogênio urinário são calculados da dieta.
- **Caso:** animal × cardápio × conjunto de preços. Cada caso chama `optimize_diet` (a mesma rota da tela Dieta ótima), com o LP na resolução normal e 10 sementes do SLSQP. O animal é avaliado em **um dia**: não é uma simulação completa (essa comparação está na aba Ração linear da Vaca leiteira).
- **288 casos:** 8 animais (4 vacas em lactação, vaca seca, novilha pré-parto e 2 novilhas em crescimento) × 3 cardápios (5, 7 e 12 alimentos) × 12 conjuntos de preços (o base e 11 sorteados, de 0,5× a 2× o base, semente fixa). Os preços são ilustrativos.
- **Diferença do caso:** (custo do LP − melhor custo do SLSQP) / melhor custo do SLSQP, em %. Negativa = o LP é mais barato. O SLSQP só conta se convergiu e atende às restrições originais.
- **Critério de equivalência (margem ±0,5%):** o IC de 90% da diferença média cabe na margem **e** ao menos 95% dos casos ficam dentro dela. O IC é um bootstrap por agrupamento (reamostra os grupos animal × cardápio, que compartilham exigências e alimentos).
- **Empate:** diferença de até 0,1% (a mesma da interface).
- **Casos sem solução:** quando o LP não acha dieta, o SLSQP é rodado também; o relatório diz se ele concorda.
- **Regra contra remendos:** o desenho acima não muda depois de ver os resultados. Se aparecer um defeito, ele é corrigido e o benchmark é repetido com outra semente de preços (`--price-seed`), para a correção não ser ajustada aos casos já vistos.

## Reprodução

```powershell
cd backend
..\.venv\Scripts\python -m dietopt.benchmark run --out ..\docs\benchmark\v3     # retoma o que já foi feito
..\.venv\Scripts\python -m dietopt.benchmark report --out ..\docs\benchmark\v3  # só refaz o resumo e o relatório
```

## O que aconteceu antes (`historico/`)

- **v1** (72 casos, NASEM e NRC): fixava metano e nitrogênio urinário em valores de teste; achou um defeito na busca do LP (até +1,77% no NASEM), corrigido depois. As pastas guardam os resultados antes da correção e a validação com preços novos.
- **v2** (72 casos): metano e nitrogênio calculados da dieta; 4 vacas, 1 cardápio, dois padrões.
- O v3 recomeça do zero: só NASEM, mais animais e cardápios, um critério único e um único diretório de saída.

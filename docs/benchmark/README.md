# Benchmark LP × SLSQP do RuFaS (v4)

Pergunta: **para o mesmo problema, o custo mínimo que o LP acha é equivalente ao melhor custo que o SLSQP do RuFaS acha?**
O LP é o método de parametrização da dieta ótima (`docs/CONCLUSOES_PREVIAS.txt`, seção 7); o SLSQP é o otimizador não linear do próprio RuFaS, que parte de um ponto inicial aleatório.

## Pastas

| Caminho | O que é |
|---|---|
| `v4/RELATORIO.txt` | O relatório legível (comece por aqui). |
| `v4/resumo.json` | As mesmas medidas, em formato de máquina, com o commit e as versões. |
| `v4/resultados.csv` | Um caso por linha (custos, diferenças, tempos, emissões). |
| `v4/execucoes_slsqp.csv` | Uma execução do SLSQP por linha (semente, estado, custo, tempo). |
| `v4/resultados.jsonl` | Os dados brutos completos, de onde o resto é gerado (e de onde a execução retoma). |
| `RELATORIO_UMA_PAGINA.pdf` / `.png` | O relatório de uma página para a apresentação (3 gráficos e o que dá e não dá para dizer), com os dados do v4 e de `simulacao/`. Gerado por `python -m dietopt.benchmark_report` (pasta `backend`). |
| `simulacao/` | A camada de simulações completas (`RELATORIO.txt`, `resumo.json`, `resultados.csv`, `intervalos.csv`, `resultados.jsonl`, `execucao.log`); ver a última seção. |
| `historico/v1`, `v2`, `v3`, `simulacao-v1` | Desenhos anteriores, guardados só para rastrear a história (ver abaixo). Não são mais produzidos. |

## Desenho do v4 (definido antes de rodar)

- **Padrão:** NASEM 2021, o único que as telas usam.
- **Caso:** animal × cardápio × conjunto de preços. Cada caso chama `optimize_diet` (a mesma rota da tela Dieta ótima) com o LP na resolução normal e 10 sementes do SLSQP. O animal é avaliado em **um dia**: não é uma simulação completa, por isso o tamanho do rebanho não entra (ele só importa na simulação completa).
- **288 casos:** 8 animais (4 vacas em lactação, vaca seca, novilha pré-parto e 2 novilhas em crescimento) × 12 cardápios × 3 conjuntos de preços.
- **Cardápios sorteados** (semente fixa), não escolhidos à mão: de um conjunto de 21 alimentos com preço (os 18 da biblioteca NASEM com preço padrão e três acrescentados: feno de leguminosa, casca de soja e fosfato bicálcico), cada cardápio tem 2 a 3 volumosos, 3 a 6 concentrados e 1 a 2 minerais.
- **Preços:** o primeiro conjunto de cada cardápio usa os preços padrão; os outros 2 multiplicam cada preço por um fator uniforme de 0,5 a 1,5. São ilustrativos, não cotações.
- **O mesmo problema para os dois métodos.** O SLSQP do RuFaS só aceita metano entérico e nitrogênio urinário como constantes; o módulo os calcula da própria dieta. Por isso cada caso tem dois LPs: o do módulo (emissões da própria dieta) e o **LP nas mesmas constantes** do SLSQP.
- **Comparação primária:** LP nas mesmas constantes contra o melhor SLSQP (o mesmo problema: a diferença é só do método de busca). O SLSQP só conta se convergiu e atende às restrições originais.
- **Secundárias:** (1) o LP do módulo contra o melhor SLSQP que também respeita a energia com as emissões da própria dieta (o produto como o usuário o vê); (2) o custo de usar emissões consistentes (LP do módulo contra LP nas mesmas constantes).
- **Diferença do caso:** (custo do LP − melhor custo do SLSQP) / melhor custo do SLSQP, em %. Negativa = o LP é mais barato. Empate = até 0,1% (a mesma da interface).
- **Critério de equivalência (margem ±0,5%):** o IC de 90% da diferença média cabe na margem **e** ao menos 95% dos casos ficam dentro dela. O IC é um bootstrap por agrupamento (reamostra os grupos animal × cardápio, que compartilham exigências e alimentos). O Wilcoxon, sobre a média de cada grupo, diz se uma pequena vantagem é sistemática.
- **Casos sem solução:** quando o LP não acha dieta, o SLSQP é rodado também; o relatório diz se ele concorda.
- **Versões:** o resumo registra o commit, a versão do RuFaS e as do Python, numpy e scipy.
- **Regra contra remendos:** o desenho acima não muda depois de ver os resultados. Se aparecer um defeito, ele é corrigido e o benchmark é repetido com outra semente (`--seed`), para a correção não ser ajustada aos casos já vistos.

## Reprodução

```powershell
cd backend
..\.venv\Scripts\python -m dietopt.benchmark run --out ..\docs\benchmark\v4     # retoma o que já foi feito (cerca de 1 h 30 min)
..\.venv\Scripts\python -m dietopt.benchmark report --out ..\docs\benchmark\v4  # só refaz o resumo, os CSVs e o relatório
```

## O que aconteceu antes (`historico/`)

- **v1** (72 casos, NASEM e NRC): fixava metano e nitrogênio em valores de teste; achou um defeito na busca do LP (até +1,77% no NASEM), corrigido depois.
- **v2** (72 casos): metano e nitrogênio calculados da dieta; 4 vacas, 1 cardápio, dois padrões.
- **v3** (288 casos, só NASEM): 8 animais, 3 cardápios escolhidos à mão. Mostrou 6 casos fora da margem; a investigação (`CONCLUSOES_PREVIAS.txt`, 5.8) achou que 4 eram diferença de problema (as constantes do SLSQP). O v4 resolve isso e sorteia os cardápios.

## Camada de simulações completas (`simulacao/`)

Pergunta: **o que o v4 mede em um animal e um dia vale dentro de uma simulação de 1 ano do RuFaS, com o SLSQP formulando a ração a cada intervalo?**

- **Unidade:** uma simulação de 1 ano (rebanho em lactação, 13 intervalos de 30 dias). Os intervalos são medidas repetidas dentro dela (só descritos).
- **Desenho:** 20 cardápios × 2 conjuntos de preços (o padrão e um sorteado) = 40 simulações; o tamanho do rebanho (60, 100, 200 ou 300 vacas) e a semente do RuFaS são sorteados por cardápio.
- **Comparação:** o SLSQP roda uma vez por intervalo, dentro do RuFaS. O LP é resolvido depois, em cada intervalo, sobre as mesmas exigências, alimentos, preços, limites e emissões do lote. A ração do LP **não volta** para o RuFaS: a camada mede o custo da ração, não o efeito sobre o leite.
- **Primária:** LP de consumo livre contra o SLSQP. **Secundária:** LP com o consumo do SLSQP. **Critério:** o mesmo do v4 (IC de 90% por cardápio dentro de ±0,5% e ao menos 95% das simulações dentro da margem).
- **Resultado (semente 20261203):** 30 de 40 simulações comparadas (10 falharam dentro do RuFaS, 8 delas com 60 vacas); diferença média −0,005% (IC de 90% de −0,074% a +0,069%); 93,3% dentro da margem, abaixo dos 95%: **equivalência não demonstrada** pelo critério (a média e o IC cabem na margem). Leitura e limites em `docs/CONCLUSOES_PREVIAS.txt`, seção 8.
- **Defeito corrigido antes:** no dia 0 o RuFaS formula com metano e nitrogênio urinário zero; a primeira rodada (`historico/simulacao-v1`, semente 20261202) usava os valores do dia 0 e foi descartada. A camada foi repetida com outra semente.

```powershell
cd backend
..\.venv\Scripts\python -m dietopt.benchmark_sim run --out ..\docs\benchmark\simulacao     # retoma o que já foi feito (cerca de 75 min)
..\.venv\Scripts\python -m dietopt.benchmark_sim report --out ..\docs\benchmark\simulacao  # só refaz o resumo, os CSVs e o relatório
```

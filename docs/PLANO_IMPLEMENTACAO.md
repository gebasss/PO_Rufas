# Plano de implementação: módulo "Exercício do quadro" ampliado e complementos

**Versão 0.18 (11/11/2026).** Este plano ordena o que será codificado depois da fase de documentação. Ele não altera o
comportamento do sistema; as regras estão nos documentos citados e este arquivo só as sequencia.

| Documento | O que fornece ao plano |
|---|---|
| `PRD.md` (RF-13, 19 a 24, 26 a 30) | O que falta atender e a prioridade (M/S/C) |
| `FSD.md`, Anexo A (RF-24, RF-26, RF-27) e Anexo B (RF-28 a RF-30) | Telas, campos, rotas, critérios de aceite |
| `LINEARIZACAO.md` | Fórmulas, técnica de linearização, tolerâncias, estudo numérico |
| `PERGUNTAS_PROFESSOR.md` | Decisões que dependem do professor (P1 a P21) |
| `DECISOES_TECNICAS.md` | Stack, ambientes, restrições (RuFaS intocado, GPLv3, Windows, OneDrive) |

---

## Andamento

| Etapa | Situação | Observações |
|---|---|---|
| E0 | Em aberto | Valem as propostas registradas; perguntas ao professor em `PERGUNTAS_PROFESSOR.md` |
| E1 | **Feita no back-end (02/11/2026)** | `standards.py`, `paths.py`; `Scenario.nutrient_standard` grava a biblioteca do padrão (com limites) e o `metadata`; preços restritos à biblioteca; `GET /api/feeds?standard=`; falta o seletor na interface (FSD A.3.1) |
| E2 | **Feita (02/11/2026)** | `module/` (`categories`, `fields`, `requirements`, `api`); `GET /api/module/defaults`, `POST /api/module/requirements`; padrão do módulo é NASEM |
| E3 | **Feita (02/11/2026)** | `module/linear.py` (classes L, E e A, em NRC e NASEM, todas as categorias), `module/evaluate.py` (oferta linear × `RationOptimizer`, erro fora do ponto, estados, violação, ordenação), `module/library.py`, `module/rufas.py`; `POST /api/module/evaluate`; 71 testes passando, e a sabotagem de coeficientes confirmou que os testes falham quando algo está errado |
| E4 | **Feita (03/11/2026)** | Rota feita junto com a E3; formatos conferidos com a interface (E5) |
| E5 | **Feita (03/11/2026)** | Tela 1 com o seletor "Exercício simples" × "Avaliar dietas (vaca real)" (o seletor e o exercício simples foram retirados em 11/11/2026, etapa R1) e os cartões Vaca, Dietas, Preços e limites e Resultado (`ExerciseView`, `ModuleView`, `views/module/`); build em `frontend/` por `scripts\build-web.ps1`; conferida no navegador (NASEM e NRC, categoria de crescimento, painel de ≈ 800 px e tela de 375 px, sem rolagem horizontal da página). **Fica de fora:** o seletor de padrão da simulação (FSD A.3.1) e a persistência em `localStorage` |
| E6 | **Feita (03/11/2026)** | `module/compare.py` (relatório sobre o resultado de `evaluate`, CSV), `POST /api/module/compare`, cartão "Comparação com o RuFaS" na tela (`CompareCard`) com tolerância editável e botão de CSV; 13 testes novos (84 no total) |
| E7 | **Feita (03/11/2026)** | `module/optimize.py` (LP por ponto da grade de escalares, refinamento, resgate, preços-sombra, verificação com as funções do RuFaS, SLSQP em várias sementes), tarefa `optimize` com cancelamento (`jobs.py`: estado `cancelled`, `POST /api/jobs/<id>/cancel`), cartão "Dieta ótima" e coluna "Desvio do ótimo" no ranking; 31 testes novos (115 no total, ≈ 80 s) |
| E8a, E8b | **Feitas (03/11/2026)** | RF-27 (`ration_checks.py`, cartão Verificações) e RF-19 (`ration_balance.py`, cartão Balanço nutricional), na tela Vaca leiteira; o balanço vem da avaliação do próprio RuFaS (`avg_eval_results_for_LAC_COW`); 17 testes novos (132 no total) |
| E8d | **Feita (03/11/2026)** | RF-22: `prices.py`, `POST /api/prices/import`, componente `PriceImport` nas telas Vaca leiteira e Avaliar dietas; 19 testes novos (151 no total) |
| E8e | **Feita (03/11/2026)** | RF-20: `exports.py` (CSV e relatório HTML), `POST /api/export/<csv\|report>/<tela>`, `ExportButtons` nas quatro telas; 8 testes novos (159 no total) |
| E8f | **Feita (03/11/2026)** | RF-21: `scenario_files.py`, `POST /api/scenario/save` e `/load`, `ScenarioFile` nas telas Vaca leiteira e Avaliar dietas; 29 testes novos (188 no total) |
| E8g | **Feita (10/11/2026)** | RF-13: `herd.py` (escala o rebanho e as baias, valida 60 a 500), campo "Vacas no rebanho" na tela Vaca leiteira com aviso de tempo e memória, estimativa da sensibilidade, arquivo de cenário, histórico, relatório e comparação com o base só entre rebanhos do mesmo tamanho; 26 testes novos (223 no total); limites medidos com simulações reais; ver `FSD.md`, A.13 |
| E8c, E8h | Não iniciadas | |
| R1 | **Feita (11/11/2026)** | Retirada do **Exercício simples** (PL de arroz e milho com tabela de cenários) da tela Exercício do quadro, a pedido do usuário: `ToyView`, `diet_lp.py`, rotas `/api/toy*`, exportação `toy`, estado do quadro no `AppProvider` e `HeatMap` saíram; a tela é só a avaliação de dietas; testes 223 → 219; documentos atualizados (RF-01 a RF-04 e RF-23 retirados) |
| D6 | **Feita (03/11/2026)** | Repaginação da Curva de lactação (marcas do ciclo, KPIs por paridade, produção acumulada) e do exercício simples (retirado depois, em R1); "ver como tabela" em todos os gráficos; ver `DESIGN_REPAGINACAO.md`, seção 12 |
| D5 | **Feita (03/11/2026)** | Repaginação da tela Avaliar dietas: entradas em abas, barra de execução com `RunButton`, resultados em abas (ranking, restrições, linearização, dieta ótima), custo por dieta, mapa de restrições, folga, erro de linearização com a tolerância, composição do LP × RuFaS e custo por semente; ver `DESIGN_REPAGINACAO.md`, seção 11 |
| D4 | **Feita (03/11/2026)** | Repaginação da tela Sensibilidade: painel fixo com `RunButton`, resultados em abas (visão geral, fatores, cenários), margem por cenário com linha da simulação-base, histograma das margens, tornado dos fatores, dispersão margem × fator e ração do cenário ótimo; ver `DESIGN_REPAGINACAO.md`, seção 10 |
| D3 | **Feita (03/11/2026)** | Histórico de execuções: `history.py` (arquivos em `runs/_history`, base por tipo, retenção), rotas `/api/history`, tarefas e avaliação de dietas gravam a execução (`run_id`), tela Execuções com detalhe, duplicar e exportar, deltas dos KPIs da Vaca leiteira; 9 testes novos; ver `FSD.md`, A.12 |
| D2 | **Feita (03/11/2026)** | Repaginação da tela Vaca leiteira: painel fixo, `RunButton` com quatro estados, resultados em abas (visão geral, ração, nutrição), gráficos de ração, balanço, leite e custo, verificações com faixa e a alternância gráfico/tabela; ver `DESIGN_REPAGINACAO.md`, seção 8 |
| D1 | **Feita (03/11/2026)** | Repaginação, etapa 1 (tokens, barra superior em pílula, sidebar flutuante, paleta de comandos, menu Tarefas, KPIs com tendência e barras com destaque). O roteiro D2 a D6 (telas, histórico de execuções e gráficos) está em `DESIGN_REPAGINACAO.md`; a E8g fica depois |

Achados do E8f: (i) o arquivo guarda só entradas e é validado na ida e na volta pelo servidor, então um arquivo salvo sempre abre e um
arquivo feito à mão é conferido; (ii) a configuração da sensibilidade era estado local da tela e se perdia ao trocar de página:
foi para a memória da página (`AppProvider`) e entra no cenário da vaca; (iii) o formato é versionado desde a versão 1, com a
tabela de migrações pronta e arquivos de versão mais nova recusados; (iv) alimentos que a biblioteca do padrão não tem saem com
aviso em vez de derrubar o arquivo.

Achados do E8e: (i) o servidor monta os arquivos a partir do JSON que a tela já tem, o que os deixa testáveis sem navegador e sem
gravar nada em disco; (ii) a simulação não devolvia os limites por alimento e passou a devolvê-los (`limits`) para o relatório;
(iii) o HTML do relatório escapa observação e nomes (teste com `<script>`); (iv) o CSV leva BOM para o Excel e usa ponto decimal,
enquanto o relatório usa o formato brasileiro.

Achados do E8d: (i) os nomes da biblioteca têm vírgulas ("Corn, Yellow") e o mesmo nome curto serve a dezenas de alimentos, então o
mapeamento seguro é por id do RuFaS; o nome só vale inteiro ("nome — descrição") e vem entre aspas no CSV; (ii) o preço de um
alimento fora da seleção não é aplicado nem o alimento é adicionado, e a tela o lista; (iii) a tela Vaca leiteira já guardava a
seleção no navegador (`dietopt.v1`), então os preços importados persistem ali.

Achados do E8a e E8b: (i) o RuFaS já calcula o balanço da ração (`NutritionEvaluator`); bastou incluir `avg_eval_results_for_LAC_COW` no
filtro de saída e a simulação guardada antes disso roda de novo (cache sem `evaluations` é descartado); (ii) a saída de exigências
do RuFaS tem todas as parcelas de energia, então o balanço mostra oferta = exigência + diferença sem recalcular nada; (iii) a
proteína e o consumo só chegam como "dentro da faixa" ou a distância até o limite; (iv) a FDN sai do RuFaS com 45,0000006%, o
que exige tolerância nas verificações; (v) na simulação real do "Conjunto base" em NRC: V1 alerta (+29,5%), V2 atenção (45,0%) e
balanço sem déficit (cálcio 345% acima da exigência).

Achados do E7: (i) a formulação foi validada pelo ponto exato: nos escalares do melhor SLSQP o LP reproduz o custo (erro relativo
< 1e-6) em NRC e NASEM, para lactação, vaca seca e novilha; (ii) no caso-base do NRC o LP fica 0,008% acima do melhor do RuFaS
(3,8345 contra 3,8342, resolução normal, ≈ 18 s) e no NASEM empata (3,08318); critério de 0,1% atendido; (iii) a busca só por
grade e padrões travava (NASEM de lactação a +2,6%; NASEM de vaca seca e de novilha sem nenhum ponto viável da grade rápida):
entraram a descida guiada pelo LP com as quantidades livres e o resgate por ponto fixo dos escalares; (iv) o SLSQP do RuFaS
é instável: com seis alimentos, uma semente parou em 3,8595 e outra não convergiu; (v) a tolerância de viabilidade do RuFaS
é relativa de 1e-5 (a estrita de 1e-9 da avaliação marcava como violada uma execução que o SLSQP considera viável).
O laço de redução de leite (LINEARIZACAO 7.6) e a otimização por fase da lactação ficam para depois.

Achados do E6: (i) nas dietas de exemplo do NRC, o maior erro a ±5% é 0,30% ("Silagem e concentrado") e 0,60% ("Só volumoso"); a
dieta "Mais concentrado" (TDN 69,9%) chega a 1,86% (energia de crescimento) e 4 das 14 restrições passam de 1%; no NASEM (metano 400 g/dia e N urinário
0,2 kg/dia) o maior erro é 0,31% (PM) e nenhuma das 33 passa de 1%; (ii) a igualdade no ponto e o mesmo estado (viável ou
violada) nas sondagens conferem nos casos conferidos (NRC e NASEM, três dietas de exemplo); (iii) o erro de uma restrição de razão (classe E) não é sondado
escalando as quantidades, porque a razão não muda com a escala: a exatidão dela é verificada em dietas aleatórias (B.9-3).

Achados do E5: (i) a resposta de `POST /api/module/evaluate` omite `supply_linear`, `supply_nonlinear`, `error_pct` e `slack` nas
restrições `indisponivel` e traz um campo `note` com o que falta; a interface trata isso (tipos opcionais); (ii) o exemplo
do NASEM só mostra a energia depois que o metano e o N urinário são preenchidos (com 400 g/dia e 0,2 kg/dia, a oferta de
46,73 Mcal/dia coincide com a do RuFaS e o erro a ±5% é 0,27%); (iii) no NRC, o erro de energia da dieta "Mais concentrado"
(TDN 69,9%) chega a 1,74% e é destacado.

Achados do E3: (i) a oferta linear coincide com a do RuFaS no ponto em todas as restrições, nas seis combinações de padrão e
categoria; (ii) a energia do NASEM exige metano e nitrogênio urinário do lote (L-Q2), que viraram campos opcionais, com
restrição "indisponível" sem eles; (iii) o RuFaS passa a FDN da ração anterior como fração, o que muda o consumo estimado da
vaca seca (+19%) e da novilha (+7%) e a PM da vaca em lactação (−5%); (iv) o erro de linearização foi medido contra a oferta
original, não contra a exigência, porque a exigência de crescimento do NRC é pequena e inflava o número; (v) com desconto de
ingestão (`D` < 1) o erro a ±5% passa de 1% quando o TDN% sobe (até 4% a 77%), o que reforça a parametrização da fase 2.

Achados do E2: (i) a idade (`days_born`) é obrigatória só no NRC para novilhas; (ii) o intervalo entre partos vazio quebra a
calculadora para vacas de 1ª e 2ª paridade, então vale 0 (que o RuFaS trata como "sem ganho de peso") com aviso; (iii) os
campos da ração anterior (TDN, energia, temperatura, FDN) têm padrão do RuFaS, e o da FDN (0,3) é uma fração tratada como
porcentagem (`LINEARIZACAO.md`, 4.7); (iv) o teste com um servidor local achou o erro de (ii) que os testes unitários, já
com o intervalo preenchido, não pegaram: por isso há teste dedicado.

---

## 1. Objetivo e escopo

**Objetivo principal (pedido do professor):** o módulo "Exercício do quadro" passa a **avaliar e comparar dietas montadas**
para uma vaca real (categoria e fase), no padrão NASEM (principal) ou NRC (apoio), com **restrições lineares** e com o erro
de linearização medido contra as equações do RuFaS. Em seguida (fase 2), ele **sugere a dieta ótima** e a compara com o
otimizador do RuFaS (SLSQP).

| Fase | Requisitos | Entrega |
|---|---|---|
| **1** | RF-28, RF-29 | Avaliar e ordenar dietas; erro de linearização; comparação oferta linear × RuFaS |
| **2** | RF-30 | Dieta ótima por LP; comparação com o SLSQP do RuFaS |
| **Apoio** | RF-24 (núcleo), RF-26, RF-27 | Padrão NASEM, arroz em grão, painel de verificações |
| **Complementos** | RF-19, 20, 21, 22, 13, 23 | Balanço, exportação, salvar, importar preços, rebanho, mais nutrientes |

**Fora do escopo deste plano:** CI/CD, autenticação, auditoria, banco de dados (seguem como em `DECISOES_TECNICAS.md`);
conversão automática de moeda e leitura automática do CEPEA (LINEARIZACAO 7.2: depois); categoria bezerra e combinações sem
otimizador no RuFaS; qualquer alteração em `vendor/RuFaS`.

## 2. Princípios

1. **RuFaS intocado.** Só se importam funções do RuFaS (calculadoras de exigência e de oferta); nada é copiado nem editado.
2. **Replicar o RuFaS onde diverge do livro** (L-D5): amido total em kg na digestibilidade da FDN, oferta de proteína do NRC no
   modo NASEM, piso do desconto, descontinuidade em TDN% = 60, ponto inicial aleatório. Cada replicação gera aviso no resultado.
3. **Linearizar só nas variáveis de decisão** (`x_i`, kg MS/dia); as exigências são constantes calculadas.
4. **Cada restrição tem identidade verificável:** a oferta linearizada, no ponto de referência, é igual à oferta original do
   RuFaS (critério B.9-1). Sem isso, nenhuma comparação com o RuFaS vale.
5. **Testes não dependem de material protegido:** os vetores de teste são números calculados pelo RuFaS (tabela 5.3 de
   `LINEARIZACAO.md`), não trechos do livro; `docs/nasem2021_notas/` é local e **não** pode ser lido por testes nem pelo código.
6. **Entregas pequenas e independentes**, cada uma com seus testes e um critério de aceite do FSD; o fluxo atual (simulação,
   sensibilidade, curva) continua funcionando em toda etapa.
7. **Commit, push e PR só quando o dono pedir**; o dono faz o merge.

## 3. Ponto de partida (código atual)

| Peça | Arquivo | Uso no plano |
|---|---|---|
| Otimização linear do quadro (LP com `scipy.linprog`) | `backend/dietopt/module/optimize.py` | Solver da fase 2 (o `diet_lp.py` do exercício simples foi retirado em 11/11/2026) |
| Biblioteca de alimentos e presets | `backend/dietopt/feeds.py` | Passa a ser **por padrão** (NRC e NASEM) |
| Adaptador do RuFaS (cenário, execução, leitura) | `backend/dietopt/rufas_adapter.py`, `rufas_results.py` | Ganha o campo `standard`; escreve `NASEM_Comp` |
| Cenários, avaliação, cache | `backend/dietopt/scenarios.py` | **Corrigir** `with_defaults`: restringir preços aos ids da biblioteca do padrão |
| Tarefas em segundo plano | `backend/dietopt/jobs.py` | Fase 2 (otimização, > 20 s) roda como tarefa |
| Servidor HTTP e rotas | `backend/dietopt/server.py` | Novas rotas `/api/module/*` |
| Testes | `backend/tests/` (`pytest`) | Novos testes por etapa |
| Interface | `web/src/views/ExerciseView.tsx`, `ModuleView.tsx`, `web/src/lib/api.ts`, `types.ts` | Quatro cartões; build por `scripts\build-web.ps1` (o seletor de modo e o `ToyView` foram retirados em 11/11/2026) |

Já verificado (FSD A.7.1, B.10): o modo NASEM roda com as nossas listas; as calculadoras NRC e NASEM rodam isoladas para as
seis categorias; as saídas do modo NASEM têm os mesmos nomes. Falta exercitar o otimizador do RuFaS em vaca seca e novilha.

## 4. Estrutura proposta de código (nova)

```
backend/dietopt/module/
    standards.py        # padrão (NRC | NASEM), categorias aceitas, restrições por categoria (LINEARIZACAO 2 e 3.1)
    requirements.py     # envelope das calculadoras de exigência do RuFaS + sobrescritas + TDN% e afins (NRC)
    coefficients.py     # coeficientes por alimento no ponto x_d (D, taxas de passagem, ME, NEm/NEl/NEg, RDP, RUP, Ca, P)
    constraints.py      # restrições: classes L, E e A (4.1 a 4.6), em forma  a·x ≥ b  com rótulo e unidade
    evaluate.py         # avaliar uma dieta: oferta linear, oferta original, erro, folga, estado, violação V, custo
    ranking.py          # ordenação (7.4) e "melhor entre as informadas"
    compare.py          # relatório linear × RuFaS por restrição (fase 1)
    optimize.py         # fase 2: parametrização dos escalares globais (5.1b), LP por ponto e por ramo
backend/tests/test_module_*.py   # um arquivo de teste por módulo acima (a pasta de testes é plana)
web/src/views/ModuleView.tsx  (+ componentes: CowCard, DietsCard, PricesCard, ResultCard)
docs/…                  # atualizar FSD (seções "implementado"), PRD (status) e README ao fim de cada etapa
```

O pacote `module` importa o RuFaS **de forma tardia** (dentro das funções), para o servidor subir rápido e para que os
testes de lógica pura rodem sem o RuFaS.

## 5. Etapas

Legenda de tamanho: **P** (pequeno, até meio dia), **M** (um a dois dias), **G** (mais de dois dias). São ordens de grandeza
para sequenciar, não prazos.

### E0. Fechar decisões que travam o código (antes de começar)

Nada aqui exige o professor para **iniciar**: cada item tem proposta registrada, usada como padrão se não houver resposta.

| Decisão | Onde | Bloqueia | Se sem resposta |
|---|---|---|---|
| Tolerância de erro de linearização (L-Q1) | LINEARIZACAO 6 e 8 | E3 | ≤ 1% da exigência para ±5% |
| Metano e N urinário do lote para vaca isolada (L-Q2) | LINEARIZACAO 7.3 | E3 (NASEM, energia) | Estimar pelo NASEM e congelar |
| Critério de ordenação das dietas (L-Q5) | LINEARIZACAO 7.4 | E3 | Inviáveis por `V`; viáveis por custo |
| Limite de +30% do consumo é intencional? (Q10) | PRD 15 | E3, E7 | Replicar o RuFaS e avisar |
| Descontinuidade em TDN% = 60 e piso do desconto (L-Q8, P21) | LINEARIZACAO 4.4 | E3, E7 | Replicar; dois regimes |
| Oferta de proteína do NRC no modo NASEM (L-Q6) | LINEARIZACAO 4.6 | E3 | Replicar e avisar |
| Mapeamento CEPEA × biblioteca; arroz em grão (L-Q3, Q9) | LINEARIZACAO 7.2 | E8 | Preço digitado ou CSV com id do RuFaS |

Saída: lista "decisões assumidas" no início de `module/standards.py` e no relatório de cada avaliação.

### E1. Padrão nutricional na base (RF-24, núcleo) — **M**

1. `Scenario` ganha `standard` (`"NRC"` por padrão); a chave do cache já o inclui.
2. Bibliotecas de alimentos por padrão; a troca de ids 301→230 e 302→167 só vale para NRC.
3. **Correção:** restringir os preços aos ids da biblioteca do padrão (o id 166 não existe no NASEM); gravar limites
   (`lower_limit`, `limit`) na cópia do CSV NASEM e apontar `NASEM_Comp` no `metadata.json`.
4. Leitor de saídas inalterado (mesmas 13 variáveis); rótulo de energia conforme o padrão.
5. Rotas `/api/jobs/simulate` e `/api/jobs/sensitivity` aceitam `standard`.

Aceite: FSD A.3.4 (critérios 1 e 2): "Conjunto base" em NASEM roda e exibe os seis indicadores; em NRC os resultados são
iguais aos da seção 15.4. Testes: construção do cenário NASEM (sem rodar o RuFaS inteiro), cache separado por padrão.

### E2. Calculadoras de exigência (envelope) — **M**

1. `requirements.py`: chama `calculate_requirements` (NRC e NASEM) sem simulação, com os campos de FSD B.3, a unidade correta
   do ganho diário (**kg/dia**) e os campos exclusivos do NRC (TDN%, temperatura anterior, energia líquida da dieta).
2. Sobrescritas das exigências pelo usuário; validação de faixas; erro claro para campo faltante da categoria.
3. `GET /api/module/defaults` (FSD B.7): campos por categoria e restrições aplicáveis.

Aceite: B.9-5 (categorias: novilha e vaca seca no NRC sem `NE_total` e `NE_lactation`); valores iguais aos das tabelas de
sondagem de 01/11/2026 (vaca em lactação, NRC e NASEM). Testes puros e com o RuFaS importado.

### E3. Núcleo linear e avaliação de dietas (RF-28, RF-29, fase 1) — **G** (caminho crítico)

Ordem interna, do mais simples ao mais difícil, cada passo com testes antes do seguinte:

1. **Classe L** (custo, limites, consumo, Ca, P) e **classe E** (FDN, FDN de forragem, gordura como `Σx(a−c) ≥ 0`).
2. **Proteína metabolizável** (classe A, com `min` em duas restrições): taxas de passagem, RDP, RUP, microbiana mínima.
3. **Energia NRC** (desconto `D(x)`, NEm/NEl/NEg por polinômio, disjunção `max`): coeficientes congelados em `x_d`.
4. **Energia NASEM** (digestibilidade da FDN com amido em kg, replicada) e fibra da Tabela 5-1 como verificação.
5. `evaluate.py`: oferta linear, oferta original (funções `NutritionSupplyCalculator.*`), erro, folga, estado, `V`, custo.
6. `ranking.py`: ordenação do FSD B.6.

Aceite: critérios **B.9-1 a B.9-8**. Em particular: identidade no ponto (1e-6), erro de ±5% em até 1% (±10% até 1,5%),
razões exatas, `min` de proteína, vetores de teste (três rações de 5.3: `D` = 0,908; 0,935; 0,855), aviso de replicação.

### E4. API do módulo — **P**

`POST /api/module/evaluate` (síncrona, FSD B.7), erros no formato da seção 11.3, validações de B.4 e B.5 (dietas com ao menos
um alimento, quantidades ≥ 0, consumo total > 0, alimentos ausentes da biblioteca do padrão removidos com aviso).
Aceite: testes de contrato da rota com dietas viáveis, inviáveis, mistas.

### E5. Interface do módulo — **M**

1. ~~Seletor "Exercício simples" × "Avaliar dietas (vaca real)" na tela 1; o exercício simples permanece o padrão.~~ Retirado em 11/11/2026: a tela 1 é só a avaliação de dietas.
2. Cartões **Vaca**, **Dietas**, **Preços** e **Resultado** (FSD B.2), estados vazio, carregando e erro.
3. Ranking, detalhe por restrição, erro de linearização; estado também em texto (não só cor).
4. Tipos e chamadas em `lib/types.ts` e `lib/api.ts`; build por `scripts\build-web.ps1`; conferir em 1.440 px e ≈ 540 px.

Aceite: FSD B.2 e B.4/B.5; sem regressão nas telas atuais (simulação, sensibilidade, curva, sobre).

### E6. Comparação com o RuFaS, fase 1 — **P** (depende de E3)

`compare.py` e relatório (tela e CSV): para a mesma vaca, lote e dieta, oferta e folga **linearizadas × originais do RuFaS**,
erro por restrição e por dieta, com as tolerâncias de LINEARIZACAO 6. Aceite: FSD B.8 (fase 1).

### E7. Dieta ótima e comparação com o SLSQP (RF-30, fase 2) — **G**

1. `optimize.py`: parametrização dos escalares globais (DMI, TDN%, %concentrado), dois regimes em TDN% = 60, um LP por ponto
   da grade e por ramo (energia e `min` de proteína), refinamento local (LINEARIZACAO 5.1b).
2. Roda como **tarefa em segundo plano** (`jobs.py`): o estudo levou 24 s para 3.536 pontos; progresso e cancelamento.
3. Comparação com o `RationOptimizer` do RuFaS: custo, ração, folgas; várias sementes (o RuFaS parte de ponto aleatório).
4. Preços-sombra das restrições ativas (só aqui existem).
5. Tela: dieta ótima como referência final e desvio de cada dieta (`(custo_d − custo_ótimo)/custo_ótimo`).

Aceite: resultado de LINEARIZACAO 10 reproduzido (custo do LP dentro de 0,1% do melhor do RuFaS no caso-base: 3,8373 contra
3,8342) e viabilidade da solução nas restrições **originais**. Se o caso-base divergir, parar e rever a formulação.

### E8. Complementos (independentes entre si; ordem sugerida)

| Etapa | Requisito | Tamanho | Observação |
|---|---|---|---|
| E8a | RF-27 painel de verificações V1 a V5 | M | Reaproveita a Tabela 5-1 e as regras de E3; só leitura de resultados existentes |
| E8b | RF-19 balanço nutricional | M | Compartilha a oferta × exigência de E3; vale para a simulação completa |
| E8c | RF-26 alimentos personalizados (arroz em grão) | M | Depende de Q9 (como tratar no NRC) e de testar o RuFaS com alimento fora da biblioteca |
| E8d | RF-22 importar preços (CSV, US$) | P | Mapeamento por id do RuFaS; itens sem correspondência listados |
| E8e | RF-20 exportar (CSV e relatório) | M | Depois de E6 e E7 para incluir os novos resultados |
| E8f | RF-21 salvar e carregar cenário | P | Arquivo local; versionar o formato |
| E8g | RF-13 tamanho do rebanho | P | Já aceito no back-end; só expor, com limites e aviso de tempo e memória |
| E8h | RF-23 mais nutrientes | — | Só se o professor exigir |

## 6. Dependências e caminho crítico

```
E0 ─┬─> E1 ──────────────┐
    └─> E2 ─> E3 ─> E4 ─> E5 ─> E6 ─> E7
                 └──────────────────> E8a, E8b
E1 ─> E8c ;  E3 ─> E8e ;  independentes: E8d, E8f, E8g
```

Caminho crítico: **E0 → E2 → E3 → E4 → E5 → E7**. E1 pode andar em paralelo com E2, mas o modo NASEM do módulo só fecha
depois de E1. Para uma primeira entrega ao professor, o conjunto mínimo é **E1 a E6** (fase 1 completa); E7 é a fase 2.

## 7. Estratégia de testes

| Camada | O que cobre | Observações |
|---|---|---|
| Unitária (lógica pura) | Classes L e E; ordenação; validações; conversões | Sem RuFaS; rápida |
| Identidade e erro | Oferta linear = original no ponto; erro fora do ponto (±5%, ±10%) | Usa as funções de oferta do RuFaS importadas |
| Vetores de referência | Três rações de 5.3 e a vaca de 650 kg / 40 kg de leite / 100 dias | Números gerados pelo RuFaS e gravados no teste |
| Contrato da API | Corpo, erros, avisos | Servidor em memória |
| Regressão do RuFaS completo | "Conjunto base" em NRC (igual à seção 15.4) e em NASEM | Lenta (≈ 20 s cada); marcada à parte (`-m rufas`) |
| Interface | Roteiro manual com capturas em 1.440 px e ≈ 540 px | Sem teste automatizado (decisão vigente) |

Execução: `..\.venv\Scripts\python -m pytest tests` a partir de `backend`. Os testes que importam o RuFaS exigem a pasta
`vendor/RuFaS` no `sys.path`; em pasta curta fora do OneDrive, se houver erro de DLL em caminho longo.

## 8. Riscos do plano

| Risco | Efeito | Mitigação |
|---|---|---|
| Importar o RuFaS no mesmo processo do servidor (estado global, memória, tempo de carga) | Lentidão ou efeitos colaterais entre requisições | Importação tardia; teste de duas avaliações seguidas; se falhar, processo auxiliar |
| Oferta não linear exige funções internas do RuFaS que mudam de assinatura | Quebra ao atualizar o RuFaS | Versão fixa (1.0.6); teste de contrato que falha cedo |
| Erro de linearização acima de 1% em dietas distantes do ponto | Comparação enganosa | Mostrar o erro sempre; recalcular os coeficientes em `x_d`; marcar "fora da região" |
| Otimizador do RuFaS não exercitado em vaca seca e novilha | Comparação da fase 2 só vale para lactação | Limitar RF-30 à vaca em lactação no início; ampliar depois |
| Fase 2 mais lenta que o estimado (grade maior, dois regimes, vários ramos) | Tela travada | Tarefa em segundo plano, grade grossa e refinamento local |
| Respostas do professor mudarem uma regra (ordenação, tolerância, replicação) | Retrabalho em E3 | Regras isoladas em `standards.py` e `ranking.py`; constantes nomeadas |
| Erro de unidade (ganho diário em g × kg) | Exigências absurdas | Validação de faixa na entrada e teste dedicado |
| Código fora de sincronia com os documentos | Documentos viram histórico | Em cada etapa, atualizar PRD (status) e FSD (marcar "implementado") |

## 9. Definição de pronto (por etapa)

1. Critérios de aceite do FSD cumpridos e testados; testes antigos continuam passando.
2. RuFaS sem alteração (`git status` limpo em `vendor/RuFaS`).
3. PRD (status do requisito), FSD (seção correspondente) e README atualizados.
4. Interface conferida nas duas larguras, com o build gerado.
5. Pendências novas registradas em `PERGUNTAS_PROFESSOR.md` ou no PRD (seção 15), nunca só no código.

## 10. Próximos passos imediatos

1. Enviar `PERGUNTAS_PROFESSOR.md` ao professor (as perguntas de E0 vão primeiro).
2. Revisão de consistência entre PRD, FSD, DOMINIO e DECISOES (item 5 do roteiro de documentação).
3. Quando o dono autorizar o início do código: abrir a ramificação de E1 e E2 (pequenas e independentes) e só então E3.

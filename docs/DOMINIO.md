# Dieta Ótima com RuFaS — Domínio e Regras de Negócio

> Documento gerado a partir da leitura direta do código-fonte (`backend/dietopt/`, `web/src/`, `scripts/`,
> `iniciar.bat`), em 12/10/2026. Reflete **exclusivamente o que está implementado e funcionando hoje**. Não contém
> histórico de decisões, propostas de mudança ou direções futuras: requisitos pendentes vivem no
> [PRD](PRD.md), decisões visuais no [DESIGN](DESIGN.md) e instruções de uso no [README](../README.md).
>
> A seção 8 (acrescentada e revista em 01/11/2026) registra as fontes científicas (NRC 2001, NASEM 2021, RuFaS) e o que foi conferido contra elas. Os requisitos
> planejados a partir dessa análise estão no [FSD](FSD.md), Anexo A, e não fazem parte do que está implementado.
>
> Escopo: apenas o que a equipe controla — a interface web, o servidor local e o adaptador que chama o RuFaS. O
> **RuFaS** (v1.0.6, `vendor/RuFaS`, sem modificação) é tratado como sistema externo: uma "caixa" que recebe arquivos
> de entrada e devolve arquivos de saída. Seu funcionamento interno só é descrito onde afeta o contrato com ele.

## 1. Problema que o sistema resolve

Formular a dieta de vacas leiteiras de custo mínimo e medir o efeito econômico dessa dieta ao longo da lactação
exige combinar um modelo de otimização (o problema da dieta, de Pesquisa Operacional) com um simulador biológico
(o RuFaS). Sem esta ferramenta, quem quer usar o RuFaS precisa editar arquivos JSON e CSV à mão, rodar linhas de
comando e processar saídas de centenas de megabytes — o que inviabiliza testar muitos cenários de preço.

O sistema automatiza essa ponte. Ele:

1. avalia dietas já montadas para uma vaca real e sugere a de custo mínimo, por programação linear, com as
   exigências do NASEM (2021) ou da NRC (2001) (Exercício do quadro, `backend/dietopt/module/`);
2. monta e executa uma simulação do RuFaS a partir de alimentos, preços e limites escolhidos na tela, e calcula custo,
   leite e **margem sobre o custo de alimentação**;
3. repete a simulação para combinações de preços (análise de sensibilidade) e mostra a tabela de cenários e o efeito
   de cada fator;
4. desenha a curva de lactação de Wood com PEV e gestação.

## 2. Quem usa

Uma pessoa por vez, na própria máquina: nutricionista, produtor de leite ou avaliador acadêmico. Não é multiusuário
nem multiestação — o servidor escuta em `127.0.0.1` (a própria máquina) e não tem autenticação (ver 5.10).

## 3. Arquitetura lógica (componentes)

| Componente | Arquivo(s) | Papel |
|---|---|---|
| Interface web (Next.js exportado como site estático) | `web/src/` → publicada em `frontend/` | Cinco telas, estado compartilhado, chamadas à API |
| Servidor local | `backend/dietopt/server.py` (porta 8000) | API JSON e arquivos estáticos; monta cenários a partir das requisições |
| Gerenciador de tarefas | `backend/dietopt/jobs.py` | Executa simulações em segundo plano, uma tarefa por vez, com progresso |
| Exercício do quadro (módulo) | `backend/dietopt/module/` | Modelo linear das restrições, avaliação e comparação de dietas e dieta ótima por PL (SciPy/HiGHS) com preços-sombra |
| Adaptador do RuFaS | `backend/dietopt/rufas_adapter.py` | `Scenario` → arquivos de entrada do RuFaS; executa `main.py` em subprocesso; detecta falha |
| Leitor de saídas | `backend/dietopt/rufas_results.py` | Filtros de saída e conversão dos JSONs do RuFaS em `SimulationResult` |
| Economia e cache | `backend/dietopt/scenarios.py` | Preços padrão, receita, custo, margem; cache por conteúdo do cenário |
| Sensibilidade | `backend/dietopt/sensitivity.py` | Pontos (grade ou hipercubo latino), cenários S1..SN, efeitos de Spearman |
| Curva de lactação | `backend/dietopt/lactation.py` | Curva de Wood e marcos (PEV, parto seguinte, secagem) |
| Biblioteca de alimentos | `backend/dietopt/feeds.py` | Lê a biblioteca NRC 2001 do RuFaS; tetos padrão; NEL estimada |
| Simulador externo | `vendor/RuFaS` (v1.0.6) | Simulação de fazenda leiteira; usado sem modificação |
| Instalação e execução | `scripts/setup.ps1`, `scripts/fetch_wheels.py`, `scripts/build-web.ps1`, `iniciar.bat` | Ambiente Python, build da interface, início do servidor |

Não há banco de dados. A "base" é o conjunto de arquivos do RuFaS (biblioteca de alimentos e exemplo `freestall`),
a pasta `runs/` (cenários e cache) e o `localStorage` do navegador.

### 3.1 Instalação, build e execução

- **Ambiente Python:** `scripts/setup.ps1` exige o Python 3.12 (`py -3.12`), clona o RuFaS v1.0.6 em `vendor/RuFaS`
  se a pasta não existir, cria `.venv` e instala `requirements-rufas.txt` com o `pip`. Se o `pip` falhar (erro de
  TLS com `files.pythonhosted.org`), `scripts/fetch_wheels.py` baixa os pacotes com `curl` para `wheelhouse/` e a
  instalação é refeita sem rede (`--no-index`). O RuFaS exige Python 3.12 ou 3.13.
- **Interface:** `scripts/build-web.ps1` copia `web/` para `%LOCALAPPDATA%\dietopt-web-build`, instala as dependências,
  compila (`output: 'export'`) e publica o resultado em `frontend/`. Só é necessário para quem altera a interface;
  quem apenas usa o sistema recebe `frontend/` já compilado.
- **Execução:** `iniciar.bat` abre `http://127.0.0.1:8000` no navegador e inicia `python -m dietopt.server --port 8000`
  a partir de `backend/`, com o Python de `.venv`. O servidor precisa continuar em execução enquanto a interface é
  usada.

### 3.2 Fluxo de uma simulação

```
Navegador                  Servidor (server.py)             Adaptador / RuFaS
   │ POST /api/jobs/simulate        │                                │
   │ ──────────────────────────────►│ JOBS.submit → job "queued"     │
   │ ◄── 202 { id, status }         │ thread aguarda o _RUN_LOCK     │
   │ GET /api/jobs/<id> (1,5 s)     │ scenario_from(params)          │
   │ ──────────────────────────────►│ evaluate(scenario)             │
   │                                │   cache_key → runs/_cache?     │ sim: devolve o resultado
   │                                │   não: run_scenario ──────────►│ monta runs/<nome>/ e executa
   │                                │                                │ main.py (subprocesso)
   │                                │ load_result (JSONs filtrados) ◄│
   │ ◄── status + progresso         │ margem = receita − custo       │
   │ ◄── done + resultado           │ grava runs/_cache/<hash>.json  │
```

## 4. Entidades e dados manipulados

### 4.1 Alimento da biblioteca (`FeedInfo`)
Lido de `NRC_comp.csv` e `user_feeds.csv` do RuFaS por `load_feed_library` (`feeds.py`). Campos: `id` (`rufas_id`),
`name`, `description`, `kind` (`Forage`, `Conc`, `Mineral`…), `category`, `dm`, `cp`, `ndf`, `ee`, `tdn`, `calcium`,
`phosphorus` e `default_price` (US$/kg MS, ilustrativo). Derivados: `default_max` (ver 5.2) e `nel_mcal_per_kg`.
Categorias excluídas por não fazerem sentido na ração de vacas em lactação: `Calf Liquid Feed`, `Starter`, e os
tipos `Milk` e `Starter`. Os 130 alimentos restantes formam a biblioteca exibida.

### 4.2 Alimento selecionado (somente no navegador)
`{ price, min, max }` por id de alimento, onde `price` é US$/kg MS e `min`/`max` são kg MS/vaca/dia. É o estado
`selected` do `AppProvider`.

### 4.3 Parâmetros da simulação (somente no navegador)
`SimParams`: `milkPrice` (padrão 0,45 US$/kg), `years` (padrão 1) e `maxReduction` (padrão 5 kg/vaca/dia).

### 4.4 Cenário (`Scenario`)
Todos os parâmetros que alteram o RuFaS (`rufas_adapter.py`): `name`, `start_date` (`2013:1`), `end_date`,
`random_seed` (42), `nutrient_standard` (`NRC` ou `NASEM`; a aplicação usa `NRC`), `cow_num` (`None` mantém o rebanho
do exemplo `freestall`), `lac_cow_ration`, `ration_tolerance`, `lac_cow_feeds`, `feed_limits` (kg/vaca/dia),
`feed_prices` (US$/kg), `milk_reduction_maximum` e `filters` (filtros de saída). Cada cenário vira a pasta
`runs/<nome>/` com cópias editadas de `config.json`, `animal.json`, `feed.json`, `NRC_comp.csv`, `metadata.json`,
`tasks.json` e `task_manager_metadata.json`. O nome das pastas de cenários da web é `web_<id do job>`.

### 4.5 Resultado da simulação (`SimulationResult`)
Extraído dos JSONs de saída (`rufas_results.py`):

- **Diário (rebanho):** `days`, `milk_kg` (leite total por dia), `milking_cows`, `avg_dim`, `fat_kg`, `protein_kg`.
- **Por intervalo de formulação da ração:** `interval_days`, `ration_kg_per_cow` (id do alimento → kg/vaca/dia, mais
  `dry_matter_intake_total`), `requirements` (exigências médias do lote), `cows_in_pen`.
- **Compras:** `purchase_cost` e `purchase_amount` por alimento e intervalo.
- **Curva de lactação:** `wood`, parâmetros `l`, `m`, `n` por paridade (1, 2, 3).

Derivados: `total_milk_kg` (soma do leite diário) e `total_purchase_cost`. Persistido em
`runs/_cache/<hash>.json` (`result_to_dict` / `result_from_dict`).

### 4.6 Avaliação econômica (`Evaluation`)
`name`, `ok`, `seconds`, `milk_kg`, `milk_revenue`, `feed_cost` (compras do rebanho no período),
`lac_cost_per_cow_day`, `margin`, `ration` (kg MS/vaca/dia, média dos intervalos), `reduction` (redução média de
leite imposta pelo RuFaS), `result` e `detail` (motivo da falha, quando `ok` é falso).

### 4.7 Tarefa (`Job`)
`id` (10 caracteres), `kind` (`simulate` ou `sensitivity`), `params`, `status` (`queued`, `running`, `done`, `error`),
`done`, `total`, `result`, `error`, `created`, `finished`. Vive só na memória do servidor.

### 4.8 Problema do quadro (removido)

Retirado em 11/11/2026 (o exercício simples de arroz e milho deixou de fazer parte do trabalho). As estruturas `Food`, `NutrientBounds` e `DietResult` saíram junto com `diet_lp.py`.

### 4.9 Fator de sensibilidade e linha de cenário
`Factor`: `key` (id do alimento ou `milk_price`), `label`, `low`, `high`. Linha de cenário: `cenario` (`S1`…`SN`), um
valor por fator, `leite_kg`, `receita`, `custo_alimentacao`, `custo_vaca_dia`, `reducao_leite`, `Res` (margem) e
`ration`; em caso de falha, `Res = null` e `erro`. Resultado da análise: `columns`, `rows` e `effects`.

### 4.10 Armazenamento local
- **Navegador (`localStorage`):** chave `dietopt.v1` com `selected` e `params` (restaurados ao abrir); `theme`
  (next-themes). Resultados de simulação e de sensibilidade ficam só na memória da página, assim como o estado do
  Exercício do quadro.
- **Disco (`runs/`):** pasta de cada cenário (inclui `console.log` da execução) e o cache `runs/_cache/`. Nenhuma pasta
  é apagada automaticamente; a pasta de um cenário é recriada se o mesmo nome for usado de novo.
- **Servidor (memória):** tarefas (`JobManager`), perdidas ao reiniciar.

## 5. Regras de negócio

### 5.1 Exercício do quadro simples (removido)

Retirado em 11/11/2026 (o exercício simples de arroz e milho deixou de fazer parte do trabalho). O Exercício do quadro é hoje a avaliação de dietas de uma vaca real (FSD, Anexo B; `LINEARIZACAO.md`).

### 5.2 Biblioteca de alimentos e tetos padrão (`feeds.py`)
O teto de inclusão padrão (`default_max`, kg MS/vaca/dia) evita que um mineral barato vire "enchimento":

| Condição (nesta ordem) | Teto |
|---|---|
| `kind = Mineral` ou categoria `Vitamin/Mineral` | 0,6 |
| extrato etéreo `ee ≥ 80` (gorduras) | 0,9 |
| proteína bruta `cp ≥ 60` (farinhas proteicas) | 1,0 |
| demais | 100 (sem teto prático) |

NEL estimada do alimento: `0,0245 · TDN − 0,12` (Mcal/kg MS, NRC 2001, Eq. 2-3). É informativa na interface; a oferta
de energia na simulação é calculada pelo RuFaS.

### 5.3 Montagem do cenário (`scenario_from`, `build_scenario`)
- **Período:** `years` é limitado a 1–3 (a interface oferece 1 ou 2). A simulação vai de `2013:1` a `<2012+years>:365`.
- **Padrão nutricional:** sempre `NRC`. Para NRC, alimentos do exemplo que só existem no NASEM são trocados:
  301 → 230 (carbonato de cálcio) e 302 → 167 (farelo de soja 48% PB), em todo campo de id (`feed_type`,
  `purchased_feed` e listas `*_feeds`).
- **Ração:** o sistema **não** impõe percentuais. Informa ao otimizador do RuFaS apenas a lista de alimentos
  permitidos às vacas em lactação (`lac_cow_feeds`); o RuFaS formula a ração de custo mínimo.
- **Limites de inclusão:** os do usuário `[mín, máx]` ou, na falta deles, `[0, default_max]` do alimento. São
  gravados nas colunas `lower_limit` e `limit` de `NRC_comp.csv`, em **kg por animal por dia**.
- **Preços:** os do usuário prevalecem sobre `DEFAULT_PRICES`. Alimento que já constava das compras do exemplo recebe o
  novo preço; os demais são adicionados com `buffer = 0.15` e limites de compra de 1000 para cada tipo de compra.
- **Redução máxima de leite:** `milk_reduction_maximum` = valor do usuário, padrão **5,0** kg/vaca/dia.
- **Semente:** 42, salvo informação em contrário. Rebanho: o do exemplo `freestall`, salvo `cow_num`.
- **Caminhos:** todo caminho passado ao RuFaS é relativo a `vendor/RuFaS` (`rel()`), porque o validador do RuFaS
  rejeita caracteres acentuados.

### 5.4 Execução do RuFaS (`run_scenario`)
- Roda `main.py` em subprocesso com `vendor/RuFaS` como diretório de trabalho, `PYTHONIOENCODING=utf-8` e tempo
  limite de 3600 s. A saída completa vai para `runs/<nome>/console.log`.
- **Sucesso** exige código de saída 0 **e** a linha `Finished task: 1/1 with 0 error(s)` no console, porque o gerenciador
  de tarefas do RuFaS sai com código 0 mesmo quando a tarefa falha.
- **Falha:** o detalhe é a última linha do console que começa com `...Error` ou `...Exception` (ou os últimos 300
  caracteres). Uma simulação isolada que falha vira erro da tarefa (`RuntimeError`); numa sensibilidade, vira linha
  com `Res = null`.
- **Filtros de saída** (`RESULT_FILTERS`): só quatro grupos são gravados — estatísticas do rebanho (leite, vacas em
  lactação, dias em lactação, gordura e proteína), ração, exigências e nutrientes do lote em lactação, compras de
  alimentos e parâmetros `l`, `m`, `n` da curva de lactação.

### 5.5 Cache de simulações (`cache_key`, `simulate`)
A chave é o SHA-1 (16 primeiros caracteres) do conteúdo do cenário **sem** `name` e `filters`. Se `runs/_cache/<chave>.json`
existe, o resultado é reaproveitado sem executar o RuFaS (`detail = "cache"`, `seconds = 0`). Só execuções bem-sucedidas
são gravadas. Mudar preço de alimento, limite, lista de alimentos, período, semente ou redução máxima gera nova chave;
mudar apenas o **preço do leite** não altera o cenário e, portanto, usa o cache.

### 5.6 Economia: custo, receita e margem (`evaluate`)
- `receita = leite_total_kg × preço_do_leite` (padrão 0,45 US$/kg).
- `custo_de_alimentação = Σ (quantidade comprada do alimento no período × preço do alimento)`, para todo o rebanho.
- **`margem = receita − custo_de_alimentação`.**
- `custo da ração por vaca por dia`: para cada intervalo, `Σ kg × preço` da ração por vaca (sem
  `dry_matter_intake_total`); depois a média dos intervalos.
- `ração média`: média, entre intervalos, dos kg MS/vaca/dia de cada alimento.
- `reduction` (**leite perdido**): média, entre intervalos, de `avg_milk_production_reduction_pen`.
- Preços: `DEFAULT_PRICES` (19 alimentos, ilustrativos) com os do usuário sobrepostos. Um alimento **sem preço em
  nenhuma das fontes** entra no custo a **US$ 0**. A interface evita isso preenchendo todo alimento selecionado
  com: preço padrão → preço da biblioteca → Forage 0,12 / Conc 0,35 / Mineral 0,15 → 0,30.
- Se a simulação falha, a avaliação sai com `ok = false` e sem valores numéricos.

### 5.7 Degradação do leite
O leite simulado segue a curva de Wood e só **cai** quando o otimizador do RuFaS não encontra ração que atenda às
exigências: ele reduz o leite em 0,25 kg por tentativa até `milk_reduction_maximum`; acima disso a simulação
aborta. O sistema não altera essa lógica; apenas amplia o limite (padrão 5,0) para a simulação degradar em vez de
abortar, e mostra o leite perdido.

### 5.8 Análise de sensibilidade (`run_sensitivity`)
- **Fatores:** preço de um alimento (exige simulação) ou `milk_price` (só altera a receita). Padrão na tela: farelo de
  arroz (138) e milho em grão (44) com ±50% do preço, e preço do leite com ±20%.
- **Pontos:** `grid` gera `max(n, 2)` níveis por fator e o produto cartesiano (`n^k` pontos); `latin` gera `n` amostras
  com uma amostra por estrato de cada fator (semente 42).
- **Simulações únicas:** pontos com os mesmos preços de alimento (arredondados a 4 casas) compartilham uma única
  simulação; fatores de leite não geram simulação. Estimativa na tela: `grade: n^(fatores de alimento)`,
  `latin: n` simulações, a 17 s cada.
- **Execução:** em lotes de até `workers` simulações (padrão 2) em paralelo; o progresso é "feitas de total".
- **Linha `Sn`:** valores dos fatores, leite total, `receita = leite × preço do leite do ponto`, custo, custo por
  vaca por dia, leite perdido, ração (apenas alimentos com mais de 0,001 kg) e `Res = receita − custo`. Falha →
  `Res = null` e `erro`.
- **Efeito:** correlação de postos de Spearman entre cada fator e `Res`, só com as linhas válidas. Fica `null` com
  menos de 3 linhas válidas, ou se o fator ou `Res` não variam.

### 5.9 Tarefas e concorrência (`jobs.py`)
- Cada requisição de simulação ou sensibilidade cria uma tarefa e a executa numa *thread*.
- Um **bloqueio global** (`_RUN_LOCK`) permite **uma tarefa por vez**; as demais ficam `queued` até a anterior terminar.
  Cada sensibilidade pode usar até 2 simulações em paralelo (~1,2 GB de RAM cada).
- Qualquer exceção vira `status = error` com tipo, mensagem e parte do *traceback*; `finished` é sempre preenchido.
- A interface consulta o estado a cada 1,5 s.

### 5.10 Servidor e API (`server.py`)
- Escuta em `127.0.0.1:8000` por padrão (`--host` e `--port` configuráveis). Não há autenticação, token, controle de
  origem nem limite de requisições: a proteção é só o endereço local. Não deve ser exposto à rede.
- Rotas: `GET /api/feeds`, `/api/defaults`, `/api/lactation`, `/api/jobs`, `/api/jobs/<id>`; `POST /api/module/*`,
  `/api/jobs/simulate`, `/api/jobs/sensitivity` (responde 202). `POST` em rota inexistente e
  tarefa desconhecida → 404 JSON; exceção → 500 JSON com `Tipo: mensagem`; `GET` fora da API tenta um arquivo
  estático e, se não houver, responde 404 em texto.
- Respostas JSON trocam `NaN` e infinito por `null`. Todas as respostas levam `Cache-Control: no-store`.
- Arquivos estáticos vêm de `frontend/`: `/` e pastas servem `index.html`; caminhos fora de `frontend/` retornam 404;
  `HEAD` é aceito; pedidos `…__next.<rota>.__PAGE__.txt` são mapeados para `…__next.<rota>/__PAGE__.txt`.

### 5.11 Curva de lactação (`lactation.py`)
- Curva de Wood: `y(t) = l · t^m · e^(−n·t)`, em kg de leite por dia, para `t = 1…330`.
- Os parâmetros por paridade vêm do RuFaS (`result.wood`). Sem simulação, vale o padrão `DEFAULT_WOOD` (média base do
  RuFaS mais o ajuste de paridade, sem os ajustes de ano, região e frequência de ordenha); a resposta indica a origem
  (`wood_from_rufas`).
- **Marcos:** `proximo_parto = PEV + gestação` e `secagem = proximo_parto − dias de secagem`. Padrão do quadro:
  PEV 60, gestação 270, secagem 60 dias antes do parto.
- **Pico:** dia e valor do máximo da curva. **Produção em 305 dias:** soma dos 305 primeiros dias.

### 5.12 Regras da interface
- Simular exige **no mínimo 3 alimentos** selecionados; a sensibilidade também desabilita o botão nesse caso, ou sem
  fatores marcados.
- Campos numéricos vazios viram um padrão antes do envio: preço do alimento 0,30; mínimo 0; máximo 100; preço do
  leite 0,45; redução máxima 5.
- Conjunto base de alimentos: ids 50, 110, 44, 167, 138, 230 e 23. Lista ampla: 50, 51, 110, 104, 95, 44, 47, 138, 167,
  164, 169, 58, 193, 194, 24, 1, 230 e 23.
- Ao abrir, a seleção anterior (`dietopt.v1`) é restaurada; sem ela, vale o conjunto base.
- Os dados sobrevivem à navegação entre telas (estado em um `AppProvider`), mas não a recarregar a página.
- Mensagens de falha mostram a primeira linha do erro; o detalhe completo está em `runs/<nome>/console.log`.

## 6. Fora de escopo (explicitamente ausente do sistema atual)

Esta ferramenta **não tem**: perfis de usuário, permissões, autenticação, banco de dados, auditoria, múltiplas
fazendas ou rebanhos salvos, histórico de simulações, salvar ou carregar cenários, exportação (CSV ou relatório),
importação de preços (CEPEA ou outra fonte), padrão NASEM 2021, balanço de nutrientes (oferta × exigência) da ração,
ajuste do tamanho do rebanho pela interface, otimização por fase da lactação, modelo próprio de resposta do leite à
dieta, linha de comando, nem hospedagem em nuvem. A ração é sempre formulada pelo otimizador do RuFaS; o sistema
não a recalcula nem a altera.

## 7. Rastreabilidade (onde cada regra vive no código)

| Regra | Arquivo | Função/trecho | Teste automatizado |
|---|---|---|---|
| Dieta ótima do Exercício do quadro e preços-sombra | `backend/dietopt/module/optimize.py` | `optimize_diet` | `test_module_optimize.py` |
| Biblioteca e tetos padrão (5.2) | `backend/dietopt/feeds.py` | `load_feed_library`, `FeedInfo.default_max`, `nel_mcal_per_kg` | `test_adapter.py`: tetos padrão |
| Limites, preços, período e redução máxima (5.3) | `backend/dietopt/server.py` | `scenario_from`, `feed_limits_from` | — |
| Troca de ids NASEM → NRC (5.3) | `backend/dietopt/rufas_adapter.py` | `NASEM_ONLY_TO_NRC`, `remap_feed_ids` | `test_adapter.py`: troca de ids |
| Arquivos de entrada do RuFaS (5.3) | `backend/dietopt/rufas_adapter.py` | `build_scenario`, `write_feed_library`, `rel` | — |
| Execução e detecção de falha (5.4) | `backend/dietopt/rufas_adapter.py` | `run_scenario`, `failure_reason` | `test_adapter.py`: resumo da falha |
| Filtros e leitura das saídas (5.4) | `backend/dietopt/rufas_results.py` | `RESULT_FILTERS`, `parse_outputs`, `load_result` | — |
| Cache (5.5) | `backend/dietopt/scenarios.py` | `cache_key`, `simulate`, `CACHE_DIR` | `test_adapter.py`: chave de cache |
| Receita, custo, margem (5.6) | `backend/dietopt/scenarios.py` | `evaluate`, `DEFAULT_PRICES`, `DEFAULT_MILK_PRICE` | — |
| Leite perdido (5.7) | `backend/dietopt/server.py`, `scenarios.py` | `milk_reduction_maximum` em `scenario_from`; `reduction` em `evaluate` | — |
| Pontos da sensibilidade (5.8) | `backend/dietopt/sensitivity.py` | `sample_points` | `test_sensitivity.py`: grade e hipercubo latino |
| Tabela S1..SN (5.8) | `backend/dietopt/sensitivity.py` | `run_sensitivity` | — |
| Efeito de Spearman (5.8) | `backend/dietopt/sensitivity.py` | `rank_effects` | `test_sensitivity.py`: sinal dos efeitos |
| Estimativa de simulações e tempo (5.8) | `web/src/views/SensitivityView.tsx` | `SECONDS_PER_SIMULATION`, `points`, `sims` | — |
| Tarefas e concorrência (5.9) | `backend/dietopt/jobs.py` | `_RUN_LOCK`, `JobManager.submit`, `_run` | — |
| Consulta de progresso (5.9) | `web/src/lib/api.ts` | `runJob` | — |
| API e arquivos estáticos (5.10) | `backend/dietopt/server.py` | `Handler.do_GET`, `do_POST`, `do_HEAD`, `_static`, `clean` | — |
| Curva de lactação e marcos (5.11) | `backend/dietopt/lactation.py` | `wood_yield`, `lactation_curve`, `milestones`, `peak`, `milk_305` | — |
| Regras de seleção e padrões da tela (5.12) | `web/src/views/CowView.tsx`, `web/src/providers/AppProvider.tsx` | `run`, `simulationBody`, `priceOf`, `PRESET_BASE`, `PRESET_WIDE`, `STORAGE_KEY` | — |
| Instalação e execução (3.1) | `scripts/`, `iniciar.bat` | `setup.ps1`, `fetch_wheels.py`, `build-web.ps1` | — |

Os 71 testes automatizados ficam em `backend/tests/` e cobrem a coluna da direita; as demais regras foram verificadas
manualmente (execução real do RuFaS e uso das telas), sem teste automatizado.

## 8. Fontes científicas e rastreabilidade das referências

Esta seção registra **de onde vêm** os números e as equações do sistema e **o que foi conferido** contra as fontes.
Descreve o estado de 01/11/2026. Os requisitos planejados a partir desta análise (padrão NASEM, alimentos
personalizados e verificações de consistência) estão no [FSD](FSD.md), Anexo A, e não fazem parte do que está
implementado.

### 8.1 Fontes

| Fonte | Como foi usada | Onde está |
|---|---|---|
| **NRC (2001)**, *Nutrient Requirements of Dairy Cattle*, 7ª ed. | Padrão nutricional do sistema, aplicado **pelo RuFaS** (`nutrient_standard = "NRC"`). O PDF tem camada de texto. | `Downloads/NRC 2001.pdf` (fora do projeto) |
| **NASEM (2021)**, 8ª ed. revisada, tradução da Santafé Agroinstituto (errata de 08/2022 incorporada) | **Somente referência**: o sistema não oferece o padrão NASEM. O PDF é uma digitalização sem texto; as notas foram feitas por OCR e auditadas | `docs/nasem2021_notas/` (local, não versionada) |
| **RuFaS v1.0.6** | Simulador; implementa as equações dos dois padrões e traz as bibliotecas de alimentos | `vendor/RuFaS` |

O livro do NASEM afirma que, em caso de divergência entre o texto e o modelo, **prevalece o código R oficial** (p. 472).
Esse código não está no projeto.

### 8.2 O que vem do NRC 2001 e foi conferido no PDF

| Item do sistema | Referência no NRC | Resultado da conferência |
|---|---|---|
| NEL estimada na lista de alimentos, `0,0245 × TDN − 0,12` (`feeds.py`) | Eq. 2-3 | Confere. O NRC avisa que a Eq. 2-3 assume consumo de 3× a manutenção. Para TDN igual a 0 (minerais) o código dá −0,12 Mcal/kg (ver FSD, D7) |
| "A NRC 2001 só tem farelo de arroz" (RN-07) | Tabela 15-1 | Confere: só existe "Rice, Bran" (entrada 95) |
| Composição dos alimentos (`NRC_comp.csv` do RuFaS) | Tabela 15-1 | 4 linhas conferidas (milho moído seco, farelo de arroz, farelo de soja 48% e silagem de milho imatura): MS, PB, FDN, EE e TDN batem. As outras 130 linhas **não** foram conferidas |
| Consumo de matéria seca de vaca em lactação calculado pelo RuFaS | Eq. 1-2 | O código do RuFaS (`nrc_requirements_calculator.py`) implementa a equação como no PDF, com FCM = 0,4 × leite + 15 × gordura × leite ÷ 100 e `(1 − e^(−0,192 × (semanas em lactação + 3,67)))` |

### 8.3 O que vem do NASEM 2021 e foi conferido (referência, não usado no cálculo)

| Item | Resultado |
|---|---|
| O RuFaS no modo NASEM: consumo (Eq. 2-1), mantença 0,10 Mcal/kg de peso metabólico (Eq. 3-13), útero gravídico (Eq. 3-15 e 3-16a), cálcio e fósforo de lactação (Eq. 7-4 e 7-8b) | Conferem com as notas do NASEM |
| Fósforo de mantença de vaca seca no RuFaS (`0,8 × consumo + 0,0006 × peso`) | Diverge das notas (Eq. 7-5b: 1,0 g/kg de MS para vacas adultas, secas e lactantes). **Confirmado na imagem da p. 124** (01/11/2026). Não afeta a vaca em lactação |
| Biblioteca NASEM do RuFaS contra a Tabela 19-1 (88 de 180 alimentos já transcritos nas notas) | 53 linhas com correspondente (MS, PB e FDN iguais); 3 diferem em amido, por arredondamento; 35 sem correspondente automático (óleos e gorduras, silagens sem espiga, arroz em grão, farelo de arroz desengordurado, glúten úmido, entre outros) |
| Arroz em grão | A Tabela 19-1 traz "Grãos de Arroz" (p. 427: MS 87,9%; PB 8,1%; amido 75,8%; FDN 6,4%). **Nenhuma** das bibliotecas do RuFaS o carrega |
| Tabela 5-1 (FDN de forragem, FDN total, amido) | Completa: (19, 25, 30), (18, 27, 28), (17, 29, 26), (16, 31, 24), (15, 33, 22). A Tabela 21-1 imprime "FDN de forragem mín. 19–25", divergente (observação nossa; as notas não a registram) |
| Biblioteca NASEM do RuFaS, coluna `is_wetforage` | Verdadeira em 33 alimentos, inclusive vários com MS acima de 80% (farelo de arroz, grão de aveia, farinha de carne e ossos). O efeito **não** foi verificado |

### 8.4 Constantes do RuFaS que condicionam a ração obtida

Valem para os dois padrões. Não vêm de uma equação do NRC nem do NASEM.

| Constante (`animal_module_constants.py`) | Valor | Efeito |
|---|---|---|
| `MINIMUM_RATION_NDF` / `MAXIMUM_RATION_NDF` | 25% / 45% da MS | FDN total da ração |
| `MINIMUM_RATION_FORAGE_NDF` | 15% da MS | FDN de forragem mínima (a Tabela 5-1 do NASEM trata de 15 a 19%, conforme FDN total e amido) |
| `MAXIMUM_RATION_FAT` | 7% da MS | Extrato etéreo máximo |
| `DMI_CONSTRAINT_FRACTION` | 0,30 | A ração pode ter consumo até 30% acima do estimado |
| `PROTEIN_UPPER_LIMIT_FACTOR` | 1,5 | Oferta de proteína metabolizável no máximo 1,5 × a exigência |

### 8.5 Observações sobre os resultados já guardados (`runs/_cache/`)

Análise de 57 simulações em cache (preços ilustrativos, padrão NRC), feita em 01/11/2026:
- O consumo estimado ficou em ≈ 25,8 kg/dia e o consumo da ração entre 28 e 34 kg/dia; várias simulações bateram no teto de ≈ 33,5 kg (+30%).
- A FDN total ficou em 45% (o teto do RuFaS) na maioria; a FDN de forragem, entre 30% e 45%; o amido, entre 2% e 28%. Todas cumprem a Tabela 5-1 do NASEM.
- Uma ração com 11 kg/dia de farelo de arroz chegou exatamente ao teto de 7% de gordura.

### 8.6 Erro típico dos modelos (do próprio NASEM)

| Saída | RMSE | CCC | Fonte |
|---|---|---|---|
| Consumo, equação só com fatores do animal (Eq. 2-1) | 12,1% (texto: 12,4%) | 0,71 | Avaliação do modelo, cap. 20, pp. 522–523 |
| Consumo, equação com fatores da dieta (Eq. 2-2) | 15,9% (texto: 17,3%) | 0,54 | idem |
| Leite (empírico, a partir de proteína e gordura previstas) | 14,6% | 0,75 | idem |
| Proteína do leite / gordura do leite | 14,4% / 17,1% | 0,75 / 0,62 | idem |
| Leite "permitido" por energia / por proteína metabolizável | 24,4% / 22,1% | 0,67 / 0,64 | idem; o livro desaconselha usá-los como meta |

Para comparação: o limite de +30% de consumo do RuFaS equivale a mais de duas vezes o erro típico da Eq. 2-1.

### 8.7 O que não tem fonte científica no código

| Item | Origem real |
|---|---|
| `DEFAULT_PRICES` e `DEFAULT_MILK_PRICE` | Valores ilustrativos escolhidos pela equipe; não são cotações (CEPEA ou outra) |
| Tetos de inclusão padrão (0,6 / 0,9 / 1,0 kg MS/vaca/dia) | Escolha da equipe, descrita no código como "tetos usuais de formulação"; **não** extraídos do NRC nem do NASEM |
| `DEFAULT_WOOD` | Média base do RuFaS mais o ajuste de paridade do arquivo de ajuste de lactação do RuFaS; a curva de Wood é de Wood (1967) |
| 17 s por simulação na estimativa da sensibilidade | Média observada (≈ 66 s para 4 simulações com 2 em paralelo) |
| Redução máxima de leite padrão de 5 kg/vaca/dia | Escolha da equipe, para a simulação degradar em vez de abortar |

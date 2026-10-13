# Documento de Requisitos do Produto (PRD)

**Produto:** Dieta Ótima com RuFaS
**Versão do documento:** 0.3 (rascunho para avaliação)
**Data:** 12/10/2026
**Status:** Versão web implementada; documento em revisão
**Autor(es):** _[a preencher]_
**Disciplina / Professor / Instituição:** Pesquisa Operacional · _[a preencher]_ · _[a preencher]_
**Escopo deste documento:** somente a **aplicação web local**. A versão em linha de comando com relatório está fora
deste PRD.
**Documentos relacionados:** [DESIGN.md](DESIGN.md) (interface) · [README](../README.md) (instalação e uso)

---

## Sumário

1. [Visão Geral do Produto](#1-visão-geral-do-produto)
2. [Problema que o Sistema Resolve](#2-problema-que-o-sistema-resolve)
3. [Objetivos do Sistema](#3-objetivos-do-sistema)
4. [Personas e Perfis de Usuário](#4-personas-e-perfis-de-usuário)
5. [Escopo da Primeira Versão](#5-escopo-da-primeira-versão)
6. [Funcionalidades Fora de Escopo](#6-funcionalidades-fora-de-escopo)
7. [Regras de Negócio](#7-regras-de-negócio)
8. [Informações que o Sistema Precisa Controlar](#8-informações-que-o-sistema-precisa-controlar)
9. [Fluxos Principais de Uso](#9-fluxos-principais-de-uso)
10. [Histórias de Usuário](#10-histórias-de-usuário)
11. [Critérios de Aceitação](#11-critérios-de-aceitação)
12. [Consultas, Relatórios e Indicadores](#12-consultas-relatórios-e-indicadores)
13. [Requisitos Não Funcionais](#13-requisitos-não-funcionais)
14. [Limitações da Primeira Versão](#14-limitações-da-primeira-versão)
15. [Pontos Pendentes Antes do FSD](#15-pontos-pendentes-antes-do-fsd)
16. [Resumo Final do PRD](#16-resumo-final-do-prd)

**Apêndices:** [A. Premissas, restrições e dependências](#apêndice-a-premissas-restrições-e-dependências) ·
[B. Riscos e mitigações](#apêndice-b-riscos-e-mitigações) · [C. Visão técnica resumida](#apêndice-c-visão-técnica-resumida) ·
[D. Rastreabilidade com o pedido do professor](#apêndice-d-rastreabilidade-com-o-pedido-do-professor) ·
[E. Glossário](#apêndice-e-glossário) · [F. Referências](#apêndice-f-referências) ·
[G. Formulação matemática](#apêndice-g-formulação-matemática) · [H. Histórico de revisões](#apêndice-h-histórico-de-revisões)

> **Nota sobre a numeração.** As seções 1 a 12 e 14 a 16 seguem a estrutura padrão de PRD pedida para este trabalho.
> A estrutura não lista a seção 13; ela foi preenchida com **Requisitos Não Funcionais**, que já existiam neste
> documento e ficariam sem lugar. Se a numeração esperada for outra, basta renumerar.

---

## 1. Visão Geral do Produto

### 1.1 Resumo

O **Dieta Ótima com RuFaS** é uma aplicação web local que ajuda a formular a dieta de vacas leiteiras de **custo
mínimo** e a medir seu efeito econômico ao longo da lactação. Ela une três peças:

- um **otimizador de dieta** (programação linear) que resolve o problema do quadro do professor, com arroz e milho;
- o **RuFaS**, um simulador de fazenda leiteira de código aberto, usado como simulador de rebanho e de exigências
  nutricionais segundo a **NRC (2001)**;
- uma **análise de sensibilidade** que varia preços de alimentos e do leite e mostra como a margem sobre o custo de
  alimentação reage.

O usuário-alvo é o **nutricionista ou produtor de leite**. O estado atual é um **protótipo acadêmico validado
tecnicamente**: o fluxo completo funciona, mas o uso profissional exige requisitos ainda pendentes (preços reais,
balanço nutricional explícito, exportação e validação contra uma referência). Esses itens estão identificados nas
seções 5.2.5, 14 e 15.

### 1.2 Ficha do produto

| Item | Descrição |
|---|---|
| Nome | Dieta Ótima com RuFaS |
| Tipo | Aplicação web local (o navegador acessa um servidor que roda na própria máquina) |
| Plataforma | Windows 10/11; Python 3.12 ou 3.13; navegador moderno |
| Usuário-alvo | Nutricionista de rebanho leiteiro e produtor de leite (persona principal e secundária, seção 4) |
| Avaliador | Professor de Pesquisa Operacional |
| Núcleo científico | RuFaS v1.0.6 (GPLv3, usado sem modificação), padrão NRC (2001) |
| Núcleo de otimização | Programação linear (SciPy/HiGHS) para o exercício; otimizador SLSQP do próprio RuFaS para a ração da vaca |
| Entrega principal | Cinco telas: exercício do quadro, vaca leiteira, curva de lactação, sensibilidade, premissas e limites |
| Estado | Implementado e testado (10 testes automatizados); validação científica pendente |

### 1.3 Proposta de valor

Responder, sem editar arquivos nem usar linha de comando: _qual ração atende à vaca pelo menor custo, quanto sobra de
margem sobre a alimentação e o que acontece se os preços mudarem?_

---

## 2. Problema que o Sistema Resolve

### 2.1 Origem

Na disciplina de Pesquisa Operacional, o professor apresentou o problema da dieta de custo mínimo de uma fazenda
(arroz e milho como fontes de carboidrato e proteína, com mínimos e máximos diários por nutriente) e, depois da
modelagem, apresentou o RuFaS e pediu um sistema que o integre para calcular a dieta de forma automatizada.

### 2.2 Problema

Formular a dieta de um rebanho leiteiro envolve decisões que se afetam mutuamente:

- a dieta precisa atender às exigências de energia, proteína, minerais e fibra da vaca, que mudam com a fase da
  lactação;
- os preços dos alimentos e do leite oscilam, e o que é ótimo hoje pode deixar de ser amanhã;
- o leite produzido, o custo da dieta e as exigências estão ligados por um modelo biológico complexo.

### 2.3 Como é feito hoje

| Alternativa atual | Limitação |
|---|---|
| Planilha de formulação | Difícil de auditar; não simula o efeito ao longo da lactação. |
| Software comercial de formulação | Caixa-preta e pago; não permite examinar o modelo nem varrer cenários com facilidade. |
| RuFaS usado diretamente | Exige editar arquivos JSON à mão, rodar linhas de comando e processar saídas de centenas de megabytes. |

Isso inviabiliza o que o professor e o usuário profissional querem fazer: **testar muitos cenários de preço e comparar
resultados**.

### 2.4 Oportunidade

Oferecer uma interface que esconda essa complexidade, preserve a fidelidade científica do RuFaS e entregue, para cada
cenário, a **dieta ótima, o custo e a margem**, com tabelas e gráficos prontos para decisão e apresentação.

---

## 3. Objetivos do Sistema

### 3.1 Objetivos

| ID | Objetivo |
|---|---|
| O1 | Reproduzir fielmente o exercício do quadro (PL de dieta de custo mínimo) e generalizá-lo para vários alimentos. |
| O2 | Integrar o RuFaS como simulador, sem modificá-lo, para obter exigências, leite e ração de uma vaca em lactação. |
| O3 | Permitir a análise de sensibilidade de preços e limites com uma tabela de cenários no formato do quadro. |
| O4 | Visualizar a curva de lactação e seus marcos reprodutivos (PEV, gestação, secagem). |
| O5 | Tornar falhas e limitações do modelo visíveis, e não escondê-las. |

Os itens que **não** são objetivos desta versão estão na seção 6.

### 3.2 Métricas de sucesso

| ID | Métrica | Meta | Medição atual | Situação |
|---|---|---|---|---|
| M1 | Reprodução do exercício do quadro | custo ótimo = US$ 15,35 ± 0,01; arroz 4,473 kg; milho 3,873 kg | US$ 15,3453; 4,473 kg; 3,873 kg | Atingida |
| M2 | Tempo de uma simulação RuFaS (1 ano, 100 vacas) | ≤ 60 s | 30 a 37 s | Atingida |
| M3 | Tempo de uma sensibilidade com 4 simulações | ≤ 3 min | ~66 s (2 em paralelo) | Atingida |
| M4 | Simulações que falham sem aviso ao usuário | 0 | 0 (bug corrigido e verificado manualmente; o teste automatizado cobre só o resumo da falha) | Atingida |
| M5 | Testes automatizados passando | 100% | 10 de 10 | Atingida |
| M6 | Desvio da ração ótima em relação a uma referência profissional (formulador comercial ou tabelas da NRC) | _a definir com o professor_ | não medido | **Pendente** |
| M7 | Cenários com preços reais (CEPEA) usados em uma demonstração | ≥ 1 cenário completo | preços ilustrativos | **Pendente** |

---

## 4. Personas e Perfis de Usuário

As personas abaixo são **ilustrativas** (fictícias) e servem para orientar decisões de produto.

### 4.1 Persona principal: Marina, nutricionista de rebanho leiteiro

- **Perfil:** atende várias fazendas; formula rações e compara alternativas de ingredientes.
- **Objetivos:** achar a ração mais barata que atenda às exigências; entender o impacto de uma alta no preço do
  milho ou do farelo de soja; justificar a recomendação ao produtor.
- **Dores:** planilhas difíceis de auditar; sem como simular o efeito ao longo da lactação; desconfia de "caixas
  pretas" e quer ver o balanço de nutrientes.
- **Necessidades do produto:** preços editáveis, limites de inclusão, balanço de nutrientes visível, tabela de
  cenários exportável, aviso claro quando o modelo não consegue atender às exigências.

### 4.2 Persona secundária: Carlos, produtor de leite

- **Perfil:** gerencia a fazenda e decide a compra de insumos.
- **Objetivos:** saber quanto a dieta custa por vaca por dia e como isso afeta a margem.
- **Dores:** pouco tempo, pouca familiaridade com modelos; quer respostas diretas.
- **Necessidades do produto:** indicadores simples (margem, custo por vaca por dia), comparação de cenários.

### 4.3 Usuário de avaliação: professor de Pesquisa Operacional

Não é o usuário final, mas é quem avalia o produto. Precisa enxergar a modelagem, a integração com o simulador e a
análise de sensibilidade, e conferir que o resultado do exercício do quadro é reproduzido.

### 4.4 Perfis de acesso

O sistema roda na máquina do próprio usuário, **sem login, sem papéis e sem dados pessoais**. Todo usuário que abre
o navegador no endereço local tem as mesmas permissões. A tabela abaixo descreve o que cada perfil tende a usar.

| Perfil | Telas mais usadas | Intenção típica |
|---|---|---|
| Nutricionista | Vaca leiteira, Sensibilidade, Premissas | Formular, comparar e justificar uma ração |
| Produtor | Vaca leiteira (indicadores) | Conhecer margem e custo por vaca por dia |
| Professor | Exercício do quadro, Curva de lactação, Sensibilidade | Conferir a modelagem de PO e a integração com o RuFaS |

---

## 5. Escopo da Primeira Versão

### 5.1 Módulos entregues

| Módulo (tela) | O que entrega | Requisitos |
|---|---|---|
| Exercício do quadro | PL de dieta, preços-sombra e tabela de cenários `S1..SN` | RF-01 a RF-04 |
| Vaca leiteira (RuFaS) | Seleção de alimentos, simulação, indicadores, ração, exigências e leite diário | RF-05 a RF-13 |
| Curva de lactação | Curva de Wood por paridade com PEV, gestação e secagem | RF-14, RF-15 |
| Sensibilidade (RuFaS) | Cenários por grade ou hipercubo latino, tabela com `Res`, efeito dos fatores | RF-16 a RF-18 |
| Premissas e limites | O que o modelo assume e não faz | RF-25 |
| Instalação local | Scripts de instalação e de execução no Windows | RNF-03, RNF-11 |

### 5.2 Requisitos funcionais

**Prioridade (MoSCoW):** M = deve ter; S = deveria ter; C = poderia ter.
**Situação:** Atendido, Parcial ou Pendente.

#### 5.2.1 Exercício do quadro (programação linear)

| ID | Requisito | Prior. | Situação | Aceite |
|---|---|---|---|---|
| RF-01 | O sistema deve resolver o problema de dieta de custo mínimo com N alimentos e nutrientes com mínimo e máximo. | M | Atendido | Resultado da M1; casos inviáveis são sinalizados. |
| RF-02 | O usuário deve poder editar custo e composição dos alimentos, adicionar alimentos e editar os limites dos nutrientes. | M | Parcial | Edição e adição de alimentos funcionam; os nutrientes são fixos (carboidrato e proteína). |
| RF-03 | O sistema deve mostrar quantidade e custo por alimento, total de cada nutriente, restrição ativa e preço-sombra. | M | Atendido | Tabelas de solução e de nutrientes exibidas. |
| RF-04 | O sistema deve gerar uma tabela de cenários variando dois fatores (custos ou limites), com a coluna `Res`. | M | Atendido | 9 cenários para 3 níveis × 3 níveis, com a dieta ótima de cada um. |

#### 5.2.2 Simulação de vaca leiteira com o RuFaS

| ID | Requisito | Prior. | Situação | Aceite |
|---|---|---|---|---|
| RF-05 | O usuário deve poder buscar e selecionar alimentos da biblioteca NRC 2001 (130 itens). | M | Atendido | Busca por nome; composição resumida (PB, FDN) visível. |
| RF-06 | O usuário deve poder informar o preço (US$/kg MS) e os limites mínimo e máximo (kg MS/vaca/dia) de cada alimento. | M | Atendido | Valores propagados ao RuFaS; tetos padrão para minerais, gorduras e farinhas animais. |
| RF-07 | O usuário deve poder definir preço do leite, período simulado (1 ou 2 anos) e a redução máxima de leite tolerada. | M | Atendido | Parâmetros enviados ao simulador. |
| RF-08 | O sistema deve executar a simulação no RuFaS em segundo plano, com indicador de progresso. | M | Atendido | Barra de progresso; interface não trava. |
| RF-09 | O sistema deve exibir margem, receita, custo de alimentação, custo da ração por vaca por dia, leite por vaca e leite total. | M | Atendido | Seis indicadores no topo dos resultados. |
| RF-10 | O sistema deve exibir a ração por intervalo de 30 dias, a composição média (kg, % e US$), as exigências (NEL, proteína metabolizável, DMI) e o leite diário do rebanho. | M | Atendido | Quatro visualizações. |
| RF-11 | O sistema deve reutilizar simulações já feitas (cache) e não repetir a simulação quando só o preço do leite muda. | S | Atendido | Segunda execução idêntica retorna em segundos. |
| RF-12 | O sistema deve indicar falhas da simulação e o leite perdido por ração insuficiente, sem mascarar. | M | Atendido | Cenário falho marcado "falhou"; indicador "Leite perdido" quando há redução. |
| RF-13 | O usuário deve poder ajustar o tamanho do rebanho. | C | Pendente | O back-end aceita o parâmetro; a interface não o expõe. |

#### 5.2.3 Curva de lactação

| ID | Requisito | Prior. | Situação | Aceite |
|---|---|---|---|---|
| RF-14 | O sistema deve desenhar a curva de Wood por paridade (1ª, 2ª, 3ª ou mais) com PEV, gestação e secagem ajustáveis. | M | Atendido | Marcos e faixa de gestação desenhados; pico e produção em 305 dias por paridade. |
| RF-15 | A curva deve usar os parâmetros calibrados pela última simulação do RuFaS e indicar a origem dos parâmetros. | S | Atendido | Selo "calibrados pela simulação RuFaS" ou "de referência". |

#### 5.2.4 Análise de sensibilidade

| ID | Requisito | Prior. | Situação | Aceite |
|---|---|---|---|---|
| RF-16 | O usuário deve poder escolher fatores (preços de alimentos selecionados e preço do leite) com faixa de variação. | M | Atendido | Faixa padrão de ±50% nos alimentos e ±20% no leite. |
| RF-17 | O sistema deve gerar cenários por grade ou por hipercubo latino e informar a estimativa de simulações e de tempo. | M | Atendido | Estimativa exibida antes de rodar. |
| RF-18 | O sistema deve apresentar a tabela de cenários no formato do quadro (fatores + `Res`), a ração de cada cenário, o efeito (correlação de Spearman) de cada fator e um gráfico de margem por cenário. | M | Atendido | Tabela, gráfico de efeitos e gráfico de margem. |

#### 5.2.5 Requisitos previstos e premissas, importantes para o usuário profissional

| ID | Requisito | Prior. | Situação | Motivo |
|---|---|---|---|---|
| RF-19 | O sistema deve mostrar o **balanço nutricional** (oferta × exigência de NEL, proteína metabolizável, Ca, P, FDN) da ração obtida. | M | Pendente | A nutricionista precisa auditar a ração; hoje só as exigências são exibidas. |
| RF-20 | O sistema deve **exportar** tabela de cenários e resultados (CSV) e gerar relatório. | S | Pendente | Documentar a recomendação. |
| RF-21 | O sistema deve **salvar e carregar** configurações de cenário. | S | Pendente | Reuso entre sessões. |
| RF-22 | O sistema deve permitir **importar preços** (CSV) para cenários com cotações reais, por exemplo do CEPEA. | S | Pendente | Hoje os preços são digitados à mão e os valores iniciais são ilustrativos. |
| RF-23 | O sistema deve permitir adicionar **nutrientes** ao exercício do quadro. | C | Pendente | Generalização do exercício. |
| RF-24 | O sistema deve oferecer o padrão **NASEM 2021** como alternativa à NRC 2001. | C | Pendente | Previsto no quadro do professor; fora desta versão. |
| RF-25 | O sistema deve ter uma tela de **premissas e limites** que explique o que o modelo assume e não faz. | S | Atendido | Tela `/sobre/`, com quatro blocos (funcionamento, premissas, limites, créditos). |

O RF-19 é o único requisito de prioridade "deve ter" ainda não atendido; ele é o principal item a especificar antes
de qualquer uso profissional (seção 15).

---

## 6. Funcionalidades Fora de Escopo

### 6.1 Fora do escopo desta versão

| Item | Motivo | Quando / dependência |
|---|---|---|
| Linha de comando e relatório em PDF | Entrega combinada em duas fases: primeiro a web completa | Fase seguinte, após a conclusão da web |
| Padrão NASEM 2021 (RF-24) | A NRC 2001 é suficiente para o exercício e para a validação inicial | Depende da resposta à questão Q6 |
| Preços automáticos do CEPEA | Exige fonte de dados e licença de uso; hoje os preços são digitados | Importação por CSV (RF-22) é o passo intermediário (Q5) |
| Contas de usuário, hospedagem em nuvem, múltiplos usuários ou fazendas | O sistema é local e de um usuário | Sem previsão |
| Modificações no código do RuFaS | O RuFaS é usado como está (GPLv3, versão fixada) | Sem previsão |
| Otimizador próprio por fase da lactação | O RuFaS formula uma ração por grupo de vacas | Depende da resposta às questões Q2 e Q3 |
| Modelo próprio de resposta do leite à dieta | A premissa P1 usa só o leite simulado pelo RuFaS | Depende da resposta à questão Q3 |

### 6.2 Não objetivos

- Substituir um software comercial de formulação de rações ou produzir recomendações para uso veterinário sem revisão
  profissional.
- Servir como serviço hospedado ou exposto a redes.
- Prever preços de mercado.

### 6.3 Requisitos previstos, ainda não implementados

Os requisitos RF-13 e RF-19 a RF-24 (seção 5.2) estão dentro da intenção do produto, mas **não implementados** nesta
versão. Eles não são "fora de escopo" definitivo; dependem de decisão ou de tempo.

---

## 7. Regras de Negócio

Regras que o sistema aplica e que um revisor deve poder conferir. As marcadas **(a definir)** dependem de decisão
registrada na seção 15.

| ID | Regra | Onde se aplica |
|---|---|---|
| RN-01 | A dieta ótima é a de **menor custo** que respeita, para cada nutriente, o mínimo e o máximo informados. | Exercício do quadro |
| RN-02 | Preços são em **US$ por kg de matéria seca (MS)**; limites de inclusão são em **kg de MS por vaca por dia**. | Todas as telas |
| RN-03 | O leite de referência é o **simulado pelo RuFaS**. O otimizador ajusta a dieta e não prevê um leite próprio (P1). | Vaca, Sensibilidade |
| RN-04 | **Margem = preço do leite × leite total − custo de alimentação.** O custo é a soma das compras registradas pelo RuFaS para todo o rebanho no período (Apêndice G.3). | Vaca, Sensibilidade |
| RN-05 | Mudar o **preço do leite** não exige nova simulação; mudar **preço ou limite de alimento** exige. Simulações idênticas são reaproveitadas (cache por conteúdo do cenário). | Vaca, Sensibilidade |
| RN-06 | O padrão nutricional é a **NRC 2001**. Alimentos que só existem no NASEM (ids 301 e 302) são trocados pelos equivalentes da NRC (ids 230 e 167). | Vaca, Sensibilidade |
| RN-07 | O "arroz" do exercício corresponde ao **farelo de arroz** (id 138), único derivado de arroz na NRC 2001 (C2). | Vaca |
| RN-08 | Alimentos têm **teto de inclusão padrão** para evitar ração irreal: 0,6 kg MS/vaca/dia para minerais, 0,9 para gorduras (extrato etéreo ≥ 80%) e 1,0 para alimentos com PB ≥ 60%. O usuário pode alterar. | Vaca, Sensibilidade |
| RN-09 | Uma simulação só é **sucesso** se o RuFaS termina a tarefa sem erro. Caso contrário o cenário é marcado "falhou"; o sistema **nunca** mostra zeros no lugar de uma falha. | Vaca, Sensibilidade |
| RN-10 | Se a ração for inviável, o RuFaS **reduz o leite** em 0,25 kg por tentativa, até a redução máxima (padrão 5 kg/vaca/dia). Acima disso a simulação aborta. O leite perdido é sempre exibido. | Vaca, Sensibilidade |
| RN-11 | A simulação exige ao menos **3 alimentos** selecionados (um volumoso, um concentrado e um mineral); a interface avisa antes de enviar. | Vaca |
| RN-12 | A semente aleatória é **fixa (42)**: mesma entrada, mesmo resultado. | Vaca, Sensibilidade |
| RN-13 | No máximo **2 simulações** rodam ao mesmo tempo e **um job** por vez, por causa do consumo de memória (~1,2 GB cada). | Servidor |
| RN-14 | A sensibilidade usa faixa padrão de **±50%** nos alimentos e **±20%** no leite. Grade gera `n^k` cenários; hipercubo latino gera `n`. O **efeito** de um fator é a correlação de Spearman com a margem. A estimativa de simulações e de tempo é mostrada antes de rodar. | Sensibilidade |
| RN-15 | A curva de lactação é a de **Wood por paridade**; o próximo parto ≈ PEV + gestação e a secagem ocorre antes dele. Valores iniciais do quadro: PEV 60 dias e gestação 270 dias. | Curva de lactação |
| RN-16 | O **preço-sombra** de um nutriente é a variação do custo ótimo por unidade adicional do seu limite mínimo ativo. | Exercício do quadro |
| RN-17 | Os preços iniciais são **ilustrativos** e rotulados como tal na interface, no rodapé e no README (P4). | Todas as telas |
| RN-18 | O exercício do quadro exige **dois fatores diferentes** para gerar a tabela de cenários. | Exercício do quadro |
| RN-19 **(a definir)** | Como o leite deve responder à dieta, já que no RuFaS v1.0.6 ela é fraca (Q3). | Vaca, Sensibilidade |
| RN-20 **(a definir)** | Se a dieta deve ser otimizada por fase da lactação, e não por grupo (Q2). | Vaca |

---

## 8. Informações que o Sistema Precisa Controlar

### 8.1 Entidades de informação

| Informação | Campos principais | Origem | Onde fica | Duração |
|---|---|---|---|---|
| **Alimento da biblioteca** | id do RuFaS, nome, PB, FDN, extrato etéreo, TDN, NEL estimada, preço padrão ilustrativo, teto padrão | Metadados da NRC 2001 no RuFaS | Lida pelo servidor a partir dos arquivos do RuFaS | Somente leitura |
| **Alimento selecionado** | id, preço (US$/kg MS), mínimo e máximo (kg MS/vaca/dia) | Usuário | Navegador (`localStorage`, chave `dietopt.v1`) | Até limpar os dados do navegador |
| **Parâmetros da simulação** | preço do leite, período (1 ou 2 anos), redução máxima de leite | Usuário | Navegador (mesma chave) | Idem |
| **Exercício do quadro** | alimentos (custo, composição, máximo), nutrientes (mínimo e máximo), fatores do cenário | Usuário | Memória da página | Perdido ao recarregar |
| **Cenário de simulação** | nome, datas, semente, padrão nutricional, ração, alimentos, limites, preços, redução máxima | Montado pelo servidor a partir da entrada | `runs/<nome>/` (cópias editadas das entradas do RuFaS) | Permanece em disco |
| **Resultado da simulação** | leite diário do rebanho, ração por intervalo, exigências, compras (quantidade e custo), parâmetros de Wood | Saídas filtradas do RuFaS | `runs/_cache/<hash>.json` | Permanece em disco |
| **Avaliação econômica** | leite total, receita, custo de alimentação, custo da ração por vaca por dia, margem, ração média, redução de leite, detalhe de falha | Calculada a partir do resultado e dos preços | Resposta da API; memória da página | Recalculada quando só os preços mudam |
| **Fator de sensibilidade** | alimento ou leite, valor mínimo, valor máximo, método, número de níveis | Usuário | Memória da página | Perdido ao recarregar |
| **Linha da tabela de cenários** | valores dos fatores, margem (`Res`), ração, redução de leite | Calculada | Resposta do job; memória da página | Perdida ao recarregar |
| **Job** | id, tipo, status (`queued`, `running`, `done`, `error`), progresso, resultado, erro | Servidor | Memória do servidor | Perdido ao reiniciar o servidor |
| **Log da simulação** | saída do console do RuFaS | RuFaS | `runs/<id>/console.log` | Permanece em disco |

### 8.2 O que o sistema não guarda

- Dados pessoais, credenciais ou qualquer identificação do usuário.
- Histórico de cenários e de recomendações (RF-21, pendente).
- Preços de mercado obtidos de fontes externas (RF-22, pendente).

### 8.3 Cuidados com a integridade dos dados

- Campos numéricos vazios são tratados como inválidos e trocados por um valor padrão antes do envio.
- O RuFaS rejeita caminhos com acentos; por isso todas as entradas e saídas ficam em caminhos **relativos** à pasta do
  RuFaS (C4).
- A pasta `runs/` cresce a cada cenário novo e **não é limpa automaticamente**. Na máquina de desenvolvimento ocupava
  cerca de 48 MB.
- A chave do cache considera o conteúdo do cenário; alterar alimento, preço de alimento ou limite gera nova simulação.

---

## 9. Fluxos Principais de Uso

### 9.1 Fluxos

**F0. Instalação e primeira execução**

1. O usuário executa `scripts\setup.ps1` (instala o ambiente e as dependências, com contorno para falha de TLS do `pip`).
2. Executa `iniciar.bat`, que sobe o servidor na porta 8000 e abre o navegador.
3. O sistema responde em `http://127.0.0.1:8000`. Se a porta estiver ocupada, o servidor não sobe; encerre o processo
   anterior.

**F1. Resolver o exercício do quadro** (professor)

1. Abrir _Exercício do quadro_.
2. Conferir ou editar custos, composição e limites; adicionar alimentos, se quiser.
3. Resolver. O sistema mostra quantidade e custo por alimento, total de cada nutriente, restrições ativas e preços-sombra.
4. Em "Cenários e sensibilidade", escolher **dois fatores diferentes** (custos ou limites) e gerar a tabela `S1..SN` com a
   coluna `Res`.
5. _Saída:_ custo ótimo (US$ 15,3453 no exemplo do quadro) e tabela de cenários colorida pelo resultado.
6. _Exceção:_ problema inviável é sinalizado; fator repetido gera aviso.

**F2. Simular uma vaca leiteira** (nutricionista)

1. Abrir _Vaca leiteira (RuFaS)_.
2. Escolher um preset ("Arroz + milho + volumosos" ou "Lista ampla") ou buscar alimentos na biblioteca.
3. Ajustar preço e limites de cada alimento; definir preço do leite, período e redução máxima de leite.
4. Iniciar a simulação. Uma barra de progresso indica o andamento; a tela continua utilizável.
5. Ler os indicadores (margem, receita, custo, custo por vaca por dia, leite por vaca, leite total), a ração por
   intervalo de 30 dias, a composição média, as exigências e o leite diário.
6. Alterar só o preço do leite e recalcular: o resultado volta em segundos (cache).
7. _Exceções:_ menos de 3 alimentos selecionados (aviso antes de enviar); simulação falha (mensagem e cenário
   marcado); ração insuficiente (indicador "Leite perdido").

**F3. Analisar a sensibilidade** (nutricionista, professor)

1. Abrir _Sensibilidade (RuFaS)_.
2. Escolher os fatores (preços de alimentos selecionados e preço do leite) e a faixa de cada um.
3. Escolher o método (grade ou hipercubo latino) e o número de níveis; conferir a estimativa de simulações e de tempo.
4. Iniciar. O progresso mostra "x de y simulações do RuFaS concluídas".
5. Ler a tabela de cenários (`Arroz | Milho | … | Res`), o gráfico de efeitos (Spearman) e a margem por cenário.
6. _Exceções:_ cenário que falha aparece como "falhou" e não entra no efeito como valor válido.

**F4. Ver a curva de lactação** (professor)

1. Abrir _Curva de lactação_.
2. Ajustar PEV, gestação e dias de secagem.
3. Ler as curvas por paridade, os marcos (parto, PEV, secagem), o pico e a produção em 305 dias. O selo indica se os
   parâmetros vêm da última simulação ou são de referência.

**F5. Consultar premissas e limites** (todos)

1. Abrir _Premissas e limites_ para ler o que o modelo assume, o que não faz e como interpretar os resultados.

### 9.2 Como uma simulação roda (F2 e F3)

```
Navegador                         Servidor Python                     RuFaS
    │  POST /api/jobs/simulate        │                                  │
    │ ───────────────────────────────►│ cria job (queued)                │
    │  { id }                         │ monta runs/<nome>/ ─────────────►│ subprocesso main.py
    │ ◄───────────────────────────────│                                  │
    │  GET /api/jobs/<id>  (a cada 1,5 s)                                │
    │ ───────────────────────────────►│ running / done n de N            │
    │  status + progresso             │ lê saídas filtradas ◄────────────│
    │ ◄───────────────────────────────│ calcula margem; grava cache      │
    │  done + resultado               │                                  │
```

### 9.3 Telas e princípios de interface

A aplicação tem **cinco telas**, acessadas por uma barra lateral (grupo _Análise_ com as quatro primeiras e grupo
_Projeto_ com a quinta), que seguem o raciocínio do quadro do professor. O detalhamento visual está em
[DESIGN.md](DESIGN.md).

1. **Exercício do quadro:** tabelas editáveis de alimentos e nutrientes, botão "Resolver", solução ótima com
   preços-sombra e gráfico de barras, e a seção "Cenários e sensibilidade" com a tabela `S1..SN` colorida pelo
   resultado.
2. **Vaca leiteira (RuFaS):** painel lateral com preço do leite, período, redução máxima de leite, presets
   ("Arroz + milho + volumosos" e "Lista ampla"), busca de alimentos e lista dos selecionados com preço e limites.
   À direita, indicadores, ração por intervalo (barras empilhadas), composição média, exigências e leite diário.
3. **Curva de lactação:** curvas por paridade com marcos (PEV, secagem, parto) e faixa de gestação.
4. **Sensibilidade (RuFaS):** escolha dos fatores com faixa, método (grade ou hipercubo latino), número de níveis,
   estimativa de simulações e tempo; resultado com tabela de cenários, gráfico de efeitos e margem por cenário.
5. **Premissas e limites:** o que o modelo assume, o que não faz e como ler os resultados.

**Princípios de interface:** mostrar sempre a unidade (US$/kg MS, kg MS/vaca/dia); destacar a margem; tornar visível
tudo o que o modelo alterou por conta própria (por exemplo, leite perdido); preços iniciais rotulados como
ilustrativos.

---

## 10. Histórias de Usuário

| ID | Como... | Quero... | Para... | Aceite |
|---|---|---|---|---|
| HU1 | professor | resolver o exercício do quadro e ver a tabela de cenários | verificar a modelagem de PO | Resultado igual ao da M1; tabela com colunas de fatores e `Res` |
| HU2 | nutricionista | escolher os alimentos disponíveis na fazenda e informar seus preços | formular uma dieta realista | Busca na biblioteca NRC; preço por alimento editável |
| HU3 | nutricionista | limitar a quantidade de cada alimento | evitar rações impraticáveis | Limites em kg de matéria seca por vaca por dia respeitados pelo otimizador |
| HU4 | nutricionista | simular com o RuFaS e ver ração, custo, leite e margem | avaliar a dieta ao longo de um ano | KPIs, ração por intervalo de 30 dias e leite diário exibidos |
| HU5 | nutricionista | variar preços de alimentos e do leite | saber a que a margem é mais sensível | Tabela de cenários e efeito de cada fator sobre a margem |
| HU6 | nutricionista | saber quando a ração não atende às exigências | confiar no resultado | Falha explícita ou "leite perdido" mostrado, nunca zero silencioso |
| HU7 | produtor | ver a margem e o custo por vaca por dia em destaque | decidir rápido | Indicadores principais no topo da tela de resultados |
| HU8 | professor | ver a curva de lactação com PEV e gestação | conferir o gráfico pedido | Curva de Wood por paridade com marcos ajustáveis |
| HU9 | nutricionista | guardar e exportar cenários e resultados | documentar a recomendação | **Pendente** (RF-20 e RF-21) |
| HU10 | nutricionista | ver o balanço entre o que a ração oferece e o que a vaca exige | auditar a ração | **Pendente** (RF-19) |
| HU11 | nutricionista | importar cotações reais de uma planilha | usar preços de mercado sem digitar | **Pendente** (RF-22) |

---

## 11. Critérios de Aceitação

### 11.1 Critérios de aceite do produto (versão web)

O produto é aceito quando:

1. O exercício do quadro retorna US$ 15,35 e as quantidades de 4,473 kg de arroz e 3,873 kg de milho (M1).
2. Uma simulação de vaca leiteira com o preset padrão termina em até 60 s e exibe os seis indicadores (RF-09).
3. Uma sensibilidade com dois fatores de alimento e o preço do leite gera a tabela de cenários com coluna `Res`
   (RF-18).
4. Nenhum cenário falho aparece como valor válido (RF-12).
5. A curva de lactação mostra PEV, secagem e parto ajustáveis (RF-14).
6. A suíte automatizada passa (M5).

### 11.2 Critérios por história de usuário

Formato _Dado / Quando / Então_. Apenas as histórias já atendidas.

| História | Critério |
|---|---|
| HU1 | **Dado** os valores do quadro, **quando** o usuário resolve, **então** o custo é US$ 15,3453, o arroz é 4,473 kg e o milho é 3,873 kg. **Quando** gera cenários com dois fatores, **então** a tabela traz 9 linhas (3 × 3) com `Res`. |
| HU2 | **Dado** a biblioteca NRC, **quando** o usuário busca por nome e seleciona um alimento, **então** ele entra na lista com preço editável e composição resumida. |
| HU3 | **Dado** um limite máximo para um alimento, **quando** a simulação termina, **então** a ração média desse alimento não o ultrapassa. |
| HU4 | **Dado** o preset padrão, **quando** o usuário simula 1 ano, **então** vê seis indicadores, a ração por intervalo de 30 dias e o leite diário, em até 60 s. |
| HU5 | **Dado** fatores com faixa, **quando** a análise termina, **então** a tabela traz um cenário por combinação, o efeito de cada fator e a margem por cenário. |
| HU6 | **Dado** uma ração inviável, **quando** a simulação termina, **então** o indicador "Leite perdido" aparece; **dado** uma simulação que aborta, **então** o cenário é marcado "falhou" e nenhum valor zero é mostrado como resultado. |
| HU7 | **Dado** um resultado pronto, **quando** a tela carrega, **então** margem e custo por vaca por dia ficam no topo. |
| HU8 | **Dado** PEV 60 e gestação 270, **quando** o usuário abre a curva, **então** vê o marco do PEV, a faixa da gestação e o pico por paridade; **quando** altera o PEV, **então** os marcos se movem. |

### 11.3 Estratégia de teste

| Nível | Cobertura | Situação |
|---|---|---|
| Unitário | PL (ótimo, preço-sombra, inviabilidade), amostragem (grade, hipercubo latino, Spearman), troca de ids NASEM→NRC, tetos padrão, resumo de falha, chave de cache | 10 testes passando |
| Integração | Execução real do RuFaS por cenário, leitura de saídas, cache, falha e degradação com perda de leite | Executado manualmente; **sem teste automatizado** |
| Interface | Uso das cinco telas no navegador, nos temas claro e escuro | Executado manualmente; **sem teste automatizado** |
| Validação científica | Comparação com formulador de referência ou tabelas da NRC | **Pendente** (M6, RNF-10) |

---

## 12. Consultas, Relatórios e Indicadores

### 12.1 Indicadores

| Indicador | Definição | Unidade | Onde aparece |
|---|---|---|---|
| Margem sobre custo de alimentação | Receita do leite − custo de alimentação (RN-04) | US$ no período | Vaca, Sensibilidade (`Res`) |
| Receita do leite | Preço do leite × leite total | US$ | Vaca |
| Custo de alimentação | Compras de alimentos do rebanho no período | US$ | Vaca |
| Custo da ração por vaca por dia | Custo da ração das vacas em lactação | US$/vaca/dia | Vaca |
| Leite por vaca | Leite médio por vaca em lactação | kg/vaca/dia | Vaca |
| Leite total | Soma do leite do rebanho no período | kg | Vaca |
| Leite perdido | Redução média de leite imposta pelo RuFaS por falta de alimento | kg/vaca/dia | Vaca, Sensibilidade |
| Custo ótimo e preços-sombra | Solução do PL e variação do custo por unidade do limite ativo | US$ e US$/kg | Exercício do quadro |
| Efeito do fator | Correlação de Spearman entre o fator e a margem (−1 a +1) | adimensional | Sensibilidade |
| Pico e produção em 305 dias | Máximo da curva de Wood e leite acumulado em 305 dias, por paridade | kg/dia e kg | Curva de lactação |

### 12.2 Consultas que o usuário consegue fazer

| Pergunta | Onde responder |
|---|---|
| Qual a dieta de custo mínimo para estes alimentos e limites? | Exercício do quadro; Vaca leiteira |
| Quanto custa a ração por vaca por dia e qual a margem? | Vaca leiteira |
| Quais alimentos a ração usa em cada intervalo de 30 dias? | Vaca leiteira (ração por intervalo) |
| A ração atende às exigências de energia, proteína e consumo? | Vaca leiteira (exigências); balanço completo pendente (RF-19) |
| A que preço a margem é mais sensível? | Sensibilidade (efeito dos fatores) |
| Em que preço o ótimo muda de ração? | Exercício do quadro e Sensibilidade (tabela de cenários) |
| Como é a lactação de cada paridade e quando seca? | Curva de lactação |

### 12.3 Relatórios e visualizações

| Visualização | Tela | Tipo |
|---|---|---|
| Solução do PL, nutrientes e preços-sombra | Exercício do quadro | Tabelas e gráfico de barras |
| Tabela de cenários `S1..SN` colorida pelo resultado | Exercício do quadro; Sensibilidade | Tabela |
| Ração por intervalo | Vaca leiteira | Barras empilhadas |
| Composição média da ração (kg, % e US$) | Vaca leiteira | Tabela |
| Exigências (NEL, proteína metabolizável, DMI) | Vaca leiteira | Gráfico |
| Leite diário do rebanho | Vaca leiteira | Linha |
| Curvas de Wood com marcos | Curva de lactação | Linhas com faixa |
| Efeito dos fatores e margem por cenário | Sensibilidade | Gráficos de barras |

### 12.4 Exportação

**Não há exportação nesta versão** (RF-20, pendente). A forma atual de documentar um resultado é a captura de tela.

### 12.5 Resultados medidos

| Cenário | Resultado |
|---|---|
| Quadro do professor | Custo US$ 15,3453; arroz 4,473 kg; milho 3,873 kg; preços-sombra US$ 0,57/kg (carboidrato) e US$ 13,22/kg (proteína) |
| Simulação, ração formulada pelo RuFaS | Margem ~US$ 385 mil; custo da ração US$ 4,02 por vaca por dia; leite de 40,3 kg por vaca por dia |
| Efeito do preço do farelo de arroz (US$ 0,375 → US$ 0,125 por kg MS; milho a US$ 0,14 e leite a US$ 0,54) | Uso passa de 0,4 para 11,2 kg por vaca por dia; margem sobe de US$ 513.574 para US$ 519.929 |
| Sensibilidade (arroz × milho × preço do leite, 8 cenários, 4 simulações) | ρ de Spearman com a margem: leite +0,87; arroz −0,44; milho −0,22. O preço do milho muda pouco o resultado porque a ração ótima quase não usa milho em grão. |
| Cenário que antes abortava (milho a US$ 0,42 e farelo de arroz a US$ 0,375) | Conclui com leite perdido de 0,17 kg/vaca/dia |

Os valores monetários dependem dos preços ilustrativos e servem para demonstrar o comportamento, não para recomendar
uma dieta.

---

## 13. Requisitos Não Funcionais

| ID | Categoria | Requisito | Situação |
|---|---|---|---|
| RNF-01 | Desempenho | Uma simulação de 1 ano com 100 vacas deve levar ≤ 60 s; uma sensibilidade de 4 simulações ≤ 3 min. | Atendido (30 a 37 s; ~66 s) |
| RNF-02 | Recursos | Cada simulação do RuFaS consome cerca de 1,2 GB de RAM (observado numa simulação de 7 anos). O sistema deve rodar no máximo 2 simulações simultâneas e um job de cada vez. | Atendido |
| RNF-03 | Portabilidade | Windows 10/11, Python 3.12 ou 3.13 (exigência do RuFaS). Depois da instalação, funcionar sem internet. | Atendido |
| RNF-04 | Usabilidade | Interface em português do Brasil; tema claro e escuro automático; uma simulação iniciável com poucos cliques a partir de uma configuração padrão. | Atendido |
| RNF-05 | Transparência | Falhas devem ser explícitas; o log de cada simulação deve ficar disponível em disco (`runs/<id>/console.log`). | Atendido |
| RNF-06 | Reprodutibilidade | Versão do RuFaS fixada (v1.0.6), dependências fixadas e semente aleatória fixa (42). Mesma entrada, mesmo resultado. | Atendido |
| RNF-07 | Segurança | O servidor escuta apenas em `127.0.0.1`, sem autenticação e sem dados pessoais. Não deve ser exposto a redes. | Atendido |
| RNF-08 | Manutenibilidade | Código modular, RuFaS sem modificação, testes automatizados cobrindo PL, amostragem, adaptador e cache. | Atendido (10 testes) |
| RNF-09 | Legal | O RuFaS é GPLv3. A distribuição conjunta deve respeitar a licença e preservar a atribuição. | Atendido (RuFaS não modificado) |
| RNF-10 | Validade científica | Os resultados devem ser comparados com uma referência profissional antes de qualquer uso real. Premissas e limites do modelo devem estar documentados. | **Pendente** (limites documentados no README; comparação não feita) |
| RNF-11 | Instalação | O ambiente deve ser reproduzível por script, mesmo onde o `pip` falha por TLS. | Atendido (`scripts/setup.ps1` com contorno via `curl`) |

---

## 14. Limitações da Primeira Versão

Limitações conhecidas, para que ninguém leia mais certeza do que o sistema entrega. As quatro primeiras afetam a
**interpretação** dos resultados; as demais, o **uso**.

| ID | Limitação | Efeito | Relacionado |
|---|---|---|---|
| L1 | No RuFaS v1.0.6 o leite quase não responde à dieta: só cai quando a ração não atende às exigências. | A margem varia sobretudo pelo custo da dieta; o trade-off "mais leite × menor custo" é fraco. | P2, R1, Q3 |
| L2 | O RuFaS formula uma ração para o grupo de vacas em lactação, não por fase (recém-parida, pico, fim). | A vaca recém-parida aparece na curva, mas não recebe dieta própria. | Q2, RN-20 |
| L3 | Os preços iniciais são ilustrativos e não vêm do CEPEA. | Valores em dólar demonstram comportamento; não servem para decidir compras. | P4, RF-22, M7 |
| L4 | O resultado não foi comparado com uma referência profissional. | Não se deve usar a ração para alimentar animais sem revisão. | M6, RNF-10, R9 |
| L5 | Não há balanço de nutrientes (oferta × exigência) da ração obtida. | Só as exigências são exibidas; o profissional não audita a ração por completo. | RF-19 |
| L6 | Não há exportação nem salvamento de cenários. | Resultados só podem ser registrados por captura de tela; os fatores se perdem ao recarregar. | RF-20, RF-21 |
| L7 | Só a NRC 2001 está disponível. | O NASEM 2021, citado no quadro, não é oferecido. | RF-24, Q6 |
| L8 | A biblioteca NRC 2001 só tem farelo de arroz; não há arroz em grão. | O "arroz" do exercício é representado pelo farelo de arroz. | C2, RN-07 |
| L9 | O tamanho do rebanho não é ajustável na interface. | Usa-se o rebanho padrão do RuFaS. | RF-13 |
| L10 | O exercício do quadro tem apenas dois nutrientes (carboidrato e proteína). | Não generaliza para energia, minerais e fibra. | RF-02, RF-23 |
| L11 | Cada simulação consome ~1,2 GB de RAM e leva 30 a 37 s; só um job roda por vez. | Análises grandes demoram; máquinas com pouca memória livre podem falhar. | RNF-02, R5 |
| L12 | Testado apenas no Windows e em um computador; sem autenticação, uso local de um usuário. | Não foi verificado em outros sistemas nem exposto a rede. | RNF-03, RNF-07 |
| L13 | Jobs ficam na memória do servidor; reiniciá-lo perde jobs em andamento e resultados não exportados. Os resultados em disco permanecem no cache. | Reiniciar durante uma análise obriga a rodar de novo (as simulações prontas voltam do cache). | Seção 8 |
| L14 | Não há testes automatizados de integração com o RuFaS nem de interface; acessibilidade não foi auditada com leitor de tela; o contraste das cores dos gráficos não foi medido. | Regressões nessas camadas só são detectadas manualmente. | Seção 11.3, DESIGN |
| L15 | A pasta `runs/` não é limpa automaticamente. | Ocupa disco com o uso prolongado. | Seção 8.3 |

---

## 15. Pontos Pendentes Antes do FSD

O **FSD** (_Functional Specification Document_, documento de especificação funcional) detalhará telas, campos,
mensagens, formatos e comportamentos do que este PRD define. Os pontos abaixo precisam ser resolvidos, ou assumidos
explicitamente, antes de escrevê-lo.

### 15.1 Decisões que dependem do professor ou da equipe

A coluna "Proposta" é o que o autor assumiria se não houver resposta; **precisa ser confirmada**.

| # | Questão | Para quem | Impacto | Bloqueia o FSD? | Proposta (a confirmar) |
|---|---|---|---|---|---|
| Q1 | PEV significa _período de espera voluntário_? Os 270 d representam a gestação a partir do PEV? | Professor | Gráfico e marcos (RF-14) | Não (parâmetros editáveis) | Manter a leitura atual |
| Q2 | O professor espera uma dieta **por fase da lactação** (recém-parida, pico, fim)? Hoje o RuFaS formula uma ração por grupo. | Professor | Pode exigir um otimizador próprio por dia em lactação | **Sim** | Manter a ração por grupo e registrar como limitação (L2) |
| Q3 | Como a resposta do leite à dieta deve ser tratada, já que no RuFaS ela é fraca (R1)? | Professor | Define o trade-off central do produto | **Sim** | Manter o leite do RuFaS (P1) |
| Q4 | Qual referência profissional usar para validar a ração (M6)? | Professor | Aceite científico | Não | Comparar com as tabelas da NRC 2001 |
| Q5 | Preços do CEPEA serão fornecidos? Em que moeda e unidade? | Equipe | RF-22, M7 | Não | Importação por CSV em US$/kg MS |
| Q6 | O NASEM 2021 é requisito de entrega? | Professor | RF-24 | Não | Fora desta versão |
| Q7 | Qual o prazo de entrega e o formato de apresentação? | Equipe | Prioridade dos itens pendentes | Não | Sem proposta |

### 15.2 Lacunas do próprio documento

- Autor(es), nome do professor e instituição estão em branco (cabeçalho).
- O prazo (Q7) define quais requisitos pendentes entram antes da entrega.
- Confirmar com o professor se a numeração do PRD (nota após o sumário) atende ao modelo esperado.

### 15.3 Requisitos a especificar no FSD

| ID | Requisito | O que o FSD precisa definir |
|---|---|---|
| RF-19 | Balanço nutricional | Quais nutrientes (NEL, PM, Ca, P, FDN), onde a oferta é lida no RuFaS, forma de exibir déficit e excesso |
| RF-20 | Exportação | Formato do CSV (colunas, separador, unidades), conteúdo e layout do relatório |
| RF-21 | Salvar e carregar | Onde guardar (arquivo local ou navegador), nome, versão do formato |
| RF-22 | Importar preços | Layout do CSV, mapeamento de nomes para ids do RuFaS, tratamento de itens sem correspondência |
| RF-13 | Tamanho do rebanho | Limites mínimo e máximo, efeito no tempo e na memória |
| RF-23, RF-24 | Mais nutrientes, NASEM | Só se o professor exigir |

### 15.4 Verificações técnicas ainda em aberto

- Medir o contraste das cores de gráficos e fazer auditoria de acessibilidade.
- Testar em outro computador e em tela de celular real (a conferência até agora foi em janela redimensionada).
- Decidir se testes automatizados de integração e de interface entram antes da entrega.

---

## 16. Resumo Final do PRD

**O quê.** Aplicação web local, em português, que formula a dieta de custo mínimo de vacas leiteiras e mede a margem
sobre o custo de alimentação ao longo da lactação, chamando o RuFaS v1.0.6 (NRC 2001) como simulador, sem modificá-lo.

**Para quem.** Nutricionista e produtor de leite; avaliada pelo professor de Pesquisa Operacional.

**O que já faz.** Cinco telas: reproduz o exercício do quadro (US$ 15,3453; 4,473 kg de arroz e 3,873 kg de milho),
simula a vaca com ração, custo e margem, desenha a curva de lactação com PEV e gestação, roda análise de
sensibilidade com tabela `S1..SN` e `Res`, e explica premissas e limites. Falhas e leite perdido ficam visíveis.

**Estado.** 17 dos 25 requisitos funcionais atendidos, 1 parcial (RF-02) e 7 pendentes (RF-13 e RF-19 a RF-24); dos 11
requisitos não funcionais, 10 atendidos e 1 pendente (validade científica, RNF-10). Dez testes automatizados passam.

**Principais limites.** Preços ilustrativos; o leite quase não responde à dieta no RuFaS v1.0.6; ração por grupo, não
por fase; sem balanço de nutrientes, exportação nem NASEM; sem validação contra referência profissional.

**Próximos passos.**

1. Obter as respostas de Q2 e Q3, que bloqueiam o FSD, e as demais questões da seção 15.
2. Especificar e implementar o balanço nutricional (RF-19), o item de maior valor para o usuário profissional.
3. Definir a referência de validação (Q4) e medir o desvio (M6).
4. Escrever o FSD; depois, a versão em linha de comando com relatório.

---

## Apêndice A: Premissas, restrições e dependências

### Premissas

- **P1.** O leite simulado pelo RuFaS é a referência do sistema; o otimizador ajusta a dieta e **não** prevê um leite
  próprio.
- **P2.** No RuFaS v1.0.6 o leite segue a curva de Wood e só cai quando a ração não atende às exigências (redução de
  0,25 kg por tentativa, até o limite configurado). A margem varia, portanto, principalmente com o custo da dieta.
- **P3.** A gestação de 270 dias e o PEV de 60 dias são os valores do quadro. A leitura de PEV como _período de
  espera voluntário_ é uma interpretação do autor (ver Q1, seção 15).
- **P4.** Preços iniciais (US$/kg MS) são **ilustrativos**, não cotações.
- **P5.** Limites de inclusão são em kg de matéria seca por vaca por dia, que é a unidade usada pelo RuFaS.

### Restrições

- **C1.** Python 3.12 ou 3.13 (o RuFaS exige `>=3.12, <3.14`).
- **C2.** A biblioteca NRC 2001 só contém **farelo de arroz**; o "arroz" do exercício vira farelo de arroz (id 138).
- **C3.** Memória: cada simulação usa cerca de 1,2 GB; a máquina de desenvolvimento tinha 15,8 GB de RAM com ~2,5 GB
  livres no momento dos testes.
- **C4.** O RuFaS rejeita caminhos com caracteres acentuados; o sistema usa caminhos relativos.
- **C5.** O RuFaS v1.0.6 exige todas as dependências de desenvolvimento do seu `pyproject.toml`.

### Dependências

| Dependência | Versão | Uso |
|---|---|---|
| RuFaS | v1.0.6 | Simulador (GPLv3) |
| Python | 3.12.10 | Ambiente de execução |
| NumPy / SciPy / pandas | 2.2.0 / 1.16.2 / 2.3.2 | Cálculo, PL e leitura de dados |
| Next.js / React / Recharts | 16.2.6 / 19.2.4 / 3.8.0 | Interface e gráficos (já compilados em `frontend/`; Node 20.9+ só é necessário para alterar a interface) |

## Apêndice B: Riscos e mitigações

| ID | Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|---|
| R1 | O leite quase não responde à dieta no RuFaS v1.0.6, o que enfraquece o trade-off "mais leite × menor custo". | Alta | Alto | Declarar na documentação e na interface; mostrar "leite perdido"; discutir com o professor a opção de um modelo de resposta do leite próprio. |
| R2 | O otimizador do RuFaS (SLSQP) não converge para certos preços e a simulação aborta. | Média | Médio | Falha explícita no cenário; folga de redução de leite (padrão 5 kg/vaca/dia) para degradar em vez de abortar. |
| R3 | Preços ilustrativos serem lidos como cotações reais. | Média | Alto | Rótulo "ilustrativo" na interface, no rodapé e no README; importação de preços (RF-22). |
| R4 | A ração ótima ser irreal (por exemplo, mineral como enchimento). | Média | Alto | Tetos padrão por tipo de alimento; balanço nutricional (RF-19) e comparação com uma referência (RNF-10). |
| R5 | Tempo e memória limitam análises grandes. | Média | Médio | Cache, no máximo 2 simulações em paralelo, estimativa antes de rodar. |
| R6 | Interpretação errada do gráfico do quadro (PEV, 270 d). | Média | Médio | Parâmetros editáveis; confirmação com o professor. |
| R7 | Mudanças em versões futuras do RuFaS quebrarem a integração (a branch `dev` já difere da v1.0.6). | Média | Médio | Versão fixada; adaptador isolado em um módulo. |
| R8 | Falha de rede (TLS) impedir a instalação do ambiente. | Média | Baixo | Script de instalação com contorno via `curl`. |
| R9 | Uso do sistema como se fosse recomendação profissional sem validação. | Baixa | Alto | Aviso de uso e plano de validação (seção 11.3). |

## Apêndice C: Visão técnica resumida

```
 Navegador (Next.js exportado como site estático: React, Tailwind, shadcn/ui, Recharts)
        │  HTTP/JSON (127.0.0.1:8000)
        ▼
 Servidor Python (biblioteca padrão) ── Jobs em segundo plano
        │
        ├── diet_lp.py        PL da dieta (SciPy / HiGHS)
        ├── sensitivity.py    grade, hipercubo latino, Spearman
        ├── scenarios.py      economia, margem, cache de simulações
        └── rufas_adapter.py  monta entradas ─► RuFaS v1.0.6 (subprocesso) ─► lê saídas filtradas
```

| Componente | Responsabilidade |
|---|---|
| `backend/dietopt/diet_lp.py` | Formulação e solução do PL; preços-sombra. |
| `backend/dietopt/rufas_adapter.py` | Cenário → arquivos de entrada do RuFaS; execução; detecção de falha. |
| `backend/dietopt/rufas_results.py` | Leitura das variáveis de saída (leite, ração, exigências, compras, parâmetros de Wood). |
| `backend/dietopt/scenarios.py` | Preços, receita, custo, margem; cache por conteúdo do cenário. |
| `backend/dietopt/sensitivity.py` | Geração de cenários e efeito dos fatores. |
| `backend/dietopt/lactation.py` | Curva de Wood e marcos reprodutivos. |
| `backend/dietopt/feeds.py` | Biblioteca NRC 2001 e tetos padrão por tipo de alimento. |
| `backend/dietopt/jobs.py`, `server.py` | Fila de jobs e API HTTP. |
| `web/` e `frontend/` | Interface em cinco telas. As fontes (Next.js) ficam em `web/`; `scripts/build-web.ps1` compila e publica o site estático em `frontend/`, servido pelo servidor Python. Ver [DESIGN.md](DESIGN.md). |

## Apêndice D: Rastreabilidade com o pedido do professor

| Elemento do quadro / pedido | Requisito no produto | Situação |
|---|---|---|
| Modelagem da dieta (arroz, milho, carboidrato, proteína, mínimos e máximos) | RF-01 a RF-03 | Atendido |
| Valor do kg de arroz e de milho | RF-06 | Atendido |
| Caixa **Simulador** (RuFaS) | RF-05 a RF-10 | Atendido |
| Caixa **Otimizador** alimentada pelo simulador | RF-06, RF-08 e RF-09 (otimizador do RuFaS com preços e limites do usuário) | Atendido |
| **Análise de sensibilidade** S1…SN | RF-16 a RF-18 | Atendido |
| Tabela de **Cenários** (`Arroz`, `Milho`, `Mín`, `Máx`, …, `Res`) | RF-04 e RF-18 | Atendido |
| Gráfico de produção × dias, com **PEV** em 60 d e faixa de 270 d | RF-14 e RF-15 | Atendido (interpretação a confirmar, Q1) |
| **NRC (2001)** | Biblioteca e exigências NRC | Atendido |
| **NASEM (2021)** | RF-24 | Pendente (fora desta versão) |
| **CEPEA** (preços) | RF-22 | Pendente (preços digitados à mão) |
| Vaca recém-parida em consideração | Curva de lactação e ração por intervalo desde o dia 0 da simulação | Parcial: a curva é exibida, mas a dieta não é otimizada por fase da lactação (o RuFaS formula uma ração para o grupo de vacas em lactação) |

## Apêndice E: Glossário

| Termo | Significado |
|---|---|
| **RuFaS** | _Ruminant Farm Systems_: modelo de simulação de fazenda leiteira, de código aberto. |
| **NRC (2001)** | _Nutrient Requirements of Dairy Cattle_, 7ª edição revisada: exigências nutricionais de vacas leiteiras. |
| **NASEM (2021)** | Edição mais recente do padrão de exigências; sucede a NRC 2001. |
| **PRD** | Documento de Requisitos do Produto (este documento). |
| **FSD** | _Functional Specification Document_: especificação funcional detalhada, posterior ao PRD. |
| **MS** | Matéria seca. |
| **DMI** | _Dry matter intake_: consumo de matéria seca. |
| **NEL** | Energia líquida de lactação (Mcal/dia). |
| **PM / MP** | Proteína metabolizável (g/dia). |
| **PB** | Proteína bruta. |
| **FDN / NDF** | Fibra em detergente neutro. |
| **PEV** | Período de espera voluntário: dias após o parto antes da primeira inseminação (interpretação, ver Q1). |
| **Curva de Wood** | Modelo da produção de leite por dia em lactação: `y(t) = l · t^m · e^(−n·t)`. |
| **PL** | Programação linear. |
| **Preço-sombra** | Variação do custo ótimo por unidade a mais de um limite ativo. |
| **Margem sobre custo de alimentação** | Receita do leite menos custo da alimentação. |
| **Hipercubo latino** | Amostragem que cobre cada faixa de cada fator de forma equilibrada. |
| **Job** | Tarefa em segundo plano (simulação ou sensibilidade) acompanhada pela interface. |
| **CEPEA** | Centro de Estudos Avançados em Economia Aplicada (ESALQ/USP): fonte de indicadores de preços agropecuários. |

## Apêndice F: Referências

1. National Research Council. _Nutrient Requirements of Dairy Cattle_, 7ª ed. revisada. Washington, DC: National
   Academies Press, 2001. (Eq. 1-2 de DMI; Eq. 2-3 de NEL; Tabela 15-1 de composição de alimentos.)
2. RuFaS: _Ruminant Farm Systems_. https://github.com/RuminantFarmSystems/RuFaS (v1.0.6, GPLv3).
3. Wood, P. D. P. Algebraic model of the lactation curve in cattle. _Nature_, 216, 164–165, 1967.
4. Virtanen, P. et al. SciPy 1.0. _Nature Methods_, 17, 261–272, 2020. (HiGHS é o solucionador de PL usado.)
5. Material de aula de Pesquisa Operacional (quadro com o problema da dieta e o diagrama
   simulador/otimizador/sensibilidade).

## Apêndice G: Formulação matemática

### G.1 Problema da dieta (exercício do quadro)

Sejam `x_i` a quantidade (kg/dia) do alimento `i`, `c_i` o custo (US$/kg) e `q_ij` a quantidade (kg) do nutriente
`j` em 1 kg do alimento `i`.

```
minimizar    Σ_i c_i · x_i
sujeito a    mín_j ≤ Σ_i q_ij · x_i ≤ máx_j      para cada nutriente j
             x_i ≥ 0
```

No exercício, `c = (1,50; 2,23)`, carboidrato `q = (0,77; 0,66)` com faixa `[6,0; 9,5]` e proteína
`q = (0,08; 0,14)` com faixa `[0,9; 1,6]`. Solução ótima: `x = (4,473; 3,873)`, custo `15,3453`. Ficam ativos os
mínimos de carboidrato e de proteína.

### G.2 Dieta da vaca leiteira (otimizador do RuFaS)

O RuFaS formula a ração do grupo de vacas em lactação resolvendo um problema não linear (SLSQP):

```
minimizar    Σ_i p_i · x_i                      (p_i = preço do alimento i, US$/kg MS)
sujeito a    oferta de NEL, PM, Ca, P  ≥  exigência (NRC 2001)
             limites de FDN, FDN de forragem e gordura
             consumo de MS dentro da faixa do DMI estimado
             l_i ≤ x_i ≤ u_i                    (limites de inclusão, kg MS/vaca/dia)
```

Se o problema é inviável, o RuFaS reduz o leite em 0,25 kg por tentativa até `milk_reduction_maximum`; acima disso, a
simulação aborta.

### G.3 Margem sobre o custo de alimentação

```
Margem = P_leite · Σ_dias leite_dia  −  Σ_alimentos preço_a · quantidade_comprada_a
```

onde `P_leite` é o preço do leite (US$/kg; padrão ilustrativo de 0,45) e a quantidade comprada é a registrada pelo
RuFaS para todo o rebanho no período.

### G.4 Curva de lactação

```
y(t) = l · t^m · e^(−n·t)            t = dias em lactação
```

`l`, `m` e `n` vêm do RuFaS por paridade (1ª, 2ª, 3ª ou mais), já ajustados à fazenda simulada. Marcos:
`parto seguinte ≈ PEV + gestação`; `secagem ≈ parto seguinte − dias de secagem`.

### G.5 Energia dos alimentos

Para a biblioteca de alimentos, a NEL de cada alimento é estimada por `NEL (Mcal/kg MS) = 0,0245 · TDN(%) − 0,12`
(NRC 2001, Eq. 2-3). Essa estimativa é só informativa na interface; a oferta de energia na simulação é calculada pelo
próprio RuFaS.

### G.6 Sensibilidade

- **Grade:** `n` níveis igualmente espaçados por fator; total de cenários = `n^k` para `k` fatores.
- **Hipercubo latino:** `n` amostras, cada fator dividido em `n` estratos com uma amostra por estrato.
- **Efeito de um fator:** correlação de postos de Spearman entre o fator e a margem (−1 a +1).
- Mudar o **preço do leite** não exige nova simulação; só os preços dos alimentos exigem.

## Apêndice H: Histórico de revisões

| Versão | Data | Autor | Mudanças |
|---|---|---|---|
| 0.1 | 12/10/2026 | _[a preencher]_ | Primeira versão, cobrindo a aplicação web. |
| 0.2 | 12/10/2026 | _[a preencher]_ | Interface migrada para Next.js e shadcn/ui (template AdminCN); incluído RF-25; referência ao DESIGN.md. |
| 0.3 | 12/10/2026 | _[a preencher]_ | Documento reorganizado na estrutura padrão de 16 seções. Novas: regras de negócio (7), informações controladas (8), fluxos de uso (9), critérios por história (11.2), consultas, relatórios e indicadores (12), limitações (14), pontos pendentes antes do FSD (15) e resumo final (16). Seções existentes refinadas e reposicionadas; riscos, premissas, glossário, referências e matemática passaram a apêndices. |

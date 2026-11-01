# Perguntas para o professor

**Versão:** 0.1 · **Data:** 01/11/2026 · **Projeto:** Dieta Ótima com RuFaS (Pesquisa Operacional)
**Origem das perguntas:** [PRD](PRD.md), seção 15 (Q1 a Q11) · [LINEARIZACAO](LINEARIZACAO.md), seção 8 (L-Q1 a L-Q7) ·
[FSD](FSD.md), Anexos A e B.

## Como usar este documento

São decisões que **só o professor ou a equipe pode tomar** e que travam partes da especificação ou da implementação.
Cada pergunta traz o contexto, uma **proposta** (o que faremos se não houver outra orientação) e o que ela **destrava**.
Basta responder **"de acordo"** ou indicar outra opção. O professor participou do desenvolvimento do RuFaS; por isso o
grupo C traz perguntas sobre o comportamento do próprio RuFaS.

A coluna **Resposta** fica em branco para o preenchimento. Prioridade das respostas: **A** (bloqueia especificação),
**B** (bloqueia implementação do módulo ampliado), **C** (melhora a fidelidade), **D** (organização).

## Resumo

| # | Grupo | Pergunta (curta) | Prioridade |
|---|---|---|---|
| P1 | Escopo | Dieta por fase da lactação | A |
| P2 | Escopo | Resposta do leite à dieta | A |
| P3 | Escopo | Prioridade e fases do módulo ampliado | A |
| P4 | Módulo ampliado | Tolerâncias de convergência e de erro | B |
| P5 | Módulo ampliado | Critério de ordenação das dietas | B |
| P6 | Módulo ampliado | Metano e nitrogênio urinário de uma vaca isolada | B |
| P7 | Módulo ampliado | Vaca recém-parida (início de lactação) | B |
| P8 | RuFaS | Amido total em kg na digestibilidade da FDN | C |
| P9 | RuFaS | Oferta de proteína do NRC no modo NASEM | C |
| P10 | RuFaS | Limite de consumo de +30% sobre o estimado | C |
| P11 | RuFaS | Fósforo de mantença da vaca seca | C |
| P12 | RuFaS | Reprodutibilidade do otimizador do RuFaS | C |
| P13 | NASEM e alimentos | O NASEM 2021 é requisito de entrega? | B |
| P14 | NASEM e alimentos | Arroz em grão | B |
| P15 | Preços | Indicadores do CEPEA e câmbio | B |
| P16 | Verificações | Limiares das verificações de consistência | C |
| P17 | Validação | Referência de validação e código R do NASEM | B |
| P18 | Organização | PEV e gestação no gráfico do quadro | D |
| P19 | Organização | Prazo e formato de apresentação | D |
| P20 | Organização | Dados do cabeçalho dos documentos | D |

---

## A. Escopo e modelo

| # | Pergunta e contexto | Proposta | Destrava | Resposta |
|---|---|---|---|---|
| **P1** (PRD Q2) | O senhor espera uma dieta **por fase da lactação** (recém-parida, pico, fim)? O RuFaS formula **uma ração por lote**; a vaca recém-parida aparece na curva de lactação, mas não recebe dieta própria. | Manter a ração por lote no simulador. No módulo ampliado, a **vaca e a fase específicas passam a ser entrada** (P3), o que atende ao pedido sem otimizar por dia. | Especificação do FSD sobre fases; RF-28 e RF-30 | |
| **P2** (PRD Q3) | Como tratar a **resposta do leite à dieta**? No RuFaS v1.0.6 o leite segue a curva de Wood e só cai quando a ração não atende às exigências; por isso a margem varia sobretudo pelo custo da dieta. O NASEM calcula **proteína e gordura do leite** a partir de aminoácidos e energia absorvidos (erro de 14,4% e 17,1%), mas o próprio livro desaconselha usar o leite "permitido" por energia ou proteína como meta (erro de 22% a 24%). | (a) Manter o leite do RuFaS. Alternativas: (b) modelo NASEM de proteína e gordura do leite; (c) outro modelo indicado pelo senhor. | Trade-off central do produto; R1 | |
| **P3** (novo) | O módulo ampliado do Exercício do quadro tem **duas fases**: (1) **avaliar e comparar dietas já montadas** para uma vaca e fase específicas, com modelo linear e comparação com o RuFaS (RF-28, RF-29); (2) **sugerir a dieta ótima** (RF-30). O senhor confirma essa ordem e o escopo de categorias: vaca em lactação, vaca seca e pré-parto, novilhas em crescimento (as que o RuFaS otimiza)? | Confirmar fase 1 como prioridade e as três categorias. Bezerras ficam de fora (o RuFaS não as otimiza). | Plano de implementação; FSD, Anexo B | |

## B. Módulo ampliado e linearização

| # | Pergunta e contexto | Proposta | Destrava | Resposta |
|---|---|---|---|---|
| **P4** (L-Q1) | Quais **tolerâncias** aceitar? A linearização usa um método iterativo (ponto fixo). | Convergir quando a maior variação de uma quantidade for menor que 0,0001 kg e o custo variar menos de 0,01%, em até 20 iterações. Erro de linearização de até 1% da exigência em cada restrição. | Critério de aceite do RF-29 | |
| **P5** (L-Q5) | Como **ordenar** as dietas, "das menos recomendadas até a ótima"? | Primeiro as **inviáveis**, da maior para a menor violação normalizada das exigências; depois as **viáveis**, do maior para o menor custo; a de menor custo é a "melhor entre as informadas" (a ótima, só na fase 2). | RF-28 | |
| **P6** (L-Q2) | Para uma vaca isolada, de onde vêm o **metano entérico** e o **nitrogênio urinário**? No RuFaS são médias do lote, produzidas pela simulação, e entram na energia do NASEM. | Estimar pelas equações do NASEM (Eq. 3-9 e 3-10a), congelar na referência e permitir ao usuário sobrescrever. | Energia no modo NASEM | |
| **P7** (L-Q7) | Como representar a **vaca recém-parida**? O NASEM (p. 476) diz que, para grupos com menos de 90 dias em lactação, a equação de consumo deve ser integrada ao longo do tempo, e que usar o dia médio superestima o consumo de 0 a 45 dias. | Avaliar a vaca individual no dia informado (sem integrar), com aviso para dias em lactação abaixo de 45. | Consumo estimado; RF-28 | |

## C. Perguntas sobre o comportamento do RuFaS

Estas perguntas vêm de leituras do código do RuFaS v1.0.6. O sistema **não modifica** o RuFaS; as respostas definem o que
replicar e o que registrar como limitação.

| # | Pergunta e contexto | Proposta | Destrava | Resposta |
|---|---|---|---|---|
| **P8** (L-Q4) | Na digestibilidade da FDN do NASEM (Eq. 3-5a), o RuFaS usa o **amido total em kg**; o livro usa **% da MS**. Estimamos que isso eleva a digestibilidade da FDN em cerca de 0,1 e a energia digestível em cerca de 0,15 Mcal/kg de MS. É intencional? | Replicar o RuFaS, para a integração futura, e **registrar a diferença** (decisão L-D5). | Comparação com o RuFaS | |
| **P9** (L-Q6) | No modo NASEM, a **oferta de proteína metabolizável** usa o método do NRC, e a **exigência** é a do NASEM. É intencional? | Replicar e registrar. | RF-24 e RF-29 | |
| **P10** (PRD Q10) | O otimizador aceita ração com consumo até **30% acima do estimado** (`DMI_CONSTRAINT_FRACTION = 0,30`), e o erro típico da equação de consumo do NASEM é 12,1%. Nas 57 simulações guardadas, a ração ficou de 3 a 8 kg acima do estimado, várias no teto. É intencional? | Perguntar e registrar a resposta; o painel de verificações (RF-27) avisa quando o consumo passa do estimado. | Custo e margem; RF-27 | |
| **P11** | O **fósforo de mantença da vaca seca** é 0,8 g/kg de MS no RuFaS; as notas do NASEM trazem 1,0 g/kg para vacas adultas, secas e lactantes (Eq. 7-5b, p. 124, a conferir). Há motivo? | Registrar; não afeta a vaca em lactação. | Categoria vaca seca | |
| **P12** | O otimizador parte de um ponto **aleatório** (`random.random()·10`) quando não há ração anterior, e o problema não é convexo. O resultado é reprodutível (semente) ou pode variar entre execuções? | Comparar sempre contra várias execuções do RuFaS e usar a de menor custo. | Comparação do RF-29 | |

## D. NASEM, alimentos, preços e validação

| # | Pergunta e contexto | Proposta | Destrava | Resposta |
|---|---|---|---|---|
| **P13** (PRD Q6) | O **NASEM 2021** é requisito de entrega? Hoje o sistema só tem o NRC 2001; o NASEM é viável (o RuFaS já o suporta) e está especificado. | Implementar o seletor de padrão e a comparação NRC × NASEM. | RF-24 | |
| **P14** (PRD Q9) | O **arroz do quadro** é o arroz em grão? A composição do quadro (carboidrato 0,77; proteína 0,08) é compatível com o arroz em grão do NASEM (amido 75,8%, PB 8,1%), que **nenhuma biblioteca do RuFaS tem** (só farelo de arroz). No padrão NRC não há dados completos. | Cadastrar o arroz em grão com os dados do NASEM, disponível só no padrão NASEM. | RF-26 | |
| **P15** (PRD Q5; L-Q3) | Quais **indicadores do CEPEA** usar (produtos e unidades) e como mapeá-los aos alimentos? Os preços ficam em **US$**; o câmbio é fixo ou uma série? O CEPEA publica em R$ por unidade comercial, na matéria natural; o modelo usa US$/kg de MS. | O usuário informa o preço em US$/kg de MS, ou o valor original com o câmbio; mapeamento e conversão automática depois. | RF-22; preços do módulo | |
| **P16** (PRD Q8) | **Limiares** das verificações de consistência da ração (consumo × estimado). | Atenção a partir de +12% (1× o erro do NASEM) e alerta a partir de +24% (2×); leite perdido em alerta a partir de 50% da redução máxima configurada. | RF-27 | |
| **P17** (PRD Q4) | Qual **referência de validação** usar para a ração? O capítulo 20 do NASEM traz todas as equações do modelo; a Tabela 21-1 traz exigências de animais-tipo, mas o consumo dela **não** é reproduzido pela Eq. 2-1 sem premissas que o texto não declara. O livro afirma que o **código R oficial** do modelo prevalece sobre o texto. O senhor tem acesso a ele? | Validar contra as equações do capítulo 20 e, se disponível, contra o código R oficial. | Métrica M6; aceite científico | |

## E. Organização

| # | Pergunta e contexto | Proposta | Destrava | Resposta |
|---|---|---|---|---|
| **P18** (PRD Q1) | No gráfico do quadro, **PEV** é o _período de espera voluntário_ (60 dias), e os 270 dias são a gestação a partir do PEV? | Manter essa leitura (parâmetros editáveis). | RF-14 | |
| **P19** (PRD Q7) | Qual o **prazo** de entrega e o **formato** da apresentação? | Sem proposta. | Prioridade dos itens pendentes | |
| **P20** | Nome do professor, instituição, autores e disciplina, para o cabeçalho dos documentos. | Preencher quando informados. | Cabeçalhos do PRD, DESIGN e demais | |

---

## Mapa de correspondência com os documentos

| Pergunta | PRD (seção 15) | LINEARIZACAO (seção 8) | FSD |
|---|---|---|---|
| P1, P2, P18, P19 | Q2, Q3, Q1, Q7 | — | Seção 27 |
| P3 | — | — | Anexo B.1 |
| P4 | Q11 | L-Q1 | Anexo B.9 |
| P5 | Q11 | L-Q5 | Anexo B.6 |
| P6 | Q11 | L-Q2 | Anexo B.3 |
| P7 | Q11 | L-Q7 | Anexo B.10 |
| P8, P9 | — | L-Q4, L-Q6 | Anexo B.6 |
| P10 | Q10 | — | Anexo A.6 |
| P11, P12 | — | — | — (novas) |
| P13 | Q6 | — | Anexo A.3 |
| P14 | Q9 | L-Q3 | Anexo A.5 |
| P15 | Q5 | L-Q3 | Anexo B.5 |
| P16 | Q8 | — | Anexo A.4 |
| P17 | Q4 | — | Anexo A.3.7 |
| P20 | — | — | — |

Quando as respostas chegarem, o PRD (seção 15), o `LINEARIZACAO.md` e o FSD serão atualizados, e as decisões passam a constar
como "decididas" nos três documentos.

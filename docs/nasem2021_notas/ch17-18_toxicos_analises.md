# NASEM 2021 — Notas técnicas: Cap. 17 (Agentes Tóxicos) e Cap. 18 (Análise dos Alimentos)

**Páginas impressas cobertas:** 369–392 (Cap. 17: pp. 369–381, texto 369–378 + referências 378–381; Cap. 18: pp. 382–392, texto 382–390 + referências 390–392).
Todas as páginas de texto foram lidas por OCR; as páginas 370–378 e 382–390 foram conferidas contra a imagem (p.369 só OCR; pp. 379–381 e 391–392 são só referências, percorridas pelo OCR).

- **Cap. 17 — Usado diretamente no modelo? NÃO.** Não há equação nem tabela no capítulo; o conteúdo é de segurança alimentar/saúde animal e humana. Serve como **regras de alerta** (flags) do otimizador/validador de dieta, com limites numéricos citados no texto (seção 6 abaixo).
- **Cap. 18 — Usado diretamente no modelo? PARCIAL.** Não calcula nada do modelo, mas define **como cada ENTRADA laboratorial do modelo deve ser medida** (métodos, correções, fontes de erro), mais 1 tabela numérica (Tabela 18-1, fatores de correção de AA após hidrólise de 24 h) usada em cálculo e algumas fórmulas de laboratório. Não traz "faixas aceitáveis" de composição de alimentos; só critérios de controle de qualidade analítico (ex.: recuperação de amido 88–92%).

Convenções: PT-BR traduzido; decimal = ponto; siglas PT (PB, FDN, FDA, PIDN, PIDA, MS, MO, MOR, AG, CSA, PNDR, PNDRd, AA, AA-PR, FDNfa, DIVFDN). Termos em inglês usados nas equações do modelo (do resto do livro): CP, NDF, ADF, FA, ROM, dNDF, IVNDFD, dRUP, RUP, RDP.

---

# PARTE A — CAPÍTULO 17: AGENTES TÓXICOS PARA BOVINOS LEITEIROS [pp.369–378]

## A.1 Papel no simulador
Capítulo qualitativo/regulatório. Não gera entradas nem saídas do modelo nutricional. Utilidade para o simulador: (i) base de **alertas** quando o usuário informar o teor de toxina/ingrediente de risco (gossipol livre, aflatoxina, DON, fumonisinas, zearalenona, ergovalina, lolitrem B, nitrato, HCN, dicumarol) e (ii) texto de ajuda/segurança. Toxinas manufaturadas (pesticidas, herbicidas) e plantas tóxicas de pastagem **não** são abordadas [p.369]. Excesso de minerais: ver Cap. 7 do livro e *Mineral Tolerance of Animals* (NRC, 2005) [p.369]. Glucosinolatos (goitrogênicos): remete à seção Iodo do Cap. 7 [p.371].

Aviso do próprio livro (nota de rodapé, p.369): níveis de ação e a base (matéria natural ou MS) devem ser verificados nas diretrizes **vigentes** do FDA (EUA). O livro cita valores do FDA, não da legislação brasileira — **o simulador deve permitir parametrizar os limites por jurisdição** (não informado pelo livro: limites do Brasil/MAPA).

## A.2 Entradas (potenciais, não existem como variáveis do modelo no livro)
| Variável | Sigla | Unidade | Definição | Faixa/valores típicos | Pág. |
|---|---|---|---|---|---|
| Gossipol livre da dieta | — | mg/kg MS da dieta | forma biologicamente ativa (a ligada não é) | grãos de caroço de algodão (G. hirsutum): 0.59–2.35 % da MS, média 1.32 %, DP 0.35 % (≈ 0.9 % do caroço integral "como fornecido") | 371 |
| Aflatoxinas totais (B1+B2+G1+G2) | — | µg/kg (base ≈88 % MS) | contaminação do alimento | ver tabela A.5 | 373–374 |
| DON (vomitoxina) | DON | mg/kg (base 88 % MS) | em grãos e subprodutos | ver tabela A.5 | 374 |
| Fumonisinas FB1+FB2+FB3 | — | mg/kg MS (dieta total) | | ver tabela A.5 | 374 |
| Zearalenona | ZEN | mg/kg da dieta | | ver tabela A.5 | 375 |
| Ergovalina / lolitrem B | — | ng/g ou µg/g do pasto | endófitos em festuca / azevém | ver tabela A.5 | 370 |
| Nitrato | NO3- | não informado (sem limite em alimento) | | ver A.5 | 372 |
| HCN potencial | — | não informado em concentração; dose tóxica em mg/kg PC | | ver A.5 | 372 |
| Dicumarol no feno | — | mg/kg matéria natural | trevo-doce mofado | ver A.5 | 371 |

## A.3 Saídas
Nenhuma do modelo. Saídas possíveis do simulador (sugestão de implementação, **não** no livro): lista de alertas com severidade.

## A.4 Equações
Nenhuma no capítulo. Valores de transferência para o leite citados como razões (ver A.5.2).

## A.5 Parâmetros e tabelas (construídas a partir do texto; o capítulo não tem tabelas numeradas)

### A.5.1 Tabela de alertas de toxinas — limites/valores de referência [conferido na imagem pp.370–375]
Legenda "tipo": REG = limite/orientação do FDA (EUA); LIT = valor de estudo/literatura (não regulatório); — = nenhum estabelecido.

| Agente | Valor de referência | Tipo | Aplicação / condição | Base | Efeito / observação | Pág. |
|---|---|---|---|---|---|---|
| **Gossipol livre** (vacas em lactação) | 0 a 1050 mg/kg MS da dieta: sem efeito na IMS ou na lactação (caroço ou farelo de algodão) | LIT (Mena et al., 2001) | vacas leiteiras em lactação | MS da dieta | a 1050 mg/kg houve **aumento da fragilidade eritrocitária** | 371 |
| Gossipol livre (bezerros) | ≤ 200 mg/kg MS: sem efeito deletério em 90 dias; ≥ 400 mg/kg: **tóxico** | LIT (Risco et al., 1992) | bezerros; texto conclui que produtos de algodão para bezerros jovens **não são recomendados** | MS da dieta | animais sem rúmen funcional desenvolvido são sensíveis | 371 |
| Gossipol livre (vacas, toxicidade) | 1,510 mg/kg IMS (Lindsey et al., 1980): vacas com respostas negativas de toxicidade; gossipol **não detectado no leite** (sensibilidade do ensaio 0.5 µg/mL) | LIT | | MS | | 371 |
| Gossipol no leite | 817 e 1,295 mg gossipol livre/kg MS (10 e 15 % da MS como caroço integral) → 0.13 e 0.22 mg gossipol/kg leite após 60 d (Wang et al., 2012); não detectado com dieta controle ou com farelo de algodão ≤ 117 mg/kg MS | LIT | | MS / leite | | 371–372 |
| Gossipol em produtos de algodão p/ consumo humano | 450 mg/kg (livre) | REG (FDA 2015d) | produtos de caroço de algodão modificados para alimento humano | produto | não é limite de ração | 372 |
| Gossipol e touros | touros de 1 ano: farelo de algodão 7 % + cascas 18 %, ou caroço integral 15 % + cascas de caroço 17 % (% da MS), por 2 meses → alterações histológicas espermatogênicas, parcialmente reversíveis após 2 meses sem gossipol | LIT (Arshami e Ruttle, 1988) | reprodutores | % MS | função reprodutiva de **vacas** é relativamente insensível | 371 |
| **Aflatoxinas** — leite | ≤ 0.5 µg/kg de aflatoxina M1 no leite | REG (FDA 2012a) | leite | leite | transferência B1→M1 no leite: **2.0–6.2 % da ingestão** (Fink-Gremmels, 2008) | 373 |
| Aflatoxinas — ração de vacas leiteiras | **≤ 20 µg/kg** (milho, produtos de amendoim, farelo de algodão e outros alimentos/ingredientes) | REG (FDA 1994) | animais leiteiros | **≈88 % MS** (equivale a grãos secos de milho, caroço de algodão e derivados de amendoim na matéria natural) | bezerros muito suscetíveis; ruminantes adultos relativamente resistentes; efeitos: função hepática e queda de ingestão; cancerígeno potencial | 373–374 |
| Aflatoxinas — bovinos de corte (animais leiteiros criados como corte) | 300 µg/kg (milho/amendoim para terminação; farelo de algodão para corte independente da idade) | REG (FDA 1994) | só se o animal leiteiro for destinado a corte | ≈88 % MS | não se aplica a vacas em lactação | 373–374 |
| **DON** (desoxinivalenol) | **5 mg/kg** em grãos e subprodutos de grãos, **e** estes ingredientes **≤ 40 % da dieta** | REG (orientação/"advisory" FDA 2005a) | bovinos leiteiros ("aparentemente se aplica") | **88 % MS** | bovinos amplamente resistentes (conversão ruminal em DOM-1); principal efeito geral = queda de ingestão; pode reduzir proteína microbiana; transferência ao leite ≤ 0.02 % da ingestão; coocorre com zearalenona | 374 |
| DON — dado experimental | sem DON no leite com dieta de "66 mg/kg" por 5 dias (imagem confere: 66; ver ⚠); DOM-1 no leite: não detectável a 26 µg/kg; a 18.8–60.8 mg/d de DON: leite 0.11–0.22 µg/kg (DON) e 1.5–2.9 µg/kg (DOM-1) | LIT | | | | 374 |
| **Fumonisinas** (FB1+FB2+FB3) | **15 mg/kg** na dieta total para touros, **vacas leiteiras em lactação** e reprodutores; **30 mg/kg** para bovinos ≥ 3 meses de idade alimentados para abate | REG (orientação FDA 2005a) | | **MS** | ruminantes tolerantes (> 80 % de FB1/FB2 vai às fezes em novilhos); transferência ao leite de FB1: 0–0.05 % da ingestão | 374 |
| **Zearalenona** | > 10 mg/kg da dieta → disfunção reprodutiva em **novilhas** leiteiras; > 20 mg/kg → em **vacas** adultas; machos jovens podem ficar inférteis | LIT (Merck 2010c) | | dieta | **nenhuma tolerância/orientação do FDA**; > 90 % convertida em zearalenol no rúmen; transferência ao leite ≈ 0.7 % (Mirocha 1981); leite abaixo do limite de detecção (1.3 e 1 µg/kg) a 238–1125 µg ZEN/d | 375 |
| **Ocratoxina A** | sem tolerância/orientação do FDA; ruminantes funcionais resistentes (degradada a ocratoxina α); bezerros alimentados com leite: dose progressiva ≥ 1 mg/kg PC → mortes; ruminantes funcionais só sofrem com doses muito altas (12 mg/kg PC) | — / LIT | | | detectada no leite europeu (5–40 µg/kg) em 1–15 % das amostras | 374–375 |
| **Patulina** | sem tolerância/orientação em ração; sem dados de transferência ao leite | — | | | in vitro: altera fermentação ruminal, reduz proteína microbiana, digestibilidade e AGV | 375 |
| **Ergovalina** (festuca com endófito) | intoxicação relatada a **50 ng ergovalina/g de festuca** | LIT (Porter, 1995) | pasto/forragem de festuca alta | forragem | laminite, perda de PC, pelagem áspera, gangrena seca, ↑ temperatura corporal e frequência respiratória, ↓ prolactina; sem ergovalina detectável no leite de ovelhas (LD 0.15 ng/mL) a 497 µg/kg MS | 370 |
| **Lolitrem B** (azevém perene) | "andar cambaleante" pode ocorrer a **5 µg lolitrem B/g** da gramínea | LIT (Porter, 1995) | azevém com endófito | forragem | vacas a ≈ 35 mg/d de lolitrem B → máx. 5 ng/mL de leite; volta a ≈ 0 em 8 dias após retirar; recuperação em 1–2 semanas se alimento não tóxico | 370 |
| **Dicumarol** (trevo-doce mofado) | feno com **20–30 mg/kg** (matéria natural) por várias semanas pode causar intoxicação e morte | LIT (Merck 2010c) | feno | matéria natural | doença hemorrágica; transfere via placenta; sem dado de passagem ao leite | 371 |
| **Nitrato** (NO3-) | **nenhum limite numérico em alimento** neste capítulo (remete a boletins de extensão, Strickland et al. 2011) | — | | | metemoglobina (sangue marrom-chocolate); risco ↑ com seca, baixa luz, adubação N; adaptação gradual reduz o risco; silagem pode gerar NO2 (gás de silo) | 372 |
| Nitrato — limites FDA (referência humana) | 10 mg/L de NO3-N na água engarrafada (= 44 mg NO3-/L); nitrato de sódio como conservante de carnes/peixes até 500 mg/kg (364 mg NO3-/kg do produto) | REG (FDA 2015b,c) | não é limite de ração | | leite comercial 2 % gordura: 0.20 mg NO3-/100 mL e 0.0002 mg NO2-/100 mL (Hord 2011); dose oral única de 150 g KNO3 (92 g NO3-) → pico 35.6 mg NO3-/L no leite (DP 10.1), volta em 50 h | 372 |
| **Ácido prússico (HCN)** | dose letal mínima ≈ **4.4 mg HCN/kg PC por hora** (morte em 15 min a algumas horas); **≈ 2 mg HCN/kg PC** é dose tóxica para a maioria dos animais | LIT (Kingsbury 1958; Merck 2010c) | Sorghum spp. (Johnsongrass > sorgos > híbridos sorgo-sudão > capim sudão em potencial de HCN) | PC | HCN potencial diminui com maturidade após 45 dias; ↑ com adubação N, seca/geada, plantas jovens, folhas > hastes | 372 |
| **Inibidor de tripsina** (soja crua) | sem valor numérico; soja/farelo comercial é tratado termicamente | — | irrelevante para ruminantes adultos (inativado no rúmen); **soja crua para bezerros jovens** reduz digestão proteica | | | 373 |
| **Samambaia** (ptaquilosídeo) | sem limite; **evitar** consumo; ptaquilosídeo no leite = 8.6 ± 1.2 % da quantidade ingerida (linear, dose-dependente) | LIT | | | cancerígeno; passa ao leite | 370 |
| Galotanino (carvalho) | sem limite; sinais em 3–7 dias | — | | | manejo: acesso a forragem, afastar de áreas com carvalho | 371 |
| **Microcistina-LR** (cianobactérias) | OMS: ingestão diária tolerável **0.04 µg/kg PC** (humanos); leite de vacas com doses letais de células: < 0.2 ng/L | REG-ref (OMS 2003) / LIT | água superficial com floração | | morte em horas a dias; fotossensibilização nos sobreviventes | 376 |
| **Botulismo** | pasteurização padrão 72 °C por 15 s inativa ≥ 99.99 % de toxina botulínica A e B no leite | LIT | silagem mal emurchecida/sem acidificação suficiente e carcaças são riscos; vacinação contra tipos C e D | | | 375–376 |
| **E. coli O157:H7 e Salmonella** | alimento/ingrediente de ração em que forem **detectadas** = **adulterado**, proibido (FDA 2005a) | REG | | | pasteurização do leite é eficaz; prevalência de O157:H7 em bovinos 0.4–48.8 % | 377 |
| **Listeria** | silagem com pH < 4.9 associada a baixa presença; algumas sobrevivem 30 dias, normalmente não > 90 dias; incidência ↑ com pH | LIT | silagem (principalmente com deterioração aeróbia) | | recuperação ≈ 50 % com tratamento | 377 |
| **Príons / EEB** | proibido desde 1997 fornecer a ruminantes a maioria das proteínas de ruminantes (exceto hemoderivados, gelatina, sebo); desde 2008 tecidos bovinos de alto risco proibidos em toda ração | REG (21 CFR 589.2000, 589.2001) | regra de composição de dieta | | 6 casos de EEB nos EUA desde 2003 (até 2018) | 378 |
| **Cryptosporidium** | oocistos resistentes a cloro; inativados por < 0 °C e > 65 °C; pasteurização 71.7 °C por 5–15 s inativa | LIT | bezerros de 1–3 semanas (48 %–70 % infectados) | | | 376 |

### A.5.2 Taxas de transferência para o leite (resumo numérico) [pp.370–375]
| Toxina | Transferência para o leite | Pág. |
|---|---|---|
| Aflatoxina B1 → M1 | 2.0–6.2 % da ingestão | 373 |
| DON | ≤ 0.02 % da ingestão (DOM-1 também detectável) | 374 |
| Fumonisina B1 | 0–0.05 % da ingestão | 374 |
| Zearalenona + metabólitos | ≈ 0.7 % (Mirocha 1981); abaixo do LD em Seeling 2005 | 375 |
| Ptaquilosídeo | ≈ 8.6 ± 1.2 % da ingestão | 370 |
| Lolitrem B | máx. 5 ng/mL de leite a ≈ 35 mg/d | 370 |
| Ergovalina | não detectada (LD 0.15 ng/mL) em ovelhas | 370 |
| Gossipol | 0.13–0.22 mg/kg de leite a 817–1,295 mg/kg MS na dieta | 371 |
| Microcistina-LR | < 0.2 ng/L | 376 |
| Dicumarol, galotanino, HCN (bovinos), ocratoxina (alimentação), patulina | "não foram encontradas informações" / não estabelecido | 371–375 |

## A.6 Regras de decisão / restrições para o otimizador (propostas de implementação com base nos limites do livro)
Regras com origem regulatória (FDA), condicionadas à **matriz de composição informada** (somente se o usuário fornecer o teor de toxina; o livro não tem tabela de teores por alimento):
1. **Aflatoxina (vaca em lactação):** ALERTA/BLOQUEIO se aflatoxina total > 20 µg/kg (base ≈ 88 % MS) em milho, produtos de amendoim, farelo de algodão ou outro ingrediente [p.373]. Limite de 300 µg/kg só se animal for destinado a corte [p.374].
2. **DON:** ALERTA se DON em grãos/subprodutos de grãos > 5 mg/kg (base 88 % MS) **ou** se esses ingredientes > 40 % da MS da dieta [p.374].
3. **Fumonisinas (FB1+FB2+FB3):** ALERTA se > 15 mg/kg MS da dieta total para vacas em lactação/reprodutores; > 30 mg/kg para bovinos ≥ 3 meses em abate [p.374].
4. **Gossipol livre:** alerta informativo — vacas lactantes sem efeito na IMS/lactação até 1050 mg/kg MS da dieta (estudo único; ↑ fragilidade eritrocitária nesse nível); **bezerros jovens:** não recomendado produto de algodão (tóxico a ≥ 400 mg/kg MS); touros: cuidado com farelo/caroço (ver tabela) [p.371]. Os valores de 200/400 e 1050 mg/kg são da literatura, não "limites oficiais".
5. **Zearalenona:** alerta de risco reprodutivo > 10 mg/kg (novilhas) e > 20 mg/kg (vacas); não há limite FDA [p.375].
6. **Ingredientes proibidos/regras de composição:** presença de Salmonella ou E. coli O157:H7 = ingrediente adulterado; proteínas de ruminantes (exceto hemoderivados, gelatina, sebo) proibidas na dieta de ruminantes; tecidos bovinos de risco proibidos em toda ração [pp.377–378].
7. **Pasto/forragem:** festuca ≥ 50 ng ergovalina/g e azevém ≥ 5 µg lolitrem B/g = risco [p.370]; feno de trevo-doce com dicumarol 20–30 mg/kg (matéria natural) = risco [p.371]; sorgo/sudão: risco por HCN ≥ ~2 mg/kg PC de dose [p.372].
8. **Silagem:** pH ≥ 4.9 aumenta risco de Listeria; silagem pouco emurchecida/sem açúcares e contaminada por carcaça = risco de botulismo — descartar alimento estragado [pp.375, 377].
9. Mesmo com análise, **amostragem** é crítica porque fungos/toxinas não se distribuem uniformemente no alimento [pp.373–374]; métodos para toxinas regulamentadas devem ser AOAC, boletins de laboratório do FDA ou literatura revisada por pares [p.373].

## A.7 Lógica e fluxo
Camada de validação **após/antes** do otimizador: (1) usuário informa composição de toxinas por ingrediente (opcional); (2) simulador calcula concentração na MS da dieta total (média ponderada pela proporção de cada ingrediente na MS — **inferência**, o livro não dá fórmula); (3) compara com tabela A.5.1. Convém armazenar a base (88 % MS vs. matéria natural) por limite. Não há entrada do modelo nutricional (Caps. 2–11) afetada — nenhum desconto de IMS/produção por toxina é dado no livro.

## A.8 Limitações, incertezas e mudanças vs. NRC 2001
- O livro admite que faltam dados de transferência ao leite (alcaloides de Phalaris/Lolium, dicumarol, galotanino, HCN em bovinos, patulina, ocratoxina em ração) e pede "trabalho adicional" [pp.370, 371, 373, 375].
- Nitrato: **sem limite numérico** neste capítulo (o NRC antigo tinha tabelas de nitrato; aqui só remete a boletins de extensão) [p.372] — a comparação com NRC 2001 não é feita no texto: "não informado".
- Os limites do FDA podem mudar; o próprio texto manda checar [p.369].
- Gossipol de vacas: apenas um estudo (Mena et al. 2001) para a faixa 0–1050 mg/kg; efeito ambíguo (fragilidade eritrocitária) [p.371].
- Toxinas manufaturadas, plantas tóxicas de pastagem e minerais em excesso: **fora do escopo** [p.369].

## A.9 Conceitos e evidências relevantes
- Gossipol livre (não ligado) é a forma ativa; microrganismos ruminais desintoxicam parcialmente; risco maior em animais sem rúmen funcional [p.371].
- Aflatoxina B1 não é modificada pelo fluido ruminal, é convertida a M1 no fígado e passa ao leite [p.373].
- Ruminais tolerantes a DON (DOM-1), fumonisinas (baixa absorção), ocratoxina (degradada a ocratoxina α + fenilalanina) [pp.374–375].
- Zearalenona: α-zearalenol é 3x mais estrogênico que a zearalenona; produzida com umidade alta e baixas temperaturas [p.375].
- DON e zearalenona coocorrem (ambos de Fusarium) [pp.374–375].
- Nitrato: toxicidade quando nitrito formado no rúmen não é totalmente convertido a amônia; nitrato dietético reduz metano (adaptação gradual reduz risco) [p.372].
- Inibidor de tripsina do colostro protege IgG; adição de inibidor de tripsina de soja ao colostro aumentou IgG/IgM séricas em bezerros Jersey [p.373].

## A.10 Dúvidas/riscos de OCR (Cap. 17)
- ⚠ **p.374 DON "66 mg/kg"** de DON por 5 dias (Côté et al., 1986): a imagem confere com 66 mg/kg, valor muito acima do limite de 5 mg/kg; possível erro de impressão/tradução (6.6?). Não usar como referência.
- OCR de p.369 traz "Capítulo 77" (provável "Capítulo 7"; p.371 diz "seção Iodo no Capítulo 7"); p.369 não foi conferida em imagem. Sem impacto numérico.
- ⚠ "Limites do FDA: nível 'aconselhado' (DON, fumonisinas) é orientação, não limite legal" — o livro usa "nível aconselhado/orientação"; a tradução PT mistura "limite" e "orientação".
- ⚠ Base de aflatoxina "≈ 88 % de MS" [p.374] é interpretação do livro ("provavelmente") — confirmar com a norma original.
- Valores numéricos conferidos na imagem: pp.370–378 (todos) — nenhuma divergência OCR vs. imagem além do indicado.

---

# PARTE B — CAPÍTULO 18: ANÁLISE DOS ALIMENTOS [pp.382–390]

## B.1 Papel no simulador
Define os **métodos analíticos que geram as entradas** das equações do livro e as precauções que mantêm essas entradas comparáveis com o banco de dados que originou as equações. Se o usuário/laboratório usar método alternativo, particularmente para análises **empíricas** (como FDN), deve verificar comparabilidade com o método citado [p.382]. Não há equações do modelo; há uma tabela (18-1) de correção de AA e fórmulas de laboratório. É a fonte para: (i) mensagens de ajuda sobre "como obter cada entrada"; (ii) correção de AA corrigido (AAcorr); (iii) tolerâncias de QC; (iv) avisos de qualidade de dados (ex.: contaminação por solo, amostras > 10 % gordura).

## B.2 Entradas do modelo e a análise de laboratório que as alimenta
(Coluna "Entrada/uso no modelo" cruza com os outros blocos de notas já escritos — Caps. 3, 5, 6, 7 — e está marcada "(cruz.)"; o que o Cap. 18 diz explicitamente está sem marca.)

| Entrada do modelo / grandeza | Análise e método recomendado | Detalhes críticos | Erro analítico / fonte de erro citada | Pág. |
|---|---|---|---|---|
| **MS** (base de todas as concentrações) | secagem em estufa de ar forçado (100–105 °C overnight/peso constante; 135 °C por 2 h — AOAC 930.15) ou micro-ondas | opção para reduzir escurecimento: 55–60 °C por 24 h em ar forçado, depois 105 °C por 48 h. Amostras para análises adicionais **não devem ser secas a > 60 °C** (altera solubilidade de proteína, lignina e fibra). Misturar amostras grandes durante a secagem. Secar a < 60 °C dá MS **menor** que a temperaturas maiores. Titulação Karl Fischer (água específica) **não** serve para MS por diferença; "perda na secagem" remove água + voláteis | MS de silagem pode perder voláteis (texto só diferencia água de perda na secagem — não quantifica) | 382–383 |
| **Cinzas / MO** (cinzas para Eq. 3-1 e FDN livre de cinzas) | mufla: 600 °C por 2 h (AOAC 942.05) ou 500–600 °C por 8–24 h | resíduo deve ser cinza-claro a branco; marrom/preto = combustão incompleta (reprocessar, checar oxigênio e temperatura) ou minerais/carbonatos | | 383 |
| **PB** (CP) | N por Kjeldahl ou combustão de Dumas; **PB = N × 6.25** (16 % N) | fator real 5.18–6.38 conforme alimento (Jones 1931); NNP (ureia) tem fator muito menor; leite: 6.38 (6.34 mais apropriado, Karman e van Boekel 1986); farinha de sangue soma frequentemente > 100 % por fator inadequado | conversão N→PB é fonte de erro; somas ≠ 100 % são normais | 382–383 |
| **PB solúvel** | PB total − PB restante após extração com tampão borato-fosfato (Licitra 1996) | não diferencia proteína de NNP; **não é usada no modelo para suprimento de nutrientes** | | 384 |
| **PIDN** (PB insolúvel em detergente neutro) | resíduo de FDN (com sulfito de sódio + α-amilase termoestável), filtração a vácuo em papel, enxágue com água fervente e acetona; secar resíduo + papel a 55–60 °C; N por Dumas/Kjeldahl; **expresso como N × 6.25** | | | 384 |
| **PIDA** | resíduo de FDA (mesmo procedimento da FDA), N por Dumas/Kjeldahl; **N × 6.25** | | | 384 |
| **AA das proteínas** | hidrólise ácida (HCl) 21–24 h, exceto **Trp: hidrólise alcalina**; **Cys e Met protegidos por oxidação com ácido perfórmico antes da hidrólise** (AOAC 2006 ou posterior; Rutherfurd e Gilani 2009) | 1 kg de proteína pura 100 % hidrolisada → ≈ 1.15 kg de AA livres (adição de água); mas hidrólise de 24 h costuma dar < 1 kg por perda de AA lábeis em ácido e liberação incompleta de ligações com resíduos hidrofóbicos; **não interpretar a diferença como NNP**. **Corrigir com Tabela 18-1** → AAcorr | | 383–384 |
| **FDN** | gravimetria, ebulição sob refluxo 1 h em detergente neutro com α-amilase termoestável + sulfito de sódio; filtro de porosidade grossa (AOAC 2002.04; Mertens 2002); FDN = peso do resíduo seco / peso seco da amostra | α-amilase remove amido, sulfito solubiliza proteína; escolher **"com cinzas" ou "livre de cinzas"** conforme a aplicação. **Na maioria das aplicações do modelo, a FDN NÃO é livre de cinzas** (a literatura de base não reportou assim). Sílica biogênica é solubilizada pelo detergente neutro, mas a sílica do **solo** contamina o resíduo → amostras com solo: base livre de cinzas ou reamostrar. **> 10 % de gordura: pré-extração com acetona** (senão FDN superestimada). Moinho: original com peneira 1 mm de moinho de facas (Wiley); moagem mais fina (ex.: atrito 1 mm) pode **reduzir** FDN (partículas finas passam pelo filtro). AOAC 2002.04 recomenda auxiliares de filtração (areia ou fibra de vidro) | **DP do erro analítico (mesma rodada):** 0.4 % forragens; 0.6 % concentrados < 10 % gordura; 0.4 % concentrados > 10 % gordura; 0.5 % geral (no material original) | 384–385 |
| **FDA** | gravimetria, refluxo 1 h em detergente ácido, cadinho de porosidade grossa (AOAC 973.18) | cinzas no resíduo contadas como MO se não for livre de cinzas (erro pequeno, exceto solo ou sílica biogênica); sílica biogênica (gramíneas C3 e C4, incl. cana-de-açúcar) é insolúvel em detergente ácido → usar base livre de cinzas para forrageiras suspeitas; **> 10 % de gordura: pré-extração com acetona**; **ferver ≤ 1 h**, lavar completamente o reagente (ácido remove mais da amostra com fervura longa ou degrada na secagem); moagem mais fina reduz FDA | | 385 |
| **Lignina** (Lignin, entrada da Eq. 3-3a, cruz.) | **lignina em ácido sulfúrico (72 %)** no resíduo de FDA (AOAC 973.18) | H2SO4 72 % **resfriado a 15 °C**; cadinhos mantidos entre **20 e 23 °C**; se não, ↑ solubilização e ↓ lignina medida | | 385 |
| **Amido** (Starch; entrada de MOR, digestão, restrições) | métodos enzimático-colorimétricos (AOAC 2014.10; Hall 2015; Bach Knudsen 1997): gelatinização (calor+umidade ou álcali) → α-amilase termoestável (E.C. 3.2.1.1) + amiloglicosidase (E.C. 3.2.1.3) ou amiloglicosidase sozinha → medida **específica de glicose** (glicose oxidase-peroxidase; HPLC; GC) | **amido = (glicose total após tratamento enzimático − glicose livre da amostra) × 0.9** (162/180). Em gelatinização com calor/umidade usar **tampões acidificados** (evita conversão a maltulose → menor recuperação). Moagem: peneira 1 mm em moinho de atrito, **0.5 mm em moinho de facas** ou 0.4 mm. Álcali pode incluir amido resistente às enzimas de mamíferos. Enzimas que liberam glicose de não amiláceos superestimam amido. **Não** usar recuperação de amostras controle para ajustar outras amostras. Alimentos cozidos/panificação/doces e alguns híbridos de milho: parte do amido é hidrolisada a material solúvel em água, mas analisada como amido → contado também em CSA (duplicação): corrigir (ver B.5) | **QC:** amido de controle deve dar 88–92 % de amido a partir da glicose; **sacarose pura < 1 %**; análise de sacarose e celulose > 1 % de glicose = enzimas/condições liberando glicose de não amiláceos. **DP:** 0.1 % (baixo amido), 0.3 % (alto amido), no material original | 385–386 |
| **CSA** (carboidratos solúveis em água; parte de MOR e CSDN, cruz.) | extração com água; detecção de espectro amplo por **fenol–ácido sulfúrico** (Dubois 1956), preferível a açúcar redutor (frutanos superestimados; lactose subestimada) | padrão do detector: **sacarose** (comum); usar lactose se lácteos, frutano se gramíneas temperadas. Moagem como a do amido. Fenol–ác. sulfúrico: 0.5 mL de amostra, 0.5 mL de fenol a 5 %, 2.5 mL de ácido; análise em **duplicata**, agitação após cada adição líquida. Etanol 80 % dá valores similares exceto frutanos/lactose. **Melaço:** usar "açúcares totais invertidos" do rótulo (se não houver lactose). Panificação: CSA inflado por maltooligossacarídeos | | 386–387 |
| **MOR** (matéria orgânica residual, ROM; Eq. 3-1, cruz.) | **calculada**, não medida: MO − PB − amido − FDN − AG (Eq. 3-1 do livro; ver B.4) | contém CSA, ácidos de fermentação (acético, lático, butírico), AG de cadeia curta e ácidos orgânicos de plantas, glicerol (livre e dos triglicerídeos), fibra solúvel (pectinas, gomas), taninos, ceras, pigmentos **e o erro analítico acumulado**; "usada para o cálculo de valores de energia" | | 387 |
| **AG (ácidos graxos)** (FA) | **GC de ésteres metílicos** com metilação e extração simultâneas (Sukhija e Palmquist 1988); variantes (benzeno, clorofórmio, T elevada) conforme o perfil lipídico | **Extrato etéreo / gordura bruta (GB) NÃO é recomendado** como medida de lipídio nutricional (contém ceras, cutina, pigmentos, indigestíveis). **GB (% MS) − 1 para estimar AG (NRC 2001) não é recomendado** — pode superestimar AG em até **2 % da MS** em forragens e dietas mistas (Palmquist e Jenkins 2003). Se for exigido rótulo: GB por AOAC 2003.05. Extração quantitativa antes da GC é crítica; **padrões internos de AG ausentes nos alimentos** devem ser adicionados; solventes que extraiam não-AG são aceitáveis se não gerarem AG "não identificados" | IVM (mid-IR) para AG do leite: mais preciso para AG principais, menos para poli-insaturados, n-3 e ramificados; estimativas de g/L de leite mais precisas que de AG na gordura | 387–388 |
| **Minerais** (macro/micro; Cap. 7) | ICP-MS (plasma indutivamente acoplado) ou absorção atômica; gravimétricos/colorimétricos para alguns | **NIRS não mede minerais diretamente** (correlação com componentes orgânicos) → resultados **não definitivos** | | 388 |
| **Cr** | moer em artefato **cerâmico** (equipamentos de aço/cromados contaminam; solo também) | contaminação de grau variável (Spears 2017) | | 388 |
| **P total e P orgânico/inorgânico** (Cap. 7, cruz.) | P total: molibdovanadato espectrofotométrico (AOAC 965.17); **P inorgânico: extração com 0.5 M HCl** e detecção de P no extrato (Ray 2012); **P orgânico = P total − P inorgânico** | | | 388 |
| **Tamanho de partícula (FDNfa, Cap. 5, cruz.)** | **Separador Penn State** (Kononoff 2003; Heinrichs 2013) | peneiras de **19 mm, 8 mm, 4 mm + bandeja**; ≈ **1.4 L** de TMR/silagem na peneira superior; agitar 5× em uma direção, girar ¼ de volta, repetir até **8 vezes (40 agitações)**; taxa **1.1 agitação/s**, curso de **17 cm (7 pol.)**; pesar o material de cada peneira; **MS de cada peneira** (micro-ondas, estufa ou outro) e % da MS total em cada peneira | | 388–389 |
| **DIVFDN / FDNd** (IVNDFD 30 ou 48 h; Eq. 3-3b, cruz.) | incubação anaeróbia **in vitro** com inóculo ruminal (Goering e Van Soest 1970); amostra moída em peneira de 1 mm (moinho de facas), **30 ou 48 h**; todo o frasco passa pelo método de FDN, resíduo por filtração a vácuo | **DIVFDN = (FDN % do alimento original − FDN residual % do alimento original) / FDN % do alimento original** (em base MS) | não informado | 389 |
| **Frações de proteína A, B e C e kd da B** (PB, PDR/PNDR, Cap. 6, cruz.) | **in situ** em sacos dacron/poliéster de **poro 40–60 µm**; amostra moída em **peneira de 2 mm** (moinho de facas) | relação **10 mg amostra/cm² de saco** (Vanzant 1998); sacos pré-embebidos em água; incubar no **rúmen ventral** de **≥ 2 animais canulados**, dietas caracterizadas (de preferência incluir o alimento incubado); **≥ 5 tempos incluindo 0 e 48 h** (+ **72 h para forragens**); modelo não linear de **1ª ordem** ajusta frações residuais e kd da B; **sacos em branco** para infiltração de partículas; **< 48 h é problemático** (fração C pode não ser detectada em muitas fontes de PNDR); **substrato padrão** recomendado; lavagem em máquina: 5 enxágues de 1 min em água fria; **corrigir contaminação microbiana (recomendado; obrigatório na prática se FDN > 20 %)** | perda de partículas pequenas do saco **superestima A e reduz B/C**; kd fracionário **aumenta** com menor tamanho de partícula; moagem em 2 mm melhora homogeneidade e reduz perda de FDN (e provavelmente N); processamento no banco do comitê varia (tesoura em forragem fresca até moagem 1–2 mm congelada ou seca ≤ 60 °C); padrões internos pressupõem comportamento igual ao do alvo; padrão deve ser subamostrado e armazenado adequadamente | 389–390 |
| **Digestibilidade intestinal da PNDR (PNDRd, Cap. 6/19, cruz.)** | **in vitro** (procedimento de 3 etapas de Calsamiglia e Stern 1995, **modificado** por Gargallo 2006; papel de filtro de poro pequeno para recuperar proteína não degradada solúvel — Hristov 2019) **ou saco móvel** (pré-incubação ruminal para alguns alimentos antes do duodeno; Hvelplund 1985) | quase todos os valores pós-NRC 2001 vêm de sacos **recuperados das fezes** (valores iniciais: cânula ileal). Método de Ross (2013) **não foi usado** no modelo e **sem recomendação**. Tamanho de poro e substrato interagem; poucas comparações com in vivo; corrigir contaminação por N bacteriano (principalmente com FDN residual) | | 389–390 |
| **Biodisponibilidade de AA-PR (AA protegidos do rúmen)** | não há método único; categorias in vitro, in situ, in vivo (Whitehouse 2016, 2017) | detalhes em B.7; comentários em Cap. 6 | variância ≥ 20 % em avaliação de ponto único (concentração sanguínea); 10–12 % para método de diluição isotópica com 13C | 390–391 |

(Fim da tabela B.2: não há, no capítulo, método para "carboidratos não fibrosos por diferença", "extrato livre de N" etc.; o texto diz que frações calculadas por diferença deixaram de ser incluídas para forçar soma 100 % [p.382].)

## B.3 Saídas
Nenhuma saída do modelo. O capítulo gera **valores de composição** para os Caps. 3, 5, 6, 7 e a biblioteca de alimentos (Cap. 19) e a correção AAcorr.

## B.4 Equações e fórmulas (todas sem número no capítulo, exceto a referência à Eq. 3-1)
Nenhuma é equação do modelo; todas são fórmulas de laboratório ou definição. Transcritas conforme texto e conferidas na imagem.

**F18-1 [p.382–383]** Conversão de nitrogênio em proteína bruta:
```
PB (CP) = N * 6.25
```
N em % ou g/kg (mesma base de PB); 6.25 = 100/16. Fatores reais de 5.18 a 6.38 (Jones 1931); leite 6.38 (6.34 mais apropriado). PIDN e PIDA também = N × 6.25 [p.384].

**F18-2 [p.385]** FDN (e FDA) por gravimetria:
```
FDN = massa do resíduo seco / massa seca da amostra original
FDA = massa do resíduo seco / massa seca da amostra original
```
(Equivalente a "peso do resíduo seco dividido pelo peso seco da amostra original"; expresso com ou sem cinzas.)

**F18-3 [p.386]** Amido pela glicose:
```
Amido = (Glicose_total_após_enzimas - Glicose_livre_da_amostra_original) * 0.9
```
0.9 = 162/180 (anidroglicose / glicose; 18 g/mol de água da hidrólise). QC: valor de 88–92 % de amido a partir da glicose de padrão amido; sacarose pura < 1 %.

**F18-4 [p.386]** Correção do CSA por amido solúvel em água (alimentos cozidos/panificação):
```
Recuperação = g detectado / g real   (maltooligossacarídeos ou amido solubilizado em fenol-ác. sulfúrico, padrão sacarose)
CSA_atribuível_ao_amido_solúvel = Amido_medido_no_extrato_de_água * (1 / Recuperação)
```
Corrigir o amido total ou o CSA para o amido solubilizado. (Opção 1 do livro: medir amido no extrato aquoso e subtrair do valor de amido.)

**F18-5 [p.388]** Digestibilidade in vitro da FDN em um tempo t:
```
DIVFDN(t) = ( FDN%_original - FDN%_residual ) / FDN%_original
```
FDN % do alimento original (base MS); resíduo após incubação de 30 ou 48 h.

**F18-6 [p.387]** MOR — o texto remete à **Eq. 3-1** (já transcrita no bloco ch01-03, p.24, "imagem conferida"):
```
ROM = 100 - Ash - NDF - Starch - (FA / FatFactor) - (CP - 0.64*sNPNCPE)
```
(Transcrição do bloco ch01-03; **não reconferida aqui** — o Cap. 18 descreve apenas: "subtraindo PB, amido, FDN e AG da MO".)

**F18-7 [p.384]** Correção de AA para hidrólise de 24 h (definição):
```
AAcorr = AA_24h * fator_AA (Tabela 18-1)
```
Após correção, a soma dos AA de uma proteína pura ≈ **1.15 × massa de proteína hidrolisada** (água adicionada). Fluxos de AA do modelo = AA "hidratado" (livre). Alternativa do NorFor (não usada): AA anidro = AA livre × (PMol_AA − 18)/PMol_AA, de modo que 1 kg de proteína → 1 kg de AA anidro [p.384].

## B.5 Parâmetros e tabelas

**Tabela 18-1 [p.384] — Fatores de correção propostos para cada AA, para estimar a concentração verdadeira a partir da concentração obtida após hidrólise de 24 h** (adaptado de Lapierre et al., 2019). Conferida na imagem (dpi 150) — OCR trouxe "115", "LIO", "107", "112"; (corrigidos pela imagem: 1.15, 1.10, 1.07, 1.12).

| Aminoácido | Fator de correção (hidrólise 24 h) |
|---|---|
| Alanina | 1.04 |
| Arginina | 1.06 |
| Asparagina + ácido aspártico | 1.02 |
| Cisteína | 1.15 |
| Glutamina + ácido glutâmico | 1.05 |
| Glicina | 1.10 |
| Histidina | 1.07 |
| Isoleucina | 1.12 |
| Leucina | 1.06 |
| Lisina | 1.07 |
| Metionina | 1.05 |
| Fenilalanina | 1.06 |
| Prolina | 1.04 |
| Serina | 1.12 |
| Treonina | 1.07 |
| Triptofano | 1.06 |
| Tirosina | 1.05 |
| Valina | 1.10 |

Notas: um único conjunto de fatores para **todos** os tipos de proteína/matriz (não há fator por alimento) [p.384]. **As composições de AA das tabelas de alimentos do livro (Cap. 19) são relatadas SEM a aplicação destes fatores**; no texto, quando corrigidas, usa-se "AAcorr"; implicações no Cap. 6 [p.384]. Triptofano exige hidrólise alcalina (e Cys/Met oxidação com ácido perfórmico) mesmo com fator de correção [p.383].

### B.5.1 Tabela de tolerâncias/critérios de QC (do texto; sem tabela no livro) [pp.382–390]
| Análise | Critério/erro | Valor | Pág. |
|---|---|---|---|
| Variância de amostragem (silagem de milho e feno) | fração da variância dentro da fazenda | 30–81 % (amostragem diária); 9–37 % (mensal), conforme o analito (St-Pierre e Weiss 2015) | 382 |
| Amostragem | recomendação | várias amostras de silagem ao longo do tempo; usar a média na formulação (Weiss et al. 2014) | 382 |
| Moinho de atrito | equivalência | peneira de 2 mm de atrito ≈ peneira de 1 mm de moinho de facas | 382 |
| FDN, DP (mesma rodada) | % no material original | 0.4 forragens; 0.6 concentrados < 10 % gordura; 0.4 concentrados > 10 % gordura; 0.5 geral | 385 |
| Amido, DP | % no material original | 0.1 (baixo amido); 0.3 (alto amido) | 386 |
| Recuperação de amido de controle | critério | 88–92 % | 386 |
| Sacarose/celulose pura na análise de amido | critério | < 1 % de glicose/amido | 386 |
| Superestimativa de AG por (GB − 1) | erro | até 2 % da MS (forragens e dietas mistas) | 387 |
| Biodisponibilidade de AA-PR por ponto único (in vivo, sangue) | variância | ≥ 20 % | 390 |
| Diluição isotópica (13C) | erro de determinação | 10–12 % | 390 |
| Degradação ruminal de AA-PR com etil-celulose | faixa | 9–37 % para tempos de ≈ 2–12 h | 389 |
| Infusão pós-ruminal: resposta plasmática linear até | doses | ≥ 85 g/d Lys (Borucki Castro 2008); ≥ 30 g/d DL-Met (Rulquin e Kowalczyk 2003); mas quadrática a 180 g/d Lys (King 1991) e a 15 g/d DL-Met (Lapierre 2012: quadrática com componente linear significativo) | 389–390 |

## B.6 Regras de decisão / restrições para o otimizador e para a entrada de dados
1. **Validação de método:** se o usuário informar método diferente do citado (principalmente FDN, FDA, lignina, PIDN/PIDA), alertar para verificar comparabilidade [p.382].
2. **FDN com cinzas:** o modelo espera FDN **com cinzas** (como na literatura de base), salvo amostras contaminadas por solo (usar livre de cinzas ou reamostrar) [p.385]. FDA: usar livre de cinzas se solo ou sílica biogênica (gramíneas C3/C4, cana-de-açúcar) [pp.385–386].
3. **Pré-extração com acetona** para amostras com > 10 % de gordura (FDN e FDA) [p.385].
4. **Secagem ≤ 60 °C** para amostras destinadas a fibra/lignina/proteína [p.383].
5. **Gordura:** usar AG por GC (não GB/extrato etéreo, não GB − 1) [p.387]. Se só houver GB, a conversão antiga superestima AG em até 2 % da MS; o livro não fornece conversão substituta ("não informado").
6. **Soma das frações ≠ 100 %** é normal; MOR absorve o resíduo (inclui erro analítico) [pp.382, 387]. Não forçar fechamento por diferença (sem "extrato livre de N", sem CNF por diferença).
7. **Proteína:** PB = N × 6.25 para todos os alimentos (exceção leite 6.38); fatores específicos só quando conhecidos [p.383]. PIDN/PIDA em % da PB (N × 6.25) [p.384].
8. **AA:** usar fatores da Tabela 18-1 se o usuário informar AA brutos (hidrólise 24 h); a biblioteca do Cap. 19 está **sem correção** — o simulador precisa de um "flag" corrigido/não corrigido para evitar aplicar o fator duas vezes (inferência).
9. **Cinética in situ:** exigir ≥ 5 tempos com 0 e 48 h (+ 72 h forragens); correção de contaminação microbiana obrigatória se FDN > 20 %; sacos em branco; modelo de 1ª ordem [pp.388–389].
10. **FDNfa (SPPS):** usar como entrada a % da MS retida em 19, 8 e 4 mm + bandeja medida segundo protocolo (1.4 L; 40 agitações; 1.1 agitação/s; 17 cm) [pp.387–388].
11. **Amostragem:** várias amostras de silagem/feno ao longo do tempo e média na formulação [p.382].
12. **NIRS para minerais:** tratar como estimativa não definitiva [p.388].
13. **P:** quando possível separar P inorgânico (HCl 0.5 M) e orgânico (total − inorgânico) para o modelo de P do Cap. 7 [p.388].

## B.7 Lógica e fluxo
- Ordem sugerida de uso das análises: amostragem → MS (≤ 60 °C para amostras de fibra/proteína) → moagem (1 mm facas p/ FDN, FDA, DIVFDN; 2 mm p/ in situ; 1 mm atrito/0.5 mm facas/0.4 mm p/ amido e CSA) → cinzas/MO → N (PB), PIDN, PIDA → FDN (→ FDA → lignina) → amido, CSA → AG (GC) → minerais → [opcional] DIVFDN, frações A/B/C/kd, PNDRd, AA hidrolisados (→ AAcorr). MOR é calculada depois por diferença (Eq. 3-1).
- Dependências (cruz.): FDN, amido, AG, PB, cinzas → MOR (Eq. 3-1, Cap. 3) → EB/ED; lignina (Eq. 3-3a) **ou** DIVFDN 48 h (Eq. 3-3b) → digestibilidade basal da FDN; frações A/B/C, kd e PNDRd → PDR/PNDR/PM (Cap. 6); AAcorr → perfil de AA (Cap. 6); SPPS → FDNfa (Cap. 5); P inorgânico/orgânico → coeficiente de absorção do P (Cap. 7, CA 0.84/0.68 — conforme bloco ch07).
- O capítulo **não** descreve o cálculo de CSDN, FDNf (FDN de forragem), PDR/PNDR. A relação entre "digestibilidade da FDN" medida in vitro e a usada no modelo está nas Eq. 3-3 (outro bloco).

## B.8 Limitações, incertezas e mudanças vs. NRC 2001
- **Mudanças vs. NRC 2001:** (i) GB − 1 para estimar AG **não é mais recomendado**; AG por GC de ésteres metílicos é o padrão [p.387]; (ii) fatores de correção de AA por hidrólise de 24 h agora **um por AA**, aplicáveis a todas as matrizes (Tabela 18-1; antes Rowan et al. 1992 propôs fatores por tipo de amostra) [p.384]; (iii) proteína solúvel **não é usada** no suprimento de nutrientes [p.384]; (iv) FDNfa (SPPS) recomendado para o sistema de FDN fisicamente ajustada [p.387]; (v) padronização in situ reiterada ("fortemente recomendada, mas muitas vezes não seguida"), com correção microbiana quando FDN > 20 % [p.389]; (vi) valores de PNDRd pós-2001 obtidos de sacos recuperados das fezes [p.389]; (vii) P fracionado em orgânico e inorgânico [p.388].
- **Admite não saber:** métodos para AA-PR sem consenso; resultados variam entre métodos [p.389]; método de Ross (2013) sem avaliação revisada por pares → **sem recomendação** e **não usado** no modelo [p.389]; correção de perdas de partículas pequenas de sacos in situ requer mais trabalho (Maxin 2013) [p.388]; diferenças de kd/fração C para partículas pequenas; fatores de correção de AA por matriz "digno de investigação mais aprofundada" [p.384]; PNDRd precisa ser padronizada e avaliada por tipo de alimento; poucas comparações com in vivo (cânula ileal em vacas leiteiras limitada) [p.389].
- **Não está no modelo (só discussão):** proteína solúvel; AA anidro (NorFor); métodos in vivo de AA-PR (regressão de concentração plasmática, resposta da produção de proteína do leite, dose de pulso em abomaso, diluição isotópica, seleno-Met); MIR para AG do leite; patulina etc.

## B.9 Conceitos e evidências relevantes
- Variância amostral explica **30–81 %** da variância dentro da fazenda em silagem de milho e feno com amostragem diária (9–37 % mensal); amostrar mais e usar média [p.382]. Alimentos de consumo rápido: a análise é retrospectiva [p.382].
- Hidrólise: 1 kg de proteína → ≈ 1.15 kg de AA (água adicionada); recuperação efetiva < 1 kg não significa NNP [p.384].
- Estudos de múltiplas hidrólises: 4–19 tempos; 2–168 h; melhores estimativas = valor máximo de cada AA ou equação com taxa de hidrólise e perda de AA lábeis [p.384].
- α-amilase remove amido do resíduo de FDN; sulfito solubiliza proteína [p.385].
- Infusão pós-ruminal de AA: resposta plasmática linear até ≥ 85 g/d Lys e ≥ 30 g/d DL-Met; Whitehouse (2016) propõe expressar Lys como razão a AA totais (excl. Lys) e Met+Cys como razão aos AA totais (excl. sulfurados) [pp.389–390].
- Proteína do leite como resposta (precisa de animais deficientes no AA); equações atualizadas do livro "esperam reduzir esse problema" [p.390].
- Mistura mecânica de Lys-PR e exposição à TMR (menor MS → maior efeito) aumentam a liberação ruminal in situ de Lys (Ji 2016) [p.390].

## B.10 Dúvidas/riscos de OCR (Cap. 18)
- Tabela 18-1: OCR trouxe "115", "LIO", "107", "112" — **corrigidos pela imagem** (Cys 1.15; Gly 1.10; His 1.07; Ser 1.12). Demais 14 valores iguais no OCR e na imagem.
- ⚠ p.383: "A secagem de amostras a < 60 °C resultará em valores de MS mais baixos" — confere na imagem; sentido físico coerente.
- ⚠ p.386: "peneira de 0.4 mm" (amido e CSA) — confere na imagem; unidade não informada em outro sentido (provavelmente mm de abertura de peneira de moinho de facas).
- ⚠ p.387: o texto de MOR diz "(ver Equação 3-1) subtraindo PB, amido, FDN e AG da MO"; a Eq. 3-1 completa (com FatFactor e NNP) foi transcrita do bloco ch01-03 e **não foi reconferida contra a imagem de p.24 aqui**.
- p.387: Cr e P (Considerações especiais dos Minerais) conferidos na imagem.
- ⚠ p.388: procedimento do SPPS — 40 agitações = 5 agitações × 8 posições (conferido na imagem: "total de oito vezes ... 40 agitações"); a resposta do modelo FDNfa (Tabela 5-2, Cap. 5) usa % em 19 mm e 8 mm; a peneira de 4 mm não tem uso descrito no Cap. 18.
- ⚠ p.388: "incubações ... no rúmen ventral de pelo menos dois animais ... alimentados com dietas caracterizadas" — confere; número mínimo de réplicas por saco/tempo **não informado**.
- ⚠ p.388–389: "Quando a FDN excede 20 % em um alimento, o comitê recomenda que os estudos sejam corrigidos para contaminação bacteriana" — confere; a técnica de correção não é detalhada (15N, qPCR citadas como promissoras).
- ⚠ Não há faixas aceitáveis de composição de alimentos (ex.: PB, FDN típicos) neste capítulo — estão no Cap. 19 (fora do escopo).
- ⚠ Os valores do Cap. 18 não foram usados para "ajustar" amostras de controle (livro proíbe usar recuperação de controle de amido para corrigir amostras) [p.386].

---

COBERTURA: páginas impressas lidas 369–392 (todas; pp.379–381 e 391–392 são apenas referências, percorridas só por OCR sem leitura de imagem). Texto (369–378, 382–390) lido por OCR e todas as páginas numéricas conferidas na imagem: 370–378, 382–390 (impressas); 369 só por OCR (página introdutória, sem números além de notas de rodapé). Não há equações numeradas nem tabelas de coeficientes no Cap. 17; Cap. 18 tem 1 tabela (18-1) e fórmulas de laboratório não numeradas (F18-1 a F18-7). Itens deduzidos ou cruzados com outros blocos estão marcados ("cruz.", "inferência"). Ficou de fora: referências bibliográficas (pp.378–381, 390–392) — percorridas, não transcritas. Nenhuma página ficou ilegível.

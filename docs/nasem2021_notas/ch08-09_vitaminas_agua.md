# Notas técnicas NASEM 2021 (Bovinos Leiteiros, 8ª ed., PT-BR) — Cap. 8 (Vitaminas) e Cap. 9 (Água)

**Páginas impressas cobertas:** 180–218 (Cap. 8: p.180–195 texto, p.196–203 referências; Cap. 9: p.204–215 texto, p.215–218 referências).
**Convenções:** decimal = PONTO, milhar = VÍRGULA. Sinais, expoentes e coeficientes de TODAS as equações e tabelas numéricas foram conferidos contra a imagem da página (dpi 150–320). Valores marcados "(derivado)" foram calculados por mim a partir do livro e NÃO estão impressos nele. Siglas PT usadas pelo livro: IA = ingestão adequada; PC = peso corporal; PL = produção de leite; ALI = água livre ingerida (água bebida, kg/d); ITA = ingestão total de água (água bebida + água dos alimentos); IMS; MS% = % de matéria seca da dieta.

**Usado diretamente no modelo?**
- Cap. 8 Vitaminas: **sim** para as IAs de vitaminas A, D e E (Eq. 8-1 a 8-3) e para os fatores de conversão a UI (Tabela 8-1). **Não** para vitaminas B, colina e vitamina C (só discussão; o comitê não estabeleceu IA nem exigência) e para β-caroteno (IA não estabelecida).
- Cap. 9 Água: **sim** para as equações de ALI (Eq. 9-1, 9-2, 9-3). **Parcial** para perdas de água (Eq. 9-4 e Figura 9-1 são descritivas/de apoio). **Parcial** para qualidade da água (Tabelas 9-2, 9-3, 9-5 funcionam como limites de alerta; não entram em cálculos de exigência).

---

# CAPÍTULO 8 — VITAMINAS (p.180–195)

## 8.1 Papel no simulador
Calcular a **Ingestão Adequada (IA)** de vitaminas lipossolúveis A, D e E em UI/d, **expressa como vitamina SUPLEMENTAR** (não total), em função de PC, produção de leite e categoria/estágio (novilha, vaca seca, pré-parto, lactação). Converter massa de cada fonte comercial em UI (Tabela 8-1) para comparar o fornecido pela dieta com a IA. O livro NÃO oferece exigências para vitaminas B, colina, vitamina C nem IA de β-caroteno. [p.180–195]

## 8.2 Entradas

| Variável | Símbolo/sigla | Unidade | Definição | Faixa/valores típicos | Pág. |
|---|---|---|---|---|---|
| Peso corporal | PC | kg | PC do animal | exemplo do livro: vaca de 625 kg | [p.183, 186, 189] |
| Produção de leite | PL (produção de leite) | kg/d | Usada só na Eq. 8-1b (vit. A), acima de 35 kg/d | limiar 35 kg/d | [p.183] |
| Categoria / estágio fisiológico | — | categórico | novilha de reposição/em crescimento; vaca seca; pré-parto (dentro de 3 semanas do parto); vaca em lactação | — | [p.183, 186, 189] |
| Consumo de forragem fresca/pasto (para ajuste de vit. E) | — | kg MS/d | MS de pasto fresco consumida | não informado (faixa) | [p.189] |
| Massa da fonte de vitamina (suplemento) | — | µg ou mg | Para converter em UI | — | [p.181] |
| Tipo/forma da fonte (retinol acetato, palmitato, colecalciferol, RRR ou all-rac tocoferil etc.) | — | categórico | Define o fator da Tabela 8-1 | — | [p.181] |
| UI rotulada de formas RRR de vit. E | — | UI | Rótulo usa fator padrão; precisa ser reconvertido (ver 8.4/8.6) | — | [p.188] |

## 8.3 Saídas

| Variável | Símbolo | Unidade | Definição | Valores típicos | Pág. |
|---|---|---|---|---|---|
| IA de vitamina A suplementar | IA Vit A | UI/d | Eq. 8-1a/8-1b | 110 UI/kg PC (≈69,000 UI/d p/ vaca de 625 kg) | [p.183] |
| IA de vitamina D suplementar (assumida D3) | IA Vit D | UI/d | Eq. 8-2a/8-2b | 30 x PC (novilha/seca); 40 x PC (lactação) | [p.186] |
| IA de vitamina E suplementar | IA Vit E | UI/d | Eq. 8-3a/b/c | ≈1,000 / 2,000 / 500 UI/d (seca / transição / lactação) | [p.189] |
| Vitamina fornecida (por fonte) em UI | — | UI/d | massa / fator da Tabela 8-1 | — | [p.181] |

## 8.4 Equações (todas verificadas na imagem)

**Eq. 8-1a — IA vitamina A, PL ≤ 35 kg/d (inclui vacas secas)** [p.183]
```
IA_VitA (UI/d) = 110 * PC            (se PL <= 35 kg/d, incluindo vacas secas)
```
PC em kg; 110 UI/kg PC. O livro também mantém 110 UI/kg PC para **novilhas em crescimento** (mantido do NRC 2001 por falta de dados recentes; "especialmente a IA para novilhas de reposição permanece mal definida") [p.182]. A IA assume forragens CONSERVADAS; "provavelmente excede" a exigência de bovinos em pastejo (forragem fresca tem muito β-caroteno), mas não há ajuste numérico para pasto [p.182].
Origem: NRC 2001 (110 UI/kg PC; baseado em pressão do líquor, edema papilar, produção de leite, imunidade, saúde da glândula mamária, reprodução e destruição ruminal esperada). Mantida sem mudança "devido à falta de dados novos" para secas [p.182–183].

**Eq. 8-1b — IA vitamina A, PL > 35 kg/d** [p.183]
```
IA_VitA (UI/d) = 110 * PC + 1000 * (PL - 35)        (se PL > 35 kg/d)
```
PL em kg/d; 1,000 UI por kg de leite acima de 35 kg/d. Fundamento: leite tem 3–11 mg retinol/kg de gordura ≈ 0.1–0.4 mg/kg de leite (3.7% gord.) ≈ 1,000 UI/kg leite; vaca com 35 kg leite secreta ≈10 mg retinol ≈ 30,000 UI/d (substancial vs. IA ≈ 69,000 UI p/ 625 kg) [p.183]. Continuidade: em PL = 35 as duas equações coincidem.

**Eq. 8-2a — IA vitamina D (D3 suplementar), novilhas de reposição e vacas secas** [p.186]
```
IA_VitD (UI/d) = 30 * PC
```
**Eq. 8-2b — IA vitamina D, vacas em lactação** [p.186]
```
IA_VitD (UI/d) = 40 * PC
```
PC em kg. IA expressa como vit. D **suplementar**, assumindo **vitamina D3** (colecalciferol); se D2 for usada "as taxas de suplementação provavelmente deverão ser aumentadas" (D2 ≈ metade da eficácia de D3 em elevar 25-OH-D no plasma; sem fator numérico adotado) [p.184–185]. NRC 2001 era 30 UI/kg PC para todas as categorias. Aumento p/ lactação baseado em Nelson et al. (2016): 20,000 UI/d nem sempre mantém 25-OH-D >30 ng/mL; ≈30,000 UI/d mantém [p.186]. Sol/pasto de verão NÃO é considerado no cálculo [p.185].

**Eq. 8-3a — IA vitamina E, vacas secas** [p.189]
```
IA_VitE (UI/d) = 1.6 * PC
```
**Eq. 8-3b — IA vitamina E, animais em pré-parto dentro de 3 semanas do parto** [p.189]
```
IA_VitE (UI/d) = 3.0 * PC
```
**Eq. 8-3c — IA vitamina E, vacas em lactação e novilhas em crescimento** [p.189]
```
IA_VitE (UI/d) = 0.8 * PC
```
PC em kg. Equivalem a ≈1,000, 2,000 e 500 UI/d para vacas secas, em transição e lactantes. IA para secas e lactantes = igual NRC 2001; a de pré-parto vem de Baldi et al. (2000): 3.0 UI/kg PC ≈ 2,000 UI/d nas últimas 2–3 semanas (menor dose com benefício; faixa benéfica citada 3.2–6.4 UI/kg PC; "dificulta estabelecer IA para periparto") [p.189].

**Regra textual (sem número de equação) — ajuste da IA de vit. E por forragem fresca/pasto** [p.189]
```
IA_VitE_ajustada (UI/d) = IA_VitE (Eq. 8-3a/b/c) - 50 * IMS_pasto_fresco (kg MS/d)
```
Texto: "a necessidade de suplementação de vitamina E foi reduzida em 50 UI/d para cada quilograma de MS de pasto fresco consumido"; premissa: forragem fresca fornece 35 mg/kg (50 UI/kg) mais α-tocoferol que feno/silagem. O livro NÃO diz explicitamente se há piso em zero nem se vale para pré-parto (⚠ ver item 10).

## 8.5 Parâmetros e tabelas

**Tabela 8-1 — Fatores de conversão de fontes comuns de vitaminas para UI (massa por 1 UI)** [p.181] (conferida na imagem)

| Vitamina | Fonte | Padrão (1 UI =) | Usada nessa edição (1 UI =) |
|---|---|---|---|
| A | β-caroteno | 2.5 µg | 2.5 µg (nota a) |
| A | All-trans retinol | 0.3 µg | 0.3 µg |
| A | All-trans retinol acetato | 0.344 µg | 0.344 µg |
| A | All-trans retinol palmitato | 0.550 µg | 0.550 µg |
| D | Colecalciferol (Vit. D3) | 0.025 µg | 0.025 µg |
| D | Ergocalciferol (Vit. D2) | 0.025 µg | 0.025 µg (nota a) |
| E | RRR-tocoferol | 0.67 mg | **0.45 mg** (nota b) |
| E | RRR-tocoferil acetato | 0.74 mg | **0.50 mg** (nota b) |
| E | RRR-tocoferil succinato | 0.83 mg | **0.55 mg** (nota b) |
| E | All-rac tocoferol | 0.91 mg | 0.91 mg |
| E | All-rac tocoferil acetato | 1.00 mg | 1.00 mg |
| E | All-rac tocoferil succinato | 1.12 mg | 1.12 mg |

Notas: (a) "A potência é provavelmente superestimada usando esse fator de conversão, mas os dados são inadequados para quantificar (ver texto)" — aplicada a β-caroteno e ergocalciferol. (b) "Com base em dados de bovinos, as formas RRR da vitamina E são mais potentes do que os fatores de conversão padrão (ver texto)". Só as 3 formas RRR mudaram vs. padrão.

**Uso:** UI = massa da fonte / fator (massa por UI). Equivalências derivadas (derivado, não impressas): 1 mg β-caroteno = 400 UI (o texto confirma: "1 mg de β-caroteno = 400 UI" p.181; humanos: 277 UI ou 83 µg retinol); retinol 3.333 UI/µg; retinil acetato 2.907 UI/µg; palmitato 1.818 UI/µg; D2/D3 40 UI/µg (40,000 UI/mg); vit. E (UI/mg, edição atual): RRR-tocoferol 2.222; RRR-acetato 2.000; RRR-succinato 1.818; all-rac tocoferol 1.099; all-rac acetato 1.000; all-rac succinato 0.893.
**Conversão de UI rotulada de formas RRR** (derivado): rótulo usa o fator padrão; para a escala desta edição multiplicar UI rotulada por 0.67/0.45 = 1.489 (RRR-tocoferol), 0.74/0.50 = 1.48 (acetato), 0.83/0.55 = 1.509 (succinato). O texto apenas diz que "os usuários precisarão converter a UI rotulada em unidades usadas na Tabela 8-1" [p.188]. Formas RRR são tratadas como ≈2x mais ativas que all-rac (só isômeros 2R ativos) [p.188].
Exemplo do livro (consistente): 1,600 mg RRR-α-tocoferol/d ≈ 3,500 UI (1600/0.45 = 3,556) [p.189].

**Tabela 8-2 — Ingestão, fluxo duodenal e síntese ruminal aparente de vitaminas B em vacas leiteiras (mg/kg de IMS)** [p.190] (conferida; só informativa, não entra em cálculo; valores negativos = destruição ruminal > ingestão)

| Vitamina | Ingestão | Fluxo duodenal | Síntese ruminal aparente |
|---|---|---|---|
| Tiamina | 1.3 a 3.8 | 0.8 a 7.8 | −1.5 a 4.2 |
| Riboflavina | 4 a 106 | 3 a 87 | −50 a 29 |
| Niacina | 22 a 170 | 47 a 146 | −123 a 120 |
| Vitamina B6 | 2.6 a 17.6 | 0.7 a 7.7 | −14.1 a 1.3 |
| Biotina | 0.2 a 7.0 | 0.2 a 6.6 | −0.9 a 0.2 |
| Folatos | 0.2 a 1.1 | 0.9 a 2.4 | 0.5 a 1.7 |
| Vitamina B12 | abaixo ou próximo ao nível de detecção (nota c) | 0.1 a 4.8 | 0.1 a 4.8 (nota d: dieta com Co 0.17–2.5 mg/kg MS) |

Sem dados para ácido pantotênico. Fontes: Steinberg e Kaufman 1977; Breves 1981; Santschi 2005a; Schwab 2006; Lebzien 2006; Niehoff 2013; Beaudet 2016; Castagnino 2016a,b, 2017.

## 8.6 Regras de decisão / restrições para o otimizador

| Regra | Condição | Pág. |
|---|---|---|
| Vit. A: usar IA como **mínimo suplementar** (110 UI/kg PC; +1,000 UI por kg de leite >35 kg/d) | todas as categorias; assume forragem conservada | [p.182–183] |
| Vit. A, limites de segurança (não há UL formal): ≈500,000 UI/d (≈6.5 x IA) no período seco reduziu PL na lactação seguinte; ≈1,300 UI/kg PC (≈12 x IA) → sinais de osteoporose (NRC 1987); 3 milhões UI/d por 10 d em bezerros de 1 semana → fechamento precoce da placa de crescimento | usar como teto de alerta | [p.183–184] |
| Vit. D: IA suplementar como D3; 30 x PC (novilhas/secas), 40 x PC (lactação) | — | [p.186] |
| Vit. D, tolerância: 50,000 UI D3/d (80 UI/kg PC) bem tolerado; 250,000 UI/d (400 UI/kg) não; 80,000 UI D2/d (160 UI/kg) leve queda de PL (Hibbs e Conrad 1983); NRC 1987: 2,200 UI/kg dieta (uso longo, >60 d) e 25,000 UI/kg dieta (curto prazo); parenteral: dose tolerável ≥100 x menor que oral | máximo tolerável é inversamente relacionado a Ca e P da dieta | [p.186–187] |
| Vit. D, indicadores plasmáticos de 25-OH-D: <5 ng/mL = deficiência; 200–300 ng/mL = toxicose; alvo ≈30 ng/mL (faixa ideal não estabelecida para bovinos; humanos 30–50) | uso de monitoramento, não do simulador | [p.186] |
| Vit. D: vacas a pasto no verão, com várias horas/dia ao sol, provavelmente dispensam suplementação (vacas leiteiras a 56° lat. em junho precisaram ≈90 min de sol/d ao redor das 13 h para manter 25-OH-D) | qualitativo; não quantificado no cálculo | [p.184–185] |
| Vit. E: IA suplementar 0.8 (lactação e novilhas em crescimento), 1.6 (secas), 3.0 (pré-parto ≤3 sem) UI/kg PC | — | [p.189] |
| Vit. E, pasto: reduzir a suplementação em 50 UI/d por kg MS de pasto fresco consumido | forragem fresca | [p.189] |
| Vit. E, UL: sem estudos em ruminantes; ratos → ≈75 UI/kg PC/d (NRC 1987); 2,500–6,000 UI/d reduziram vit. A e β-caroteno nos tecidos; 3,000 UI/d por ≈60 d em secas aumentou risco de mastite vs 135 UI/d | alerta | [p.190] |
| Vit. E total recomendada (dieta basal + suplemento) ≈2.6 UI/kg PC no fim da gestação e lactação; dieta basal fornece em média ≈1.8 UI/kg PC (0.8 feno muito seco a 2.8 pastagem) em lactantes e ≈1.0 (0.5–2.3) em secas | informativo | [p.189] |
| β-caroteno: **sem IA** (dados inconsistentes); colina, vitaminas B, vit. C: sem exigência/IA | não modelar como exigência | [p.183, 195, 196] |
| Colina: colina desprotegida é "inútil" (degradação ruminal extensa); colina PR (rumen-protegida) ≈13 g/d de colina verdadeira → +≈1.5 kg/d leite, +≈0.5 kg/d IMS (metanálises Sales 2010 e Arshad 2020, principalmente vacas de transição) | opcional/fora do núcleo | [p.194–195] |

## 8.7 Lógica e fluxo
1. Entradas de outros capítulos: PC, PL, categoria/estágio (o simulador já os tem).
2. Escolher categoria: novilha → Eq. 8-1a, 8-2a, 8-3c; vaca seca → 8-1a, 8-2a, 8-3a; pré-parto ≤3 sem → (8-1a), 8-2a, 8-3b (o livro não dá equação separada de vit. A/D para pré-parto; usa a de vaca seca); lactação → 8-1a ou 8-1b conforme PL ≤/> 35, 8-2b, 8-3c.
3. Se houver pasto fresco, abater 50 UI/d de vit. E por kg MS de pasto.
4. Comparar com UI suplementada = Σ(massa da fonte / fator da Tabela 8-1). Conferir tetos (UL) como alertas.
5. Vitaminas não dependem de IMS nem de energia; independentes dos demais blocos.

## 8.8 Limitações, incertezas e mudanças vs. NRC 2001
- **Mudança vs. NRC 2001:** vit. A — nova Eq. 8-1b (acréscimo por leite >35 kg/d); vit. D — IA de lactação sobe de 30 para 40 UI/kg PC (novilhas/secas ficam em 30); vit. E — mantidas as IAs de seca e lactação (NRC 2001), e IA explícita para pré-parto (3.0 UI/kg PC); **Tabela 8-1: fatores de RRR-tocoferóis alterados** (0.45/0.50/0.55 mg/UI vs. padrão USP 0.67/0.74/0.83) com base em dados de bovinos [p.183, 186, 188–189].
- Termo "IA" em vez de exigência porque faltam dados (conteúdo de β-caroteno/tocoferol/vit. D dos alimentos é variável e raramente analisado) [p.182, 185, 189].
- Fatores de β-caroteno (1 mg = 400 UI) e de ergocalciferol provavelmente superestimam a potência; dados insuficientes para quantificar [p.181, nota a].
- Contribuições de sol (vit. D), de forragem fresca (vit. A: não quantificada; vit. E: −50 UI/kg MS) não entram além do ajuste de vit. E [p.185, 189].
- IA de vit. A para novilhas "mal definida"; faltam dados de novilhas leiteiras [p.182–183]. Estudos de vit. A usaram vacas <35 kg leite/d [p.183].
- Não há modelo de biodisponibilidade: vit. A destruída no rúmen ≈20% (dietas ricas em forragem) a ≈70% (50–70% de concentrado) in vitro; ≈60% in vivo (novilhos, feno + milho); perda de atividade em premix ≈3.5%/mês (sem microminerais) a ≈9%/mês (com microminerais inorgânicos); vit. E: 1–2%/mês, até 6%/mês em extrusados [p.181, 187]. Não incorporados ao cálculo.

## 8.9 Conceitos e evidências relevantes (curtos)
- Vit. A: biodisponibilidade <100%; 1 mg β-caroteno = 400 UI (humano revisado para 277 UI) [p.181]. Retinol sérico baixo associado a retenção de membranas fetais, mastite, claudicação [p.182].
- Vit. A em vacas secas (110 UI/kg PC mantida): feto, colostro (retinol do colostro correlaciona com ingestão no período seco), 170,000 UI/d aumentou PL (Oldham 1991), risco de retenção de placenta/mastite com baixo status [p.183].
- Vit. D é pró-hormônio; 25-OH-D plasmática é o bom indicador; deficiência → raquitismo (jovens) e osteomalácia (adultos); 25-OH-D dietética (calcidiol) disponível, mas atividade relativa em UI/massa "não é conhecida" [p.184–185]. 10,000 UI/d (≈16 UI/kg) basta para metabolismo de Ca no final da gestação na maioria dos casos; 40,000 UI D2/d (50–70 UI/kg) produziu mais leite no estudo de Hibbs e Conrad [p.186].
- Vit. E: antioxidante lipossolúvel; α-tocoferol de forragem fresca 20–150 mg/kg MS; silagem de milho ≈9–20; feno geralmente <25; grãos e farelos <6; secagem/ensilagem reduz em 25–65% [p.187]. Suplementação periparto (1,000–4,000 UI/d) melhora função de neutrófilos, reduz retenção de membranas fetais (metanálise Bourne 2007) e mastite (maioria dos estudos) [p.188–189]. Colostro: 5–7.5 mg α-tocoferol/kg (≈100–150 mg/10 kg) [p.189]. 3,000–11,000 UI/d reduziram parcialmente (não eliminaram) a depressão de gordura do leite com óleos poli-insaturados (<3% óleo adicionado); sem efeito com >6% óleo [p.189].
- Vitaminas B (sem IA): síntese ruminal grande e variável; deficiência clínica rara em adultos. Perdas ruminais de suplementos: tiamina escapa 52–68%; riboflavina 99% destruída; niacina >90% destruída; ácido pantotênico só 22% (ou 15% in vitro) escapa; B6 60–100% escapa; biotina biodisponibilidade ≈45%; ácido fólico destruição ≈72% (estimada); B12 depende de Co (só 11% do Co ingerido vira corrinoides, 4% vit. B12) [p.190–194]. Doses citadas com resposta: niacina 12 g/d (modesto aumento de gordura/proteína/leite; 6 g/d sem efeito; metanálise 27 estudos); biotina 20 mg/d (↑ IMS, leite, gordura e proteína; 10–20 mg/d saúde de cascos); ácido fólico + B12 combinados (parenteral, semanal) aumentam leite no início da lactação; tiamina 150–300 mg/d (resultados variáveis); tiamina injetável 2 mg/kg PC reverte poliencefalomalácia [p.191–194].
- Colina: não essencial (sintetizada), extensamente degradada no rúmen; colina do leite 70–100 mg/L [p.194–195]. Vit. C: sintetizada no fígado; bezerros só após ≈3 semanas; "dados não suportam suplementação rotineira" [p.195–196].

## 8.10 Dúvidas/riscos de OCR (cap. 8)
- ⚠ OCR perdeu os símbolos "≤" (Eq. 8-1a), "µ" e subscritos; **todos** foram corrigidos pela imagem (corrigido pela imagem). Tabela 8-1: OCR omitiu as notas a/b nas linhas certas; atribuição conferida na imagem.
- ⚠ Pasto e vit. E: o texto não declara piso em zero nem aplicação à IA de pré-parto/vit. A/D (requer decisão de implementação).
- ⚠ "Eq. 8-3b" diz "dentro de 3 semanas do parto" mas o texto-base cita "últimas 2 a 3 semanas" (Baldi) e "cerca de 2 semanas" para o benefício; usar 3 semanas (equação).
- ⚠ Aritmética do livro: "500,000 UI (≈6.5 x IA atual)" implica IA ≈77,000 UI/d (vaca ≈700 kg), enquanto o exemplo da p.183 usa 625 kg (IA ≈69,000 → razão 7.3). Anotado apenas; não afeta equações.
- ⚠ Tabela 8-2, coluna ingestão de B12: "—" com nota c ("abaixo ou próximo ao nível de detecção"); o texto do OCR tinha fundido colunas — conferido na imagem.
- ⚠ Ácido fólico "2 a 6 mg/kg de PC desprotegido" (p.193) como impresso; unidade/dia não explícita (discussão, não usada no modelo).

---

# CAPÍTULO 9 — ÁGUA (p.204–215)

## 9.1 Papel no simulador
Prever a **água livre ingerida (ALI, kg/d)** de vacas em lactação e secas (equações 9-1, 9-2, 9-3) a partir de IMS, composição da dieta (MS%, Na+K, PB%), leite e temperatura; descrever perdas de água; e **avaliar a qualidade da água** (STD, sulfato, nitrato, minerais, microbiologia) por faixas/limites de alerta. Não há equação para bezerras e novilhas. [p.205–215]

## 9.2 Entradas

| Variável | Símbolo/sigla | Unidade | Definição | Faixa/valores típicos | Pág. |
|---|---|---|---|---|---|
| Ingestão de matéria seca | IMS | kg/d | Eq. 9-1, 9-3 | não informado (faixa) | [p.206] |
| Produção de leite | Leite | kg/d | Eq. 9-2 | — | [p.206] |
| % MS da dieta | MS% | % | percentual de matéria seca da dieta (como fornecida) | — | [p.206] |
| % PB da dieta | PB% | % da MS | teor de PB da dieta | — | [p.206] |
| Soma de Na e K da dieta | NaK | mEq/kg MS | (%Na/0.023 + %K/0.039) x 10 | derivado: 1% Na = 434.8 mEq/kg | [p.206] |
| Temperatura ambiente média diária | TAM | °C | Eq. 9-1, 9-2, 9-3 | — | [p.206] |
| Dias em lactação | DEL | d | Eq. 9-2 (símbolo não definido na nota da tabela; ver ⚠) | — | [p.206] |
| Temperatura de referência (termo quadrático) | TAMC² = (TMP − 16.4)² | °C² | Eq. 9-3 | 16.4 °C | [p.206] |
| Temperatura (ar) e umidade relativa | Ta, UR | °C, % | Eq. 9-4 | — | [p.209] |
| Concentrações de analitos da água | — | mg/L | Tabelas 9-2, 9-3, 9-5 | — | [p.210–213] |
| Categoria animal (bezerra com leite/pós-desmame, lactante, seca) | — | categórico | escolher equação/regra | — | [p.205–207] |

## 9.3 Saídas

| Variável | Símbolo | Unidade | Definição | Pág. |
|---|---|---|---|---|
| Água livre ingerida | ALI | kg/d | água de reservatório/bebedouro (exclui água do alimento) | [p.205] |
| Ingestão total de água | ITA | kg/d | ALI + água dos alimentos; só usada para repartir perdas (Fig. 9-1); não há equação | [p.208] |
| Perda respiratória de água | PRA | g/h | Eq. 9-4 | [p.209] |
| Alertas de qualidade da água | — | classe | por analito (Tabelas 9-2, 9-3, 9-5) | [p.210–213] |

## 9.4 Equações (Tabela 9-1 e Eq. 9-4; todas verificadas na imagem a 200–320 dpi)

Notas de rodapé da Tabela 9-1 [p.206]: ALI em kg/d; IMS (kg/d), PV [= PC] (kg), Leite = produção de leite (kg/d), MS% = % de MS da dieta, CONC% = teor de concentrado da dieta (% da MS), PB% = PB da dieta (% da MS), Cinzas = cinzas totais da dieta (% MS), NaI = ingestão de sódio (g/d), TAM = temperatura ambiente média diária (°C), mnTAM = temperatura ambiente mínima diária (°C), DJ = data juliana, TAMC² = (TMP − 16.4)², NaK = soma da concentração de Na e K na dieta, mEq/kg MS, (%Na/0.023 + %K/0.039) x 10. Tabela "adaptada de Appuhamy et al. (2016)". Estimativas de ALI do livro são uma média; temperatura média, mínima e máxima são correlacionadas, "uma medida provavelmente é adequada" [p.205].

### Equações RECOMENDADAS (escolhidas pelo livro para uso/software)

**Eq. 9-1 — vacas em lactação, COM estimativa confiável de IMS** (Appuhamy et al. 2016) [p.206]
```
ALI = -91.1 + (2.93 * IMS) + (0.61 * MS%) + (0.062 * NaK) + (2.49 * PB%) + (0.76 * TAM)
```
**Eq. 9-2 — vacas em lactação, SEM estimativa confiável de IMS** (Appuhamy et al. 2016) [p.206]
```
ALI = -60.2 + (1.43 * Leite) + (0.064 * NaK) + (0.83 * MS%) + (0.54 * TAM) + (0.08 * DEL)
```
**Eq. 9-3 — vacas secas** (Appuhamy et al. 2016) [p.206]
```
ALI = (1.16 * IMS) + (0.23 * MS%) + (0.44 * TAM) + (0.061 * TAMC^2)      onde TAMC^2 = (TAM - 16.4)^2
```
(sem intercepto, como impresso; a nota da tabela escreve "(TMP − 16.4)²", provável erro de grafia para TAM.)
Regra de escolha (texto, p.205–206): "quando estimativas confiáveis de IMS estão disponíveis, a Equação 9-1 deve ser usada; a Equação 9-2 quando não estiverem". As duas são diferentes das alternativas por incluírem **K (e Na) dietético** (K aumenta consumo de água e taxa de passagem de líquido ruminal). Para vacas secas: Eq. 9-3 recomendada porque os dados de desenvolvimento cobriram maior variedade de IMS, ambiente e dieta; "faltam estudos publicados medindo ALI em vacas secas" [p.206]. Estatísticas de ajuste (n, R², RMSE) NÃO são citadas no livro; o texto remete à avaliação independente de Appuhamy et al. (2016).

Verificação numérica minha (derivado, para teste de implementação): dieta com 0.4% Na e 1.3% K → NaK = 507.2 mEq/kg; Eq. 9-1 com IMS = 25, MS% = 50, PB% = 17, TAM = 15 → 97.8 kg/d; Eq. 9-2 com Leite = 35, MS% = 50, TAM = 15, DEL = 100 → 79.9 kg/d; Eq. 9-3 com IMS = 12, MS% = 50, TAM = 15 → 32.1 kg/d (TAM = 28 → 45.9 kg/d).

**Eq. 9-4 — perda respiratória de água (PRA), Berman (2006)** [p.209]
```
PRA = 0.41 - 0.02 * Ta + 0.0005 * Ta^2 - 0.004 * UR + 0.00004 * UR^2
```
PRA em g/h (como impresso no texto: "PRA (g h^-1)"); Ta em °C; UR em %. Obtida de dados de câmaras climáticas; PRA aumenta com Ta, diminui com UR, sem interação [p.209]. Base do animal (por animal, por kg PC^0.75 etc.) NÃO é informada (⚠). Não é usada para calcular ALI (derivado: Ta = 28 °C, UR = 60% → 0.146; Ta = 35, UR = 30 → 0.238).

### Equações ALTERNATIVAS da Tabela 9-1 (listadas, NÃO adotadas) [p.206]
Vacas em lactação:
```
Murphy 1983:        ALI = 16.0 + (1.58*IMS) + (0.90*Leite) + (0.05*NaI) + (1.20*mnTAM)
Meyer 2004:         ALI = -26.1 + (1.30*Leite) + (0.406*NaI) + (1.516*TAM) + (0.058*PV)
Murphy 1983:        ALI = 23.0 + (2.38*IMS) + (0.64*Leite)
Holter e Urban 1992: ALI = -32.4 + (2.47*IMS) + (0.60*Leite) + (0.62*MS%) + (0.091*DJ) - (0.00026*DJ^2)
Khelil-Arfa 2012:   ALI = -77.6 + (3.22*IMS) + (0.92*Leite) - (0.28*CONC%) + (0.83*MS%) + (0.037*PV)
Appuhamy 2014:      ALI = -34.6 + (2.75*IMS) + (0.84*Leite) + (2.32*Cinzas%) + (0.27*MS%)
Little e Shaw 1978: ALI = 12.3 + (2.15*IMS) + (0.73*Leite)
Stockdale e King 1983: ALI = -9.37 + (2.30*IMS) + (0.53*MS%)
Castle e Thomas 1975:  ALI = -15.3 + (2.53*Leite) + (0.45*MS%)
Khelil-Arfa 2012:   ALI = -41.1 + (1.54*Leite) - (0.29*CONC%) + (0.97*MS%) + (0.039*PV)
Dahlborn 1998:      ALI = 14.3 + (1.28*Leite) + (0.32*MS%)
```
Vacas secas (alternativas):
```
Appuhamy 2016:      ALI = (0.69*IMS) + (0.28*MS%) + (0.85*TAM)
Holter e Urban 1992: ALI = 10.34 + (0.230*MS%) + (2.21*IMS) + (0.0394*(PB%)^2)
```
(Holter e Urban impresso "(0.0394 × (PB%)²)"; Appuhamy 2006 observou que Murphy 1983 e Meyer 2004 exigem IMS e tiveram bom desempenho; a equação alternativa de Holter e Urban para secas "pudesse estimar tão bem ou melhor" que a 9-3 [p.206].)

### Regras/relações numéricas de ALI em texto (sem número de equação)
- Temperatura: +1.5 kg ALI por °C (Meyer 2004; faixa média 8.6 ± 7.1 °C, mín. −5.6, máx. 23.3 °C); ALI 29% maior a 32 °C que a 15–24 °C (McDowell 1969); de 15 para 28 °C, ALI +10% em lactantes e +42% em secas (Khelil-Arfa 2014) [p.207].
- Bezerras: ALI ≈0.75–1 kg/d no início da vida; relação ALI/IMS ≈4:1 (kg) após desmame; ≈2:1 antes do desmame (Quigley 2006); pode ser <2:1 com altas taxas de dieta líquida; aumento acentuado aos 20 dias; diarreia aumenta ALI em 25–50% [p.207]. Sem equação.
- Novilhas mais velhas: dados limitados, sem equação; as equações de NASEM (2016) para bovinos confinados em crescimento "não parecem ser acuradas" [p.207].

## 9.5 Parâmetros e tabelas

**Figura 9-1 — Partição das perdas de água em % da ITA, vacas em lactação (Khelil-Arfa et al. 2014)** [p.208] (lido da imagem; os valores NÃO somam 100% por água metabólica, água retida e erro analítico)

| Via de perda | (A) termoneutro 15 °C, ITA = 108 kg | (B) alta temperatura 28 °C, ITA = 113 kg |
|---|---|---|
| Leite | 25% | 22% |
| Fezes | 44% | 35% |
| Urina | 16% | 18% |
| Evaporação | 18% | 30% |

(O texto cita 24% e 21% para leite em 15 °C e 28 °C, ligeiramente diferente de 25%/22% da figura; ver ⚠.)

**Tabela 9-2 — Padrões de água de bebida para humanos e limites superiores de concentrações potencialmente preocupantes para bovinos** [p.210] (conferida na imagem; mg/L salvo indicação; "—" = não informado)

| Constituinte | EPA: Aplicável (A) ou Secundário (S) | NMC humano | Concentração potencialmente preocupante para bovinos (esta publicação) |
|---|---|---|---|
| STD (sólidos totais dissolvidos) | S | 500 | consultar Tabela 9-3 |
| pH | S | 6.5–8.5 | — |
| Nitrato-N (NO3-N) | A | 10 (nota f: = 44 mg/L de NO3) | consultar Tabela 9-5 |
| Nitrito-N (NO2-N) | A | 1.0 | — |
| Sulfato (SO4^2-) | S | 250 (nota g) | Bezerros = 500; bovinos adultos = 1,000 |
| Alumínio | S | 0.05–0.20 | 5.0–10.0 (Beede 2012) |
| Arsênico | A | 0.01 | 0.20 (NRC 2005) |
| Bário | A | 2.0 | >10 (Beede 2012) |
| Boro | — | — | 150 (NRC 2005) ⚠ |
| Cádmio | A | 0.005 | 0.01–0.05 (NRC 2005; Beede 2012) |
| Cálcio | — | — | — (nota h: >500 mg/L sugere avaliação adicional) |
| Cloreto | S | 250 | 300 (Beede 2012) |
| Cloro (Cl2) | A | 4.0 (nota i: nível máximo de desinfetante residual) | — |
| Cromo | A | 0.1 | 0.1–1.0 (NRC 2005; Beede 2012) |
| Cobalto | — | — | 1.0 (NRC 2005) |
| Cobre | A | 1.3 | 1.3 (EPA 2009) |
| Cobre | S | 1.0 | — |
| Fluoreto | S | 2.0 | 2.0 (NRC 2005) |
| Ferro | S | 0.3 | 0.40 (Beede 2012) |
| Chumbo | A | 0.015 | 0.05–0.10 (NRC 2005) |
| Magnésio | — | — | — (nota h: >125 mg/L sugere avaliação adicional) |
| Manganês | S | 0.05 | 0.50 (Beede 2012) |
| Mercúrio | A | 0.002 | 0.01 (Beede 2012) |
| Molibdênio | — | — | 0.06 (Beede 2012) |
| Níquel | — | — | 1.0 (Beede 2012) |
| Fósforo | — | — | — |
| Potássio | — | — | — (nota j: ≥20 mg/L em água de vacas secas pode justificar avaliação adicional pelo efeito na DCAD) |
| Selênio | A | 0.05 | 0.05 (Beede 2012) |
| Prata | S | 0.10 | 0.05 (Beede 2012) |
| Sódio | — | — | 300 (Beede 2012) |
| Vanádio | — | — | 0.10 (NRC 2005; Beede 2012) |
| Zinco | S | 5.0 | 5.0–25.0 (NRC 2005; Beede 2012) |

Notas da tabela: faltam dados de pesquisa para muitos componentes (intervalos refletem falta de informação); acima do listado o sabor/odor pode ser afetado e/ou a dieta pode precisar de modificação; (b) problemas podem ocorrer com fluoreto >2.4 mg/L (manchas nos dentes), manganês >0.05 mg/L (sabor), sódio >20 mg/L (pode afetar bezerros) (Beede 2012); sulfato-enxofre (SO4-S) = sulfato (SO4) x 0.333 (nota g). Valores "para bovinos" são baseados em NRC 2001, 2005, Beede 2012 e Socha 2003, "mas, no geral, são exclusivos dessa publicação" e **não pretendem definir concentração tóxica nem nível recomendado**: servem de referência ao avaliar amostras; padrões EPA (aplicáveis e secundários) "podem atuar como recomendações seguras" (conservadoras) para pecuária [p.214].

**Tabela 9-3 — Recomendações para STD na água de bovinos leiteiros (fonte NRC 1974)** [p.211] (conferida)

| STD (mg/L) | Comentário |
|---|---|
| <1,000 | Seguro e não deve causar problemas de saúde. |
| 1,000–2,999 | Geralmente seguro, mas pode causar diarreia leve e temporária em animais não acostumados à água. |
| 3,000–4,999 | A água pode ser recusada quando oferecida pela primeira vez ou causar diarreia temporária; desempenho pode ser inferior ao ideal porque a ingestão de água não é maximizada. |
| 5,000–6,999 | Evite esta água como fonte de água de bebida; pode resultar em redução na produção de leite. |
| >7,000 | Esta água não deve ser fornecida a bovinos; resultará em problemas de saúde e/ou perda na produção. |

Nota: medir apenas STD não é adequado; sugere-se medir também componentes salinos específicos e bactérias. (Faixa entre 6,999 e 7,000 não coberta pela tabela, como impresso.)

**Tabela 9-4 — Elementos e espécies iônicas principais e secundárias comuns em águas subterrâneas (adaptado de Tchobanoglous e Schroeder 1985)** [p.212] (lista qualitativa, conferida)
- Principais — cátions: Ca2+, Mg2+, Na+, K+; ânions: HCO3−, SO4 2−, Cl−, NO3−.
- Secundárias — cátions: Al3+, NH4+, As, Ba2+, boro (BO3 3−), Cu2+, Fe2+ (ferroso), Fe3+ (férrico), Mn2+; ânions: HSO4−, HSO3−, CO3 2−, F−, OH−, H2PO4−, HPO4 2−, PO4 3−, S2−, SO3 2−.

**Tabela 9-5 — Recomendações para NO3− e NO3-N na água ingerida por bovinos leiteiros (fonte NRC 1974)** [p.213] (conferida)

| Nitrato NO3− (mg/L) | Nitrato-N NO3-N (mg/L) | Recomendação |
|---|---|---|
| 0–44 | 0–10 | Seguro para ser consumido por bovinos |
| 45–132 | 10–20 | Geralmente seguro quando oferecido com dietas balanceadas com alimentos com baixo teor de nitrato |
| 133–220 | 20–40 | Pode ser prejudicial se consumido por longos períodos de tempo |
| 221–660 | 40–100 | Bovinos em risco e possibilidade de morte |
| >660 | >100 | Não seguro, possibilidade de morte; não use como fonte de água |

Conversões: NO3-N x 4.43 = NO3 (nota); texto: dividir NO3 por 4.43 e NO2 por 3.29 para obter N [p.214]. Recomendação do livro: NO3-N na água **não deve exceder 10 mg/L (= 44 mg/L NO3)**; água adiciona-se ao nitrato de alimentos [p.214].

## 9.6 Regras de decisão / restrições para o otimizador

| Regra | Condição | Pág. |
|---|---|---|
| Fornecer água à vontade, sempre disponível, a vacas em lactação (especialmente em clima quente) e a bezerras, inclusive as alimentadas com dieta líquida | manejo | [p.206, 205] |
| Usar Eq. 9-1 se IMS confiável; senão Eq. 9-2 (lactação); Eq. 9-3 (secas); sem equação para bezerras/novilhas | seleção de equação | [p.205–207] |
| Consumo de água, por si só, NÃO deve ser usado para avaliar qualidade da água (subconsumo pode vir de doença, baixa produção, acesso aos bebedouros) | interpretação | [p.206] |
| STD: faixas da Tabela 9-3 (<1,000 seguro; ≥7,000 não fornecer) | — | [p.211] |
| Sulfato ≤500 mg/L (bezerros), ≤1,000 mg/L (adultos); NRC 2005: <600 para dietas de alto concentrado, até 2,500 seguro com dieta rica em forragem; 1,000–1,500 mg/L pode causar antagonismo Cu e Se (depende do S dietético); ≥3,000 mg/L reduz ingestão de água (sulfato de Mg mais que sulfato de Na) | — | [p.212–213] |
| Nitrato: NO3-N ≤10 mg/L (44 mg/L NO3); faixas da Tabela 9-5 | — | [p.213–214] |
| Ferro: 0.3 mg/L (EPA) listado como nível de cautela (listado 0.40 na Tab. 9-2); vacas reduziram ALI com 8 mg/L de lactato ferroso; evitar suplementar Fe na dieta se a água contém Fe | — | [p.210, 213] |
| Dureza: categorias mole 0–60, moderadamente dura 61–120, dura 121–180, muito dura >180 mg/L (NRC 1980); sem efeito na ALI de lactantes até 290 mg/L; efeito negativo em bezerras desmamadas; afeta incrustação e limpeza da ordenha | alerta de manejo | [p.211] |
| pH: sem diretriz para bovinos; EPA humano 6.5–8.5 | — | [p.211–212] |
| Minerais da água: normalmente NÃO somar ao fornecimento total da dieta; usuário pode reduzir o fornecimento dietético se a água tiver concentração alta; efeito total em geral insignificante (Castillo 2013) | opcional | [p.212] |
| Balanço iônico de laudo: Σ cátions (eq/L) = Σ ânions; diferença ≤2% aceitável, ≥5% sugere erro de coleta/análise ou espécie não relatada | validação do laudo | [p.212] |
| DCAD (Na + K) − (Cl + S), mEq/kg: Na e K da água geralmente não alteram a DCAD (contraíon Cl−), mas sulfato alto (contraíon Mg/Ca) reduz a DCAD; exemplo: 11 kg MS e 35 L/d com 500 mg S/L reduz DCAD em ≈90 mEq/kg | relevante para dietas pré-parto | [p.211] |
| Microbiologia: sem padrões formais; mediana de 1,000 coliformes termotolerantes (fecais)/L recomendada para bovinos (ANZECC 2000); teste não indica patógenos; cianobactérias: oferecer fonte alternativa se suspeita (risco no fim do verão/outono, águas rasas, alcalinas, ricas em N e P) | alerta | [p.214–215] |
| Restrição de água: desidratação de 10% da água corporal total = sérias implicações; 15–20% pode ser fatal | — | [p.209] |
| Amostrar a água no ponto de consumo, em diferentes estações; manter histórico; método analítico importa (análise sem acidificação deu só 7–25% do Fe obtido com acidificação nítrica) | procedimento | [p.209, 213] |

## 9.7 Lógica e fluxo
1. Lactação: se IMS estimada/medida disponível → Eq. 9-1 (precisa também de MS%, PB%, NaK a partir de %Na e %K da dieta, e TAM). Se não → Eq. 9-2 (precisa de leite, DEL, MS%, NaK, TAM). Seca → Eq. 9-3 (IMS, MS%, TAM; termo quadrático em (TAM − 16.4)).
2. IMS, composição da dieta (Na, K, PB, MS%) e leite vêm de outros capítulos (predição de IMS Cap. 2; dieta/minerais Cap. 7; produção de leite do usuário).
3. Perdas de água (Fig. 9-1, Eq. 9-4) e restrição hídrica são descritivas; sem acoplamento obrigatório ao cálculo de ALI.
4. Qualidade da água: comparar analitos do laudo com a Tabela 9-2 (limite superior), STD (9-3), nitrato (9-5), sulfato (texto); gerar alertas e, opcionalmente, ajustar minerais dietéticos para baixo.

## 9.8 Limitações, incertezas e mudanças vs. NRC 2001
- **Mudança vs. NRC 2001:** o volume anterior recomendava a equação de Murphy et al. (1983); agora recomendam-se as equações de Appuhamy et al. (2016), que incluem K e Na dietéticos e temperatura; novas equações para secas [p.205].
- Faltam estudos controlados para quantificar efeito de temperatura, ITU, radiação solar, UR, vento e chuva na ALI; algumas dessas variáveis só entram nas equações via temperatura [p.205]. Equação para secas baseada em poucos dados; K provavelmente afeta ALI de secas, mas faltam dados [p.206].
- Sem modelo para bezerras e novilhas [p.207].
- Estudos de qualidade da água em bovinos leiteiros são limitados; recomendações extrapoladas entre espécies; padrões humanos "particularmente conservadores" [p.209]. Tabela 9-2 é referência de cautela, não definição de toxicidade [p.214].
- Não há padrões de qualidade microbiológica por falta de evidência [p.215].
- Não incorporado ao modelo (discussão): ACT e compartimentos corporais, comportamento de beber, sudorese por raça, preferências de temperatura da água, restrição hídrica.

## 9.9 Conceitos e evidências relevantes (curtos)
- Água é o nutriente consumido em maior quantidade; ≈65% do corpo da vaca madura, ≈80% do feto, 85% do leite; fluxo de água em lactantes ≈30% maior que em outros ruminantes domésticos [p.204].
- Compartimentos: água intracelular ≈40% do PV; plasma ≈6.4% do PV em lactantes; ACV (água no corpo vazio) ≈70% em bezerros, diminui com gordura corporal; −7, 63 e 269 d pós-parto: 59, 66, 60% do PV (Andrew 1995), 64.7 ± 3.02% do PV em lactantes (Agnew 2005) [p.204–205].
- Comportamento: vacas bebem 40% da ingestão diária de água dentro de 2 h após alimentação e ordenha; tempo de bebida 13–17 min/d; dominância social correlaciona com consumo; bovinos de corte sobrevivem 3–5 d sem água (inverno) [p.205–206].
- Temperatura da água: preferem 20–28 °C; água morna aumentou ALI (+2.8% a +5.9% em vacas sem estresse térmico; Osborne 2002); água gelada no verão aumenta ALI e reduz frequência respiratória e temperatura corporal; estro pode diminuir ALI [p.207].
- Perdas (lactantes): leite ≈34% da ITA (19–52%; Holter e Urban, 329 vacas a 18 °C); fezes 30–44% (diminui com calor); fecal ≈61% da água do esterco (23 kg leite); urina 11–21% (15→21% com calor e bicarbonato de sódio 0.20–0.50% MS, só em lactantes); evaporação 18→30% (lactantes) e 28→44% (secas) de termoneutro para calor [p.207–208]. Vaporizar 1 L de água/suor consome 0.58 Mcal (2.42 MJ) [p.208]. Taxa de sudorese: Jersey 189 ± 84.6 g/m²·h; Holandesa predominantemente preta 414 ± 158.7; predominantemente branca 281 ± 119.4 [p.208–209]. Acima de 32 °C sem resfriamento, >85% da dissipação de calor é por vaporização de água (pele e pulmões) [p.209].
- Restrição de água a 50% da ingestão voluntária por 4 d → PL −74%; 90% da ingestão por 14 d → PL −3% (Little 1980) [p.209]. Bezerras com acesso restrito: −38% ganho de peso e −31% ingestão inicial de concentrado [p.206–207].
- STD: efeito em leite depende dos íons; efeitos de NaCl são mais consistentes (200→2,500 mg/L de STD via NaCl: leite 34.8→32.9 kg/d; Jaster 1978); 1,000, 5,000 ou 10,000 mg/L sem efeito em vacas a pasto (≈24 kg/d; Valtorta 2008); Challis 1987: 4,400→441 mg/L aumentou leite de ≈25 para 34 kg/d [p.211].

## 9.10 Dúvidas/riscos de OCR e inconsistências (cap. 9)
- ⚠ **Eq. 9-2, símbolo "DEL"**: não está definido na nota da tabela (que define "DJ = data juliana", usada só na equação alternativa de Holter e Urban). Provavelmente "dias em lactação" (DIM), mas o livro NÃO diz; **conferir com humano/inglês original**.
- ⚠ **Eq. 9-3 termo TAMC²**: nota escreve "(TMP − 16.4)²" — provável TAM; unidade °C². Eq. 9-3 não tem intercepto na imagem.
- ⚠ **Eq. 9-4**: unidade impressa g/h e magnitude de 0.1–0.3 sugere que a base (por kg PC, por m², por kg^0.75…) foi omitida; não definida no livro.
- ⚠ Texto diz "sete equações alternativas", mas a Tabela 9-1 lista **11** alternativas para lactantes (+2 para secas).
- ⚠ Fig. 9-1: valores da figura para leite (25% e 22%) divergem do texto (24% e 21%) [p.208].
- ⚠ Tabela 9-2, boro: "150 (NRC, 2005)" conferido na imagem como impresso, mas valor parece muito alto (confirmar com original em inglês).
- ⚠ Tabela 9-2, cobre: aparece duas vezes (Aplicável 1.3 e Secundário 1.0); para bovinos só a linha Aplicável tem valor (1.3).
- ⚠ Exemplo de DCAD (p.211): recalculando (35 L x 500 mg S/L / 32.06 x 2 / 11 kg MS) obtém-se ≈99 mEq/kg, não "cerca de 90" (derivado; livro diz ≈90).
- ⚠ Tabela 9-3: lacuna entre 6,999 e 7,000 mg/L como impresso; Tabela 9-2 nota j diz "≥20 mg/L" para K (OCR leu ">").
- ⚠ OCR da p.208 trouxe "206" no cabeçalho (é a p.208); texto de Tabela 9-1 do OCR foi todo substituído pela leitura da imagem (corrigido pela imagem).
- Páginas 196–203 (referências do cap. 8) e 215–218 (referências do cap. 9): apenas percorridas.

---

**COBERTURA:** páginas lidas 180–218. Texto do cap. 8 (p.180–196) e do cap. 9 (p.204–215) lidos integralmente via OCR; imagens conferidas para p.181, 183, 186, 189, 190 (cap. 8) e 206, 208, 209, 210, 211, 212, 213 (cap. 9). **Ficou de fora:** referências bibliográficas p.196–203 (cap. 8) e p.215–218 (cap. 9), apenas percorridas por não conterem dados técnicos (p.203 conferida visualmente em miniatura). Páginas de texto cujas imagens não foram conferidas linha a linha (apenas narrativa, sem equação/tabela): 180, 182, 184, 185, 187, 188, 191–195, 204, 205, 207, 214. Contagem: 7 equações do cap. 8 (8-1a, 8-1b, 8-2a, 8-2b, 8-3a, 8-3b, 8-3c) + 1 regra textual (ajuste de vit. E por pasto); 4 equações numeradas do cap. 9 (9-1 a 9-4) + 13 alternativas da Tabela 9-1 transcritas; 7 tabelas (8-1, 8-2, 9-1, 9-2, 9-3, 9-4, 9-5) + dados da Figura 9-1.

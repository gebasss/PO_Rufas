# Notas técnicas — NASEM 2021, Capítulo 7 (Minerais)

**Cobertura:** Capítulo 7 "Minerais", páginas impressas 116–179 (macrominerais: Ca, P, Mg, Na, K, Cl, S; microminerais: Co, Cu, I, Fe, Mn, Mo, Se, Zn, e demais; tabelas 7-1 etc.). Referências no fim apenas percorridas.
**Usado diretamente no modelo? sim** (todo o capítulo: o sistema fatorial de minerais absorvíveis, os coeficientes de absorção e os limites máximos toleráveis alimentam o simulador). Observação: as TABELAS de coeficientes de absorção de suplementos minerais citadas como "Tabela 19-3" no texto estão no Capítulo 19 (fora deste bloco).

Convenções: IMS = ingestão de matéria seca (kg/d); PC = peso corporal (kg); PMat = PC à maturidade (kg); GMD = ganho médio diário (kg/d); CA = coeficiente de absorção (fração; "AC" na tabela impressa); NMT = nível máximo tolerável. `^` expoente, `_` subscrito, `*` multiplicação. Página impressa entre colchetes.

---
# CÁLCIO (Ca) [p.116–122]

## Papel no simulador
O simulador calcula a exigência de Ca ABSORVÍVEL (g/d) pelo método fatorial (mantença + crescimento + gestação + lactação) e converte em Ca dietético dividindo pelo CA ponderado dos alimentos (Tabela 7-1). Ca da dieta é comparado com o NMT de 1.5% da MS. [p.117–122]

## Entradas
| variável | símbolo | unidade | definição | faixa/valores típicos | pág. |
|---|---|---|---|---|---|
| Ingestão de MS | IMS | kg/d | base da perda fecal metabólica | ex. 7 (novilha 300 kg), 13 (seca), 25 (lactante) | 117 |
| Peso corporal | PC | kg | crescimento, gestação | — | 117–118 |
| PC à maturidade | PMat | kg | Eq. 7-2 | — | 117 |
| Ganho médio diário | GMD | kg/d | Eq. 7-2 | — | 117 |
| Dia de gestação | t | d | Eq. 7-3, válido para t > 190 | 190–280 | 118 |
| Proteína verdadeira do leite | — | % | Eq. 7-4 | Holandesa 3.08; Jersey 3.65 (médias AIL 2015) | 118 |
| Produção de leite | — | kg/d | multiplica g Ca/kg leite | — | 118 |
| Ca (% MS) e classe/fonte de cada alimento | — | % MS | para ponderar com CA da Tabela 7-1 | — | 120 |

## Saídas
| variável | unidade | definição | pág. |
|---|---|---|---|
| Exigência de Ca absorvível por componente (mantença, crescimento, gestação, lactação) | g/d | soma = exigência total absorvível | 117–118 |
| Ca dietético exigido | g/d (ou % MS) | Ca absorvível total / CA da dieta | 118–121 |
| Ca absorvido verdadeiro | g/d | ingestão de Ca (g/d) x CA (por alimento) | 119 |

## Equações
**Eq. 7-1 — Mantença (Ca fecal metabólico, todos os estados fisiológicos)** [p.117]
```
Exigência de mantença (g/d) = 0.90 (±0.034) * IMS
```
IMS em kg/d. R² = 0.92; EP = 1.75 g/d. Intercepto não significativo descartado. Perda urinária de Ca ignorada (trivial; geralmente ≤ 1–2% do Ca absorvido). Dados agrupados de Hansard et al. (1954, 1957), Visek et al. (1953), Martz et al. (1990, 1999). Comparação do livro: NRC 2001 dava 4.6, 10.8 e 21.7 g/d (novilha 300 kg, seca e lactante de 700 kg); novo sistema com IMS 7, 13, 25 kg/d dá 6.3, 11.7 e 22.5 g/d. (NRC 2001: 0.0154 g Ca/kg PC para novilhas e secas; 0.031 g/kg PC para lactantes.)

**Eq. 7-2 — Crescimento (alométrica, AFRC 1991)** [p.117] (verificada na imagem)
```
Ca (g/d) = ((9.83 * PMat^0.22) * PC^-0.22) * GMD
```
PMat e PC em kg; GMD em kg/d. Exigência por kg de ganho diminui com o aumento do PC. Texto: NASEM (2016, corte) usa 71 g Ca/kg de ganho de proteína corporal (experimentos recentes até 144 g Ca/kg de proteína); a Eq. 7-2 dá valores 25–30% maiores que NASEM 2016 em PC baixo relativo à maturidade e muito maiores perto do PC maduro. [p.117–118]

**Eq. 7-3 — Gestação (Ca absorvível do útero e concepto, House e Bell 1993)** [p.118] (verificada na imagem)
```
Ca (g/d) = ( 0.02456 * e^((0.05581 - 0.00007*t)*t)
           - 0.02456 * e^((0.05581 - 0.00007*(t-1))*(t-1)) ) * (PC / 715)
```
t = dia de gestação (usar para t > 190; abaixo disso a exigência é considerada desprezível); PC em kg; 715 kg = peso médio das vacas do estudo (escala). O texto diz que a exigência pode exceder 10 g/d nas últimas semanas. (A diferença entre o termo em t e o termo em t-1 é a taxa diária de acúmulo.) O livro imprime a expressão com o termo em (t-1) quebrado em duas linhas; a leitura acima foi confirmada pela imagem. [p.118]

**Eq. 7-4 — Ca do leite** [p.118] (verificada na imagem)
```
Ca do leite (g/kg de leite) = 0.295 (±0.73) + 0.239 (±0.029) * Proteína verdadeira do leite (%)
```
RMSE = 0.065; R² = 0.86. ⚠ O livro imprime "±0.73" para o EP do intercepto (provável erro tipográfico de 0.073; não afeta o cálculo). Verificação: 3.08% -> 1.03 g/kg; 3.65% -> 1.17 g/kg (texto confirma 1.03 e 1.17). Exigência de lactação (g/d) = Ca do leite (g/kg) * produção de leite (kg/d) (implícito). Referência anterior (NRC 2001): 1.22 g/kg (Holandesa), 1.45 (Jersey), 1.37 (outras raças). Dados de literatura: mediana 1.01 g/kg leite de tanque (Castillo et al. 2013, >30,000 vacas, 39 rebanhos CA); Holandesa 1.10, Jersey 1.25, Pardo Suíço 1.25 (Carroll et al. 2006); tanque Holandesa 1.04 e Jersey 1.13 (Robinson et al. 2002). 65% do Ca do leite está nas micelas de caseína. (O texto escreve "1.01 mg de Ca/kg", obviamente g.) [p.118]

**Exigência de absorvível total:** soma de mantença (Eq. 7-1) + crescimento (7-2) + gestação (7-3) + lactação (7-4 x leite). Mobilização/reposição óssea: NÃO incluída (ver Limitações). [p.117–118]

**Coeficiente de absorção (CA) e Ca dietético:** CA = Ca verdadeiro absorvido (g/d) / ingestão de Ca (g/d); Ca verdadeiro absorvido = Ca aparente + Ca fecal metabólico (0.9 * IMS). Ca da dieta exigido = Ca absorvível exigido / CA da dieta (média ponderada por alimento). [p.119]

## Parâmetros e tabelas

**Tabela 7-1 — CA revisado para Ca de suplementos minerais e classes de ingredientes** [p.120] (verificada contra a imagem; OCR corrigido onde necessário). Colunas: NRC 2001 | CAs ajustados (NASEM 2021, os usados no modelo) | Hansard et al. (1957) | Kiarie e Nyachoti (2010), "CA da literatura".

| Fonte de Ca | NRC 2001 | **Ajustado (NASEM 2021)** | Hansard 1957 | Kiarie e Nyachoti 2010 |
|---|---|---|---|---|
| Farinha de ossos, cozida no vapor | 0.95 | **0.60** | 0.61 | — |
| Carbonato de cálcio, CaCO3 | 0.75 | **0.50** | 0.46 | 0.59 |
| Cloreto de cálcio anidro, CaCl2 | 0.95 | **0.60** | 0.57 | 0.63 |
| Cloreto de cálcio dihidratado, CaCl2.2H2O | 0.95 | **0.60** | — | 0.63 |
| Hidróxido de cálcio, Ca(OH)2 | 0.55 | **0.60** | — | — |
| Óxido de cálcio, CaO | 0.50 | **0.33** | — | — |
| Fosfato de cálcio (monobásico), Ca(H2PO4)2 | 0.95 | **0.60** | 0.56 | 0.55 |
| Sulfato de cálcio dihidratado, CaSO4.2H2O | 0.70 | **0.60** | — | — |
| Fosfato curação (Curaçao) | 0.70 | **0.45** | — | — |
| Fosfato dicálcico (dibásico), CaHPO4 | 0.94 | **0.60** | 0.47 | 0.73 |
| Calcário dolomítico (magnésio) | 0.60 | **0.35** (a) | — | 0.50 |
| Calcário, moído | 0.70 | **0.45** | 0.41 | 0.50 |
| Óxido de magnésio, MgO | 0.70 | **0.45** | — | — |
| Ostra, farinha (moída) | 0.75 | **0.50** | — | — |
| Fosfato, defluorado | 0.70 | **0.45** | — | — |
| Fosfato de rocha | 0.30 | **0.22** | — | — |
| Fosfato de rocha, baixo flúor | 0.30 | **0.22** | — | 0.48 |
| Argila coloidal de fosfato de rocha mole | 0.30 | **0.22** | — | — |
| Média para todos os suplementos minerais (exceto fosfatos naturais) | 0.86 | **0.55** | 0.52 | 0.57 |
| Leguminosas forrageiras | 0.30 | **0.30** | 0.36 | 0.58 |
| Silagem de milho | 0.60 | **0.40** | — | 0.52 |
| Feno de gramíneas | 0.30 | **0.40** | 0.45 | 0.04 (⚠ valor impresso; provável erro da fonte) |
| Todas as outras forragens | 0.30 | **0.40** | 0.45 | — |

(a) Valor de absorção para dolomítico de Gerken e Fontenot (1967). [p.120]
Observação: a imagem mostra "Óxido de magnésio MgO" listado na tabela de fontes de Ca com NRC 2001 = 0.70 e ajustado = 0.45 (é o que está impresso). O texto também fixa (sem linha própria na tabela): grãos de cereais e suplementos proteicos = 0.60 (pouca base experimental, contribuem pouco); sabões de Ca de AG de óleo de palma (7–9% Ca) = 0.60. [p.121]

**Figura 7-1** [p.120] — comparação absorção verdadeira de Ca medida vs estimada: com CAs do NRC 2001: Ca absorvível (g/d) = 8.6 (±4.80) + 0.668 (±0.04514) * estimado; P<0.001, R²=0.84, RMSE = 11.2 g/d (superestima). Com CAs ajustados (Tab. 7-1): Ca absorvível = 2.9 (±5.24) + 0.973 (±0.0674) * estimado; P<0.001, R²=0.84, RMSE=11.4 g/d (inclinação e intercepto não diferem de 1 e 0). 45 médias de tratamento de vacas de alta produção em início de lactação (Wohlt 1986; Martz 1999; Knowlton e Herbein 2002; Moreira 2009; Taylor 2009). [p.119–121]

**Parâmetros avulsos de Ca**
| parâmetro | valor | contexto | pág. |
|---|---|---|---|
| CA médio histórico | 0.45 (NRC 1971, 1978); 0.38 (NRC 1989); 0.50 (NASEM 2016 corte); 0.30–0.55 (INRA 2018) | única média dietética | 119 |
| CA verdadeiro médio medido nas 45 médias | 0.45 (±0.047 DP) vs 0.60 estimado pelo NRC 2001 | — | 119 |
| Intercepto de CA em ingestão zero de Ca | 50.2 (±1.5) = CA verdadeiro 0.50 | — | 119 |
| Efeito da ingestão de Ca no CA | queda de 0.008 a 0.059 unidades de CA por 100 g de ingestão de Ca (pequeno); faixa de Ca dietético 0.17–1.03% | — | 119 |
| CA do CaCl2 em bezerros <30 d (NRC 2001) | 0.95 | muito alto para adultos | 119 |
| CA do Ca (CaCl2) em novilhos jovens / maduros | 0.60 / 0.53 | Hansard 1957 | 119 |
| CaCl2 vs CaCO3 | CaCl2 é 1.2–1.32 vezes mais absorvível | Hansard 1957 | 120 |
| Relação Ca:P | sem ajuste de CA, a menos que >7:1 ou <1:1 | modelo não ajusta | 121 |
| Ca ósseo | 53% das cinzas ósseas; 21 g de cinzas/kg de tecido mobilizado => 11 g Ca/kg de tecido corporal mobilizado | — | 118 |
| Balanço de Ca negativo no início da lactação | -11 a -15 g/d com 0.52% de Ca (Taylor 2009) | semanas 1–8 | 118 |
| Perda de Ca ósseo no início da lactação | 800–1,300 g (Ellenberger 1931) => até 8 g/d absorvível nas últimas 20 sem. para repor (NÃO incluído) | — | 118 |
| Absorção de Ca | 22% no final da gestação -> 36% no dia 8 de lactação (van't Klooster 1976); fluxo de entrada de Ca ×1.55 do dia pré-parto a 10 d de lactação (Ramberg 1974) | efeito fisiológico (não modelado) | 121 |
| Ca necessário/kg de leite p/ balanço neutro no início da lactação | 5 g Ca/kg de leite (Ward 1972) | informativo | 121–122 |

## Regras de decisão / restrições para o otimizador
- **NMT de Ca = 1.5% da MS da dieta** (NRC 2005). [p.122] Excesso interfere na absorção de Zn e Se e dilui energia e proteína.
- CA por alimento conforme Tabela 7-1; cálculo do Ca dietético: soma(Ca_i * CA_i). [p.118–121]
- Não ajustar CA por idade em bovinos >200 kg PC. [p.121]
- Não ajustar CA pela relação Ca:P (exceto referência de risco >7:1 ou <1:1). [p.121]
- Sem provisão para reposição de Ca esquelético mobilizado no início da lactação. [p.118]

## Lógica e fluxo
IMS, PC, PMat, GMD, dia de gestação, produção e proteína verdadeira do leite (de outros capítulos) -> exigências absorvíveis por componente -> soma -> / CA da dieta (ponderado pelos alimentos da biblioteca; CA da Tabela 7-1) -> Ca dietético exigido vs fornecido; comparar com NMT. [p.117–122]

## Limitações, incertezas e mudanças vs. NRC 2001
- Mudou: perda fecal metabólica passa de função do PC (0.0154 / 0.031 g/kg PC) para função da IMS (0.90 g/kg IMS); Ca do leite passa de valor fixo por raça (1.22/1.45/1.37 g/kg) para função da proteína verdadeira (Eq. 7-4); CAs de suplementos reduzidos em ~25% (CaCl2 de 0.95 para 0.60; CaCO3 0.75 para 0.50). [p.117–121]
- Dados de disponibilidade de Ca de alimentos/suplementos individuais são escassos (especialmente leguminosas e farelo de canola); fatores como tamanho de partícula do calcário não quantificados. [p.121]
- Absorção de Ca é altamente regulada (vitamina D): dados de absorção publicados provavelmente subestimam a disponibilidade quando os animais não são alimentados na exigência. [p.119]
- Equação de crescimento (alométrica) mantida por falta de dado melhor. [p.117]

## Conceitos e evidências relevantes
- 98% do Ca corporal está no esqueleto; Ca plasmático 2.2–2.5 mM (9–10 mg/dL); Ca ionizado deve ficar entre 1 e 1.25 mM. [p.116]
- Leite = 50–75% das perdas de Ca em vacas lactantes. [p.117]
- Transporte ativo (1,25-diidroxivitamina D) é a principal via em ruminantes adultos; absorção passiva só com Ca ionizado >6 mM (drenches). [p.117]
- Deficiência: osteoporose/osteomalácia; concentração de Ca no leite não muda mesmo com deficiência grave. [p.122]
- Vacas ficam em balanço negativo de Ca no início da lactação e passam a positivo por volta de 6–8 semanas. [p.121]

## Dúvidas/riscos de OCR
- ⚠ Eq. 7-4: "±0.73" impresso (provável 0.073).
- ⚠ Tabela 7-1: feno de gramíneas, coluna Kiarie e Nyachoti = 0.04 (impresso).
- ⚠ Tabela 7-1: linha "Óxido de magnésio MgO" aparece na tabela de Ca (conforme impresso).

---
# FÓSFORO (P) [p.122–128]

## Papel no simulador
Exigência de P absorvível por método fatorial; CA do P é calculado por alimento a partir das frações inorgânica (CA 0.84) e orgânica (CA 0.68) do P, ou CA tabelado para suplementos de P (Tabela 19-3, Cap. 19). Compara com NMT de 0.79% da MS. [p.123–128]

## Entradas
| variável | símbolo | unidade | definição | faixa/valores típicos | pág. |
|---|---|---|---|---|---|
| IMS | IMS | kg/d | perda fecal endógena | — | 124 |
| PC | PC | kg | perda urinária endógena e crescimento | — | 124 |
| PMat | PMat (PCMat) | kg | Eq. 7-6 | — | 124 |
| GMD | GMD | kg/d | Eq. 7-6 | — | 124 |
| Dia de gestação | t | d | Eq. 7-7 (t>190) | 190–280 | 124 |
| Produção de leite | — | kg/d | Eq. 7-8 | — | 124 |
| Proteína verdadeira do leite | — | % | Eq. 7-8b | média 3.1% | 124 |
| P total e P inorgânico do alimento | — | % MS | partição P inorgânico (molibdovanadato) e orgânico (total - inorgânico) | — | 125 |
| Categoria animal (novilha em crescimento vs vaca adulta) | — | — | escolhe Eq. 7-5a ou 7-5b | — | 124 |

## Saídas
| variável | unidade | definição | pág. |
|---|---|---|---|
| P absorvível exigido (mantença, crescimento, gestação, lactação) | g/d | — | 124 |
| P dietético exigido | g/d, % MS | P absorvível / CA da dieta | 124–125 |

## Equações
**Eq. 7-5a — Mantença, novilhas em crescimento (g/d)** [p.124] (verificada na imagem)
```
P absorvível mantença (g/d) = 0.8 g P/kg IMS + 0.0006 g P/kg PC
```
(P fecal endógeno 0.8 g/kg IMS (NRC 2001, bovinos em crescimento) + P urinário endógeno 0.0006 g/kg PC = 0.6 mg/kg PC.)

**Eq. 7-5b — Mantença, vacas adultas (secas e lactantes) (g/d)** [p.124]
```
P absorvível mantença (g/d) = 1.0 g P/kg IMS + 0.0006 g P/kg PC
```
Multiplicar 0.8 ou 1.0 por IMS (kg/d) e 0.0006 por PC (kg).
Base: urinário endógeno histórico 2 mg/kg PC (NRC 2001) reduzido para 0.6 mg/kg PC (maior valor medido em vacas leiteiras; faixa geral 0.2–0.9, média 0.5, DP 0.28; lactantes 0.24–0.58, média 0.4). P fecal endógeno: lactantes com CA assumido 0.80, excreção fecal 0.95–1.4 g P/kg IMS (média 1.2, DP 0.14, 14 médias) => 1.0 g/kg IMS; Myers e Beede (2009): 1.04 g/kg IMS ad libitum (~25 kg/d), 1.36 e 1.19 g/kg IMS com 50% e 75% da IMS ad libitum (dados restritos NÃO usados); vacas secas: 0.4–0.5 g/kg IMS por diluição isotópica (Martz 1999; dietas atípicas, descartado) vs média 1 g/kg IMS (0.92 e 1.07; Valk 2002) -> adotado 1.0 g P absorvível/kg MS. [p.123–124]

**Eq. 7-6 — Crescimento (alométrica, mantida do NRC 2001)** [p.124] (verificada na imagem)
```
P (g/d) = (1.2 + ((4.635 * PMat^0.22) * (PC^-0.22))) * GMD
```
PMat e PC em kg; GMD em kg/d. ⚠ O livro imprime a unidade "P, kg/d" no lado esquerdo (erro evidente; deve ser g/d, coerente com NRC 2001 e com as demais exigências em g/d) e omite o sinal "=". Alternativa de NASEM (2016): 3.9 g P/100 g de proteína retida (não usada, pois exigiria conhecer a proteína do ganho).

**Eq. 7-7 — Gestação (P absorvível do concepto, House e Bell 1993)** [p.124] (verificada na imagem)
```
P absorvível (g/d) = ( 0.02743 * e^((0.05527 - 0.000075*t)*t)
                     - 0.02743 * e^((0.05527 - 0.000075*(t-1))*(t-1)) ) * (PC / 715)
```
t = dia de gestação (>190; para t<=190 a exigência é zero no modelo); 715 kg = PC médio das vacas do estudo (18 Holandesas multíparas abatidas entre 190 e 270 d). Taxa de acúmulo do concepto de 1.7 g/d (dia 190) a 5.4 g/d (dia 280). Mantida do NRC 2001 (sem dado novo). [p.124]

**Eq. 7-8a — Lactação, proteína do leite desconhecida (g/d)** [p.124]
```
P absorvível lactação (g/d) = Produção de leite (kg/d) * 0.90
```
**Eq. 7-8b — Lactação, proteína do leite conhecida (g/d)** [p.124]
```
P absorvível lactação (g/d) = Produção de leite (kg/d) * [0.49 + 0.13 * Proteína verdadeira do leite (%)]
```
Klop et al. 2013. Com 3.1% de proteína verdadeira: 0.88 g P/kg leite (0.49 + 0.13*3.1 = 0.893; o livro cita 0.88). Faixa de P no leite: grupos 0.83–1.00 g/kg; vacas individuais ~0.7–1.2 g/kg. ⚠ Nota: 0.49+0.13*3.1 = 0.893, livro diz "0.88" (arredondamento; conferir).

**CA do P dietético (cálculo):** P dietético exigido = P absorvível total / CA da dieta; CA da dieta = média ponderada dos CA dos alimentos; CA do alimento = média ponderada de P inorgânico (CA 0.84) e P orgânico (CA 0.68) pelas respectivas frações; se não houver dados de fração, usar CA de alimento similar ou o padrão 0.72. [p.124–125]

## Parâmetros e tabelas
| parâmetro | valor | contexto | pág. |
|---|---|---|---|
| CA do P inorgânico | 0.84 | modelo de P (Hill 2008; Feng 2015, 2016) | 125 |
| CA do P orgânico (fitato + não fitato) | 0.68 | fitato 0.66 vs não fitato 0.70, combinados | 125 |
| CA padrão (sem dados de fração de P) | 0.72 | — | 125 |
| CA do P no NRC 2001 | 0.64 (todas as forragens exceto silagem de milho); 0.70 (demais alimentos); suplementos 0.30–0.90; dieta total ~0.70 | referência | 124 |
| CA de suplementos de P | mantidos do NRC 2001 (Tabela 19-3, Cap. 19; fonte Soares 1995b, Peeler 1972) | referências: fosfato bicálcico (Ca dibásico) 0.75 em bovinos; ácido fosfórico 0.90 em bovinos; fosfato monossódico 0.90 em ovinos | 125 |
| P salivar reciclado | 30–75 g/d em vacas lactantes; salivar fornece ≥2x mais P ao intestino delgado que a dieta; CA do P salivar endógeno 0.68–0.81 (bezerros) | — | 122, 125 |
| P corporal | 80% em ossos e dentes; P plasma 1.3–2.6 mmol/L (4–8 mg/dL) | — | 122 |
| P na dieta para crescimento máximo de novilhas | 0.3–0.34% (resultados confirmados com 0.3 vs 0.4%) | informativo | 126 |
| P na dieta de vacas lactantes (NRC 2001) | 0.32–0.42% conforme potencial de leite; sem benefício acima de 0.42% | informativo | 126 |
| Fitase exógena | não reduz consistentemente a excreção fecal de P em vacas | — | 125 |
| Ca da dieta vs absorção de P | sem efeito geral | — | 125 |

(O livro cita "Tabela 19-3" para CA de suplementos de P e de Mg — fora do capítulo 7.)

## Regras de decisão / restrições para o otimizador
- **NMT de P = 0.79% da MS** (NRC 2005) — escolhido por falta de estudos acima disso, não por efeitos negativos observados abaixo de 0.7%. [p.128]
- Os CAs da Tabela 19-3 e das frações de P são "absorção máxima": acima da exigência o CA real cai e é superestimado, mas isso não afeta a quantidade de P dietético necessária para atender a exigência absorvível. [p.125]
- Hipofosfatemia periparto não é corrigida aumentando P dietético acima da exigência no final da gestação/início da lactação (secundária à hipocalcemia). [p.127]
- Sem ajuste para fitase nem para Ca dietético. [p.125]
- P >80 g/d em vacas próximas ao parto aumentou febre do leite e hipocalcemia; superalimentação moderada pré-parto = fator de risco para hipocalcemia (metanálise Lean 2006). [p.128]

## Lógica e fluxo
Exigências por componente (mantença Eq. 7-5a/b; crescimento 7-6; gestação 7-7; lactação 7-8a/b) -> soma -> P absorvível; CA do alimento vem da biblioteca (frações inorgânica e orgânica) -> P dietético exigido; compara com ingestão de P e NMT. [p.123–125]

## Limitações, incertezas e mudanças vs. NRC 2001
- Mudou: P urinário endógeno de 2 mg/kg PC para 0.6 mg/kg PC; lactação ganhou Eq. 7-8b (usando proteína do leite); CA do P por alimento passa a vir da partição inorgânico/orgânico (0.84 / 0.68) em vez de 0.64/0.70 por classe. Mantidos: P fecal endógeno 0.8 (crescimento) e 1.0 g/kg IMS (adultas), alométrica de crescimento (7-6), gestação (7-7), CA de suplementos. [p.123–125]
- Faltam dados analíticos de frações de P em alimentos (maioria dos laboratórios comerciais não faz P inorgânico). [p.125]
- Efeito da ingestão de P sobre o CA (queda acima da exigência) não quantificado. [p.125]
- Dados de primeira lactação (Odongo 2007): 0.35% P dietético não foi adequado para vacas de primeira lactação, mas não foi avaliado com o modelo (falta paridade no estudo). [p.126]
- Estudos de longo prazo apoiam as exigências calculadas; dieta com 0.32% de P não atende a exigência pelo modelo atual. [p.126]

## Conceitos e evidências relevantes
- Reciclagem salivar é o principal mecanismo homeostático do P; absorção líquida no intestino delgado; absorção passiva predomina com P adequado/excessivo (saturável; Michaelis-Menten nos modelos de P). Aumento da excreção urinária <10% do aumento da ingestão. [p.122–123]
- Dieta com 0.24% de P reduziu digestibilidade da FDN vs 0.34% (Puggaard 2011). [p.122]
- Deficiência grave de P: P <0.20% da MS por longo período afeta reprodução (geralmente por baixa ingestão/energia). Reprodução em lactantes não melhora com P acima da exigência (10 estudos). [p.126–127]
- Hipofosfatemia aguda: <2 mg P/dL de plasma; crônica <4 mg/dL; casos graves <1 mg/dL. [p.127]
- 0.69% de P por 14 sem. pré-parto a 22 sem. de lactação não causou toxicidade (De Boer 1981); P 0.64% vs 0.22% reduziu absorção de Mg em novilhas (Schonewille 1994). [p.128]

## Dúvidas/riscos de OCR
- ⚠ Eq. 7-6 unidade "kg/d" impressa (deve ser g/d) e sinal "=" ausente.
- ⚠ Eq. 7-8b: 0.49 + 0.13*3.1 = 0.893 vs 0.88 no texto.

---
# MAGNÉSIO (Mg) [p.128–131]

## Papel no simulador
Exigência de Mg absorvível pelo método fatorial e CA do Mg ajustado por entrada do usuário: a absorção verdadeira depende do K da dieta e da proporção de Mg suplementar (MgO) — Eq. 7-13 (CA basal padrão = 0.31 para K = 12 g/kg MS). [p.128–131]

## Entradas
| variável | símbolo | unidade | definição | faixa/valores típicos | pág. |
|---|---|---|---|---|---|
| IMS | IMS | kg/d | perda fecal endógena | — | 129 |
| PC | PC | kg | perda urinária e gestação | — | 129 |
| GMD | GMD | kg/d | crescimento | — | 129 |
| Produção de leite | Leite | kg/d | lactação | — | 129 |
| K da dieta | K | g/kg de MS da dieta | Eq. 7-13 | dados do ajuste: média 24.9, DP 12.7, min 6.9, max 75.6; basal 12 | 130–131 |
| Mg suplementar | Suplementar | % do Mg dietético vindo de MgO | Eq. 7-13 | 0 a 100%; dados do ajuste média 27.0, min 0, max 90 | 130 |
| Dias de gestação | — | d | >190 d | — | 129 |

## Saídas
| variável | unidade | pág. |
|---|---|---|
| Mg absorvível exigido por componente | g/d | 129 |
| Absorção verdadeira de Mg (CA) | fração | 130 |
| Mg dietético exigido | g/d, % MS | 129–131 |

## Equações
**Eq. 7-9 — Mantença** [p.129] (verificada na imagem)
```
Mg absorvível mantença (g/d) = 0.3 * IMS + 0.0007 * PC
```
0.3 g Mg/kg IMS = perda fecal endógena (valor absoluto do intercepto da regressão de Mg da dieta sobre Mg aparentemente digerido, g/kg; só estudos com K dietético ≤2%; metanálises de Weiss 2004 e Schonewille 2008); 0.0007 g/kg PC = perda urinária obrigatória (Schonewille 2000b). Não há ajuste do Mg fecal endógeno pelo estado de Mg da vaca. Valores antigos de Mg fecal endógeno: 2–5 mg/kg PC. [p.128, 130]

**Eq. 7-10 — Crescimento** [p.129]
```
Mg absorvível crescimento (g/d) = 0.45 * GMD
```
(Mg corporal cai de ~0.65 g/kg ao nascer para ~0.2 g/kg a 500 kg PC; 0.45 g/kg GMD mantido do NRC 2001.)

**Eq. 7-11 — Gestação (>190 d)** [p.129]
```
Mg absorvível gestação (g/d) = 0.3 * (PC / 715)
```
(Acúmulo fetal-placentário medido ~0.18 g/d; adotado 0.3 g/d com base no conteúdo do bezerro recém-nascido e na hipomagnesemia no parto.)

**Eq. 7-12 — Lactação** [p.129]
```
Mg absorvível lactação (g/d) = 0.11 * Leite
```
IMS, GMD e Leite em kg/d; PC em kg. Mg no leite ~0.11 g/kg; colostro ~0.38 g/kg (Cap. 12).

**Eq. 7-13 — Absorção verdadeira de Mg (CA)** [p.130–131] (verificada na imagem)
```
Absorção verdadeira de Mg = (44.1 - 5.42 * ln(K) - 0.08 * Suplementar) / 100
```
K = g/kg da dieta total (MS); Suplementar = % do Mg dietético fornecido por MgO. EP dos coeficientes: 4.8 (intercepto), 1.54 (K), 0.034 (Suplementar). 97 médias de tratamento de 23 estudos (novilhas, secas, lactantes); ensaio como efeito aleatório; apenas K e % de Mg suplementar foram significativos (colinearidade Mg dietético x suplementação r = 0.70; Mg da dieta não significativo). Com Suplementar = 0 e K = 12 g/kg: CA = 0.31 (padrão para todos os alimentos basais). Com Suplementar = 100% e K = 12: 0.23 (padrão para MgO; 26% menor que basal). Intervalo de predição de 95% para os CAs estimados = ±0.16; usuário pode ajustar o CA conforme tolerância a risco (NRC 2001 reduziu o CA basal em 1 DP). [p.130–131]
Conferência: 44.1 - 5.42*ln(12) = 44.1 - 5.42*2.4849 = 30.63 -> 0.31 ✓; com Suplementar 100: 30.63 - 8 = 22.63 -> 0.23 ✓.

## Parâmetros e tabelas
**Tabela 7-2 — Descrição dos dados usados para gerar a equação de Mg (média de 97 tratamentos)** [p.130] (verificada na imagem; corrige o OCR)
| variável | Média | DP | Mínimo | Máximo |
|---|---|---|---|---|
| Ingestão de matéria seca, kg/d | 13.6 | 6.49 | 5.8 | 26.1 |
| K da dieta, g/kg | 24.9 | 12.7 | 6.9 | 75.6 |
| Mg da dieta, g/kg | 3.60 | 2.75 | 1.08 | 17.3 |
| Ingestão de Mg, g/d | 42.6 | 23.4 | 11.8 | 124.3 |
| Mg suplementar, % do Mg total | 27.0 | 28.1 | 0 | 90 |
| Absorção verdadeira de Mg | 0.26 | 0.10 | 0.07 | 0.47 |

**CA relativo de suplementos de Mg (texto, p.131)** (a tabela completa de CA de suplementos de Mg está na Tabela 19-3, Cap. 19):
| fonte | CA relativo ao MgO | observação |
|---|---|---|
| MgO | 1.0 (CA padrão 0.23 com K=12) | média do MgO usado nos experimentos; varia com tamanho de partícula (<0.25 mm positivo; >1.0 mm negativo), calcinação, origem |
| MgSO4 | 1.2 (modelo) | dados: 1.7x (van Ravenswaay 1989, ovinos) e ~1.1x (Tebbe 2018); modelo adotou 1.2 |
| MgCl2 | = MgSO4 | sem dados; solubilidade semelhante |
| Mg(OH)2 | ~1.0 | Davenport 1990; Hemingway 1998 |
| MgCO3 reagente | ~1.0 | Ammerman 1972 |
| Calcário dolomítico | ~0.5 | Gerken e Fontenot 1967 |
| Magnesita | ~0.2 | Ammerman 1972 |

Outros parâmetros: concentração plasmática de Mg 0.75–1.0 mmol/L (1.8–2.4 mg/dL); Mg corporal 60–70% no osso (200–250 g), <4 g no extracelular, ~90 g intracelular — osso não é fonte utilizável em déficit. [p.128] Absorção satura acima de 1.1% Mg dietético em vacas secas. [p.129]

## Regras de decisão / restrições para o otimizador
- **NMT de Mg = 0.6% da MS** (NRC 2005); efeitos negativos só observados >1% (redução da ingestão, da digestibilidade, diarreia osmótica). [p.131]
- Dietas de vacas no final da gestação devem fornecer Mg adequado para a síntese de colostro (reservas lábeis limitadas). [p.128–129]
- Suposição recomendada (NÃO incluída no software): reduzir absorção de Mg em 20% quando há gordura suplementar (2.5–5% de gordura adicionada reduziu absorção aparente ~20%; até 5% de caroço de algodão integral sem efeito). [p.130]
- Efeito da monensina (aumenta absorção de MgO em 10–28%; reduz absorção de MgSO4 em 23%/~30%) NÃO está no modelo; efeito do amido NÃO modelado; amônia ruminal aguda reduz absorção (evitar mudanças abruptas, ex. pasto rico em proteína); K dietético alto é o principal antagonista; deficiência de Na eleva K ruminal. [p.129–131]
- Fator de segurança: se um fator de segurança igual ao do NRC 2001 fosse incluído, a exigência dietética seria ~25% maior. [p.129]

## Lógica e fluxo
Exigência absorvível (Eq. 7-9 a 7-12) -> / CA (Eq. 7-13, usando K da dieta e % de Mg de MgO; ou CA da Tabela 19-3 por fonte) -> Mg dietético exigido. K da dieta e % Mg suplementar vêm da formulação (entradas do usuário/dieta). [p.129–131]

## Limitações, incertezas e mudanças vs. NRC 2001
- Mudou: CA agora função de K e MgO (antes CA fixo por alimento com redução de 1 DP); Mg fecal endógeno passa a ser 0.3 g/kg IMS (antes em função do PC). Exigências dietéticas "geralmente semelhantes" mas sem fator de segurança. [p.129–131]
- Erro de estimativa alto da Eq. 7-13 (±0.16 IC95%). [p.131]
- Incerteza na perda fecal endógena de Mg. [p.130]

## Conceitos e evidências relevantes
- Absorção no rúmen (dois sistemas ativos: dependente da diferença de potencial, inibido por K; e dependente do gradiente de concentração); sem regulação hormonal; excesso excretado pela urina. [p.129]
- Tetania de pastagem/lactação: Mg plasmático <~0.7 mmol/L é fator de risco para hipocalcemia clínica. [p.131]
- P dietético ~0.6% reduziu absorção aparente de Mg em novilhas em ~18%. [p.129]

## Dúvidas/riscos de OCR
- Nenhum crítico (equações 7-9 a 7-13 e Tabela 7-2 conferidas na imagem).

---
# ÍONS FORTES: SÓDIO (Na), CLORO (Cl), POTÁSSIO (K) e DCAD [p.131–144]

## Papel no simulador
Na, K e Cl têm CA = 1.00 (Na, K) e 0.92 (Cl) para todos os alimentos; a exigência é fatorial com perda fecal metabólica proporcional à IMS (justificada pela osmorregulação da umidade fecal) e, para K, uma IA arbitrária de perda urinária endógena proporcional ao PC. A DCAD é descrita como medida e resposta, sem exigência fixa para lactantes. [p.131–144]

## Equações — geral dos íons fortes
**Água fecal vs íons fortes fecais** [p.132] (verificada na imagem)
```
H2O fecal (L/d) = 15.5 (±1.78) + 5.88 (±0.385) * Íons fortes fecais (Eq/d)
```
122 experimentos de balanço com vacas leiteiras; excreção média de íons fortes fecais = 3.47 (±1.24) Eq/d; RMSE = 3.89; R² = 0.861; P < 0.001. Fezes ≈ 85% de água. Motivação da perda fecal metabólica de Na, K e Cl. Verdade média dos íons fortes: absorção verdadeira ≥ 0.9. Volume urinário é linear com a ingestão de íons fortes (Bannink 1999). Ruminantes evoluíram com forragens >20 g K/kg MS, ≤1 g Na/kg MS e 3–6 g Cl/kg MS. [p.131–132]

## SÓDIO (Na) [p.132–136]

### Entradas
| variável | símbolo | unidade | definição | faixa/valores típicos | pág. |
|---|---|---|---|---|---|
| IMS | IMS | kg/d | mantença | ex. 28 (vaca 650 kg), 7 (novilha 300 kg) | 133 |
| GMD | GMD | kg/d | crescimento | PC 150–600 kg | 134 |
| PC | PC | kg | gestação | — | 134 |
| Produção de leite | Leite | kg/d | lactação | — | 134 |
| Na de cada alimento | — | % MS | CA = 1.00 | — | 134 |

### Saídas
Na absorvível exigido (g/d); Na dietético exigido (g/d e % MS) = absorvível / 1.00. [p.133–135]

### Equações (g de Na absorvível/d) [p.134] (verificadas na imagem)
```
Eq. 7-14  Mantença             = 1.45 * IMS
Eq. 7-15  Crescimento          = 1.4 * GMD
Eq. 7-16  Gestação (>190 d)    = 1.4 * (PC / 715)
Eq. 7-17  Lactação             = 0.4 * Leite
```
IMS, GMD e Leite em kg/d; PC em kg. Gestação: 1.4 g/d x (PC/715) de 190 a 270 dias; NÃO usar para <190 d (House e Bell 1993). Crescimento: 1.4 g/kg GMD para animais de 150–600 kg PC (Gueguen 1989). Lactação: 0.4 g/kg de leite (Na médio ponderado do leite 0.41 ±0.037 g/kg; antes 0.65 g/kg a partir de 0.63 do ARC 1965). Mantença: aplica-se a crescimento e lactação (e secas).

**Regressão da perda fecal metabólica de Na** [p.133]
```
Na absorvido (g/kg MS) = -1.45 (±0.25) + 0.98 (±0.036) * Ingestão de Na (g/kg MS)
```
137 mensurações de 8 experimentos (dietas com 0.27–1.17% Na); RMSE = 0.52; R² = 0.91; P < 0.001. Inclinação não difere de 1 => CA = 1.0; Na fecal metabólico = 1.45 g/kg IMS. NRC 2001 usava 0.038 g Na/kg PC (e 0.015 antes) com CA 0.90.

**Perda de Na no suor (estresse térmico) — NÃO usada no modelo** [p.133] (exponente verificado na imagem)
```
Excreção de Na no suor (g/m^2/d) = 0.198 * e^(0.044 * ITU)       R^2 = 0.9678
Área de superfície (Brody 1945): M^2 = 0.147 * PC^0.56            (m^2; PC em kg)
```
ITU = índice de temperatura e umidade. Vaca de 700 kg: 5.8 m^2; perda esperada de Na no suor 0.64–1.10 g/d em 25–35 °C e ITU 72–85. NRC 2001 sugeria acréscimos de 0.10 e 0.50 g Na/100 kg PC (0.7 e 3.5 g/d para 700 kg) a 25–30 °C e >30 °C; NASEM 2021: "o modelo não fornece meios para estabelecê-la" (dados insuficientes; perda real pode ser 5–10x maior). Concentração de Na no suor 0.25 g/L (11 mEq/L). Taxas de sudorese: 5–66 mL/m²/h (Jenkinson e Mabon) vs 14–600 g/m²/h (metanálise Thompson 2011). [p.133–134]

### Exemplos numéricos do livro (conferência)
- Vaca de 650 kg, 28 kg IMS, 45 kg leite: mantença 28*1.45 = 41 g/d; leite 45*0.4 = 18 g/d; total 59 g/d = 0.21% da MS (NRC 2001: 63 g/d, 0.25%). [p.133–135]
- Novilha de 300 kg, 7 kg IMS: 10 g/d de mantença (0.145% da MS) vs 4.5 g (NRC 2001). [p.133]

### Parâmetros
| parâmetro | valor | pág. |
|---|---|---|
| CA do Na (todos os alimentos; NaCl, NaHCO3, Na2CO3, sesquicarbonato) | 1.00 (NRC 2001: 0.90) | 134 |
| Na plasma / saliva / fluido ruminal | 150 mEq/L / 160–180 mEq/L / 80–90 mEq/L (faixa 50–140) | 132 |
| Na ósseo não trocável | 30–50% do Na corporal | 132 |
| Dieta mínima possível | ~0.07% Na se K for mais que adequado (K substitui Na na osmorregulação fecal) | 133 |
| Na para exigência em bovinos de corte (Morris 1980) | 0.10% (lactantes) e 0.07% (crescimento) da MS | 133 |

### Regras de decisão
- **NMT de NaCl = 3% da MS para bovinos lactantes; 4.5% para bovinos em crescimento** (NRC 2005). [p.135–136]
- Sem Na em dieta (0.16% Na) leva a queda de IMS e leite em 1–2 semanas; 0.14% Na em pasto sustentou >30 kg leite/d. Dados empíricos (Sanchez 1994b,c; 15 experimentos): desempenho máximo de IMS/leite com 0.70–0.80% Na (confundido com DCAD e interações com K, Cl, P); em clima quente, resposta de 0.18% para 0.55% Na. [p.135] (Evidência; não vira restrição do modelo.)
- NaCl na mistura de grãos a 4% (≈ 0.8–1.0% Na da dieta) sem efeito nocivo por 2 semanas; 0.88% Na (NaCl ou Na2CO3) sem toxicidade; alta ingestão de NaCl pode aumentar edema de úbere. [p.135]
- Deficiência de Na: sinais em 2–3 semanas (Babcock 1905); reverte rápido com NaCl. [p.136]

### Limitações
- Exigência de mantença subiu (1.45 g/kg IMS vs 0.038 g/kg PC / 0.90): total de Na ligeiramente menor que no NRC 2001 porque o Na do leite caiu (0.4 vs 0.65 g/kg). [p.133–135]
- Efeito do calor sobre Na não modelado. [p.134]

## CLORO (Cl) [p.136–139]

### Equações (g de Cl absorvível/d) [p.137] (verificadas na imagem)
```
Eq. 7-18  Mantença            = 1.11 * IMS
Eq. 7-19  Crescimento         = 1.0 * GMD
Eq. 7-20  Gestação (>190 d)   = 1.0 * (PC / 715)
Eq. 7-21  Lactação            = 1.0 * Leite
```
IMS, GMD e Leite em kg/d; PC em kg. Gestação: IA (não há dados diretos; extrapolada do Na — Cl:Na no feto/bezerro 41.5% Cl e 58.5% Na, ARC 1980). Crescimento: 1.0 g/kg GMD para PC 150–600 kg (Gueguen 1989). Lactação: Cl no leite 0.97 (±0.06) g/kg (média ponderada) arredondado para 1.0 (antes 1.15 g/kg, ARC 1965).

**Regressão da perda fecal metabólica de Cl** [p.136–137] (verificada na imagem)
```
Cl absorvível (g/kg MS) = -1.11 (±0.25) + 0.92 (±0.075) * Ingestão de Cl (g/kg MS)
```
144 mensurações de 9 experimentos (dietas 0.25–0.61% Cl); RMSE = 0.52; R² = 0.87; P < 0.001. => perda fecal metabólica 1.11 g Cl/kg MS (0.11% da MS) e CA médio 0.92 (usado para todos os alimentos). NRC 2001: 2.25 g/100 kg PC de mantença (17.5 g/d para 700 kg). Novo: 700 kg e 25 kg IMS => 30.1 g/d fecal (25*1.11/0.92). (Texto: "76% maior".)

**Perda de Cl no suor — NÃO usada no modelo** [p.137] (exponente corrigido pela imagem: 0.045; OCR leu "00")
```
Excreção de Cl no suor (g/m^2/d) = 0.198 * e^(0.045 * ITU)       R^2 = 0.93
```
Concentração de Cl no suor 0.28 g/L; 0.7–1.2 g/d para vaca de 700 kg com ITU 72–85. Não incluído (incerteza).

### Exemplo (conferência) [p.138]
Vaca de 650 kg, 28 kg IMS, 45 kg leite: mantença 28*1.11/0.92 = 34 g/d + leite 45*1/0.92 = 49 g/d = 83 g Cl dietético/d (NRC 2001: 81 g/d).

### Parâmetros
| parâmetro | valor | pág. |
|---|---|---|
| CA do Cl (todos os ingredientes) | 0.92 (absorção aparente em lactantes com forragem fresca média 88%, faixa 71–95%; ≥ 90% geral) | 137–138 |
| Cl plasma / líquido ruminal | 90–110 mEq/L / 10–30 mEq/L | 136 |
| Cl corporal | 1.2–1.4 g/kg PCV (100–500 kg PCV; ARC 1980) | 136 |
| 80% do Cl que entra no trato vem de secreções endógenas | — | 136 |
| Excreção urinária de Cl na deficiência | <2 g/d | 136 |

### Regras de decisão
- **NMT de Cl** não determinado; NMT de NaCl = 3.0% MS (lactantes) e 4.5% (crescimento). [p.139]
- Se Na for fornecido por NaHCO3 ou outro sal sem Cl, pode ser preciso suprir Cl com KCl. Cl aumenta efeito sobre DCAD (reduz DCAD). Cl na água de beber contribui (+6.5% da ingestão total em 39 rebanhos da Califórnia). [p.138]
- Evidência: 0.18% Cl conservou Cl sem queda de desempenho vs 0.40% (Coppock 1986); 0.10% de Cl dá deficiência clínica rápida (Fettman 1984); aumento de Cl de 0.15 a 1.62% reduziu IMS e leite (Sanchez 1994b; pior no calor). Bezerros: 0.038% Cl por 7 semanas sem deficiência clínica; 0.063% + drenagem abomasal dá deficiência. [p.138]

## POTÁSSIO (K) [p.139–142]

### Equações (g de K absorvível/d) [p.141] (verificadas na imagem)
```
Eq. 7-22a  Mantença (vacas em lactação)     = 2.5 * IMS + 0.2 * PC
Eq. 7-22b  Mantença (animais não lactantes) = 2.5 * IMS + 0.07 * PC
Eq. 7-23   Crescimento                      = 2.5 * GMD
Eq. 7-24   Gestação (>190 d)                = 1.03 * PC / 715
Eq. 7-25   Lactação                         = 1.5 * Leite
```
IMS, GMD e Leite em kg/d; PC em kg. "Não lactantes" = novilhas em crescimento e vacas secas. 2.5 g/kg IMS = perda fecal metabólica (regressão abaixo). 0.2 g/kg PC (lactantes) e 0.07 g/kg PC (não lactantes) = "IA arbitrária" para perda urinária endógena, definida para atingir mínimos dietéticos de ~1.00% (lactantes) e 0.60% (crescimento/secas) de K na MS (NÃO é medida de perda urinária). Crescimento: retenção de K 2.5 g/kg de ganho (K corporal 2.49 g/kg; NRC 2001 usava 1.6). Lactação: K no leite constante, média ponderada 1.49 (±0.11) g/kg, mantido 1.5. Gestação: 1.03 g/d x PC/715 após 190 d (House e Bell 1993); insignificante antes.

**Regressão da perda fecal metabólica de K** [p.140] (verificada na imagem)
```
K absorvível (g/kg MS) = -2.48 (±0.74) + 1.02 (±0.056) * Ingestão de K (g/kg MS)
```
149 mensurações de 9 experimentos (dietas 0.96–1.86% K); RMSE = 0.52; R² = 0.93; P < 0.001 (o livro imprime "P < 0,001"). => 2.48 arredondado para 2.5 g K/kg IMS; CA verdadeiro 1.02 (não difere de 1) => CA = 1.0. NRC 2001: 0.038 g K/kg PC + 6.1 g/kg IMS (2.6 fecal + 3.5 ajuste empírico) — o ajuste empírico implicava CA aparente de 0.49 com dieta de 1.2% K, "muito abaixo de qualquer valor medido".

**Perda de K no suor — NÃO usada no modelo** [p.140] (exponente verificado na imagem)
```
Excreção de K no suor (g/m^2/d) = 0.08 * e^(0.091 * ITU)          R^2 = 0.93
```
Concentração de K no suor 0.45 g/L; 0.8–2.5 g/d (vaca de 700 kg, ITU 72–85), ~2x as perdas de Na e Cl, mas <1% da ingestão típica de 250–350 g/d. NRC 2001: 0.04 e 0.36 g K/100 kg PC (25–30 °C e >30 °C) = 0.28 e 2.5 g/d (700 kg). Modelo não fornece valores. [p.140]

### Exemplos numéricos do livro (conferência) [p.141]
- Novilha de 300 kg, 1 kg/d de ganho, 7 kg IMS: 2.5*7 + 0.07*300 + 2.5*1 = 41 g/d = 0.59% da MS (NRC 2001: 35 g, 0.49%).
- Vaca de 650 kg, 28 kg IMS, 45 kg leite: 2.5*28 + 0.2*650 + 1.5*45 = 267.5 ≈ 268 g/d = 0.96% da MS (NRC 2001: 265 g, 0.94%).

### Parâmetros
| parâmetro | valor | pág. |
|---|---|---|
| CA do K (todos os alimentos e fontes minerais) | 1.00 | 141 |
| K corporal | ~80% em tecido magro e osso; 15% no conteúdo gastrointestinal | 139 |
| K plasma / ruminal / saliva | 5–10 / 40–100 / <10 mEq/L; intracelular 150–155 mEq/L | 139 |
| K em novilhas maduras Holandesas | 2.0 (±0.08) g/kg PC; 1.95 (±0.06) g/kg PCV | 140 |
| Exigência de crescimento (corte NASEM 2016) | 0.55–0.60% K para confinados; 0.3–0.4% a pasto | 141 |
| Bezerras: crescimento maximizado com 0.58% K | — | 141 |
| Lactação: resposta de IMS até ~1.0% K; resposta máxima 1.50% K (estação fria); no calor, IMS e leite aumentam ao longo da faixa 0.66–1.96%; 1.5% maximiza desempenho no estresse térmico | informativo | 142 |

### Regras de decisão
- **NMT de K = 2.0% da MS** (NRC 2005, por índices de saúde); bovinos toleram >3% por longos períodos (pastagens de início de primavera). K reduz a absorção de Mg (tetania). Sinais de deficiência grave: dietas com 0.06–0.15% K; com 0.5–0.7% o único sinal é menor IMS/leite. [p.142]
- Mínimos dietéticos implícitos das IAs: ~1.00% K (lactantes), ~0.60% K (crescimento e secas). [p.140]
- Aplicar a regra: "Na pode substituir K como cátion urinário depois que perdas fecais e leite forem atendidos" — a questão ficou em aberto. [p.140]
- Toxicidade aguda: 501 g de K como KCl por sonda gástrica mataram uma vaca de 475 kg; 393 g em bovinos de ~300 kg 1 morte; 182 e 240 g sem sinais. [p.142]

### Limitações
- Mudou: perda fecal de K (6.1 g/kg IMS -> 2.5 g/kg IMS) e perda urinária (0.038 g/kg PC -> 0.2 ou 0.07 g/kg PC); totais dietéticos quase iguais, mas a via passa de fecal para urinária endógena. [p.141]
- A IA urinária é arbitrária (baseada em respostas de IMS/leite de estudos com dietas atípicas e DCAD baixa de 0–50 mEq/kg); incerto para dietas com DCAD ≥200 mEq/kg. [p.140]

## DIFERENÇA CÁTION-ANIÔNICA DA DIETA (DCAD) [p.142–144]

### Definições
- **DCAD (Mongin 1981):** (Na + K) − Cl, em mEq/kg de MS. **DCAD-S (Ender et al. 1971):** (Na + K) − (Cl + S), com S como S^2-, em mEq/kg de MS. O livro não imprime a fórmula numerada com os fatores de conversão. [p.142–143]
- Exemplo do livro: dieta com 1.11% K, 0.25% Na, 0.33% Cl, 0.20% S: DCAD = 300 mEq/kg e DCAD-S = 185 mEq/kg [p.143]. ⚠ INCONSISTÊNCIA: na p.144, a MESMA composição (1.11, 0.25, 0.33 e 0.20%) é dada como DCAD-S = 174 mEq/kg e DCAD (Mongin) = 301 mEq/kg. Conferência independente (não do livro) com pesos equivalentes: K 11.1 g/kg / 39.1 = 283.9; Na 2.5 / 23.0 = 108.7; Cl 3.3 / 35.45 = 93.1; S 2.0 g/kg x 2 eq/mol / 32.06 = 124.8 => DCAD ≈ 299.5; DCAD-S ≈ 174.7. Portanto 174 (p.144) é coerente; o "185" da p.143 parece erro do livro (ou do OCR; a imagem também mostra 185).

### Respostas de lactação [p.143–144]
**Hu e Murphy (2004)** (17 experimentos, 69 médias; DCAD pela equação de Mongin): queda de 1.5 kg/d de IMS e de 1 unidade de pH urinário quando DCAD cai de 340 para 120 mEq/kg MS. DCAD de resposta máxima: IMS 396; leite 336; LCG 489; gordura 550 mEq/kg MS. DCAD em que 80% da resposta máxima ocorre: 200, 185, 190 e 305 mEq/kg MS, respectivamente (IMS, leite, LCG, gordura). Sanchez 1994b: IMS máxima, leite e LC4% com DCAD = 380 mEq/kg MS.

**Iwaniuk e Erdman (2015)** (43 estudos, 196 médias; modelo assintótico Y = a + b*(1 - e^(-k*DCAD-S)))  [p.143–144] (verificadas na imagem):
```
IMS (kg/d) = 18.44 (±0.389) + 1.11 (±0.468) * (1 - e^(-0.0038 (±0.002) * DCAD-S))        R^2 = 0.41; RMSE = 0.53
LCG 3.5% (kg/d) = 25.49 (±0.751) + 4.82 (±1.57) * (1 - e^(-0.0024 (±0.001) * DCAD-S))    R^2 = 0.48; RMSE = 0.73
```
DCAD-S em mEq/kg MS. IMS: 80% e 66% da resposta máxima em DCAD-S 425 e 290 mEq/kg MS. LCG: 80% e 66% em 675 e 450 (675 fora da faixa de inferência). Resposta máxima da produção de leite pequena: 1.1 kg/d. Gordura do leite aumenta linearmente: +0.1 ponto percentual e +39 g/d por +100 mEq/kg MS de DCAD-S. pH ruminal (83 médias) aumenta linearmente (+0.03 por +100 mEq/kg). Digestibilidade (52 e 42 observações): +100 mEq/kg MS de DCAD-S dá +0.73 e +1.54 pontos percentuais na digestibilidade da MS e da FDN, respectivamente (FDN responde por ~2/3 do aumento da MS).

### Regras de decisão
- **Não há exigência fixa de DCAD para lactantes**: a escolha deve vir de custo/benefício das respostas (Hu e Murphy 2004; Iwaniuk e Erdman 2015). [p.144]
- **Mínimo prático / IA de DCAD**: o que resulta de atender mínimos de K, Na, Cl e S. Vaca de 700 kg com 50 kg leite exige 1.11% K, 0.25% Na, 0.33% Cl e 0.20% S na MS => DCAD-S = 174 mEq/kg MS; DCAD (Mongin) = 301 mEq/kg. Se Cl e S medidos excederem os mínimos, pode ser preciso K ou Na adicionais. [p.144]
- **Bezerras em crescimento (IA de DCAD-S):** 150–200 mEq/kg MS (valor aproximado obtido quando recebem as exigências mínimas de K, Na e Cl). [p.144]
- **Novilhas leiteiras em crescimento (sem estudos):** DCAD (Mongin) adequada = 150 mEq/kg MS (novilhos de corte: 150 mEq/kg maximizou IMS e crescimento, testados 0, 150, 300, 450). [p.144]
- DCAD baixa pré-parto reduz febre do leite (Cap. 12). Abaixo de pH urinário 7, aumenta a excreção urinária de Ca. [p.143]

### Limitações
- Nenhuma exigência de DCAD no NRC 2001 (apenas discussão); agora duas metanálises, mas o modelo não impõe valor. Cuidado: o pH ruminal e o status ácido-básico são dois mecanismos confundidos. [p.143–144]

## Dúvidas/riscos de OCR (íons fortes)
- ⚠ DCAD-S exemplo: 185 (p.143) vs 174 (p.144) para a mesma dieta.
- ⚠ Expoentes de sudorese de Na (0.044), Cl (0.045) e K (0.091): conferidos na imagem (OCR errado para Cl e K). Não entram no modelo.
- Equações 7-14 a 7-25 conferidas na imagem.

---
# ENXOFRE (S) [p.144–146]

## Papel no simulador
Exigência dietética total (não absorvível) de S como % da MS ou g/d; compara com NMT dependente do teor de forragem. S também é componente da DCAD-S e antagoniza Cu e Se. [p.145–146]

## Entradas
IMS (kg/d); S total da dieta (% MS ou g/kg MS; inclui S da água de beber); proporção de forragem/concentrado da dieta (para o NMT). [p.145–146]

## Equação
**Eq. 7-26 — Exigência de S (IA)** [p.145] (verificada na imagem)
```
S total (g/d) = IMS * 2.0
```
IMS em kg/d. Equivale a 0.2% da MS para TODAS as classes de bovinos leiteiros (exceto bezerras pré-ruminantes). S total da dieta, não só absorvível. Mantido do NRC 2001 por falta de dados novos. Base: digestibilidade máxima de fibra com 0.15–0.25% S total (Guariola 1983; Qi 1994); 0.20% S sustentou retenção máxima em vacas de 30–37 kg leite/d (Bouchard e Conrad 1973a,b). Relação N:S 10:1–12:1 histórica não é importante quando a exigência de S é atendida.

## Parâmetros
- CA do S: não definido (a exigência é dietética total). Fontes inorgânicas de S (sulfatos) têm valores biológicos semelhantes. [p.145]
- S corporal ≈ 0.15% do corpo. [p.144]

## Regras de decisão / NMT
- **NMT de S (NRC 2005), considerando água como fonte trivial: 0.3% da MS para dietas com 85% de concentrado; 0.5% da MS para dietas com ≥40% de forragem** (mais representativo de vacas leiteiras). [p.146]
- Bovinos de corte em dieta de terminação sem forragem: risco de polioencefalomalacia sobe com S >0.42%; com 8% de FDN de forragem, ~0.6% (Nichols 2012). Polioencefalomalacia improvável em leiteiras. [p.146]
- Efeitos antagonistas: ~0.2% de S de SO4 adicionados (S total ~0.4%) reduzem a absorção de Cu e Se; possivelmente de Mn e Zn; efeitos negativos provavelmente abaixo de 0.4% de S total. Dietas com 0.2% de S de sulfato adicionado reduziram IMS de vacas. S >0.5% para dietas aniônicas pré-parto é aceitável por poucas semanas; a alimentação de longo prazo com S alto (ex.: 0.5% da MS, valor pela imagem; OCR leu 0.59%) não é recomendada. [p.145–146]
- Altas concentrações de sulfato na água reduzem ingestão de água (Cap. 9). [p.145]

## Limitações
- Laboratórios nem sempre analisam S; médias tabeladas provavelmente subestimam forragens adubadas com S. Dieta com degradabilidade proteica muito baixa poderia limitar S ruminal, mas improvável na prática. [p.145]

## Dúvidas/riscos de OCR
- ⚠ Texto p.146: OCR leu "(por exemplo, 0.59%)" para uso de longo prazo; a imagem mostra "(por exemplo, 0.5%)". Valor correto pela imagem: 0.5%. (corrigido pela imagem)

---
# MICROMINERAIS [p.146 em diante]

## CROMO (Cr) [p.146–147]

### Resumo
Exigência/IA NÃO estabelecida para bovinos (ingestão basal+suplementar não medida; concentração basal de Cr em alimentos pouco confiável por contaminação na moagem). Não usado como exigência no modelo. [p.146–147]

**Tabela 7-3 — Concentrações de Cr em alimentos comuns (mg Cr/kg MS)** [p.146] (verificada na imagem; fonte Spears et al. 2017; * = moído em moinho Wiley, provável contaminação)
| Alimento | Média | DP | Amplitude |
|---|---|---|---|
| Feno ou silagem de alfafa* | 0.522 | 0.220 | 0.199–0.889 |
| Polpa de beterraba* | 1.222 | 0.386 | 0.776–1.451 |
| Grão de milho, moído* | 0.049 | 0.031 | 0.014–0.114 |
| Grão de milho, inteiro | 0.026 | 0.015 | 0.008–0.054 |
| Silagem de milho* | 0.220 | 0.087 | 0.105–0.441 |
| Caroço de algodão* | 0.094 | 0.086 | 0.033–0.155 |
| Grãos de destilaria secos | 0.160 | 0.056 | 0.084–0.238 |
| Feno de gramínea* | 0.155 | 0.093 | 0.098–0.320 |
| Aveia, inteira | 0.025 | 0.008 | 0.021–0.034 |
| Grão de soja, inteiro | 0.069 | 0.035 | 0.034–0.122 |
| Casca de soja, solta | 0.262 | 0.073 | 0.191–0.336 |
| Casca de soja, peletizada* | 0.550 | 0.175 | 0.309–0.705 |
| Farelo de soja | 0.208 | 0.050 | 0.154–0.286 |
| Trigo | 0.041 | 0.014 | 0.029–0.062 |
| Sêmola de trigo | 0.084 | 0.031 | 0.044–0.132 |

### Parâmetros / limites
| item | valor | pág. |
|---|---|---|
| IA humana de Cr | 20–44 µg/d (NRC 2006) — não aplicável | 146 |
| Cr suplementar permitido nos EUA (propionato de cromo) | máximo 0.5 mg Cr suplementar/kg MS da dieta | 146 |
| Doses usadas em estudos | 4–10 mg/d (≈0.5 mg/kg MS) em lactantes; 6–9 mg/d aumentam leite no início da lactação em vacas >30 kg/d | 147 |
| Menor dose suficiente p/ resposta máxima | 0.01 mg Cr/kg PC (crescimento) ou 0.006 mg Cr/kg PC (lactantes); máxima resposta de leite ~0.01 mg/kg PC (~6 mg/d) | 147 |
| **NMT de Cr3+ (formas solúveis)** | **100 mg Cr/kg MS** (NRC 2005; dados muito limitados) | 147 |
| Redução de leite com 0.025 mg Cr/kg PC (15 mg/d) | Hayirli 2001 | 147 |
| Absorção de Cr em não ruminantes | <1% (inorgânico); ~3% (orgânico) — sem dados quantitativos para ruminantes | 146 |

### Conceitos
Cr participa da cromodulina (potencia sinalização de insulina); suplementação periparto reduz AGNE; efeito sobre sensibilidade à insulina depende do estado fisiológico; melhora blastogênese de linfócitos T. [p.146–147]

## COBALTO (Co) [p.147–149]

### Equação
**Eq. 7-27 — IA de Co (total, basal + suplementar)** [p.148] (verificada na imagem)
```
IA de Co (mg/d) = 0.2 * IMS
```
IMS em kg/d. Equivale a 0.2 mg Co/kg MS (total da dieta). Exigência anterior 0.11 mg/kg MS (Marston 1970, plasma vitamina B12 >0.3 µg/L). Faixas de resposta: dieta adequada 0.13–0.25 mg/kg MS (Stangl 2000); crescimento máximo 0.15–0.18; vitamina B12 hepática e folato máximos em 0.24 e 0.19; B12 plasmática 0.26; homocisteína e ácido metilmalônico minimizados em 0.16 e 0.12 mg/kg MS; Co basal médio dos estudos ~0.1 mg/kg MS; leite sem resposta com ≥0.20 mg/kg (menor concentração avaliada).

### Parâmetros
| item | valor | pág. |
|---|---|---|
| **NMT de Co** | **25 mg/kg MS** (NRC 2005) | 149 |
| Co 0.25–0.35 mg/kg MS | melhora digestão ruminal de forragem de menor qualidade (acima do necessário p/ B12) | 149 |
| Vitamina B12 hepática | <0.1 µg/g peso úmido indica deficiência de Co | 148 |
| Fontes de Co | carbonato, cloreto, nitrato, sulfato e gluco-heptonato adequados; óxido de Co menos disponível/solúvel | 148 |
| CA do Co | não informado | — |

### Notas
Deficiência: ruminantes mais sensíveis (B12 na gliconeogênese e metilmalonil-CoA -> succinil-CoA); estoques hepáticos duram meses; microrganismos ruminais não têm reserva (succinato ruminal sobe em dias); jovens mais sensíveis. Dietas ricas em grãos (85% grãos, cevada) reduzem B12 ruminal/plasma vs milho (não se sabe para vacas leiteiras, <40% grãos). [p.148–149]


## COBRE (Cu) [p.149–152]

### Papel no simulador
Exigência de Cu ABSORVÍVEL (mg/d) pelo método fatorial; CA do Cu muito baixo (0.05 para alimentos e CuSO4 com S <0.22% e Mo <1 mg/kg), tabelado por fonte; antagonismo de S, Mo e Fe descrito e uma equação (Eq. 7-28) fornecida mas NÃO incluída no software. NMT = 40 mg/kg MS. [p.149–152]

### Entradas
| variável | símbolo | unidade | definição | pág. |
|---|---|---|---|---|
| PC | PC | kg | mantença e gestação | 151 |
| GMD | GMD | kg/d | crescimento | 151 |
| Leite | Leite | kg/d | lactação | 151 |
| Dia de gestação | — | d | faixas 90–190 e >190 | 151 |
| Cu, S e Mo da dieta; S da água | — | mg/kg MS; g/kg MS | CA/antagonismo | 150 |
| Fonte de Cu suplementar | — | — | CA por fonte (Cap. 19, Tabela 19-3) | 150–151 |

### Equações (mg de Cu absorvível/d) [p.151] (verificadas na imagem)
```
Eq. 7-29  Mantença                 = 0.0145 * PC
Eq. 7-30  Crescimento              = 2.0 * GMD
Eq. 7-31  Gestação (90 a 190 d)    = 0.0003 * PC
Eq. 7-32  Gestação (>190 d)        = 0.0023 * PC
Eq. 7-33  Lactação                 = 0.04 * Leite
```
GMD e Leite em kg/d; PC em kg. Mantença: perda biliar+urinária de 0.0145 mg Cu/kg PC (Buckley 1991, isótopos; >2x o valor do NRC 2001). Crescimento: Cu dos tecidos em crescimento (inclui fígado) 2–2.5 mg/kg; fixado em 2.0 mg/kg de mudança de peso vivo por preocupação com excesso de Cu. Lactação: 0.04 mg Cu/kg de leite (-70% vs 0.15 do NRC 2001); pode chegar a 0.2 mg/kg com dieta rica em Cu. Gestação: concepto aos 190 d de vacas Holandesas (715 kg) tinha ~20 mg de Cu; considerou-se que NÃO há acúmulo no 1º trimestre (<90 d) e acúmulo linear entre 90 e 190 d (0.2 mg Cu/d = 0.3 µg Cu/kg PC materno/d); de 190 d ao parto: 1.6 mg/d = 2.3 µg/kg PC/d (House e Bell 1993). Para <90 d: exigência de gestação = 0 (implícito).
Conferência dos exemplos do livro: vaca de 650 kg, 35 kg leite, 150 d gestação: 0.0145*650 + 0.04*35 + 0.0003*650 = 9.43 + 1.40 + 0.20 = 11.0 mg/d (NRC 2001: 11.4); com 23 kg IMS e CA 0.045 => ~11 mg Cu/kg MS. Vaca seca 700 kg, 260 d: 0.0145*700 + 0.0023*700 = 10.15 + 1.61 = 11.7 mg/d (NRC 2001: 7 mg/d); ~20 mg Cu/kg MS com 13.5 kg IMS. [p.151]

**Eq. 7-28 — Absorção de Cu em função de S e Mo (McLauchlan e Suttle 1976; ovinos) — NÃO incluída no software** [p.150] (verificada na imagem)
```
Absorção de Cu = 10^( -1.153 - 0.0019*Mo - 0.076*S - 0.0131*S*Mo )
```
Absorção de Cu = g absorvido / g de Cu total; S = S da dieta (g/kg MS); Mo = Mo da dieta (mg/kg MS). Exatidão não avaliada em bovinos. Texto: com Mo ≤1 mg/kg e S de 0.3, 0.4 e 0.5% a absorção cai ~15, 30 e 43% vs dieta com 0.22% de S; com 4 mg Mo/kg a redução estimada é ~25% a mais em cada concentração de S. (Conferência independente: com Mo = 1 e S = 3, 4, 5 g/kg, a razão em relação a S = 2.2 g/kg dá quedas de 15%, 31%, 43%, coerente; com Mo = 0 as quedas seriam 13%, 27%, 39%.)

### Parâmetros
| parâmetro | valor | pág. |
|---|---|---|
| **CA do Cu em alimentos (verdadeiro)** | **0.05** (Buckley 1991), para dieta total com S <0.22% e Mo <1 mg/kg (NRC 2001: 0.04) | 150 |
| **CA do Cu do CuSO4** | **0.05** (mantido do NRC 2001) | 150 |
| CA do suplemento comercial genérico de Cu (biblioteca) | igual ao CuSO4 (0.05); usuário pode modificar | 151 |
| CA de CuCl2 | semelhante ao CuSO4 | 150–151 |
| CA de CuO dietético | quase zero (cápsulas ruminais de CuO podem ser eficazes) | 150 |
| CA de outras fontes (proteinatos, complexos Cu-AA, CuCl2 tribásico) | tabelados no Cap. 19 (Tabela 19-3) com base em biodisponibilidade relativa por Cu hepático; resultados inconsistentes na literatura (CuCl2 tribásico até ~2x CuSO4 na presença de S e Mo; igual sem antagonistas) | 151 |
| CA do Cu em bezerros pré-ruminantes | até 0.70; 50–60% do Cu (sulfato) retido no fígado (3–14 sem.) | 149 |
| CA do Cu em adultos com rúmen funcional | geralmente <0.05 | 149 |
| Cu em alimentos | 4–15 mg/kg MS | 150 |
| Fe antagoniza Cu | com Fe suplementar >250 mg/kg MS (Fe de forragem contaminada com solo é, em geral, óxido inerte; silagem torna Fe mais reativo) | 149–150 |
| Zn antagoniza Cu | só em 10–20x a exigência — sem importância prática | 149 |
| S dietético reduz Cu hepático | 0.5–0.6% S total; água com ~500 mg S/L | 150 |
| Ingestão de solo reduz absorção de Cu | ~50% (ovinos e bovinos) — NÃO incluído no modelo (usuário pode aumentar Cu em pastejo em solos argilosos) | 150 |
| Raça | Jersey acumula mais Cu hepático; modelo não inclui efeito de raça (exigência pode estar superestimada para Jersey) | 150 |

### Regras de decisão / limites
- **NMT de Cu = 40 mg/kg MS (NRC 2005)** — mas definir toxicidade por concentração dietética não é possível (antagonistas, acúmulo hepático contínuo). Crescimento/conversão reduzidos em corte com Cu hepático 290 mg/kg MS e 30 mg Cu/kg MS total (20 suplementar); digestibilidade da fibra reduzida em vacas leiteiras com 20 mg Cu/kg total (CuSO4). [p.152]
- Indicadores: Cu plasma <0.5 mg/L = deficiência clínica; Cu hepático <10 mg/kg MS = deficiência clínica iminente; <~35 mg/kg MS = subótimo; toxicidade a 300–350 mg/kg de peso seco. [p.152]

### Limitações
- Controle homeostático da absorção de Cu em ruminantes não determinado. Exigências foram calculadas com dados de Holandesas. Eq. 7-28 não validada em bovinos. [p.149–151]

### Dúvidas/riscos de OCR
- ⚠ Eq. 7-31: OCR imprimiu "77-31"; imagem mostra 7-31 (corrigido pela imagem). Eq. 7-28: OCR deformada; transcrita pela imagem.

## IODO (I) [p.152–155]

### Papel no simulador
Ingestão ADEQUADA (IA, não exigência) de I em mg/d como função do PC (mantença, derivada da taxa de secreção de tiroxina) mais 0.1 mg por kg de leite. Sem CA explícito (absorção 80–90%; derivação usa 20% de incorporação tireoidiana e 66% de I na T4). Não ajusta goitrogênios no modelo. [p.152–155]

### Equações
**Taxa de secreção de tiroxina (TSR)** (Swanson 1972 e Mixner 1962; R² = 0.96) [p.153] (verificada na imagem)
```
TSR (mg/d) = 0.0653 * PC^0.528
```
**IA de mantença de I** (T4 contém 66% de I; 20% do I da dieta usado pela tireoide quando I não é limitante) [p.153]
```
I (mg/d) = 0.216 * PC^0.528
```
(0.0653 * 0.66 / 0.20 = 0.2155.)

**Eq. 7-34 — IA total de I para todas as classes, exceto bezerras não ruminantes** [p.153] (verificada na imagem)
```
I da dieta (mg/d) = 0.216 * PC^0.528 + 0.1 * Leite
```
PC em kg; Leite em kg/d. Lactação: leite com baixa ingestão de I contém ~0.05 mg I/L e transferência da dieta para o leite ~0.5 => IA lactação 0.1 mg/L (= 0.1 mg/kg). Mantença é igual para secas e lactantes (TSR 25% maior na lactação vs final da gestação, evidência limitada; 2.5x sugerido por Sorensen foi descartado).
**IA de I para bezerras não ruminantes:** 0.8 mg I/kg IMS (baseada em IA de bebês humanos); quando ruminando, usar Eq. 7-34. [p.153]

### Exemplos do livro (conferência) [p.153]
- Vaca seca de 700 kg: 0.51 mg I/kg MS (sem goitrogênios) — 1.02 mg/kg com dieta goitrogênica (2x). Vaca lactante média de 650 kg e 35 kg/d de leite: 0.48 mg I/kg MS (0.96 com goitrogênios). (Conferência: 0.216*700^0.528 = 6.9 mg/d; com 13.5 kg IMS = 0.51 mg/kg. Lactante: 0.216*650^0.528 + 0.1*35 = 6.6 + 3.5 = 10.1 mg/d.)

### Parâmetros
| parâmetro | valor | pág. |
|---|---|---|
| Absorção de I da dieta | 80–90% (maior parte do I não absorvido pela tireoide vai para urina e leite) | 152 |
| I incorporado em hormônios tireoidianos | 0.25 mg/d (bezerros 45 kg) -> 1.4 mg/d (novilhas 400 kg); ~1.5 mg/d no final da gestação; 4–4.5 mg/d em lactantes de alta produção | 152 |
| Incorporação do I dietético pela tireoide | <20% (I adequado/excessivo); ~30% (marginal); até 65% (deficiência grave) | 152 |
| TSR | 0.008 a 0.0030 mg/kg PC em novilhas de 77–686 d (⚠ intervalo como impresso; provável 0.0080–0.0030, decrescente); lactantes ~0.30 mg/100 kg PC | 153 |
| Goitrogênios (farelo de canola etc.) | reduzem a transferência de I ao leite em ≥50%; IA seria 2x, mas ajuste NÃO está no modelo (usuário deve considerar) | 153 |
| I no leite | 100–300 µg/L típico; 26–39% do I suplementar (EDDI) vai ao leite; limite sugerido para o leite 500 µg I/kg | 154 |
| Fontes | iodetos de Na, K e Ca; KI volatiliza; ortoperiodato pentacálcico e EDDI mais estáveis | 154 |

### Regras de decisão
- **NMT de I = 50 mg I/kg MS (NRC 2005)**. FDA (EUA): máximo de suplementação de I (como EDDI) = 50 mg/d (vaca de 25 kg MS/d => 2.0 mg I/kg MS, ~3x a IA). O I suplementar não deve exceder as quantidades da IA (risco de saúde pública pelo leite). [p.153–155]
- Uso de EDDI para casco/dermatite digital limitado em vacas lactantes por preocupação com I no leite. [p.153–154]

### Limitações
- IA e não exigência: dados de tiroxina de 1960–70; falta de dados modernos. Dietas com goitrogênios precisam de mais I; sem ajuste. [p.152–153]

### Dúvidas/riscos de OCR
- ⚠ OCR de Eq. 7-34 quebrada ("PCº52%8"); imagem: PC^0.528. (corrigido pela imagem)

## FERRO (Fe) [p.155–157]

### Papel no simulador
IA de Fe absorvível (mantença = 0); CA de ingredientes basais = 0.10 (provavelmente alto demais por contaminação por solo); suplementos: sulfato ferroso 0.20, carbonato ferroso 0.10, Fe de óxido/contaminantes 0.01. NMT 500 mg/kg MS (dependente da fonte). [p.155–157]

### Equações (mg de Fe absorvível/d) [p.155] (verificadas na imagem)
```
Eq. 7-35  Mantença             = 0
Eq. 7-36  Crescimento          = 34 * GMD
Eq. 7-37  Gestação (>190 d)    = 0.025 * PC
Eq. 7-38  Lactação             = 1.0 * Leite
```
GMD e Leite em kg/d; PC em kg. Mantença insignificante (Fe reciclado). Gestação: 0.025 mg Fe/kg PC materno (18 mg/d para 715 kg; House e Bell 1993); antes de 190 d exigência não quantificada (não há dados; hematopoiese fetal). Crescimento: teor de Fe corporal de bezerros 18–34 mg/kg PC; adotado 34 mg Fe/kg GMD. Leite: ~1 mg Fe/kg.
Exemplo do livro: vaca de 650 kg, 25 kg leite, 205 d gestação, 20 kg IMS => 41 mg Fe/d absorvido (0.025*650 + 25 = 41.25); com CA 0.1: 20 mg Fe/kg MS. [p.156]

### Parâmetros
| parâmetro | valor | pág. |
|---|---|---|
| CA de Fe de ingredientes basais | 0.10 (mantido do NRC 2001; "CA menor que 0.10 presumivelmente mais adequado") | 156 |
| CA do sulfato ferroso | 0.20 (Hoskins e Hansard 1964; NRC 2001 usava 0.4–0.6 p/ suplementos) | 156 |
| CA do carbonato ferroso | 0.10 | 156 |
| CA de Fe de óxido (e contaminação de suplementos minerais) | 0.01 | 156 |
| CA do Fe de bezerras com deficiência, dietas líquidas | 0.55–0.72; CA do Fe solúvel de dietas líquidas cai de 0.40 para 0.15 ao subir Fe de 40 para 100 mg/kg (ARC 1980) | 156 |
| CA do Fe em bovinos adultos (radioativo) | <0.02 com dieta muito acima da exigência; 0.21 em ovelhas com 20 mg Fe/kg | 156 |
| Bezerros de vitela <15 sem. | 39 mg Fe/kg MS permite crescimento normal (anemia leve); 50 mg/kg adequado (Lindt e Blum 1994) | 156 |
| Silagem | solubilidade do Fe ~20x maior que pré-ensilagem (não se sabe se aumenta absorção) | 156 |
| Suplementação de 30 mg Fe/kg (Fe-AA) | sem efeito em vacas secas/lactantes | 155 |

### Regras de decisão
- **NMT de Fe = 500 mg/kg MS (NRC 2005)**; vale para Fe prontamente disponível (se vier de forragem contaminada, dietas acima disso provavelmente não causam problema); produção de leite e IMS caíram linearmente com 0, 250, 400 mg Fe suplementar (sulfato) (McCaughey 2005); 500 mg Fe (sulfato) reduz Cu. [p.156–157]
- Fe de água pode afetar ingestão de água e estresse oxidativo (Cap. 9). [p.157]
- Bezerras alimentadas com leite são o único grupo que normalmente requer suplementação de Fe. [p.156]

### Limitações
- IA derivada fatorialmente; absorção depende do status de Fe (regulação estrita; máxima em animais deficientes). Falta de dados com ruminantes. [p.155–156]


## MANGANÊS (Mn) [p.157–159]

### Papel no simulador
IA (não exigência) de Mn absorvível em mg/d; CA extremamente baixo (0.004 para alimentos; 0.005 para MnCl2 e MnSO4). NMT 2,000 mg/kg MS. [p.158–159]

### Equações (mg de Mn absorvível/d) [p.158–159] (verificadas na imagem)
```
Eq. 7-39  Mantença                 = 0.0026 * PC
Eq. 7-40  Crescimento              = 2.0 * GMD
Eq. 7-41  Gestação (>190 d)        = 0.00042 * PC
Eq. 7-42  Lactação                 = 0.03 * Leite
```
GMD e Leite em kg/d; PC em kg. Origem: mantença — Weiss e Socha (2005): ~580 mg Mn/d dietético mantém balanço zero em lactantes; menos 150 mg/d dietético (secreção no leite 0.6 mg/d / CA 0.004) = 430 mg para vaca de 650 kg; 430 * 0.004 = 1.7 mg absorvível = 0.0026 mg/kg PC (30% maior que 0.002 do NRC 2001). Gestação: 0.3 mg/d depositados no feto de 190 d ao parto (vaca de 715 kg; House e Bell 1993) => 0.00042 mg/kg PC. Lactação: Mn do leite 0.016–0.050 mg/kg, média ponderada 0.027, arredondada 0.03 mg/kg (mesmo NRC 2001). Crescimento: Mn em carcaça de bezerros 2.5 mg/kg (MS) com 27% de MS => 0.7 mg Mn/kg de ganho; MAS o livro fixa 2.0 mg Mn/kg GMD na Eq. 7-40 ("a exigência de crescimento não foi alterada"; valor do NRC 2001). ⚠ O texto (0.7) e a equação (2.0) divergem; vale a equação impressa (2.0). [p.158]
Exemplos do livro: vaca de 700 kg final de lactação: 1.8 mg (mantença) + 0.3 mg (gestação) = 2.1 mg/d absorvível = ~490 mg dietético (CA 0.0042) => 40 mg Mn/kg MS com 12.5 kg IMS. Vaca de 650 kg com 45 kg de leite, 26 kg IMS: mantença 1.7 + leite 1.35 = 3.1 mg/d (texto) => ~27 mg Mn/kg MS. [p.158]

### Parâmetros
| parâmetro | valor | pág. |
|---|---|---|
| CA do Mn (MnCl2) | 0.005 (NRC 2001: 0.01 para cloreto e 0.0075 para sulfato, em todos os alimentos) | 158 |
| CA do MnSO4 | 0.005 | 158 |
| CA de ingredientes basais | 0.004 (= 0.005 * 0.75) | 158 |
| CA do carbonato de Mn | 0.0015 | 158 |
| CA do óxido (monóxido) de Mn | 0.003 | 158 |
| Absorção medida | ~0.5% em vacas (2 estudos, 2 vacas cada); humanos 1.0–2.5%; ratos 1.8% (bovinos ≈ 1/4 de não ruminantes) | 158 |
| Ingestão de 250–300 mg Mn/d total em gestantes | não evitou deficiência nos bezerros | 158 |
| Dietas com ~16 mg Mn/kg MS em toda a gestação | bezerros com deformidade óssea, mães normais | 157 |
| Fertilidade de novilhas | 10 mg Mn/kg: baixa; 30–40 mg/kg: melhora | 157 |

### Regras de decisão
- **NMT de Mn = 2,000 mg/kg MS (NRC 2005)**; 500 mg Mn/kg MS agravou deficiência de Cu e sinais de deficiência de Fe em dietas deficientes em Cu. Toxicidade improvável (absorção muito baixa). [p.159]
- Sem indicador sensível de status de Mn; Mn plasmático/sangue total não reflete ingestão em bovinos normais. [p.157]
- Antagonismos (DMT1): Fe, Co e Cu possivelmente; S alto reduziu absorção aparente em novilhos. [p.157–158]

### Dúvidas
- ⚠ Crescimento: 0.7 (texto) vs 2.0 (Eq. 7-40). ⚠ OCR imprimiu "77-42" para Eq. 7-42 (corrigido pela imagem).

## SELÊNIO (Se) [p.159–161]

### Papel no simulador
IA de Se total (basal + suplementar) em mg/d como função da IMS. Não há equação fatorial (dados de perdas endógenas inexistentes). [p.161]

### Equação
**Eq. 7-43 — IA de Se** [p.161] (verificada na imagem)
```
IA de Se (mg/d) = 0.3 * IMS
```
IMS em kg/d. Equivale a 0.3 mg Se/kg MS para todas as classes de bovinos. NRC 2001 (0.3 mg/kg MS) mantido: dados de selenito/selenato com Se total na dieta de 0.35–0.40 mg/kg. A dieta basal geralmente é considerada sem Se; usuários em áreas ricas em Se (ex.: Dakotas) devem analisar forragens e incluir Se basal. A biblioteca de alimentos do modelo traz médias de Se por alimento (variam muito entre fazendas). [p.160–161]

### Parâmetros
| parâmetro | valor | pág. |
|---|---|---|
| Absorção aparente de Se sem suplementação | 0.30–0.60 (ovinos, caprinos, vacas não lactantes) | 160 |
| Absorção aparente de selenito/selenato | 0.36–0.51 | 160 |
| Absorção aparente de Se-levedura | ~0.57–0.62 (≈24% maior que selenito: 0.62 vs 0.50 em ovinos); absorção de Se-levedura de alta qualidade ≥1.2x a do inorgânico | 160 |
| Absorção verdadeira (regressão) | ~0.5 em vacas com Se inorgânico; sem dado p/ levedura | 160 |
| Acúmulo fetal de Se (dieta 0.3 mg/kg inorgânico) | 0.055 mg/d no último trimestre | 161 |
| Se no leite | ~0.02 mg/kg (selenito) e ~0.04 mg/kg (Se-levedura) com 0.3 mg Se/kg dieta; Se do leite ~1.9x maior com levedura | 160–161 |
| Se no sangue total/plasma p/ prevenir mastite | >~0.18 µg/mL (sangue total); ~0.075 µg/mL (plasma); ~6 mg/d de Se inorgânico mantém | 161 |
| Antagonistas da absorção de Se inorgânico | S dietético (+0.2 a +0.4 pontos percentuais de sulfato), Ca dietético baixo (<0.6%) e alto (1.0%), tiossulfato e molibdato (in vitro) | 160 |
| Se em forragens | planícies centrais EUA/Canadá >0.1 mg/kg MS; leste do Mississippi e oeste das Rochosas <0.1 mg/kg MS | 159 |

### Regras de decisão
- **NMT de Se = 5 mg/kg MS (NRC 2005)**, ~16x a concentração recomendada (0.3). Toxicidade: selenometionina 10 mg Se/kg MS ou selenito 25 mg/kg MS por 120 d (bovinos de um ano); aguda com 10–20 mg Se/kg PC (selenito); injeção de 0.5 mg Se/kg PC causou 67% de mortalidade em bezerros jovens (~200 kg). [p.161]
- **Limite regulatório FDA (EUA)**: Se suplementar máximo 0.3 mg/kg de dieta (considerada ~90% MS); formas permitidas: selenito de sódio, selenato de sódio e levedura enriquecida com Se. [p.159, 161]

### Limitações
- IA e não exigência fatorial; dados de endógeno inexistentes; Se-levedura vs inorgânico não diferenciado na IA. [p.161]

## ZINCO (Zn) [p.161–165]

### Papel no simulador
Exigência de Zn ABSORVÍVEL (mg/d) pelo método fatorial; CA do Zn de ingredientes basais e ZnCl2 = 0.20; fontes suplementares com CA específico (ZnO 0.16). NMT 500 mg/kg MS. [p.162–165]

### Equações (mg de Zn absorvível/d) [p.164] (verificadas na imagem)
```
Eq. 7-44  Mantença                 = 5.0 * IMS
Eq. 7-45  Crescimento              = 24 * GMD
Eq. 7-46  Gestação (>190 d)        = 0.017 * PC
Eq. 7-47  Lactação                 = 4 * Leite
```
IMS, GMD e Leite em kg/d; PC em kg. Mantença: perda fecal endógena = exigência de mantença = 5 mg Zn/kg IMS (média arredondada de 2.0 mg/kg IMS em novilhas de 300 kg — 0.027 mg/kg PC; Hansard 1968 — e 8.6 mg/kg IMS em cabras — 0.17 mg/kg PC; Hattori 2010); perda urinária obrigatória = ZERO (0.003 mg/kg PC em bovinos em crescimento e 0.0016 mg/kg PC em lactantes, muito baixas). NRC 2001: fecal 0.033 + urinária 0.012 = 0.045 mg/kg PC (CA 0.15). Gestação: 0.017 mg/kg PC materno = 12 mg/d aos 190 d–parto para vaca de 715 kg (House e Bell 1993); não alterada. Lactação: 4 mg Zn/kg de leite (faixa 3–6 mg/kg). Crescimento: média 24 mg Zn/kg GMD (intervalo 16–31); em ovinos 28 mg/kg PCV (24 mg/kg a 15 kg PC e 30 mg/kg a ~50 kg); valor único usado.

### Tabela 7-4 — Exigências de Zn atuais e do NRC 2001 [p.164] (verificada na imagem; corrige OCR das IMS)
| | Vaca 650 kg, 30 kg leite/d, IMS = 22.4 kg | Vaca 650 kg, 50 kg leite/d, IMS = 29.4 kg | Vaca seca 700 kg, 270 d de gestação, IMS = 13 kg |
|---|---|---|---|
| Exigência total absorvível, atual (mg/d) | 232 | 347 | 65 |
| Exigência total absorvível, NRC 2001 (mg/d) | 149 | 229 | 44 |
| Exigência total da dieta, atual (mg/d) (a) | 1,160 | 1,735 | 325 |
| Exigência total da dieta, NRC 2001 (mg/d) (a) | 993 | 1,526 | 293 |
(a) CA = 0.20 para as exigências atuais e 0.15 para o NRC 2001.
Conferência: 5*22.4 + 4*30 = 232 ✓; 5*29.4 + 4*50 = 347 ✓; 232/0.20 = 1,160 ✓; 347/0.20 = 1,735 ✓; 149/0.15 = 993 ✓; 229/0.15 = 1,526 ✓; 44/0.15 = 293 ✓. ⚠ Vaca seca: 65 = 5*13 (somente mantença); a Eq. 7-46 para 700 kg daria 0.017*700 = 11.9 mg/d adicionais (total 76.9 mg/d absorvível; 385 mg/d dietético); a tabela impressa NÃO inclui a gestação — inconsistência do livro (a tabela parece omitir o termo de gestação). ⚠ 

### Parâmetros
| parâmetro | valor | pág. |
|---|---|---|
| **CA do Zn de ingredientes basais e ZnCl2** | **0.20** (NRC 2001: 0.15; absorção de 12–33% em bovinos com dietas comuns; cabras: 0.182) | 162 |
| CA do ZnSO4 | = ZnCl2 (0.20); carbonato de Zn = ZnSO4 | 162 |
| CA do ZnO | 0.16 (≈80% do ZnSO4) | 162 |
| Outras fontes (Cap. 19, Tabela 19-3) | biodisponibilidade 10–20% maior que ZnSO4 para alguns compostos | 162 |
| Absorção em vacas adaptadas a dieta deficiente (6 mg Zn/kg MS) | ~50% (não desejável maximizar) | 162 |
| Antagonistas | S dietético elevado (~0.5%) aumenta perda urinária e reduz absorção em corte; Fe 1,000 mg/kg reduziu Zn hepático ~18%; Cu só com relação Zn:Cu muito baixa (~0.15:1); fitato/fibra/Ca sem efeito claro em ruminantes; monensina pode aumentar absorção | 162–163 |
| Zn sérico | normal 0.7–1.3 µg/mL; deficiente <0.5 µg/mL (estresse/doença redistribuem Zn) | 164 |
| Dieta com ~41 mg Zn/kg MS | maior CCS vs 63 mg/kg; 41 mg/kg não atenderia às exigências atuais | 164 |

### Regras de decisão
- **NMT de Zn = 500 mg/kg MS (NRC 2005)**; "vacas leiteiras provavelmente são capazes de tolerar maiores concentrações". Toxicidade clínica com 900 mg Zn/kg; ingestão, leite e status de Cu reduzidos com 2,000 mg/kg (ZnSO4) mas não com 1,000 mg/kg. [p.164–165]
- Defeito genético de absorção de Zn em Holandesa-Frísia (lethal trait A46). [p.164]

### Limitações
- Dados extremamente limitados de Zn fecal endógeno em vacas leiteiras (2.0 a 8.6 mg/kg IMS); mantença subiu muito (Tabela 7-4) enquanto o CA basal também aumentou (0.15 -> 0.20). Perda fecal depende do status de Zn (metalotioneína). [p.163–164]

## ARSÊNIO, MOLIBDÊNIO, NÍQUEL E VANÁDIO [p.165–166]
Dados de essencialidade em bovinos leiteiros inexistentes; nenhuma IA/exigência no modelo; apenas NMT. [p.165]
| elemento | limite / observação | pág. |
|---|---|---|
| Arsênio (As) | **NMT = 30 mg/kg MS** (NRC 2005); cabras com 0.35 vs 0.035 mg As/kg MS tiveram mais cabritos (Anke 1986); As inorgânico mais tóxico que orgânico | 165 |
| Molibdênio (Mo) | essencial (xantina oxidase, aldeído oxidase, sulfito oxidase); sem deficiência clínica; toxicidade = deficiência de Cu (antagonista do Cu com S; mais Cu corrige). NMT de Mo: não informado no capítulo | 165 |
| Níquel (Ni) | essencial para ruminantes (urease); estímulo da urease ruminal com 5 mg Ni/kg (vs basal 0.06 mg/kg) em cordeiros; novilhas (125 kg) 0–3 mg/kg Ni suplementar aumentaram IMS e GMD; **NMT = 100 mg Ni/kg** (NRC 2005); vacas lactantes com 0, 50 ou 250 mg/kg MS sem efeito (O'Dell 1970) | 165 |
| Vanádio (V) | ação semelhante à insulina; vacas: 0–0.12 mg V/kg PC^0.75 (sulfato de vanadil) de 4 sem. pré a 4 sem. pós-parto => leite aumentou quadraticamente, máximo em 0.04 mg V/kg PC^0.75; V basal 0.89 mg/kg MS; cabras 2 mg/d; sem dados para IA; **NMT = 50 mg V/kg MS** (NRC 2005); função ruminal prejudicada em cordeiros com 7 mg V/kg | 165–166 |
Observação: as páginas impressas 165 (parte final) a 179 contêm REFERÊNCIAS (apenas percorridas); não há tabelas nem equações nelas.

---
# QUADROS CONSOLIDADOS (para implementação)

## Q1. Coeficientes fatoriais de exigência absorvível (unidades: g/d para macrominerais; mg/d para microminerais)
Convenção: PC em kg; IMS, GMD e Leite em kg/d; t = dia de gestação (aplicar apenas para t > 190, exceto onde indicado).
| Mineral | Mantença | Crescimento | Gestação | Lactação | Eq. | Pág. |
|---|---|---|---|---|---|---|
| Ca (g/d) | 0.90 * IMS | ((9.83 * PMat^0.22) * PC^-0.22) * GMD | (0.02456*e^((0.05581-0.00007t)*t) - 0.02456*e^((0.05581-0.00007(t-1))*(t-1))) * (PC/715) | [0.295 + 0.239 * %PV leite] * Leite | 7-1 a 7-4 | 117–118 |
| P (g/d) | novilhas: 0.8*IMS + 0.0006*PC; adultas: 1.0*IMS + 0.0006*PC | (1.2 + (4.635*PMat^0.22)*(PC^-0.22)) * GMD | (0.02743*e^((0.05527-0.000075t)*t) - 0.02743*e^((0.05527-0.000075(t-1))*(t-1))) * (PC/715) | Leite*0.90 ou Leite*[0.49+0.13*%PV] | 7-5 a 7-8 | 124 |
| Mg (g/d) | 0.3*IMS + 0.0007*PC | 0.45*GMD | 0.3*(PC/715) | 0.11*Leite | 7-9 a 7-12 | 129 |
| Na (g/d) | 1.45*IMS | 1.4*GMD | 1.4*(PC/715) | 0.4*Leite | 7-14 a 7-17 | 134 |
| Cl (g/d) | 1.11*IMS | 1.0*GMD | 1.0*(PC/715) | 1.0*Leite | 7-18 a 7-21 | 137 |
| K (g/d) | lactantes: 2.5*IMS + 0.2*PC; não lactantes: 2.5*IMS + 0.07*PC | 2.5*GMD | 1.03*PC/715 | 1.5*Leite | 7-22a/b a 7-25 | 141 |
| S (g/d, S TOTAL da dieta) | IA: 2.0 * IMS | — | — | — | 7-26 | 145 |
| Co (mg/d, total) | IA: 0.2 * IMS | — | — | — | 7-27 | 148 |
| Cu (mg/d) | 0.0145*PC | 2.0*GMD | 90–190 d: 0.0003*PC; >190 d: 0.0023*PC | 0.04*Leite | 7-29 a 7-33 | 151 |
| I (mg/d, IA) | 0.216*PC^0.528 (+ lactação abaixo) | — | — | + 0.1*Leite | 7-34 | 153 |
| Fe (mg/d) | 0 | 34*GMD | 0.025*PC | 1.0*Leite | 7-35 a 7-38 | 155 |
| Mn (mg/d, IA) | 0.0026*PC | 2.0*GMD | 0.00042*PC | 0.03*Leite | 7-39 a 7-42 | 158–159 |
| Se (mg/d, IA, total) | 0.3*IMS | — | — | — | 7-43 | 161 |
| Zn (mg/d) | 5.0*IMS | 24*GMD | 0.017*PC | 4*Leite | 7-44 a 7-47 | 164 |
| Cr, As, Mo, Ni, V | sem exigência/IA | — | — | — | — | 146–166 |
Observações: Ca, P e Mg têm CA ajustável por dieta (Ca: Tabela 7-1; P: frações inorgânica/orgânica; Mg: Eq. 7-13). Para P, a mantença usa 0.8 g/kg IMS em novilhas em crescimento e 1.0 g/kg IMS em adultas. Gestação de Na, Cl, K, Mg, Fe, Mn, Zn e Cu (>190 d) usa PC/715 (ou coeficiente por kg de PC já escalonado) — ver cada equação.

## Q2. Coeficientes de absorção (CA) — resumo
| Mineral | CA padrão / regra | Pág. |
|---|---|---|
| Ca | por alimento/fonte, Tabela 7-1 (forragens 0.30–0.40; silagem de milho 0.40; calcário 0.45; CaCO3 0.50; fosfatos Ca 0.60 etc.; grãos e proteicos 0.60) | 120–121 |
| P | inorgânico 0.84; orgânico 0.68; padrão 0.72; suplementos de P em Tabela 19-3 (Cap. 19) | 125 |
| Mg | Eq. 7-13: (44.1 - 5.42*ln(K) - 0.08*Suplementar)/100; basal 0.31 (K=12 g/kg); MgO 0.23; MgSO4 = 1.2 x MgO; MgCl2 = MgSO4; demais em Tabela 19-3 | 130–131 |
| Na | 1.00 (todos) | 134 |
| Cl | 0.92 (todos) | 138 |
| K | 1.00 (todos) | 141 |
| S | exigência em S total (sem CA) | 145 |
| Co | IA em Co total (sem CA) | 148 |
| Cu | 0.05 (alimentos e CuSO4; S <0.22%, Mo <1 mg/kg); CuO ~0; genérico = CuSO4 | 150–151 |
| I | IA total; absorção 80–90% (não usada) | 152–153 |
| Fe | 0.10 basais; FeSO4 0.20; FeCO3 0.10; óxido/contaminação 0.01 | 156 |
| Mn | 0.004 basais; MnCl2 e MnSO4 0.005; MnCO3 0.0015; MnO 0.003 | 158 |
| Se | IA total; absorção verdadeira ~0.5 (não usada) | 160–161 |
| Zn | 0.20 basais e ZnCl2/ZnSO4/ZnCO3; ZnO 0.16 | 162 |

## Q3. Níveis máximos toleráveis (NMT; NRC 2005, citados no capítulo)
| Mineral | NMT | Pág. |
|---|---|---|
| Ca | 1.5% da MS | 122 |
| P | 0.79% da MS (ver: dado limitado; sem efeitos negativos <0.7%) | 128 |
| Mg | 0.6% da MS (efeitos só >1%) | 131 |
| NaCl | 3% da MS (lactantes); 4.5% (crescimento) | 135–136, 139 |
| Cl | não determinado | 139 |
| K | 2.0% da MS (bovinos toleram >3%) | 142 |
| S | 0.3% (85% concentrado); 0.5% (≥40% forragem) | 146 |
| Cr3+ solúvel | 100 mg/kg MS | 147 |
| Co | 25 mg/kg MS | 149 |
| Cu | 40 mg/kg MS | 152 |
| I | 50 mg/kg MS (FDA: máx. suplementação 50 mg/d como EDDI; ≈2.0 mg/kg MS em vaca de 25 kg MS/d) | 154 |
| Fe | 500 mg/kg MS (dependente da fonte) | 156 |
| Mn | 2,000 mg/kg MS | 159 |
| Se | 5 mg/kg MS (FDA suplementar 0.3 mg/kg dieta) | 161 |
| Zn | 500 mg/kg MS | 164–165 |
| As | 30 mg/kg MS | 165 |
| Mo | não informado | 165 |
| Ni | 100 mg/kg | 165 |
| V | 50 mg/kg | 166 |
| Cr suplementar (legal EUA, propionato) | 0.5 mg/kg MS | 146 |

## Q4. Mínimos dietéticos implícitos e IAs de referência (derivados/descritos no texto)
- K na dieta: ~1.00% MS (lactantes); 0.60% (crescimento e secas) [p.140]. Na: IA derivada 0.21% MS (vaca 650 kg, 28 kg IMS, 45 kg leite); mínimo possível ~0.07% com K mais que adequado [p.133–135]. Cl: 83 g/d (mesma vaca) [p.138]. S: 0.20% MS [p.145]. Co: 0.2 mg/kg MS [p.148]. Se: 0.3 mg/kg MS [p.161].
- DCAD: sem exigência; IA prática DCAD-S = 174 mEq/kg MS (301 pela eq. de Mongin) para vaca de 700 kg com 50 kg de leite; bezerras 150–200 mEq/kg (DCAD-S); novilhas 150 mEq/kg (Mongin). [p.144]

---
# LÓGICA E FLUXO GERAL DO CAPÍTULO (resumo para o desenvolvedor)
1. Entradas de outros capítulos: IMS (kg/d), PC (kg), PMat (kg), GMD (kg/d), produção de leite (kg/d), proteína verdadeira do leite (%), dia de gestação, composição de alimentos (macrominerais em % MS, microminerais em mg/kg MS; P inorgânico e total; S e Mo da dieta), fontes suplementares (para CA) e K/Mg suplementar (para CA de Mg), proporção de forragem (para NMT de S).
2. Para cada mineral: exigência absorvível = soma de componentes (Q1); dividir pela CA (Q2) para obter a exigência dietética; comparar com ingestão e NMT (Q3).
3. Ca e P usam coeficiente por alimento (soma ponderada pela massa de mineral fornecida por cada alimento); Mg usa CA da dieta como um todo (K da dieta e % de Mg de MgO); demais usam CA fixo por fonte.
4. Gestação: termos aplicados só para t > 190 d (Ca, P exponenciais; Na, Cl, K, Mg, Fe, Mn, Zn, Cu lineares com PC/715 ou por kg de PC); Cu também 90–190 d. Mobilização óssea de Ca/P em início de lactação NÃO modelada.
5. Não modelados (somente discussão): efeito do calor sobre Na/Cl/K (sudorese), efeito de gordura/ionóforos/amido sobre Mg, goitrogênios sobre I, solo/raça sobre Cu, fitase, idade sobre Ca, relação Ca:P, Eq. 7-28 (Cu: S x Mo).

# LIMITAÇÕES GERAIS E MUDANÇAS vs. NRC 2001
- Perdas fecais endógenas passam a ser expressas em função da IMS (Ca, P, Mg, Na, Cl, K, Zn, Co/S/Se por IMS na IA) em vez do PC; CAs de Ca revisados para baixo (~25%), CA do Na 0.90 -> 1.00, Cl 0.92, K 1.00, Zn 0.15 -> 0.20, Mn reduzido (0.01/0.0075 -> 0.005/0.004), Cu 0.04 -> 0.05, Mg passa a depender de K e MgO. Leites: Ca por proteína; Na 0.65 -> 0.4; Cl 1.15 -> 1.0; Cu 0.15 -> 0.04. Mn/Se/I/Co/S/Fe/Cr: IAs ou sem exigência por falta de dados.
- DCAD discutida (sem exigência no NRC 2001): agora duas metanálises; Cr, Ni, V, As: sem exigência.

# CONCEITOS E EVIDÊNCIAS ADICIONAIS
- Indicadores de status: Cu hepático (padrão ouro), Se (sangue/GPx), Zn sem indicador aceito, Fe (ferritina em jovens), Mn sem indicador sensível. [p.152, 157, 160, 164]
- Cr: suplementação periparto afeta sensibilidade à insulina e AGNE; Co: vitamina B12 ruminal; Fe: bezerros de vitela única classe com suplementação necessária. [p.147–148, 156]

# DÚVIDAS/RISCOS DE OCR — LISTA CONSOLIDADA (⚠ = precisam conferência humana)
1. ⚠ Eq. 7-4: "(±0.73)" impresso para o EP do intercepto (provável 0.073).
2. ⚠ Eq. 7-6: unidade "kg/d" impressa e sinal "=" ausente (deve ser g/d).
3. ⚠ Eq. 7-8b: 0.49+0.13*3.1 = 0.893 vs "0.88" no texto.
4. ⚠ Tabela 7-1: Kiarie e Nyachoti, feno de gramíneas = 0.04 (impresso).
5. ⚠ DCAD-S de exemplo: 185 (p.143) vs 174 (p.144) para a mesma dieta; 174 confere com cálculo independente.
6. ⚠ Mn crescimento: texto 0.7 vs Eq. 7-40 = 2.0.
7. ⚠ TSR de novilhas "0.008 a 0.0030 mg/kg PC" (p.153, como impresso).
8. ⚠ Tabela 7-4, vaca seca: 65 mg/d = só mantença (omite 0.017*700 = 11.9 mg/d de gestação da Eq. 7-46).
9. ⚠ Texto do S p.146: OCR "0.59%" vs imagem "0.5%" (corrigido).
10. (corrigido pela imagem) expoentes de sudorese: Na 0.044, Cl 0.045 (OCR "00"), K 0.091 (OCR "9-09!"); Tabela 7-2 (mínimos/máximos); IMS da Tabela 7-4 (22.4 e 29.4); Eq. 7-28 e 7-34.
11. Texto-sobre-texto não conferido na imagem (narrativa numérica): p.116, 119, 121–123, 125–128, 131, 135–136, 138–139, 142, 146–147, 149, 152, 154, 156–157, 160, 162, 165. Equações e tabelas numéricas conferidas.

# CONTAGEM
Equações numeradas do capítulo transcritas: Eq. 7-1 a 7-47 (47 equações numeradas; 7-5, 7-8 e 7-22 em duas variantes a/b) + 8 equações/regressões sem número (água fecal; regressões de perdas fecais de Na, Cl e K; excreção no suor de Na, Cl e K; área de superfície de Brody; TSR; respostas de IMS e LCG à DCAD-S; IA de mantença de I) e a Figura 7-1 (regressões). Tabelas: 7-1, 7-2, 7-3, 7-4 (todas verificadas na imagem).

COBERTURA: páginas lidas 116–165 integralmente (texto OCR + conferência por imagem das páginas 117, 118, 120, 124, 129, 130, 132, 133, 134, 137, 140, 141, 143, 144, 145, 146, 148, 150, 151, 153, 155, 158, 159, 161, 162, 163, 164, 165); páginas 165 (final)–179 são REFERÊNCIAS, apenas percorridas (171–179 apenas varridas por busca de tabelas/equações; nenhuma encontrada). Não conferidos na imagem: narrativa de p.119, 121–123, 125–128, 131, 135–136, 138–139, 142, 147, 149, 152, 154, 156–157, 160 (sem equações/tabelas).

# NASEM 2021 (Bovinos Leiteiros, 8ª ed., PT-BR) — Notas técnicas: Caps. 11 e 12

**Capítulos e páginas cobertas (páginas IMPRESSAS):** Cap. 11 Crescimento [pp.278–291] (texto 278–289; referências 289–291); Cap. 12 Vacas Secas e Vacas em Transição [pp.292–315] (texto 292–307; referências 307–315).
Convenções: `^` expoente, `_` subscrito, `*` multiplicação. Siglas PT: PC=BW, PCV=EBW (peso corporal vazio), GPV=EBG (ganho de PCV), GMD=ADG, PCMat=MatBW (PC à maturidade), ER=RE (energia retida), PL=NP (proteína líquida), MLG=FFM (matéria livre de gordura), PM=MP, EM=ME, IMS=DMI, DCAD, AGNE=NEFA.

- **Cap. 11 — Usado diretamente no modelo? SIM** (exigências de EM/PM de novilhas em crescimento, composição do ganho, estimativa de GMD a partir de EM, PM/EM mínima). As Tabelas 11-3 e 11-4 são saídas de exemplo das equações (reproduzi-las numericamente serve de teste de aceitação).
- **Cap. 12 — Usado diretamente no modelo? PARCIAL.** Só as Eqs. 12-1/12-2 (IMS de vacas e novilhas pré-parto) são equações de modelo; as exigências de gestação vêm dos capítulos de nutrientes (Cap. 3 energia, Cap. 6 proteína, Cap. 7 minerais, Cap. 8 vitaminas) e o colostro NÃO entra nas exigências. DCAD, Ca, P, Mg, vit. E, Se etc. entram como **restrições/regras do otimizador e alertas**, não como equações.

Verificação: todas as equações e tabelas numéricas foram conferidas contra a imagem da página (dpi 140–300). Além disso, **reconstruí numericamente as Tabelas 11-3 e 11-4 a partir das equações** (script Python; ver §7 e §10): bateu em todas as linhas exceto as inconsistências listadas em §10.

---

# CAPÍTULO 11 — CRESCIMENTO

## 1. Papel no simulador
Calcula, para novilhas (e, com ajuste de fator, vacas em crescimento pós-parto), (a) a composição do PCV e do ganho conforme a maturidade (PC/PCMat), (b) exigências diárias de EM e PM = mantença + crescimento + gestação, (c) um piso de PM por Mcal de EM (PM/EM mínima), (d) metas de PC por fase, e (e) o caminho inverso: estimar GMD, gordura e proteína do ganho a partir da ingestão de EM. Entradas vêm dos Caps. 2 (IMS), 3 (EM da dieta, gestação) e 6 (PM, gestação); saídas alimentam o balanceamento e o otimizador (EM e PM requeridas, densidades de EM/PB). [pp.278–289]

## 2. Entradas

| Variável | Símbolo | Unidade | Definição | Faixa/valores típicos | Pág. |
|---|---|---|---|---|---|
| Peso corporal (vivo, sem jejum) | BW (PC) | kg | peso normal sem jejum | Holandesa: nascimento 42; desmame 84; concepção 385; pós-1º parto 574 (Tabela 11-2) | 278, 285 |
| Peso corporal à maturidade | MatBW (PCMat) | kg | PC adulto esperado; base da abordagem proporcional ao tamanho | referência 700 (Holandesa), 520 (Jersey); equações válidas para outras raças via razão BW/MatBW | 281, 285 |
| Ganho médio diário (meta ou calculado) | ADG (GMD) | kg/d | aumento de PC | Holandesa 0.70–0.98 nas Tabelas; pré-púbere meta 0.90 | 278, 285 |
| Ingestão de MS | DMI (IMS) | kg/d | para PMF (Eq. 11-3c); estimada no Cap. 2 | Tabela 11-3: 3.3 a 10.9 | 279, 287 |
| NDF da dieta | NDF%DM | % MS | para PMF (Eq. 11-3c) | não informado para as tabelas (valores implícitos 34–49 %, ver §10) | 279 |
| Ingestão de EM (para estimar ganho) | ME intake | Mcal/d | EM consumida | — | 287 |
| EM e PM de gestação | ME/MP for pregnancy | Mcal/d; g/d | vindos dos Caps. 3 e 6 | Tabela 11-3 (560 kg, 40 d pré-parto): 4.16 Mcal e 250 g; Tabela 11-4 (416 kg): 3.04 e 183 | 286, 287–288 |
| Conversão PB→PM da dieta | — | — | usada só nas tabelas para converter exigência de PM em % de PB | 0.62 | 287 |
| Dias de gestação / ECC / fase (pré- ou pós-parto) | — | — | para escolher fator 0.85 vs 0.82 e ECC alvo | ECC alvo 3.0–3.5 | 282, 283 |

## 3. Saídas

| Variável | Símbolo | Unidade | Definição | Valores típicos | Pág. |
|---|---|---|---|---|---|
| PC vazio e GPV | EBW, EBG | kg; kg/d | Eqs. 11-1a/b | EBW=0.85 BW | 278 |
| Composição do PCV (gordura, proteína, MLG, cinzas, água) | Fat_EBW etc. | kg/kg | Eqs. 11-4a–e | gordura 9 % do PCV a 70 kg; 22 % a 470 kg | 281 |
| Composição do GPV e do GMD (gordura, proteína, ER) | Fat_EBG, RE_EBG, Fat_ADG... | kg/kg; Mcal/kg | Eqs. 11-5a–f, 11-6a–c | ER_ADG de 1.90 a 3.58 Mcal/kg (Tabela 11-3) | 282 |
| EM de mantença; PM de mantença | — | Mcal/d; g/d | Eqs. 11-2, 11-3a–c | Tabela 11-3 | 279 |
| EM e PM de crescimento | — | Mcal/d; g/d | Eqs. 11-7, 11-8, 11-9 | — | 283 |
| PM/EM mínima | Minimum MP | g PM/Mcal EM | Eq. 11-10 | 49 a 33 | 286 |
| Exigências totais EM e PM | — | Mcal/d; g/d | soma + piso (Eq. 11-11) | Tabelas 11-3/11-4 | 286 |
| GMD, ER do ganho, gordura e proteína do ganho a partir de EM | ADG, RE, Fat_ADG, Protein_ADG | kg/d... | Eqs. 11-12a–e | — | 287–288 |
| Metas de PC (concepção, parto) e GMD por fase | — | kg; kg/d | Tabela 11-2 | — | 285 |
| Densidade de EM e de PB da dieta requerida | — | Mcal/kg MS; % MS | derivadas nas Tabelas 11-3/11-4 | EM 2.1–3.0; PB 12.7–24 % | 287–288 |

## 4. Equações

### 4.1 Peso corporal vazio e ganho de PCV — Eqs. 11-1a e 11-1b [p.278] (verificadas)
```
EBW = 0.85 * BW                    (Eq. 11-1a)
EBG = 0.85 * ADG                   (Eq. 11-1b)
```
EBW=PCV (kg); BW=PC (kg); EBG=GPV (kg/d); ADG=GMD (kg/d). 0.85 = 1 − enchimento intestinal (15 %); vem de NRC (1989), respaldado por Waldo et al. (1997). O comitê reconhece que o enchimento não é constante (Waldo: 11 % do GMD para 1,000 g/d com silagem de milho a 19 % para 770 g/d com alfafa) e adota valor fixo de 15 % [p.278]. Para vacas pós-parto o enchimento fixo é 18 % (fator 0.82) [pp.281, 282].

### 4.2 Mantença de EM — Eq. 11-2 [p.279] (verificada)
```
ME_maintenance (Mcal/d) = 0.15 * BW^0.75               (Eq. 11-2)
```
BW em kg. Igual à mantença de vacas; equivale a ~0.095 x BW^0.75 em EL (NASEM beef 2016). A atividade é presumida como 10 % da exigência; novilhas em piquetes grandes/pasto podem exigir mais; sem ajuste para crescimento compensatório, ECC ou temperatura [p.279].

### 4.3 Mantença de PM — Eqs. 11-3a, 11-3b, 11-3c [p.279] (verificadas em dpi 230; expoente de 11-3a é 0.60: corrigido pela imagem, o OCR leu "0.S")
```
MP_scurf (g/d)               = (0.20 * BW^0.60) / 0.69                                  (Eq. 11-3a)
MP_endogenous_urinary (g/d)  = 53 * 6.25 * BW * 0.001                                   (Eq. 11-3b)
MP_MFP (g/d)                 = ((11.62 + 0.134 * NDF%DM) * DMI) / 0.69                  (Eq. 11-3c)
```
- BW (kg); NDF%DM em % da MS; DMI (kg/d). Resultados em base PB (N x 6.25) [p.279].
- Eficiência PM→PL: 0.69 (meta de eficiência) para descamação e PMF; **1.0 para o N urinário endógeno** (por isso 11-3b não divide) [p.279].
- Mantença total de PM = soma das três (usado nas Tabelas 11-3/11-4; reproduzido, ver §7).
- ⚠ Diferença de formulação vs. Cap. 6: aqui a descamação é 0.20*BW^0.60/0.69 (sem o fator 0.85 de proteína verdadeira que aparece na Eq. 6-7a). O Cap. 11 trabalha direto em PB. Origem: "mesmas equações usadas para vacas adultas (ver Cap. 6)" [p.279]; n de estudos/R² não informados aqui.

### 4.4 Composição do PCV — Eqs. 11-4a a 11-4e [p.281] (verificadas)
```
Fat_EBW (kg/kg)     = 0.067 + 0.188 * (BW / MatBW)       (Eq. 11-4a)
FFM_EBW (kg/kg)     = 1 - Fat_EBW                         (Eq. 11-4b)
Protein_EBW (kg/kg) = 0.215 * FFM_EBW                     (Eq. 11-4c)
Ash_EBW (kg/kg)     = 0.056 * FFM_EBW                     (Eq. 11-4d)
Water_EBW (kg/kg)   = 0.729 * FFM_EBW                     (Eq. 11-4e)
```
- Fat_EBW = gordura (kg/kg de PCV); FFM = matéria livre de gordura; BW/MatBW adimensional (o texto equipara a EBW/PCV maduro, Eq. 11-8 [p.283]; as tabelas foram reproduzidas usando BW/MatBW).
- Composição constante da MLG: 21.5 % proteína, 5.6 % cinzas, 72.9 % água (Waldo et al., 1997) [p.281].
- Base: meta-análise de de Souza e VandeHaar (2018), **26 publicações, 129 médias de tratamentos** de Holandesas do nascimento à maturidade (Tabela 11-1). Regressão do teor de gordura do PCV vs PCV (linear serviu tão bem quanto quadrática/log/qualquer potência). **Linhas válidas só entre 70 e 490 kg de PCV** (legenda Fig. 11-1) [pp.280–281]. R², RMSE: não informados.
- Verificação do texto (calculada): a 70 kg de PCV (12 % do PCV maduro de 574 kg) gordura 9 % e proteína 20 %; a 470 kg (82 %) gordura 22 % e proteína 17 % [p.281]; coincide com 11-4a/c.
- PCV à maturidade de referência = 574 kg (82 % de 700) [p.281].

### 4.5 Composição do ganho de PCV — Eqs. 11-5a a 11-5f [p.282] (verificadas)
```
Fat_EBG (kg/kg)     = 0.067 + 0.375 * (BW / MatBW)                  (Eq. 11-5a)
FFM_EBG (kg/kg)     = 1 - Fat_EBG                                    (Eq. 11-5b)
Protein_EBG (kg/kg) = 0.215 * FFM_EBG                                (Eq. 11-5c)
RE_EBG (Mcal/kg)    = 9.4 * Fat_EBG + 5.55 * Protein_EBG             (Eq. 11-5d)
Ash_EBG (kg/kg)     = 0.056 * FFM_EBG                                (Eq. 11-5e)
Water_EBG (kg/kg)   = 0.729 * FFM_EBG                                (Eq. 11-5f)
```
- 0.375 = 2 x 0.188 (derivada da Eq. 11-4a: a gordura do ganho é a derivada da gordura do corpo em relação à massa). Valores de energia: **9.4 Mcal/kg de gordura e 5.55 Mcal/kg de proteína** (NRC, 2001) [p.281]. Ash e Water não são necessárias no modelo, só informativas [p.282].
- Idem: usadas com EBW = 0.85 x BW e EBG = 0.85 x ADG [p.282].

### 4.6 Composição do ganho de PC vivo — Eqs. 11-6a a 11-6c [p.282] (verificadas)
```
Fat_ADG (kg/kg)     = 0.85 * Fat_EBG          (Eq. 11-6a)
RE_ADG (Mcal/kg)    = 0.85 * RE_EBG           (Eq. 11-6b)
Protein_ADG (kg/kg) = 0.85 * Protein_EBG      (Eq. 11-6c)
```
- **Pós-primeiro parto** (ECC mantido entre 3.0 e 3.5; enchimento 18 %): usar Eqs. 11-5a–d, mas nas Eqs. 11-6a–c **substituir 0.85 por 0.82** [p.282].
- **Mudança de PC associada a mudança de ECC:** 62 % gordura, 8 % proteína, 6.3 Mcal/kg [p.282].
- Em animais próximos à maturidade (95 % do PCMat), GMD de "frame" real → 36 % gordura, 10.5 % proteína, 4.0 Mcal ER/kg [p.282] (conferi com as equações: 36.0 %, 10.5 %, 3.96).

### 4.7 EM para crescimento — Eq. 11-7 [p.283] (verificada)
```
ME_growth (Mcal/d) = RE (Mcal/d) / 0.40         (Eq. 11-7)
```
RE (energia retida) = RE_ADG x ADG (diária). Eficiência EM→ER = 0.40, igual ao NRC (2001) e NÃO validada para novilhas (só assumida) [pp.283, 289]. Também é assumido que digestibilidade e conversão ED→EM são as mesmas de vacas [p.289].

### 4.8 Eficiência PM→PL e PM para crescimento — Eqs. 11-8 e 11-9 [p.283] (verificadas)
```
NP_eff = 0.64 - 0.3 * (EBW / Mature_EBW)                   (Eq. 11-8)
MP_growth (g/d) = Retained_protein (g/d) / NP_eff          (Eq. 11-9)
```
- EBW não pode exceder Mature EBW; EBW/Mature EBW "pode ser equiparado" a BW/MatBW. Dá 0.60 (12 % do PCMat) a 0.39 (82 %) [p.283]. NRC (2001) ia de 0.77 a 0.39; NASEM (2016) usava 0.5 fixo [p.283].
- Retained protein (g/d) = Protein_ADG x ADG x 1000 (reproduzido nas Tabelas, §7).

### 4.9 PM/EM mínima — Eq. 11-10 [p.286] (verificada)
```
Minimum_MP (g PM / Mcal EM) = 53 - 25 * (BW / MatBW)        (Eq. 11-10)
```
Piso empírico (não é exigência de deposição) baseado em estudos de proteína/energia em novilhas (Whitlock 2002, Lammer & Heinrichs 2000, Pirlo 1997, Gabler & Heinrichs 2003) para: atingir ganhos desejados, minimizar gordura excessiva, otimizar frame, tecido magro, desenvolvimento mamário e leite futuro [p.286].

### 4.10 Exigências totais — equações sem número [p.286] (verificadas)
```
Total_ME_requirement (Mcal/d) = ME_maintenance + ME_growth + ME_pregnancy
Total_MP_requirement (g/d)    = MP_maintenance + MP_growth + MP_pregnancy
```
Gestação: Caps. 3 e 6 (não neste capítulo).

### 4.11 Piso de PM — Eq. 11-11 [p.286] (verificada)
```
Se MP (g/d) < (53 - 25 * BW/MatBW) * ME (Mcal/d), então
    MP (g/d) = (53 - 25 * BW/MatBW) * ME (Mcal/d)            (Eq. 11-11)
```
ME = a EM total (Mcal/d) da novilha. "A exigência total de PM deve ser aumentada se estiver abaixo do limiar mínimo PM/EM" [p.286]. Em todas as colunas exceto a última de 11-3, o piso foi o determinante (ver §7).

### 4.12 Estimativa de ganho a partir de EM — Eqs. 11-12a a 11-12e [pp.287–288]
```
RE (Mcal/d) = (ME_intake - ME_maintenance) * 0.40                                  (Eq. 11-12a)

ADG (kg/d) = RE / (0.85 * (1.74 + 3.08 * (BW/MatBW)) * (0.0012 * MatBW^0.1)^(1/1.1))   (Eq. 11-12b, COMO IMPRESSA)

RE_of_ADG (Mcal/kg) = RE (Mcal/d) / ADG (kg)                                       (Eq. 11-12c)

Fat_ADG (kg/kg) = 0.85 * ((RE_of_ADG / 0.85 - 1.19) / 8.21)                        (Eq. 11-12d)

Protein_ADG (kg/kg) = 0.85 * (1 - (Fat_content_of_ADG / 0.85) * 0.215)             (Eq. 11-12e, COMO IMPRESSA)
```
- ⚠ **Eq. 11-12b como impressa é dimensionalmente inconsistente** (com os parênteses impressos dá GMD ~100x errado). Reconstituição consistente (equivale à lógica descrita no texto: RE por kg base = 0.85*(1.74+3.08*BW/MatBW) para GMD base = 0.0012*MatBW kg/d, e RE/kg proporcional a GMD^0.1, ou seja RE proporcional a GMD^1.1):
```
K        = 0.85 * (1.74 + 3.08 * (BW/MatBW))             # Mcal ER/kg de ganho no GMD base
ADG_base = 0.0012 * MatBW                                # kg/d  (840 g/d p/ 700 kg; 624 g/d p/ 520 kg)
ADG      = ( RE * ADG_base^0.1 / K )^(1/1.1)             # RE em Mcal/d
```
 Teste (calculado): BW=336, MatBW=700, RE=2.30 → ADG=0.840 kg/d (concorda com a Tabela 11-3). Também K coincide com "Energia no GMD" da Tabela 11-3 (ex.: 0.85*(1.74+3.08*0.48)=2.74). **O desenvolvedor deve validar esta forma contra o livro/errata; marcada ⚠.**
- ⚠ **Eq. 11-12e como impressa** tem parênteses ambíguos. A forma consistente com 11-5c/11-12d (Fat_ADG = 0.85*Fat_EBG) é `Protein_ADG = 0.85 * (1 - Fat_ADG/0.85) * 0.215`. Teste: gordura no GMD 10.8 % → proteína 15.95 % (Tabela 11-3: 16.0 %). A Eq. 11-12d vem de inverter 11-5d: RE_EBG = 1.193 + 8.207*Fat_EBG (1.19 = 5.55*0.215; 8.21 = 9.4 − 1.19) [verificado].
- Lógica do texto: RE por dia ∝ GMD^1.097 no NRC (2001); aqui arredondado para **GMD^1.1 (ER por kg ∝ GMD^0.1)**; o teor base de ER do ganho é definido para novilha de **PCMat 700 kg ganhando 840 g/d (= 0.12 % do PCMat/d)**; para PCMat 520 kg o ganho base é 620 g/d (0.0012*520 = 0.624). Ganhos > base → maior ER/kg ou menor ganho do que o estimado sem ajuste [pp.286–287].
- **Importante:** o ajuste de GMD^0.1 NÃO é usado ao calcular exigências (as Tabelas 11-3/11-4 usam ER/kg constante com GMD, ex. 2.74 Mcal/kg a 336 kg para 700, 840 e 980 g/d), só na estimativa inversa de ganho [p.286].
- Ganho estimado a partir de PM: NÃO estimado (a PM/EM mínima foi o fator determinante). Se a PM/EM da dieta for menor que o da Tabela 11-3/11-4 para o PC, a dieta tem proteína insuficiente [p.287].

## 5. Parâmetros e tabelas

### Tabela 11-1 [p.280] — Estudos usados para as equações de composição (resumo)
Não é usada em cálculo. 31 linhas: 11 de novilhas (ex.: Brown 2005b, Chelikani 2003, Davis Rincker 2008b, Diaz 2001, Meinert 1992, Meyer 2005, Moallem 2004, Radcliff 1997, Steen 1992, Waldo 1997, Whitlock 2002), 9 de bezerras (Bartlett 2006 ... Tikofsky 2001) e 10 de vacas (Agnew 2005 ... von Soosten 2012). Colunas: método de composição (composição do PCV, de carcaça/costela, diluição de ureia ou D2O, K40), PCV avaliado (sim/não), faixa de PCV (kg) e faixa de GMD (g/d). Faixas gerais: novilhas PCV 40–584 kg, GMD 379–1,270 g/d; bezerras PCV 44–150 kg, GMD 250–1,230 g/d; vacas PCV 398–689 kg. Nota: se o PCV não foi avaliado, PCV = soma das partes, ou 0.85*PC (bezerras/novilhas) ou 0.82*PC (vacas). Linhas individuais: não transcritas (ver p.280).

### Tabela 11-2 [p.285] — Metas de peso (kg), idades e GMD (kg/d) (verificada na imagem em dpi 300)

| Item | % do PC à maturidade | Holandesa | Jersey |
|---|---|---|---|
| PC à maturidade | 100 | 700 | 520 |
| PC ao nascimento | 6 | 42 | 31 |
| PC ao desmame | 12 | 84 | 62 |
| PC à concepção | 55 | 385 | 286 |
| PC no pré-parto do primeiro parto | 91 | 638 | 426 ⚠ |
| PC no pós-parto do primeiro parto | 82 | 574 | 474 ⚠ |
| PC no pós-parto do segundo parto | 92 | 644 | 478 |
| Idade à concepção, meses | — | 13 | 13 |
| Idade ao primeiro parto, meses | — | 22 | 22 |
| GMD pré-púbere | 0.13 (%PCMat/d) | 0.90 | 0.67 |
| GMD pós-púbere | 0.10 | 0.69 | 0.51 |
| Ganho pós-puberdade + gestação | 0.13 | 0.92 | 0.69 |
| GMD na primeira lactação | 0.027 | 0.19 | 0.14 |
| GMD na segunda lactação | 0.022 | 0.15 | 0.11 |

⚠ Os valores de Jersey de pré-parto (426) e pós-parto (474) do 1º parto parecem trocados na impressão: 0.91*520 = 473 e 0.82*520 = 426. Transcrito como impresso; usar % x PCMat no modelo. Unidade da coluna "%": percentual do PCMat (para GMD, % do PCMat por dia: ex. 0.13 % x 700 = 0.91 kg/d).

### Tabela 11-3 [p.287] — Exigências de energia e proteína para novilhas com PCMat de 700 kg (verificada na imagem em dpi 170; reproduzida numericamente, ver §7)

| Item | 112 | 224 | 336 | 420 | 560 |
|---|---|---|---|---|---|
| PC vivo, kg | 112 | 224 | 336 | 420 | 560 |
| PC como % do PCMat | 16 | 32 | 48 | 60 | 80 |
| IMS estimada, kg/d | 3.3 | 6.0 | 8.0 | 9.3 | 10.9 |
| Mantença EM, Mcal/d | 5.2 | 8.7 | 11.8 | 13.9 | 17.3 |
| Mantença PM, g/d | 121 | 228 | 325 | 389 | 486 |
| Gordura corporal, % (do PC vivo) | 8.2 | 10.8 | 13.3 | 15.3 | 18.4 |
| Proteína corporal, % (do PC vivo) | 16.5 | 16.0 | 15.4 | 15.0 | 14.3 |
| Energia corporal, Mcal/kg | 1.69 | 1.90 | 2.11 | 2.27 | 2.53 |
| Gordura no GMD, % | 10.8 | 15.9 | 21.0 | 24.8 | 31.2 |
| Proteína no GMD, % | 16.0 | 14.9 | 13.8 | 12.9 | 11.6 |
| Energia no GMD, Mcal/kg | 1.90 | 2.32 | 2.74 | 3.05 | 3.58 |
| ER, Mcal/d — GMD 700 g/d | 1.33 | 1.62 | 1.92 | 2.14 | 2.50 |
| ER — 840 g/d | 1.60 | 1.95 | 2.30 | 2.56 | 3.00 |
| ER — 980 g/d | 1.86 | 2.27 | 2.68 | 2.99 | 3.50 |
| Ganho de proteína, g/d — 700 | 112 | 104 | 96 | 91 | 81 |
| — 840 | 134 | 125 | 116 | 109 | 97 |
| — 980 | 156 | 146 | 135 | 127 | 113 |
| EM para gestação, Mcal/d | — | — | — | — | 4.16 |
| PM para gestação, g/d | — | — | — | — | 250 |
| Exigência de EM, Mcal/d — 700 | 8.5 | 12.7 | 16.6 | 19.3 | 27.7 |
| — 840 | 9.2 | 13.6 | 17.5 | 20.3 | 28.9 |
| — 980 | 9.8 | 14.4 | 18.5 | 21.4 | 30.2 |
| Conversão de PM para PL (NP_eff) | 0.59 | 0.54 | 0.50 | 0.46 | 0.40 |
| PM/EM mínima, g/Mcal | 49 | 45 | 41 | 38 | 33 |
| Exigência de PM, g/d — 700 | 416 | 573 | 679 | 732 | 939 |
| — 840 | 448 | 610 | 718 | 772 | 979 |
| — 980 | 481 | 646 | 758 | 813 | 1,020 |
| EM, Mcal/kg MS dieta — 700 | 2.5 | 2.1 | 2.1 | 2.1 | 2.5 |
| — 840 | 2.7 | 2.3 | 2.2 | 2.2 | 2.7 |
| — 980 | 2.9 | 2.4 | 2.3 | 2.3 | 2.8 |
| PB, % da MS da dieta — 700 | 19.9 | 15.4 | 13.6 | 12.7 | 13.5 |
| — 840 | 21.5 | 16.4 | 14.4 | 13.4 | 14.1 |
| — 980 | 23.1 | 17.4 | 15.2 | 14.1 | 14.7 |

Nota de rodapé [p.287]: IMS estimada e as densidades de EM e PB baseadas na estimativa de IMS do Cap. 2 e usando **0.62 como conversão de PB para PM**. As novilhas da última coluna estão a **40 dias pré-parto** (por isso gestação só nessa coluna).
Observações da reconstrução (calculadas): "Gordura/proteína/energia corporal" = composição do PC VIVO (Eq. 11-4 x 0.85); "gordura/proteína/energia no GMD" = Eqs. 11-6 (ex.: 0.85*(0.067+0.375*0.16)=10.8 %).

### Tabela 11-4 [p.288] — Exigências de energia e proteína para novilhas com PCMat de 520 kg (verificada na imagem em dpi 170)

| Item | 83 | 166 | 250 | 312 | 416 |
|---|---|---|---|---|---|
| PC vivo, kg | 83 | 166 | 250 | 312 | 416 |
| PC como % do PCMat | 16 | 32 | 48 | 60 | 80 |
| IMS estimada, kg/d | 2.5 | 4.5 | 6.0 | 6.9 | 8.1 |
| Mantença EM, Mcal/d | 4.1 | 6.9 | 9.4 | 11.1 | 13.8 |
| Mantença PM, g/d | 90 | 170 | 242 | 290 | 362 |
| Gordura corporal, % | 8.2 | 10.8 | 13.3 | 15.3 | 18.4 |
| Proteína corporal, % | 16.5 | 16.0 | 15.4 | 15.0 | 14.3 |
| Energia corporal, Mcal/kg | 1.69 | 1.90 | 2.11 | 2.27 | 2.53 |
| Gordura no GMD, % | 10.8 | 15.9 | 21.0 | 24.8 | 31.2 |
| Proteína no GMD, % | 16.0 | 14.9 | 13.8 | 12.9 | 11.6 |
| Energia no GMD, Mcal/kg | 1.90 | 2.32 | 2.74 | 3.05 | 3.58 |
| ER, Mcal/d — GMD 520 g/d | 0.99 | 1.21 | 1.42 | 1.59 | 1.86 |
| — 624 | 1.19 | 1.45 | 1.71 | 1.90 | 2.23 |
| — 728 | 1.38 | 1.69 | 1.99 | 2.22 | 2.60 |
| Ganho de proteína, g/d — 520 | 83 | 77 | 72 | 67 | 60 |
| — 624 | 100 | 93 | 86 | 81 | 72 |
| — 728 | 116 | 108 | 100 | 94 | 84 |
| EM para gestação, Mcal/d | — | — | — | — | 3.04 |
| PM para gestação, g/d | — | — | — | — | 183 |
| Exigência de EM, Mcal/d — 520 | 6.6 | 10.0 | 13.0 | 15.1 | 21.5 |
| — 624 | 7.1 | 10.6 | 13.7 | 15.9 | 22.4 |
| — 728 | 7.6 | 11.2 | 14.4 | 16.7 | 23.4 |
| Conversão de PM para PL | 0.59 | 0.54 | 0.50 | 0.46 | 0.40 |
| PM/EM mínima | 49 | 45 | 41 | 38 | 33 |
| Exigência de PM, g/d — 520 | 323 | 448 | 532 | 574 | 710 |
| — 624 | 348 | 475 | 561 | 604 | 740 |
| — 728 | 372 | 503 | 590 | 634 | 771 |
| EM, Mcal/kg MS dieta — 520 | 2.6 | 2.2 | 2.2 | 2.2 | 2.7 |
| — 624 | 2.8 | 2.4 | 2.3 | 2.3 | 2.8 |
| — 728 | 3.0 | 2.5 | 2.4 | 2.4 | 2.9 |
| PB, % da MS — 520 | 20.9 | 16.2 | 14.4 | 13.4 | 14.1 |
| — 624 | 22.4 | 17.2 | 15.1 | 14.1 | 14.7 |
| — 728 | 24.0 | 18.2 | 15.9 | 14.8 | 15.3 |

Mesma nota de rodapé (IMS do Cap. 2; PB→PM = 0.62; última coluna 40 d pré-parto) [p.288].

### Constantes consolidadas do Cap. 11
| Constante | Valor | Pág. |
|---|---|---|
| Enchimento intestinal novilhas / vacas | 15 % / 18 % (EBW = 0.85 / 0.82 x BW) | 278, 281, 282 |
| Composição da MLG (proteína / cinzas / água) | 21.5 % / 5.6 % / 72.9 % | 281 |
| Energia retida por kg: gordura / proteína | 9.4 / 5.55 Mcal/kg | 281 |
| PCMat de referência e PCV maduro | 700 kg e 574 kg (82 %) | 281 |
| Eficiência EM→ER | 0.40 | 283 |
| Eficiência PM→PL: mantença (descamação, PMF) / N urinário endógeno | 0.69 / 1.0 | 279 |
| NP_eff crescimento | 0.64 − 0.3*(BW/MatBW) (0.60 a 12 %; 0.39 a 82 %) | 283 |
| Mantença EM | 0.15*BW^0.75 | 279 |
| Expoente de ER/kg vs GMD (só para estimar ganho) | 0.1 (ER ∝ GMD^1.1) | 286–287 |
| GMD base (ER base) | 0.12 % do PCMat/d (840 g/d p/ 700 kg; ~620 g/d p/ 520 kg) | 286–287 |
| Conversão PB→PM nas tabelas | 0.62 | 287 |
| ΔECC: gordura / proteína / energia | 62 % / 8 % / 6.3 Mcal/kg | 282 |

## 6. Regras de decisão / restrições para o otimizador
- **Metas de PC (% do PCMat):** concepção 55 % (Holandesa ~380–385 kg); 1ª inseminação ideal pode ser 50 % ou menos (a concepção costuma exigir mais de uma inseminação); pós-1º parto 82 % (570–574 kg); pós-2º parto 92 % (640–644 kg); meta de 1º parto pode ser > 82 % do PCMat em algumas situações. Metas de ECC em todas as etapas (reprodução e parto): **3.0–3.5** [p.283].
- **Idade:** 1º parto entre 22 e 24 meses = equilíbrio ótimo; concepção aos 13 meses para parto aos 22. Para 350–380 kg aos 13 meses: ~0.85 kg/d do nascimento aos 13 meses, ~0.90 kg/d após os 2 primeiros meses [p.283–284].
- **Limites de GMD pré-desmame→reprodução:** GMD > 0.9 kg/d reduz em geral o leite na 1ª lactação (Zanton e Heinrichs, 2005); 0.9–1.0 kg/d → queda pequena (≤ 5 %); > 1.0 kg/d → queda > 10 % [p.284]. Meta pré-púbere = 0.13 % do PCMat/d (0.90 Holandesa; **limite superior para Jersey pré-púbere ~750 g/d**) [p.285]. Janela de crescimento lento aceitável entre 3 meses de idade e puberdade, ou durante manejo para cobertura [p.289]. Faixa "razoável" citada: 0.65–0.95 kg/d [pp.284–285]. Cada 1 kg a menos de PC ao parto → ~10 kg a menos de leite na 1ª lactação [p.283].
- **Mínimo de PM/EM (restrição de piso):** PM/EM ≥ 53 − 25*(BW/MatBW) g/Mcal em toda a fase desmame→parto (Eq. 11-10); exigência de PM = máx(soma de mantença+crescimento+gestação; piso x EM) [pp.286]. Em termos de PB da dieta: exigência de PM / 0.62.
- **Proteína dietética (g PB/Mcal EM):** evidências citadas: 48–66 (Whitlock), 46–61 (Lammer & Heinrichs; melhor 61), 40–62 (Pirlo), 59 ou 68 melhor que 48 ou 77 (Gabler & Heinrichs) [pp.285–286]. NRC 2001 pedia 72 g PB/Mcal EM a 150 kg e 900 g/d [p.285].
- **Tipo de dieta:** dietas de alta energia com ingestão limitada são custo-efetivas se concentrado barato e reduzem metano/esterco; exigem fornecimento uniforme (ECC adequado em todos) [p.289].
- **Ambiente de criação:** metas da Tabela 11-2 valem para criação intensiva ou piquetes; a pasto/alimentos de menor qualidade, manter metas de PC mas com metas de idade mais tardias [p.286].
- **Monitoramento:** ganho de PC e ECC devem ser monitorados de perto; o modelo não prevê efeitos de atividade, ambiente, genética e saúde sobre ganho [pp.289–290].

## 7. Lógica e fluxo (ordem de cálculo)
Reproduzi as Tabelas 11-3 e 11-4 com este fluxo (todas as linhas coincidem, ver ⚠ de §10 para exceções):
1. x = BW/MatBW; EBW = 0.85*BW (Eq. 11-1).
2. Composição do ganho: Fat_EBG (11-5a) → FFM_EBG → Protein_EBG (11-5c) → RE_EBG (11-5d); multiplicar por 0.85 (ou 0.82 pós-parto) → Fat_ADG, Protein_ADG, RE_ADG (Eqs. 11-6).
3. Para um GMD alvo: RE = RE_ADG x ADG (ER/kg constante nas tabelas); EM_crescimento = RE/0.40 (11-7). PM_crescimento = (Protein_ADG x ADG x 1000)/NP_eff (11-8, 11-9).
4. Mantença: EM = 0.15*BW^0.75 (11-2). PM = 11-3a + 11-3b + 11-3c (precisa de IMS e FDN da dieta).
5. Gestação (EM e PM): Caps. 3 e 6 (entrada). Total_EM = soma; Total_PM_soma = soma.
6. Piso: PM_final = máx(Total_PM_soma; (53 − 25x) x Total_EM) (Eqs. 11-10/11-11).
7. Densidade requerida: EM (Mcal/kg MS) = Total_EM / IMS; PB (%MS) = PM_final / 0.62 / IMS / 10 [IMS do Cap. 2].
8. **Inverso (estimativa de ganho):** RE = (EM ingerida − EM mantença) x 0.40 (11-12a) → GMD (11-12b, forma reconstruída) → ER/kg (11-12c) → gordura (11-12d) e proteína (11-12e) do ganho.
- Verificações numéricas feitas: ex. 700 kg, 336 kg de PC, 840 g/d: ER = 2.74*0.84 = 2.30; EM = 11.8 + 2.30/0.4 = 17.5; PM piso = 41*17.5 = 718 (tabela: 718). Última coluna (560 kg com gestação): soma de PM = 486 + 97/0.40 (=242) + 250 = 979 (tabela 979), maior que o piso 33*28.9 = 955, portanto a soma prevalece; no Jersey 416 kg, soma = 362 + 150 + 183 = 695 < piso 33*21.5 = 710 e a tabela traz 710.
- Valores de NDF implícitos na PM de mantença (calculados invertendo 11-3c com a IMS da tabela): 36.5, 38.9, 44.7, 45.6, 49.1 % (700 kg) e 33.6, 37.8, 43.1, 45.8, 48.9 % (520 kg). O livro NÃO informa o NDF usado; o desenvolvedor deve tratar NDF como entrada.
- Dependências externas: IMS de novilhas (Cap. 2), EM/ED da dieta (Cap. 1–3), PM da dieta (Cap. 6), exigências de gestação (Caps. 3/6).

## 8. Limitações, incertezas e mudanças vs. NRC 2001
- **Mudou:** (i) as equações do 7º ed. vinham de gado de corte (mais gordura) com abordagem proporcional ao tamanho confusa (ex.: enchimento 14.5 % do PC mas só 4 % do ganho); agora equações próprias para Holandesas (129 médias, 26 estudos), com PCMat de referência de 700 kg (antes 500 kg, 25 % de gordura a ECC 3; vacas Holandesas maduras ECC 3 têm 22 % de gordura) [pp.278–281]. (ii) Energia do ganho não é mais ∝ PC^0.75; ajuste log/linear [p.279]. (iii) GPV = 85 % do GMD (NRC 2001: 96 %), o que reduz a proteína do ganho e as exigências de proteína relativas à energia [pp.282, 285]. (iv) NP/PM de 0.60 a 0.39 (antes 0.77→0.39; NASEM 2016: 0.5) [p.283]. (v) Teor de gordura/energia do ganho é maior que NRC 2001 em novilhas jovens e menor em velhas (Fig. 11-2) [p.282]. (vi) Nova PM/EM mínima (Eq. 11-10) [p.286].
- **Mantido igual ao NRC 2001:** eficiência EM→ER 0.40; atividade 10 % da mantença; uso do expoente ~0.1 para ER/kg vs GMD (arredondado de 0.097) [pp.279, 283, 286].
- **Admitidas lacunas:** enchimento intestinal não é constante; sem ajustes de crescimento compensatório, ECC ou temperatura na mantença; composição do ganho não ajustada à taxa de ganho nas exigências (dados diferem muito: Waldo 21 vs 25 % gordura; Radcliff 17 vs 25 %; Davis Rincker 8 vs 25 %; Meyer: ~2.1 vs quase o dobro Mcal/kg a 300–350 kg) [pp.288–289]; digestibilidade e ED→EM de novilhas = vacas; sem estimativa de ganho por PM; exigências de PM para leite futuro podem ser maiores que para frame [pp.286, 289]. Linhas de composição válidas só entre 70 e 490 kg de PCV [p.281]. Abordagem futura sugerida: estimar a composição do ganho de "frame" e usar ΔECC para desvios [p.289].

## 9. Conceitos e evidências relevantes
- Glândula mamária cresce alometricamente do nascimento à puberdade; dieta melhor pré-desmame ↑ leite futuro; plano alto entre desmame e puberdade pode ↓ leite [p.284]. Excesso de gordura (não só taxa de ganho) pode ser o problema; leptina inibe proliferação mamária estimulada por IGF-1 [pp.284–285].
- Lin et al. (1986): inseminadas aos 11.5 vs 15 meses → 23 vs 26 meses ao parto, −50 kg PC, −300 kg de leite; Abeni et al. (2000): −550 kg (7 %) de leite corrigido para energia [p.283]. Radcliff et al. (2000): 1.1 vs 0.8 kg/d → ECC à inseminação 4.2 vs 3.5; −10 % de leite [p.284]. Meyer et al. (2006): 0.95 vs 0.65 kg/d sem diferença na taxa de crescimento do parênquima, mas puberdade mais cedo e menor massa de parênquima [p.284].
- Programas "em escada" (alternar crescimento lento e rápido) parecem sem desvantagem a longo prazo [p.289].
- Figura 11-1 [p.281]: gordura e proteína no PCV vs PCV (pontos = médias de tratamento; linhas = Eqs. 11-4). Figura 11-2 [p.282]: composição do GMD (% proteína, % gordura, Mcal ER/kg) vs % do PCMat, nova edição (linha sólida) vs NRC 2001 a 0.6 e 1.0 kg/d.
- Mantença de PM idêntica à de vacas (Cap. 6) [p.279].

---

# CAPÍTULO 12 — VACAS SECAS E VACAS EM TRANSIÇÃO

## 1. Papel no simulador
Fornece (a) a equação de IMS de vacas e novilhas secas/pré-parto (Eqs. 12-1 e 12-2), única parte puramente quantitativa do capítulo; (b) dados de colostro (Tabela 12-1) que explicam por que NÃO se somam exigências de colostro; (c) regras e faixas para prevenção nutricional de distúrbios metabólicos (hipocalcemia/DCAD, fígado gorduroso, cetose, edema de úbere, retenção de placenta, deslocamento de abomaso), úteis como restrições e alertas do otimizador e como validações da formulação pré-parto. [pp.292–307]

## 2. Entradas

| Variável | Símbolo | Unidade | Definição | Faixa/valores típicos | Pág. |
|---|---|---|---|---|---|
| FDN da dieta | FDN (NDF) | % da MS | assume-se majoritariamente de forragem; limitado a 30–55 % | 30–55 | 297 |
| Semana pré-parto | Semana | semanas (número negativo) | −3 = dias 21 a 15 pré-parto; −2 = 14 a 8; −1 = 7 a 1 | −3, −2, −1 | 297 |
| PC da vaca/novilha | BW | kg | para converter kg/100 kg PC em kg/d | ex. 650 | 296 |
| Escore de condição corporal | ECC | escala 1–5 | > 4 → reduzir IMS em 8 % | — | 295, 297 |
| Paridade | — | nulípara vs multípara | novilhas: Eq. 12-2 (x 0.88) | — | 297 |

## 3. Saídas
| Variável | Unidade | Definição | Valores típicos | Pág. |
|---|---|---|---|---|
| IMS pré-parto de vaca | kg/100 kg PC/d | Eq. 12-1 | 2.0, 1.9, 1.8 para FDN 30, 40, 50 % (início do período seco = valor da semana −3) | 297 |
| IMS pré-parto de novilha | kg/100 kg PC/d | Eq. 12-2 (vaca x 0.88) | — | 297 |
| Secreção de colostro (referência, não entra em exigências) | kg; Mcal; kg; g Ca... | 10 kg de colostro Holandesa | 14 Mcal, 1.35 kg proteína, 21 g Ca, 30 mg retinol, 60 mg tocoferol | 294 |

## 4. Equações

### Eq. 12-1 — IMS de vacas secas/pré-parto [p.297] (verificada na imagem)
```
IMS_diária (kg/100 kg PC) = 1.47 - [(0.365 - 0.0028 * FDN) * Semana] - 0.035 * Semana^2      (Eq. 12-1)
```
- FDN = % da MS da dieta (assumindo que a maioria seja de forragem). **Se FDN < 30, usar 30; se FDN > 55, usar 55.** Semana = semana antes do parto previsto, **expressa como NÚMERO NEGATIVO** (−3, −2, −1). Válida apenas para dietas com 30–55 % de FDN [p.297].
- **Vacas com ECC > 4: reduzir a IMS estimada em 8 %** (dados limitados; Hayirli et al., 2003) [p.297].
- **Período seco inicial (dias 60 a 21 pré-parto): IMS = valor da semana −3** (exemplos: 2.0, 1.9 e 1.8 kg/100 kg PC para dietas com 30, 40 e 50 % de FDN) [p.297].
- Efeito: no período seco inicial, menos FDN → maior IMS; perto do parto o efeito da FDN diminui (Fig. 12-1) [p.297].
- Origem: regressão múltipla combinando dados de Hayirli et al. (2003) e estudos recentes (Holcomb 2001, Dann 2006, Janovick e Drackley 2010, Mann 2015); só estudos com forragem como fonte predominante de FDN. n de estudos, R² e RMSE: não informados. Substitui as funções de decaimento logarítmico do NRC 2001 (RMSEP de 77 % da ingestão média e viés de +1.1 kg em vacas) [p.296].
- Verificação (calculada): semana −3: FDN 30 → 1.998; 40 → 1.914; 50 → 1.830 (coincide com 2.0/1.9/1.8 do texto). Para obter kg/d: multiplicar por BW/100.
- ⚠ Imprecisa com muitos subprodutos de FDN muito digestível (casca de soja, DDG/DDGS) — a IMS real pode ser bem maior [pp.296–297].

### Eq. 12-2 — IMS de novilhas pré-parto [p.297] (verificada)
```
IMS_novilha (kg/100 kg PC) = (1.47 - [(0.365 - 0.0028 * FDN) * Semana] - 0.035 * Semana^2) * 0.88     (Eq. 12-2)
```
Mesmas regras de FDN/Semana; fator 0.88 = redução de 12 % (diferença entre novilhas e vacas na fase inicial do período seco, 60 a 22 dias pré-parto, Hayirli et al., 2003). Sem interação paridade x FDN x estágio por falta de dados [p.297]. Derivada com dados de Holandesas; "presume-se que funcionem para outras raças". Observação: com a dieta mais digestível (39 % FDN) Janovick et al. (2011) viram IMS semelhante entre novilhas e vacas (~2 kg/100 kg PC) de 35 a 21 dias pré-parto; com palha (51 % FDN) novilhas comeram ~25 % menos [p.296–297].

### Equações de DCAD (texto, sem numeração) [p.304] (verificadas na imagem)
```
DCAD (mEq/kg MS) = (Na + K) - (Cl + 0.6 * S)        # melhor preditora de pH urinário e mais associada à febre do leite (Charbonneau et al., 2006)
DCAD (mEq/kg MS) = (Na + K) - (Cl + S)              # provavelmente a mais usada (DeGaris e Lean, 2008)
```
Unidades: mEq por kg de MS da dieta; Na, K, Cl, S em mEq/kg MS (laboratórios medem S em vez de sulfato). Com base na meta-análise (n e R² não informados aqui), **DCAD de ~ −200 mEq/kg (forma (Na+K)−(Cl+S)) é necessário para pH urinário 6.5** [p.304]. Ver Cap. 7 para as equações de DCAD do modelo.

## 5. Parâmetros e tabelas

### Tabela 12-1 [p.295] — Composição média do colostro (Holandesa; valores entre parênteses = Jersey) (verificada na imagem)

| Nutriente | Concentração (Holandesa) | Jersey |
|---|---|---|
| Proteína bruta, g/kg | 145 | 193 |
| Gordura, g/kg | 65 | 50 |
| Lactose, g/kg | 25 | 25 |
| Energia bruta, Mcal/kg | 1.4 | 1.5 |
| Retinol, mg/kg | 3.0 | — |
| α-Tocoferol, mg/kg | 6.0 | — |
| Vitamina B12, µg/kg | 19 | — |
| Cálcio, "mg/kg" ⚠ | 2.1 | 2.4 |
| Fósforo, "mg/kg" ⚠ | 1.8 | — |
| Magnésio, "mg/kg" ⚠ | 0.3 | — |
| Potássio, "mg/kg" ⚠ | 1.3 | — |
| Sódio, "mg/kg" ⚠ | 0.9 | — |
| Cobre, mg/kg | 0.5 | — |
| Selênio, mg/kg | 0.04 a 0.17 (menor = Se inorgânico; maior = Se-levedura) | — |
| Zinco, mg/kg | 15 | — |

Notas: Cu, Mn e Fe são muito baixos e não mostrados. ⚠ Unidade impressa "mg/kg" para Ca, P, Mg, K e Na é evidentemente g/kg (10 kg de colostro x 2.1 = 21 g de Ca, como no texto [p.294]). Referências por linha: ver p.295 (não transcritas).

### Valores do texto (colostro e cálcio) [pp.294, 302–303]
| Item | Valor | Pág. |
|---|---|---|
| Colostro 1ª ordenha | ~4 kg (1ª lactação) a ~8 kg (mais velhas); Jersey ~4 kg (2.5 kg inverno a 6.6 kg verão) | 294 |
| Colostro no 1º dia (Holandesa) | 8–14 kg | 294 |
| Secreção em 10 kg de colostro | 14 Mcal, 1.35 kg proteína, 21 g Ca, 30 mg retinol (~100,000 UI de vit. A), 60 mg tocoferol (⚠ ver §10) | 294–295 |
| Ca de 7 kg de colostro (Mann 2016) | 7 x 2.1 = ~16 g de Ca removidos do plasma | 302 |
| Ca para vaca de 650 kg, 12 kg MS, final de gestação | absorver ~24 g/d (mantença 11 g + feto 13 g) | 302 |
| Ca nas 5 primeiras ordenhas | 44 kg de leite, >2 g Ca/L → ~88 g, ou ~35 g/d com 2 ordenhas/d (4x a exigência pré-parto) | 302–303 |
| Pool plasmático permutável de Ca | ~10 mg/kg PC (vaca de 650 kg: renovado > 5 vezes/dia nos 2–3 primeiros dias) | 303 |

## 6. Regras de decisão / restrições para o otimizador

**Ingestão e dieta pré-parto**
- Aplicar Eq. 12-1/12-2 com FDN truncado em 30–55 %; ECC > 4 → x 0.92; novilhas x 0.88 [p.297]. Fatores: IMS cai nos 7–10 dias pré-parto; vacas/novilhas gordas (> 4) consomem ~8 % menos; vacas doentes/hipocalcêmicas comem menos [pp.295–296].
- Efeitos de dieta: PB entre ~10 e 16 % em geral não altera a IMS pré-parto; PNDR associada negativamente à IMS (provavelmente efeito da fonte); gordura reduz IMS só em novilhas; mais FDN de baixa qualidade (gramínea de baixa qualidade, casca de algodão, palha) reduz IMS [pp.295–296]. Médias por classe de FDN (Hayirli 2002): baixa (28–32 %) 2.0; média (35–50 %) 1.7; alta (50–62 %) 1.6 kg/100 kg PC nas últimas 3 semanas [p.296].
- **Proteína pré-parto (vacas):** > ~12 % PB provavelmente não aumenta leite; meta-análise (Lean 2013) sem efeito da PB pré-parto; PNDR extra e PM pré-parto não afetam vacas, mas PM extra pré-parto **beneficia novilhas** (Husnain e Santos, 2019) [pp.297–298]. Balanço de N materno positivo com 10.6 % PB (Putnam e Varga) [p.298]. A PB adicional para crescimento mamário (~120–130 g/d, ≈ 1 ponto percentual de PB da dieta) **não foi incluída no modelo** [p.298].
- **Energia pré-parto:** aumentar amido/energia (substituindo FDN) eleva IMS pré-parto, mas em geral NÃO aumenta IMS pós-parto nem leite; dietas pré-parto com **menor** concentração energética reduzem risco de cetose subclínica e clínica; mesmo restrição de ~50 % da ingestão pré-parto não afetou pós-parto (Dann 2006). Estudos típicos compararam ~exigência vs 25–50 % de excesso de energia; só alguns viram queda de leite com redução da energia pré-parto [p.298].
- **Colostro:** NÃO incluído nas exigências (síntese nos últimos dias; proteína do colostro de curto prazo; sem efeito benéfico demonstrado de maior aporte pré-parto), mas o usuário deve reconhecer o impacto potencial nas últimas dias [pp.294–295].
- **Vitamina E:** exigência aproximada 1,000 UI/d; 4,000 UI/d nas últimas 2 semanas preveniu queda de tocoferol plasmático e reduziu mastite clínica (Weiss 1997); 2,000 UI/d (não 1,000) reduziu CCS (Baldi 2000) [p.295]. **Vitamina A:** perda plasmática de retinol ocorre mesmo com 550,000 UI/d (~7x NRC 2001); acima das recomendações do Cap. 8 não se espera efeito em retenção de placenta; β-caroteno 600–1,200 mg/d reduziu retenção de placenta mas sem dados para IA [pp.295, 302]. **Selênio:** dieta basal < 0.1 mg Se/kg MS + 0.1–0.3 mg/kg adicionais (ou injeção 2–3 semanas pré-parto) reduz retenção de placenta; ingestões acima das recomendadas (Cap. 7) e vitamina E acima das recomendadas (Cap. 8) provavelmente sem efeito [pp.301–302].
- **PB baixa extrema:** 8 % PB durante todo o período seco → 50 % de retenção de placenta vs 20 % com 15 % PB (Julien 1976) [p.302].

**Hipocalcemia / DCAD (prevenção de febre do leite)**
- Ca plasmático normal 9–10 mg/dL (2.25–2.5 mM); febre do leite em ~5 % das multíparas, Ca < 4.5 mg/dL (1.12 mM); hipocalcemia subclínica (< 8.0–8.6 mg/dL, depende do estudo) em ~50 % das multíparas e 25 % das novilhas [p.302]. Jersey/Guernsey têm maior incidência (colostro com ~20 % mais Ca) [p.303].
- **Estratégia aniônica:** reduzir DCAD [(Na+K)−(Cl+S)] até ~ **−200 mEq/kg MS** (pH urinário alvo 6.5). **Alvo de pH urinário: < 7.0 e geralmente próximo de 6.0**; abaixo de 6.3 a excreção líquida de ácido deixa de acompanhar a DCAD (NH4+ urinário aparece); **pH < 5.3–5.5 = acidose metabólica não compensada, que reduz muito a IMS**; pouca diferença prática no grau de hipocalcemia entre pH 5.5 e 6.7; pH 7.3 é melhor que 7.9 mas pior que 6.0 [p.304]. Se a adição de ânions não levar o pH urinário a < 7.0, não há melhora no status de Ca [p.304].
- Cl é absorvido com ~100 % de eficiência; **sulfato tem apenas 60 % do efeito acidificante do Cl** (daí o 0.6 S) [p.303]. K e Na (sem contra-íon inorgânico, ex. bicarbonato) são alcalinizantes (absorção ~100 %); Ca e Mg menos (absorção baixa); carbonato de cálcio tem leve efeito alcalinizante [pp.303–304]. Vacas em dietas de forragem (alto K) vivem em alcalose metabólica compensada que reduz a resposta ao PTH [p.303].
- **Ca dietético com DCAD negativa:** concentração ideal "não conhecida"; dietas aniônicas bem-sucedidas continham **0.65–1.7 % de Ca**; atendida a exigência de Ca, mais Ca tem pouco efeito se o sangue estiver igualmente acidificado [pp.304]. A DCAD baixa pode reduzir a IMS por palatabilidade ou efeito metabólico; suplementos aniônicos comerciais são mais palatáveis [p.304].
- **Estratégia de baixo Ca (alternativa):** balanço negativo de Ca por 7–14 dias antes do parto; Ca dietético < 18 g/d (provê só 5–9 g absorvíveis); para ATENDER a exigência de uma vaca de 650 kg com 12 kg MS e disponibilidade de 0.44 (dieta de forragem), a dieta precisaria de ~52 g de Ca = **0.43 % da MS**; dietas realmente deficientes em Ca são muito difíceis com alimentos comuns [p.304]. Zeólita A (dietas com 0.6–0.7 % Ca) liga Ca e P (pode baixar Mg plasmático, mas não quando a dieta tem > 0.21 % Mg); ácido fítico de farelo de arroz tratado também liga Ca [pp.304–305].
- **Fósforo:** excesso de P pré-parto agrava a hipocalcemia (FGF23 ↓ 1,25-(OH)2 vit. D); **restringir P apenas à exigência**: dieta aniônica com **0.21 % P** (≈ exigência) teve menos hipocalcemia que com **0.44 % P**; P sérico normal 4–6 mg/dL (1.23–1.86 mmol/L); decúbito hipofosfatêmico (< 1.5 mg/dL, 0.46 mmol/L) é complicação, não causa dietética [p.305].
- **Magnésio:** Mg sanguíneo normal 1.9–2.4 mg/dL (0.8–1 mmol/L); < 1.25 mg/dL (0.5 mmol/L) compromete o PTH; < 1.7 mg/dL (0.7 mmol/L) altera a resposta tecidual; Mg sanguíneo ≤ 2.0 mg/dL (0.83 mmol/L) em 24 h pós-parto sugere Mg dietético inadequado. **Aumentar Mg dietético de 0.3 para 0.4 % da MS (DCAD e Ca constantes) → ~62 % menos risco de febre do leite** (Lean 2006) [p.305].
- **Vitamina D:** seguir Cap. 8; megadoses (até 10 milhões de UI entre 4 e 14 dias pré-parto) previnem mas ficam muito próximas da toxicidade (calcificação metastática); doses menores podem induzir febre do leite; 25-OH e 1,25-(OH)2 D com resultados inconsistentes/impraticáveis [pp.305–306].

**Fígado gorduroso e cetose** [pp.298–300]
- Alerta: AGNE pré-parto > 0.5 mEq/L e pós-parto > 1.0 mEq/L (risco); saudáveis < 0.2 mEq/L até dias antes do parto, pico ~0.8–1.0 mEq/L no 2º–3º dia de lactação. Fígado moderado (5–10 % TG do peso úmido) a grave (> 10 %) quase sempre acompanha cetose [pp.293, 298].
- Cetose: BHBA > 1.2 mmol/L (corte 1.0–1.4) define cetose subclínica; incidência de rebanho 20–40 % [p.299]. Tipo 1 (semanas após o parto; falta de precursores de glicose) e tipo 2 (no parto; fígado gorduroso) [p.300].
- Prevenção/estratégias: evitar obesidade (ECC) no parto; amido pós-parto ↑ reduz BHBA, ↑ glicose e reduziu acúmulo de gordura hepática; monensina pós-parto ↓ BHBA (não demonstrou reduzir gordura hepática); propilenoglicol (drench/bolus) ↓ BHBA; colina protegida ↓ gordura hepática; niacina protegida ↓ AGNE sem efeito claro em gordura hepática; gordura dietética sem efeito consistente (AG saturados podem ↓ lipídios hepáticos); amido pré-parto ↑ IMS pré-parto mas em geral não reduz gordura hepática [pp.299–300]. Doses específicas de colina/niacina/monensina/propilenoglicol: não informadas nestas páginas.

**Edema de úbere** [pp.300–301]: limitar Na e K suplementares e usar forragens de baixo K (se o edema for prevalente); ingestão excessiva de sais cloretos de Na ou K aumenta severidade em novilhas; ~450 g K/d (alfafa adubada com K) e 454 g de NaCl+KCl/d foram associados; CaCl2 a ~1.5 % da MS frequentemente reduziu prevalência/severidade (resultados mistos); vitamina E 1,000 UI/d reduziu edema; Fe de sulfato ferroso (12 g/d, ~1,300 mg/kg MS) anulou o efeito da vit. E.

**Retenção de placenta e metrite** [pp.301–302]: definição RP = não expulsão em 24 h; fatores nutricionais acima (Se, vit. E, A, β-caroteno, Ca, calcidiol em vez de colecalciferol [Martinez 2018], energia/proteína extremamente deficientes, vacas gordas).

**Deslocamento de abomaso** [pp.306–307]: reduzir fatores que limitam IMS: espaço de cocho < 30 cm/vaca, sobras não removidas, cocho vazio parte do dia, lotes/cochos lotados, TMR mal misturada, ingredientes não palatáveis; hipocalcemia subclínica ↑ 3.7x a probabilidade; mais grão no final da gestação ↑ incidência; fornecer fibra efetiva adequada (Cap. 5) [p.307]. Vacas gordas na secagem e perda excessiva de ECC até 4 semanas pós-parto são fatores de risco [p.306].

## 7. Lógica e fluxo
1. Escolher o período: seco inicial (60 a 21 dias pré-parto; IMS constante = semana −3) e pré-parto imediato (semanas −3, −2, −1; Eq. 12-1); aplicar x 0.92 se ECC > 4 e x 0.88 se novilha.
2. IMS (kg/d) = Eq. 12-1/12-2 x BW/100.
3. Exigências de nutrientes: usar capítulos individuais (energia, proteína, minerais, vitaminas); NÃO somar colostro. A PM de crescimento mamário não é somada (decisão explícita).
4. Checagens da dieta pré-parto: DCAD (se aniônica), Ca %, P %, Mg %, vit. E/A, Se; ver §6.
- Dependências: DCAD e exigências minerais (Cap. 7), vitaminas (Cap. 8), fibra efetiva (Cap. 5), energia e IMS de vacas lactantes (Cap. 2).

## 8. Limitações, incertezas e mudanças vs. NRC 2001
- Mudança: IMS pré-parto agora depende de FDN e semana (NRC 2001: funções logarítmicas só do dia, uma para novilhas e outra para vacas; precisão ruim em vacas). Sem dados para interação paridade x FDN x estágio de gestação [pp.296–297].
- Equação imprecisa com subprodutos de FDN muito digestível; fonte de FDN/forragem raramente reportada nos estudos [pp.296–297].
- Efeitos de dieta de transição na morfologia ruminal, DCAD ótima de Ca e concentração ideal de Ca com dietas aniônicas "não conhecidas"; aminoácidos pré-parto, efeito da proteína na qualidade/produção de colostro e diferença de PB/PM em novilhas: dados insuficientes [pp.294, 297–298, 304].

## 9. Conceitos e evidências relevantes
- Transição = últimas 3 semanas de gestação + primeiras 3 de lactação; insulina, IGF-1 e leptina ↓ e GH ↑; resistência à insulina; hormônios tireoidianos ↓ ~50 % no parto; AGNE sobem 1–2 dias antes do parto; glicogênio hepático se recupera até o dia 14; mobilização de proteína corporal cessa em ~4 semanas de lactação; massa ruminal +5 % entre 1 semana pré e 10 dias pós-parto [pp.292–293].
- Imunossupressão no periparto (neutrófilos, Ig para colostro, hipocalcemia); estresse oxidativo comum e pior com obesidade; Cu, Zn, Mn, Fe, Se e vit. E/A/β-caroteno em sistemas antioxidantes [pp.293–294].
- Novilhas têm homeostase de Ca mais robusta (mais osteoclastos; mais receptores de vit. D) [p.303].

## 10. Dúvidas / riscos de OCR (⚠ para conferência humana)
1. ⚠ **Eq. 11-12b** (p.287): impressa de forma dimensionalmente inconsistente; propus reconstrução `ADG = (RE*(0.0012*MatBW)^0.1/(0.85*(1.74+3.08*BW/MatBW)))^(1/1.1)` validada contra a Tabela 11-3 (RE=2.30 → 0.840 kg/d). Confirmar com errata/autores.
2. ⚠ **Eq. 11-12e** (p.288): parênteses impressos ambíguos; usei `0.85*(1 − Fat_ADG/0.85)*0.215` (bate com 11-5c e com Tabela 11-3).
3. ⚠ **Tabela 11-2, Jersey** (p.285): pré-parto 426 e pós-parto 474 parecem trocados (0.91*520 = 473; 0.82*520 = 426). Transcrito como impresso.
4. ⚠ **Tabelas 11-3/11-4, coluna do PC de 80 % (40 d pré-parto), linha "PB, % da MS"**: os valores impressos (13.5/14.1/14.7 e 14.1/14.7/15.3) correspondem ao PISO PM/EM x EM, e não à PM da soma impressa (939/979/1,020 em 11-3; ex.: 939/0.62/10.9 = 13.9 % ≠ 13.5 %). Para o Jersey (710/740/771) bate. Provável inconsistência da tabela; a linha "Exigência de PM" da coluna 560 kg usa a soma (mantença 486 + proteína retida/NP_eff + gestação 250 = 938 para 700 g/d), não o piso (914).
5. ⚠ **Tabela 12-1** (p.295): unidades "mg/kg" de Ca, P, Mg, K, Na são na verdade g/kg; "Selênio 0.04 a 0.17" (o OCR lia 0.177; corrigido pela imagem).
6. ⚠ **Colostro, p.294–295:** texto diz 1.35 kg de proteína para 10 kg de colostro, mas a Tabela 12-1 (145 g/kg) implica 1.45 kg; tocoferol aparece como 60 mg (p.294) e "135 UI de vit. E (50 mg de RRR-tocoferol)" (p.295) — valores internos inconsistentes. "135 UI" provavelmente é erro (o texto original em inglês não foi consultado).
7. ⚠ **p.296:** "nulíparos consumiram cerca de 127 % menos MS" no OCR; a imagem diz **12 %** (corrigido pela imagem); coerente com o fator 0.88 da Eq. 12-2.
8. ⚠ NDF usado para PMF nas Tabelas 11-3/11-4 não informado (valores implícitos de 34 a 49 %, ver §7 do Cap. 11).
9. Eq. 11-3a: expoente **0.60** (OCR leu "0.S"; corrigido pela imagem em dpi 230). Eq. 11-1a no OCR aparecia como "11-la" (é 11-1a).
10. ⚠ Eq. 11-3b é linear em BW (sem expoente); conferido na imagem.
11. Tabela 11-1 e referências de cada linha da Tabela 12-1 não transcritas linha a linha.

COBERTURA: páginas lidas 278–315 (todas). Texto do Cap. 11: 278–289; referências do Cap. 11: 289–291 (percorridas, sem extração). Texto do Cap. 12: 292–307; referências do Cap. 12: 307–315 (percorridas por amostragem; apenas lista bibliográfica). Imagens conferidas: pp.278–283, 285–288, 294–297, 304 (equações, Tabelas 11-1 a 11-4 e 12-1, Fig. 12-1). Páginas apenas por OCR de texto narrativo, sem equações/tabelas: 284, 289, 292–293, 298–303, 305–307 (números-chave do texto, como limiares clínicos, conferidos no OCR sem verificação por imagem: ⚠ leitura de OCR). Ficaram de fora: Tabela 11-1 linha a linha e referências por linha da Tabela 12-1 (não usadas em cálculo); equações do Cap. 7 (DCAD detalhado), Cap. 3/6 (exigências de gestação) e Cap. 2 (IMS de novilhas), que são entradas externas.

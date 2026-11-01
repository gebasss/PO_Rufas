# NASEM 2021 (Bovinos Leiteiros, 8ª ed., tradução PT-BR) — Notas técnicas: Capítulo 10 "Exigências Nutricionais de Bezerras"

**Páginas impressas cobertas:** 219–277. Texto técnico: 219–262 (o texto termina no item "Butirato", p.262). Referências: p.262–277 (apenas percorridas; nenhum dado numérico do modelo nelas).
**Usado diretamente no modelo? Capítulo 10: SIM (núcleo do submodelo "bezerra", animal < 18% do PC à maturidade = até 125 kg para vaca de 700 kg).** Partes só discursivas, que não entram em cálculo (viram alertas/regras de manejo): níveis de fornecimento de leite, forma física do concentrado, forragem, frequência, alojamento, nutrição fetal, colostro (exceto como regra de manejo), água/eletrólitos, doenças, sucedâneos (proteínas alternativas, AA, gordura), leite integral/descarte, aditivos.

Convenções: `^` expoente, `_` subscrito, `*` multiplicação. Siglas PT do livro: PC=peso corporal (BW), PCV=peso corporal vazio, GMD=ganho médio diário (ADG), GPV=ganho de PCV, PCMat=peso corporal à maturidade (MatBW), IMS=ingestão de matéria seca, EM=energia metabolizável (ME), IEM=ingestão de EM, EMm=EM de mantença, ELm/ELg=energia líquida de mantença/ganho, ER=energia retida, PCa=produção de calor (HP), k_m/k_g=eficiências de uso da EM p/ mantença/ganho, PM=proteína metabolizável (MP), PB=proteína bruta, PL=proteína líquida, PLg=PL de ganho, PBEU=PB endógena urinária, PMF=PB metabólica fecal, NMF=N metabólico fecal, MR/sucedâneo=milk replacer, IA=ingestão adequada (AI), CA=coeficiente de absorção, EAAbs=eficiência aparente de absorção de IgG. Variáveis em inglês das equações do livro foram traduzidas só onde o livro já traduziu (EMiDL=MEiLD, Tpconc=FPstarter).

Metodologia de verificação usada nestas notas: (a) toda equação e tabela foi conferida contra a imagem da página (130–250 dpi); (b) **além disso, reconstruí numericamente as Tabelas 10-7, 10-8, 10-9, 10-10, 10-11 e 10-17 a partir das equações impressas** (script próprio; ver seção 7). Isso confirmou os dígitos de quase todas as células e revelou erros de impressão do próprio livro (marcados ⚠). Quando OCR e imagem divergiram, vale a imagem: `(corrigido pela imagem)`.

---

## 1. Papel no simulador

O capítulo define o submodelo de **bezerras pré-ruminantes, em transição e desmamadas até 125 kg de PC**, em quatro situações: (i) só leite/sucedâneo, (ii) leite/sucedâneo + concentrado inicial (com ou sem forragem), (iii) desmamadas (só alimento sólido), (iv) vitelos (veal; só líquido, ganho alto). Substitui, para essa categoria, os módulos de energia/proteína/minerais dos cap. 3, 6, 7 e 11. Entrega: IMS do concentrado inicial prevista, EM dos alimentos líquidos e sólidos, exigência de EM (mantença + termorregulação + ganho), exigência de PM e PB, ganho de PCV/GMD permitido por EM e por PM, e Ingestões Adequadas (IA) de macro/microminerais e vitaminas lipossolúveis. Também traz regras de manejo (colostro, nível de líquido, desmame, concentrado) que viram restrições/alertas.

Fases digestivas (Davis e Clark, 1981) [p.220]: (1) **líquida** (leite/sucedâneo supre quase tudo; goteira esofágica desvia o líquido ao omaso), (2) **transição** (líquido + concentrado inicial; o inicial sustenta o desenvolvimento retículo-ruminal), (3) **ruminante** (tudo de alimento sólido; fermentação e síntese microbiana ainda imaturas no início).

Mudanças vs NRC 2001 [p.219–220]: (1) PCV usado em todos os cálculos; (2) nova equação de IMS de concentrado inicial; (3) exigências de energia atualizadas (mantença distinta por categoria/raça/ambiente; composição do ganho; novo k_g); (4) cálculo de EM dos alimentos revisado; (5) PM no lugar de proteína digestível aparente (PDA); (6) minerais viram IA (abordagem fatorial) e algumas vitaminas revisadas.

---

## 2. Entradas

| Variável | Símbolo/sigla | Unidade | Definição | Faixa/valores típicos | Pág. |
|---|---|---|---|---|---|
| Categoria animal | — | — | "bezerra" se PC < 18% do PCMat (125 kg p/ PCMat 700 kg); acima disso "novilha" (cap. 11). Eq. 10-15 não vale > 200 kg nem p/ novilhas ruminantes > 125 kg | — | 220, 230 |
| Porte/raça | RP/RG | — | RP = raça pequena (base Jersey, PCMat = 530 kg); RG = raça grande (base Holandesa, PCMat = 700 kg) | RP 530; RG 700 | 236 |
| Peso corporal | PC | kg | Peso vivo | tabelas: 25–225 kg | 220–240 |
| PC à maturidade | PCMat | kg | Para a razão PC/PCMat na Eq. 10-15 | 530 / 700 | 229–230, 236 |
| Idade | — | semanas | Usada como proxy de Tpconc (assume concentrado oferecido na 1ª semana de vida) | pré-desmame < 8 sem; desmamadas > 8 sem | 220–221 |
| Semana do 1º fornecimento de concentrado | Tpconc | semanas | variável das Eq. 10-1/10-2 | — | 220–221 |
| Ganho médio diário alvo (ou real) | GMD (ADG) | g/d ou kg/d | Meta de ganho; as tabelas cobrem 200–1,500 g/d | 0.2–1.5 kg/d | 235–240 |
| Estado alimentar | — | — | só líquido / líquido + concentrado inicial (com ou sem forragem) / desmamada (só sólido) / vitelo | — | 221, 235–236 |
| IMS de líquido (leite/sucedâneo) | IMSAL | kg MS/d | Entra em PMF (Eq. 10-12) e na EM líquida | dados de desenvolvimento: 0.11–1.99 kg/d (temperado), 0.21–2.07 (subtropical) | 220–221, 229 |
| IMS de sólido (concentrado inicial + forragem) | IMSAS | kg MS/d | Entra em PMF; dados: 0–2.85 kg/d (temperado), 0–1.93 (subtropical) | — | 220–221, 229 |
| EM diária da dieta líquida | EMiDL (MEiLD) | Mcal/d | IEM só do líquido; entra nas Eq. 10-1/10-2 | — | 221 |
| Composição do líquido | MS, PB, GB (AG), cinzas, lactose | % MS | Para Eq. 10-16; AG = GB × 0.945; Tabela 10-4 dá ingredientes | cinzas do sucedâneo 6–12% da MS | 232 |
| Tipo de proteína do sucedâneo | flag "proteína vegetal" | s/n | Se s, NMF = 34.4 g/kg de IMS (energia não muda) | — | 230 |
| Composição do concentrado inicial | ED/EM, PB, amido, FDN, GB… | — | ED conforme cap. 3 (com gordura 0.81, sem desconto de amido); EM = ED × 0.93 | EM típica do inicial 2.5–3.5 Mcal/kg MS (Tabela 10-16: 2.48–3.37) | 232–233, 246 |
| Opção de desconto de 10% na EM do concentrado | flag | s/n | Aplica 10% de desconto à EM do concentrado inicial de bezerra pré-desmame consumindo ≥ 1.5% do PC como sólidos de leite/sucedâneo | desligável no software | 233 |
| Temperatura ambiente efetiva | T | °C | Para termorregulação e escolha entre Eq. 10-1 e 10-2 | T > 35 °C → Eq. 10-2 (subtropical); caso contrário Eq. 10-1 | 221, 224–225 |
| Temperatura crítica inferior/superior | TCI/TCS | °C | Ver seção 6 e ⚠7 | ver abaixo | 224–225 |
| Dias de vida (para regras de colostro) | — | h/d | colostro ≤ 1 h, 10–12 h; fechamento ~24 h | — | 253–254 |

## 3. Saídas

| Variável | Símbolo | Unidade | Definição | Faixa/valores típicos | Pág. |
|---|---|---|---|---|---|
| IMS de concentrado inicial prevista | — | g/d | Eq. 10-1 (clima temperado) ou 10-2 (T > 35 °C) | RMSEP 262 g/d (10-1), 222 g/d (10-2) | 221 |
| IMS total de referência | — | % do PC | média pré-desmame (< 8 sem): 1.93 ± 0.33% (1.17–3.06); desmamadas (> 8 sem): 3.06 ± 0.31% (2.16–4.45) | — | 220 |
| PCV e GPV | PCV, GPV | kg, kg/d | PCV = PC × (PCV/PC); GPV = GMD × (GPV/GMD) (Tabela 10-1) | 0.85–0.96 | 220, 224 |
| EM dos alimentos líquidos | EM | Mcal/kg MS | Eq. 10-16 × 0.91 (sucedâneo) ou × 0.93 (leite integral) | MR 4.6–4.9; leite 5.37 | 232 |
| EM do concentrado inicial | EM | Mcal/kg MS | ED (cap. 3, gordura 0.81) × 0.93; opcional −10% | 2.5–3.5 | 232–233 |
| ELm, EMm | ELm, EMm | Mcal/d | ELm = coef × PCV^0.75; EMm = ELm/k_m | Tabelas 10-1, 10-7 a 10-11 | 224 |
| Acréscimo de mantença por temperatura | — | kcal/d | 2.01 kcal/kg PCV^0.75 por °C fora da zona termoneutra | Tabela 10-2 | 224–225 |
| Energia retida | ER | Mcal/d | Eq. 10-5 | média do banco 1.456 Mcal/d | 226–227 |
| Eficiências k_m, k_g | — | — | Leite: k_m 0.72 (0.719), k_g 0.55; sólido: Eq. 10-4 e 10-6; dieta mista = média ponderada pela contribuição à EM | k_g sólido 0.378–0.441 | 222, 227, 235 |
| Exigência de EM total | EM | Mcal/d | EMm (+ termorregulação) + ER/k_g | Tabelas 10-7 a 10-11 | 236–240 |
| IMS necessária p/ atender EM | — | kg/d | EM/densidade de EM da dieta (não é ingestão voluntária) | Tabelas | 235 |
| Composição do ganho | fração gordura, proteína | kg/kg GPV | Eq. 10-7, 10-8 | 0.132 e 0.181 na ER média | 227 |
| Exigência de PM e PB | PM, PB | g/d | Eq. 10-10 a 10-15 + conversões PB→PM | Tabelas 10-7 a 10-11 | 229–230, 236–240 |
| GPV/GMD permitido por EM e por PM | — | kg/d | usa-se o mais limitante (Eq. 10-17; ajuste Eq. 10-18 só na validação) | — | 234 |
| IA de macrominerais | Ca, P, Mg, K, Na, Cl | g/d | Eq. 10-19 a 10-23 | Tabela 10-13 | 238–239 |
| IA de microminerais | Cu, Fe, Mn, Zn | mg/d | Eq. 10-24 a 10-27 | — | 239 |
| IA de I, Se, vitaminas | I, Se, A, D, E | mg/kg MS; UI/kg PC | 0.8 mg I/kg MS; 0.3 mg Se/kg MS; A 110, D 32, E 2.0 UI/kg PC | Tabela 10-15 | 241–243 |
| Concentrações recomendadas no sucedâneo/concentrado | — | % ou mg/kg MS | Tabela 10-13 | — | 241 |

---

## 4. Equações

### 4.1 IMS do concentrado inicial

**Eq. 10-1 (clima temperado, T ≤ 35 °C)** [p.221] ⚠1
```
IMS_conc_ini (g/d) = -652.525 + (PC * 14.734) + (EMiDL * 18.896) + (Tpconc * 73.303)
                     + (Tpconc^2 * 13.496) - (29.614 * Tpconc * EMiDL)
```
(corrigido pela imagem: a ordem dos termos é essa; **o operador entre `(Tpconc*73.303)` e `(Tpconc^2*13.496)` não aparece na impressão** — quebra de linha engoliu o sinal. Teste numérico: com "+" a equação dá 600 g/d em 6 sem (PC 60 kg, EMiDL 3.5), 1.9 kg/d em 8 sem desmamada e 2.76 kg/d em 10 sem/90 kg (= 3.06% do PC, batendo com o valor médio de desmamadas, p.220); com "−" dá valores negativos (−662 g/d). Logo "+" é o único consistente; mantido como inferência, não como texto do livro.)
- PC (kg); EMiDL (Mcal/d, EM só do líquido); Tpconc (semanas). Idade é proxy de Tpconc (assume concentrado oferecido já na 1ª semana).
- Dados: 26,952 observações de 1,356 bezerras, 28 estudos (GA 168, IL 1,925, MN 6,052, OH 16,457, Holanda 2,350). Validação externa: 8,891 obs., 9 estudos (IA 6,332; NH 1,519; NY 892; VA 148). RMSEP 262 g/d, CCC 0.71; R² médio validação cruzada K-fold (n = 500, k = 10): 0.66 ± 0.01 (desenvolvimento) e 0.67 ± 0.02 (avaliação). Modelos mistos lineares (estudo aleatório), seleção por AIC. [p.220–221]
- Não informado: tratamento de valores negativos (para semanas 1–3 a equação dá ≈ 0 ou < 0; o livro não diz se trunca em 0).

**Eq. 10-2 (clima subtropical, T > 35 °C)** [p.221]
```
IMS_conc_ini (g/d) = 600.053 * (1 + 14863.651 * exp(-1.553 * Tpconc))^(-1) + (9.951 * PC) - (130.434 * EMiDL)
```
- Mesmas unidades. Dados: 3,491 obs. de 853 bezerras, 15 estudos (FL 1,127; GA 179; Brasil 2,185); avaliação: 479 obs., 5 estudos (GA 96; Brasil 383). RMSEP 222 g/d, CCC 0.78. Regra de seleção: "quando os usuários inserem uma temperatura > 35 °C usa-se a 10-2; caso contrário a 10-1" [p.221–222] (verificado na imagem).
- Observação: ingestão de leite/sucedâneo nos dados subtropicais 0.21–2.07 kg/d MS; concentrado 0–1.93 kg/d.

### 4.2 Mantença e eficiências

**Eq. 10-3 (produção de calor, bezerras líquido ou líquido + sólido, raças pequenas e grandes)** [p.222] (verificado)
```
PCa = 0.077 * exp(3.3426 * IEM)      [PCa e IEM em Mcal/PCV^0.75 por dia]
(RMSEP = 0.011, CCC = 0.950; sem viés de média ou de inclinação)
```
- PCa = produção de calor; IEM = ingestão de EM; ambos em Mcal/(kg PCV^0.75)/d. O intercepto **0.077 = ELm** (Mcal/kg PCV^0.75; "ELm = a × e^(b×IEM) quando IEM = 0"). n = 235 observações após remoção de tratamentos de Bartlett et al. (2006) com deficiência de proteína e outliers; 255 bezerras de 7 estudos de abate comparativo (6 Holandesa, 1 Jersey; 2 estudos com sólido). Estudo como efeito aleatório (nlme). Figura 10-1.
- Método: EMm = ponto onde IEM = PCa (sem retenção). **O livro fixa EMm = 0.107 Mcal/kg PCV^0.75 (= 0.101 Mcal/kg PC^0.75)** e k_m = ELm/EMm = 0.719 ⚠4 (o ponto fixo calculado da Eq. 10-3 como impressa é ≈ 0.112; as tabelas do livro reproduzem-se com 0.107).
- Expoente 0.75 mantido (0.85 de Labussière et al. 2008b melhoraria o ajuste em vitelos 73–221 kg, mas aumentou a variação no banco atual).
- Atividade: 10% da ELm é considerado excessivo; Labussière: 3.5–8% da IEM.

**Eq. 10-4 (ELm do alimento sólido; Galyean et al., 2016)** [p.224] (verificado)
```
ELm (Mcal/kg MS) = (1.1104 * EM) - (0.0946 * EM^2) + (0.0065 * EM^3) - 0.7783
```
- EM em Mcal/kg MS. k_m do sólido = ELm/EM. Para EM do concentrado inicial 2.5–3.5 Mcal/kg MS a eficiência varia de 0.60 a 0.64 (conferido: 0.603 a 0.637). Eficiência geral da dieta = média ponderada da EM de líquido e sólido (como NRC 2001).
- Observação: "onde ME é expressa em Mcal/kg MS" (ME = EM).

**Temperatura (termorregulação)** [p.224–226] — parâmetro, não equação numerada:
```
Produção extra de calor = 2.01 kcal / kg PCV^0.75 / d  por °C abaixo da TCI  (Schrama et al., 1992a)
                        = mesma proporção por °C acima da TCS (suposição do comitê, sem dados)
Tratado como EL com 100% de eficiência da EM (i.e., ΔEMm = ΔELm).
```
(Tabela 10-2 foi calculada para PCV = 45 kg.) Limiares na seção 6 e ⚠7.

### 4.3 Crescimento: energia retida e eficiências

**Eq. 10-5 (ER; escolhida entre 3 candidatas)** [p.226] (corrigido pela imagem: expoentes 1.100 e 0.205)
```
ER (Mcal/d) = GPV^1.100 * PCV^0.205         [GPV em kg/d; PCV em kg]
(viés médio 0.004; viés de inclinação −0.012; RMSE 0.186; CCC 0.966)
```
- Candidatas: (1) a×GPV^b×PCV^c (NRC 2001; descartada, VIF > 964); (2) mesma com PCV^0.75; (3) sem o coeficiente a (escolhida, menor EMQP). 255 bezerras.
- Verificação: EM = EMm + ER/0.55 reproduz a Tabela 10-7 (seção 7).

**k_g do leite/sucedâneo** [p.226–227]: regressão ER = a + b×IEM (Mcal/PCV^0.75/d) deu b = 0.46; o comitê adotou **k_g = 0.55** (média do banco atual e de estimativas da literatura; INRA 2019 = 0.55; Labussière et al. 2007 = 0.64; NRC 2001 = 0.69). Silva et al. (2017, Holandês × Gir): ER/EM aparente 0.574 (leite integral) e 0.516 (leite + inicial); k_g do inicial 0.393.

**Eq. 10-6 (ELg do alimento sólido; Galyean et al. 2016 modificada)** [p.227] (verificado)
```
ELg (Mcal/kg MS) = (1.1376 * EM) - (0.1198 * EM^2) + (0.0076 * EM^3) - 1.2979
```
- EM em Mcal/kg MS; k_g do sólido = ELg/EM. Texto: "ao longo de EM 2.5 a 3.5, ER/EM varia de 0.378 a 0.441" — conferido: 0.441 em 3.5; em 2.5 dá 0.366 (0.378 corresponde a EM = 2.6) ⚠19. Exemplo: EM 3.1 → k_g = 0.4206, k_m = 0.6285.

**Eq. 10-7 e 10-8 (composição do GPV; 6 estudos Holandesa; método NASEM 2016)** [p.227] (verificado)
```
Proporção de gordura no GPV   = 0.0786 + 0.0370 * ER      [ER em Mcal/d]
Proporção de proteína no GPV  = 0.1910 - 0.0071 * ER      [ER em Mcal/d]
```
- Na ER média do banco (1.456 Mcal/d): gordura 0.132 e proteína 0.181 (conferido: 0.1325 e 0.1807).

**Eq. 10-9 (Roy, 1980; literatura, apenas discussão)** [p.228]
```
Ganho de PC (kg/d) = 0.175 + 3.92 * ganho de proteína (kg/d) + 0.618 * ganho de gordura (kg/d)
```
- Proteína retém água ~4:1. Não é usada no cálculo das tabelas.

**Eq. 10-17 (GPV a partir de ER; usada p/ GMD permitido pela EM)** [p.234] ⚠3
```
Ganho de PCV (kg/d) = ER (Mcal/d) / (PCV^0.205, kg)^(1/1.1)
```
(transcrição literal da imagem; o texto diz "reorganização da Equação 10-6" mas refere-se à 10-5). **Atenção:** a inversão algébrica exata da Eq. 10-5 seria `GPV = (ER / PCV^0.205)^(1/1.1)`; a forma impressa é diferente (linear em ER). Teste: as colunas "Desmamada" da Tabela 10-17 são reproduzidas **exatamente pela forma impressa** (−0.164/0.144/0.452/0.760 vs tabela −0.16/0.14/0.45/0.76) e **não** pela inversão exata (−0.181/0.160/0.454/0.728). Recomendação: implementar a forma impressa para prever GPV a partir da EM disponível, e a Eq. 10-5 direta para ER a partir de GPV.

**Eq. 10-18 (calibração com a literatura)** [p.234] (verificado)
```
GMD observado (kg/d) = 0.073 + 0.867 * GMDe (kg/d)       [GMDe = GMD estimado pelo modelo]
```
- Média estimada 0.679 vs observada 0.689 kg/d; RMSE 0.110 kg/d (15.9% da média); CCC 0.95. Regressão com estudo como efeito aleatório. O texto não diz se o software aplica essa calibração ao GMD previsto ⚠21 (parece ser só avaliação).

### 4.4 Cálculo da EM dos alimentos

**Eq. 10-16 (energia bruta do alimento líquido)** [p.232] ⚠2
```
EB (Mcal/kg MS) = ((AG * 9.4) + (Proteína * 5.65) + (100 - Proteína - AG - Cinzas * 4)) / 100
```
(transcrição literal da imagem; valores em % da MS.) A leitura literal "Cinzas × 4" subtraído dá resultados absurdos; a leitura coerente é `(100 − Proteína − AG − Cinzas) × 4` (restante = lactose/carboidratos a 4 Mcal/kg). Teste com leite integral (MS: GB 30.8 → AG = 0.945×30.8 = 29.1; PB 25.4; cinzas 6.3): EB = 5.74; × 0.93 = 5.34 vs Tabela 10-4 = 5.37 (OK). Leitura literal: 4.37 (errado).
- AG = GB × 0.945 (Paul e Southgate, 1978). Outros compostos orgânicos (amido hidrolisado, dextrinas, glicose, glicerol; em geral < 10% da MS) têm calor de combustão = lactose (4 Mcal/kg). Cinzas (6–12% da MS do sucedâneo) devem ser analisadas. Rótulos estão em matéria natural/seca ao ar (MS do sucedâneo = 95–97%): converter.

**Fatores EB → EM (texto)** [p.232–233]:
```
EM_sucedâneo      = EB * 0.91          (0.91 = digestibilidade média 0.95 × metabolizabilidade da ED 0.96)
EM_leite_integral = EB * 0.93          (digestibilidade do leite 0.97; NRC 2001)
ED_sólido  = cap. 3, com coeficiente de digestibilidade da gordura = 0.81 (em vez de 0.74)
             e SEM desconto de amido (IMS fixada em 3.5% do PC; amido da dieta = 25% nas equações)
EM_sólido  = ED * 0.93                 (eficiência ED→EM 0.91–0.95 em bezerras; Pattanaik et al., 2003)
Opcional: EM do concentrado de bezerra pré-desmame com ≥ 1.5% do PC como sólidos de leite/sucedâneo: × 0.90
```
(corrigido pela imagem: a condição do desconto é "≥ 1.5% do PC", OCR dizia ">"). O desconto reflete rúmen imaturo (digestibilidade da FDN menor).

### 4.5 Proteína

**Eq. 10-10 (PB de descamação; Swanson 1997)** [p.229] (corrigido pela imagem: expoente 0.60)
```
PB_descamação (g/d) = 0.22 * PC^0.60            [PC em kg]
```

**Eq. 10-11 (PB endógena urinária)** [p.229] (corrigido pela imagem: expoente 0.50)
```
PBEU (g/d) = 2.75 * PC^0.50                      [PC em kg]
```

**Eq. 10-12 (PB metabólica fecal; igual à edição anterior)** [p.229]
```
PMF (g/d) = (11.9 * IMSAL, kg/d) + (20.6 * IMSAS, kg/d)
```
- IMSAL = IMS de alimentos líquidos; IMSAS = IMS de alimentos sólidos. Se sucedâneo com proteína vegetal: NMF → 34.4 g/kg de IMS [p.230] (não alterando a energia).

**Eq. 10-13 (PM de mantença)** [p.229]
```
PM_mantença (g/d) = PBEU + ((PB_descamação + PMF) / 0.68)
```
- PL de mantença = PBEU + PMF + descamação; eficiência PL→PM = 0.68 para descamação e PMF e 1.0 para PBEU (como nas outras categorias; cap. 6).

**Eq. 10-14 (PL de ganho)** [p.229] (verificado)
```
PLg (g/d) = (166.2 * GPV) + (6.1276 * (ER / GPV))        [GPV em kg/d; ER em Mcal/d]
```
- 255 bezerras, 7 estudos. NRC 2001 usava 30 g N/kg de ganho de PC (constante). Verificação: ER/GPV ≈ 1.6 Mcal/kg → PLg ≈ 176 g/kg GPV (coerente com a fração proteica da Eq. 10-8).

**Eq. 10-15 (eficiência PM → PLg)** [p.230] (verificado) ⚠11
```
Eficiência da PM para ganho = 0.70 - 0.532 * (PC / PCMat)       [razão PC/PCMat, adimensional]
```
- Texto: cai de 0.70 ao nascimento (6% do PCMat) para 0.55 aos 200 kg (28% do PCMat). Conferido: 0.55 em 28%; em 6% a equação dá 0.668, não 0.70. Não usar em > 200 kg nem em novilhas ruminantes > 125 kg. PCMat: 700 (RG) e 530 (RP) (verificado na reprodução da Tabela 10-7).

**Exigência de PM total:** `PM = PM_mantença + PLg / Eficiência(Eq. 10-15)` (reprodução numérica da Tabela 10-7; o texto descreve os dois componentes mas não escreve a soma).

**Conversão PB → PM** [p.230–232]:
```
leite e ingredientes lácteos:                    PM/PB = 0.95   (digestibilidade verdadeira da proteína do leite em bezerras)
proteína dietética digerida pós-rúmen em bezerra com leite/sucedâneo + concentrado inicial: 0.75  (mantido do NRC 2001)
bezerra com rúmen funcional:                     0.70
mistura (líquido + inicial): média de 0.95 e 0.75 ponderada pela PB fornecida por cada fonte (aditivo)
```
Derivação do 0.70: assumindo fluxo de N ao abomaso ≈ N ingerido, PB microbiana = 80% proteína verdadeira, 80% digestível, e proteínas não degradáveis 0.80 digestíveis → ≈ 0.71; adotou-se 0.70 (ARC 1980 e NRC 2001 usavam 0.75). Dados insuficientes para PDR/PNDR.

### 4.6 Validação (equações de regressão de avaliação, ver seção 7)

Obs.= a + b × Est (kg/d): só leite (103 médias, 21 estudos): `0.070 + 0.903×GMDe` [p.235]; leite + inicial (219 médias, 64 estudos): `0.112 + 0.773×GMDe` [p.236]; desmamadas (79 médias, 23 estudos): `0.366 + 0.662×GMDe` [p.236]; geral (Eq. 10-18).

### 4.7 Minerais (IA, g/d ou mg/d da dieta total, bezerras pré-desmame)

Nas Eq. 10-19 a 10-23, PCV e GPV equivalem a **0.94 × PC e 0.91 × GMD** (kg) [p.239]. O denominador é o **coeficiente de retenção** determinado experimentalmente (Castro et al., 2019), que converte mineral retido em mineral da dieta; **não se usam CA para macrominerais em bezerras jovens**. Equações de Castro et al. (2019): 5 estudos de abate comparativo pré-desmame (4 com leite + inicial, 1 só sucedâneo; Holandesa e Holandesa × Gir; raça sem efeito) [p.237–238].

```
Eq. 10-19  Ca (g/d) = [0.0127*PCV + (14.4  * PCV^-0.139 * GPV)] / 0.73
Eq. 10-20  P  (g/d) = [0.0118*PCV + (5.85  * PCV^-0.027 * GPV)] / 0.65
Eq. 10-21  Mg (g/d) = [0.0035*PCV + (0.60  * PCV^-0.036 * GPV)] / 0.30
Eq. 10-22  K  (g/d) = [0.0203*PCV + (1.14  * PCV^-0.048 * GPV)] / 0.13
Eq. 10-23  Na (g/d) = [0.00637*PCV + (1.508 * PCV^-0.045 * GPV)] / 0.24
```
(corrigido pela imagem: expoentes negativos −0.139, −0.027, −0.036, −0.048, −0.045 — o OCR os havia perdido.) PCV em kg, GPV em kg/d. Cl: **0.8 × Na** (relação Cl/Na de vacas em lactação; não há dados para bezerras) [p.239].
Verificação interna: bezerra de 50 kg, GMD 0.6 kg/d (PCV 47, GPV 0.546) → Ca 7.1 g/d, P 5.3 g/d; com IMS ≈ 0.88 kg/d dá 0.80% Ca e 0.60% P, idêntico à Tabela 10-13 (sucedâneo).

```
Eq. 10-24  Cu (mg/d) = (0.0145*PC + 2.5 * GMD) / 0.5
Eq. 10-25  Fe (mg/d) = (34 * GMD) / 0.25
Eq. 10-26  Mn (mg/d) = [(0.0026*PC + 0.7 * GMD)] / 0.01
Eq. 10-27  Zn (mg/d) = (2 * IMS + 24 * GMD) / 0.25
```
(verificado na imagem; PC em kg, GMD em kg/d, IMS em kg/d; denominadores = CA específicos de bezerra.) ⚠12: o denominador do Zn é 0.25 na equação, mas a Tabela 10-12 lista CA do Zn = 0.20 para sucedâneo+concentrado inicial. Usa-se 2.5 mg Cu/kg GMD (novilhas: 2.0) por maior Cu em órgãos; 24 mg Zn/kg GMD (novilhas: 30). Sem IA de Co no sucedâneo (rúmen não funcional → sem vitamina B12). I e Se: IA = 0.8 mg I/kg MS (IA de crianças) e 0.3 mg Se/kg MS, sem CA [p.241–242].

### 4.8 Colostro (fórmulas)

```
IgG sérica (g/L) = Ingestão de IgG (g) * EAAbs / VP          [EAAbs: fração; VP = volume plasmático, L]
EAAbs = IgG sérica (g/L) * VP (L) / Ingestão de IgG (g)
VP ≈ 8.9% do PC (bezerras Holandesas e Jersey recém-nascidas)
IgG do colostro (g/L) = Intercepto + Curva * BRIX (%)        [Tabela 10-18]
```
[p.253–254] (Quigley e Drewry, 1998; verificado na imagem; o OCR havia inserido "9%" na definição de EAAbs, que não existe na imagem). EAAbs típica: < 10% a ~40% (limite ~50%).

---

## 5. Parâmetros e tabelas

### Tabela 10-1 — Relação PCV/PC e exigências energéticas de leite ou sucedâneo [p.224] (conferida na imagem)

| Item | Apenas leite/sucedâneo: Holandesa/Raças Grandes | Apenas leite/sucedâneo: Jersey/Raças Pequenas | Leite/sucedâneo + sólido: Holandesa/RG | Leite/sucedâneo + sólido: Jersey/RP | Desmamadas, só sólido: Holandesa/RG | Desmamadas, só sólido: Jersey/RP |
|---|---|---|---|---|---|---|
| PCV/PC | 0.94 | 0.94 | 0.93 | 0.93 | 0.85 | 0.85 |
| GPV/GMD | 0.94 | 0.94 | 0.91 | 0.91 | 0.85 | 0.85 |
| ELm, kcal/kg PCV^0.75 | 76.9 | 76.9 | 76.9 | 76.9 | 97.0 | 97.0 |
| ELm, kcal/kg PC^0.75 | 72.3 | 72.3 | 72.3 | 72.3 | 82.5 | 82.5 |
| EMm, kcal/kg PCV^0.75 | 107.0 | 107.0 | 113.8 | 113.8 | Var^b | Var^b |
| EMm, kcal/kg PC^0.75 | 100.0 | 100.0 | 105.8 | 105.8 | Var | Var |
| Eficiência da EM para ELm, k_m | 0.72 | 0.72 | 0.69 | 0.69 | Var^b | Var^b |

Notas: ^a expresso como função do PCV metabólico ou PC vivo e k_m. ^b determinado como eficiência de uso do alimento sólido (densidade de EM pela Eq. 10-4). Texto: PCV/PC varia de 0.85 a 0.96 [p.220]; **vitelos pesados (> 125 kg): PCV = 0.93 × PC** (Gerrits et al. 1996) [p.220]; durante a transição do desmame PCV/PC fica entre 0.93 e 0.85. ⚠5 ⚠6: (i) para "leite + sólido" a EMm 113.8 com k 0.69 implica ELm ≈ 78.5 (= 76.9 × 1.02, os "~2% maiores" do texto, p.223), embora a linha ELm mostre 76.9; (ii) as linhas por PC^0.75 foram obtidas multiplicando as de PCV^0.75 pela razão PCV/PC (linear), e não por (PCV/PC)^0.75; para cálculo use sempre as linhas por PCV^0.75 (as que reproduzem as Tabelas 10-7 a 10-11); (iii) GPV/GMD = 0.94 (só leite) vs 0.91 usado nos vitelos (Tabela 10-11, p.236), nas Eq. 10-19–23 (p.239) e nos exemplos do texto (p.235: ER/GMD 1.62 e 2.11 Mcal/kg só reproduzem-se com 0.91); (iv) o texto diz que na transição GPV varia "de 0.5 a 0.6 do GMD" [p.220], contra 0.85 da tabela.

Outras constantes de mantença citadas [p.222–223]: ELm NRC 2001 = 0.086 Mcal/kg PC^0.75; ELm desmamadas até 125 kg = 0.097 Mcal/kg PCV^0.75 (0.0825/kg PC^0.75), EMm correspondente "0.138 Mcal/kg PCV^0.75 (0.117/kg PC^0.75)" ⚠20 (as Tabelas 10-10 usam k_m da Eq. 10-4, ≈ 0.626 em EM 3.0 → EMm ≈ 0.155; não 0.138); Jersey: ELm +6.6% e EMm +15.1% (n.s.), mantença de Jersey pode ser até 20% maior que Holandesa, mas o comitê manteve iguais; NASEM 2016 (corte): ELm leiteiras 0.095/PC^0.75 = 0.112/PCV^0.75; Brody (1945): área superficial = 0.14 × PC^0.57 (41–617 kg). Mantença nas bezerras alimentadas com sólido foi ~2% maior que só leite (n.s.).

### Tabela 10-2 — Efeito da temperatura ambiental na exigência energética de bezerras [p.225] (conferida na imagem; corrigida a última linha)

Calculada para bezerra de 45 kg de PCV; produção extra de calor = 2.01 kcal/kg PCV^0.75/d por °C (ver 4.2). (b) Nascimento até 3 sem: EMm 107 kcal/kg PCV^0.75 (TCI na faixa 15–25 °C; cálculo com TCI 15 °C e TCS 25 °C). (c) > 3 sem: EMm 113.8 (cálculo com TCI 5 °C e TCS 25 °C).

| °F | °C | Acréscimo ELm (kcal/d) ≤ 3 sem | Acréscimo ELm > 3 sem | EM de mantença (kcal/d) ≤ 3 sem | EM de mantença > 3 sem | Acréscimo na EM de mantença (%) ≤ 3 sem | > 3 sem |
|---|---|---|---|---|---|---|---|
| 113 | 45 | 698 | 698 | 2,557 | 2,675 | 38 | 40 |
| 104 | 40 | 524 | 524 | 2,383 | 2,501 | 28 | 30 |
| 95 | 35 | 349 | 349 | 2,208 | 2,326 | 19 | 20 |
| 86 | 30 | 175 | 175 | 2,034 | 2,152 | 9 | 10 |
| 77 | 25 | 0 | 0 | 1,859 | 1,977 | 0 | 0 |
| 68 | 20 | 0 | 0 | 1,859 | 1,977 | 0 | 0 |
| 59 | 15 | 175 | 0 | 2,034 | 1,977 | 9 | 0 |
| 50 | 10 | 349 | 0 | 2,208 | 1,977 | 19 | 0 |
| 41 | 5 | 524 | 175 | 2,383 | 2,152 | 28 | 9 |
| 32 | 0 | 698 | 349 | 2,557 | 2,326 | 38 | 18 |
| 23 | −5 | 873 | 524 | 2,732 | 2,501 | 47 | 26 |
| 14 | −10 | 1,048 | 698 | 2,907 | 2,675 | 56 | 35 |
| 5 | −15 | 1,222 | 873 | 3,081 | 2,850 | 66 | 44 |
| −4 | −20 | 1,397 | 1,048 | 3,256 | 3,025 | 75 | 53 |
| −13 | −25 | 1,572 | 1,222 | 3,431 | 3,199 | 85 | 62 |
| −22 | −30 | 1,746 | 1,397 | 3,605 | 3,374 | 94 | 71 |

⚠7 Os acréscimos (175 kcal por 5 °C = 2.01 × 45^0.75... = 34.9 kcal/°C × 5) implicam, **na tabela**, TCI = 20 °C (≤ 3 sem) e 10 °C (> 3 sem) e TCS = 25 °C, ao passo que a nota de rodapé diz TCI 15/5 °C e o texto adota TCS = **26 °C** (bezerras ofegam a 26 °C; Spain e Spiers 1996) [p.225]. O exemplo do texto (TCI 15 °C, 0 °C ambiente → +38% p/ < 3 sem) só é reproduzido com ΔT = 20 °C (698 kcal). Valores EM de mantença sem estresse: 1,859 (= 107.0 × 17.4) e 1,977 (≈ 113.8 × 17.4) kcal/d.

### Tabela 10-3 — Estudos usados para relacionar IMS ao fluxo de N microbiano [p.231] (conferida na imagem)

| Referência | N | Forragem (%) | Idade (sem) | IMS (kg/d) | N microbiano (% do N total) |
|---|---|---|---|---|---|
| Lallès e Poncet, 1990 | 6 | 20 | 9–20 | 0.8–2.4 | 60–68 |
| Leibholz, 1975 | 8 | 15 | 6–13 | 0.6–2.5 | 32–74 |
| Leibholz, 1978 | 5 | 15 | 6–10 | 0.8–1.8 | 28–70 |
| Obitsu et al., 1995 | 8 | 30–40 | 10–15 | 1.5–2.4 | 48–64 |
| Quigley et al., 1985 | 39 | 0/ad libitum^b | 2–11 | 0.1–3.1 | 6–83 |

^a fluxo de N microbiano como % do fluxo total de N no abomaso/duodeno. ^b metade das bezerras tinha feno longo de gramínea ad libitum. Total 66 observações (soma = 66). Regressão linear segmentada (Robbins et al. 2006; St-Pierre 2001): **ponto de quebra 1.32 kg/d de IMS (EP 0.118), platô 60.6% (EP 1.43) do N total como N microbiano; R² ajustado 0.70** (Figura 10-2; texto diz "1.3 kg/d"). Interceptação em IMS = 0 ≈ 15% (lido do gráfico; não informado no texto). Quigley e Schwab (1988): r = 0.92 entre ingestão de inicial e % de N microbiano no abomaso (2–11 sem). ⚠17: o texto fala "quatro estudos", a tabela lista cinco.

### Tabela 10-4 — Composição de ingredientes de sucedâneos [p.232] (conferida na imagem; OCR havia perdido colunas)

| Alimento/ingrediente | MS (%) | ED (Mcal/kg MS) | EM (Mcal/kg MS) | Cinzas (% MS) | PB (% MS) | GB (% MS) | Lactose (% MS) |
|---|---|---|---|---|---|---|---|
| Leite integral | 12.5 | 5.59 | 5.37 | 6.3 | 25.4 | 30.8 | 39.2 |
| Leite desnatado, fresco | 10 | 4.19 | 4.02 | 6.9 | 35.5 | 0.3 | 56 |
| Leite desnatado, pó | 94 | 4.25 | 4.08 | 6.9 | 37.4 | 1.0 | 54 |
| Soro do leite, desidratado | 93 | 3.80 | 3.65 | 8.1 | 13.5 | 1.0 | 76 |
| Proteína concentrada do soro do leite | 93 | 4.35 | 4.17 | 6.0 | 37.1 | 2.2 | 54 |
| Soro do leite, fresco | 7 | 3.78 | 3.62 | 8.7 | 14.2 | 0.7 | 76 |
| Soro do leite, sem lactose | 93 | 3.54 | 3.40 | 16.5 | 23.0 | 1.5 | 55 |
| Soro do leite permeado | 98 | 3.55 | 3.41 | 9.0 | 3.7 | 0 | 87 |
| Caseína | 91 | 5.29 | 5.08 | 4.0 | 92.7 | 0.7 | — |
| Caseinato, sódio | 96 | — | — | 2.5 | 85 | 0.5 | — |
| Proteína concentrada de soja | 96 | — | — | 7.0 | 67 | 0.3 | — |
| Proteína isolada de soja | 95 | — | — | 4.5 | 86 | 0.5 | — |
| Farinha de soja | 96 | — | — | 6.3 | 53 | 0.2 | — |
| Proteína modificada de trigo | 96 | — | — | 3.0 | 82 | 2.0 | — |
| Proteína plasmática suína | 97 | — | — | não informado | 67 | 0.5 | — |
| Proteína plasmática bovina | 97 | — | — | não informado | 68 | 0.5 | — |

(Células em branco no livro: sem ED/EM p/ proteínas vegetais e plasma; sem cinzas p/ plasma.) ⚠24: ED/EM tabelados não se reproduzem exatamente por Eq. 10-16 × 0.91/0.93 (erros 2–4%, p.ex. leite desnatado em pó calcula EM ≈ 4.00 vs 4.08 tabelado); usar os valores tabelados quando o ingrediente estiver na lista.

### Tabela 10-5 — Digestibilidade da GB em bezerras desmamadas (7 estudos, 37 médias de tratamento) [p.233] (conferida na imagem)

| Item | Média | Variação | DP |
|---|---|---|---|
| PC, kg | 98.7 | 63–135 | 24.6 |
| Idade, dias | 76 | 51–112 | 24.8 |
| IMS, kg/d | 2.5 | 1.3–4.3 | 0.76 |
| Gordura da dieta, % da MS | 4.0 | 2.2–5.1 | 0.69 |
| Digestibilidade da gordura | 0.81 | 0.70–0.91 | 0.05 |

Fontes: Chapman 2016; Dennis 2018; Hill 2010, 2016b, 2016c; Hu 2019; Stewart e Schingoethe 1984. Origem do coeficiente 0.81.

### Tabela 10-6 — Estudos usados na validação [p.233]
Lista de referências (não numérica): só leite/sucedâneo (20 itens listados), leite/sucedâneo + inicial com ou sem forragem (~62 itens), desmamadas (~22 itens). Sem dados de cálculo. Contagem do texto: 21, 64 e 23 estudos respectivamente; 416 médias de tratamento de 94 estudos (p.233) vs 397 médias na legenda da Figura 10-3 (p.234) ⚠18.

### Tabela 10-7 — Exigências diárias de energia e proteína, bezerras de reposição em aleitamento só com leite/sucedâneo, 25–50 kg [p.236] (conferida na imagem; **reconstruída numericamente: EM, IMS e ELm batem; PM/PB do modelo ficam 0.3–1.6 g/d acima**)

RP = raça pequena (Jersey, PCMat 530 kg); RG = raça grande (Holandesa, PCMat 700 kg). IMS: MS necessária p/ atingir a EM com sucedâneo de **4.7 Mcal EM/kg MS (RP) ou 4.6 (RG)**. PB: todas as proteínas do leite, **PM/PB = 0.95**. ⚠8: a coluna rotulada "EMm (Mcal/d)" contém na verdade **ELm** (0.82 = 0.0769 × (0.94×25)^0.75), embora o cabeçalho diga EMm; nas Tabelas 10-8 a 10-11 a coluna é corretamente "ELm".

| PC (kg) | Raça | GMD (g/d) | IMS (kg/d) | EM (Mcal/d) | EMm [= ELm] (Mcal/d) | PM (g/d) | PB (g/d) | PB (% da IMS) |
|---|---|---|---|---|---|---|---|---|
| 25 | RP | 200 | 0.36 | 1.69 | 0.82 | 83 | 87 | 24.2 |
| 25 | RP | 400 | 0.49 | 2.33 | 0.82 | 132 | 139 | 28.2 |
| 30 | RP | 200 | 0.40 | 1.88 | 0.94 | 86 | 91 | 22.7 |
| 30 | RP | 400 | 0.54 | 2.54 | 0.94 | 136 | 143 | 26.6 |
| 30 | RP | 600 | 0.69 | 3.23 | 0.94 | 186 | 196 | 28.5 |
| 35 | RP | 200 | 0.44 | 2.06 | 1.06 | 89 | 94 | 21.4 |
| 35 | RP | 400 | 0.58 | 2.74 | 1.06 | 140 | 147 | 25.2 |
| 35 | RP | 600 | 0.73 | 3.45 | 1.06 | 190 | 200 | 27.2 |
| 35 | RP | 800 | 0.89 | 4.19 | 1.06 | 240 | 253 | 28.3 |
| 40 | RG | 200 | 0.48 | 2.23 | 1.17 | 91 | 96 | 19.8 |
| 40 | RG | 400 | 0.64 | 2.93 | 1.17 | 142 | 149 | 23.4 |
| 40 | RG | 600 | 0.80 | 3.66 | 1.17 | 192 | 202 | 25.4 |
| 40 | RG | 800 | 0.96 | 4.42 | 1.17 | 242 | 254 | 26.5 |
| 45 | RG | 200 | 0.52 | 2.40 | 1.28 | 94 | 99 | 19.0 |
| 45 | RG | 400 | 0.68 | 3.11 | 1.28 | 145 | 152 | 22.5 |
| 45 | RG | 600 | 0.84 | 3.86 | 1.28 | 195 | 205 | 24.5 |
| 45 | RG | 800 | 1.02 | 4.64 | 1.28 | 245 | 258 | 25.6 |
| 50 | RG | 200 | 0.56 | 2.56 | 1.38 | 97 | 102 | 18.3 |
| 50 | RG | 400 | 0.71 | 3.29 | 1.38 | 148 | 155 | 21.8 |
| 50 | RG | 600 | 0.88 | 4.05 | 1.38 | 198 | 209 | 23.7 |
| 50 | RG | 800 | 1.05 | 4.85 | 1.38 | 249 | 262 | 24.9 |
| 50 | RG | 1,000 | 1.23 | 5.66 | 1.38 | 299 | 315 | 25.6 |

(Corrigido pela imagem vs OCR: PB% da linha 45 kg/400 g = 22.5 (OCR "2.5"); 30 kg RP 200 g PB% 22.7.) Exemplos do texto [p.235–236]: EM de bezerra RG 50 kg, 0.60 kg/d só líquido = 3.89 Mcal/d (a Tabela mostra 4.05 para 600 g/d com o rótulo "50 kg RG 600" — o texto cita 3.89; ⚠ divergência não resolvida entre texto e tabela), vs 4.18 e 4.40 com 80% e 40% da MS como sucedâneo (Tabela 10-8). Energia do ganho (Eq. 10-6, texto): 1.62 Mcal/kg p/ 40 kg ganhando 0.20 kg/d e 2.11 Mcal/kg p/ 75 kg ganhando 0.80 kg/d (NRC 2001: 1.56 e 2.57, ou seja −18%); EM 2.20 e 5.66 Mcal/d (NRC 2001: 2.04 e 5.52).

### Tabela 10-8 — Bezerras de raças pequenas, leite/sucedâneo + concentrado inicial, dois níveis de dieta [p.237] (conferida na imagem; **reconstrução aproximada: EM e IMS dentro de ±0.03–0.06**)

Dieta = proporção da MS como sucedâneo : concentrado inicial. ^d (80:20): sucedâneo 4.9 Mcal EM/kg MS + inicial 3.1; ^e (40:60): sucedâneo 4.7 + inicial 3.2 (conferido: IMS = EM/densidade média, 4.54 e 3.80 Mcal/kg). IMS = IMS total com a densidade média de EM necessária p/ atender a EM. PB = PB total da dieta assumindo sucedâneo só com proteína do leite. O texto chama a coluna ELm (Mcal/d).

| PC (kg) | GMD (g/d) | Dieta | IMS (kg/d) | EM (Mcal/d) | ELm (Mcal/d) | PM (g/d) | PB (g/d) | PB (% da IMS) |
|---|---|---|---|---|---|---|---|---|
| 30 | 200 | 80:20 | 0.43 | 1.96 | 0.93 | 86 | 94 | 21.8 |
| 30 | 200 | 40:60 | 0.53 | 2.02 | 0.93 | 91 | 109 | 20.6 |
| 30 | 400 | 80:20 | 0.58 | 2.62 | 0.93 | 135 | 148 | 25.6 |
| 30 | 400 | 40:60 | 0.72 | 2.75 | 0.93 | 142 | 170 | 23.6 |
| 30 | 600 | 80:20 | 0.73 | 3.32 | 0.93 | 184 | 202 | 27.6 |
| 30 | 600 | 40:60 | 0.93 | 3.52 | 0.93 | 192 | 232 | 25.0 |
| 40 | 200 | 80:20 | 0.51 | 2.33 | 1.16 | 92 | 101 | 19.7 |
| 40 | 200 | 40:60 | 0.63 | 2.39 | 1.16 | 98 | 118 | 18.7 |
| 40 | 400 | 80:20 | 0.67 | 3.03 | 1.16 | 142 | 156 | 23.4 |
| 40 | 400 | 40:60 | 0.83 | 3.16 | 1.16 | 150 | 180 | 21.7 |
| 40 | 600 | 80:20 | 0.83 | 3.77 | 1.16 | 192 | 211 | 25.4 |
| 40 | 600 | 40:60 | 1.05 | 3.98 | 1.16 | 202 | 243 | 23.2 |
| 40 | 800 | 80:20 | 1.00 | 4.54 | 1.16 | 241 | 265 | 26.5 |
| 40 | 800 | 40:60 | 1.27 | 4.82 | 1.16 | 253 | 305 | 24.0 |
| 50 | 400 | 80:20 | 0.75 | 3.41 | 1.37 | 149 | 163 | 21.8 |
| 50 | 400 | 40:60 | 0.93 | 3.54 | 1.37 | 157 | 189 | 20.3 |
| 50 | 600 | 80:20 | 0.92 | 4.18 | 1.37 | 199 | 219 | 23.8 |
| 50 | 600 | 40:60 | 1.16 | 4.40 | 1.37 | 210 | 253 | 21.9 |
| 50 | 800 | 80:20 | 1.10 | 4.98 | 1.37 | 252 | 274 | 25.0 |
| 50 | 800 | 40:60 | 1.39 | 5.28 | 1.37 | 263 | 317 | 22.8 |
| 50 | 1,000 | 80:20 | 1.28 | 5.80 | 1.37 | 300 | 330 | 25.8 |
| 50 | 1,000 | 40:60 | 1.63 | 6.19 | 1.37 | 316 | 380 | 23.4 |
| 60 | 400 | 80:20 | 0.83 | 3.75 | 1.57 | 155 | 170 | 20.6 |
| 60 | 400 | 40:60 | 1.03 | 3.90 | 1.57 | 164 | 198 | 19.3 |
| 60 | 600 | 80:20 | 1.00 | 4.56 | 1.57 | 206 | 227 | 22.6 |
| 60 | 600 | 40:60 | 1.26 | 4.79 | 1.57 | 218 | 263 | 20.9 |
| 60 | 800 | 80:20 | 1.19 | 5.39 | 1.57 | 258 | 283 | 23.8 |
| 60 | 800 | 40:60 | 1.50 | 5.70 | 1.57 | 272 | 328 | 21.8 |
| 60 | 1,000 | 80:20 | 1.38 | 6.25 | 1.57 | 309 | 340 | 24.7 |
| 60 | 1,000 | 40:60 | 1.75 | 6.64 | 1.57 | 326 | 392 | 22.4 |

(Uso da PCV/PC = 0.93 e GPV/GMD = 0.91 da Tabela 10-1 na coluna "leite + sólido": ELm 0.93 em 30 kg = 0.0769 × (0.93×30)^0.75.)

### Tabela 10-9 — Bezerras de raças grandes, leite/sucedâneo + concentrado inicial [p.238] (conferida na imagem; **células com erro de impressão marcadas ⚠9**)

^d (80:20): sucedâneo 4.6 Mcal EM/kg MS + inicial 3.2; ^e (40:60): sucedâneo 4.7 + inicial 3.2. Valores ⚠ abaixo = como impressos; a reconstrução do modelo (e a Tabela 10-8 equivalente) indica o valor esperado entre colchetes.

| PC (kg) | GMD (g/d) | Dieta | IMS (kg/d) | EM (Mcal/d) | ELm (Mcal/d) | PM (g/d) | PB (g/d) | PB (% da IMS) |
|---|---|---|---|---|---|---|---|---|
| 50 | 400 | 80:20 | 0.79 | 3.40 | 1.37 | 147 | 162 | 20.6 |
| 50 | 400 | 40:60 | 0.93 | 3.54 | 1.37 | 155 | 187 | 20.0 |
| 50 | 600 | 80:20 | 0.97 | 4.18 | 1.37 | 197 | 217 | 22.4 |
| 50 | 600 | 40:60 | 1.16 | 4.40 | 1.37 | **250 ⚠ [≈ 208–210]** | 250 | 21.6 |
| 50 | 800 | 80:20 | 1.15 | 4.98 | 1.37 | **271 ⚠ [≈ 248–252]** | 271 | 23.6 |
| 50 | 800 | 40:60 | 1.39 | 5.28 | 1.37 | **312 ⚠ [≈ 260–263]** | 312 | 22.5 |
| 60 | 400 | 80:20 | 0.87 | 3.75 | 1.57 | 153 | 168 | 19.4 |
| 60 | 400 | 40:60 | 1.03 | 3.90 | 1.57 | 162 | 195 | 19.0 |
| 60 | 600 | 80:20 | 1.05 | 4.55 | 1.57 | 204 | 224 | 21.2 |
| 60 | 600 | 40:60 | 1.26 | 4.79 | 1.57 | 214 | 258 | 20.5 |
| 60 | 800 | 80:20 | 1.25 | 5.38 | 1.57 | 254 | 279 | 22.4 |
| 60 | 800 | 40:60 | 1.50 | 5.70 | 1.57 | 267 | 322 | 21.4 |
| 60 | 1,000 | 80:20 | 1.44 | 6.24 | 1.57 | 305 | 335 | 23.2 |
| 60 | 1,000 | 40:60 | 1.75 | **6.24 ⚠ [≈ 6.64]** | 1.57 | 320 | 386 | 22.0 |
| 70 | 400 | 80:20 | 0.94 | 4.08 | 1.76 | 159 | 174 | 18.4 |
| 70 | 400 | 40:60 | 1.11 | 4.24 | 1.76 | 168 | 202 | 18.1 |
| 70 | 600 | 80:20 | 1.14 | 4.91 | 1.76 | 210 | 231 | 20.3 |
| 70 | 600 | 40:60 | 1.35 | 5.15 | 1.76 | 221 | 267 | 19.7 |
| 70 | 800 | 80:20 | 1.33 | 5.77 | 1.76 | 261 | 287 | 21.5 |
| 70 | 800 | 40:60 | 1.60 | 6.10 | 1.76 | **375 ⚠ [≈ 275]** | 332 | 20.6 |
| 70 | 1,000 | 80:20 | 1.54 | 6.65 | 1.76 | 312 | 343 | 22.3 |
| 70 | 1,000 | 40:60 | 1.86 | 7.07 | 1.76 | 328 | 396 | 21.3 |
| 80 | 600 | 80:20 | 1.21 | 5.25 | 1.90 | 216 | 237 | 20.5 |
| 80 | 600 | 40:60 | 1.45 | 5.50 | 1.90 | 228 | 275 | 19.0 |
| 80 | 800 | 80:20 | 1.42 | **6.03 ⚠ [≈ 6.13]** | 1.90 | 268 | 294 | 20.7 |
| 80 | 800 | 40:60 | 1.70 | 6.47 | 1.90 | 282 | 340 | 20.0 |
| 80 | 1,000 | 80:20 | 1.63 | 7.03 | 1.90 | 320 | 351 | 21.6 |
| 80 | 1,000 | 40:60 | 1.96 | 7.47 | 1.90 | 337 | 406 | 20.6 |

Justificativa dos ⚠9: (a) PM impressa = PB impressa em 3 linhas (250, 271, 312), impossível (PM < PB) e muito acima das mesmas condições da Tabela 10-8 (210, 252, 263); a PB e a PB% estão corretas (250/1.16 = 21.6%). (b) PM 375 > PB 332 em 70 kg/800/40:60. (c) EM 6.24 repetida (60 kg/1,000/40:60; IMS 1.75 × densidade 3.8 = 6.65). (d) EM 6.03 em 80 kg/800/80:20 (IMS 1.42 × 4.32 = 6.13; vizinhas 5.25 e 7.03).

### Tabela 10-10 — Bezerras desmamadas (RG ou RP), só alimento sólido [p.239] (conferida na imagem; **reconstruída: EM/IMS/ELm exatos; PM 0.3–1.5% abaixo/acima**)

^a assume concentrado inicial com **3.0 Mcal EM/kg MS**. PB = PM/0.70.

| PC (kg) | GMD (g/d) | IMS (kg/d) | EM (Mcal/d) | ELm (Mcal/d) | PM (g/d) | PB (g/d) | PB (% da IMS) |
|---|---|---|---|---|---|---|---|
| 55 | 400 | 1.47 | 4.39 | 1.73 | 174 | 249 | 17.0 |
| 55 | 600 | 1.77 | 5.30 | 1.73 | 228 | 325 | 18.4 |
| 55 | 800 | 2.08 | 6.25 | 1.73 | 282 | 402 | 19.3 |
| 65 | 400 | 1.61 | 4.82 | 1.97 | 183 | 262 | 16.3 |
| 65 | 600 | 1.92 | 5.76 | 1.97 | 238 | 340 | 17.7 |
| 65 | 800 | 2.25 | 6.74 | 1.97 | 292 | 418 | 18.6 |
| 75 | 400 | 1.74 | 5.23 | 2.19 | 192 | 274 | 15.7 |
| 75 | 600 | 2.07 | 6.20 | 2.19 | 247 | 353 | 17.1 |
| 75 | 800 | 2.40 | 7.20 | 2.19 | 303 | 433 | 18.0 |
| 85 | 600 | 2.20 | 6.61 | 2.40 | 251 | 359 | 16.3 |
| 85 | 800 | 2.55 | 7.64 | 2.40 | 307 | 438 | 17.2 |
| 85 | 1,000 | 2.90 | 8.70 | 2.40 | 362 | 517 | 17.8 |
| 95 | 600 | 2.34 | 7.01 | 2.61 | 259 | 370 | 15.9 |
| 95 | 800 | 2.69 | 8.07 | 2.61 | 316 | 451 | 16.8 |
| 95 | 1,000 | 3.05 | 9.15 | 2.61 | 372 | 531 | 17.4 |
| 105 | 600 | 2.47 | 7.39 | 2.82 | 267 | 382 | 15.5 |
| 105 | 800 | 2.82 | 8.47 | 2.82 | 324 | 463 | 16.4 |
| 105 | 1,000 | 3.19 | 9.58 | 2.82 | 381 | 545 | 17.1 |
| 105 | 1,200 | 3.57 | 10.70 | 2.82 | 438 | 626 | 17.6 |
| 115 | 600 | 2.59 | 7.77 | 3.01 | 275 | 393 | 15.2 |
| 115 | 800 | 2.95 | 8.86 | 3.01 | 333 | 475 | 16.1 |
| 115 | 1,000 | 3.33 | 9.99 | 3.01 | 391 | 558 | 16.8 |
| 115 | 1,200 | 3.71 | 11.14 | 3.01 | 449 | 641 | 17.3 |
| 125 | 600 | 2.71 | 8.13 | 3.21 | 283 | 404 | 14.9 |
| 125 | 800 | 3.08 | 9.24 | 3.21 | 341 | 487 | 15.8 |
| 125 | 1,000 | 3.46 | 10.39 | 3.21 | 400 | 571 | 16.5 |
| 125 | 1,200 | 3.85 | 11.56 | 3.21 | 459 | 655 | 17.0 |
| 125 | 1,400 | 4.25 | 12.74 | 3.21 | 517 | 739 | 17.4 |

### Tabela 10-11 — Vitelos de raças grandes, só leite/sucedâneo [p.240] (conferida na imagem; corrigidas 5 células do OCR; **reconstruída: EM/IMS/ELm exatos**)

^a IMS necessária com sucedâneo de **4.6 Mcal EM/kg MS**. ^b PM/PB = 0.95. GPV/GMD = 0.91 e PCV = 0.94 PC.

| PC (kg) | GMD (g/d) | IMS (kg/d) | EM (Mcal/d) | ELm (Mcal/d) | PM (g/d) | PB (g/d) | PB (% da IMS) |
|---|---|---|---|---|---|---|---|
| 40 | 300 | 0.55 | 2.54 | 1.17 | 114 | 120 | 21.8 |
| 40 | 600 | 0.78 | 3.59 | 1.17 | 187 | 197 | 25.2 |
| 50 | 300 | 0.63 | 2.88 | 1.38 | 120 | 126 | 20.1 |
| 50 | 600 | 0.86 | 3.98 | 1.38 | 193 | 204 | 23.6 |
| 50 | 900 | 1.12 | 5.13 | 1.38 | 267 | 281 | 25.2 |
| 75 | 300 | 0.79 | 3.65 | 1.87 | 132 | 139 | 17.6 |
| 75 | 600 | 1.05 | 4.84 | 1.87 | 208 | 219 | 20.8 |
| 75 | 900 | 1.32 | 6.10 | 1.87 | 284 | 299 | 22.6 |
| 75 | 1,200 | 1.61 | 7.40 | 1.87 | 360 | 379 | 23.6 |
| 100 | 600 | 1.22 | 5.60 | 2.32 | 222 | 234 | 19.2 |
| 100 | 900 | 1.51 | 6.93 | 2.32 | 300 | 316 | 21.0 |
| 100 | 1,200 | 1.81 | 8.31 | 2.32 | 379 | 399 | 22.0 |
| 100 | 1,500 | 2.11 | 9.73 | 2.32 | 457 | 480 | 22.8 |
| 125 | 600 | 1.37 | 6.30 | 2.75 | 235 | 247 | 18.1 |
| 125 | 900 | 1.67 | 7.70 | 2.75 | 316 | 333 | 19.9 |
| 125 | 1,200 | 1.99 | 9.14 | 2.75 | 397 | 418 | 21.0 |
| 125 | 1,500 | 2.31 | 10.62 | 2.75 | 478 | 503 | 21.8 |
| 150 | 600 | 1.51 | 6.95 | 3.15 | 248 | 261 | 17.2 |
| 150 | 900 | 1.83 | 8.40 | 3.15 | 331 | 349 | 19.1 |
| 150 | 1,200 | 2.15 | 9.90 | 3.15 | 415 | 437 | 20.3 |
| 150 | 1,500 | 2.49 | 11.40 | 3.15 | 498 | 525 | 21.1 |
| 175 | 600 | 1.65 | 7.57 | 3.54 | 260 | 274 | 16.6 |
| 175 | 900 | 1.97 | 9.07 | 3.54 | 349 | 365 | 18.5 |
| 175 | 1,200 | 2.31 | 10.62 | 3.54 | 433 | 456 | 19.8 |
| 175 | 1,500 | 2.65 | 12.20 | 3.54 | 519 | 547 | 20.6 |
| 200 | 600 | 1.77 | 8.17 | 3.91 | 273 | 287 | 16.2 |
| 200 | 900 | 2.11 | 9.70 | 3.91 | 362 | 381 | 18.1 |
| 200 | 1,200 | 2.45 | 11.29 | 3.91 | 452 | 475 | 19.4 |
| 200 | 1,500 | 2.81 | 12.92 | 3.91 | 541 | 569 | 20.3 |
| 225 | 600 | 1.90 | 8.73 | 4.27 | 286 | 301 | 15.8 |
| 225 | 900 | 2.24 | 10.31 | 4.27 | 378 | 398 | 17.8 |
| 225 | 1,200 | 2.59 | 11.94 | 4.27 | 471 | 496 | 19.1 |
| 225 | 1,500 | 2.96 | 13.61 | 4.27 | 563 | 593 | 20.0 |

(Corrigido pela imagem vs OCR: 125 kg/900 g EM 7.70 (OCR "TM"); 200 kg/900 g IMS 2.11 (OCR "2.4"); 175 kg/1,200 g IMS 2.31; 225 kg/1,200 g ELm 4.27 (OCR "4279"); 175 kg/1,500 ELm 3.54.) Mesmo acima de 200 kg usa-se Eq. 10-15 (o texto proíbe > 200 kg: tabela chega a 225 kg) ⚠11.

### Tabela 10-12 — CA dos minerais para bezerras [p.240] (conferida na imagem)

| Mineral | Sucedâneo e concentrado inicial^a (pré-desmame) | Dieta pós-desmame^b |
|---|---|---|
| Ca | NA^c | 0.60 |
| P | NA | 0.75 |
| Mg | NA | 0.26 |
| K | NA | 1.0 |
| Na | NA | 1.0 |
| Cu | 0.5 | 0.10 |
| Fe | 0.25 | 0.10 |
| Mn | 0.01 | 0.005 |
| Zn | 0.20 | 0.20 |

^a adequados p/ rúmen imaturo. ^b usados p/ pós-desmame; macrominerais e maioria dos microminerais típicos de dietas de animais adultos; CA do Cu derivado de cordeiros recém-desmamados (Suttle 1975) e continuará caindo até 0.05 (animais velhos) conforme aumenta a ingestão de forragem. ^c para macrominerais pré-desmame usa-se o coeficiente de retenção (Castro et al. 2019) em vez de CA. Regras: um CA único para a dieta total (não por alimento); se o usuário seleciona "bezerra" e a dieta não tem líquido (desmamada), usam-se as equações dos animais mais velhos (cap. 7) com a coluna "pós-desmame"; quando havia vários CA, adotou-se o mais baixo [p.240]. Se "novilha em crescimento" é selecionada, os CA passam aos do cap. 7; o submodelo de bezerra vale até 125 kg de PC [p.242].

### Tabela 10-13 — Concentrações recomendadas de minerais (base MS) p/ fornecer as IA, bezerras de 35–125 kg e ganho 0.5–1.2 kg/d [p.241] (conferida na imagem; OCR trocava "P" por "PB")

| Mineral | Sucedâneo | Concentrado inicial | Dieta de crescimento |
|---|---|---|---|
| Ca, % | 0.80 | 0.75 | 0.65 |
| P, % | 0.60 | 0.37 | 0.33 |
| Mg, % | 0.15 | 0.15 | 0.16 |
| K, % | 1.10 | 0.60 | 0.60 |
| Na, % | 0.40 | 0.22 | 0.20 |
| Cl, % | 0.32 | 0.17 | 0.15 |
| Co, mg/kg | NA | 0.2 | 0.2 |
| Cu, mg/kg | 5 | 12 | 12 |
| I, mg/kg | 0.8 | 0.8 | 0.5 |
| Fe, mg/kg | 85 | 60 | 55 |
| Mn, mg/kg | 60 | 40 | 60 |
| Se, mg/kg | 0.3 | 0.3 | 0.3 |
| Zn, mg/kg | 65 | 55 | 50 |

Derivação [p.241–242]: sucedâneo = média de 20 cenários (bezerras de 35–85 kg, ganho 0.5–1.0 kg/d, diferentes proporções de sucedâneo/inicial); como bezerras consomem líquido como única dieta por alguns dias, a concentração no sucedâneo = a da dieta total. Concentrado inicial: bezerras de 60–110 kg (Jersey–Holandesa) e ganho 0.5–1.2 kg/d, alimentadas só com sólido, usando equações de ruminantes funcionais (cap. 7) exceto Cu (absorção de cordeiros recém-desmamados). Dieta de crescimento: bezerras de 80–125 kg. Mudanças vs NRC 2001: Ca menor no sucedâneo e similar nos demais; P ~15% menor; K ~70% maior no sucedâneo; Na similar; Cu ~metade; Fe ~15% menor no sucedâneo; Mn maior no sucedâneo; Zn ~40% maior.

### Tabela 10-14 — Concentrações de minerais e vitaminas lipossolúveis no leite integral, por litro [p.241] (conferida na imagem)

| Mineral | Faixa | Média^b |
|---|---|---|
| Ca, g | 0.93–1.47 | 1.0 |
| P, g | 0.8–1.0 | 0.9 |
| Mg, g | 0.10–0.13 | 0.11 |
| K, g | 1.27–1.71 | 1.49 |
| Na, g | 0.33–0.48 | 0.41 |
| Cl, g | 0.85–1.09 | 0.97 |
| S, g | 0.18–0.31 | 0.25 |
| Cu, mg | 0.03–0.06^c | 0.04 |
| I, mg | 0.1–0.4^d | 0.2 |
| Fe, mg | 0.1–0.4 | 0.2 |
| Mn, mg | 0.012–0.05 | 0.03 |
| Se, mg | 0.018–0.04^e | 0.02 |
| Zn, mg | 3–6 | 4.0 |
| Vitamina A, UI | 300–1,300 | 1,000 |
| Vitamina D, UI | 14–40 | 27 |
| Vitamina E, UI | 0.7–1.8 | 1.2 |

^b médias p/ vacas Holandesas (raça pode afetar). ^c maiores se vacas recebem muito Cu. ^d relação linear positiva com ingestão de I. ^e menores com Se inorgânico, maiores com levedura de Se. Vitaminas A, D, E correlacionam-se positivamente com a ingestão da vaca e a gordura do leite. S = enxofre.

### Tabela 10-15 — IA recomendadas para vitaminas lipossolúveis [p.243] (conferida na imagem)

| Vitamina | UI/kg PC | UI/kg MS: sucedâneo^b | UI/kg MS: concentrado inicial^c | UI/kg MS: concentrado de crescimento^d |
|---|---|---|---|---|
| Vitamina A | 110 | 11,000 | 3,700 | 3,700 |
| Vitamina D | 32 | 3,200 (texto: 3,500) | 1,100 | 1,100 |
| Vitamina E | 2.0 | 200 | 67 | 67 |

^a Vitaminas hidrossolúveis necessárias no sucedâneo, por kg de MS (NRC 2001): 6.5 mg tiamina, riboflavina e piridoxina; 13 mg ácido pantotênico; 10 mg niacina; 0.1 mg biotina; 0.5 mg ácido fólico; 0.07 mg B12; 1,000 mg colina (o rodapé diz "6.5 mg de MS" por erro de redação). Síntese microbiana intestinal de vitamina K parece suficiente. ^b bezerra de 60 kg consumindo 0.6 kg de sólidos de sucedâneo; concentrações devem ser reduzidas se o consumo de sucedâneo for substancialmente maior (≥ 1 kg de sólidos/d). ^c bezerra de 80 kg consumindo 2.4 kg MS de inicial. ^d bezerra de 110 kg consumindo 3.3 kg MS de concentrado de crescimento. ⚠13: o texto (p.243) diz 3,500 UI vit D/kg de sólidos para 65 kg (2,100 UI/d ÷ 0.6 kg); a tabela (60 kg) dá 3,200 (= 32×60/0.6).

### Tabela 10-16 — Exemplos de especificações de concentrados iniciais típicos [p.246] (conferida na imagem)

| Variável | Unidade | 16% PB baixo amido | 18% PB baixo amido | 18% PB alto amido (a) | 18% PB alto amido (b) | 22% PB amido moderado | 22% PB alto amido |
|---|---|---|---|---|---|---|---|
| MS | % matéria natural | 87.7 | 87.5 | 88.7 | 86.3 | 87.8 | 89.0 |
| Amido | % MS | 15.1 | 20.7 | 36.9 | 39.0 | 25.5 | 32.9 |
| PB | % MS | 18.8 | 20.0 | 18.7 | 20.2 | 24.7 | 25.0 |
| FDA | % MS | 10.1 | 14.2 | 7.9 | 7.6 | 9.4 | 7.0 |
| FDN | % MS | 24.8 | 29.5 | 18.9 | 15.9 | 16.3 | 13.7 |
| FDND48 | % FDN | 49.1 | 60.0 | 53.1 | 55.4 | 65.3 | 59.6 |
| Lignina | % MS | 2.91 | 2.19 | 2.09 | 1.83 | 1.61 | 1.61 |
| Cinzas | % MS | 8.0 | 9.1 | 8.3 | 7.9 | 7.0 | 8.8 |
| Carboidratos hidrossolúveis | % MS | 4.2 | 3.5 | 8.2 | 7.2 | 12.0 | 9.2 |
| Gordura bruta | % MS | 6.9 | 5.1 | 3.9 | 3.6 | 3.3 | 3.2 |
| ED (base não informada no cabeçalho truncado) | Mcal/kg | 2.67 | 3.21 | 3.22 | 3.19 | 3.62 | 3.38 |
| EM | Mcal/kg | 2.48 | 2.99 | 2.99 | 2.97 | 3.37 | 3.14 |

(A linha "Amido" aparece duas vezes na tabela impressa, com os mesmos valores.) ⚠14: o cabeçalho "16% PB" contrasta com PB medida 18.8%; EM/ED = 0.93 em todas as colunas. FDND48 = FDN digestível em 48 h (% da FDN).

### Tabela 10-17 — GPV estimado para bezerras de igual PCV, pré e pós-desmame [p.250] (conferida na imagem)

^a devido ao enchimento intestinal, o PCV é menor proporção do PC após o desmame. ^b EM do concentrado inicial = 3.1 Mcal/kg.

| | Antes do desmame: PC (kg) | PCV (kg) | IMS sucedâneo (kg/d) | IMS concentrado inicial (kg/d) | GPV (kg/d) | Desmamada: PC (kg) | PCV (kg) | IMS concentrado inicial^b (kg/d) | GPV (kg/d) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 60 | 55.8 | 0.25 | 0.75 | 0.20 | 65.6 | 55.8 | 0.75 | −0.16 |
| 2 | 60 | 55.8 | 0.25 | 1.25 | 0.52 | 65.6 | 55.8 | 1.25 | 0.14 |
| 3 | 60 | 55.8 | 0.25 | 1.75 | 0.83 | 65.6 | 55.8 | 1.75 | 0.45 |
| 4 | 60 | 55.8 | 0.25 | 2.25 | 1.14 | 65.6 | 55.8 | 2.25 | 0.76 |
| 5 | 80 | 74.4 | 0.25 | 1.0 | 0.24 | 87 | 74.4 | 1.0 | −0.15 |
| 6 | 80 | 74.4 | 0.25 | 1.5 | 0.54 | 87 | 74.4 | 1.5 | 0.14 |
| 7 | 80 | 74.4 | 0.25 | 2.0 | 0.84 | 87 | 74.4 | 2.0 | **0.51 ⚠ [≈ 0.43]** |
| 8 | 80 | 74.4 | 0.25 | 2.5 | 1.13 | 87 | 74.4 | 2.5 | 0.724 |

⚠10: a célula 0.51 (87 kg, 2.0 kg) quebra a progressão (0.14 → ? → 0.724); pela Eq. 10-17 impressa o valor é 0.432. As colunas "Desmamada" reproduzem-se com: ELm = 0.097×PCV^0.75; k_m e k_g do sólido de EM 3.1 pelas Eq. 10-4/10-6 (0.6285 e 0.4206); GPV = ER/(PCV^0.205)^(1/1.1). Colunas "antes do desmame" não foram reproduzidas exatamente (modelo dá ≈ +0.03–0.06 acima; dependem da EM do sucedâneo, não informada nesta tabela, e de como k é ponderado). "Pré-desmame" usa PCV/PC = 0.93 (55.8/60); "desmamada" PCV/PC = 0.85 (55.8/65.6; 74.4/87.5 ⇒ 87 kg impresso é arredondado).

### Tabela 10-18 — Equações p/ estimar IgG do colostro pela leitura Brix [p.254] (conferida na imagem)

`IgG do colostro (g/L) = Intercepto + Curva × BRIX (%)`. PE = ponto de equilíbrio = BRIX (%) recomendado p/ ≥ 50 g/L de IgG.

| Autor | N | Raça | Intercepto | Curva | R² | PE |
|---|---|---|---|---|---|---|
| Chigerwe et al., 2008 | 171 | Holandesa | −24.7 | 3.96 | 0.41 | 22 |
| Bielmann et al., 2010 (ótico) | 273 | Holandesa | −188.262 | 10.730 | 0.51 | 22 |
| Bielmann et al., 2010 (digital) | 273 | Holandesa | −207.434 | 11.561 | 0.53 | 22 |
| Morrill et al., 2012^c | 823 | Misturadas^d | −40.509 | 5.2358 | 0.53 | 18 |
| Quigley et al., 2013 | 183 | Holandesa | −61.896 | 5.666 | 0.75 | 21 |
| Bartier et al., 2015 | 460 | Não relatado | −29.257 | 3.8393 | 0.43 | 23 |
| Morrill et al., 2015 | 58 | Jersey | −49.292 | 6.0052 | 0.63 | 18 |
| Løkke et al., 2016 | 126 | Misturadas^d | −58.00 | 4.82 | 0.66 | 22 |
| Silva-del-Río et al., 2017 | 202 | Jersey^e | −53.3 | 5.5 | 0.58 | 21 |

^c Brix calculado a partir do índice refrativo. ^d amostras de Holandesas e Jerseys não categorizadas, pool. ^e primeira e segunda ordenha de vacas Jersey multíparas. ⚠15: o PE impresso não é sempre (50 − a)/b: Chigerwe 18.9, Morrill 2012 17.3, Quigley 19.7, Bartier 20.6, Morrill 2015 16.5, Silva-del-Río 18.8; (Bielmann 22.2/22.3 e Løkke 22.4 conferem). Usar o PE impresso e as recomendações do texto (≥ 22% Holandesa; ≥ 18% Jersey).

---

## 6. Regras de decisão / restrições para o otimizador e alertas

**Categoria e escopo**
- Bezerra: PC < 18% do PCMat (125 kg p/ PCMat 700); acima → novilha (cap. 11). Tabelas/equações de proteína (Eq. 10-15) não valem > 200 kg nem p/ novilhas ruminantes > 125 kg [p.220, 230].
- Se a dieta não tem alimento líquido (desmamada): minerais pelas equações do cap. 7 com CA pós-desmame (Tabela 10-12) [p.240].

**Energia e ingestão**
- IMS máxima de leite/sucedâneo ≈ 2.25% do PC; 2% do PC na 1ª semana; ~2.5% do PC em > 65 kg ad libitum; vitelos < 2% a 120 kg [p.220]. Ad libitum de leite ≈ 20% do PC (10–12 L/d para 50–60 kg) ≈ 1.3–1.6 kg sólidos/d (≈ 2.5% PC); sucedâneo ad lib 1.2–1.4 kg MS/d [p.243–244].
- IMS das tabelas = quantidade necessária p/ a EM; **não** é predição de ingestão voluntária [p.235].
- Concentrado inicial: Eq. 10-1 se T ≤ 35 °C; Eq. 10-2 se T > 35 °C [p.221–222]. Ingestão do inicial é inversamente proporcional ao líquido ofertado; desenvolvimento ruminal leva ~3 semanas de consumo; CV da ingestão do inicial 90% entre estudos (19–38% no mesmo local) [p.220, 244].
- Desconto opcional de 10% na EM do concentrado pré-desmame com ≥ 1.5% do PC de sólidos de leite/sucedâneo [p.233].
- EM e PM: crescimento é limitado pelo **mais limitante** entre EM e PM; "na maioria dos casos o crescimento é limitado pela EM, não pela PM" [p.234, 236]. PB total da dieta ≥ PB das Tabelas; relação PB:EM do sucedâneo (% PB / Mcal EM/kg MS): GMD 0.2–0.4 kg/d → 4.2–4.9; 0.4–0.7 → 5.0–5.7; > 0.7 → 5.8–6.2 [p.258].
- Primeira semana de vida: EMm pode estar subestimada (taxa metabólica basal alta) e a digestibilidade menor (superestima o suprimento); GMD real na semana 1 pode ser bem menor que o previsto [p.235]. Digestão de proteína do leite imatura nas 2–3 primeiras semanas (0.95 pode estar superestimado) [p.230].

**Temperatura**
- Zona termoneutra de bezerras muito jovens 15–25 °C; TCI 15 °C (nascimento–3 sem); para mais velhas/maior consumo a TCI pode chegar a −5 a −10 °C; TCS 26 °C (texto) [p.224–225]. Fora da zona: +2.01 kcal/kg PCV^0.75/°C (ver ⚠7 sobre TCI/TCS da tabela). Calor: a bezerra não come mais para compensar (a ingestão cai, sobretudo o inicial) [p.226].
- Frio: alertar que sem alimentação a bezerra tem reservas p/ ≤ ~1 dia abaixo da TCI [p.224]; exemplo: 45 kg com 0.51 kg MS de sucedâneo 4.7 Mcal/kg (9% do PC a 12.5%) cobre mantença + 0.19 kg/d de ganho em termoneutralidade (0.29 kg/d com leite integral) e **perde peso a −5 °C** [p.245]. Mitigação: mais líquido, mais um fornecimento, mais sólidos, gordura adicional no líquido/inicial, água morna 2–3×/dia [p.225].
- Concentração de MS do sucedâneo: **≤ 20%** (excesso de minerais/desequilíbrio osmótico; sempre água livre) [p.225, 259].

**Nível de fornecimento de líquido** [p.244–245]
- "Restrição severa": < 400 g de sólidos/d (RG) ou < 300 (RP) — pode não cobrir mantença, alertar; "baixa": 400–600 (RG) / 300–450 (RP); "moderada": 600–900 (RG) / 451–700 (RP); "alta": > 900 (RG) / > 700 (RP) até ad libitum.
- **Mínimo recomendado em termoneutralidade: 1.5% do PC ao nascimento em sólidos do leite/sucedâneo**; bem-estar/fome: 8 L/d ≈ 1,000 g de sólidos (bezerras com < 8 L/d mostram sinais de fome); fornecer quantidade fixa desde o dia 1 (6–8 L/d) aumentou o crescimento nas 3 primeiras semanas sem prejudicar a saúde [p.245]. Quantidade diária constante melhora ingestão e ganho; com leite descartado de composição variável o crescimento cai [p.258–259].
- Sucedâneo típico tem 10–20% menos energia que volume igual de leite integral (gordura 15–20% vs 25–30%) [p.245].

**Desmame** [p.250]
- Critério clássico (RG): ≥ 0.9 kg MS/d de inicial de boa qualidade por ≥ 3 dias consecutivos (Drackley 2008). **Recomendação do comitê antes de concluir o desmame: RP ≥ 1.25 kg/d e RG ≥ 1.5 kg/d de concentrado inicial (90% MS)**, sobretudo p/ bezerras com alta ingestão de leite e crescimento rápido. Desmame gradual em 4–10 dias (não abrupto). Desmame com 4 semanas já foi bem-sucedido com líquido limitado e bom manejo; desmame com 24 dias suprimiu parte da imunidade inata vs 45 dias; programas agressivos de leite atrasam o inicial e a idade ao desmame.
- Alertar (Tabela 10-17): com PCV 55.8 kg, após o desmame o GPV é negativo se o inicial < ~1 kg/d (0.75 kg → −0.16; 1.25 → 0.14); a ingestão do inicial deve compensar a perda de EM líquida; EMm sobe porque o intestino/rúmen cresce e a razão PCV/PC cai de 0.93 para 0.85.

**Concentrado inicial** [p.245–249]
- Estimular consumo desde a 1ª semana; manter limpo, fresco e separado da água; água livre sempre. Amido típico 22–38% (formulações < 20% a > 40%); amido > 32% pode derrubar o pH ruminal para < 5.5; ideal manter pH > 6.0; fibra prontamente fermentável (polpa de beterraba, DDGS, casca de soja, polpa cítrica); forragem na fibra do inicial < 15%; FDN > 13% da MS (recomendação comum; forma física importa). Palatabilidade: melaço de 12% da MS reduziu a ingestão vs 5%.
- Tamanho de partícula: ≥ 80% das partículas > 1,190 µm e média ponderada ≥ ~2,000 µm (evita paraqueratose e timpanismo); peneirar em matéria natural. Concentrado fino/peletizado sem forragem e cama não orgânica: alertar; inconsistência de forma física (pellets com finos) reduz ingestão. (Terré 2013: 18% FDN > 27% FDN em GMD) [p.247–248].
- PB do inicial: 18% (MS) suficiente com 0.45–0.55 kg/d MS de líquido; 22–25% com ≥ 0.9 kg/d MS de líquido; RP de crescimento rápido podem precisar > 22% PB. Suplementar PNDR para elevar PM em geral não aumentou GMD. Gordura no inicial: respostas inconsistentes (em geral < 5% da MS) [p.248–249].
- Forragem: fornecer apenas se inicial peletizado/fino e cama sem palha; **feno de alfafa ≤ 10% da IMS total; outras forragens picadas ≤ 5% da MS total**; > 15% da IMS total aumenta enchimento intestinal (infla GMD sem ganho de tecido); bezerras com inicial texturizado adequado e cama de palha picada ganham pouco com forragem [p.249–250].

**Sucedâneo (formulação)** [p.257–259]
- Proteína do soro pode substituir leite desnatado sem perda; proteínas vegetais processadas podem substituir ~50% da proteína do leite; farinha de soja crua e proteína concentrada de ervilha são mal utilizadas; AA limitantes: Lys, Met, Thr — equiparar ao leite; sucedâneo 26% PB: ótimos Lys 2.34% e Met 0.72% da MS; 27% PB com Lys 2.43%, Met 0.76%, Arg 0.68%, His 0.48% (sem efeito de Arg/His a 680 g sólidos/d); Met adicional desnecessária se > 28% PB e 0.57% Met (Castro 2016c). Proteínas vegetais → NMF 34.4 g/kg MS (flag).
- Gordura: sebo, gordura branca, banha, palma; óleo de coco < 15% dos lipídios; homogeneização crítica; óleos vegetais com muitos AG livres são mal digeridos; **sem exigência estabelecida de C18:2/C18:3** (leite padrão 1–3% de C18:2 e 0.5–2% de C18:3, razão 4:1 a 6:1; 1 kg de sólidos do leite ≈ 5.1 g C18:2 e 1.5 g C18:3). Lactose: > 97% desaparece até o íleo; amido/maltodextrinas pouco digeridos: **não recomendados para bezerras < 4 semanas**.
- Mistura: seguir a temperatura do fabricante; 12.5–15% de sólidos usual; > 15% mais timpanismo abomasal (Burgstaller 2017); a 20% manter água livre. Leite integral com ≥ 600 mOsm/kg pode atrasar o esvaziamento abomasal [p.259].

**Leite integral / descarte** [p.259–260]: composição variável (média 11.2% sólidos, 5.1–13.4% na amostra de Moore 2009); padronizar sólidos (até 20% da MS) com sucedâneo em pó; pasteurizar e fornecer em ≤ 1 h; risco de patógenos (Cryptosporidium, Mycoplasma, MAP) e resíduos de antibióticos (apenas leite de descarte pasteurizado de vacas não tratadas; descartar o de vacas tratadas); leite desequilibrado em vit. D, E e Fe, Mn, Zn, Cu, I, Se → suplementar.

**Colostro e transferência de imunidade** [p.253–255]
- Fechamento intestinal ≈ 24 h (22–24 h; IgM 16 h, IgA 22 h, IgG 27 h; DP ~4 h); EAAbs < 10% a ~40% (teto ~50%); VP = 8.9% do PC; IgG sérica ≥ 10 g/L aos 24–48 h = transferência adequada (< 10 g/L = falha; 13% das bezerras nos EUA; 14.3% entre 10 e 14; 72.7% > 15 g/L).
- Meta: **150 g de IgG no 1º fornecimento e 200 g nas primeiras 24 h**; colostro de boa qualidade > 50 g IgG/L; ~25% dos colostros de 1ª ordenha não fornecem > 150 g em ≤ 4 L. Holandesas: 3 L de colostro com ≥ 22% Brix em ≤ 1 h + 2–3 L aos 10–12 h; Jersey: 2 L com ≥ 18% Brix em ≤ 1 h e novamente aos 10–12 h; alternativa: 3.8–4.0 L por sonda esofágica ≤ 1 h (+ 2 L opcional aos 10–12 h). 8.5% do PC ao nascimento superou 7% e 10% (IgG sérica 15–25% maior) [p.254–255]. Não usar colostro de baixo Brix. Leite de transição (dias 2–3) fornecer se possível; colostro pasteurizado (sem perda de Ig) melhora IgG e saúde; substitutos de colostro devem fornecer 150–200 g de IgG, EAA igual ou menor que colostro materno.
- IgG do colostro cai 27% em coleta 10 h após o parto vs 2 h; segunda ordenha de Jersey −44%.

**Água e eletrólitos** [p.255–256]: água desde a 1ª semana (morna 16–18 °C > fria 6–8 °C); falta de água reduz ingestão do inicial e GMD em > 30%; +1 L de água → +82 g de inicial e +56 g/d de GPV (5 sem); consumo < 2 L/d nas 3 primeiras semanas, ~4:1 L água/kg MS seca pós-desmame. Diarreia: perda de 1–10% do PC; mortalidade comum com desidratação > 12%; repor água e eletrólitos **fora** do programa de leite (misturar não repõe água); osmolaridade da solução final < 700–750 mOsm/L; solução de reidratação oral: Na, agentes de absorção (glicose, citrato, acetato, propionato, glicina), alcalinizantes e energia; manter leite; bicarbonato pode inibir coágulo de caseína.
**Doença e nutrição** [p.256–257]: morbidade pré-desmame 34% (digestiva > 50%, respiratória 31%); com diarreia: fezes 20–40× maiores, queda da digestibilidade da MS (~40%), gordura < 50% digestível em diarreia aquosa (> 50 g/kg PC), > 50% em balanço energético negativo; ingestão de inicial −40% nos 21 d. Não modelado.
**Frequência e alojamento** [p.250–252]: 1×/d dá desempenho semelhante a 2×/d com baixo/moderado líquido; > 2×/d pode melhorar eficiência em alta taxa (≥ 2.5× mantença) e reduz risco de úlcera/timpanismo abomasal; frio: um fornecimento extra. Grupos > 8 bezerras/baia aumentam risco; alimentador automático: introdução em < 24 h, > 6 L/d, ventilação, cama seca.
**Nutrição fetal** [p.252–253]: > 60% do ganho fetal nos últimos 60 dias; sub/super-alimentação moderada da vaca seca não muda peso ao nascer; deficiência de P, Mn, Co, Cu, Zn, Se pode causar déficit; bezerra nasce com baixo status de vit. A, D, E (depende do colostro).
**Aditivos** [p.260–262] (não modelados): ionóforos/decoquinato (coccidiose); NaHCO3 1–3% do inicial sem resposta; produtos de levedura ~1.5×10^6 cfu/g do inicial (corrigido pela imagem); cultura de levedura 3.5–14 g/d; butirato de sódio ~0.3% da MS; OE 2.5 g/d; plasma 4–5% do sucedâneo; gema de ovo IgY 5–10 g/d; lactoferrina; antibióticos como promotor de crescimento proibidos sem receita nos EUA.

**Vitaminas e minerais — restrições específicas** [p.241–243]
- Vit. A: IA = 110 UI/kg PC (≈ 6,600 UI/d p/ 60 kg; 11,000 UI/kg sólidos a 0.6 kg/d); com ingestão alta de sucedâneo (> 1 kg sólidos/d) a concentração deve ser **< 9,900 UI/kg de sólidos**; sem benefício acima de ~7,000 UI/d; 17,000–39,000 UI/d reduziu α-tocoferol plasmático (vit. A em excesso prejudica status de vit. E). Dados: ~5,400 UI/d mantêm retinol hepático ≈ 20 mg/kg; 3,800 UI/d é insuficiente.
- Vit. D: IA = 32 UI/kg PC (2,100 UI/d p/ 65 kg) p/ 25-OH-D sérica 30 ng/mL; Vit. E: IA = 2 UI/kg PC (≈ 125 UI/d; a menor dose benéfica; pode ser insuficiente para bezerras de crescimento rápido; ~30 UI/d só evita estresse oxidativo por AGPI).
- Vit. K: não necessária (exceto trevo-doce mofado). B e colina: adicionar ao sucedâneo; pós-desmame suficiente.
- Se: 0.3 mg/kg MS (doença do músculo branco); leite integral geralmente não fornece o suficiente. I: 0.8 mg/kg MS. Co: sem IA no sucedâneo.

---

## 7. Lógica e fluxo

**Ordem de cálculo sugerida** (a ordem é minha, montada a partir das equações; o livro não descreve o fluxo do software; itens marcados "(rep.)" foram **reproduzidos numericamente contra as tabelas**):
1. Categoria (bezerra se PC < 18% PCMat). Fase: só líquido / líquido + sólido / desmamada / vitelo. PCMat = 700 (RG) ou 530 (RP).
2. PCV = PC × (PCV/PC); GPV = GMD × (GPV/GMD) (Tabela 10-1; só leite 0.94/0.94 (rep. Tab. 10-7); líquido + sólido 0.93/0.91 (rep. Tab. 10-8); desmamada 0.85/0.85 (rep. Tab. 10-10); vitelo 0.94/0.91 (rep. Tab. 10-11)).
3. EM dos alimentos: líquidos (Eq. 10-16 × 0.91 ou 0.93; Tabela 10-4); concentrado inicial (cap. 3 com gordura 0.81, sem desconto de amido, × 0.93; desconto opcional 10%).
4. Previsão de IMS do concentrado (Eq. 10-1/10-2) a partir de PC, EMiDL, Tpconc.
5. k_m e k_g da dieta: líquido: k_m 0.719 (só leite) e k_g 0.55; sólido: k_m = ELm(EM)/EM (Eq. 10-4), k_g = ELg(EM)/EM (Eq. 10-6); dieta mista = média ponderada pela contribuição à EM total (a ponderação exata e o k_m do líquido nas misturas — 0.69 da Tabela 10-1 vs 0.719 — não são especificados ⚠22).
6. Mantença: ELm = coef × PCV^0.75 (76.9 kcal; 97.0 kcal desmamadas; ×1.02 implícito com sólido); EMm = ELm/k_m (rep.: 0.107 × PCV^0.75 só leite).
7. Termorregulação: ΔEMm = 2.01 kcal × PCV^0.75 × ΔT fora da zona termoneutra.
8. Ganho: **exigência**: ER = GPV^1.1 × PCV^0.205 (Eq. 10-5); EM_ganho = ER/k_g; EM total = EMm + termorreg + EM_ganho (rep.: EM = 0.107×PCV^0.75 + ER/0.55 reproduz a Tabela 10-7 com erro ≤ 0.01 Mcal; vitelos com GPV = 0.91 GMD reproduzem a Tabela 10-11). **Predição**: ER = (IEM − EMm − termorreg) × k_g; GPV = ER/(PCV^0.205)^(1/1.1) (Eq. 10-17 literal, rep. Tab. 10-17 desmamadas); GMD = GPV/(GPV/GMD).
9. Composição do ganho (Eq. 10-7, 10-8) a partir da ER.
10. Proteína: PBEU (10-11), descamação (10-10), PMF (10-12; 11.9×IMSAL + 20.6×IMSAS), PM_mant (10-13); PLg (10-14); eficiência (10-15); **PM = PM_mant + PLg/ef** (rep. Tab. 10-7, 10-10, 10-11, 10-8); PB = PM / (0.95 leite; 0.75 leite + inicial pós-rúmen; 0.70 rúmen funcional; mistura ponderada pela PB de cada fonte).
11. GMD permitido = mínimo entre o permitido pela EM e pela PM.
12. Minerais (Eq. 10-19–10-27; PCV=0.94 PC, GPV=0.91 GMD) e vitaminas (UI/kg PC; Tabela 10-15); concentrações recomendadas (Tabela 10-13).

**Receita numérica verificada (para testes de unidade)** — script em /tmp/claude-0/nasem/work/c10/model.py:
- Tabela 10-7: IMS = EM/4.6 (RG) ou /4.7 (RP); EMm = 0.107×PCV^0.75; ELm = 0.0769×PCV^0.75; EM = EMm + (GPV^1.1·PCV^0.205)/0.55; PCV = 0.94 PC; GPV = 0.94 GMD; PM = [2.75·PC^0.5 + (0.22·PC^0.6 + 11.9·IMS)/0.68] + PLg/(0.70 − 0.532·PC/PCMat); PB = PM/0.95. Exemplos: 25 kg RP/200 g → EM 1.694 (tab. 1.69), PM 83.3 (83), PB 87.6 (87); 50 kg RG/1,000 g → EM 5.66 (5.66), PM 300.6 (299), PB 316.4 (315). Erro máximo nas 22 linhas: EM 0.01 Mcal; PM +1.6 g/d; IMS 0.01.
- Tabela 10-11: igual, com GPV = 0.91 GMD (PCV = 0.94 PC) e sucedâneo 4.6: 33 linhas, EM ≤ 0.04 Mcal, PM +0.3 a +3 g/d (modelo ligeiramente acima).
- Tabela 10-10: ELm = 0.097×(0.85 PC)^0.75; k_m = ELm(3.0)/3.0 = 0.6257 e k_g = ELg(3.0)/3.0 = 0.4140; GPV = 0.85 GMD; PMF com 20.6×IMS; PB = PM/0.70; IMS = EM/3.0: 28 linhas, EM ≤ 0.01 Mcal; PM −3 a +2 g/d.
- Tabelas 10-8 e 10-9: reconstrução com EM = ELm_{×1.0–1.02}/k_m + ER/k_g, k ponderados pela fração de EM, EM do sucedâneo 4.9/4.7/4.6 e do inicial 3.1/3.2: EM e IMS dentro de ±0.03–0.06 (menor erro médio com k_m,leite 0.68–0.69). Identificou os 6 erros de impressão da Tabela 10-9.

**Dependências de outros capítulos:** ED de alimentos sólidos (cap. 3 e 19); parâmetros de proteína dos cap. 6; minerais e CA de ruminantes funcionais (cap. 7); vitaminas (cap. 8); novilhas > 125 kg (cap. 11); período de transição (cap. 12).

---

## 8. Limitações, incertezas e mudanças vs NRC 2001

- **Mantença:** ELm caiu de 0.086 (NRC 1989/2001, Mcal/kg PC^0.75, com 10% de atividade embutida) para 0.077 Mcal/kg PCV^0.75; k_m de 0.86 para 0.719 (INRA 2019: 0.726; Silva et al. 2017: 0.706); EMm 0.107 (similar ao NRC 2001). Não há valores separados por raça/dieta (estatisticamente indistinguíveis); Jersey pode ter mantença até 20% maior (mantida igual; "pesquisa necessária").
- **Primeira semana de vida:** mantença subestimada e digestibilidade menor que a modelada [p.235].
- **k_g do leite 0.55 (vs 0.69 NRC 2001)**; do sólido 0.378–0.441; ganho de energia por kg de PC 18% menor que o NRC 2001 em bezerras grandes e de ganho rápido (2.11 vs 2.57 Mcal/kg).
- **EMm do desmamado** (0.097 ELm) baseia-se em apenas dois estudos (Stamey Lanier 2021, Meyer 2005); "dados adicionais são necessários" [p.223]. Modelo subestima GMD baixo e superestima GMD alto em desmamadas (obs = 0.366 + 0.662×est; viés de inclinação não corrigido) [p.236].
- Transição para desmame: relação PCV/PC e GPV/GMD ainda mal definidas ("necessita mais pesquisas") [p.220].
- Dados insuficientes para modelar: efeito da fonte de gordura/perfil de AG na digestibilidade; interações gordura × IEM × PM na eficiência para ER; digestibilidade de PB relacionada à idade; PDR/PNDR e fluxo de PB microbiana por IMS (só o platô 1.32 kg/d); custo energético adicional de proteínas vegetais (só NMF muda); EM efetiva sob rúmen imaturo (só desconto arbitrário de 10%) [p.226–233].
- Estresse por calor: TCS 26 °C e inclinação igual à do frio são suposições "na ausência de dados" [p.225].
- **O que não entra no modelo (só discussão):** Eq. 10-9 (Roy 1980), fatores de colostro (exceto como regra), nível de fornecimento, forragem, frequência, alojamento, aditivos, doenças, nutrição fetal, água (exceto como alerta).
- NRC 2001 vs atual (subgrupo de 111 médias): atual `obs = 0.98·est + 0.01`, RMSE 0.12, CCC 0.93; NRC 2001 `1.01·est − 0.09`, RMSE 0.16, CCC 0.85, erro de média 21.6% do EMQP [p.234]. (O livro imprime "CIA −170.0" e "−120"; provavelmente AIC.)
- Proteína: PM/PB 0.70 (vs 0.75 ARC/NRC 2001) para rúmen funcional; PM no lugar de PDA; VB 0.80 do NRC substituído por eficiências 0.70→0.55 (Eq. 10-15).
- Minerais: viram IA (abordagem fatorial c/ coeficientes de retenção) em vez de concentrações fixas; Co sem IA no sucedâneo; vit. D 3,200 UI/kg (aumento substancial), vit. A 110 UI/kg PC.

---

## 9. Conceitos e evidências relevantes

- Rúmen funcional depende de AGV (principalmente butirato) de concentrado fermentável; forragem seca (exceto grama fresca com açúcares) não desenvolve o rúmen [p.219–220, 245].
- Máximo de contribuição do N microbiano ao N total (60.6%) é atingido com IMS ≈ 1.3 kg/d de sólidos [p.231]; proteína de bezerras ruminantes: PB→PM 0.70.
- Deposição de gordura corporal em pré-ruminantes vem da gordura da dieta, não de carboidratos; glicose da lactose abastece síntese proteica [p.226, 228–229]. Gerrits 1996: platô de deposição proteica em vitelos pesados (160–240 kg) a 498 g/d de PB digestível (244 g/d de proteína retida) [p.229].
- Maior crescimento pré-desmame associado a maior produção de leite na 1ª lactação; novilhas de crescimento rápido não são mais pesadas ao 1º parto mas podem parir mais cedo; maior massa/proliferação mamária com alto plano de sucedâneo (1.1 vs 0.44 kg) [p.245].
- Digestibilidade da FDN: pré-desmame 32.0% (4.8–69.3), recém-desmamadas 42.6% (4.6–71.2), ≥ 3 sem pós-desmame 57.6% (42.3–70.7); sobe até ~2 kg de FDN cumulativa ingerida [p.247]. A ingestão cumulativa de carboidratos não fibrosos explica melhor a digestão e o alcance da EM estimada (Quigley 2019).
- Exemplo de energia: bezerra de 45 kg com 0.51 kg de sólidos de sucedâneo (9% do PC a 12.5%) ganha 0.19 kg/d em termoneutralidade, 0.29 kg/d com leite integral, perde peso a −5 °C [p.245].
- Sem alimentação, bezerra recém-nascida abaixo da TCI tem reserva p/ ~1 dia [p.224].
- Bezerras < 8 sem: IMS média 1.93 ± 0.33% do PC (n = 219 trat., 64 estudos; PC 54.5 ± 8.8 kg); desmamadas > 8 sem: 3.06 ± 0.31% (n = 79, 27 estudos; PC 95.6 ± 19.0 kg) [p.220].
- Cl/Na de vacas em lactação (0.8) usado para bezerras; Zn e Cu por kg GMD ajustados à concentração em músculo vs órgãos [p.239].
- Lactose pura não limita digestão em bezerras; amido: 61.6% de desaparecimento ileal, mas 89% do amido ingerido é fermentado [p.228].

---

## 10. Dúvidas / riscos de OCR (itens ⚠ para conferência humana)

1. ⚠1 **Eq. 10-1:** operador antes de `(Tpconc² × 13.496)` ausente na impressão; "+" inferido por teste numérico (resultados plausíveis só com "+"). Sem truncamento em 0 documentado.
2. ⚠2 **Eq. 10-16:** parentização impressa `(100 − Proteína − AG − Cinzas × 4)`; leitura correta provável `(100 − P − AG − Cinzas) × 4`. Tabela 10-4 só se aproxima (±2–4%) — ⚠24.
3. ⚠3 **Eq. 10-17:** forma impressa ≠ inversa exata da Eq. 10-5; a forma impressa reproduz a Tabela 10-17; o texto referencia "Eq. 10-6" no lugar da 10-5.
4. ⚠4 **Eq. 10-3 vs EMm 0.107:** ponto fixo da Eq. 10-3 como impressa é ≈ 0.112 (k_m 0.687); o livro e as tabelas usam 0.107 (k_m 0.719).
5. ⚠5 **Tabela 10-1:** EMm 113.8/k 0.69 implica ELm ≈ 78.5 (não 76.9); colunas por PC^0.75 usam razão linear PCV/PC.
6. ⚠6 **GPV/GMD** 0.94 (só leite) vs 0.91 (vitelo, minerais, exemplos do texto) vs "0.5–0.6" na transição (p.220); PCV/PC = 0.93 para vitelos > 125 kg vs 0.94 usado na Tabela 10-11.
7. ⚠7 **Tabela 10-2:** limiares implícitos (TCI 20/10 °C; TCS 25 °C) ≠ nota de rodapé (TCI 15/5 °C) ≠ texto (TCS 26 °C); exemplo textual (+38% a 0 °C com TCI 15 °C) só fecha com ΔT = 20 °C.
8. ⚠8 **Tabela 10-7:** cabeçalho "EMm" mas valores são ELm. Também o texto (p.236) cita EM = 3.89 Mcal/d para 50 kg/0.60 kg/d "só líquido", enquanto a Tabela 10-7 mostra 4.05 (e 3.66 em 40 kg/600 g); não resolvido.
9. ⚠9 (6 células) **Tabela 10-9:** PM 250, 271 e 312 (iguais à PB; esperado ≈ 209, 250, 262); EM 6.24 (60 kg/1,000/40:60; esperado ≈ 6.64); PM 375 (70 kg/800/40:60; esperado ≈ 275); EM 6.03 (80 kg/800/80:20; esperado ≈ 6.13).
10. ⚠10 **Tabela 10-17:** GPV 0.51 (desmamada, 87 kg, 2.0 kg; esperado 0.43); colunas pré-desmame não reproduzidas exatamente; "0.724" com 3 casas.
11. ⚠11 **Eq. 10-15** em 6% do PCMat dá 0.668 (texto: 0.70); Tabela 10-11 vai a 225 kg apesar de a equação só valer até 200 kg.
12. ⚠12 **Eq. 10-27:** denominador 0.25 vs CA do Zn 0.20 (Tabela 10-12); texto cita "Equações 10-25 a 10-28" (não existe 10-28).
13. ⚠13 **Vit. D no sucedâneo:** 3,200 UI/kg (Tabela 10-15, 60 kg) vs 3,500 (texto, 65 kg).
14. ⚠14 **Tabela 10-16:** rótulo "16% PB" com PB medida 18.8%; cabeçalho de ED truncado.
15. ⚠15 **Tabela 10-18:** PE impresso ≠ (50 − intercepto)/curva em 6 linhas.
16. ⚠16 **p.242:** "30,000 UI de retinol (≈ 0.9 mg)" (30,000 UI ≈ 9 mg); "100 mg/d de peso úmido" (deveria ser mg/kg).
17. ⚠17 **Fig. 10-2/Tabela 10-3:** "quatro estudos" no texto vs cinco na tabela; inclinação e intercepto da regressão segmentada não informados (só ponto de quebra e platô).
18. ⚠18 **Contagens de validação:** 416 médias/94 estudos (p.233) vs 397 médias (Fig. 10-3) vs 21 + 64 + 23 = 108 estudos; desmamadas: 79 médias/27 estudos (IMS, p.220) vs 79/23 (GMD, p.236).
19. ⚠19 **ER/EM 0.378–0.441:** 0.378 corresponde a EM = 2.6 (a EM = 2.5 dá 0.366).
20. ⚠20 **EMm de desmamadas** "0.138 Mcal/kg PCV^0.75" (texto) vs ≈ 0.155 implícito nas Tabelas 10-10 (k_m da Eq. 10-4).
21. ⚠21 **Eq. 10-18:** não está claro se a calibração é aplicada no software.
22. ⚠22 **Ponderação de k_m/k_g em dietas mistas** (Tabelas 10-8/10-9) e atribuição das notas d/e (primeiras linhas de cada dieta) inferidas; reprodução aproximada.
23. ⚠23 **PM/PB das Tabelas 10-7/10-10/10-11:** o modelo reconstruído dá PM de 0.3% a 1% acima/abaixo; origem da diferença (arredondamento de eficiência ou uso de PCV na razão PC/PCMat) não identificada.
24. ⚠24 **Tabela 10-4:** ED/EM de ingredientes não reproduzidos exatamente por Eq. 10-16 × 0.91/0.93; plantas/plasma sem ED/EM.
25. ⚠25 **Ingestão de leite descartado e leite sem tabela:** não há tabela de composição de leite de descarte além do valor médio de 11.2% de sólidos.
26. ⚠26 **p.260 (leveduras):** expoente conferido na imagem: 1.5 × 10^6 cfu/g do concentrado inicial (resolvido; informativo, não entra no cálculo).
27. ⚠27 **Dígitos em texto corrido** da p.262 e das páginas de referências conferidos só por OCR; as p.248, 249, 251, 252, 255, 257, 259, 260 e 261 foram conferidas na imagem (sem divergências relevantes). Não entram em cálculo.

Itens corrigidos pela imagem (OCR errou): Eq. 10-5 expoentes; Eq. 10-10/10-11 expoentes (0.60, 0.50); Eq. 10-19–10-23 expoentes negativos; Tabela 10-1 (colunas); Tabela 10-2 (última linha); Tabela 10-3 (todas as colunas); Tabela 10-4 (colunas); Tabela 10-7 (PB% 22.5); Tabela 10-11 (5 células); Tabela 10-13 ("P" em vez de "PB"; Cu 5); Tabela 10-15 (3,200); desconto de 10% "≥ 1.5% do PC"; Terré 2013: 18% vs 27% FDN; fórmula de IgG sérica (sem "9%").

---

COBERTURA: páginas lidas 219–277 (impressas). Texto técnico integral lido p.219–262, com conferência por imagem das páginas 220–261 (todas as que contêm equações, tabelas ou números usados no modelo; p.262 só OCR, fim do texto) e conferência numérica por reconstrução das Tabelas 10-7 a 10-11 e 10-17. Páginas 262–277: apenas referências (percorridas, sem conteúdo técnico). Ficaram de fora do detalhe: lista de referências da Tabela 10-6 (apenas contada) e a discussão extensa de aditivos (resumida na seção 6). Equações capturadas: 27 numeradas (10-1 a 10-27) + 4 fórmulas não numeradas (IgG sérica, EAAbs, Brix→IgG, Brody citada) + parâmetro de temperatura (2.01 kcal/kg PCV^0.75/°C). Tabelas capturadas: 18 (10-1 a 10-18; a 10-6 é lista de referências). Itens ⚠: 27.

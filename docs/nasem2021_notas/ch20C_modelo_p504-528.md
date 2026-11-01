# NASEM 2021 (Gado Leiteiro, 8a ed., PT-BR) — Cap. 20, PARTE C: Descrição e Avaliação do Modelo
**Páginas impressas cobertas: 504–528** (p.503 lida só como continuação; as Eq. 20-271 a 20-275, que ficam nela, estão transcritas em 4.0 por serem pré-requisito das Eq. 20-276 em diante).
Conferência: toda equação e tabela abaixo foi conferida contra a imagem da página (150 dpi; trechos duvidosos a 220-300 dpi). Onde OCR e imagem divergiram, vale a imagem e está marcado `(corrigido pela imagem)`.

- Usado diretamente no modelo? **SIM** — Cap. 20 Parte C, seções "Uso de energia e AA para mantença", "Aporte de EM", "Balanço de energia, proteína e AA", "Estimativas de produção permitidas", "Dejetos", "Eficiências", "Aporte e uso de vitaminas e minerais" (Eq. 20-276 a 20-496).
- "Avaliações de modelo" (Tabelas 20-11 a 20-16): **NÃO** entra no cálculo; serve de referência de acurácia esperada (testes de aceitação do simulador).
- "Variação do modelo em relação às especificações de desempenho animal e dieta" (Tabelas 20-17 a 20-21): **PARCIAL** — não é equação de cálculo; é análise de incerteza/sensibilidade (útil para faixas de tolerância e análise de risco).
- "Aplicação do modelo no R": **NÃO** (só descrição do software de referência; o dev não programa a partir dele, mas deve replicar o comportamento).

---

## 0. Convenções, glossário e advertências gerais

**Convenções**: `^` expoente; `_` subscrito (os códigos de variável são mantidos EXATAMENTE como impressos, em inglês); `*` ou `×` multiplicação. Separador decimal ponto, milhar vírgula. Nas tabelas "Criteria | Value" do livro (chaves), cada linha é uma condição (avaliar de cima para baixo; "else" = demais casos).

**Sufixos de variável (padrão do livro)**: `_g` = g/d (ou unidade em gramas); `_mg` = mg/d; sem sufixo e com unidade kg/d = kg/d. Prefixos: `An_` = animal; `Dt_` = dieta; `Fd_` = ingrediente (feed) f; `Fe_` = fezes; `Ur_` = urina; `Scrf_` = descamação (scurf); `Gest_` = gestação; `Milk_`/`Mlk_` = leite; `Body_`/`Bod_` = ganho corporal; `Trg_` = valor-alvo informado pelo usuário; `Env_` = ambiente; `Man_` = dejeto (manure); `Inf` = infusão (ruminal `InfRum_`, intestino delgado `InfSI_`, abomasal etc.); `Abs_` = absorvido.

**Tradução de siglas PT desta edição**: PL = proteína líquida (**NP**, net protein); PVer = proteína verdadeira (**TP**); PB = proteína bruta (**CP**); PM = proteína metabolizável (**MP**); PNDR = proteína não degradada no rúmen; MO = matéria orgânica; EL = energia líquida (**NE**); EM = energia metabolizável (**ME**); ED = energia digestível (**DE**); EB = energia bruta (**GE**); AGs = ácidos graxos (**FA**); IMS = ingestão de matéria seca (**DMIn**); PC = peso corporal (**BW**); PCV = peso corporal vazio (**EBW**); ECC = escore de condição corporal (**BCS**); Frm/Rsrv = ganho de tecido "formação"(frame) / reserva; CA = coeficiente de absorção (AC; `Fd_acXx`); CCC = coeficiente de correlação de concordância de Lin (1989); RMSE = raiz do erro quadrático médio.

**Convenção de viés nas tabelas de avaliação**: viés médio = **observado − predito** (checado: Tab. 20-13 DMIn obs 20.6, pred 20.8, viés -0.2; Tab. 20-15 Fe_CP obs 1.08, pred 0.89, viés +0.2).

**Glossário dos termos recorrentes** (unidades; definição; origem). "Cap. X" = vem de outro capítulo/seção do livro (não descrito neste bloco).

| Variável | Tradução / definição | Unidade | Origem |
|---|---|---|---|
| An_BW | PC do animal | kg | entrada |
| An_BW_mature (aparece também como An_BWmature, An_BW_Mature, An_BW_NPr_3) | PC maduro (adulto) do animal; "An_BW_NPr_3" (Eq. 20-272, vacas) = PC (subscrito NPr_3; definição não dada neste bloco) | kg | entrada / Cap. 20 pt. anteriores |
| An_EBW, An_EBW_mature | PC vazio e PC vazio maduro | kg | derivado (cap. 11/20) |
| An_EBWgain, An_BWgain | ganho de PCV / de PC | kg/d | entrada / cap. 11 |
| An_BW_empty, An_BW_mature_empty | PC vazio e PC vazio maduro (Eq. 20-271) | kg | idem |
| An_DMIn | IMS total do animal (dieta + infusões; no livro muitas vezes = Dt_DMIn) | kg/d | cap. 2/20 |
| Dt_DMIn | IMS da dieta | kg/d | cap. 2/20 |
| Dt_DMIn_ClfLiq | IMS de alimento líquido (leite/substituto) do bezerro | kg/d | entrada |
| Dt_DMIn_Milk | IMS de leite (Eq. 20-272, novilhas) | kg/d | entrada |
| An_StatePhys | estado fisiológico (valor "Calf" = bezerro; demais: novilha, vaca etc.) | texto | entrada |
| An_Parity | paridade (0 = novilha; >0 = vaca) | n | entrada |
| An_MilkProd / Mlk_Prod / Trg_MilkProd | produção de leite do animal / produzida / alvo informada pelo usuário | kg/d | entrada |
| MlkNP_Milk (aparece como MIkNP_Milk) | teor de proteína (líquida) do leite | g/g (⚠ ver 10.4) | entrada/cap. 6 |
| Trg_MilkTPp | teor-alvo de proteína verdadeira do leite informado pelo usuário | % | entrada |
| An_GestDay | dia de gestação | d | entrada |
| An_Preg | indicador de prenhez (1 = prenhe) | 0/1 | entrada |
| An_GEIn, An_DEIn, An_MEIn, An_NEIn | ingestão de EB/ED/EM/EL | Mcal/d | cap. 2/20 |
| An_NDF | NDF da dieta (usado nas Eq. 20-300 e 20-310) | % MS | cap. 20 |
| An_DigNDF | NDF digerido | % MS (⚠ unidade não informada aqui) | cap. 20 |
| Dt_ME | concentração de EM da dieta | Mcal/kg MS | cap. 20 |
| An_CPIn, An_DigCPtIn, An_MPIn(_g) | ingestão de PB; PB digestível total; PM | kg/d (CP, DigCPtIn); g/d (MP_g) | cap. 6/20 |
| Dt_PastIn / Dt_PastSuppIn | IMS de pasto / de não-pasto (suplemento) | kg/d | entrada |
| Env_DistParlor, Env_TripsParlor, Env_TopoParlor | distância de ida e volta lote→sala (m), nº de ordenhas/viagens, subida diária total (m) | m; n; m | entrada |
| T, LCT, UCT | temperatura média; temp. crítica inferior; superior | °C | Eq. 20-2 e 20-3 (início do Cap. 20) |
| AA(i)_NPScrf, AA(i)_NPGain, AA(i)_NPMFP, AA(i)_NPMilk | concentração do AA i na proteína de descamação / do ganho corporal / fecal metabólica | g/100 g PL | **Tabela 6-5** (Cap. 6) |
| Kg_MP_NP, Km_MP_NP, Ky_MP_NP, Kx_MP_NP, Kl_MP_NP,Trg | eficiências de conversão PM→PL para ganho / mantença / gestação / "x" (descamação, fecal; valor não dado neste bloco) / lactação (alvo) | g/g | Cap. 6 (Km: Eq. 20-306; Kg: Eq. 20-271) |
| Kg_ME_RE, Kl_ME_NE, Km_NE | eficiência EM→energia retida; EM→EL do leite; eficiência de mantença de bezerro (ponderada líquido/seco, composição não dada aqui) | Mcal/Mcal | Cap. 2/20 |
| NEgain_BWgain, GainNP_Gain | EL por kg de ganho de PC; PL por kg de ganho | Mcal/kg; g/kg | Cap. 11/20 |
| MilkNE_Milk | EL por kg de leite | Mcal/kg | Cap. 20 |
| Milk_NP_g, Body_NPgain_g, Gest_NP_g, Gest_NPgain_g, Milk_NP, Body_NPgain, Gest_NP, An_NPmilk_g | PL do leite, do ganho corporal, da gestação (g/d; versões sem _g em g/d também nas Eq. 20-355, 20-358..361 — sem conversão informada) | g/d | Cap. 6/20 (partes anteriores) |
| Milk_AA(i)_g, Bod_AAgain(i)_g, Gest_AA(i)_g, Abs_AA(i)_g, Dt_AAIn(i) | AA do leite, do ganho, da gestação; AA absorvido; AA ingerido | g/d | Cap. 6/20 |
| Milk_MPuse_g, Body_MPuse_g, Gest_MPuse_g, Scrf_MPuse_g, Fe_MPenduse_g, Ur_MPenduse_g | uso de PM para leite, ganho, gestação, descamação, fecal endógeno, urinário endógeno | g/d | Cap. 6/20 |
| Milk_MEuse, Body_MEuse, Gest_MEuse, An_NEgain, Gest_NEuse, Milk_NEuse | uso de EM / EL (leite, ganho, gestação) | Mcal/d | Cap. 2/20 |
| Fe_CP_g, Fe_OM, Dt_LgIn, Fe_N_g, Scrf_N_g, Ur_Nout_g | PB fecal; MO fecal; lignina ingerida; N fecal; N de descamação; N urinário | g/d; kg/d | Cap. 20 (partes anteriores) |
| An_WaIn | ingestão de água | kg/d | Cap. 9 |
| Dt_XxIn, Fd_XxIn_f, Fd_acXx_f, N_f | ingestão dietética do nutriente Xx; ingestão do nutriente pelo ingrediente f; CA do ingrediente f (g/g); nº de ingredientes | g/d, mg/d; g/g; n | biblioteca de alimentos (Cap. 19) |
| RumDevDisc_Clf | indicador de distúrbio de desenvolvimento ruminal em bezerro (definição não dada aqui) | 0/1 | ⚠ |

**Advertências gerais** (valem para todo o bloco):
1. O próprio livro usa nomes inconsistentes para a mesma grandeza (An_MilkProd / Mlk_Prod / Trg_MilkProd; An_BW / An_BW_NPr_3; Scrf_NP_g / Scrf_TP_g; Ur_N_g / Ur_Nout_g; An_NEm / An_NEmUse). Registrei como impresso e anotei a identidade provável.
2. Algumas equações impressas têm erros tipográficos aparentes (ver seção 10). Transcritas LITERALMENTE; a correção provável é indicada à parte, sem alterar a transcrição.
3. A errata de ago/2022 já está incorporada no texto-fonte (INSTRUCTIONS).

---

## 1. Papel no simulador
Esta parte é o "motor de contabilidade" do simulador: dado o que o animal ingere (energia, PB, AA, minerais, vitaminas — calculados nas partes A e B do Cap. 20) e o que produz (leite, ganho, gestação), calcula (a) exigências de mantença (energia e proteína/AA), (b) EM disponível, (c) balanços de EM, EL, PL, PM e AA, (d) produção permitida (ganho, leite, mudança de ECC) pela energia e proteína, (e) dejetos, água excretada, (f) eficiências fracionárias de uso de nutrientes, (g) exigências, balanço e produto retido de cada mineral e vitamina. É a camada que gera as SAÍDAS de exigência/balanço e as restrições do otimizador de dieta.

---

## 2. Entradas
Não há seção de entradas própria nesta parte; as entradas vêm das partes anteriores. As usadas diretamente aqui:

| Variável | Símbolo | Unidade | Definição | Faixa/valores típicos | Pág. |
|---|---|---|---|---|---|
| Estado fisiológico | An_StatePhys | texto | "Calf" ou outros; condiciona quase todas as equações de mineral | não informado | 503-519 |
| Paridade | An_Parity | n | 0 = novilha, >0 = vaca | — | 504, 512, 520 |
| PC, PC maduro, PCV, ganho | An_BW, An_BW_mature, An_EBW, An_BWgain, An_EBWgain | kg; kg/d | ver glossário | PC mínimo dos dados de avaliação 319 kg | vários |
| Dia de gestação | An_GestDay | d | gestação >190 d ativa efeitos de mineral (Mg, Na, Cl, K, Fe, Mn, Zn) | — | 512-519 |
| Produção de leite (real/alvo), proteína do leite | An_MilkProd, Trg_MilkProd, MlkNP_Milk | kg/d; g/g | — | — | 512-520 |
| Temperatura e limites TNZ | T, LCT, UCT | °C | Eq. 20-2/20-3 | — | 503 |
| Pasto/ambiente | Dt_PastIn, Dt_PastSuppIn, Env_DistParlor, Env_TripsParlor, Env_TopoParlor | kg/d; m; n; m | custos de locomoção | topografia: Suave 50, Moderado 200, Forte 500 m/d de subida | 503-504 |
| Monensina | "Dietary monensin" | sim/não | reduz perda de energia gasosa 5% | — | 507 |
| Concentrações da dieta | Dt_ME, Dt_NDF/An_NDF, Dt_K, Dt_Mg, Dt_Mg_Vitamin/Mineral, Dt_FA, Dt_LgIn etc. | vários | — | — | vários |
| CA de minerais por ingrediente | Fd_acCa, Fd_acPtot, Fd_acNa, Fd_acCl, Fd_acK, Fd_acCu, Fd_acFe, Fd_acMn, Fd_acZn | g/g | biblioteca de alimentos | — | 511-519 |
| Raça | Breed (Jersey, Holstein, Other) | texto | define An_kCal_l | — | 512 |
| Infusões | InfRum_DMIn, InfSI_DMIn, InfRum_FAIn | kg/d | infusão ruminal/intestinal | — | 505, 507 |

## 3. Saídas
(Resumo; cada uma com sua equação em 4.x.)

| Saída | Símbolo | Unidade | Pág. |
|---|---|---|---|
| NEm total de mantença | An_NEmUse | Mcal/d | 504 |
| MEm de mantença | An_MEmUse | Mcal/d | 504 |
| PL/PM de mantença; perdas endógenas | An_NPmUse_g, An_MPmUse_g, Ur_Nend_g, Fe_CPend … | g/d | 504-506 |
| EM ingerida, metano, perdas urinárias | An_MEIn, An_GasEOut, CH4out_g, CH4out_L, Ur_N_g, Ur_DEIn | Mcal/d; g/d; L/d | 506-507 |
| Proteína/AA/PM usados e exportados | An_NPxprt_g, An_NPprod_g, An_AAuse(i)_g, An_MPuse_g, An_Nuse_g | g/d | 507-508 |
| Balanços | An_MEbal, An_NEbal, An_NPbal_g, An_AAbal(i)_g | Mcal/d; g/d | 508 |
| Produção permitida | Body_Gain_ME_Allow, Body_Gain_MP_Allow, Milk_ME_Allow, Milk_MP_Allow, An_BCS_1Δ_d | kg/d; d | 508-509 |
| Dejetos | Man_Out, Man_VolSold, Man_Nout_g, Man_XxOut, Man_MacroMinOut_g, Man_MicroMinOut_mg, Man_WaOut | kg/d; g/d; mg/d | 509 |
| Água | An_WaOut_Insens, WaIn_Milk, ManWa_Milk | kg/d; kg/kg | 509-510 |
| Eficiências fracionárias | AnDE_AnGE … UrNout_DigNIn | Mcal/Mcal; g/g | 510-511 |
| Minerais: absorvido, exigência, balanço, produto | Abs_XxIn, An_Xx_req, An_Xx_bal, An_Xx_prod | g/d; mg/d | 511-519 |
| Vitaminas: exigência e balanço | An_VitX_req, An_VitX_bal | IU/d | 519-520 |

---

## 4. Equações

### 4.0 Contexto — Final de p.503 (Eq. 20-271 a 20-275; fora do intervalo formal, mas necessárias)

**Eq. 20-271** [p.503] — eficiência de conversão de PM em PL para ganho. Transcrição literal da tabela:
```
Kg_MP_NP (g/g) =
  An_StatePhys = Calf                                  :  0.70 - 0.532 * (An_BW / An_BW_mature) * 0.86
  An_Parity = 0 and An_BW_empty / An_BW_mature_empty > 0.12 :  0.64 - 0.3 * An_EBW / An_EBW_mature) * 0.86      [sic: ")" sem "(" correspondente]
  An_Parity > 0                                        :  Trg_MP_NP * 0.86
```
Texto: Kg_MP_NP não deve ser visto como a eficiência máxima alcançável (composição de AA da PM afeta a eficiência e não foi considerada). **Eficiência mínima fixada em 0.39** [p.503]. ⚠ parênteses: a leitura mais provável é (0.70 − 0.532×(BW/BW_mature))×0.86 e (0.64 − 0.3×EBW/EBW_mature)×0.86.

**Eq. 20-272** [p.503] — NEm sem estresse ambiental, An_NEmUse_NS (Mcal/d):
```
Calves: Dt_DMIn_LiquidFeed > 0              : 0.0769 * An_EBW^0.75
Calves: Dt_DMIn_LiquidFeed = 0              : 0.097 * An_BW^0.75
Heifers: Dt_DMIn_Milk = 0 & Parity = 0      : 0.10 * An_BW^0.75
Cows: Parity > 0                            : 0.10 * An_BW_NPr_3^0.75     [subscrito NPr_3 como impresso]
```
**Eq. 20-273** [p.503] — custo adicional de mantença por temperatura fora da TNZ, An_NEmUse_Env (Mcal/d):
```
LCT < T < UCT              : 0
T < LCT  & An_BW < 100     : 0.00201 * (LCT - T) * An_BW^0.75
T > UCT  & An_BW < 100     : 0.00201 * (T - UCT) * An_BW^0.75
```
⚠ O critério "An_BW < 100" é como impresso (parece estranho para vacas; não informado se há tratamento para BW ≥ 100 — o livro não diz; na tabela impressa, T fora da TNZ com BW ≥ 100 não tem linha → tratar como 0 por omissão? NÃO INFORMADO).

**Eq. 20-274** [p.503] — locomoção em pastejo, An_NEmUse_Graze (Mcal/d):
```
Dt_PastIn / Dt_DMIn < 0.005   : 0
Dt_PastIn / Dt_DMIn >= 0.005  : 0.0075 * An_BW^0.75 * (600 - 12 * Dt_PastSuppIn) / 600
```
Dt_PastIn, Dt_PastSuppIn em kg MS/d (pastagem e não pastagem). Assume topografia plana.

**Eq. 20-275** [p.503] — locomoção até a sala de ordenha, An_NEmUse_Parlor (Mcal/d):
```
An_NEmUse_Parlor = 0.00035 * (Env_DistParlor / 1000) * Env_TripsParlor * An_BW
```
Env_DistParlor em m (ida e volta); Env_TripsParlor = nº de ordenhas (viagens); superfície plana.

### 4.1 Energia de mantença (p.504)

**Eq. 20-276** [p.504] (corrigido pela imagem: coeficiente 0.0067; o OCR leu 0.006)
```
An_NEmUse_Topo (Mcal/d) = 0.0067 * (Env_TopoParlor / 1,000) * An_BW
```
Env_TopoParlor = subida total diária (m) durante pastejo e trânsito sala↔lote/piquete (só subida; descida não subtraída). Tabela de estimativas por topografia (p.504, sem número):

| Nível | Distância vertical escalada |
|---|---|
| Suave | 50 m/d |
| Moderado | 200 m/d |
| Forte | 500 m/d |

A subida também pode ser estimada de monitores de atividade, imagens de satélite (movimento aleatório no pasto + canalizado de/para ordenha) ou GPS.

**Eq. 20-277** [p.504]
```
An_NEmUse_Act (Mcal/d) = An_NEmUse_Graze + An_NEmUse_Parlor + An_NEmUse_Topo
```
**Eq. 20-278** [p.504]
```
An_NEmUse (Mcal/d) = An_NEmUse_NS + An_NEmUse_Env + An_NEmUse_Act
```
**Eq. 20-279** [p.504]
```
An_MEmUse (Mcal/d) = An_NEm / Km_ME_NE
```
(impresso "An_NEm"; identidade provável: An_NEmUse da Eq. 20-278.)

**Eq. 20-280** [p.504] — bezerros só com líquido:
```
Km_ME_NE(ClfLiq) = 0.718
```
**Eq. 20-281** [p.504] — bezerros só com sólido (corrigido pela imagem: termos verificados):
```
Km_ME_NE(ClfDry) = 1.1104 - (0.0946 * Dt_ME) + (0.0065 * Dt_ME^2) - 0.7783 / Dt_ME
```
Dt_ME em Mcal/kg MS (unidade não citada; implícita). As duas eficiências parciais são ponderadas pela quantidade de alimento líquido e seco consumido para dar a eficiência de mantença total do bezerro (a fórmula de ponderação NÃO é dada; ela entra como `Km_NE` na Eq. 20-282).

**Eq. 20-282** [p.504] — Km_ME_NE (Mcal/Mcal), eficiência de mantença total (constante p/ novilhas e vacas, independe da dieta):
```
An_StatePhys = "Calf" and An_ME_ClfDry > 0 and Dt_DMIn_ClfLiq = 0 : Km_NE
An_StatePhys = "Calf" and Dt_DMIn_ClfLiq = 0                         : 0.69
An_StatePhys != "Calf" & An_Parity = 0                               : 0.63
An_Parity > 0                                                         : 0.66
```
(Verificado a 300 dpi.) ⚠ A linha 1 vem escrita como "Km_NE" (ponderada, não detalhada) e a ordem das linhas 1-2 como impresso.

### 4.2 Proteína e AA de mantença (pp.504-506)

**Eq. 20-283** [p.504]  `Scrf_CP_g (g/d) = 0.20 * An_BW^0.60`  — deposição líquida de PB em descamação.
**Eq. 20-284** [p.504]  `Scrf_TP_g (g/d) = Scrf_CP_g * 0.86`  — PVer em descamação (no texto chamada Scrf_NP_g; ⚠ Scrf_TP_g ≡ Scrf_NP_g nas equações seguintes).
**Eq. 20-285** [p.504]  `Scrf_TP (kg/d) = Scrf_TP_g / 1,000`
**Eq. 20-286** [p.504]
```
Scrf_AA(i)_g (g/d) = Scrf_NP_g * AA(i)_NPScrf / 100
```
AA(i)_NPScrf = % do AA i na proteína de descamação (Tabela 6-5).

**Perdas endógenas urinárias de N** (ureia, 3-metil-histidina [3MH], derivados de purina [PD], creatinina [Creatn], creatina [Creat], ácido hipúrico [Hipp]):

**Eq. 20-287** [p.505]  `Ur_Nend_Urea_g (g/d) = 0.010 * An_BW`
**Eq. 20-288** [p.505]  `Ur_Nend_Creatn_g (g/d) = 0.00946 * An_BW`
**Eq. 20-289** [p.505]  `Ur_Nend_Creat_g (g/d) = Ur_Nend_Creatn_g * 0.37`
**Eq. 20-290** [p.505]  `Ur_Nend_PD_g (g/d) = 0.0271 * An_BW^0.75`
**Eq. 20-291** [p.505]  `Ur_Nend_3MH_g (g/d) = (7.82 + 0.55 * An_BW) * (3 * 14) / 169 / 1,000`
**Eq. 20-292** [p.505]
```
Ur_Nend_sum_g (g/d) = (Ur_Nend_Urea_g + Ur_Nend_Creatn_g + Ur_Nend_Creat_g + Ur_Nend_PD_g + Ur_Nend_3MH_g) / (1 - 0.46)
```
**Eq. 20-293** [p.505]  `Ur_Nend_Hipp_g (g/d) = Ur_Nend_sum_g * 0.46`
**Eq. 20-294** [p.505]  `Ur_Nend_g (g/d) = 0.053 * An_BW`   — "usado para cálculos daqui por diante" (aproximação global; as Eq. 20-287..293 são a decomposição).
Assume-se perda de PVer endógena líquida urinária com 16% de N e que todo Ur_Nend deriva de PVer/AAs.
**Eq. 20-295** [p.505]
```
Ur_NPend_g (g/d) =
  An_StatePhys = "Calf"   : 2.75 * An_BW^0.50
  An_StatePhys != "Calf"  : Ur_Nend_g * 6.25
```
**Eq. 20-296** [p.505] (corrigido pela imagem: fator 0.001)  `Ur_NPend (kg/d) = Ur_NPend_g * 0.001`
**Eq. 20-297** [p.505]  `Ur_EAAend_g (g/d) = 0.010 * An_BW * 6.25`  — fração da perda urinária endógena que vem só de AAE metabolizável (ureia e 3MH).
**Eq. 20-298** [p.505]  (i = AA individual, exceto His)
```
Ur_AAend(i)_g (g/d) = Ur_EAAend_g * AA(i)_NPGain / 100
```
(concentração do AA na proteína corporal — Tabela 6-5.)
**Eq. 20-299** [p.505]  (His, inclui contribuição da 3MH)
```
Ur_AAend(His)_g (g/d) = Ur_NP_g * AA(His)_NPGain / 100 + Ur_Nend_3MH_g * 169 / (3 * 14)
```
⚠ Impresso "Ur_NP_g" (identidade provável: Ur_EAAend_g ou Ur_NPend_g; livro não esclarece — ver 10.3).

**Perdas endógenas fecais** (metabólico):
**Eq. 20-300** [p.505] (corrigido pela imagem)
```
Fe_CPend (kg/d) = (12.0 + 0.12 * An_NDF) * (Dt_DMIn + InfRum_DMIn + InfSI_DMIn) / 1,000
```
**Eq. 20-301** [p.506]  `Fe_Nend (kg/d) = Fe_CPend * 0.16`
**Eq. 20-302** [p.506]  `Fe_NPend_g (g/d) = Fe_CPend * 0.73`   (73% do Fe_CPend é PVer) ⚠ unidade: Fe_CPend está em kg/d; o resultado é rotulado g/d sem fator 1,000 (como impresso).
**Eq. 20-303** [p.506]
```
Fe_AAend(i)_g (g/d) = Fe_NP_g * AA(i)_NPMFP / 100
```
(AA(i)_NPMFP: Tabela 6-5; ⚠ Fe_NP_g impresso, identidade provável Fe_NPend_g.)

**Uso líquido de PL e PM de mantença:**
**Eq. 20-304** [p.506]  `An_NPmUse_g = Scrf_NP_g + Fe_NPend_g + Ur_NPend_g`
**Eq. 20-305** [p.506]
```
An_MPmUse_g (g/d) = (An_NPmUse_g - Ur_NPend_g) / Km_MP_NP + Ur_NPend_g
```
**Eq. 20-306** [p.506]  `Km_MP_NP (g/g) = 0.69`  — eficiência-alvo PM→PL de mantença (assumida igual à de proteínas secretadas). Ur_NPend_g é tratado como uso de PM com eficiência 1 (AAs do sangue para urina sem perda de conversão).

### 4.3 Aporte de EM (p.506-507)
**Eq. 20-307** [p.506] — transcrição literal:
```
An_MEIn (Mcal/d) =
  An_StatePhys = "Calf" and Dt_DMIn_ClfLiq > 0 :  An_DEIn_base_ClfLiq * 0.96 + An_DEIn_base_ClfDry * K_DE_ME_ClfDry
  An_StatePhys != "Calf"                        :  An_DEIn - An_GasEIn - Ur_DEIn
```
An_DEIn_base = ED não ajustada para DMIn; K_DE_ME_ClfDry = eficiência de conversão de ED em EM (do alimento sólido do bezerro). (Impresso "An_GasEIn" na linha 2, enquanto a saída é An_GasEOut: ⚠ identidade provável.)

**Equação adicionada posteriormente, NÃO NUMERADA** [p.506] (verificada a 300 dpi):
```
K_DE_ME_ClfDry (Mcal/Mcal) =
  An_StatePhys = "Calf" and Dt_DMIn_ClfLiq > 0.015 * An_BW and RumDevDisc_Clf = 1 :  0.93
  An_StatePhys = "Calf" and RumDevDisc_Clf = 1                                     :  0.93 * 0.90
```
⚠ Como impresso; o que acontece com RumDevDisc_Clf = 0 e não definido; leitura provável: 0.93 é o valor padrão e 0.93×0.90 se há distúrbio de desenvolvimento ruminal. NÃO CONFIRMADO.

**Eq. 20-308** [p.506] — N urinário (calcular APÓS as seções de uso de PL):
```
Ur_N_g (g/d) = ( An_CPIn * 1,000 - Fe_CP_g - Scrf_NP_g - Fec_NP_Metab_g - Milk_NP_g - Body_NPgain_g - Gest_NP_g ) / 6.25
```
**Eq. 20-309** [p.506] (corrigido pela imagem: 0.0143; OCR leu 0.014/0.01433)  `Ur_DEIn (Mcal/d) = 0.0143 * Ur_N_g`
Texto [p.506]: "Pela Equação 20-308, o uso de PL deve ser calculado antes que Ur_N_g possa ser definido. Assim, no modelo, toda a seção EM deve ser colocada APÓS as seções que definem o uso do PL (abaixo). As equações são colocadas aqui por motivos organizacionais."

**Eq. 20-310** [p.507] — perda de energia gasosa (metano), An_GasEOut (Mcal/d). Transcrição literal (verificada a 250 dpi):
```
Calves: An_BW <= 0.16 * An_BW_Mature                                   : 0
Heifers: An_BW > 0.16 * AnBWMature and An_Parity = 0                    : -0.038 + 0.051 * An_GEIn + 0.0091 * An_NDF
Dry Cow: An_Parity > 0 and An_MilkProd = 0                              : 0.69 + 0.053 * An_GEIn - 0.07 * ((Dt_FAIn + InfRum_FAIn) / (Dt_DMIn + InfRum_DMIn)) * 100
Lactating Cow: An_MilkProd > 0                                          : 0.294 * (Dt_DMIn + InfRum_DMIn) - 0.347 * (Dt_FA + InfRum_FAIn / InfRum_DMIn * 100) + 0.0409 * An_DigNDF
```
⚠ Linha "Lactating Cow": impressa assim (Dt_FA aparece sem "In" e a fração InfRum_FAIn/InfRum_DMIn × 100 está agrupada com "+" dentro do parêntese); transcrição literal. Provável intenção: 0.294×DMI − 0.347×(% AG na MS total) + 0.0409×An_DigNDF. A unidade das duas expressões em An_GEIn (Mcal/d) e DMI (kg/d) é a do Cap. 20 (partes anteriores; não informada aqui).
**Eq. 20-311** [p.507]
```
An_GasEOut (Mcal/d) =  No monensin : An_GasEOut ;  Dietary monensin : An_GasEOut * 0.95
```
**Eq. 20-312** [p.507]  `CH4out_g (g/d) = An_GasEOut / (55.5 / 4.184) * 1,000`   (⚠ texto diz 55.6 MJ/kg; equação impressa 55.5 — registrar a divergência; fatores: 4.184 MJ/Mcal)
**Eq. 20-313** [p.507]  `CH4out_L (L/d) = CH4out_g / 1,000 * 1,497`  (1,497 L/kg)
**Eq. 20-314** [p.507]  `CH4g_Milk (g/kg) = CH4out_g / Mlk_Prod`
**Eq. 20-315** [p.507]  `CH4L_Milk (L/kg) = CH4out_L / Mlk_Prod`
**Eq. 20-316** [p.507]  `An_ME (Mcal/kg DM) = An_MEIn / An_DMIn`
**Eq. 20-317** [p.507]  `AnME_DE (Mcal/Mcal) = An_MEIn / An_DEIn`
Texto [p.507]: as equações acima valem para animais DESMAMADOS de todas as idades; "Equações alternativas de aporte de energia são usadas para bezerros alimentados com leite" (não apresentadas neste bloco).

### 4.4 Balanço de energia, proteína e AA (pp.507-508)
**Eq. 20-318** [p.507]
```
An_NPxprt_g (g/d) = Milk_NP_g + BodyNPgain_g + Scrf_NP_g + Fe_NPend_g + Ur_NPend_g
```
(proteína total secretada do corpo e crescimento corporal)
**Eq. 20-319** [p.507]  `An_NPprod_g (g/d) = An_NPmilk_g + Gest_NPgain_g`
**Eq. 20-320** [p.507]  `AnNPxprt_g (g/d) = An_NPxprt_g * 0.16`   (⚠ rótulo/unidade como impresso: multiplicar PL por 0.16 dá N, não PL; identidade provável An_Nxprt_g)
**Eq. 20-321** [p.507]
```
An_AAuse(i)_g (g/d) = Gest_AA(i)_g + Mlk_AA(i)_g + Bod_AAgain(i)_g + Scrf_AA(i)_g + Fe_AAend(i)_g + Ur_AAend(i)_g
```
(impresso "Mik_AA" = Milk_AA(i)_g.)
**Eq. 20-322** [p.507]
```
An_MPuse_g (g/d) = Gest_MPuse_g + Milk_MPuse_g + Body_MPuse_g + Scrf_MPuse_g + Fe_MPenduse_g + Ur_MPenduse_g
```
**Eq. 20-323** [p.508]  `An_Nuse_g (g/d) = An_NPuse_g * 0.16`
**Eq. 20-324** [p.508]  `An_NEprod_Avail (Mcal/d) = An_NEIn - An_NEmUse`
**Eq. 20-325** [p.508]  `An_MEprod_Avail (Mcal/d) = An_MEIn - An_MEmUse`
**Eq. 20-326** [p.508]  `An_MEbal (Mcal/d) = An_MEIn - An_MEmUse - Body_MEuse - Gest_MEuse - Milk_MEuse`
**Eq. 20-327** [p.508]  `An_NEbal (Mcal/d) = An_NEIn - An_NEmUse - An_NEgain - Gest_NEuse - Milk_NEuse`
**Eq. 20-328** [p.508]
```
An_NPbal_g (g/d) = An_MPIn_g - Gest_NP_g / Ky_MP_NP - Mlk_NP_g / Kx_MP_NP - Body_NPgain_g / Kg_MP_NP - Scrf_NP_g / Kx_MP_NP - Fe_NPend_g / Kx_MP_NP - Ur_NPend_g
```
**Eq. 20-329** [p.508]
```
An_AAbal(i)_g (g/d) = Abs_AA(i)_g - Gest_AA(i)_g - Mlk_AA(i)_g - Body_AAgain(i)_g - Scrf_AA(i)_g - Fe_AAend(i)_g - Ur_AAend(i)_g
```

### 4.5 Estimativas de produção permitida (pp.508-509)
Texto [p.508]: energia e proteína disponíveis podem ser particionadas em ganho, leite ou gestação; a gestação "parece ser amplamente prescrita dentro dos limites normais" e é ignorada nesses cenários. Rearranja-se 20-327 e 20-328 por conservação de massa, com taxas constantes para as demais funções e eficiências-alvo de PM→PL. A disponibilidade de nutrientes não é o único determinante da produção: estas predições são "guias na melhor das hipóteses"; as predições por superfície de resposta (Milk_NP e Milk_Fat) refletem melhor as mudanças esperadas e devem ser a referência de expectativa.

**Eq. 20-330** [p.508]  `An_MEavail_Gain (Mcal/d) = An_MEIn - An_MEmUse - Gest_MEuse - Milk_MEuse`
**Eq. 20-331** [p.508]  `Body_Gain_ME_Allow (kg/d) = An_MEavail_Gain / (Kg_ME_RE * NEgain_BWgain)`   (ganho de Frm e Rsrv proporcional ao ganho corporal, conforme a proporção de ganho de Frm e Rsrv de entrada)
**Eq. 20-332** [p.508]  `BodyFat_BCS (kg/BCS Unit) = An_BW * 0.098`   (1 unidade de ECC = 9.8% do PC)
**Eq. 20-333** [p.508]  `An_BCS_1Δ_d (d) = BodyFat_BCS / Body_Gain_ME_Allow`   (dias para mudar 1 unidade de ECC supondo toda a energia extra nas reservas)
**Eq. 20-334** [p.509]
```
An_MPavail_Gain (kg/d, rótulo impresso) = An_MPIn - Gest_MPuse - Milk_MPuse_Trg - Scrf_MPuse - Fe_NPenduse - Ur_NPenduse
```
(⚠ unidade impressa kg/d mas MP está em g/d; "Fe_NPenduse/Ur_NPenduse" impressos, vs. "Fe_MPenduse/Ur_MPenduse" na Eq. 20-337.)
**Eq. 20-335** [p.509]  `Body_Gain_MP_Allow (kg/d) = An_MPavail_Gain / (Kg_MP_NP * GainNP_Gain)`  (assume composição de AAE da PM adequada e conversão PM→PL do leite na eficiência-alvo)
**Eq. 20-336** [p.509]  `An_MEavail_Milk (Mcal/d) = An_MEIn - An_MEmUse - Body_MEuse - Gest_MEuse`
**Eq. 20-337** [p.509]  `An_MPavail_Milk_g (kg/d, rótulo impresso) = An_MPIn - Gest_MPuse - Body_MPuse - Scrf_MPuse - Fe_MPenduse - Ur_MPenduse`
**Eq. 20-338** [p.509]  `Milk_ME_Allow (kg/d) = An_MEavail_Milk / (Kl_ME_NE * MilkNE_Milk)`
**Eq. 20-339** [p.509]  `Milk_MP_Allow (kg/d) = An_MPavail_Milk / (Kl_MP_NP,Trg * Trg_MilkTPp / 100)`
Texto: o teor de proteína do leite predito pode ser usado em vez do valor-alvo informado pelo usuário na Eq. 20-339.
**AVISO do livro [p.523]**: as produções de leite suportadas por EM e PM (Eq. 20-338/339) "são fortemente encorajados a não fazer uso dessas predições, pois claramente são muito tendenciosas" (ver Tabela 20-16 e seção 9). Use Milk_NP e Milk_Fat (Eq. 20-185/215/216, partes anteriores) para expectativas de produção.

### 4.6 Dejetos (p.509)
**Eq. 20-340** [p.509]  `Man_Out (kg Wet/d) = -28.3 + 3.6 * An_DMIn + 12.4 * Dt_K`   (Dt_K em % da MS — ⚠ unidade não informada nesta página)
**Eq. 20-341** [p.509]  `Man_VolSold (kg/d) = Fe_OM - Dt_LgIn + Ur_Nout_g / (0.16 * 1,000)`
**Eq. 20-342** [p.509]  `Man_Nout_g (g/d) = Ur_Nout_g + Fe_N_g + Scrf_N_g`
**Eq. 20-343** [p.509]  `Man_XxOut (g/d) = Dt_XxIn - An_Xx_prod`   (Xx = cada mineral; produção em dejetos = fezes + urina, calculada por diferença entre ingestão dietética e retido no produto)
**Eq. 20-344** [p.509]  `Man_MacroMinOut_g (g/d) = Man_Ca_out + Man_P_out + Man_Mg_out + Man_K_out + Man_Na_out + Man_Cl_out`
**Eq. 20-345** [p.509]  `Man_MicroMinOut_mg (mg/d) = Man_CuOut + Man_FeOut + Man_MnOut + Man_ZnOut`

### 4.7 Água e eficiências (pp.509-511)
**Eq. 20-346** [p.509]
```
Man_WaOut (kg/d) = Man_Out - Fe_OM - Ur_Nout_g / (0.45 * 1,000) - Man_MacroMinOut_g / 1,000 - Man_MicroMinOut_mg / 1,000,000
```
**Eq. 20-347** [p.509]  `An_WaOut_Insens (kg/d) = An_WaIn - Mlk_Prod - Man_WaOut`  (perda insensível de água)
**Eq. 20-348** [p.510]  `WaIn_Milk (kg/kg) = An_WaIn / Mlk_Prod`
**Eq. 20-349** [p.510]  `ManWa_Milk (kg/kg) = Man_WaOut / Mlk_Prod`

Eficiências de transferência de energia [p.510]:
**Eq. 20-350**  `AnDE_AnGE (Mcal/Mcal) = An_DEIn / An_GEIn`
**Eq. 20-351**  `AnNE_AnDE (Mcal/Mcal) = An_NEIn / An_DEIn`
**Eq. 20-352**  `AnNE_AnME (Mcal/Mcal) = An_NEIn / An_MEIn`

Eficiências de uso de dieta e PM [p.510]:
**Eq. 20-353**  `AnNP_DtCP (g/g) = An_NPuse / An_CPIn`
**Eq. 20-354**  `AnNP_AnMPa (g/g) = An_NPuse / An_MPIn`
**Eq. 20-355**
```
AnNP_AnMPt (g/g) = ( Milk_NP_g + Body_NPgain_g + Scrf_NP_g + Fe_NPend_g + Gest_NP_g / Ky_MP_NP ) / ( An_MPIn - Ur_NPend )
```
**Eq. 20-356**  `AnNPexprt_DtCP (g/g) = An_NPexprt / An_CPIn`
**Eq. 20-357**  `AnNPexprt_AnMP (g/g) = An_NPexprt / An_MPIn`
**Eq. 20-358**  `MilkNP_AnCP (g/g) = Milk_NP / An_CPIn`
**Eq. 20-359**  `MilkNP_AnMP (g/g) = Milk_NP / An_MPIn`
**Eq. 20-360**  `BodyNPgain_AnMP (g/g) = Body_NPgain / An_MPIn`
**Eq. 20-361**  `GestNP_AnMP (g/g) = Gest_NP / An_MPIn`
Texto [p.510]: a conversão fracionária de PM em PL endógena urinária é 1 → por isso Ur_NPend é subtraído de An_NP e de An_MPIn na Eq. 20-355; o uso integral em apoio à gestação também é considerado (a ineficiência de deposição ocorre fora do animal). Ajuste semelhante poderia valer para as demais equações usando An_MPIn, mas NÃO foi feito. **O valor da Eq. 20-355 é usado para comparação com a eficiência-alvo do Cap. 6.**

Eficiências de AA [p.510-511] (a = AA essencial):
**Eq. 20-362** [p.510]  `AnAA(a)_DtAA(a) (g/g) = An_AAuse(a) / Dt_AAIn(a)`
**Eq. 20-363** [p.510]
```
AnAAxprt(a)_AbsAAt(a) (g/g) = ( Mlk_AA(a)_g + Bod_AAgain(a)_g + Scrf_AA(a)_g + Fe_AAend(a)_g ) / ( Abs_AA(a) - Ur_AAend_a - ( Gest_AA(a)_g / Ky_MP_NP ) )
```
**Eq. 20-364** [p.511]  `AnAAa(a)_AbsAA(a) (g/g) = An_AAuse(a) / Abs_AA(a)`
**Eq. 20-365** [p.511]  `MilkAA(a)_DtAA(a) (g/g) = Milk_AA(a) / Dt_AAIn(a)`
**Eq. 20-366** [p.511]  `MilkAA(a)_AbsAA(a) (g/g) = Milk_AA(a) / Abs_AA(a)`
**Eq. 20-367** [p.511]  `BodyAA(a)_AbsAA(a) (g/g) = Body_AAgain(a) / Abs_AA(a)`
**Eq. 20-368** [p.511]  `GestAA(a)_AbsAA(a) (g/g) = Gest_AA(a) / Abs_AA(a)`
**Eq. 20-369** [p.511]  `UrNout_DigNIn (g/g) = Ur_Nout_g / (An_DigCPtIn * 1,000 / 6.25)`
Texto: as eficiências de uso de cada EAA absorvido para secreção de proteína e proteína corporal (Eq. 20-363) supõem eficiência 1 para AAs endógenos urinários e eficiência mais baixa para gestação; devem ser comparadas com as eficiências-alvo do Cap. 6. "Uma série de eficiências fracionárias adicionais também são calculadas para exibição em relatórios, mas não apresentadas aqui" [p.511].

### 4.8 Minerais (pp.511-519)

**Estrutura geral [p.511]**: coeficientes de absorção (CAs; `Fd_acXx`, g/g) foram avaliados para macrominerais e alguns microminerais. Para estes, o aporte absorvido por ingrediente (`Fd_absXxIn`) é somado em `Abs_XxIn` e comparado à exigência de mineral absorvido (`An_Xx_req`). Para os microminerais restantes (S, Co, I, Se) e vitaminas, a exigência é em termos de ingestão dietética (`Dt_XxIn`). Exigências fatoriais: mantença (`_m`), crescimento (`_g`/`_gr`), gestação (`_y`), lactação (`_l`) → `_req`; balanço `_bal`; retido no produto `_prod`.
Minerais baseados em absorvido: Ca, P, Mg, Na, K, Cl, Co (ver 4.8 Co: tratado como ingestão), Cu, Fe, Mn, Zn; CAs por ingrediente vêm da biblioteca de alimentos (`Fd_acXx`).

**Bezerros (An_StatePhys = "Calf")**: onde a exigência de alguns minerais é baseada na concentração da dieta, o CA foi definido como 1 (para uma estrutura comum; não implica absorção completa). Para bezerros não desmamados (An_StatePhys = "Calf" e Dt_DMIn_ClfLiq > 0) os valores por ingrediente geralmente NÃO são usados; no lugar, CAs dietéticos [p.511]:

| Mineral | Alimento líquido | Alimento sólido |
|---|---|---|
| Ca | 1.0 | 0.60 |
| P | 1.0 | 0.75 |
| Mg | 1.0 | 0.26 |
| K | 1.0 | 1.0 |
| Na | 1.0 | 1.0 |
| Cl | 1 | 0.92 |
| Cu | 0.10 (único) | — |
| Fe | 0.10 (único) | — |
| Mn | 0.005 (único) | — |
| Zn | 0.20 (único) | — |

⚠ Divergências texto x equações: Mn dieta sólida do texto = 0.005, mas Eq. 20-467 imprime 0.05; Fe texto = 0.10, mas Eq. 20-457 só tem as linhas 1 / Fd_acFe (sem 0.10); as equações de Ca e P (20-370, 20-381) não trazem o ramo de bezerro (está só no texto). Seguir texto ou equação: decisão do dev/registrar.

#### Cálcio (g/d)
**Eq. 20-370** [p.511]  `Fd_absCaIn_f (g/d) = Fd_CaIn_f * Fd_acCa_f`
**Eq. 20-371** [p.511]  `Abs_CaIn (g/d) = SUM_{f=1..N_f} Fd_absCaIn_f`
**Eq. 20-372** [p.511] — Ca de bezerros com dieta líquida (corrigido pela imagem: expoente -0.139)
```
An_Ca_Clf (g/d) = ( (0.0127 * An_EBW) + (14.4 * An_EBW^-0.139 * An_EBWgain) ) / 0.73
```
**Eq. 20-373** [p.512]  `Fe_Ca_m (g/d) = 0.9 * An_DMIn`
**Eq. 20-374** [p.512]  `An_Ca_g (g/d) = (9.83 * An_BWmature^0.22 * An_BW^-0.22) * An_BWgain`
**Eq. 20-375** [p.512] — gestação (conferido a 300 dpi)
```
An_Ca_y (g/d) = ( 0.0245 * e^((0.05581 - 0.00007 * An_GestDay) * An_GestDay) - 0.0245 * e^((0.05581 - 0.00007 * (An_GestDay - 1)) * (An_GestDay - 1)) ) * An_BW / 715
```
**Eq. 20-376** [p.512] — Ca na lactação (g/d; pode ser predito pelo volume de leite ou pela proteína do leite)
```
An_Ca_l (g/d) =
  An_MilkProd = 0                         : 0
  An_MilkProd > 0   (or) MlkNP_Milk > 0   : An_kCa_l * Trg_MilkProd   (or)   (0.295 + 0.239 * MlkNP_Milk) * An_MilkProd
```
Leitura: duas alternativas na mesma linha — por volume (kCa × leite-alvo) ou, se MlkNP_Milk > 0, por proteína. ⚠ unidade de MlkNP_Milk: para dar ≈1.0-1.1 g Ca/kg o termo precisa estar em % (ex. 3.2), enquanto na Eq. 20-389 aparece "× 100" (fração). Não informado pelo livro.
**Eq. 20-377** [p.512]  `An_kCa_l (g/L) = Jersey 1.17 ; Holstein 1.03 ; Other 1.17`  (g Ca/L de leite, por raça)
**Eq. 20-378** [p.512]
```
An_Ca_req (g/d) =  An_StatePhys = "Calf" and Dt_DMIn_ClfLiq > 0 : An_Ca_Clf ;  else : Fe_Ca_m + An_Ca_g + An_Ca_y + An_Ca_l
```
**Eq. 20-379** [p.512]  `An_Ca_bal (g/d) = Abs_CaIn - An_Ca_req`
**Eq. 20-380** [p.512]  `An_Ca_prod (g/d) = Abs_Ca_y + An_Ca_l + An_Ca_g`   (⚠ "Abs_Ca_y" impresso; provável An_Ca_y)

#### Fósforo (g/d)
**Eq. 20-381** [p.512]  `Fd_absPIn_f (g/d) = Fd_PIn_f * Fd_acPtot_f`
**Eq. 20-382** [p.512]  `Abs_PIn (g/d) = SUM_{f=1..N_f} Fd_absPIn_f`
**Eq. 20-383** [p.512]  `An_P_Clf (g/d) = ( 0.0118 * An_EBW + (5.85 * An_EBW^-0.027 * An_EBWgain) ) / 0.65`
**Eq. 20-384** [p.512]  `Ur_P_m = 0.0006 * An_BW`   (g/d)
**Eq. 20-385** [p.512]  `Fe_P_m (g/d) = Parity 0 : 0.8 * An_DMIn ;  Parity 1+ : 1.0 * An_DMIn`
**Eq. 20-386** [p.513]  `An_P_m (g/d) = Ur_P_m + Fe_P_m`
**Eq. 20-387** [p.513] (conferido a 300 dpi)  `An_P_g (g/d) = (1.2 + (4.635 * An_BWmature^0.22 * An_BW^-0.22)) * An_BWgain`
**Eq. 20-388** [p.513] (conferido a 300 dpi)
```
An_P_y (g/d) = ( 0.02743 * e^((0.05527 - 0.000075 * An_GestDay) * An_GestDay) - 0.02743 * e^((0.05527 - 0.000075 * (An_GestDay - 1)) * (An_GestDay - 1)) ) * An_BW / 715
```
(A linha do expoente no impresso está tipograficamente embaralhada; a forma acima segue o paralelo com a Eq. 20-375 e com a segunda linha, que está clara.)
**Eq. 20-389** [p.513]  `An_P_l (g/d) = (0.48 + 0.13 * MlkNP_Milk * 100) * An_MilkProd`
**Eq. 20-390** [p.513] (se proteína do leite desconhecida)  `An_P_l (g/d) = 0.09 * An_MilkProd`
**Eq. 20-391** [p.513]  `An_P_req (g/d) = Calf & Dt_DMIn_ClfLiq > 0 : An_P_Clf ;  else : An_P_m + An_P_g + An_P_y + An_P_l`
**Eq. 20-392** [p.513]  `An_P_bal (g/d) = Abs_PIn - An_P_req`
**Eq. 20-393** [p.513]  `An_P_prod (g/d) = An_P_y + An_P_g + An_P_l`
**Eq. 20-394** [p.513]  `Fe_P_g (g/d) = Dt_PIn - An_P_l - An_P_gr - Ur_P_m`   (⚠ impresso An_P_gr (provável An_P_g); não subtrai An_P_y; "Fe_P_g" = P fecal)

#### Magnésio (g/d)
Texto [p.513]: a absorção de Mg de fontes inorgânicas é afetada pelo K da dieta; o Mg dos ingredientes da categoria vitaminas/minerais é somado e o CA do Mg é calculado a partir de Dt_K.
**Eq. 20-395** [p.513] (conferido a 300 dpi; transcrição literal)
```
Dt_acMg (rótulo g/d; na verdade g/g) =
  An_StatePhys = "Calf" and Dt_DMIn_ClfLiq > 0 : 1
  An_StatePhys = "Calf" and Dt_DMIn_ClfLiq = 0 : 0.26
  else : ( (44.1 - 5.42 * ln(Dt_K * 10) - 0.08) * (Dt_Mg_Vitamin/Mineral / Dt_Mg) * 100 ) / 100
```
⚠ Estrutura impressa: parênteses grandes envolvem "44.1 − 5.42 × ln(Dt_K×10) − 0.08"; depois "× Dt_Mg_Vitamin/Mineral / Dt_Mg × 100"; tudo ÷ 100. A leitura provável do autor é 44.1 − 5.42×ln(Dt_K×10) − 0.08×(Mg de vit/min ÷ Dt_Mg ×100), tudo ÷100 (CA fracionário). NÃO CONFIRMADO — conferir com o código R oficial.
**Eq. 20-396** [p.513]  `Abs_MgIn (g/d) = Dt_acMg * Dt_MgIn`
**Eq. 20-397** [p.513]  `An_Mg_Clf (g/d) = ( 0.0035 * An_EBW + (0.60 * An_EBW^-0.036 * An_EBWgain) ) / 0.30`
**Eq. 20-398** [p.514]  `Ur_Mg_m = 0.0007 * An_BW`
**Eq. 20-399** [p.514]  `Fe_Mg_m = 0.3 * An_DMIn`
**Eq. 20-400** [p.514]  `An_Mg_m = Ur_Mg_m + Fe_Mg_m`
**Eq. 20-401** [p.514]  `An_Mg_g = 0.45 * An_BWgain`
**Eq. 20-402** [p.514]  `An_Mg_y = An_GestDay <= 190 : 0 ;  An_GestDay > 190 : 0.3 * An_BW / 715`
**Eq. 20-403** [p.514]  `An_Mg_l = 0.11 * An_MilkProd`
**Eq. 20-404** [p.514]  `An_Mg_req = Calf & Dt_DMIn_ClfLiq > 0 : An_Mg_Clf ;  else : An_Mg_m + An_Mg_g + An_Mg_y + An_Mg_l`
**Eq. 20-405** [p.514]  `An_Mg_bal = Abs_MgIn - An_Mg_req`
**Eq. 20-406** [p.514]  `An_Mg_prod = An_Mg_g + An_Mg_y + An_Mg_l`

#### Sódio (g/d)
**Eq. 20-407** [p.514]  `Fd_absNaIn_f = Fd_NaIn_f * Fd_acNa_f`
**Eq. 20-408** [p.514]  `Abs_NaIn = SUM_{f=1..N_f} Fd_absNaIn_f`
**Eq. 20-409** [p.514]  `An_Na_Clf = ( 0.00637 * An_EBW + (1.508 * An_EBW^-0.045 * An_EBWgain) ) / 0.24`
**Eq. 20-410** [p.514]  `Fe_Na_m = 1.45 * An_DMIn`
**Eq. 20-411** [p.514]  `An_Na_g = 1.4 * An_BWgain`
**Eq. 20-412** [p.514]  `An_Na_y = An_GestDay <= 190 : 0 ;  An_GestDay > 190 : 1.4 * An_BW / 715`
**Eq. 20-413** [p.514]  `An_Na_l = 0.4 * An_MilkProd`
**Eq. 20-414** [p.514]  `An_Na_req = Calf & Dt_DMIn_ClfLiq > 0 : An_Na_Clf ;  else : Fe_Na_m + An_Na_g + An_Na_y + An_Na_l`
**Eq. 20-415** [p.515]  `An_Na_prod = An_Na_g - An_Na_y - An_Na_l`   (⚠ sinais "−" como impresso; por analogia com 20-406/393 seria "+")
**Eq. 20-416** [p.515]  `An_Na_bal = Abs_NaIn - An_Na_req`
(Na: não há termo urinário de mantença; só fecal Fe_Na_m.)

#### Cloreto (g/d)
**Eq. 20-417** [p.515]  `Fd_absClIn_f = Fd_ClIn_f * Fd_acCl_f`
**Eq. 20-418** [p.515]  `Abs_ClIn = SUM_{f=1..N_f} Fd_absClIn_f`
**Eq. 20-419** [p.515] (corrigido pela imagem: fator 0.8, não "3X")
```
An_Cl_Clf = 0.8 * ( 0.00637 * An_EBW + (1.508 * An_EBW^-0.045 * An_EBWgain) ) / 0.24
```
**Eq. 20-420** [p.515]  `Fe_Cl_m = 1.11 * An_DMIn`
**Eq. 20-421** [p.515]  `An_Cl_gr = 1.0 * An_BWgain`   (nome impresso "An_Cl_gr"; nas Eq. 20-424/425 aparece "An_Cl_g")
**Eq. 20-422** [p.515]  `An_Cl_y = An_GestDay <= 190 : 0 ;  An_GestDay > 190 : 1.0 * An_BW / 715`
**Eq. 20-423** [p.515]  `An_Cl_l = 1.0 * An_MilkProd`
**Eq. 20-424** [p.515]  `An_Cl_req = Calf & Dt_DMIn_ClfLiq > 0 : An_Cl_Clf ;  else : Fe_Cl_m + An_Cl_g + An_Cl_y + An_Cl_l`
**Eq. 20-425** [p.515]  `An_Cl_prod = An_Cl_g - An_Cl_y - An_Cl_l`   (⚠ sinais como impresso)
**Eq. 20-426** [p.515]  `An_Cl_bal = Abs_ClIn - An_Cl_req`

#### Potássio (g/d)
**Eq. 20-427** [p.515]  `Fd_absKIn_f = Fd_KIn_f * Fd_acK_f`
**Eq. 20-428** [p.515]  `Abs_KIn = SUM_{f=1..N_f} Fd_absKIn_f`
**Eq. 20-429** [p.515]  `An_K_Clf = ( 0.0203 * An_EBW + (1.14 * An_EBW^-0.048 * An_EBWgain) ) / 0.13`
**Eq. 20-430** [p.515]  `Ur_K_m = Trg_MilkProd > 0 : 0.07 * An_BW ;  Trg_MilkProd = 0 : 0.2 * An_BW`
**Eq. 20-431** [p.516]  `Fe_K_m = 2.5 * An_DMIn`
**Eq. 20-432** [p.516]  `An_K_m = Ur_K_m + Fe_K_m`
**Eq. 20-433** [p.516]  `An_K_g = 2.5 * An_BWgain`
**Eq. 20-434** [p.516]  `An_K_y = An_GestDay <= 190 : 0 ;  An_GestDay > 190 : 1.03 * An_BW / 715`
**Eq. 20-435** [p.516]  `An_K_l = 1.5 * An_MilkProd`
**Eq. 20-436** [p.516]  `An_K_req = Calf & Dt_DMIn_ClfLiq > 0 : An_K_Clf ;  else : An_K_m + An_K_g + An_K_y + An_K_l`
**Eq. 20-437** [p.516]  `An_K_prod = An_K_g - An_K_y - An_K_l`   (⚠ sinais como impresso)
**Eq. 20-438** [p.516]  `An_K_bal = Abs_KIn - An_K_req`

#### Enxofre (g/d) — baseado em ingestão dietética
**Eq. 20-439** [p.516]  `An_S_req = 2.0 * An_DMIn`
**Eq. 20-440** [p.516]  `An_S_bal = Dt_SIn - An_S_req`

### Microminerais (mg/d)

#### Cobalto
**Eq. 20-441** [p.516]  `Abs_CoIn (mg/d) = Calf & Dt_DMIn_ClfLiq > 0 : 0 ;  else : Dt_CoIn`
**Eq. 20-442** [p.516]  `An_Co_req = 0.2 * An_DMIn`
**Eq. 20-443** [p.516]  `An_Co_bal = Abs_CoIn - An_Co_req`

#### Cobre
**Eq. 20-444** [p.516]  `Fd_acCu_f = Calf & Dt_DMIn_ClfLiq > 0 : 1 ;  Calf & Dt_DMIn_ClfLiq = 0 : 0.1 ;  else : Fd_acCu_f`
**Eq. 20-445** [p.516]  `Fd_absCuIn_f = Fd_CuIn_f * Fd_acCu_f`
**Eq. 20-446** [p.517]  `Abs_CuIn = SUM_{f=1..N_f} Fd_absCuIn_f`
**Eq. 20-447** [p.517]  `An_Cu_Clf = ( 0.0145 * An_BW + (2.5 * An_BWgain) ) / 0.5`
**Eq. 20-448** [p.517]  `An_Cu_m = 0.0145 * An_BW`
**Eq. 20-449** [p.517]  `An_Cu_g = 2.0 * An_BWgain`
**Eq. 20-450** [p.517]  `An_Cu_y = An_GestDay < 90 : 0 ;  90 <= An_GestDay <= 190 : 0.0003 * An_BW ;  An_GestDay > 190 : 0.0023 * An_BW`
**Eq. 20-451** [p.517]  `An_Cu_l = 0.04 * An_MilkProd`
**Eq. 20-452** [p.517]  `An_Cu_req = Calf & Dt_DMIn_ClfLiq > 0 : An_Cu_Clf ;  else : An_Cu_m + An_Cu_g + An_Cu_y + An_Cu_l`
**Eq. 20-453** [p.517]  `An_Cu_prod = An_Cu_g + An_Cu_y + An_Cu_l`   (unidade impressa g/d; ⚠ provável mg/d)
**Eq. 20-454** [p.517]  `An_Cu_bal = Abs_CuIn - An_Cu_req`   (unidade impressa g/d; ⚠ provável mg/d)

#### Iodo
**Eq. 20-455** [p.517]  `An_I_req (mg/d) = Calf & Dt_DMIn_ClfLiq > 0 : 0.8 * An_DMIn ;  else : 0.216 * An_BW^0.528 + 0.1 * Trg_MilkProd`
**Eq. 20-456** [p.517]  `An_I_bal = Dt_IIn - An_I_req`   (baseado em ingestão dietética)

#### Ferro
**Eq. 20-457** [p.517]  `Fd_acFe_f = Calf & Dt_DMIn_ClfLiq > 0 : 1 ;  else : Fd_acFe_f`
**Eq. 20-458** [p.517]  `Fd_absFeIn_f = Fd_FeIn_f * Fd_acFe_f`
**Eq. 20-459** [p.517]  `Abs_FeIn = SUM_{f=1..N_f} Fd_absFeIn_f`
**Eq. 20-460** [p.517]  `An_Fe_Clf = 34 * An_BWgain / 0.25`
**Eq. 20-461** [p.518]  `An_Fe_g = 34 * An_BWgain`
**Eq. 20-462** [p.518]  `An_Fe_y = An_GestDay <= 190 : 0 ;  An_GestDay > 190 : 0.025 * An_BW`
**Eq. 20-463** [p.518]  `An_Fe_l = 1.0 * An_MilkProd`
**Eq. 20-464** [p.518]  `An_Fe_req = Calf & Dt_DMIn_ClfLiq > 0 : An_Fe_Clf ;  else : An_Fe_g + An_Fe_y + An_Fe_l`   (SEM termo de mantença)
**Eq. 20-465** [p.518]  `An_Fe_prod = An_Fe_g + An_Fe_y + An_Fe_l`   (unidade impressa g/d; ⚠ provável mg/d)
**Eq. 20-466** [p.518]  `An_Fe_bal = Abs_FeIn - An_Fe_req`

#### Manganês
**Eq. 20-467** [p.518]  `Fd_acMn_f = Calf & Dt_DMIn_ClfLiq > 0 : 1 ;  Calf & Dt_DMIn_ClfLiq = 0 : 0.05 ;  else : Fd_acMn_f`   (⚠ texto p.511: 0.005)
**Eq. 20-468** [p.518]  `Fd_absMnIn_f = Fd_MnIn_f * Fd_acMn_f`
**Eq. 20-469** [p.518]  `Abs_MnIn = SUM_{f=1..N_f} Fd_absMnIn_f`
**Eq. 20-470** [p.518]  `An_Mn_m = 0.0026 * An_BW`
**Eq. 20-471** [p.518]  `An_Mn_Clf = ( 0.0026 * An_BW + (0.7 * An_BWgain) ) / 0.01`
**Eq. 20-472** [p.518]  `An_Mn_g = 0.7 * An_BWgain`
**Eq. 20-473** [p.518]  `An_Mn_y = An_GestDay <= 190 : 0 ;  An_GestDay > 190 : 0.00042 * An_BW`
**Eq. 20-474** [p.518]  `An_Mn_l = 0.03 * An_MilkProd`
**Eq. 20-475** [p.518]  `An_Mn_req = Calf & Dt_DMIn_ClfLiq > 0 : An_Mn_Clf ;  else : An_Mn_m + An_Mn_g + An_Mn_y + An_Mn_l`
**Eq. 20-476** [p.519]  `An_Mn_prod = An_Mn_g + An_Mn_y + An_Mn_l`   (unidade impressa g/d; ⚠ provável mg/d)
**Eq. 20-477** [p.519]  `An_Mn_bal = Abs_MnIn - An_Mn_req`

#### Selênio (baseado em ingestão dietética)
**Eq. 20-478** [p.519]  `An_Se_req (mg/d) = 0.3 * An_DMIn`
**Eq. 20-479** [p.519]  `An_Se_bal = Dt_SeIn - An_Se_req`

#### Zinco
**Eq. 20-480** [p.519]  `Fd_acZn_f = Calf & Dt_DMIn_ClfLiq > 0 : 1 ;  Calf & Dt_DMIn_ClfLiq = 0 : 0.20 ;  else : Fd_acZn_f`
**Eq. 20-481** [p.519]  `Fd_absZnIn_f = Fd_ZnIn_f * Fd_acZn_f`
**Eq. 20-482** [p.519]  `Abs_ZnIn = SUM_{f=1..N_f} Fd_absZnIn_f`
**Eq. 20-483** [p.519]  `An_Zn_Clf = ( 2.0 * An_DMIn + (24 * An_BWgain) ) / 0.25`
**Eq. 20-484** [p.519]  `An_Zn_m = 5.0 * An_DMIn`
**Eq. 20-485** [p.519]  `An_Zn_g = 24 * An_BWgain`
**Eq. 20-486** [p.519]  `An_Zn_y = An_GestDay <= 190 : 0 ;  An_GestDay > 190 : 0.017 * An_BW`
**Eq. 20-487** [p.519]  `An_Zn_l = 4.0 * An_MilkProd`
**Eq. 20-488** [p.519]  `An_Zn_req = Calf & Dt_DMIn_ClfLiq > 0 : An_Zn_Clf ;  else : An_Zn_m + An_Zn_g + An_Zn_y + An_Zn_l`
**Eq. 20-489** [p.519]  `An_Zn_prod = An_Zn_g + An_Zn_y + An_Zn_l`   (unidade impressa g/d; ⚠ provável mg/d)
**Eq. 20-490** [p.519]  `An_Zn_bal = Abs_ZnIn - An_Zn_req`

### 4.9 Vitaminas (pp.519-520), IU/d, baseadas em ingestão dietética
**Eq. 20-491** [p.519]  `An_VitA_req = An_MilkProd <= 35 kg/d : 110 * An_BW ;  An_MilkProd > 35 kg/d : 110 * An_BW + 1,000 * (An_MilkProd - 35)`
**Eq. 20-492** [p.520]  `An_VitA_bal = Dt_VitAIn - An_VitA_req`
**Eq. 20-493** [p.520]  `An_VitD_req = An_MilkProd = 0 kg/d : 32 * An_BW ;  An_MilkProd > 0 kg/d : 40 * An_BW`
**Eq. 20-494** [p.520]  `An_VitD_bal = Dt_VitDIn - An_VitD_req`
**Eq. 20-495** [p.520]
```
An_VitE_req =
  An_MilkProd = 0 & An_Parity >= 1 : 2.0 * An_BW
  An_GestDay >= 259 & An_Preg = 1  : 3.0 * An_BW
  Otherwise                        : 0.8 * An_BW
```
**Eq. 20-496** [p.520]  `An_VitE_bal = Dt_VitEIn - An_VitE_req`
Texto [p.520]: se os animais pastam, a exigência de vitamina E é **reduzida em 50 UI/kg de MS de pasto ingerido**; a contribuição é limitada na exigência total de vitamina E (limite exato NÃO informado).

---

## 5. Parâmetros e tabelas
(Tabelas de cálculo: topografia [4.1], CAs de bezerros [4.8]. Abaixo, as tabelas numeradas 20-11 a 20-21, transcritas integralmente e conferidas contra a imagem. Células em branco no original = "—".)

### 5.1 AVALIAÇÕES DE MODELO — dados e métodos [p.520-523]
- Banco de dados grande da literatura usado para AJUSTE do modelo, principalmente para digestão de proteína e gordura e para derivar as predições de proteína, gordura e produção de leite. Os mesmos dados serviram para teste; logo, as avaliações de digestão de proteína/gordura e de produção de leite **não são independentes** dos dados de derivação (mas houve avaliação cruzada extensa na derivação). Predições de **DMIn e digestão de carboidratos** foram desenvolvidas com dados independentes: suas avaliações são independentes [p.520].
- Estatísticas: RMSE e sua partição em viés médio e viés de inclinação (slope bias) (Bibby e Toutenberg, 1977) + CCC (Lin, 1989). Sem ajuste para efeito aleatório de estudo, salvo indicação [p.520].
- Dados de digestão de proteína e gordura: **1,149 médias de tratamento de 275 publicações**. Critérios de seleção: (1) fluxo de saída ruminal, (2) digestibilidade de AGs no trato total, (3) infusões de AA ou proteínas, (4) ensaios com AA protegidos do rúmen, (5) diferenças arteriovenosas mamárias. Principalmente vacas adultas em lactação (N = 1,023); algumas vacas secas e animais jovens; **PC mínimo 319 kg** [p.520, 522].
- Texto remete a "Tabela 20-11" (características dos animais) e "Tabela 20-12" (dietas). ⚠ A Tabela 20-11 impressa (p.520) traz o MESMO conteúdo da Tabela 20-13 (resíduos); a tabela de características de animais NÃO está impressa de fato. Verificado célula a célula: idêntica à 20-13.

### 5.2 Tabela 20-12 — Resumo das características dietéticas dos dados de avaliação [p.521] (N = 1,149; valores em % da MS salvo indicação)
| Variável | Média | Mediana | DP | Min | Max | 1.Quartil | 3.Quartil | Distorção | Curtose |
|---|---|---|---|---|---|---|---|---|---|
| Dt_DMIn, kg/d | 20.0 | 20.2 | 4.2 | 5.8 | 31.8 | 17.5 | 22.9 | -0.33 | 0.41 |
| Dt_ForWet | 40.3 | 44.8 | 21.4 | 0.0 | 100.0 | 30.0 | 55.0 | -0.51 | -0.14 |
| Dt_ForDry | 11.3 | 0.0 | 16.8 | 0.0 | 99.7 | 0.0 | 17.5 | 1.77 | 3.02 |
| Dt_Conc | 48.4 | 50.0 | 12.5 | 0.0 | 100.0 | 40.0 | 55.4 | -0.41 | 1.93 |
| Dt_Ash | 7.55 | 7.40 | 1.97 | 4.0 | 22.47 | 6.31 | 8.40 | 2.93 | 17.73 |
| Dt_NDF | 32.7 | 31.9 | 6.1 | 14.6 | 54.3 | 28.4 | 35.9 | 0.65 | 0.62 |
| Dt_ForNDF_NDF, % of NDF | 74.0 | 76.6 | 12.9 | 0.0 | 100.0 | 66.2 | 83.0 | -0.83 | 1.10 |
| Dt_ADF | 20.0 | 19.3 | 4.2 | 7.2 | 39.0 | 17.2 | 22.0 | 0.91 | 1.64 |
| Dt_Lg | 3.65 | 3.45 | 0.96 | 1.57 | 7.65 | 2.94 | 4.22 | 0.84 | 0.59 |
| Dt_St | 26.7 | 27.3 | 8.5 | 1.1 | 53.0 | 21.4 | 32.6 | -0.41 | 0.40 |
| Dt_rOM | 13.6 | 13.5 | 5.2 | -5.8 | 42.4 | 10.7 | 16.5 | 0.28 | 2.41 |
| Dt_CP | 16.5 | 16.6 | 2.5 | 7.7 | 26.2 | 15.1 | 18.0 | -0.08 | 1.27 |
| Dt_TP | 16.1 | 16.3 | 2.7 | 7.7 | 26.2 | 14.6 | 17.8 | -0.14 | 0.64 |
| Dt_NPNCP | 0.37 | 0.00 | 0.91 | 0.00 | 7.10 | 0.00 | 0.00 | 3.78 | 17.81 |
| Dt_NPN | 0.06 | 0.00 | 0.15 | 0.00 | 1.14 | 0.00 | 0.00 | 3.78 | 17.81 |
| Dt_CPA_CP, % of CP | 37.0 | 35.5 | 8.3 | 18.2 | 81.8 | 31.2 | 41.4 | 1.12 | 2.34 |
| Dt_CPB_CP, % of CP | 53.9 | 54.5 | 9.0 | 13.0 | 74.0 | 49.2 | 59.8 | -0.68 | 0.89 |
| Dt_CPC_CP, % of CP | 8.88 | 8.49 | 2.77 | 3.63 | 29.85 | 7.00 | 10.50 | 1.34 | 4.96 |
| Dt_FA | 3.39 | 2.85 | 1.53 | 0.77 | 15.22 | 2.30 | 4.36 | 1.64 | 5.80 |
| Dt_C12 | 0.052 | 0.038 | 0.051 | 0.003 | 1.004 | 0.015 | 0.075 | 6.45 | 105.43 |
| Dt_C14 | 0.041 | 0.034 | 0.035 | 0.005 | 0.413 | 0.015 | 0.052 | 2.71 | 14.52 |
| Dt_C16 | 0.666 | 0.456 | 0.450 | 0.118 | 3.574 | 0.385 | 0.815 | 2.24 | 6.48 |
| Dt_C161 | 0.034 | 0.018 | 0.041 | 0.005 | 0.527 | 0.013 | 0.033 | 3.77 | 24.37 |
| Dt_C180 | 0.157 | 0.074 | 0.208 | 0.010 | 2.420 | 0.057 | 0.156 | 4.11 | 27.00 |
| Dt_C181t | 0.023 | 0.006 | 0.044 | 0.000 | 0.540 | 0.003 | 0.019 | 4.29 | 29.34 |
| Dt_C181c | 0.758 | 0.547 | 0.593 | 0.020 | 7.546 | 0.402 | 1.005 | 3.04 | 20.89 |
| Dt_C182 | 1.235 | 1.165 | 0.534 | 0.129 | 4.573 | 0.884 | 1.449 | 1.21 | 2.56 |
| Dt_C183 | 0.333 | 0.300 | 0.185 | 0.056 | 2.273 | 0.211 | 0.415 | 3.65 | 28.20 |
| Dt_OtherFA | 0.113 | 0.077 | 0.110 | 0.027 | 1.333 | 0.063 | 0.127 | 6.04 | 55.25 |
| Dt_ArgIn, g/d | 164 | 159 | 59 | 30 | 338 | 124 | 202 | 0.33 | -0.20 |
| Dt_HisIn, g/d | 80 | 80 | 26 | 21 | 183 | 61 | 98 | 0.19 | -0.07 |
| Dt_IleIn, g/d | 139 | 139 | 43 | 34 | 269 | 107 | 168 | 0.17 | -0.24 |
| Dt_LeuIn, g/d | 274 | 277 | 89 | 73 | 621 | 213 | 331 | 0.35 | 0.51 |
| Dt_LysIn, g/d | 153 | 152 | 54 | 29 | 298 | 113 | 193 | 0.12 | -0.56 |
| Dt_MetIn, g/d | 54 | 54 | 17 | 14 | 114 | 41 | 64 | 0.35 | 0.23 |
| Dt_PheIn, g/d | 160 | 161 | 49 | 38 | 311 | 121 | 193 | 0.18 | -0.01 |
| Dt_ThrIn, g/d | 129 | 129 | 39 | 33 | 251 | 99 | 155 | 0.10 | -0.23 |
| Dt_TrpIn, g/d | 40 | 40 | 13 | 9 | 87 | 30 | 48 | 0.31 | 0.38 |
| Dt_ValIn, g/d | 173 | 176 | 51 | 43 | 344 | 133 | 208 | 0.16 | 0.00 |

(Corrigidos pela imagem vs OCR: Dt_ForDry mediana 0.0; Dt_C14 distorção 2.71; Dt_NPNCP máx 7.10; Dt_NPN máx 1.14; Dt_MetIn máx 114; Dt_PheIn máx 311; Dt_ForNDF 1.Quartil 66.2. Nota do livro: variáveis são as especificadas para o modelo. Dt_rOM = MO residual ("rOM"). ⚠ Dt_C14 e demais ácidos graxos individuais em % da MS.)

### 5.3 Tabela 20-13 (= conteúdo também impresso como "Tabela 20-11", p.520) — Análises residuais da predição de CMS (IMS) de animais em lactação e de efluxo ruminal de N, amido e FDN [p.521]
Viés médio = observado − predito.
| Variável | DMIn | DMIn | Du_MicN | Du_NANMN | Du_NAN | Du_St | Du_NDF |
|---|---|---|---|---|---|---|---|
| Equação | 20-21 | 20-22 | 20-74 | 20-83 | 20-82 | 20-57 | 20-56 |
| Unidades | kg/d | kg/d | g/d | g/d | g/d | kg/d | kg/d |
| N | 951 | 951 | 596 | 587 | 585 | 178 | 319 |
| Média observada | 20.6 | 20.6 | 278 | 205 | 487 | 2.66 | 3.76 |
| Média predita | 20.8 | 22.3 | 269 | 203 | 474 | 2.31 | 3.98 |
| CCC | 0.71 | 0.54 | 0.51 | 0.56 | 0.74 | 0.54 | 0.43 |
| RMSE | 2.50 | 3.29 | 81 | 68 | 88 | 1.18 | 1.03 |
| RMSE, % média | 12.1 | 15.9 | 29.2 | 33.1 | 18.0 | 44.3 | 27.3 |
| Viés médio, %MSE | 0.4 | 26.8 | 1.2 | 0.1 | 2.0 | 8.8 | 4.7 |
| Viés de inclinação, %MSE | 9.0 | 3.2 | 2.1 | 2.1 | 1.6 | 0.1 | 0.0 |
| Viés médio | -0.2 | -1.7 | 8.9 | 2.2 | 12.3 | 0.3 | -0.2 |
| Viés de inclinação | 0.31 | 0.26 | 0.22 | -0.17 | 0.11 | 0.05 | -0.01 |
| P viés médio | 0.06 | 0.00 | 0.01 | 0.44 | 0.00 | 0.00 | 0.00 |
| P viés de inclinação | 0.0001 | 0.0001 | 0.0003 | 0.0004 | 0.002 | 0.61 | 0.88 |
Nota do livro: erros de predição do fluxo ruminal de AA estão na Tabela 20-14; CCC desses valores variou de 0.43 a 0.59 com viés de inclinação mínimo ou nenhum e pequenas proporções de viés médio. Eq. 20-21 = IMS "com base em fatores do animal"; Eq. 20-22 = "fatores do animal e dos alimentos"; Du_MicN = N microbiano duodenal; Du_NANMN = NAN não microbiano; Du_NAN = NAN total; Du_St e Du_NDF = fluxo duodenal de amido e FDN.

### 5.4 Tabela 20-14 — Resíduos das predições do fluxo ruminal de AA (g/d) pela Eq. 20-87 [p.522]
| Variável | Arg | His | Ile | Leu | Lys | Met | Phe | Thr | Val |
|---|---|---|---|---|---|---|---|---|---|
| N | 216 | 221 | 221 | 221 | 223 | 220 | 221 | 221 | 221 |
| Média observada | 119 | 57.4 | 122 | 225 | 158 | 48.6 | 130 | 124 | 138 |
| Média predita | 130 | 60.7 | 135 | 229 | 184 | 54.5 | 141 | 132 | 150 |
| CCC | 0.54 | 0.51 | 0.49 | 0.60 | 0.45 | 0.43 | 0.57 | 0.58 | 0.52 |
| RMSE | 32.8 | 18.1 | 36.2 | 62.5 | 56.6 | 17.4 | 34.8 | 31.1 | 40.3 |
| RMSE, % média | 27.7 | 31.5 | 29.8 | 27.7 | 35.9 | 35.7 | 26.7 | 25.1 | 29.1 |
| Viés médio, %MSE | 11.9 | 3.3 | 13.9 | 0.4 | 21.8 | 11.5 | 10.3 | 7.1 | 8.6 |
| Viés de inclinação, %MSE | 0.2 | 2.2 | 0.1 | 0.1 | 0.0 | 0.0 | 0.0 | 0.8 | 0.0 |
| Viés médio | -11.3 | -3.3 | -13.5 | -4.0 | -26.5 | -5.9 | -11.2 | -8.3 | -11.8 |
| Viés de inclinação | -0.06 | -0.18 | -0.05 | 0.04 | -0.02 | -0.01 | 0.01 | 0.11 | 0.02 |
| P viés médio | 0.00 | 0.01 | 0.00 | 0.34 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| P viés de inclinação | 0.45 | 0.03 | 0.60 | 0.60 | 0.83 | 0.95 | 0.92 | 0.16 | 0.81 |
(Corrigido pela imagem: Arg obs 119 [OCR 19], Phe/Thr/Val RMSE e Met viés médio %MSE 11.5.) Todos os AA têm fluxo ruminal SUPERESTIMADO (viés médio negativo), exceto sem significância em Leu (P=0.34).

### 5.5 Tabela 20-15 — Resíduos das predições de excreção fecal de nutrientes (kg/d) [p.522]
| Variável | Fe_CP | Fe_NDF | Fe_St | Fe_FA | Fe_OM |
|---|---|---|---|---|---|
| Equação | 20-138 | 20-120 | 20-98 | 20-162 | 20-166 |
| N | 458 | 412 | 203 | 121 | 448 |
| Média observada | 1.08 | 3.24 | 0.451 | 0.340 | 5.58 |
| Média predita | 0.89 | 3.20 | 0.666 | 0.312 | 5.00 |
| CCC | 0.53 | 0.77 | 0.27 | 0.80 | 0.71 |
| RMSE | 0.29 | 0.56 | 0.45 | 0.093 | 1.04 |
| RMSE, % média | 26.8 | 17.4 | 99.8 | 27.4 | 18.7 |
| Viés médio, %MSE | 40.9 | 0.3 | 22.8 | 9.0 | 30.9 |
| Viés de inclinação, %MSE | 9.8 | 0.2 | 22.2 | 4.4 | 0.1 |
| Viés médio | 0.2 | 0.0 | -0.2 | 0.0 | 0.6 |
| Viés de inclinação | 0.51 | 0.03 | -0.65 | 0.16 | 0.02 |
| P viés médio | 0.00 | 0.26 | 0.00 | 0.00 | 0.00 |
| P viés de inclinação | 0.0001 | 0.41 | 0.0001 | 0.02 | 0.49 |

### 5.6 Tabela 20-16 — Resíduos das predições de produção de leite e componentes [p.523]
**Atenção**: na imagem os RÓTULOS das linhas estão deslocados uma linha em relação aos valores (a linha rotulada "N" contém as unidades, etc.). Reconstrução validada numericamente (RMSE/média = RMSE%; CCC e RMSE% batem com o texto do livro: CCC 0.75/0.62/0.75; RMSE 14.4/17.1/14.6%; viés = obs − pred: 929−930 = −1.1; 30.9−34.7 = −3.7). Valores como impressos, com o rótulo CORRETO:
| Variável | Proteína | Gordura | Leite | Milk_ME_Allow | Milk_MP_Allow |
|---|---|---|---|---|---|
| Equação | 20-185 | 20-215 | 20-216 | 20-338 | 20-339 |
| Unidades | g/d | g/d | kg/d | kg/d | kg/d |
| N | 935 | 935 | 935 | 935 | 935 |
| Média observada | 929 | 1,098 (impresso 1.098) | 30.9 | 30.9 | 30.9 |
| Média predita | 930 | 1,114 (impresso 1.114) | 31.0 | 34.7 | 32.6 |
| CCC | 0.75 | 0.62 | 0.75 | 0.67 | 0.64 |
| RMSE | 133 | 188 | 4.50 | 7.50 | 6.80 |
| RMSE, % média | 14.4 | 17.1 | 14.6 | 24.4 | 22.1 |
| Viés médio, %MSE | 0.0 | 0.7 | 0.1 | 24.5 | 5.9 |
| Viés de inclinação, %MSE | 3.1 | 0.0 | 3.3 | 37.9 | 28.6 |
| Viés médio | -1.1 | -16.0 | -0.1 | -3.7 | -1.7 |
| Viés de inclinação | 0.16 | 0.02 | 0.16 | -0.45 | 0.43 |
| P viés médio | 0.54 | 0.01 | 0.38 | 0.00 | 0.00 |
| P viés de inclinação | 0.0001 | 0.51 | 0.0001 | 0.0001 | 0.0001 |
⚠ No impresso a linha de "Equação" (20-185, 20-215, 20-216, 20-338, 20-339) está correta; "Eq. 20-216" prediz leite (empírica, a partir de proteína e gordura previstas).

### 5.7 Tabela 20-17 — DP de análises de amostras repetidas, grãos e subprodutos (St-Pierre e Weiss, 2015) [p.524]
(DP inclui variância fazenda a fazenda, mês a mês, amostral e analítica; 6 ingredientes de 12 meses em várias fazendas. Concentrado = média de milho e farelo de soja.)
| Nutriente | Caroço de algodão inteiro | Milho seco | Milho c/ alto teor de umidade | Grãos secos de destilaria | Farelo de soja | Resíduo úmido de cervejaria | Concentrado |
|---|---|---|---|---|---|---|---|
| MS | 2.11 | 1.96 | 6.14 | 1.9 | 0.81 | 1.98 | 1.38 |
| Cinzas | 0.55 | 0.58 | 0.33 | 0.91 | 0.56 | 0.58 | 0.57 |
| PB | 1.68 | 0.54 | 0.73 | 3.57 | 1.41 | 4.09 | 0.975 |
| Amido | — | 1.49 | — | — | 0.49 | — | 0.99 |
| FDN | 4.14 | 2 | 5.36 | 2.56 | 1.67 | 3.98 | 1.835 |
| Lignina | — | 4.73 | — | — | 3.69 | — | 4.21 |
| Ca | 0.091 | 0.026 | 0.034 | 0.043 | 0.096 | 0.112 | 0.061 |
| K | 0.092 | 0.055 | 0.057 | 0.285 | 0.18 | 0.049 | 0.118 |
| Mg | 0.046 | 0.018 | 0.015 | 0.09 | 0.033 | 0.031 | 0.026 |
| Na | — | 0.015 | 0.015 | 0.081 | 0.053 | 0.023 | 0.034 |
| P | 0.085 | 0.038 | 0.036 | 0.147 | 0.051 | 0.088 | 0.045 |
| Cu | 3.69 | 2.22 | 1.33 | 2.2 | 2.71 | 4.89 | 2.465 |
| Fe | 38.2 | 29.16 | 39.92 | 23.2 | 41.7 | 67.1 | 35.43 |
| Mn | 9.8 | 4.39 | 3.07 | 7.25 | 6.01 | 15.3 | 5.2 |
| Zn | 10.8 | 8.45 | 5.84 | 18.4 | 6.07 | 22.3 | — |
(Posição das células vazias conferida: a coluna Concentrado = média das colunas milho seco e farelo de soja, ex. FDN (2+1.67)/2 = 1.835. Unidades: MS, cinzas, PB, amido, FDN, lignina, Ca, K, Mg, Na, P em % [de MS]; Cu, Fe, Mn, Zn em mg/kg — unidades não impressas na tabela ⚠.) Corrigido pela imagem: DDG Cu 2.2 e farelo de soja Cu 2.71 (OCR 22 e 2.1).

### 5.8 Tabela 20-18 — DP de análises de amostras duplicadas de um ingrediente, laboratório comercial dos EUA (Rock River Laboratories; amostras duplicadas aleatórias por técnico por dia, mar/2018–out/2019) [p.525]
| Analito | Unid. | TMR | Silagem de milho | Gramíneas | Leguminosas | Mix de forragem | Forragem de grãos pequenos | Sorgo sudão |
|---|---|---|---|---|---|---|---|---|
| N | — | 34 | 1264 | 121 | 1043 | 515 | 284 | 62 |
| MS (manual) | % MN | 1.11 | 3.96 | 4.31 | 5.21 | 1.90 | 1.09 | 1.41 |
| MS (NIR) | % MN | 0.68 | 0.31 | 0.47 | 0.34 | 0.31 | 0.57 | 0.90 |
| Cinza | % MS | 0.07 | 0.17 | 0.28 | 1.10 | 0.41 | 0.79 | 0.87 |
| PB | % MS | 0.32 | 0.37 | 0.74 | 1.45 | 0.84 | 0.11 | 0.12 |
| Aminoácidos totais | % MS | — | 0.54 | 0.70 | 1.16 | 0.48 | 0.16 | 0.16 |
| Amido | % MS | 2.14 | 6.16 | 0.15 | 3.03 | 1.21 | 0.95 | 1.66 |
| Etanol sol. CHO | % MS | 0.17 | 0.12 | 0.53 | 0.28 | 0.31 | 0.50 | 0.23 |
| Água sol. CHO | % MS | 0.20 | 0.13 | — | — | — | — | — |
| FDN | % MS | 2.14 | 3.31 | 1.90 | 4.94 | 4.25 | 0.91 | 0.55 |
| FDN (sem cinzas) | % MS | 2.06 | 3.15 | 1.82 | 4.59 | 4.57 | 1.05 | 0.85 |
| FDA | % MS | 1.33 | 1.81 | 0.24 | 1.65 | 0.83 | 0.82 | 0.33 |
| Lignina | % MS | 0.071 | 0.066 | 0.071 | 0.096 | 0.128 | 0.094 | 0.026 |
| dFDNr30 | % MS | 0.96 | 1.25 | 0.48 | 1.46 | 3.75 | 0.90 | 0.54 |
| dFDNr48 | % MS | — | 1.24 | 1.44 | 1.72 | 1.35 | 1.32 | 0.89 |
| dFDNr120 | % MS | 0.30 | 1.27 | 1.03 | 1.67 | 1.46 | 1.37 | 0.76 |
| dFDNr240 | % MS | 0.66 | 1.05 | 0.75 | 1.64 | 1.60 | 1.29 | 0.62 |
| Gordura bruta | % MS | 0.052 | 0.028 | 0.012 | 0.020 | 0.015 | 0.006 | 0.04 |
| Ácidos graxos totais | % MS | 0.032 | 0.015 | 0.007 | 0.007 | 0.004 | 0.007 | 0.03 |
| Linoleico | % AGT | 0.60 | 4.20 | 1.01 | 5.73 | 4.45 | 0.86 | 1.09 |
| Linolênico | % AGT | 1.10 | 4.98 | 1.18 | 9.92 | 10.27 | 2.34 | 2.77 |
| Mirístico | % AGT | 0.006 | 0.010 | 0.005 | 0.019 | 0.013 | 0.003 | 0.003 |
| Oleico | % AGT | 0.40 | 1.51 | 0.35 | 2.54 | 2.28 | 0.23 | 0.29 |
| Palmítico | % AGT | 0.51 | 0.50 | 0.63 | 1.60 | 1.11 | 0.37 | 0.48 |
| Esteárico | % AGT | 0.006 | 0.010 | 0.030 | 0.026 | 0.024 | 0.033 | 0.015 |
| Ca | % MS | — | 0.0002 | 0.0071 | 0.0073 | 0.0061 | 0.0023 | 0.0014 |
| K | % MS | — | 0.004 | 0.0201 | 0.0258 | 0.0264 | 0.0238 | 0.0307 |
| Mg | % MS | — | 0.00009 | 0.00025 | 0.00042 | 0.00025 | 0.00018 | 0.00036 |
| P | % MS | — | 0.00005 | 0.00011 | 0.00012 | 0.00016 | 0.00009 | 0.00008 |
| S | % MS | — | 0.000018 | 0.000088 | 0.00016 | 0.00083 | 0.000025 | 0.000021 |
(Rótulos PT impressos: "Amino Acidos Totais", "Ethanol Sol. CHO", "Agua Sol. CHO". Os DPs de mineral em Ca/K/Mg/P/S da silagem de milho parecem muito baixos frente aos demais, mas estão como impressos ⚠. "% MN" = % da matéria natural.)

### 5.9 Tabela 20-19 — Estimativas de variância para produção de leite observada e predita com variância nos dados de entrada e na medição do leite [p.526]
| | Leite kg/d | Prot. leite g/d | Prot. leite % | Gordura leite g/d | Gordura leite % |
|---|---|---|---|---|---|
| **Observado** — Média | 31.0 | 935 | 3.03 | 1,100 | 3.59 |
| Variância | 53.7 | 46,936 | 0.046 | 65,058 | 0.27 |
| DP | 7.33 | 217 | 0.21 | 255 | 0.52 |
| **Observado (2º bloco; rótulo repetido no impresso — refere-se ao predito com variância nas entradas; ⚠)** — Média | 30.29 | 907 | 2.98 | 1,100 | 3.65 |
| Variância | 27.7 | 31,532 | 0.034 | 37,374 | 0.20 |
| DP | 5.27 | 178 | 0.19 | 193 | 0.45 |
| **Modelo + animal + ambiente** (derivado por diferença) — Média | 0.75 | 28.2 | 0.044 | 0.58 | -0.066 |
| Variância | 25.9 | 15,404 | 0.012 | 27,684 | 0.072 |
| DP | 5.09 | 124 | 0.11 | 166 | 0.27 |
(Corrigido pela imagem: proteína média 28.2, não 282. Checagem: 53.7−27.7 ≈ 25.9 (arredondamento); 46,936−31,532 = 15,404; 65,058−37,374 = 27,684.)

### 5.10 Tabela 20-20 — Variância para dados de entrada e modelo para um nível de produção específico, por tamanho de grupo [p.526]
Nota: "Variância foi estimada para cada dieta e calculada a média entre as dietas para vários tamanhos de grupo." (Texto fala em DP médio entre dietas; título e nota falam em variância: ⚠ ambiguidade.) Unidades: Dt_DMIn kg/d; Dt_NDF, Dt_St, Dt_CP, Dt_CPA/B/C, Dt_FA, ácidos graxos em % MS; Dt_DEIn Mcal/d (impresso "% MS" no 1º e 3º blocos, mas Mcal/d no 2º ⚠).

**Bloco "Leite"**
| Grupo | Dt_DMIn | Dt_NDF | Dt_DEIn | Dt_St | Dt_CP | Dt_CPA | Dt_CPB | Dt_CPC | Dt_FA |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.18 | 9.27 | 3.92 | 12.99 | 3.83 | 1.33 | 2.92 | 0.41 | 1.25 |
| 4 | 0.18 | 9.19 | 3.84 | 12.83 | 3.81 | 1.32 | 2.92 | 0.40 | 1.24 |
| 8 | 0.18 | 8.91 | 3.75 | 12.40 | 3.71 | 1.29 | 2.84 | 0.39 | 1.19 |
| 16 | 0.17 | 8.48 | 3.63 | 11.84 | 3.59 | 1.25 | 2.75 | 0.38 | 1.16 |
| 32 | 0.17 | 8.20 | 3.57 | 11.54 | 3.57 | 1.24 | 2.75 | 0.37 | 1.13 |
| 64 | 0.16 | 8.27 | 3.42 | 11.45 | 3.51 | 1.22 | 2.72 | 0.38 | 1.12 |
| 128 | 0.16 | 7.43 | 3.30 | 9.75 | 3.10 | 1.07 | 2.44 | 0.32 | 1.02 |
| 256 | 0.15 | 7.07 | 3.37 | 9.09 | 3.00 | 1.03 | 2.37 | 0.32 | 1.06 |

**Bloco "Proteína do leite"**
| Grupo | Dt_DMIn kg/d | Dt_NDF % MS | Dt_DEIn Mcal/d | Abs_His g/d | Abs_Ile | Abs_Leu | Abs_Lys | Abs_Met | Abs_Thr |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.19 | 9.10 | 3.78 | 10.35 | 21.37 | 33.24 | 29.55 | 8.97 | 18.65 |
| 4 | 0.18 | 9.05 | 3.76 | 10.37 | 21.29 | 33.21 | 29.45 | 8.93 | 18.58 |
| 8 | 0.18 | 8.82 | 3.64 | 10.31 | 21.11 | 32.75 | 29.19 | 8.74 | 18.41 |
| 16 | 0.18 | 8.68 | 3.55 | 9.93 | 20.77 | 31.88 | 28.57 | 7.97 | 18.03 |
| 32 | 0.17 | 8.22 | 3.44 | 9.46 | 20.04 | 30.37 | 27.27 | 7.56 | 17.33 |
| 64 | 0.17 | 8.12 | 3.26 | 9.13 | 19.22 | 29.29 | 26.38 | 7.18 | 16.73 |
| 128 | 0.16 | 7.91 | 3.19 | 8.87 | 19.00 | 28.56 | 25.60 | 7.09 | 16.31 |
| 256 | 0.15 | 7.46 | 3.18 | 8.52 | 17.94 | 26.58 | 24.18 | 6.56 | 15.30 |

**Bloco "Gordura do leite"**
| Grupo | Dt_DMIn kg/d | Dt_NDF | Dt_FA | Dt_C16 | Dt_C18 | Dt_C18.1t | Dt_C18.1c | Dt_C18.2 | Dt_C18.3 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.18 | 9.28 | 1.26 | 0.306 | 0.107 | 0.022 | 0.45 | 0.47 | 0.16 |
| 4 | 0.18 | 9.19 | 1.26 | 0.306 | 0.107 | 0.022 | 0.45 | 0.47 | 0.16 |
| 8 | 0.18 | 9.13 | 1.26 | 0.306 | 0.106 | 0.021 | 0.45 | 0.47 | 0.16 |
| 16 | 0.18 | 8.89 | 1.20 | 0.290 | 0.100 | 0.020 | 0.43 | 0.45 | 0.15 |
| 32 | 0.17 | 8.67 | 1.17 | 0.282 | 0.098 | 0.019 | 0.41 | 0.44 | 0.15 |
| 64 | 0.17 | 8.36 | 1.10 | 0.264 | 0.095 | 0.018 | 0.39 | 0.42 | 0.14 |
| 128 | 0.16 | 8.06 | 1.09 | 0.254 | 0.094 | 0.018 | 0.39 | 0.41 | 0.14 |
| 256 | 0.15 | 7.96 | 1.11 | 0.275 | 0.106 | 0.019 | 0.39 | 0.40 | 0.13 |
(Corrigido pela imagem: Dt_St grupo 4 = 12.83 [OCR "12..83"]; Dt_FA grupo 256 no bloco gordura = 1.11 [OCR "Lil"].) Tendência: variância cai com o tamanho do grupo, mas não vai a zero mesmo com 256 animais (variância do "modelo+animal+ambiente").

### 5.11 Tabela 20-21 — Correlações parciais entre produção de leite/componentes e entradas de nutrientes selecionados [p.527]
(Calculadas de dados simulados ±1 erro padrão, tamanho de grupo = 256, em torno dos valores médios previstos para cada leite, proteína e gordura.)
| Entrada | Leite | Proteína do leite | Gordura do leite |
|---|---|---|---|
| Dt_DEIn | 0.22 | 0.18 | 0.26 |
| Dt_NDFIn | 0.34 | 0.49 | 0.18 |
| Dt_LgIn | 0.06 | 0.04 | 0.17 |
| Dt_StIn | 0.31 | 0.47 | 0.13 |
| Dt_rOMIn | 0.21 | 0.41 | 0.04 |
| Dt_CPAIn | -0.03 | 0.01 | -0.02 |
| Abs_His_g | -0.01 | 0.03 | 0.02 |
| Abs_Ile_g | 0.02 | 0.05 | 0.01 |
| Abs_Leu_g | -0.03 | -0.05 | -0.05 |
| Abs_Lys_g | 0.13 | 0.09 | -0.01 |
| Abs_Met_g | 0.16 | 0.18 | 0.25 |
| Abs_Thr_g | -0.01 | 0.03 | 0.03 |
| Dt_FAIn | 0.03 | 0.15 | -0.03 |
| Dt_C16In | 0.09 | 0.03 | 0.10 |
| Dt_C18.3In | 0.08 | -0.01 | 0.18 |

---

## 6. Regras de decisão / restrições para o otimizador
- Eficiência mínima Kg_MP_NP = **0.39** [p.503].
- Crítico: **Km_MP_NP = 0.69** (Eq. 20-306); Km_ME_NE = 0.69 (bezerro sólido sem líquido), 0.63 (não-bezerro, paridade 0), 0.66 (paridade > 0) (Eq. 20-282); Km_ME_NE bezerro líquido 0.718 (Eq. 20-280).
- Locomoção em pastejo só se Dt_PastIn/Dt_DMIn ≥ 0.005 (Eq. 20-274); custo por frio/calor só para An_BW < 100 conforme impresso (Eq. 20-273, ⚠).
- Monensina na dieta: An_GasEOut × 0.95 (Eq. 20-311).
- Gestação (Mg, Na, Cl, K, Fe, Mn, Zn): exigência só quando An_GestDay > 190; Cu: 0 (<90 d), 0.0003×BW (90–190 d), 0.0023×BW (>190 d); Ca e P: curvas exponenciais desde o dia 1 (Eq. 20-375/388).
- Vitamina E: 2.0×BW (vaca seca, paridade ≥ 1, leite = 0), 3.0×BW (≥ 259 d de gestação e prenhe), 0.8×BW demais; reduzir 50 UI/kg MS de pasto ingerido [p.520].
- Vitamina A: 110×BW; acima de 35 kg/d de leite soma 1,000 UI por kg excedente [p.519]. Vitamina D: 32×BW (seca) / 40×BW (lactação) [p.520].
- Balanço de cada mineral/vitamina = ingerido (absorvido ou dietético) − exigência; o otimizador deve manter `An_Xx_bal >= 0` (o livro NÃO fixa margens de segurança nesta parte).
- Bezerros pré-desmame (An_StatePhys = "Calf" e Dt_DMIn_ClfLiq > 0): exigência de mineral = fórmula "Clf" (concentração de dieta; CA = 1) em vez da fatorial.
- Produção permitida por EM/PM (Eq. 20-338/339): NÃO usar como meta de produção (viés severo; Tabela 20-16).
- Regra de ordem: Ur_N_g depende do uso de PL → a seção EM é calculada depois da de proteína (p.506).

## 7. Lógica e fluxo (ordem de cálculo sugerida a partir do livro)
Fato textual do livro: "toda a seção EM deve ser colocada após as seções que definem o uso do PL" [p.506]. A ordem abaixo é uma sugestão consistente com as dependências das equações (marcadas "sugerida"):
1. Entradas das partes A/B do Cap. 20: ingestões (DMIn, EB, ED, PB, PM, AA absorvidos), PL de leite/ganho/gestação, LCT/UCT (Eq. 20-2/20-3).
2. Energia de mantença: 20-272 → 20-273 → 20-274..277 → 20-278 → Km (20-280..282) → 20-279 (An_MEmUse).
3. Proteína de mantença: descamação (20-283..286) → urina endógena (20-287..299) → fecal endógena (20-300..303) → 20-304..306.
4. Uso de PL/AA/PM (20-318..323) e (partes anteriores) Fe_CP_g, Milk_NP_g, etc.
5. N e energia urinária (20-308, 20-309) → gás (20-310, 20-311) → An_MEIn (20-307; bezerro com leite: caminho alternativo) → 20-316/317, 20-312..315.
6. Balanços e disponibilidade (20-324..329), produção permitida (20-330..339).
7. Dejetos e água (20-340..349) — dependem das excreções minerais (20-343..345), que dependem dos An_Xx_prod de 4.8 ⇒ calcular minerais antes de Man_MacroMinOut/Man_MicroMinOut e Man_WaOut.
8. Eficiências (20-350..369).
9. Minerais (20-370..490) e vitaminas (20-491..496): independentes entre si, só dependem de An_BW, An_DMIn, ganho, gestação, leite e CAs.
Dependências externas citadas: Eq. 20-2, 20-3 (LCT/UCT), 20-21/20-22 (DMIn), 20-56, 20-57, 20-74, 20-82, 20-83, 20-87 (fluxos ruminais), 20-98, 20-120, 20-138, 20-162, 20-166 (excreção fecal), 20-185, 20-215, 20-216 (leite) e Tabela 6-5 (composição de AA), Cap. 6 (eficiências-alvo), Cap. 19 (biblioteca de alimentos: Fd_acXx).
Observação: fórmulas "Clf" (bezerro) e o ramo de aporte de EM para bezerros alimentados com leite estão apenas parcialmente neste bloco.

## 8. Limitações, incertezas e mudanças vs. NRC 2001
- Kg_MP_NP: a composição de AA da PM afeta a eficiência e não foi considerada [p.503].
- Custos de locomoção em confinamento ignorados (pequena subestimação se o lote é longe da ordenha); considerar atividade em pastagem [p.503].
- Produção permitida por energia/proteína: guias na melhor das hipóteses; superfícies de resposta (Milk_NP, Milk_Fat) são preferíveis; muito tendenciosas, comparadas ao sistema do NRC (2001) que tinha viés de inclinação severo [p.508, 523].
- Eficiências de AA/PL "ajuste análogo com An_MPIn não realizado" [p.510].
- Gestação é praticamente ignorada na produção permitida [p.508].
- Faixa superior de produção nos dados de avaliação não alcança rebanhos atuais de alta produção → extrapolação [p.523].
- Dados de avaliação não são independentes para proteína/gordura/leite [p.520, 523]; "avaliações independentes adicionais são necessárias".
- Mudanças vs NRC 2001 citadas neste bloco: produção de proteína e gordura do leite agora estimadas (antes não); leite predito empiricamente a partir de proteína e gordura previstas (CCC 0.75, RMSE 14.6%) vs. abordagem NRC (viés de inclinação severo) [p.523].
- Mantença de proteína: composição por urina endógena (ureia, 3MH, PD, creatinina, creatina, hipúrico) como na Eq. 20-287 a 20-293.
- Fe sem exigência de mantença; Co/I/Se/S sem partição fatorial completa; Co para bezerro líquido = 0.

## 9. Conceitos e evidências relevantes (AVALIAÇÕES, VARIAÇÃO)
**Resultados por saída (Tabelas 20-13 a 20-16)** [p.522-523]
- IMS de vacas em lactação: pelos fatores do animal (Eq. 20-21) → pequeno viés médio, moderado viés de inclinação, melhor precisão (tabela: RMSE 12.1%, CCC 0.71; texto: "12.4%, 0.70"); por animal + alimento (Eq. 20-22) → viés médio maior (26.8% do MSE), sem viés de inclinação relevante, pior precisão (tabela: 15.9%, 0.54; texto: "17.3, 0.56") → fatores dos alimentos introduzem mais variação do que explicam. ⚠ texto x tabela divergem (ver 10).
- Fluxo ruminal de N: CCC 0.5–0.75, viés médio mínimo, viés de inclinação significativo (ajustados aos mesmos dados). Fluxo de amido: CCC 0.54 (subestimado = degradação ruminal excessiva); NDF: CCC 0.43 na tabela (texto 0.41) (superestimado = degradação inadequada); estas duas são avaliações independentes.
- Fluxo de AA ruminal (Tab. 20-14): CCC 0.43–0.60; RMSE 25–36% da média; todos SUPERESTIMAM (obs − pred negativo: média predita > observada nos 9 AA) (corrigido na verificação: estava "subestimam", contradizendo a seção 5.4); proporção de viés médio no MSE de 0.4 a 21.8% (nota do livro: "pequenas proporções"; a nota de rodapé diz CCC 0.43–0.59, mas a tabela traz máx. 0.60 em Leu — divergência do próprio livro).
- Fecal (Tab. 20-15): CP CCC 0.53, subestimada em 0.20 kg/d, e a subpredição aumenta com a excreção (viés de inclinação positivo = 0.51) → compatível com superestimativa da digestibilidade de PNDR ou PB microbiana; fluxos endógenos (incl. ureia do sangue → proteína microbiana no intestino grosso) podem estar mal capturados. NDF fecal: sem viés médio nem de inclinação, CCC 0.77, RMSE 17.4% (texto 17.7%). Amido fecal: CCC 0.27 (texto "0.19"), baixa previsibilidade (pequena fração de grande entrada); viés negativo (digestibilidade intestinal predita baixa demais; deve aumentar, e mais ainda porque o amido ruminal efluente foi subestimado). AG fecais: CCC 0.80 (texto 0.81), RMSE 27.4% (texto 26.6%), viés de inclinação positivo → digestibilidade ligeiramente superestimada. MO fecal: apenas 14 observações disponíveis para o somatório de nutrientes (para o texto); a Tabela 20-15 mostra N = 448, CCC 0.71 (texto 0.82), RMSE 18.7% (texto 18.6%), viés +0.6 kg/d (texto 0.58): excreção de MO subestimada em média (erros opostos de proteína e amido). Diferenças relativas entre dietas bem capturadas; o viés deve ser constante.
- Leite (Tab. 20-16): proteína CCC 0.75, RMSE 14.4%; gordura CCC 0.62, RMSE 17.1%; leite (empírico) CCC 0.75, RMSE 14.6%, baixo viés; leite suportado por EM (Eq. 20-338) CCC 0.67, RMSE 24.4%, viés de inclinação −0.45; por PM (Eq. 20-339) CCC 0.64, RMSE 22.1%, viés de inclinação 0.43.
**Variação do modelo em relação às especificações de desempenho animal e dieta (análise de incerteza/sensibilidade)** [p.524-527]
- Oito fontes de variação: (1) composição nutricional dos ingredientes; (2) quantidade de cada ingrediente na dieta; (3) quantidade de dieta consumida; (4) tamanho do animal; (5) desempenho animal; (6) variação genética e epigenética; (7) efeitos ambientais; (8) o modelo. As cinco primeiras podem ser avaliadas separadamente; as três últimas só de forma agregada por diferença da variância total (abordagem do comitê com os dados do Cap. 6; St-Pierre, 2016). Os 7 primeiros contribuem para a incerteza do modelo (estrutura e parâmetros).
- Tabelas 20-17/20-18: DP de análises (St-Pierre e Weiss, 2015; Rock River Laboratories); amostragem representativa é crítica; amostra enviesada sempre dá composição enviesada; tabelas de composição do Cap. 19 têm DP mas incluem mais fontes que amostragem/análise.
- Variação de pesagem e entrega da dieta e do conteúdo de MS dos ingredientes não pode ser conhecida retrospectivamente na literatura, mas deve ser avaliada/monitorada na fazenda.
- Simulação: com variâncias das Tabelas 20-17/18 + as listadas, população de **200 observações por dieta** da literatura (reduzida às observações com leite, proteína e gordura do leite → **935 médias de tratamento; 187,000 observações simuladas**) [p.525]. Tabela 20-19: variância total observada (leite 53.7; proteína 46,936 g²/d²; gordura 65,058) vs predita com variância nas entradas e na medição (27.7; 31,532; 37,374); por diferença, o conjunto "modelo + animal + ambiente" tem variância 25.9 (leite), 15,404, 27,684; DP 5.09 kg/d de leite, 124 g/d de proteína, 166 g/d de gordura.
- Especificações de dieta para um nível de produção (Tabela 20-20): mesmos dados, removendo a variância de medição do leite e adicionando a de modelo + animal + ambiente; selecionaram-se observações dentro de ±1 EP da média por dieta para leite/proteína/gordura; calculou-se a variância de cada fator por dieta original e fez-se a média entre dietas (garante que diferenças entre dietas não influenciem). Tamanhos de grupo 1 (animal individual), 4 (maioria dos estudos), 8 e 16 (ensaios de produção), 32–256 (fazenda).
- As estimativas são "superespecificadas" porque o modelo cria covariância nas respostas (ex.: gordura do leite usa AG totais, C16:0, C18:3, Ile e Met absorvidas; uma redução em uma entrada pode ser compensada por outra) → considerar correlações parciais (Tabela 20-21): maiores entre proteína do leite e NDFIn (0.49), StIn (0.47), rOMIn (0.41); gordura com Met absorvida (0.25), DEIn (0.26), C18:3 (0.18), FDN (0.18), Lg (0.17).
- Usos propostos: determinar quando reformular a dieta e se o desempenho animal se desviou significativamente do esperado.

## 11. APLICAÇÃO DO MODELO NO R [p.527]
Tudo que o livro diz (nada mais é informado sobre assinaturas, parâmetros ou formatos):
- O modelo descrito é **codificado em R como uma função** aplicável a uma **tabela de dados** (data frame; uma linha = uma observação/animal-dieta) com `mapply` ou `lapply`; se o conjunto de dados é grande, `mcmapply` ou `parLapply` processam as observações individuais **em paralelo** (OCR leu "memapply"; imagem: "mcmapply").
- A saída da função por observação é **reunida em uma lista de matrizes ou de bancos de dados (data frames)** devolvida ao ambiente de trabalho R; as listas podem ser consolidadas em um único data frame/matriz e **juntadas aos dados observados** para avaliar o desempenho do modelo.
- **Entregue**: o código do modelo e os scripts para executar "as cinco observações" (exemplo de cinco observações; ⚠ o texto não detalha o conteúdo) estão no website da National Academies Press (https://www.nap.edu/catalog/25806) e na pasta `\NASEM\NASEM-Dairy-8\script` após instalar o software.
- Não informado: nomes das funções do modelo, lista de parâmetros, formato/colunas de entrada, formato/campos de saída, dependências de pacotes. Para o simulador: replicar o padrão "uma função por observação (linha) + processamento vetorial/paralelo + saída em lista de data frames", com as saídas listadas em 3.

## 10. Dúvidas/riscos de OCR e de consistência (⚠) 
**10.1 Impressão ambígua / parênteses (conferir com o código R)**
1. Eq. 20-271: parênteses (")" sem "("); posição do ×0.86 (todo o termo?).
2. Eq. 20-272: subscrito "NPr_3" em An_BW de vacas; Eq. 20-273: critério "An_BW < 100" e ausência de linha para BW ≥ 100.
3. Eq. 20-310 (linha de vaca em lactação): agrupamento "Dt_FA + InfRum_FAIn/InfRum_DMIn × 100".
4. Eq. 20-312: 55.5 (equação) vs 55.6 MJ/kg (texto).
5. Eq. 20-376: unidade de MlkNP_Milk (% vs fração; ver Eq. 20-389).
6. Eq. 20-395: estrutura do CA do Mg (onde entra o "−0.08" e o ×100/100).
7. Eq. 20-388: linha do expoente embaralhada na impressão (reconstruída por paralelo com 20-375; 0.05527 e 0.000075 vs 0.05581 e 0.00007 em Ca).
8. K_DE_ME_ClfDry (equação não numerada): critérios; RumDevDisc_Clf não definido.
**10.2 Erros tipográficos prováveis nas equações do livro (transcrição literal mantida)**
Eq. 20-279 (An_NEm), 20-307 (An_GasEIn), 20-299 (Ur_NP_g), 20-302 (unidade kg→g), 20-303 (Fe_NP_g), 20-320 (rótulo/unidade), 20-334 (Fe_NPenduse, Ur_NPenduse; unidade kg/d; Milk_MPuse_Trg), 20-337 (unidade kg/d), 20-380 (Abs_Ca_y), 20-394 (An_P_gr; falta An_P_y), 20-415/20-425/20-437 (sinais "−" em An_Xx_prod), 20-421 (An_Cl_gr vs An_Cl_g), 20-453/454/465/476/489 (unidades g/d em mg/d), 20-395 (rótulo g/d).
**10.3 Divergências texto × equação**
Mn sólido 0.005 (texto) vs 0.05 (Eq. 20-467); Fe 0.10 (texto) sem equação; CAs de Ca/P para bezerro só no texto; Eq. 20-299 usa Ur_NP_g (≠ Ur_NPend_g).
**10.4 Avaliações: texto × tabela**
IMS (texto: RMSE 12.4%/CCC 0.70 vs 17.3/0.56; tabela: 12.1/0.71 vs 15.9/0.54); NDF ruminal CCC (texto 0.41; tabela 0.43); amido fecal CCC (0.19 vs 0.27); AG fecal (0.81/26.6% vs 0.80/27.4%); MO fecal (0.82/18.6%/0.58 vs 0.71/18.7%/0.6; texto fala de "14 observações" mas a tabela traz N = 448); NDF fecal RMSE 17.7 vs 17.4%. Tabela 20-11 duplica a 20-13 (a tabela real de características dos animais não existe na impressão). Tabela 20-16: rótulos de linha deslocados (reconstrução validada). Tabela 20-19: rótulo "Observado" repetido no 2º bloco. Tabela 20-20: variância vs DP; unidade de Dt_DEIn nos blocos 1 e 3.
**10.5 Dígitos de OCR corrigidos pela imagem** (todos já aplicados): 20-276 (0.0067), 20-296 (×0.001), 20-300, 20-309 (0.0143), 20-372 (−0.139), 20-419 (0.8), Tabela 20-12 (várias), 20-14 (Arg 119), 20-16 (reconstrução), 20-17 (DDG Cu 2.2; soja 2.71), 20-19 (28.2), 20-20 (12.83).
**10.6 Células pequenas lidas a 150–300 dpi**: expoentes das Eq. 20-375 e 20-388 (impressão pequena; lidos a 300 dpi). Equações de bezerros (Clf) com constantes de pequenos expoentes (−0.139, −0.027, −0.036, −0.045, −0.048): conferir contra o código R oficial se possível.
**10.7 Itens NÃO informados no livro (para o dev decidir)**: fórmula de ponderação do Km do bezerro; unidade de Dt_K em Eq. 20-340; definição de RumDevDisc_Clf, Kx_MP_NP, Ky_MP_NP, An_BW_NPr_3; limite do crédito de vitamina E de pasto; conteúdo das "cinco observações" do software R.

COBERTURA: páginas lidas 504–528 (+503 como contexto), todas conferidas contra imagens (150 dpi; zoom 220–300 dpi em Eq. 20-271, 20-282, 20-307, 20-310, 20-375, 20-387/388, 20-395 e Tabelas 20-14/20-15). Equações numeradas capturadas: 20-271 a 20-496 (226: 20-276→20-496 = 221 no intervalo + 5 do contexto da p.503) + 1 equação não numerada (K_DE_ME_ClfDry) + 1 tabela de topografia + lista de CAs de bezerros; Tabelas 20-11 a 20-21 (11, sendo a 20-11 duplicata da 20-13). P.528 (referências: Bell 1995; Bell et al. 1995; Bibby e Toutenberg 1977; Derrig et al. 1974; Ferrell et al. 1976; Hanigan et al. 1998, 2009; Hayirli et al. 2003; House e Bell 1993; Koong et al. 1975; Li et al. 2019; Lin 1989; NRC 2001; Orskov 1992; Spires et al. 1975; St-Pierre 2016; St-Pierre e Weiss 2015; Storry et al. 1974; Tedeschi e Fox 2020; Tyrrell e Reid 1965) só percorrida (lista continua na p.529, fora do escopo). Fora do arquivo: eficiências "adicionais para relatórios" (não apresentadas no livro), equações de aporte de energia de bezerros com leite (não neste bloco).

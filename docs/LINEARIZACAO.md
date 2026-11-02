# Linearização do simulador/otimizador: estudo e especificação

**Versão:** 0.1 (rascunho para avaliação) · **Data:** 01/11/2026 · **Autor(es):** _[a preencher]_
**Relacionado:** [PRD](PRD.md) · [FSD](FSD.md) · [DOMINIO](DOMINIO.md) · [DECISOES_TECNICAS](DECISOES_TECNICAS.md)

> **Status:** estudo e especificação. **Nada aqui está implementado.** O texto descreve (a) como o RuFaS v1.0.6 calcula a
> ração, lido diretamente no código de `vendor/RuFaS`, e (b) como esse cálculo será linearizado no módulo ampliado do
> "Exercício do quadro". Onde um fato não foi verificado, o texto diz **"a verificar"**; onde a decisão é nossa e
> ainda precisa de confirmação, diz **"(a confirmar)"**.

---

## 1. Contexto e decisões

O professor pediu que as equações do nosso simulador/otimizador sejam **lineares**: as equações não lineares do RuFaS
precisam ser **linearizadas** na nossa aplicação, para podermos comparar o nosso otimizador (programação linear) com o do
RuFaS (programação não linear, `SLSQP`).

### 1.1 Decisões já tomadas

| ID | Decisão | Origem |
|---|---|---|
| L-D1 | O módulo ampliado do "Exercício do quadro" recebe as **características da vaca**, as **exigências e restrições nutricionais** dela, a **dieta** escolhida e os **preços** dos alimentos. | Pedido do professor |
| L-D2 | **Documento principal: NASEM 2021**, onde o RuFaS teve maior influência. **Apoio: NRC 2001.** **Preços: CEPEA**, em **dólares** (as conversões de moeda ficam para depois). | Alinhamento de 01/11/2026 |
| L-D3 | Categorias: **só as que o RuFaS trabalha** (seção 2), "sem mais nem menos". | Alinhamento de 01/11/2026 |
| L-D4 | A entrada é uma **dieta já montada**. O módulo deve **testar várias dietas e compará-las**, da menos recomendada até a ótima. **Sugerir** a dieta ótima para uma vaca e uma fase específicas é uma funcionalidade **posterior** (fase 2). | Alinhamento de 01/11/2026 |
| L-D5 | **Seguir o RuFaS onde o RuFaS diverge do livro**, porque o simulador será integrado ao RuFaS depois. Exemplo: o amido total entra na digestibilidade da FDN em **kg**, e o livro usa **% da MS** (seção 4.7). A divergência fica **registrada** para validação futura. | Alinhamento de 01/11/2026 |

### 1.2 Premissa central

**A linearidade é exigida só nas variáveis de decisão: as quantidades `x_i` (kg de matéria seca por dia) de cada
alimento `i`.** As exigências da vaca são funções não lineares das características do animal (por exemplo `PC^0,75` e
`e^(−0,053·DEL)`), mas são calculadas **antes** do otimizador e entram como **constantes** no lado direito das
restrições. Elas **não** precisam ser linearizadas.

---

## 2. Escopo: as categorias que o RuFaS trabalha

Verificado em `animal_types.py`, `animal_combination.py` e `ration_optimizer.py`.

| Tipo de animal (`AnimalType`) | Lote (`AnimalCombination`) | Passa pelo otimizador? | Restrições no modo NRC | Restrições no modo NASEM | No módulo |
|---|---|---|---|---|---|
| Vaca em lactação (`LAC_COW`) | `LAC_COW` | Sim | Conjunto completo (seção 3) | Conjunto NASEM (seção 3) | **Sim** |
| Novilha I e II (`HEIFER_I`, `HEIFER_II`) | `GROWING` | Sim | Conjunto completo **sem** `NE_total` e `NE_lactation` | Mesmo conjunto da vaca | **Sim** |
| Novilha III e vaca seca (`HEIFER_III`, `DRY_COW`) | `CLOSE_UP` | Sim | Idem | Mesmo conjunto da vaca | **Sim** |
| Lotes mistos | `GROWING_AND_CLOSE_UP` | Sim | Idem | Mesmo conjunto da vaca | **Sim** (como união dos dois) |
| Bezerra pré-desmame (`CALF`) | `CALF` | **Não**: usa `calf_ration_manager.py`, sem restrições nem otimização | — | — | **Não** (o RuFaS não otimiza) |

Para cada categoria, as exigências vêm das calculadoras do RuFaS (`nasem_requirements_calculator.py` e
`nrc_requirements_calculator.py`), que dependem de `animal_type`.

---

## 3. Inventário do que o RuFaS calcula

Variáveis: `x_i` (kg MS/dia do alimento `i`), `DMI = Σ x_i`. Para cada alimento, as propriedades vêm da biblioteca (`DM`,
`CP`, `NDF`, `EE`, `TDN`, `DE`, `starch`, `Kd`, `N_A`, `N_B`, `dRUP`, `Ca`, `P` etc.). `BW` é o peso médio do lote.

**Classes:** **L** = já linear · **E** = não linear, mas com linearização **exata** · **A** = não linear, com linearização
**aproximada** (precisa de coeficientes de referência).

### 3.1 Resumo das restrições do otimizador

| Restrição (`ration_optimizer.py`) | Modo | Classe | Seção |
|---|---|---|---|
| Objetivo: `Σ preço_i · x_i` | ambos | L | 4.1 |
| Limites por alimento (`lower_limit`, `limit`) | ambos | L | 4.1 |
| `DMI_constraint_lower` e `DMI_constraint_upper` | ambos | L | 4.1 |
| `calcium_constraint`, `phosphorus_constraint` | ambos | L | 4.2 |
| `NDF_constraint_lower/upper`, `forage_NDF_constraint`, `fat_constraint` | ambos | E | 4.3 |
| `NE_maintenance_and_activity_constraint`, `NE_lactation_constraint`, `NE_growth_constraint` | NRC | A | 4.4 |
| `NE_total_constraint` (usa o **máximo** de três ofertas) | NRC (só vaca) | A + disjunção | 4.4 |
| `NASEM_net_energy_constraint` | NASEM | A | 4.5 |
| `protein_constraint_lower`, `protein_constraint_upper` | ambos (ver 4.6) | A + `min` | 4.6 |

### 3.2 Exigências (parâmetros, não variáveis)

Entradas da calculadora de exigências (assinatura de `calculate_requirements`, modo NASEM):
`body_weight`, `mature_body_weight`, `day_of_pregnancy`, `body_condition_score_5`, `days_in_milk`,
`average_daily_gain_heifer`, `animal_type`, `parity`, `calving_interval`, `milk_fat`, `milk_true_protein`,
`milk_lactose`, `milk_production`, `housing`, `distance`, `lactating`, `ndf_percentage` e
`process_based_phosphorus_requirement`. Saída: energia de mantença, crescimento, gestação, lactação e atividade;
proteína metabolizável; cálcio; fósforo; consumo estimado; aminoácidos essenciais. São constantes para o problema linear.

Verificado em 01/11/2026: (i) as calculadoras NRC e NASEM rodam **sem uma simulação inteira**, para as seis categorias;
(ii) `average_daily_gain_heifer` é em **kg/dia** (0,8), embora o texto de ajuda do RuFaS diga g; com 800 os valores explodem;
(iii) o NRC pede ainda TDN% (fração) e, para novilhas, temperatura anterior e concentração de energia líquida da dieta, que
dependem da dieta avaliada.

---

## 4. Formulação por restrição e linearização

### 4.1 Custo, limites e consumo (classe L)

```
minimizar    Σ p_i · x_i                                   (p_i em US$/kg MS)
sujeito a    l_i ≤ x_i ≤ u_i                               (limites por alimento, kg MS/dia)
             DMI_min ≤ Σ x_i ≤ DMI_max
             DMI_min = 0,70 · DMI_req(atual)       (DMI_constraint_lower)
             DMI_max = 1,30 · DMI_req(inicial)     (DMI_constraint_upper; DMI_CONSTRAINT_FRACTION = 0,30)
```

O RuFaS usa o consumo estimado **atual** no mínimo e o **inicial** no máximo. Isso é fiel ao código e deve ser mantido
(L-D5). Observação: o teto de +30% é folgado em relação ao erro típico da equação de consumo do NASEM (12,1%); ver
[DOMINIO](DOMINIO.md), seção 8.

### 4.2 Cálcio e fósforo (classe L)

Coeficientes de digestibilidade por tipo de alimento (`calculate_calcium_supply`, `calculate_phosphorus_supply`):

| Tipo | Cálcio | Fósforo |
|---|---|---|
| Forragem (`Forage`) | 0,30 | 0,64 |
| Concentrado (`Conc`) | 0,60 | 0,70 |
| Mineral (`Mineral`) | 0,95 | 0,80 |

```
oferta_Ca = 1000 · Σ x_i · dCa_tipo(i) · Ca_i / 100   ≥  exigência_Ca
oferta_P  = 1000 · Σ x_i · dP_tipo(i)  · P_i  / 100   ≥  max(exigência_P, exigência_P_processo)
```

### 4.3 Fibra e gordura (classe E: razão com linearização exata)

As restrições são razões entre uma soma ponderada e o consumo. Com `DMI > 0`, multiplica-se por `DMI` e obtém-se uma
restrição linear **equivalente**, sem aproximação:

| Restrição no RuFaS | Forma linear exata | Constante |
|---|---|---|
| `Σ x_i·NDF_i / Σ x_i ≥ 25` | `Σ x_i · (NDF_i − 25) ≥ 0` | `MINIMUM_RATION_NDF = 25` |
| `Σ x_i·NDF_i / Σ x_i ≤ 45` | `Σ x_i · (NDF_i − 45) ≤ 0` | `MAXIMUM_RATION_NDF = 45` |
| `Σ_{forragens} x_i·NDF_i / Σ x_i ≥ 15` | `Σ x_i · (NDFf_i − 15) ≥ 0`, com `NDFf_i = NDF_i` se `Forage`, senão 0 | `MINIMUM_RATION_FORAGE_NDF = 15` |
| `Σ x_i·EE_i / Σ x_i ≤ 7` | `Σ x_i · (EE_i − 7) ≤ 0` | `MAXIMUM_RATION_FAT = 7` |

### 4.4 Energia no modo NRC (classe A, mais disjunção)

**Desconto de ingestão `D(x)`** (`calculate_nutrient_intake_discount`):

```
TDN_tot = Σ x_i · TDN_i / 100                 (kg)
TDN%    = 100 · TDN_tot / DMI
se TDN% < 60  ou  TDN_tot < 0,035 · BW^0,75 :  D = 1
senão:  M = TDN_tot / (0,035 · (0,96·BW)^0,75)
        D = max( (TDN% − (0,18·TDN% − 10,3)·(M − 1)) / TDN% ,  0,6 )
```

`D` é uma função racional de `x`: **não linear**. Mas é um **escalar único** para a ração inteira.

**Descontinuidade.** O NRC define `D = 1` para dietas com TDN1X **de 60% ou menos** (Eq. 2-9 e o texto do cap. 2); o
RuFaS usa `TDN% < 60`. Logo `D(x)` é **descontínua** em `TDN% = 60`: a consumo alto, o salto é de ≈ 3,5% (por
exemplo, `D = 1,0` em 59,5% e `D = 0,965` em 60,5%, com consumo de 33 kg). O estudo da seção 10 mostra que o
otimizador do RuFaS **explora esse salto**. Outra diferença: o NRC limita o **TDN descontado** a no mínimo 60%; o RuFaS
limita o **fator** `D` a no mínimo 0,6 (`MINIMUM_TDN_DISCOUNT`).

**Por alimento, dado `D`** (`feeds`: mineral = 0 em tudo; "gordura" = `is_fat`):

```
DE_i^a = DE_i · D                                          (energia digestível ajustada)
ME_i   = gordura:  DE_i
         EE_i ≥ 3: 1,01·DE_i^a − 0,45 + 0,0046·(EE_i − 3)
         demais:   1,01·DE_i^a − 0,45
NEl_i  = gordura:  0,8·DE_i^a
         EE_i ≥ 3: 0,703·ME_i − 0,19 + ((0,097·ME_i + 0,19)/97)·(EE_i − 3)
         demais:   0,703·ME_i − 0,19
NEm_i  = gordura:  0,8·ME_i
         demais:   1,37·ME_i − 0,138·ME_i² + 0,0105·ME_i³ − 1,12
NEg_i  = gordura:  0,55·ME_i
         demais:   1,42·ME_i − 0,174·ME_i² + 0,0122·ME_i³ − 1,65
oferta_k = Σ x_i · NEk_i        (k = m, l, g)
```

Com `D` **fixo**, todos os `NEk_i` são **constantes por alimento** (os polinômios cúbicos passam a ser números), e a
oferta `Σ x_i·NEk_i` é **linear** em `x`. A não linearidade do problema está só em `D(x)`.

**Restrições (vaca):**

```
NEm:    oferta_m ≥ exigência_mantença + exigência_atividade
NEl:    oferta_l ≥ exigência_lactação + exigência_gestação
NEg:    oferta_g ≥ exigência_crescimento
Total:  max(oferta_m, oferta_g, oferta_l) ≥ exigência_total
```

A restrição **Total** é uma **disjunção** (ao menos uma das três ofertas cobre a exigência total). **Tratamento:** resolver
**um LP por ramo** (`k = m`, `l`, `g`) e ficar com o de menor custo; na prática, `g` raramente importa (seção 5.4).
Novilhas e vacas secas não têm `NE_total` nem `NE_lactation` no modo NRC.

### 4.5 Energia no modo NASEM (classe A)

`NASEM_net_energy_constraint` vale para **todas** as categorias:

```
DE_i(x) = 0,042·NDF_i·dNDF_i + 0,0423·St_i·dSt_i + 0,0940·FA_i·0,73
        + 0,0565·(RDP_i + RUP_i·dRUP_i/100 − NPN_i) + 0,0089·NPN_i + 0,040·ROM_i·0,96 − 0,318
dNDF_i  = [0,75·(NDF_i − Lig_i)·(1 − (Lig_i/NDF_i)^0,667)]/NDF_i − 0,0059·(S_tot − 26) − 1,1·(DMI/BW − 0,035)
dSt_i   = St_dig_i/100 − 1,0·(DMI/BW − 0,035)
S_tot   = Σ x_j · St_j / 100                                 (em kg: ver 4.7)
DE_tot  = Σ x_i · DE_i(x)
ME_tot  = DE_tot − 13,28·CH4 − 0,0146·UN         (CH4 convertido para kg e UN para g; ambos do lote)
NE      = 0,66 · ME_tot   ≥   exigência_total
```

`dNDF_i` e `dSt_i` são **afins** em `(S_tot, DMI)`, portanto `x_i·DE_i(x)` é **quadrático** em `x`. Com `S_tot` e `DMI`
**congelados** num valor de referência, cada `DE_i` vira uma constante e a restrição fica **linear**.
`CH4` e `UN` são constantes do lote no RuFaS (`pen_average_enteric_methane`, `pen_average_urine_nitrogen`); ver 7.3.

### 4.6 Proteína metabolizável (classe A, com `min`)

O otimizador chama `calculate_metabolizable_protein_supply` (método do **NRC 2001**) **nos dois padrões**: no modo NASEM,
o RuFaS usa a **oferta** de proteína do NRC contra a **exigência** do NASEM (**a verificar**; é o que o código do
otimizador mostra).

```
pbw   = 100·DMI/BW ;   %conc = 100·Σ_{Conc} x_i / DMI
k_i   = Conc:                      2,904 + 1,375·pbw − 0,02·%conc
        Forage e não úmida:        3,362 + 0,479·pbw − 0,017·NDF_i − 0,007·%conc
        úmida (is_wetforage):      3,054 + 0,614·pbw
RDP_i = (Kd_i/(Kd_i + k_i))·(N_B_i/100)·CP_i + (N_A_i/100)·CP_i        (se k_i > −Kd_i; senão 0)
RUP_i = CP_i − RDP_i
PMmic = 0,64 · min( 0,13·1000·Σ x_i·TDN_i·D/100 ,  0,85·1000·Σ x_i·RDP_i/100 )
PMrup = 1000 · Σ x_i · (RUP_i/100) · (dRUP_i/100)
PMend = 0,4 · 11,8 · DMI
PM    = PMmic + PMrup + PMend                          (g/dia)
PM ≥ exigência_PM                       (protein_constraint_lower)
PM ≤ 1,5 · exigência_PM(inicial)        (protein_constraint_upper; PROTEIN_UPPER_LIMIT_FACTOR = 1,5)
```

Não linearidades: `D(x)`, `pbw(x)` e `%conc(x)` (razões em `x`), a razão `Kd/(Kd + k)` e o `min`.
**Tratamento:**
- **Congelar** `D`, `pbw` e `%conc` na referência: `k_i`, `RDP_i`, `RUP_i` viram constantes por alimento.
- **`min`, restrição inferior:** `min(a,b) + c ≥ r` equivale a **duas** restrições lineares, `a + c ≥ r` **e** `b + c ≥ r`
  (exato).
- **`min`, restrição superior:** `min(a,b) + c ≤ U` equivale a `a + c ≤ U` **ou** `b + c ≤ U`. Impor o ramo que é o mínimo na
  referência e **verificar** a outra no fim (seção 6).

### 4.7 Anomalias do RuFaS que o módulo replica (L-D5)

| Item | O RuFaS faz | O livro diz | Efeito estimado |
|---|---|---|---|
| Amido total em `dNDF_i` (4.5) | `S_tot` em **kg** (`Σ x_j·St_j/100`) | `Dt_St` em **% da MS** (Eq. 3-5a) | A digestibilidade da FDN fica ≈ 0,1 acima; para uma dieta com 35% de FDN, a energia digestível sobe ≈ 0,15 Mcal/kg MS (**estimativa, a confirmar com o código R oficial**) |
| Oferta de proteína no modo NASEM | Método do NRC (4.6) | O NASEM tem outro sistema de proteína (cap. 6) | Oferta e exigência de padrões diferentes (**a verificar**) |
| Ponto de partida do `SLSQP` | `random.random()·10` se não há ração anterior | — | O ótimo do RuFaS é local; em 30 execuções o custo variou 0,1% (seção 10) |
| FDN padrão da ração anterior (calculadora NASEM) | `DEFAULT_NDF_PERCENTAGE = 0,3` (fração) vai à calculadora, que espera **porcentagem** | `NDF_conc` em % (cap. 6) | Sem ração anterior, a PM exigida fica ≈ 5% menor que com 33% (verificado em 02/11/2026; vaca de 650 kg e 40 kg de leite); o módulo replica e avisa |
| Piso do desconto de ingestão | Fator `D ≥ 0,6` | TDN **descontado** ≥ 60% (NRC, cap. 2), isto é, `D ≥ 60/TDN1X` | Para TDN1X de 70%, o piso do NRC é 0,857 e o do RuFaS é 0,6; raramente é atingido (`D` de 0,855 a 0,94 nas rações guardadas) |

---

## 5. Técnicas de linearização

| Técnica | Quando | Exatidão |
|---|---|---|
| **A. Transformação exata** | Razões (4.3); `min` na restrição inferior (4.6) | Exata |
| **B. Congelamento e ponto fixo** | `D(x)`, consumo, `%conc`, amido total (4.4 a 4.6) | Exata **no ponto de referência**; o erro cresce com a distância; **pode parar num ponto subótimo** (5.1 e seção 10) |
| **F. Parametrização dos escalares globais** (recomendada) | `D(x)`, passagem ruminal e consumo dependem de poucos escalares: `DMI`, `TDN%` e `%conc` | **Exata em cada ponto da grade**: fixar os escalares como **parâmetros** e impor as igualdades lineares `Σx = DMI`, `Σ TDN_i·x_i = TDN%·DMI`, `Σ_{conc} x_i = (%conc/100)·DMI`; o erro vira o passo da grade |
| **C. Taylor de 1ª ordem (programação linear sucessiva)** | Se B não chegar perto do RuFaS | Inclui a sensibilidade dos coeficientes a `x`; exige região de confiança |
| **D. Enumeração de ramos** | Disjunções (`max` de NE; `min` na restrição superior) | Exata (um LP por ramo) |
| **E. Linearização por partes com variáveis inteiras** | Descartada | Quebra os preços-sombra e deixa de ser PL |

### 5.1 Ponto fixo (técnica B)

```
1. Referência x⁰ (a dieta informada; na fase 2, uma ração inicial)
2. Calcular escalares globais: DMI, %conc, TDN%, D, S_tot (e, no NASEM, dNDF_i e dSt_i)
3. Calcular os coeficientes por alimento: NEk_i, DE_i, RDP_i, RUP_i, ... (constantes)
4. Montar e resolver o LP (por ramo, se houver disjunção)  →  x¹
5. Recalcular os escalares em x¹ e repetir até convergir
```

**Convergência (a confirmar):** `max_i |x_i^{n+1} − x_i^n| < 1e-4 kg` e variação relativa do custo `< 0,01%`, máximo de 20
iterações. Se oscilar, amortecer a atualização (`x ← x_anterior + 0,5·(x_novo − x_anterior)`).

**Propriedade importante:** no ponto fixo, os coeficientes são avaliados **na própria solução**, então a solução do LP
satisfaz as restrições **não lineares originais**. A solução é **viável** para o problema do RuFaS; mas pode ser
**subótima**, e o estudo numérico mostrou que a diferença **não é pequena**: o ponto fixo convergiu para um custo **4,8%
acima** do melhor do RuFaS, porque a iteração não enxerga a descontinuidade em `TDN% = 60` (seção 10).

### 5.1b Método recomendado: parametrização dos escalares globais (técnica F)

```
para cada ponto (DMI, TDN%, %conc) de uma grade (e, depois, de um refinamento local):
    calcular D, as taxas de passagem e os coeficientes por alimento nesses escalares   (constantes)
    resolver o LP (um por ramo da disjunção de energia e do `min` de proteína)
        com as igualdades lineares  Σx = DMI,  Σ TDN_i·x_i = TDN%·DMI,  Σ_{conc} x_i = (%conc/100)·DMI
escolher o ponto de menor custo
```

- **Exatidão:** em cada ponto, os escalares do LP **coincidem** com os da solução; a solução satisfaz as restrições
  originais (folga mínima de −5e-13 no estudo). Não há erro de linearização, só o erro da grade.
- **Descontinuidade:** tratar como **dois regimes**: `TDN% ≤ 60` (`D = 1`, energia independente do consumo) e `TDN% > 60`
  (`D < 1`). Em cada regime a formulação é suave.
- **Custo computacional:** 3.536 pontos × 6 LPs em 24 s (seção 10); a dimensão é 3, então a grade é barata.
- A técnica **C (Taylor)** e o **ponto fixo (B)** ficam como refinamentos locais dentro de um regime.

### 5.2 Região de operação

O consumo é limitado a ±30% do estimado, e `D` não varia muito. Nas simulações guardadas, `D` ficou entre **0,86 e 0,94**.
Isso justifica o congelamento como primeira aproximação e delimita o erro esperado.

### 5.3 Disjunção `max(NEm, NEl, NEg) ≥ exigência total`

Replicando as fórmulas da seção 4.4 sobre três rações guardadas (vaca em lactação, preços ilustrativos):

| Ração | Consumo (kg) | TDN% | `D` | `oferta_m` | `oferta_l` | `oferta_g` | Exigência de lactação | Exigência de mantença |
|---|---|---|---|---|---|---|---|---|
| 1 | 29,6 | 66,6 | 0,908 | 41,7 | 42,0 | 24,3 | 31,2 | 10,0 |
| 2 | 29,8 | 63,9 | 0,935 | 41,9 | 42,0 | 24,7 | 31,2 | 10,0 |
| 3 | 32,0 | 70,5 | 0,855 | 44,8 | 45,9 | 26,1 | 31,2 | 10,0 |

- Nas rações 1 e 2, a oferta calculada fica a ≈ 1% da soma das exigências de mantença, lactação e crescimento
  (≈ 41,7 Mcal; gestação e atividade não entram nessa soma, **a verificar**): a replicação reproduz a restrição ativa do
  RuFaS, o que apoia as fórmulas da seção 4.4. Na ração 3 a oferta passa 7% a 10% da exigência, porque outra restrição
  (por exemplo, fibra ou gordura) deve estar ativa.
- `oferta_m` e `oferta_l` ficam a menos de 3% uma da outra: **os dois ramos competem** e precisam ser resolvidos.
- `oferta_g` fica bem abaixo da exigência total: o ramo `g` pode ser descartado na prática, mas o LP o verifica.

### 5.4 Resultado esperado da comparação com o RuFaS

- O RuFaS resolve um problema **não convexo** a partir de um ponto inicial, e obtém um ótimo **local**; o LP linearizado
  obtém o ótimo **global do problema linearizado**. Por isso o custo do LP pode ser **menor**.
- Protocolo de comparação: avaliar a ração do RuFaS com as funções **originais** e com as **linearizadas**; a diferença
  é o **erro de linearização**.
- Métricas: custo (US$/dia), ração (kg por alimento), folga de cada restrição, erro de linearização por restrição.

---

## 6. Verificação do erro de linearização

Ao final de cada resolução, avaliar **todas** as restrições com as funções **originais** (não lineares) na solução:

| Medida | Definição | Tolerância (a confirmar) |
|---|---|---|
| Erro de oferta | `(oferta_não_linear − oferta_linear) / exigência` | ≤ 1% por restrição, **com os coeficientes congelados e as quantidades variando até ±5%** (a ±10% o erro de energia chegou a 1,2% a 1,5%; seção 10) |
| Violação | `max(0, exigência − oferta_não_linear)` | 0 nas restrições de piso |
| Ramo da disjunção | O ramo escolhido continua o de maior oferta? | Sim |

Se uma tolerância falhar: repetir o ponto fixo; se persistir, passar à técnica C.

---

## 7. O módulo "Exercício do quadro" ampliado

### 7.1 Entradas

| Grupo | Conteúdo | Fonte |
|---|---|---|
| **Vaca** | As características da seção 3.2 (peso, paridade, dias em lactação, produção e composição do leite, gestação, escore de condição corporal, alojamento, distância, etc.) e a **categoria** (seção 2) | Usuário |
| **Exigências** | Calculadas pelo RuFaS (NASEM) para a vaca informada; o usuário pode **sobrescrever** | NASEM (principal), NRC (apoio) |
| **Restrições** | Fibra, gordura, consumo, proteína, cálcio e fósforo (seções 4.1 a 4.6) | Constantes do RuFaS; Tabela 5-1 do NASEM como verificação |
| **Dieta** | Uma ou várias dietas **já montadas**: lista de alimentos com `x_i` (kg MS/dia) | Usuário |
| **Preços** | Por alimento, em US$ (seção 7.2) | CEPEA |
| **Padrão** | NASEM (principal) ou NRC | Usuário |

### 7.2 Preços (CEPEA, em dólares)

Os indicadores do CEPEA costumam ser em **R$ por unidade comercial** (por exemplo, saca de 60 kg) e na **matéria natural**;
o modelo usa **US$/kg de MS**. Regra de conversão a registrar (as taxas e o mapeamento ficam para depois):

```
preço (US$/kg MS) = preço_original / (kg por unidade comercial) / (MS do alimento, fração) / câmbio (R$ por US$)
```

Campos por preço: valor original, unidade comercial, moeda, `câmbio`, base (matéria natural ou MS), fonte (indicador
CEPEA e data). O mapeamento entre os indicadores do CEPEA e os alimentos da biblioteca é **a verificar**.

### 7.3 Entradas do lote que o RuFaS usa na energia do NASEM

`pen_average_enteric_methane` (g/dia) e `pen_average_urine_nitrogen` (kg) são **saídas do RuFaS** para o lote. Para uma
vaca isolada, o módulo precisa **recebê-las** ou **estimá-las** pelas equações do NASEM (metano e nitrogênio urinário,
Eq. 3-9 e 3-10a), também congeladas na referência. No RuFaS esses dois valores são a **média do lote** dos valores do dia
anterior de cada animal (só o NASEM os usa), e não existem para uma vaca isolada. **Decisão pendente (L-Q2).**

### 7.4 Comparação de dietas (L-D4)

Para cada dieta `d` informada:
1. Calcular oferta e folga de cada restrição, linearizadas **na própria dieta** (coeficientes avaliados em `x_d`).
2. Calcular o custo `Σ p_i·x_i`.
3. Classificar: **viável** (todas as restrições cumpridas) ou **inviável** (soma das violações normalizadas
   `V = Σ max(0, (exigência − oferta)/exigência)` maior que zero).

**Ordem de apresentação, da menos para a mais recomendada** (a confirmar):
1. Inviáveis, em ordem **decrescente** de `V`.
2. Viáveis, em ordem **decrescente** de custo.
3. **Dieta ótima** do LP (fase 2), quando existir, como referência final, com o **desvio** de cada dieta em relação a ela
   (`(custo_d − custo_ótimo)/custo_ótimo`).

### 7.5 Saídas

Para cada dieta: custo (US$/dia), folga e estado de cada restrição, erro de linearização (seção 6) e, no padrão NASEM, a
verificação da Tabela 5-1 (FDN de forragem, FDN total, amido). Os **preços-sombra** das restrições ativas (US$ por
unidade da exigência) só existem quando um LP com `x` livre é resolvido: na fase 2 (dieta ótima) ou numa dieta de
referência; avaliar uma dieta já montada não os produz.

### 7.6 Fase 2 (posterior)

Sugerir e prever a dieta ótima para uma vaca e uma fase específicas: resolver o LP da seção 4 com `x_i` livres, pelo
ponto fixo (seção 5.1), para cada fase da lactação. O laço de redução de leite do RuFaS (0,25 kg por tentativa, quando a
ração é inviável) passa a ser um laço externo sobre LPs.

---

## 8. Pendências e perguntas

| ID | Questão | Proposta (a confirmar) |
|---|---|---|
| L-Q1 | Tolerâncias de convergência e de erro de linearização (seções 5.1 e 6) | Valores propostos acima; o estudo numérico sustenta ≤ 1% para variações de até ±5% |
| L-Q2 | Metano e nitrogênio urinário do lote para uma vaca isolada (7.3) | Estimar pelo NASEM e congelar |
| L-Q3 | Mapeamento CEPEA × biblioteca de alimentos; arroz em grão (RF-26) | A verificar com o professor |
| L-Q4 | O amido em kg (4.7) deve ser replicado em todas as comparações? | Sim (L-D5); registrar a diferença quando o módulo estiver completo |
| L-Q5 | Critério final de ordenação das dietas (7.4) | Proposta acima |
| L-Q6 | A oferta de proteína do NRC no modo NASEM (4.6) é intencional no RuFaS? | Perguntar ao professor |
| L-Q7 | Como representar a vaca recém-parida (início de lactação), em que a equação de consumo precisa ser integrada para grupos com menos de 90 dias (NASEM, p. 476)? | A estudar |
| L-Q8 | A **descontinuidade** do desconto de ingestão em `TDN% = 60` e o piso do fator `D` em 0,6 (4.4 e 4.7): são intencionais no RuFaS? O RuFaS replica o NRC (que define `D = 1` para TDN1X ≤ 60%), mas o piso do NRC é outro | Replicar o RuFaS e tratar os dois regimes (5.1b) |

## 9. Fontes

- RuFaS v1.0.6: `RUFAS/biophysical/animal/ration/ration_optimizer.py` (restrições, objetivo, `SLSQP`),
  `RUFAS/biophysical/animal/nutrients/nutrition_supply_calculator.py` (ofertas),
  `nasem_requirements_calculator.py` e `nrc_requirements_calculator.py` (exigências),
  `animal_module_constants.py` (constantes), `animal_types.py`, `animal_combination.py`.
- NASEM 2021, tradução brasileira: capítulos 2 (consumo), 3 (energia, Eq. 3-5a, 3-8 a 3-12), 5 (Tabela 5-1), 6, 7 e 20
  (equações do modelo). Notas em `docs/nasem2021_notas/` (local, não versionada; o texto do livro é protegido por direitos autorais).
- NRC 2001: capítulo 2 (energia, desconto de ingestão), capítulo 5 (proteína), Tabela 15-1 (composição).
- Replicação numérica da seção 5.3: rações em `runs/_cache/`, preços ilustrativos.

---

## 10. Estudo numérico (01/11/2026)

Experimento feito em **scripts descartáveis**, fora do repositório, usando as **funções do próprio RuFaS** v1.0.6 para
calcular as ofertas e as restrições, o `RationOptimizer` (`SLSQP`) do RuFaS como referência, e o HiGHS (SciPy) para os LPs.
**Escopo:** modo NRC, uma vaca, um conjunto de alimentos, preços ilustrativos. Não é uma simulação completa do RuFaS.

### 10.1 Cenário

| Item | Valor |
|---|---|
| Vaca | Lactação, 650 kg, peso à maturidade 700 kg, 100 dias em lactação, 60 dias de gestação, 2ª lactação, ECC 3,0, 40 kg de leite (gordura 3,7%, proteína 3,1%, lactose 4,85%) |
| Exigências (NRC, pelo RuFaS) | Consumo estimado 25,82 kg; PM 2.681 g; Ca 70,9 g; P 64,0 g; energia total 39,6 Mcal (mantença 10,30; lactação 28,71; crescimento 0,59) |
| Alimentos | "Conjunto base": silagem de milho imatura (50), silagem de leguminosa (110), milho moído seco (44), farelo de soja 48% (167), farelo de arroz (138), carbonato de cálcio (230), farinha de sangue (23) |
| Preços e tetos | Preços ilustrativos do sistema; tetos de inclusão padrão |

### 10.2 Resultados

| Método | Custo (US$/vaca/dia) | Consumo (kg) | TDN% | Observações |
|---|---|---|---|---|
| **RuFaS (`SLSQP`), 30 sementes** | 3,8342 (mínimo), 3,8342 (mediana), 3,8382 (máximo) | 33,4 (mediana); máximo permitido 33,57 | 59,7 a 60,0 | 30 de 30 convergiram; variação de custo de 0,1% |
| **LP por ponto fixo** (2 pontos iniciais) | 4,0169 | 27,6 | `D` = 0,937 | 10 e 8 iterações, **mesmo ponto final**; **+4,8%** sobre o RuFaS; restrições originais satisfeitas (folga mínima −1,7e-4) |
| **LP por parametrização** (grade de 3.536 pontos) | 3,8373 | 33,3 | 59,5 | 417 pontos viáveis, 24 s; **+0,08%** sobre o melhor do RuFaS; folga mínima −5e-13 |
| **LP exato nos escalares do melhor RuFaS** (DMI 33,34; TDN% 60,00; conc. 3,67%) | **3,8342** | 33,34 | 60,00 | **Idêntico** ao melhor do RuFaS (4 casas) |

### 10.3 Conclusões

1. **O LP reproduz o RuFaS.** Para os mesmos escalares globais, o LP e o `SLSQP` chegam ao mesmo custo (3,8342): o
   otimizador do RuFaS converge para o ótimo do problema linear **dado** o conjunto de escalares. Isso valida as fórmulas
   da seção 4 e o método da seção 5.1b.
2. **O RuFaS explora a descontinuidade do desconto.** As 30 soluções têm `TDN%` entre 59,7 e 60,0, logo abaixo do ponto em
   que o desconto de ingestão liga (`D = 1`), e consumo próximo do teto de +30%. A ração é barata porque usa silagem em
   grande quantidade, a consumo alto, sem desconto de energia. É consequência de uma regra do próprio NRC, mas é uma
   característica do **modelo**, não de uma dieta realista. O painel de verificações (RF-27) deve sinalizar o consumo.
3. **O ponto fixo simples não basta.** Parando em `D = 0,937` (regime com desconto), ele ficou 4,8% acima do RuFaS, e a
   iteração não escapa. A parametrização dos escalares (5.1b) acha o mesmo ótimo que o RuFaS, em 24 s.
4. **Erro fora do ponto, com coeficientes congelados.** Variando as quantidades da solução do ponto fixo:

| Variação das quantidades | Erro na NEl | Erro na NEm | Erro na PM |
|---|---|---|---|
| −10% | −1,19% | −1,50% | 0,12% |
| −5% | −0,60% | −0,76% | 0,06% |
| +5% | +0,60% | +0,77% | 0,00% |
| +10% | +1,21% | +1,55% | 0,01% |

   A tolerância de 1% vale para variações de até ±5%; a ±10% o erro de energia passa de 1%.
5. **Reprodutibilidade do RuFaS.** O custo varia 0,1% entre 30 sementes, e a ração, um pouco mais; o ótimo local do `SLSQP`
   é praticamente estável neste cenário. A pergunta P12 fica respondida **para este cenário**.

### 10.4 Limites do estudo

- Um cenário (uma vaca, um conjunto de alimentos, preços ilustrativos). Nas três rações de simulações completas examinadas
  (seção 5.3), `TDN%` ficou entre 64 e 71%, no regime com desconto; o resultado dessas simulações não foi reproduzido aqui.
- Só o modo **NRC**. O modo NASEM (energia quadrática em `x`, seção 4.5) **não** foi exercitado.
- A grade tem 3 escalares; o refinamento local foi simples (passos fixos). A otimalidade global da grade não foi provada.
- Os LPs usaram os coeficientes por alimento calculados pelas funções do RuFaS (exatos), mas as restrições de fibra,
  gordura, cálcio e fósforo foram escritas por nós e conferidas pelas funções de restrição do RuFaS no ponto final
  (todas satisfeitas).

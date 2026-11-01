# NASEM 2021 — Cap. 20 (Descrição e Avaliação do Modelo), PARTE B — páginas impressas 485–503

**Capítulo coberto:** 20 — Descrição e Avaliação do Modelo, Parte B (digestão de FDN, proteína, AA e AG; energia bruta/digestível; produção de leite; gestação; crescimento e reservas; início da mantença). Contexto de continuação: p.484 (Eqs. 20-95 a 20-109, digestão de amido e rOM) e p.504 (Eqs. 20-276 a 20-286, só listadas).
**Usado diretamente no modelo? sim** (é o núcleo de cálculo: digestibilidade, aporte de PM/AA, ED, predição de proteína/gordura/volume de leite, gestação, ganho).

Convenções: `^` expoente, `_` subscrito, `*` multiplicação. Prefixos do livro: `Fd_` = alimento (ingrediente f), `Dt_` = dieta (soma dos alimentos), `An_` = animal (dieta + infusões), `Inf_` = infusão (`_Rum` ruminal, `_SI` intestino delgado, `_Bld` sangue/arterial), `Du_` = fluxo duodenal, `Fe_` = fecal, `Abs_` = absorvido, `TT_` = trato total. Sufixos de unidade em nomes: `_g` = g/d; `In` = ingestão. `N_f` = número de alimentos; `a` = índice de AA.
Verificação: cada equação conferida na imagem da página (150 dpi; trechos duvidosos em 230–450 dpi). Correções pela imagem estão marcadas "(corrigido pela imagem)". Itens com ⚠ estão listados na seção final.
Termos usados nesta parte mas DEFINIDOS FORA do intervalo (Parte A / outros capítulos): Fd_DMIn_f, Fd_NDF_f, Fd_Lg_f, Fd_RUPIn_f, Fd_dcRUP_f, Fd_ttdcFA_f, Fd_FA_f, Dt_NDFIn, Dt_StIn, Dt_CPIn, Dt_TPIn, Dt_RUPIn(An_RUPIn), An_RDPIn, An_RDTPIn, An_CPIn, An_TPIn, Du_MiCP, Du_AAMic(a), SI_dcMiCP, fRum, fSI, An_OMIn, An_DMIn, Dt_NPNCPIn, Dt_CFatIn, Dt_rOMIn, Fe_CP, Fe_NPend, Fe_MiCP, Fe_MiTP, AA(a)_NP_*(Tab. 6-5).

---
## 0. Contexto da p.484 (só listagem; fora do intervalo detalhado)
Eqs. 20-95 a 20-98 (amido digerido: An_DigStIn = Dt_DigStIn + Inf_StIn × Inf_ttdcSt/100; An_dcSt; An_DigSt; Fe_St = Dt_StIn + Inf_StIn − An_DigStIn). Eqs. 20-99 a 20-109 (rOM): Fd_DigrOMt_f = Fd_dcrOMt/100 × Fd_rOM_f (dcrOMt fixada em 96.1 %); **Fe_rOMend = 0.034 × Dt_DMIn (kg/d)** [p.484, Eq. 20-100]; Fd_DigrOMa_f = Fd_DigrOMt_f − 3.43; Dt_DigrOMaIn = Dt_DigrOMtIn − Fe_rOMend (Eq. 20-105); Eq. 20-106 inclui infusões: An_DigrOMaIn = Dt_DigrOMaIn + (Inf_GlcIn + Inf_AcetIn + Inf_PropIn + Inf_ButrIn) × (fRum + fSI); Fe_rOMout = An_rOMIn − An_DigrOMaIn (Eq. 20-109). Estimativas aparentes por alimento podem ser negativas (fontes minerais); só a soma da dieta é confiável [p.484].
Este bloco (20-110 em diante) começa na p.485 com a frase que termina na p.484.

---
## 1. Digestão de FDN no trato total [pp.484–485]

**Papel no simulador:** calcula a FDN digerida da dieta: digestibilidade base por alimento (via lignina ou digestibilidade in vitro 48 h), somada na dieta e descontada por efeitos negativos de amido e IMS.

### Equações
**Eq. 20-110** [p.485] — dcFDN base por lignina (por alimento)
```
Fd_dcNDF_Lg  (% of NDF) = 0.75 * (Fd_NDF - Fd_Lg) * [ 1 - (Fd_Lg / Fd_NDF)^0.667 ] / Fd_NDF * 100
```
Fd_dcNDF_Lg = FDN digestível estimada pela lignina (% da FDN); Fd_NDF = FDN do alimento; Fd_Lg = lignina do alimento (mesma unidade de Fd_NDF; razão adimensional). (Fd_NDF − Fd_Lg)/Fd_NDF dá a fração não lignificada. Lê-se: [0.75*(NDF−Lg)*(1−(Lg/NDF)^0.667)/NDF]*100.

**Eq. 20-111** [p.485] — dcFDN base por digestibilidade in vitro 48 h
```
Fd_dcNDF_IV48  (% of NDF) = 12 + 0.61 * Fd_dcNDF_IV48h
```
Fd_dcNDF_IV48h = digestibilidade in vitro de FDN em 48 h (% da FDN), medida do alimento (biblioteca de alimentos).

**Eq. 20-112** [p.485] — seleção da base (opção `Use_dcNDF_IV48`)
```
Fd_dcNDF_Base (%) =
  Use_dcNDF_IV48 = 0 :  Fd_dcNDF_Lg
  Use_dcNDF_IV48 = 1 :  Forage: Fd_dcNDF_IV48 ;  Concentrate: Fd_dcNDF_Lg
  Use_dcNDF_IV48 = 2 :  All Feeds: Fd_dcNDF_IV48
```
Texto: opção 1 = IV48 só para forragens; 2 = todos. Em todos os casos usa-se a estimativa por lignina se os valores IV estiverem ausentes [p.485].

**Eq. 20-113** [p.485]
```
Dt_DigNDFIn_Base (kg/d) = SUM_{f=1..N_f} ( Fd_dcNDF_Base_f * Fd_NDF_f * Fd_DMIn_f )
```
⚠ As unidades são impressas sem "/100": Fd_dcNDF_Base_f é % da FDN e Fd_NDF_f é (nas bibliotecas) % da MS; para obter kg/d é preciso dividir por 100 cada fator em %. Ver ⚠.

**Eq. 20-114** [p.485]
```
Dt_dcNDF_Base (% of NDF) = Dt_DigNDFIn_Base / Dt_NDFIn * 100
```
**Eq. 20-115** [p.485] — desconto por IMS e amido (verificada em 150 dpi)
```
Dt_dcNDF (% of NDF) = [ Dt_dcNDF_Base/100
                         - 1.1 * ( An_DMI_BW - 0.035 )
                         - 0.59 * ( (Dt_StIn + Inf_StIn_Rum + Inf_StIn_SI)
                                    / (Dt_DMIn + Inf_DMIn_Rum + Inf_DMIn_SI) - 0.26 ) ] * 100
```
An_DMI_BW = IMS como fração do PC (kg MS/kg PC; 0.035 = 3.5 % do PC); razão de amido = fração do amido na MS total (0.26 = 26 %). Efeito: dcFDN cai 1.1 ponto-fração por unidade de IMS/PC acima de 0.035 e 0.59 por unidade de fração de amido acima de 0.26 (e aumenta abaixo desses pontos).

**Eq. 20-116** [p.485] `Dt_DigNDFIn (kg/d) = Dt_dcNDF/100 * Dt_NDFIn`
**Eq. 20-117** [p.485] `An_DigNDFIn (kg/d) = Dt_DigNDFIn + Inf_NDFIn_Rum * Dt_dcNDF/100`
**Eq. 20-118** [p.485] `Dt_DigNDF (% of DM) = Dt_DigNDFIn / Dt_DMIn * 100`
**Eq. 20-119** [p.485] `An_DigNDF (% of DM) = ( An_DigNDFIn / (Dt_DMIn + Inf_DMIn_Rum + Inf_DMIn_SI) ) * 100`
**Eq. 20-120** [p.485] `Fe_NDF (kg/d) = Dt_NDFIn - Dt_DigNDFIn`

Fluxo: 20-110/111 → 20-112 (por alimento) → 20-113 → 20-114 → 20-115 (usa 20-97 de amido/IMS) → 20-116/117 → 20-118/119/120. **An_DigNDF (20-119) é entrada da predição de proteína do leite (Eq. 20-185)**.

---
## 2. Digestão e absorção de proteína [pp.485–487]

### Equações
**Eq. 20-121** [p.486] `Fd_idRUPIn_f (kg/d) = Fd_dcRUP_f/100 * Fd_RUPIn_f` (PNDR intestinalmente digerida; Fd_dcRUP_f = digestibilidade intestinal da PNDR, % da PNDR, da biblioteca de alimentos)
**Eq. 20-122** [p.486] `Dt_idRUPIn (kg/d) = SUM_{f=1..N_f} Fd_idRUPIn_f`
**Eq. 20-123** [p.486] `An_idRUPIn (kg/d) = Dt_idRUPIn + InfRum_idRUPIn + InfSI_idTPIn`
**Eq. 20-124** [p.486] `Fe_RUPout_f (kg/d) = Fd_RUPIn_f * ( 1 - Fd_dcRUP_f/100 )`
**Eq. 20-125** [p.486] `Fe_RUPout (kg/d) = An_RUPIn + Inf_TPIn_SI - An_idRUPIn`
**Eq. 20-126** [p.486] `Du_idMiCP (kg/d) = Du_MiCP * 0.80` (digestibilidade intestinal da PB microbiana = 80 %)
**Eq. 20-127** [p.486] `Du_idMiTP (kg/d) = Du_idMiCP * 0.824` (82.4 % da PB microbiana digerida é proteína verdadeira)
**Eq. 20-128** [p.486] `Fe_MiCPout (kg/d) = Du_MiCP - Du_idMiCP` (não inclui PB microbiana sintetizada no intestino grosso)
**Eq. 20-129** [p.486] `An_idCPIn (kg/d) = Dt_idRUPIn + Du_idMiCP + Inf_idCPIn`
**Eq. 20-130** [p.486] `An_DigCPaIn (kg/d) = Dt_CPIn + Inf_CPIn_Rum + Inf_CPIn_SI - Fe_CP`
**Eq. 20-131** [p.486] `An_DigTPaIn (kg/d) = An_TPIn + Inf_TPIn_Rum + Inf_TPIn_SI - Fe_CP`  (impresso "- Fe_CP" também na versão de proteína verdadeira)
**Eq. 20-132** [p.486] `An_dcCPa (% of CP) = ( An_DigCPaIn / (Dt_CPIn + Inf_CPIn_Rum + Inf_CPIn_SI) ) * 100`
**Eq. 20-133** [p.486] `An_DigCPtIn (kg/d) = An_RDPIn - Fe_MiCP + An_idRUPIn - Fe_NPend`
**Eq. 20-134** [p.486] `An_DigTPtIn (kg/d) = An_RDTPIn - Fe_MiTP + An_idRUPIn - Fe_NPend`
**Eq. 20-135** [p.486] `An_dcCPt (% of CP) = ( An_DigCPtIn / (Dt_CPIn + Inf_CPIn_Rum + Inf_CPIn_SI) ) * 100`
(a = aparente; t = verdadeira.)

**Eq. 20-136** [p.487] — Proteína metabolizável ingerida (kg/d)
```
An_MPIn (kg/d) =
  An_StatePhys = "Calf"  :  An_TPIn - Fe_CPout + Fe_CPend
  An_StatePhys != "Calf" :  An_idRUPIn + Du_idMiTP + Inf_TPIn_Bld
```
(impresso "An_StatePhs"; mesmo símbolo que An_StatePhys.) Para bezerras usa-se abordagem empírica de trato total porque os dados da digestão ruminal não incluem bezerras; o programa exclui a digestão ruminal para bezerras e o usuário deve garantir coeficientes de digestibilidade coerentes para proteínas/AA infundidos [p.487].
**Eq. 20-137** [p.487] `An_MP (% of DM) = ( An_MPIn / (Dt_DMIn + Inf_DMIn_Rum + Inf_DMIn_SI) ) * 100`
Texto: expressar PM só relativa à MS que chega ao intestino é arbitrário; também seria lógico usar An_DMIn [p.487].

**Eq. 20-138** [p.487] — PB fecal (kg/d) (verificada em 260 dpi)
```
Fe_CPout (kg/d) =
  An_StatePhys = "Calf" & An_CPIn_ClfLiq > 0 :  0.05 * An_CPIn_ClfLiq + 0.25 * An_CPIn_ClfDry
  An_StatePhys != "Calf"                     :  Fe_RUPout + Fe_MiCPout + Fe_CPend
                                                + Inf_CPIn_SI - Inf_idCPIn_SI
```
Texto: Dt_CPIn de alimentos líquidos é 95 % digerida e de sólidos 75 % para bezerras consumindo líquido; 70 % para bezerras só com sólido [p.487] (coerente com 0.05 e 0.25 só para o caso "líquido > 0"; o caso bezerra só sólida com 0.30 não está escrito na tabela; ⚠).
**Eq. 20-139** [p.487] `Fe_Nout (kg/d) = Fe_CPout / 6.25`

**Eq. 20-140** [p.487] — PB endógena fecal (corrigido pela imagem a 260 dpi)
```
Fe_CPend_LiqFd (kg/d) =
  NonMilkCP_ClfLiq = 0 :  0.0119 * Dt_DMIn_LiqFd
  NonMilkCP_ClfLiq = 1 :  0.0344 * Dt_DMIn_LiqFd
Fe_CPend_DryFd (kg/d) =
  An_PhysState = "Calf"   :  0.0206 * Dt_DMIn_DryFd
  An_PhysState != "Calf"  :  12.0 + (0.12 * An_NDF) * (Dt_DMIn + InfRum_DMIn + InfSI_DMIn)
Fe_CPend (kg/d) = Fe_CPend_LiqFd + Fe_CPend_DryFd
```
NonMilkCP_ClfLiq = indicador (1 = o líquido contém PB não-leite). An_NDF = FDN da dieta (% da MS). Impresso literalmente: "12.0 + (0.12 × An_NDF) × (…)": ⚠ unidades/precedência (provavelmente (12.0 + 0.12*NDF) × IMS em g/d e depois /1000 para kg/d; ver ⚠).
**Eq. 20-141** [p.487] `Fe_EndRDP (kg/d) = Fe_CPend * An_RDPIn / An_CPIn`
**Eq. 20-142** [p.487] `Fe_EndRUP (kg/d) = Fe_CPend * An_RUPIn / An_CPIn`  (divisão arbitrária)

---
## 3. Aminoácidos [pp.487–488]
**Eq. 20-143** [p.487]
```
Fd_idAARUPIn(a)_f (g/d) = Fd_AARUPIn(a)_f * Fd_dcRUP_f/100 * F_idAARUP(a)
```
Fd_AARUPIn(a)_f = AA (a) na PNDR do alimento f (g/d); F_idAARUP(a) (g/g) = fator de ajuste da digestibilidade intestinal de cada AA em relação à PNDR; **todos fixados em 1** (dados inadequados, cap. 6) [pp.487–488].
**Eq. 20-144** [p.488] `Dt_idAARUPIn(a) (g/d) = SUM_{i=1..N_f} Fd_idAARUPIn(a)_f` (índice impresso i; deveria ser f)
**Eq. 20-145** [p.488] `Du_idAAMic(a) (g/d) = Du_AAMic(a) * SI_dcMiCP / 100`  (SI_dcMiCP = digestibilidade da PB microbiana no ID, %; 80 pela Eq. 20-126)
**Eq. 20-146** [p.488] `Du_idAAIn(a) (g/d) = Du_idAAMic(a) + Dt_idAARUPIn(a)`
**Eq. 20-147** [p.488] `An_idAAIn(a) (g/d) = Du_idAAIn(a) + Inf_idAAIn(a)`
**Eq. 20-148** [p.488] `Abs_AA(a)_g (g/d) = An_idAAIn(a) + Inf_AA(a)_g * fArt`
fArt (g/g) = proporção da proteína verdadeira infundida que entra no sangue (texto: "definida pela equação 20-147", referência imprecisa; valor não dado nesta página).
**Eq. 20-149** [p.488] `Abs_EAA_g (g/d) = SUM_{a=1..N_EAA} Abs_AA(a)_g`
**Eq. 20-150** [p.488] `Abs_NEAA_g (g/d) = An_MPIn * 1.15 - Abs_EAA_g`
(Aqui An_MPIn deve estar em g/d; a Eq. 20-136 o dá em kg/d. ⚠ conversão ×1000.) 1.15 = massa de hidratação média quando proteína vira AA livre [p.488].
**Eq. 20-151** [p.488] `Abs_AA_EAA(a) (% of EAA) = Abs_AA(a)_g / Abs_EAA_g * 100`
**Eq. 20-152** [p.488] `Abs_AA_MP(a) (% of MP) = Abs_AA(a)_g / An_MPIn_g * 100`

---
## 4. Ácidos graxos [pp.488–489]
Digestibilidade total (Fd_ttdcFA_f, % dos AG) vem da biblioteca de alimentos (cap. 4); ausente = **73 %** (exceto categorias gorduras/suplementos de AG, fixos pelo cap. 4). **Bezerras: todos os ingredientes da categoria concentrado usam 81 %**, independente da biblioteca [p.488]. Digestibilidade de cada AG individual = a do total.
**Eq. 20-153** [p.488] `Fd_DigFAIn_f (kg/d) = Fd_ttdcFA_f/100 * Fd_FA_f/100 * Fd_DMIn`  (Fd_FA_f = % AG na MS; impresso Fd_DMIn sem subscrito f)
**Eq. 20-154** [p.488] `Fd_DigFA(fa)In_f (kg/d) = Fd_ttdcFA_f/100 * Fd_FA(fa)_FA_f/100 * Fd_FA_f/100 * Fd_DMIn_f`
fa ∈ {C12, C14, C16, C16:1, C18:0, C18:1c, C18:1t, C18:2, C18:3, outros}; Fd_FA(fa)_FA = % do AG fa no total de AG.
**Eq. 20-155** [p.489] `Dt_DigFAIn (kg/d) = SUM_{f=1..N_f} Fd_DigFAIn_f`
**Eq. 20-156** [p.489] `Dt_DigFA(fa)In (kg/d) = SUM_{f=1..N_f} Fd_DigFA(fa)In_f`
**Eq. 20-157** [p.489] `Dt_DigFA_FA (% of FA) = Dt_DigFAIn / Dt_FAIn * 100`
**Eq. 20-158** [p.489] `Dt_DigFA(fa)_FA (% of FA) = Dt_DigFA(fa)In / Dt_FAIn * 100`
**Eq. 20-159** [p.489] `An_DigFAIn (kg/d) = Dt_DigFAIn + Inf_DigFAIn`
**Eq. 20-160** [p.489] `An_DigFA_FA (% of FA) = ( An_DigFAIn / (Dt_FAIn + Inf_FAIn_Rum + Inf_FAIn_SI) ) * 100`
**Eq. 20-161a** [p.489] `An_DigUFAIn (kg/d) = An_DigC161In + An_DigC181tIn + An_DigC181cIn + An_DigC182In + An_DigC183In`
**Eq. 20-161b** `An_DigMUFAIn (kg/d) = An_DigC161In + An_DigC181tIn + An_DigC181cIn`
**Eq. 20-161c** `An_DigPUFAIn (kg/d) = An_DigC182In + An_DigC183In`
**Eq. 20-161d** `An_DigSatFAIn (kg/d) = An_DigFAIn - An_DigUFAIn`
Só a digestibilidade total de AG é exportada (biohidrogenação não modelada); ingestão e digestibilidade de AG individuais "não são consideradas", mas podem ser adicionadas [p.489].
**Eq. 20-162** [p.489] `Fe_FAout (kg/d) = Dt_FAIn + Inf_FAIn_Rum + Inf_FAIn_SI - Dt_DigFAIn - Inf_DigFAIn`
**Eq. 20-163** [p.489] `An_dcFA (% of FA) = ( Dt_DigFAIn + Inf_DigFAIn_Rum + Inf_DigFAIn_SI ) / ( Dt_FAIn + Inf_FAIn_Rum + Inf_FAIn_SI ) * 100`
Perda fecal/digestibilidade aparente de AG individuais: não incluídas (dados insuficientes).

---
## 5. MO digestível e fecal [pp.489–490]
**Eq. 20-164** [p.489] `An_DigOMaIn (kg/d) = An_DigNDFIn + An_DigStIn + An_DigFAIn + An_DigrOMaIn + An_DigCPaIn`
**Eq. 20-165** [p.489] `An_DigOMtIn (kg/d) = An_DigNDFIn + An_DigStIn + An_DigFAIn + An_DigrOMtIn + An_DigCPtIn`
**Eq. 20-166** [p.490] `Fe_OMout (kg/d) = Fe_CPout + Fe_NDFout + Fe_Stout + Fe_rOMout + Fe_FAout`
**Eq. 20-167** [p.490] `Fe_OMend (kg/d) = Fe_CPend + Fe_rOMend`
**Eq. 20-168** [p.490] `TT_dcOMa (% OM) = An_DigOMaIn / An_OMIn * 100`
**Eq. 20-169** [p.490] `TT_dcOMt (% OM) = An_DigOMtIn / An_OMIn * 100`
(Fe_NDFout = Fe_NDF da Eq. 20-120; Fe_Stout = Fe_St da Eq. 20-98: nomes impressos diferentes.)

---
## 6. Aporte de EB, ED [pp.490–491]
**Eq. 20-170** [p.490]
```
An_GEIn (Mcal/d) = (Dt_NDFIn + Inf_NDFIn) * En_NDF
                 + (Dt_StIn + Inf_StIn) * En_St
                 + Dt_rOMIn * En_rOM
                 + (Dt_CFatIn + Inf_FAIn) * En_FA
                 + (Dt_TPIn + Inf_CPIn) * En_CP
                 + Dt_NPNCPIn * En_NPNCP
                 + Inf_AcetIn * En_Acet + Inf_PropIn * En_Prop + Inf_ButrIn * En_Butr
```
**Eq. 20-171** `An_GE (Mcal/kg DM) = An_GEIn / An_DMIn`
**Eq. 20-172** `An_DEStIn (Mcal/d) = An_DigStIn * En_St`
**Eq. 20-173** `An_DErOMIn (Mcal/d) = An_DigrOMaIn * En_rOM`
**Eq. 20-174** `An_DENDFIn (Mcal/d) = An_DigNDFIn * En_NDF`
**Eq. 20-175** `An_DECPIn (Mcal/d) = An_DigCPaIn * En_CP`
**Eq. 20-176** `An_DENPNCPIn (Mcal/d) = An_NPNCPIn * En_NPNCP`
**Eq. 20-177** `An_DETPIn (Mcal/d) = An_DECPIn - ( An_DENPNCPIn / En_NPNCP * En_CP )`
**Eq. 20-178** `An_DEFAIn (Mcal/d) = An_DigFAIn * En_FA`
**Eq. 20-179** `Inf_DEAcetIn = Inf_AcetIn * En_Acet`; **Eq. 20-180** `Inf_DEPropIn = Inf_PropIn * En_Prop`; **Eq. 20-181** `Inf_DEButrIn = Inf_ButrIn * En_Butr` (Mcal/d)
**Eq. 20-182** [p.490]
```
An_DEIn (Mcal/d) = An_DENDFIn + An_DEStIn + An_DErOMIn + An_DETPIn + An_DENPNCPIn + An_DEFAIn
                 + Inf_DEAcetIn + Inf_DEPropIn + Inf_DEButrIn
```
**Eq. 20-183** [p.491] `An_DE (Mcal/kg DM) = An_DEIn / An_DMIn`
**Eq. 20-184** [p.491] `An_DEInp (Mcal/d) = An_DEIn - An_DENPNCPIn`
(ED não proteica "para uso como termo energético em predições de proteína do leite que contém efeitos independentes de PM ou AA"; observe que a definição subtrai só a ED de NNP, apesar do texto falar em "ED a partir da proteína".) ⚠

### Tabela 20-9 [p.491] — Calores de combustão (Mcal/kg) para nutrientes digeridos (corrigido pela imagem: FDN = 4.2, OCR leu "42")
| Nutriente | Variável | Entalpia (Mcal/kg) |
|---|---|---|
| rOM | En_rOM | 4.0 |
| Amido | En_St | 4.23 |
| FDN | En_NDF | 4.2 |
| PB | En_CP | 5.65 |
| NNP (base PB) | En_NPNCP | 0.89 |
| AG | En_FA | 9.4 |
| Acetato | En_Acet | 3.48 |
| Propionato | En_Prop | 4.96 |
| Butirato | En_Butr | 5.95 |


---
## 7. Utilização de nutrientes e produção animal — esquema geral [p.491]
Estima-se energia líquida (NE) e proteína líquida (NP) de cada processo (mantença, produção, gestação, crescimento) e converte-se para EM / PM com coeficientes de eficiência K com subscrito: Kg (crescimento), Kl (lactação), Km (mantença), Ky (gestação) [p.491].

## 8. Proteína do leite [pp.491–496]

**Papel no simulador:** prediz a proteína líquida do leite (Mlk_NP_g) a partir de 5 AAE absorvidos, outros AA, ED não proteica, FDN digerida e PC; com escalonamento do termo quadrático pela produção de proteína do rebanho (para acomodar alto mérito genético); calcula uso de PM e secreção de AA no leite.

### Entradas principais (de seções anteriores)
| variável | sigla | unidade | origem | pág. |
|---|---|---|---|---|
| AA absorvidos His, Ile, Leu, Lys, Met, Arg, Phe, Thr, Trp, Val | Abs_His_g … Abs_Val_g | g/d | Eq. 20-148 | 488 |
| AANE absorvidos | Abs_NEAA_g | g/d | Eq. 20-150 | 488 |
| ED não proteica | An_DEInp | Mcal/d | Eq. 20-184 | 491 |
| FDN digerida | An_DigNDF | % da MS | Eq. 20-119 | 485 |
| Peso corporal | An_BW | kg | entrada | 491 |
| Proteína do leite do rebanho em 305 d | Mlk_NP_RHA(305d) | kg/305 d | **ENTRADA obrigatória do modelo** | 495 |
| Fator de resposta | β_g | adim. | usar 1 | 495 |

### Equações
**Eq. 20-185** [p.491] (conferida a 230 dpi) — Proteína líquida do leite (g/d)
```
Mlk_NP_g (g/d) = -97.0
               + 1.68   * Abs_His_g
               + 0.885  * Abs_Ile_g
               + 0.466  * Abs_Leu_g
               + 1.15   * Abs_Lys_g
               + 1.84   * Abs_Met_g
               + 0.0773 * Abs_OthAA_g
               - 0.00215 * EAAb2
               + 10.79  * An_DEInp
               - 4.60   * (An_DigNDF - 17.06)
               - 0.420  * (An_BW - 612)
```
Centros: FDN digerida 17.06 % da MS; PC 612 kg. Origem: Cap. 6 (n/R²/RMSE não repetidos aqui).
**Eq. 20-186a** `Abs_OthAA_g (g/d) = Abs_NEAA_g + Abs_Arg_g + Abs_Phe_g + Abs_Thr_g + Abs_Trp_g + Abs_Val_g`
**Eq. 20-186b** `EAAb2 (g^2/d) = Abs_His_g^2 + Abs_Ile_g^2 + 0.466 * Abs_Leu_g^2 + Abs_Lys_g^2 + Abs_Met_g^2` (coeficiente 0.466 só no Leu²; conferido na imagem).

### Discussão do termo quadrático [pp.491–492] (conceitos numéricos)
- Produção de leite EUA +90 kg/ano; a 1.5 kg leite/kg MS ⇒ +0.17 kg IMS/d/ano; em 15 anos +2.5 kg IMS/d; PM média do conjunto de dados = 9.94 % da MS; +250 g PM/d, +5.75 g Met absorvível/d. A 23 kg IMS: PM 2,290 g/d e 52 g Met abs.; com acréscimo 2,550 g PM e 58 g Met (28 e 27 % acima das médias) [p.491].
- Produção máxima no conjunto de dados = 53.8 kg/d. Pela Eq. 20-186a [sic; texto] a resposta máxima à PM ocorre em **3,087 g PM/d**, ≈1,450 g proteína do leite/d (depende de An_DEInp). NRC 2001: IMS 33.6 kg/d (vaca 750 kg, 60 kg leite, 3.0 % PB, 3.5 % gordura) ⇒ PM 3,087 g/d = 9.2 % da MS (média do conjunto 9.9 %). A 70 kg leite: IMS 37 kg, PM 8.3 % da MS e PB < 14 % [pp.491–492].
- Divisão por ano 2000: antes de 2000 platô 1,051 g/d a 1,673 g AAE/d (DEInp = 74 Mcal/d); depois, quase linear, máximo a 6,415 g AAE/d. Com variável "idade" (0/1): platôs 1,312 g/d a 1,559 g AAE/d (antigos) e 1,854 g/d a 3,767 g AAE/d (novos); tentativa por década: termos não significativos, modelo superparametrizado [p.492].

### Escalonamento quadrático (Fatores de Escala) [pp.492–495]
Lógica: escolher um ponto de referência na faixa linear inferior (10 % do X do platô original); exigir que a curva reescalonada passe pelo mesmo Y nesse X e mantenha o mesmo intercepto; fixar novo platô (múltiplo do original); resolver a e b.

**Eq. 20-187** [p.492] (exemplo demonstrativo, PM): `Mlk_NP_g (g/d) = -0.000114 * An_MPIn^2 + 0.681 * An_MPIn + 25.8` (An_MPIn em g/d)
**Eq. 20-188** `Y_1 = a_1*X^2 + b_1*X + c_1`
**Eq. 20-189** `Ym_1 = c_1 - b_1^2/(4*a_1)`
**Eq. 20-190** `Xm_1 = -b_1/(2*a_1)`
(Ym = platô; Xm = concentração de AAE que produz o platô; subscrito 1 = equação existente.)
**Eq. 20-191** `Y_2 = a_2*X^2 + b_2*X + c_1`
**Eq. 20-192** `Ym_2 = c_1 - b_2^2/(4*a_2)`
**Eq. 20-193** `Xm_2 = -b_2/(2*a_2)`
O intercepto c_1 é comum aos dois conjuntos [p.493].
Exemplo [p.493]: com os parâmetros 20-187, Ym_1 = 1,043 g/d e Xm_1 = 2,987 g/d (verificado: 25.8 + 0.681²/(4*0.000114) = 1,043; Xm = 2,987). 10 % de Xm_1 = 299 g/d (= X_1); Y_1(X_1) = 219 g/d.
**Eq. 20-194** `Y_1 = a_1*X_1^2 + b_1*X_1 + c_1 = 219`
**Eq. 20-195** `Ym_2 = c_1 - b_2^2/(4*a_2) = 2086`  (platô dobrado)
**Eq. 20-196** `Y_2 = a_2*X_1^2 + b_2*X_1 + c_1 = a_2*299^2 + b_2*299 + c_1 = 219`
Retirando o intercepto, 20-195 e 20-196 resolvem-se em (corrigido/conferido a 300 dpi):
**Eq. 20-197** `a_2 = ( 2*SQRT(Ym_2^2 - Y_2*Ym_2) - 2*Ym_2 + Y_2 ) / X_1^2`
**Eq. 20-198** `b_2 = -( 2*SQRT(Ym_2^2 - Y_2*Ym_2) - 2*Ym_2 ) / X_1`
**Verificação numérica (minha):** as fórmulas só reproduzem os números do texto se Y_2 e Ym_2 forem os valores SEM intercepto: Y_2 = 219 − 25.8 = 193.2; Ym_2 = 2086 − 25.8 = 2060.2 ⇒ a_2 = −5.32e-5; b_2 = 0.6621; platô = 2,086 em X = 6,224 g/d. (Usando 219 e 2086 com intercepto o platô dá 2,112.) Para múltiplos 1.25/1.5/1.75/2.0 do platô original sem intercepto (1,017.2): a_2 = −8.92e-5/−7.33e-5/−6.22e-5/−5.40e-5; b_2 = 0.6736/0.6688/0.6655/0.6631; X_platô ≈ 3,775/4,562/5,348/6,135 g PM/d; Y_platô ≈ 1,297/1,551/1,806/2,060 g/d.
Derivação: com c fixo, Ym_2' = −b_2²/(4a_2) ⇒ a_2 = −b_2²/(4Ym_2'); substituindo em a_2 X_1² + b_2 X_1 = Y' dá a raiz menor b_2 = (2Ym_2' − 2√(Ym_2'² − Y'Ym_2'))/X_1 (ramo de inclinação positiva); é o que 20-198 imprime.

**Generalização a vários AAE** [pp.493–494]: soma de quadráticas com **a comum**:
**Eq. 20-199** `Y = a_1*V_1^2 + β_1*V_1 + a_1*W_1^2 + δ_1*W_1 + a_1*X_1^2 + γ_1*X_1 + ... + c`  (V, W, X, … = AAE e termos; a comum; β, δ, γ lineares)
**Eq. 20-200** `Ym_1 = c - β_1^2/(4*a_1^2) - δ_1^2/(4*a_1^2) - γ_1^2/(4*a_1^2)`  (como impresso, denominador 4a_1^2; ⚠ pela 20-201 deveria ser 4*a_1)
**Eq. 20-201** `Ym_V1 = -β_1^2/(4*a_1)` ; **Eq. 20-202** `Ym_W1 = -δ_1^2/(4*a_1)` ; **Eq. 20-203** `Ym_X1 = -γ_1^2/(4*a_1)`  (resposta máxima por termo, sem intercepto)
**Eq. 20-204** `Vm_1 = -β_1/(2*a_1)` ; **Eq. 20-205** `Wm_1 = -δ_1/(2*a_1)` ; **Eq. 20-206** `Xm_1 = -γ_1/(2*a_1)`  (concentração que dá cada máximo)
Procedimento [p.494]: (i) escolher escalar comum s (ex. 2); multiplicar 20-201–20-203 por s; (ii) avaliar a Eq. 20-199 sem intercepto a 10 % das concentrações máximas 20-204–20-206 com os coeficientes anteriores (⇒ Y_1 e X_1 para cada AA); (iii) calcular novos a_2, β_2, δ_2, γ_2 com 20-197 e 20-198; a_2 é igual para cada AA, mas os termos lineares variam por AA (a menos que todos tenham inclinações idênticas no início).

**Escalar do rebanho** [p.494–495]: o escalar é baseado na proteína do leite produzida pelo rebanho em 305 d (Mlk_NP_RHA(305d)). DEL médio do conjunto de dados = 136 d (≈ meio de uma lactação de 305 d); produção média 918 g/d de proteína ⇒ 280 kg em 305 d.
**Eq. 20-207** [p.495] `f_g = 1 + β_g * ( Mlk_NP_RHA(305d) / 280 - 1 )`
Mlk_NP_RHA(305d) em kg proteína do leite/305 d; β_g esperado = 1 ("neste momento um valor de 1 deve ser usado"; pode-se ajustar para maior/menor responsividade com dados). O modelo REQUER a produção de proteína do leite em 305 d como entrada. f_g é o múltiplo do platô (Ym_2 = f_g × Ym_1 sem intercepto) usado no procedimento acima ⇒ interpretação (o texto não escreve explicitamente a ligação 20-207 → 20-197/198; ⚠).
**Eq. 20-208** [p.495] (monitor de viabilidade) `MlkNP_MlkNPmax (g/g) = Mlk_NP_g / Mlk_NPmax_g`
**Eq. 20-209** [p.495] (conferida a 260 dpi)
```
Mlk_NPmax_g (g/d) = -97.0 + SUM_{a=1..N_EAA} ( mPrtmx_a_g ) + 0.077 * Abs_OthAA_g   [livro imprime "mPrtm_g" no somatório da 20-209 e "mPrtmx_a_g" na 20-210; unificado (corrigido na verificação)]
                  + 10.79 * An_DEInp - 4.60 * (An_DigNDF - 17.06) - 0.420 * (An_BW - 612)
```
(coeficiente 0.077 aqui versus 0.0773 na 20-185: como impresso; ⚠.)
**Eq. 20-210** [p.495] `mPrtmx_a_g (g/d) = -(scaled quadratic coefficient)^2 / ( 4 * (scaled linear coefficient)_a )` — como impresso; ⚠ numerador/denominador parecem trocados (matematicamente: −(coef. linear)²/(4·coef. quadrático), como na 20-201).
Regra: razão MlkNP_MlkNPmax deve ser **< 0.9** (a produção pode subir > 10 % por curtos períodos com dieta rica em grãos); caso contrário aumentar Mlk_NP_RHA(305d) até atingir ≤ 0.9. Meta acima do máximo escalonado não será atingida [p.495].
Opção: usuário pode usar `mPrt_eqn` = 0 para usar `Trg_MilkTPp` como produção especificada; as equações seguintes (AA, eficiência, balanço de PM) usam então a meta [p.495]. A Eq. 20-185 escalonada é considerada a de maior acurácia; a predição por PM − mantença com eficiência estática "não é particularmente precisa" [p.495].

**Fig. 20-1** [p.493]: eixo x PM (g/d, 0–8000), eixo y proteína do leite (g/d, 0–2500). Curvas: Original (Eq. 20-187; platô 1,043 g/d perto de 3,000 g PM) e reescalonadas para 1.25, 1.5, 1.75 e 2.0 × o máximo original (Eqs. 20-197/198). Todas coincidem na faixa linear inicial (até ≈ 1,000 g PM, onde passam pelo ponto de referência X_1 = 299/Y_1 = 219 e seguem inclinação ≈ 0.6–0.68) e divergem à direita: platôs a ≈ 1,300 / 1,550 / 1,800 / 2,060 g/d com posições do ápice ≈ 3,800 / 4,500–5,000 / 5,300–5,500 / 6,000–6,500 g PM (leitura visual; coerente com meus cálculos acima). Legenda: "Original, 1.25rig, 1.50rig, 1.75rig, 2.00rig".
**Fig. 20-2** [p.494]: predição da Eq. 20-185 com parâmetros originais (quadrados, linha cheia) versus após escalonamento para platô 2× (triângulos, tracejada). x = AAE totais absorvidos (g/d, 0–3,500); y = proteína do leite predita (g/d, 0–2,500). Pontos = AA individuais e energia fixados em mínimo observado, 1º quartil, média, 3º quartil, máximo, máximo×1.5 e máximo×2 do conjunto de dados. Leitura visual aproximada: original ≈ 300, 800, 900, 1,020, 1,190 (x≈1,550), 1,060 (x≈2,300), 560 (x≈3,050) g/d (cai após o máximo, resposta negativa); escalonada ≈ 330, 870, 1,000, 1,100, 1,700, 2,100, 2,330 g/d (continua crescendo, com concavidade). Mensagem: sem escalonamento, extrapolação além do máximo observado dá queda de produção.

### Secreção de AA e PM exigida [p.495–496]
**Eq. 20-211** [p.495] `Mlk_AA(a) (g/d) = Mlk_NP_g * AA(a)_NP_Milk / 100`  (a ∈ Arg, His, Ile, Leu, Lys, Met, Phe, Thr, Trp, Val; AA(a)_NP_Milk = g de AA hidratado/100 g Mlk_NP, Tabela 6-5; a soma dos 20 AA ≈ 115 g/100 g de proteína verdadeira do leite — correção de hidratação; ignorada no passado causava viés [p.495])
**Eq. 20-212** [p.495] `Mlk_MPuse (kg/d) = Mlk_NP / Kl_MP_NP`  (Kl_MP_NP g/g = eficiência fracionária predita, Eq. 20-355 [fora do intervalo, Cap. 20 final]; não reflete PM mínima)
**Eq. 20-213** [p.496] `Mlk_MPuse_Trg (kg/d) = Mlk_NP / Kl_MP_NP,Trg`
**Eq. 20-214** [p.496] `Kl_MP_NP,Trg (g/g) = 0.69` (eficiência-alvo observada, referência mínima atingível; a eficiência da Eq. 20-356 deve ser próxima ou > 0.68 com dietas ótimas)

## 9. Gordura do leite [p.496]
Desempenho da equação: validação cruzada boa; **RMSE = 205 g/d (18.9 % da média observada); CCC = 0.62; 1.6 % do EQM em viés médio; 5.2 % em viés de inclinação** [p.496].
**Eq. 20-215** [p.496] (conferida a 260 dpi)
```
Milk_Fat_g (g/d) = 453 - 1.42 * An_LactDay
                 + 24.52 * (Dt_DMIn - Dt_FAIn)
                 + 0.41 * Dt_DigC160In * 1000
                 + 1.80 * Dt_DigC183In * 1000
                 + 1.45 * Abs_Ile_g + 1.34 * Abs_Met_g
```
Dt_DMIn, Dt_FAIn: kg/d; Dt_DigC160In e Dt_DigC183In: C16:0 e C18:3 digeridos (kg/d; ×1000 ⇒ g/d); Abs_Ile_g, Abs_Met_g: g/d. **An_LactDay limitado a máximo 375 d.** Usuário pode usar `Trg_MilkFatp` com `mFat_eqn = 0` (calcula tudo com o nível especificado).

## 10. Volume de leite [pp.496–497]
**Eq. 20-216** [pp.496–497] (conferida a 260 dpi)
```
Mlk_Prod_Hol (kg/d) = 4.541 + 11.13 * Mlk_NP + 2.65 * Mlk_Fat + 0.183 * An_DEIn
                    - 0.0626 * (An_LactDay - 137)
                    + 2.766e-4 * (An_LactDay - 137)^2
                    + 1.603e-6 * (An_LactDay - 137)^3
                    - 7.397e-9 * (An_LactDay - 137)^4
                    + 1.57 * (An_Parity - 1)
Mlk_Prod (kg/d) = Holstein: Mlk_Prod_Hol ;  Jersey: Mlk_Prod_Hol - 3.40 ;  Other: Mlk_Prod_Hol - 1.53
```
Mlk_NP e Mlk_Fat em **kg/d** (predições acima, que estão em g/d ⇒ dividir por 1000); An_DEIn em Mcal/d; An_LactDay centrado em 137 d (máx 375 d); An_Parity contínua: 1 primípara, 2 multípara (ou média do grupo). Texto diz que An_BW foi centrado em 612 kg mas a equação impressa não tem termo de PC (⚠). **RMSE 4.5 kg/d (14.6 % da média); CCC 0.75; 0.1 % do EQM em viés médio; 3.3 % em viés de inclinação.** Usuário pode especificar o volume com `mProd_eqn = 0` (o texto diz "Trg_MilkTPp" mas para volume seria Trg_MilkProd; ⚠).

## 11. Energia do leite [pp.497]
**Eq. 20-217** [p.497] (se lactose do leite informada)
```
Milk_NEp (Mcal/kg) = 9.29 * Milk_Fat% /(Milk*100) + 5.85 * Milk_Protein% /(Milk*100) + 3.95 * Milk_Lactose%_Target /(Milk*100)
```
Impressa assim (fração de componente por kg de leite; ⚠ denominador "Milk × 100" com % no numerador: interpretar como kg componente/kg leite, i.e., equivalente à Eq. 20-218). Se for PB do leite (não proteína verdadeira), trocar 5.85 por 5.5.
**Eq. 20-218** `Milk_NEp_Trg (Mcal/kg) = 9.29*Milk_Fat_Trg/Milk_Trg + 5.85*Milk_Protein_Trg/Milk_Trg + 3.95*Milk_Lactose_Trg/Milk_Trg`  (alvos do usuário)
**Eq. 20-219** (Tyrrell e Reid 1965; sem lactose/proteína) `Milk_NEp_Trg (Mcal/kg) = 0.36 + 9.69 * Milk_Fat_Trg / Milk_Trg`
**Eq. 20-220** `Milk_NEuse_Trg (Mcal/d) = Milk_NEp_Trg * Milk_Trg`
**Eq. 20-221** `Milk_NEuse (Mcal/d) = Milk_NEp * Milk`
**Eq. 20-222** `Milk_MEuse (Mcal/d) = Milk_NE / Kl_ME_NE` (impresso Milk_NE; = Milk_NEuse)
**Eq. 20-223** `Kl_ME_NE (Mcal/Mcal) = 0.66`
"Milk" = produção de leite (kg/d), não definida explicitamente nesta página (Mlk_Prod da 20-216 ou meta do usuário). Coeficientes 9.29, 5.85, 3.95 Mcal/kg = gordura, proteína verdadeira, lactose.

## 12. Gestação [pp.497–500]

**Eq. 20-224** [p.497] (Koong et al. 1975; ajustada a Bell et al. 1995 e House e Bell 1993)
```
Q(DayGest) = Q_{DayGest=0} * EXP{ ( K_growth - K_growth_decay * DayGest ) * DayGest }
```
Q = massa úmida (kg), energia (Mcal) ou proteína (kg) do útero gravídico/feto/tecido materno no dia DayGest; Q_{DayGest=0} = quantidade na concepção; K_growth (d^-1); K_growth_decay (d^-1). Parâmetros: Tabela 20-10.
O modelo foi reorganizado para usar peso do bezerro ao nascer (Fetus_Wt, kg) e duração gestacional esperada/observada, e ganhou involução uterina pós-parto (conservação de massa); AA da involução entram na oferta de AA (Hanigan et al. 2009) [pp.497–498].
**Eq. 20-225** [p.498] `GrUter_Wt_(t=parturition) (kg) = Fetus_Wt_(t=parturition) * f_GrUter_Fetus`
**Eq. 20-226** `Uter_Wt_(t=parturition) (kg) = Fetus_Wt_(t=parturition) * f_Uter_Fetus`
Para 280 d de gestação: **f_GrUter_Fetus = 1.816 kg/kg; f_Uter_Fetus = 0.231 kg/kg** (verificação: 49.0 kg × 1.816 = 89.0 kg; × 0.231 = 11.3 kg, = Tabela 20-10).
**Eq. 20-227** [p.498] (conferida a 250 dpi)
```
GrUter_Wt_Gest (kg) = GrUter_Wt_(t=parturition) * EXP( -( K_GrUterSyn - K_GrUterSynDecay * DayGest ) * ( LengthGest - DayGest ) )
```
(aproximação "para trás" a partir do peso no parto; ⚠ não é exatamente o inverso da 20-224, que exigiria (K − Kd·(T+t))·(T−t).)
**Eq. 20-228** `GrUter_Wt_PP (kg) = Uter_Wt_(t=parturition) * EXP( -K_UterDeg * DayLact )`  (involução; K_UterDeg = 0.2 d^-1 assumido: involução essencialmente completa no dia 21; 202 g PL/d no dia 1 pós-parto para bezerro de 50 kg; dobrar/reduzir pela metade muda pouco [p.499])
**Eq. 20-229** [p.498] (valor em kg; cabeçalho impresso "kg/kg BW", ⚠ rótulo) — critérios avaliados na ordem impressa:
```
GrUter_Wt (kg) =
  0 < DayGest <= GestationLength : GrUter_Wt_Gest
  0 < DayLact < 100              : GrUter_Wt_PP
  An_AgeDay < 240                : 0
  Otherwise                      : 0.204
```
(0.204 kg = quantidade inicial do tecido materno, Tabela 20-10; valor basal da vaca não gestante.)

### Tabela 20-10 [p.498] — Regressão não linear de pesos úmidos, proteína e energia líquida do útero gravídico, feto e tecido materno por dia de gestação (conferida a 250 dpi)
Dados de Bell et al. (1995) e House e Bell (1993); ajuste com função nls (pacote lme4, R 3.5.1). K_Syn e K_Syn Decay em d^-1; EP = erro padrão.
| Componente | Parâmetro | Peso (kg) Estim. | EP | Energia (Mcal) Estim. | EP | Proteína (kg) Estim. | EP |
|---|---|---|---|---|---|---|---|
| Útero gravídico | Quantidade_Inicial | 0.674 | — | 0.444 | — | 0.059 | — |
| | K_Syn (d-1) | 2.43e-2 | 1.0e-3 | 2.25e-2 | 1.3e-3 | 2.19e-2 | 1.1e-3 |
| | K_Syn Decay | 2.45e-5 | 4.1e-6 | 1.35e-5 | 5.0e-6 | 1.16e-5 | 4.3e-6 |
| | Quantidade_T=280 | 89.0 | — | 88.6 | — | 10.9 | — |
| Feto | Quantidade_Inicial | 0.010 | — | 9.2e-3 | — | 1.1e-3 | — |
| | K_Syn (d-1) | 5.16e-2 | 1.1e-3 | 4.95e-2 | 1.5e-3 | 4.82e-2 | 1.5e-3 |
| | K_Syn Decay | 7.59e-5 | 4.5e-6 | 6.35e-5 | 5.8e-6 | 5.85e-5 | 6.0e-6 |
| | Quantidade_T=280 | 49.0 | — | 66.2 | — | 8.14 | — |
| Tecido materno | Quantidade_Inicial | 0.204 (b) | — | — | — | — | — |
| | K_Syn (d-1) | 2.42e-2 | 4.0e-5 | — | — | — | — |
| | K_Syn Decay | 3.53e-5 | 1.6e-7 | — | — | — | — |
| | Quantidade_T=280 | 11.3 | — | 15.3 (c) | — | 1.88 (c) | — |
(b) Derivado do modelo de regressão de Bell (1995). (c) Estimado como (útero + peso da carúncula) × energia ou proteína fetal em DayGest = 280; 280 d escolhido pela duração gestacional observada em Holandesas.
Verificação numérica (minha) da Eq. 20-224 em T = 280: peso útero gravídico 89.00 ✓; proteína 10.94 (tab. 10.9) ✓; feto 49.02 / 66.22 / 8.143 ✓✓✓; tecido materno 11.23 (tab. 11.3) ≈. **Energia do útero gravídico dá 83.9 Mcal, não 88.6** (⚠: 83.9/89.0 = 0.943 ≈ 0.950 Mcal/kg do texto; 88.6 parece erro de impressão/OCR; impresso 88.6 na imagem).

**Eq. 20-230** [p.499] `An_BW_NPr (kg) = An_BW - GrUter_Wt`  (PC não gestante; NPr = não prenhe)
**Eq. 20-231** `GrUter_Wt_Gain_Gest (kg/d) = ( K_GrUterSyn - K_GrUterSynDecay * DayGest ) * GrUter_Wt`
**Eq. 20-232** `GrUter_Wt_Gain_PP (kg/d) = - K_UterDeg * Uter_Wt`  (impresso Uter_Wt; = GrUter_Wt_PP atual; ⚠)
**Eq. 20-233** `GrUter_Wt_Gain (kg/d) = 0<DayGest<GestationLength : GrUter_Wt_Gain_Gest ; 0<DayLact<100 : GrUter_Wt_Gain_PP ; Otherwise : 0`
**Eq. 20-234** `Gest_NEgain (Mcal/d) = GrUter_Wt_Gain * 0.950`  (0.950 Mcal/kg de útero gravídico no parto)
**Eq. 20-235** `Gest_NPgain_g (g/d) = GrUter_Wt_Gain * 123 * 0.86`  (123 g PB/kg; 0.86 g PVer/g PB)
**Eq. 20-236** `Ky_ME_NE (Mcal/Mcal) = Gest_NEgain >= 0 : 0.14 ; Gest_NEgain < 0 : 0.89`  (0.14 de Ferrell et al. 1976; 0.89 na regressão uterina)
**Eq. 20-237** `Gest_MEuse (Mcal/d) = Gest_NEgain / Ky_ME_NE`
**Eq. 20-238** `Ky_MP_NP (g/g) = Gest_NPgain >= 0 : 0.33 ; Gest_NPgain < 0 : 1`  (0.33 como NRC 2001)
**Eq. 20-239** `Gest_MPuse_g (g/d) = GrUter_NP_gain / Ky_MP_NP`  (impresso "GrUter_NP gain" = Gest_NPgain_g da 20-235)
**Eq. 20-240** `Gest_AA(i) (g/d) = Gest_MP * AA(i)_NP_GrUter / 100`  (composição AA da proteína do útero gravídico = proteína corporal, Tabela 6-5; "Gest_MP" = Gest_MPuse_g)
Notas [p.500]: como EL e PL são acumulados em toda a gestação, as taxas representam a composição média; erros de meio de gestação se compensam no parto; a liberação de energia/proteína do útero em involução é levemente subestimada (composição do útero é maior que a do gravídico) — erros pequenos.

---
## 13. Crescimento e reservas corporais [pp.500–503]

**Papel no simulador:** converte o PC alvo e as metas de ganho de estrutura (frame) e de reservas em ganho de PCV, gordura, proteína, água, cinzas, energia retida e exigências de ME/MP. Texto: relações de composição de ganho "não são bem definidas para todos os estados fisiológicos e permanecem incompletas" [p.500].

### Enchimento intestinal e PCV
**Eq. 20-241** [p.500] (conferida a 250 dpi) `GutFill_BW (kg/kg BW)` — critérios impressos nesta ordem:
| # | Critério | Valor |
|---|---|---|
| 1 | Dt_DMIn_Milk > 0 & Dt_DMIn_Starter <= 0.1 | 0.06 |
| 2 | Dt_DMIn_Milk > 0 & Dt_DMIn_Starter > 0.1 | 0.07 |
| 3 | Dt_DMIn_Milk > 0 & Dt_DMIn_Starter <= 0.1 & An_BW > 0.16 × An_BW_Mature | 0.09 |
| 4 | Dt_DMIn_Milk = 0 & Dt_DMIn_Starter > 0.1 & An_BW > 0.16 × An_BW_Mature | 0.15 |
| 5 | An_Parity > 0 | 0.18 |
(Dt_DMIn_Milk = IMS de leite/sucedâneo; Dt_DMIn_Starter = IMS do concentrado inicial; kg/d.) ⚠ A linha 3 repete a condição da linha 1 acrescida de PC > 16 % do maduro: avaliada em ordem seria inalcançável; ordem/condições exatas dependem do código original. Casos não cobertos (ex.: sem leite e inicial ≤ 0.1 em novilha) = não informado. Vaca (parity > 0): 18 % do PC (cap. 3: conteúdo do trato = 18 % do PC).
Texto: o enchimento real é calculado com An_BW_NPr ("An_GutFill = GutFill_BW × PC", expressão não numerada) e subtraído de An_BW e An_BW_NPr [p.500].
**Eq. 20-242** `An_EBW (kg) = An_BW - An_GutFill`
**Eq. 20-243** `An_EBW_NPr (kg) = An_BW_NPr - An_GutFill`
**Eq. 20-244** `An_EBW_Mature (kg) = An_BW_Mature * 0.82`
**Eq. 20-245** `BW_BCS (kg/BCS) = 0.094 * An_BW`  (1 unidade de ECC = 9.4 % do PC; 650 kg ⇒ 61 kg; cap. 3)
**Eq. 20-246** `An_EBW_NPr3 (kg) = An_EBW_NPr + { (3 - BCS) * BW_BCS * BW }`  (EBW ajustado a ECC padrão 3.0; impresso com "× BW" extra: ⚠ dupla contagem do PC se BW_BCS já for 0.094·An_BW)

### Ganho
**Eq. 20-247** [p.500] `An_BWgain (kg/d) = Frm_Gain + Rsrv_Gain`  (ganho de PC = ganho de estrutura (frame) + reservas)
**Eq. 20-248** [p.501] `Frm_Gain (kg/d) = Frm_Gain_Target`; **Eq. 20-249** `Rsrv_Gain (kg/d) = Rsrv_Gain_Target`  (variáveis gerais para futuros esquemas de predição; opções de entrada existem mas "não implementadas no código"; podem ser trocadas por "se")
**Eq. 20-250** [p.501] ganho de frame vazio
```
Frm_Gain_Empty (kg/d) = Dt_DMIn_ClfLiq > 0 & Dt_DMIn_ClfDry > 0 : Frm_Gain * 0.91
                         otherwise                               : Frm_Gain * (1 - GutFill_BW)
```
(bezerros: enchimento = 9 % do ganho de frame.)
**Eq. 20-251** `Rsrv_Gain_Empty (kg/d) = Rsrv_Gain`  (reservas sem mudança de enchimento)
**Eq. 20-252** `An_EBW_Gain (kg/d) = Frm_Gain_Empty + Rsrv_Gain_Empty`

### Composição do ganho (g/g)
**Eq. 20-253** [p.501] (conferida a 250 dpi) `FatGain_FrmGain (kg/kg)`
```
An_BW <= 0.16 * An_BW_Mature                     : 0.0786 + 0.0370 * An_REGain
An_BW >  0.16 * An_BW_Mature & Parity = 0        : ( 0.067 + 0.375 * An_BW/An_BW_Mature ) * An_EBW_Gain / An_BW_Gain
```
(Parity > 0: não informado; An_REGain em Mcal/d, Eq. 20-264.) ⚠
**Eq. 20-254** `FatGain_RsrvGain (kg/kg) = 0.622`
**Eq. 20-255** `NPgain_FrmGain (kg/kg) = ( 0.201 - 0.081 * An_BW/An_BW_Mature ) * 0.85 * 0.86`  (0.85 = proporção PB no ganho de proteína?? não explicado; 0.86 = PVer/PB)
**Eq. 20-256** `NPgain_RsrvGain (kg/kg) = 0.068 * 0.86`
**Eq. 20-257** `Body_FatGain (kg/d) = FatGain_FrmGain * Frm_Gain_Empty + FatGain_RsrvGain * Rsrv_Gain_Empty`
**Eq. 20-258** `Body_NPGain (kg/d) = NPgain_FrmGain * Frm_Gain + NPgain_RsrvGain * Rsrv_Gain`
**Eq. 20-259** `Body_NPGain_g (g/d) <- Body_NPGain * 1000`
**Eq. 20-260** [p.502] `Body_AAGain_g(a) (g/d) = Body_NPGain_g * AA(a)_NP_Body / 100`  (composição AA do corpo, Tabela 6-5)
**Eq. 20-261** `Body_NonFatGain (kg/d) = An_EBW_Gain - Body_FatGain`
**Eq. 20-262** `Body_AshGain (kg/d) = 0.056 * Body_NonFatGain`
**Eq. 20-263** `Body_WaterGain (kg/d) = 0.729 * Body_NonFatGain`

### Energia retida e eficiências [pp.502–503]
**Eq. 20-264** [p.502] (conferida a 250 dpi) `An_REGain (Mcal/d)`
```
An_BW <= 0.16 * An_BW_Mature :  An_EBWgain^1.10 * An_EBW^0.205        (bezerras; = Eq. 10-5 do cap. 10)
An_BW >  0.16 * An_BW_Mature :  9.4 * Body_FatGain + 5.55 * Body_CPgain
```
Body_CPgain não definido no intervalo (provavelmente = ganho de PB; 5.55 Mcal/kg proteína; ⚠ não é Body_NPGain). "Exceto para bezerros, gordura corporal e ganho de PL são usados para estimar a energia retida."
**Eq. 20-265** [p.502] `Kg_NEL_RE (Mcal/Mcal)` (conversão An_REGain → An_NELGain)
| Critério | Valor |
|---|---|
| An_BW <= 0.16 × An_BW_Mature | 1.0 |
| An_BW > 0.16 × An_BW_Mature & Parity = 0 | 0.89 |
| Parity > 0 & Mlk_Prod > 0 | 1.12 |
| Parity > 0 & Mlk_Prod = 0 | 0.89 |
Km_ME_NE e Kl_ME_NE = 0.66 [p.502].
**Eq. 20-266** [p.502] `Kf_ME_RE (Mcal/Mcal)` — eficiência ME→RE para ganho de frame (tabela impressa em raster de baixa resolução; verificada a 450–600 dpi, partes ilegíveis marcadas)
```
An_StatePhys = "Calf" :
    ( 0.56 * Dt_DMIn_ClfLiq / Dt_DMIn )
  + ( 1.1376*An_DE*0.93 - 0.1198*(An_DE*0.93)^2 + 0.0076*(An_DE*0.93)^3 - 1.2979 ) / ( An_DE*0.93 ) * Dt_DMIn_ClfDry / Dt_DMIn
An_BW > 0.16 * An_BW_Mature                 : 0.63
Parity > 0 & Mlk_Prod > 0                   : 0.66   (⚠ leitura incerta)
Parity > 0 & Mlk_Prod = 0                   : 0.66   (⚠ leitura incerta)
```
(An_DE em Mcal/kg MS; An_DE×0.93 = EM do alimento sólido; o polinômio é a Eq. 10-6 de ELg do cap. 10 ÷ EM. O coeficiente do líquido lido "0.56" — ⚠ cap. 10 [p.226] adota k_g do leite/sucedâneo = 0.55.)
**Eq. 20-267** [p.502] `Kr_ME_RE (Mcal/Mcal)` — eficiência ME→RE para ganho de reservas
| Critério | Valor |
|---|---|
| An_BW > 0.16 × An_BW_Mature & An_MilkProd = 0 | 0.60 |
| Mlk_Prod > 0 & Rsrv_Gain > 0 | 0.75 |
| Mlk_Prod > 0 & Rsrv_Gain < 0 | 0.89 |
A eficiência global é a média ponderada de Kf_ME_RE e Kr_ME_RE.
**Eq. 20-268** [p.502] `Body_MEuse (Mcal/d) = An_NEGain_Rsrv / Kr_ME_RE + An_NEGain_Frm / Kf_ME_RE`  (ME exigida para ganho; An_NEGain_Frm e An_NEGain_Rsrv não são definidos nesta parte: obtidos de An_REGain × 1/Kg_NEL_RE por componente; ⚠)
**Eq. 20-269** `NEgain_BWgain (Mcal/kg) = ( An_NEGain_Frm + An_NEGain_Rsrv ) / An_BWgain`
**Eq. 20-270** [p.502] `Body_MPuse (kg/d) = An_NPgain / Kg_MP_NP`  (rótulo impresso "Mcal/d"; é kg/d; ⚠)
**Eq. 20-271** [p.503] (conferida a 300 dpi) `Kg_MP_NP (g/g)`
```
An_StatePhys = Calf                                              : ( 0.70 - 0.532 * (An_BW/An_BW_mature) ) * 0.86
An_Parity = 0 & An_BW_empty/An_BW_mature_empty > 0.12            : ( 0.64 - 0.3 * (An_EBW/An_EBW_mature) ) * 0.86
An_Parity > 0                                                    : Trg_MP_NP * 0.86
```
(parênteses externos deduzidos pelo ")" impresso; ⚠.) "Não deve ser visto como a eficiência máxima atingível; a composição AA da PM afeta a eficiência e não foi considerada. **Eficiência mínima fixada em 0.39.**" [p.503].

## 14. Mantença: energia [pp.503–504]
**Eq. 20-272** [p.503] `An_NEmUse_NS (Mcal/d)` (sem estresse ambiental)
```
Calves: Dt_DMIn_LiquidFeed > 0           : 0.0769 * An_EBW^0.75
Calves: Dt_DMIn_LiquidFeed = 0           : 0.097  * An_BW^0.75
Heifers: Dt_DMIn_Milk = 0 & Parity = 0   : 0.10   * An_BW^0.75
Cows: Parity > 0                         : 0.10   * An_BW_NPr_3^0.75
```
**Eq. 20-273** [p.503] estresse térmico/frio: `An_NEmUse_Env (Mcal/d)`
```
LCT < T < UCT              : 0
T < LCT   & An_BW < 100    : 0.00201 * (LCT - T) * An_BW^0.75
T > UCT   & An_BW < 100    : 0.00201 * (T - UCT) * An_BW^0.75
```
T = temperatura média (°C); LCT/UCT = temperaturas críticas inferior/superior da zona termoneutra (Eqs. 20-2 e 20-3, Parte A). Para An_BW ≥ 100 não há linha: tratado em outra parte (não informado aqui).
**Eq. 20-274** [p.503] pastejo: `An_NEmUse_Graze (Mcal/d)`
```
Dt_PastIn/Dt_DMIn < 0.005   : 0
Dt_PastIn/Dt_DMIn >= 0.005  : 0.0075 * An_BW^0.75 * ( 600 - 12 * Dt_PastSuppIn ) / 600
```
Dt_PastIn = MS de pastagem (kg/d); Dt_PastSuppIn = MS não pastagem (kg/d). Topografia plana.
**Eq. 20-275** [p.503] `An_NEmUse_Parlor (Mcal/d) = 0.00035 * Env_DistParlor/1000 * Env_TripsParlor * An_BW`  (Env_DistParlor = distância ida e volta lote–sala de ordenha (m); Env_TripsParlor = nº de ordenhas/viagens por dia; superfície plana)
Texto: custos de locomoção em vacas já estão em grande parte nas exigências de mantença de câmara metabólica (ficar em pé, comer, beber); bezerros e novilhas via abate comparativo em baias; ignorar locomoção em confinamento subestima ligeiramente a mantença; mais importante em pastagem [p.503].

### Continuação na p.504 (contexto; esta seção termina lá) — conferida na imagem a 150–400 dpi
**Eq. 20-276** `An_NEmUse_Topo (Mcal/d) = 0.0067 * Env_TopoParlor/1,000 * An_BW`  (corrigido pela imagem: 0.0067; OCR leu 0.006). Env_TopoParlor = subida total diária (m; só subida): Suave 50 m/d; Moderado 200 m/d; Forte 500 m/d.
**Eq. 20-277** `An_NEmUse_Act (Mcal/d) = An_NEmUse_Graze + An_NEmUse_Parlor + An_NEmUse_Topo`
**Eq. 20-278** `An_NEmUse (Mcal/d) = An_NEmUse_NS + An_NEmUse_Env + An_NEmUse_Act`
**Eq. 20-279** `An_MEmUse (Mcal/d) = An_NEm / Km_ME_NE`
**Eq. 20-280** `Km_ME_NE(ClfLiq) = 0.718`; **Eq. 20-281** `Km_ME_NE(ClfDry) = 1.1104 - (0.0946*Dt_ME) + (0.0065*Dt_ME^2) - 0.7783/Dt_ME` (Dt_ME em Mcal/kg MS)
**Eq. 20-282** `Km_ME_NE`: Calf & An_ME_ClfDry > 0 & Dt_DMIn_ClfLiq = 0 : "Km_NE" (valor/variável como impresso); Calf & Dt_DMIn_ClfLiq = 0 : 0.69; non-Calf & Parity = 0 : 0.63; Parity > 0 : 0.66 (⚠ tabela como impressa; as duas primeiras linhas parecem incoerentes — as eficiências parciais 20-280/281 são ponderadas pela quantidade de alimento líquido e seco).
Eqs. 20-283 a 20-286 (descamação: Scrf_CP_g = 0.20 × An_BW^0.60; Scrf_TP_g = Scrf_CP_g × 0.86; Scrf_TP (kg/d) = Scrf_TP_g/1,000; Scrf_AA(i)_g = Scrf_NP_g × AA(i)_NP_Scrf/100) pertencem à seção de proteína de mantença que continua em p.504–505 (fora do intervalo).

---
## 15. Regras de decisão / restrições para o otimizador
- Razão MlkNP_MlkNPmax (Eq. 20-208) deve ser **≤ 0.9**; senão aumentar Mlk_NP_RHA(305d) [p.495].
- An_LactDay limitado a **375 d** nas Eqs. 20-215/216 [pp.496–497].
- Eficiência Kg_MP_NP mínima **0.39** [p.503].
- Eficiência-alvo PM→proteína do leite: 0.69 (referência mínima atingível; 0.68 esperado com dietas ótimas) [p.496].
- Uso de `Use_dcNDF_IV48`: 0 = lignina; 1 = IV48 só para forragens; 2 = IV48 em todos; fallback para lignina se IV ausente [p.485].
- Opções de override: `mPrt_eqn`, `mFat_eqn`, `mProd_eqn` = 0 ⇒ usar `Trg_MilkTPp`, `Trg_MilkFatp` e o volume alvo do usuário em todos os cálculos subsequentes [pp.495–497].
- Bezerras: usar abordagem empírica de trato total; desligar digestão ruminal [p.487]; digestibilidade de AG = 81 % para concentrados [p.488].
- Gestação/pós-parto: involução uterina por 100 d após o parto [pp.498–499].

## 16. Lógica e fluxo (ordem de cálculo)
1. Digestão (por alimento → dieta → animal): rOM e amido (p.484) → FDN (20-110…20-120, usa IMS/PC e amido) → PNDR/PB microbiana/PM (20-121…20-142) → AAE (20-143…20-152) → AG (20-153…20-163) → MO digestível/fecal (20-164…20-169).
2. Energia: EB (20-170/171) → ED por nutriente (20-172…20-182) → An_DE (20-183) → **An_DEInp (20-184)**.
3. Entradas do bloco de leite: Abs_AA (20-148) e Abs_NEAA/OthAA (20-150, 20-186a), An_DEInp, An_DigNDF, An_BW, Mlk_NP_RHA(305d) → f_g (20-207) → coeficientes escalonados → **Mlk_NP_g (20-185 escalonada)** [ou meta do usuário] → Mlk_AA(a) (20-211), Mlk_MPuse (20-212/213) → Milk_Fat_g (20-215) e Mlk_Prod (20-216; usa kg de NP e gordura, An_DEIn) → Milk_NEp/NEuse/MEuse (20-217…20-223).
4. Gestação: Fetus_Wt, LengthGest, DayGest/DayLact → GrUter_Wt (20-225…20-229) → An_BW_NPr (20-230) → ganhos (20-231…20-233) → Gest_NEgain/NPgain (20-234/235) → Gest_MEuse/MPuse/AA (20-236…20-240).
5. Crescimento: GutFill (20-241) → EBW (20-242…20-246) → ganhos (20-247…20-252) → composição (20-253…20-263) → An_REGain (20-264) → Kg e eficiências (20-265…20-267) → Body_MEuse (20-268) e Body_MPuse (20-270/271).
6. Mantença (20-272…20-282, continua na p.504–505).
Referências cruzadas: Eq. 20-2/20-3 (LCT/UCT, Parte A); Eqs. 20-355/356 (eficiências de PM, fim do cap. 20); Tabela 6-5 (composição AA); cap. 4 (digestibilidade de AG); cap. 6 (Eq. 20-185 origem; AA); cap. 10 (ELg/ELm de bezerros; Eq. 10-5, 10-6, 10-4); cap. 3 (0.82, 0.18, 0.094).

## 17. Limitações, incertezas e mudanças vs. NRC 2001
- A predição de proteína do leite é quadrática e tende a platô/queda com o aumento do aporte (a produção cresce ~90 kg/ano); por isso o escalonamento pelo mérito genético do rebanho, ainda "provisório" (escalar baseado na produção do rebanho captura também manejo) [pp.491–495].
- Dividir os dados por 2000 ou incluir "idade" sugeriu platô crescente, mas o modelo ficou superparametrizado [p.492].
- Gordura do leite: "provavelmente não tão robusta como proteína" (RMSE 18.9 %, CCC 0.62) [p.496]. Volume: CCC 0.75 [p.497].
- Fatores de digestibilidade intestinal de AA relativos à PNDR = 1 (dados inadequados) [pp.487–488]. Biohidrogenação de AG não modelada [p.489].
- Predição de PM a partir de eficiência estática (NRC 2001) "não é particularmente precisa" [p.495]; Kl_MP_NP,Trg = 0.69 como referência.
- Sem predição de AG fecais individuais [p.489]. Opções de predição de ganho de frame/reservas "não implementadas no código" [p.501].
- Predições de digestão ruminal não incluem dados de bezerras [p.487]. Composição do útero em involução ligeiramente subestimada [p.500].
- Mudanças vs. NRC 2001: PB microbiana verdadeira 82.4 % e digestibilidade 80 % (cap. 6), correção 1.15 de hidratação dos AA, equação de proteína do leite com 5 AAE + energia + FDN, exigências de gestação por modelo de útero gravídico (Koong) em lugar de equações NRC; Ky_MP_NP = 0.33 e K ME→NE gestação 0.14 mantidos de NRC/Ferrell et al.

## 18. Conceitos e evidências relevantes
- PNDR digerida usa digestibilidade intrínseca por ingrediente; PB microbiana: 80 % digestível e 82.4 % PVer [p.486].
- PB endógena fecal repartida arbitrariamente entre PDR e PNDR proporcionalmente a An_RDPIn/An_CPIn [p.487].
- Lactose sintase depende de α-lactalbumina; proteína do leite é determinante primário do volume [p.496].
- Equação de energia do leite: 9.29 (gordura), 5.85 (PVer; 5.5 se PB), 3.95 (lactose) Mcal/kg [p.497].
- Conteúdo final do útero gravídico: 0.950 Mcal/kg e 123 g PB/kg; PVer/PB = 0.86 [p.499].

## 19. Dúvidas / riscos de OCR (⚠)
1. ⚠ **Eq. 20-113** sem "/100": unidades de Fd_dcNDF_Base (%) e Fd_NDF (% MS) — normalizar para kg/d e % da FDN em 20-114.
2. ⚠ **Eq. 20-115**: conferida na imagem; coeficientes −1.1 e −0.59 e centros 0.035/0.26 lidos a 150 dpi (nítidos).
3. ⚠ **Eq. 20-140** (DryFd, não bezerra): "12.0 + (0.12 × An_NDF) × (IMS)" — unidade/precedência (g/d vs kg/d) ambígua; transcrito literal.
4. ⚠ **Eq. 20-138**: bezerra só com sólidos (An_CPIn_ClfLiq = 0) não aparece na tabela (texto: 70 % digestível ⇒ 0.30 de PB fecal).
5. ⚠ **Eq. 20-150/152**: An_MPIn em g/d × 1.15 vs. 20-136 em kg/d (conversão ×1000 implícita).
6. ⚠ **Eq. 20-184**: definição subtrai só ED do NNP; texto diz "ED a partir da proteína".
7. ⚠ **Eq. 20-200**: denominador impresso 4a_1² (esperado 4a_1, coerente com 20-201).
8. ⚠ **Eq. 20-210**: numerador/denominador (coeficiente quadrático vs. linear) parecem trocados; fórmula correta do máximo: −(linear)²/(4·quadrático).
9. ⚠ **Eqs. 20-197/198**: valem com Y_2 e Ym_2 SEM intercepto (verificação numérica minha; ver §8).
10. ⚠ **Eq. 20-207 → escalar**: o texto não escreve como f_g entra (interpretado como múltiplo do platô; Ym_2 = f_g × Ym_1 sem intercepto).
11. ⚠ **Eq. 20-209**: coeficiente 0.077 (vs 0.0773 em 20-185); Σ sobre "N_EAA" = os 5 AAE com termos lineares.
12. ⚠ **Eq. 20-216**: termo de PC ausente apesar de o texto citar centragem em 612 kg; NP e gordura em kg/d; rótulo de override cita Trg_MilkTPp.
13. ⚠ **Eq. 20-217**: forma "% / (Milk × 100)" ambígua; usar 20-218 como forma dimensionalmente coerente (kg/kg).
14. ⚠ **Eq. 20-222**: numerador "Milk_NE" (= Milk_NEuse).
15. ⚠ **Tabela 20-10**: energia do útero gravídico em T = 280 impressa 88.6 Mcal; a Eq. 20-224 com os parâmetros dá 83.9 (≈ 0.950 Mcal/kg × 89 kg = 84.6). Conferido na imagem: 88.6 está impresso.
16. ⚠ **Eq. 20-227/232/229**: aproximação "para trás" não inversa de 20-224; Uter_Wt vs GrUter_Wt em 20-232; cabeçalho "kg/kg BW" em 20-229; valor 0.204 em "Otherwise".
17. ⚠ **Eq. 20-239/240**: nomes GrUter_NP_gain e Gest_MP não definidos explicitamente (= Gest_NPgain_g e Gest_MPuse_g).
18. ⚠ **Eq. 20-241**: linha 3 sobreposta à linha 1 (inalcançável em avaliação ordenada); casos não cobertos.
19. ⚠ **Eq. 20-246**: "× BW" extra com BW_BCS = 0.094·An_BW.
20. ⚠ **Eq. 20-253**: sem caso Parity > 0. **Eq. 20-255**: origem do fator 0.85 não explicada. **Eq. 20-264**: Body_CPgain não definido.
21. ⚠ **Eq. 20-266** (tabela em imagem de baixa resolução): coeficiente do líquido lido "0.56" (cap. 10 usa 0.55); valores das duas últimas linhas ilegíveis, lidos como 0.66.
22. ⚠ **Eq. 20-268**: An_NEGain_Frm/An_NEGain_Rsrv não definidos nesta parte. **Eq. 20-270**: unidade impressa "Mcal/d" (deveria ser kg/d). **Eq. 20-271**: parênteses.
23. ⚠ **Eq. 20-273**: sem linha para An_BW ≥ 100. **Eq. 20-282** (p.504): linhas 1–2 incoerentes como impressas.
24. ⚠ Termos fRum, fSI, fArt, SI_dcMiCP, Fd_ttdcFA: definidos na Parte A/outros capítulos — conferir.
25. ⚠ OCR corrigido pela imagem: Tabela 20-9 FDN 4.2 (OCR "42"); Eq. 20-276 0.0067 (OCR "0.006"); Eq. 20-140 (OCR ilegível); Eq. 20-241 (OCR garbled); Eq. 20-266.

COBERTURA: páginas impressas lidas 485–503 integralmente (texto OCR + imagens a 150 dpi, com ampliações de 230–600 dpi nas equações frágeis); p.484 e p.504 lidas como contexto (Eqs. 20-95–20-109 listadas; Eqs. 20-276–20-282 transcritas por continuarem a seção de locomoção/mantença; 20-283–20-286 apenas listadas). Ficou de fora/incerto: partes ilegíveis da Eq. 20-266 (raster 106 ppi), definição de termos da Parte A (p.≤483) e Eqs. 20-355/356 (fora do intervalo).

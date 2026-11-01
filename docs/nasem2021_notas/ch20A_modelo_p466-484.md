# NASEM 2021 — Capítulo 20 (Descrição e Avaliação do Modelo), PARTE A — notas técnicas

**Páginas impressas cobertas: 466–484** (p.485 lida só como contexto de continuação; ver fim do arquivo).
Trecho: "Abreviaturas e unidades do modelo" (466-471), "Entradas do modelo" (467-472), "Aporte de nutrientes" (472-484): água, IMS, composição da dieta, infusões, digestão ruminal de FDN/amido, PDR/PNDR, proteína microbiana/endógena, fluxo ruminal de AA, digestão de amido e de MO residual no trato total.

Usado diretamente no modelo? **Cap. 20 (466-484): SIM** (núcleo do simulador; o texto foi escrito transcrevendo o código R; em caso de divergência o código R prevalece [p.472]).

Convenção de leitura deste arquivo: equações transcritas com `*` multiplicação, `^` expoente, `_` já faz parte dos nomes de variável do livro (ex.: `Dt_DMIn`). Subscritos do livro (f, a, Rum, SI, LiqFd...) escritos como `_f`, `[Rum]` etc. quando necessário. Toda equação foi conferida contra a imagem da página (dpi 150, e recortes a 300-400 dpi nas complexas: 20-1, 20-4 a 20-6, 20-10, 20-11, 20-16, 20-18, 20-21, 20-22, 20-52, 20-53, 20-60, 20-61, 20-74/75, 20-95, 20-106 a 20-108, Tab. 20-7, Tab. 20-8).

---

## 1. Papel no simulador
O capítulo define o esquema de nomes (Local_Nutriente_Modificador), unidades, ENTRADAS do modelo e a primeira metade do modelo: **aporte de nutrientes** (do alimento escolhido até os nutrientes digeridos/absorvidos). Parte B (fora deste bloco) trata da utilização (exigências, produção). Aqui: ingestão de água e de MS (várias equações por estado fisiológico), composição e ingestão de nutrientes por alimento e dieta, infusões, digestão ruminal e do trato total de FDN, amido e MO residual, PDR/PNDR, proteína microbiana e endógena, fluxos de AA que saem do rúmen.

## 2a. DICIONÁRIO — convenções de nomes e unidades [pp.466-467]
- Padrão: **Local_Nutriente_Modificador** (Location Nutrient Modifier). Ex.: `Rum_DigNDF`, `Fd_NDF`, `Dt_NDF`, `Du_NDF`, `Fe_NDF` = FDN do alimento, da dieta, digerida no rúmen, fluindo no duodeno, nas fezes [p.466].
- Duplo local para fluxos rastreados: usa-se o 2º local dentro do nome do nutriente: `SI_RUP` (PNDR no intestino delgado), `SI_dcRUP` (coef. de digestão intestinal da PNDR), `SI_DigRUP`, `SI_DigAARUP` [p.466].
- Mantidas siglas históricas: PDR=RDP, PNDR=RUP; D=digerido, M=metabolizado, N=líquido (DE, ME, NE, MP, NP) [p.466].
- **Sufixo `In`** = ingestão/aporte (kg/d ou g/d). **Sem `In`** = concentração (% da MS para ingredientes/nutrientes dietéticos). Ex.: `Rum_DigCPIn` (aporte), `Rum_DigCP` (concentração na MS) [p.467].
- **`_CP`** (sublinhado + nutriente de referência) = concentração relativa a outra entidade, em % salvo indicação (ex.: `Rum_DigCP_CP` = % da PB; `Fd_CPB_CP` = % da PB do alimento na fração B) [p.467].
- **`out`** = fluxo que sai do local (ex.: `Fec_DMout`; convenção "aprovada para uso futuro", não plenamente adotada; `Fe_OM` denota SAÍDA de MO fecal, não concentração) [p.467].
- **Unidades padrão**: tempo = 1 dia; massa = kg para macronutrientes; **`g` ao fim do nome (`_g`)** = gramas (AA são em g/d); vitaminas e minerais: UI, mg ou g conforme o nutriente. PC em kg; IMS e produção de leite em kg/d [p.467].
- **Subscritos**: `f` = alimento (ex.: `Fd_CP_f` PB do alimento f; `Fd_NDFIn_f`; `Fd_dcFA_f`; `Fd_CPB_CP_f`); `a` = cada AA individual; `fa` = cada AG individual [p.467]. Exemplos do livro: `Dt_StIn`, `Dt_DEIn`, `Dt_ArgIn_g` (g/d), `Du_LeuRUP_g` (Leu na PNDR, g/d), `Body_NPgain`, `Mlk_NEout`, `Mlk_Fat_g` [pp.467-468].
- **Prefixos de local**: `Fd_` alimento individual; `Dt_` dieta; `An_` = animal total = `Dt_Xxx + Inf_Xxx` (dieta + infusão); `Inf_Xxx` = infusão; `InfRum_`, `InfSI_` = infusão no rúmen / intestino delgado [Tab. 20-2 nota a; p.479].
- Fósforo: NÃO usar "P" para proteína; "Ph" evitado (conflito futuro com pH); usa-se `P` para fósforo total, `Pinorg`, `Porg` [p.467].

### Tabela 20-1 — Local e nutrientes [p.468] (transcrita; conferida na imagem)
| Local | Descrição | | Nutriente | Descrição |
|---|---|---|---|---|
| Fd | Alimento | | Wt | Peso |
| Dt | Dieta | | GE | Energia bruta |
| An | Animal | | DE | Energia digestível |
| | | | DEnp | DE menos DE de TP |
| Rum | Rúmen | | ME | Energia metabolizável |
| SI | Intestino delgado | | GasE | Energia gasosa |
| LI | Intestino grosso | | NE | Energia líquida |
| TT | Trato digestivo total | | DM | Matéria seca |
| Fe | Fezes | | OM | Matéria orgânica |
| Ur | Urina | | NDF | Fibra em detergente neutro |
| Body | Corpo vazio | | ForNDF | FDN de forragem |
| Frm | Frame corporal | | ADF | Fibra em detergente ácido |
| Rsrv | Reservas corporais | | Lg | Lignina |
| Gest | Gestação | | St | Amido |
| GrUter | Útero gravídico | | rOM | MO residual |
| Uter | Útero com carúnculas | | CP | Proteína bruta |
| Fet | Feto | | TP | Proteína verdadeira |
| Mlk | Leite e lactação | | MP | Proteína metabolizável |
| Scrf | Descamação | | NP | Proteína líquida |
| Env | Ambiente do animal | | CPA | PB fração A, in situ |
| (Outras abrev.) | | | CPB | PB fração B, in situ |
| Conc | Concentrados | | CPC | PB fração C, in situ |
| For | Forragens | | NPN | Nitrogênio não proteico |
| ForDry | Forragem seca | | FA | Ácidos graxos |
| ForWet | Forragem fresca | | Ash | Cinzas |
| Past | Pasto | | Arg, His, Ile, Leu, Lys, Met, Phe, Thr, Trp, Val | os 10 AA essenciais |
| Dc | Digestibilidade | | C12 / C14 / C16 / C16.1 | láurico / mirístico / palmítico / palmitoleico |
| Dig | Digerido | | C18.0 / C18.1c / C18.1t | esteárico / oleico / vacênico + elaídico |
| | | | C18.2 / C18.3 | linoleico / linolênico |
| | | | OtherFA | Outros AG |
| Minerais e vitaminas: Ca cálcio; P fósforo total; Pinorg P inorgânico; Porg P orgânico; Na sódio; Mg magnésio; K potássio; Cl cloro; S enxofre; Co cobalto; Cu cobre; Fe ferro; I iodo; Mn manganês; Mo molibdênio; Se selênio; Zn zinco | | | VitA / VitD / VitE | Vitaminas A, D, E |
| | | | DCAD | Cátions–ânions |

(Nota: em Fd/Dt/An o "Fe" de local = fezes; "Fe" de nutriente = ferro.)

### Tabela 20-2 — Abreviaturas: dieta e digestão de macronutrientes [p.469] (conferida)
Colunas: Nutriente | Dieta (% MS) | Dieta (kg/d ou g/d) | Saída ruminal | Digerido/absorvido | Fezes. Nota a: concentrações/ingestões de alimento individual usam prefixo `Fd_` no lugar de `Dt_`; conjunto adicional para `Dt_Xxx + Inf_Xxx` rotulado `An_Xxx`.
| Nutriente | % MS | kg/d | Saída ruminal | Digerido/absorvido | Fezes |
|---|---|---|---|---|---|
| Matéria seca | Dt_DM | Dt_DMIn | | An_DigDM | Fe_DM |
| Água | | An_WaIn | | | |
| Forragem total | Dt_For | Dt_ForIn | | | |
| Forragem seca | Dt_ForDry | Dt_ForDryIn | | | |
| Forragem fresca | Dt_ForWet | Dt_ForWetIn | | | |
| Concentrado | Dt_Conc | Dt_ConcIn | | | |
| Pasto | Dt_Pasture | Dt_PastureIn | | | |
| Cinzas | Dt_Ash | Dt_AshIn | | | |
| Matéria orgânica | Dt_OM | Dt_OMIn | | An_DigOM | Fe_OM |
| MO residual | Dt_rOM | Dt_rOMIn | | An_DigrOMa | Fe_rOM |
| Nitrogênio | | | | | Fe_N_g |
| Proteína bruta | Dt_CP | Dt_CPIn | Du_CP | An_DigCP | Fe_CP, Fe_InfCP |
| Proteína verdadeira | Dt_TP | Dt_TPIn | Du_TP | An_DigTP | |
| Proteína metabolizável | Dt_MP | Dt_MPIn | | | |
| N não proteico (NPN, expresso como N) | Dt_NPN | Dt_NPNIn | Du_NPN | | |
| PB equivalente de NPN | Dt_NPNCP | Dt_NPNCPIn | Du_NPNCP | | |
| MS de fonte NPN | Dt_NPNDM | Dt_NPNDMIn | Du_NPNDM | | |
| Fração A da PB | Dt_CPA | Dt_CPAIn | | | |
| Fração B da PB | Dt_CPB | Dt_CPBIn | | | |
| Fração C da PB | Dt_CPC | Dt_CPCIn | | | |
| PB ruminalmente degradada | Dt_RDP | Dt_RDPIn | | | |
| PB ruminalmente não degradada | Dt_RUP | Dt_RUPIn | Du_RUP | Du_idRUP | Fe_RUP |
| PB microbiana | | | Du_MiCP_g | Du_idMiCP_g | Fe_MiCP |
| N microbiano | | | Du_MiN_g | Du_idMiN_g | |
| TP microbiano | | | Du_MiTP_g | Du_idMiTP_g | |
| PB endógena | | | Du_CPend_g | | Fe_CPend_g |
| N endógeno | | | Du_Nend_g | | Fe_Nend_g |
| Amido | Dt_St | Dt_StIn | Du_St | An_DigSt | Fe_St |
| FDN | Dt_NDF | Dt_NDFIn | Du_NDF | An_DigNDF | Fe_NDF |
| FDN de forragem | Dt_ForNDF | Dt_ForNDFIn | | | |
| FDA | Dt_ADF | Dt_ADFIn | | | |
| Lignina | Dt_Lg | Dt_LgIn | | | |
| Ácidos graxos | Dt_FA | Dt_FAIn | Du_FA | An_DigFA | Fe_FA |
| (Energia, Mcal/kg e Mcal/d) Energia bruta | Dt_GE | Dt_GEIn | | | Fe_GE |
| Energia digestível | Dt_DE | Dt_DEIn | | | |
| Energia metabolizável | Dt_ME | Dt_MEIn | | | |

Nota b: NPN = fontes sem AA livres ou ligados a peptídeos (ureia, sais de amônio); expresso como N (NPN), equivalente de PB (NPNCP) ou MS (NPNDM). Nota c: CPA = PB que escapa de análise in situ no tempo 0; CPC = PB resistente à degradação no tempo infinito; CPB = PB que degrada em função do tempo no rúmen. [A nota impressa na p.469 grafa "CPC" nas duas últimas definições (erro tipográfico do livro); a segunda foi lida como CPB (corrigido na verificação).]

### Tabela 20-3 — Abreviaturas: dieta e digestão de AA e AG [p.470] (conferida)
Padrão para os 10 AA (Arg, His, Ile, Leu, Lys, Met, Phe, Thr, Trp, Val), com `Xxx` = o AA:
| Item | % da MS | kg/d ou g/d | Saída PNDR (g/d) | Saída microbiana (g/d) | Digerido/absorvido (g/d) |
|---|---|---|---|---|---|
| AA | Dt_Xxx | Dt_XxxIn_g | Du_XxxRUP_g | Du_XxxMic_g | Abs_Xxx_g |
Ex.: Dt_Arg, Dt_ArgIn_g, Du_ArgRUP_g, Du_ArgMic_g, Abs_Arg_g.
Ácidos graxos (concentração Dt_, ingestão Dt_..In, digerido An_Dig..): C12:0 → Dt_C12, Dt_C12In, An_DigC12; C14:0 → Dt_C14 / Dt_C14In / An_DigC14; C16:0 → Dt_C16 / Dt_C16In / An_DigC16; C16:1 → Dt_C16.1 / Dt_C16.1In / An_DigC16.1; C18:0 → Dt_C18 / Dt_C18In / An_DigC18; C18:1 trans → Dt_C18.1t / Dt_C18.1tIn / An_DigC18.1t; C18:1 cis → Dt_C18.1c / Dt_C18.1cIn / An_DigC18.1c; C18:2 → Dt_C18.2 / Dt_C18.2In / An_DigC18.2; C18:3 → Dt_C18.3 / Dt_C18.3In / An_DigC18.3; Outros AG → Dt_FAoth / Dt_FAothIn / An_DigFAoth.

### Tabela 20-4 — Abreviaturas: mantença e uso de energia e proteína [p.470] (conferida)
| Nutriente | Mantença | Fezes | Urina | Descamação | Atividade | Ambiente |
|---|---|---|---|---|---|---|
| Energia digestível | | | Ur_DEout | | | |
| Energia metabolizável | An_MEmUse | | | | | |
| Energia líquida | An_NEmUse | | | | An_NEm_Act | An_NEm_Env |
| Proteína líquida | | Fe_NPend_g | Ur_NPend_g | Scrf_NP_g | | |
| Nitrogênio | | Fe_N_g | Ur_Nout_g | | | |
| Fósforo | | Fe_P_g | Ur_P_g | | | |
| Fator: Temperatura | | | | | | Env_TempCurr |
| Fator: Distância | | | | | | Env_DistParlor |
| Fator: Topografia | | | | | | Env_Topo |
| AA (Xxx = Arg...Val) | | Fe_XxxMet_g | Ur_XxxEnd_g | Scrf_Xxx_g | | |

### Tabela 20-5 — Uso total e produtivo de energia (Mcal/d), proteína e gordura (kg ou g/d) [p.471] (conferida)
| Nutriente | Total | Produção | Crescimento | Gestação | Leite |
|---|---|---|---|---|---|
| Peso | An_BW | | Body_Gain | GrUter_Wt, Uter_Wt, Fet_Wt, GrUter_BWgain | Mlk_Prod |
| Energia metabolizável | | An_MEprod_Avail | | Gest_Meuse | Mlk_MEout |
| Energia líquida | An_NEgain | An_NEprod_Avail | | Gest_Neuse | Mlk_NEout, Mlk_NE_Milk |
| Proteína | | | Body_NPgain | Gest_NP_g | Mlk_NP_g, MlkNP_Milk |
| Gordura | Body_Fat | | Body_Fatgain | | Mlk_Fat_g, MlkFat_Milk |
| AA (g/d), Xxx=Arg..Val | An_XxxUse_g | | Body_XxxGain_g | Gest_Xxx_g | Mlk_Xxx_g |
| Tempo | | | An_AgeDay | An_GestDay | An_LactDay |
(Energia digestível: linha vazia na tabela.)

### Tabela 20-6 — Minerais e vitaminas [p.471] (conferida)
Sufixos de exigência: `_m` mantença, `_g` crescimento, `_y` gestação, `_l` lactação, `_req` exigência total. `Abs_XxxIn` = ingestão absorvida (g/d ou mg/d).
| Nutriente | Dieta (unid.) | Ingestão | Absorvido | Mantença | Cresc. | Gest. | Lact. | Exigência |
|---|---|---|---|---|---|---|---|---|
| Cálcio (% MS; g/d) | Dt_Ca | Dt_CaIn | Abs_CaIn | An_Ca_m | An_Ca_g | An_Ca_y | An_Ca_l | An_Ca_req |
| Cloro | Dt_Cl | Dt_ClIn | Abs_ClIn | An_Cl_m | An_Cl_g | An_Cl_y | An_Cl_l | An_Cl_req |
| Magnésio | Dt_Mg | Dt_MgIn | Abs_MgIn | An_Mg_m | An_Mg_g | An_Mg_y | An_Mg_l | An_Mg_req |
| Fósforo | Dt_P | Dt_PIn | Abs_PIn | An_P_m | An_P_g | An_P_y | An_P_l | An_P_req |
| Potássio | Dt_K | Dt_KIn | Abs_KIn | An_K_m | An_K_g | An_K_y | An_K_l | An_K_req |
| Sódio | Dt_Na | Dt_NaIn | Abs_NaIn | An_Na_m | An_Na_g | An_Na_y | An_Na_l | An_Na_req |
| Enxofre | Dt_S | Dt_SIn | | | | | | An_S_req |
| (mg/kg MS; mg/d) Cobalto | Dt_Co | Dt_CoIn | | | | | | An_Co_req |
| Cobre | Dt_Cu | Dt_CuIn | Abs_CuIn | An_Cu_m | An_Cu_g | An_Cu_y | An_Cu_l | An_Cu_req |
| Iodo | Dt_I | Dt_IIn | | | | | | An_I_req |
| Ferro | Dt_Fe | Dt_FeIn | Abs_FeIn | An_Fe_m | An_Fe_g | An_Fe_y | An_Fe_l | An_Fe_req |
| Manganês | Dt_Mn | Dt_MnIn | Abs_MnIn | An_Mn_m | An_Mn_g | An_Mn_y | An_Mn_l | An_Mn_req |
| Selênio | Dt_Se | Dt_SeIn | | | | | | An_Se_req |
| Zinco | Dt_Zn | Dt_ZnIn | Abs_ZnIn | An_Zn_m | An_Zn_g | An_Zn_y | An_Zn_l | An_Zn_req |
| (UI/kg; UI/d) Vitamina A | Dt_VitA | Dt_VitAIn | | | | | | An_VitA_req |
| Vitamina D | Dt_VitD | Dt_VitDIn | | | | | | An_VitD_req |
| Vitamina E | Dt_VitE | Dt_VitEIn | | | | | | An_VitE_req |
(Molibdênio e DCAD aparecem só na Tab. 20-1.) [Nesta tabela o livro imprime o sufixo de ingestão em minúsculas em vários símbolos (Dt_Pin, Dt_Kin, Dt_Sin, Dt_Coin, Dt_Cuin, Dt_Iin, Dt_Fein, Dt_Mnin, Dt_Sein, Dt_Znin, Dt_VitAin/VitDin/VitEin, Abs_Pin, Abs_Kin); a tabela acima normaliza para "In" conforme a convenção do cap. (corrigido na verificação: uso de "In" confirmado como intenção; grafia impressa registrada).] Texto p.479: concentrações de vitaminas e minerais são "estequiometricamente ajustadas" às unidades da tabela (fórmula não dada).

---

## 2b. ENTRADAS do modelo [pp.467-468, 469, 472]
Texto: entradas = fatores do animal, dos alimentos e ambientais; animal e ambiente semelhantes ao NRC 2001; alimentos expandidos (mais informação de carboidratos e composição de AG, usada só para gerar concentrações dietéticas de AG). "Todas as entradas não são necessárias para cada tipo de animal e fase" [p.467]. O livro NÃO dá valores padrão nem faixas, exceto onde indicado abaixo ("não informado" = o livro não diz).

| # | Variável | Símbolo (como impresso) | Unidade | Definição / valores | Obrig./padrão/faixa | pág. |
|---|---|---|---|---|---|---|
| 1 | Raça | An_Breed | texto | "Holstein", "Jersey", "Other" | não informado | 467 |
| 2 | Estado fisiológico atual | An_StatePhys | texto | "Calf", "Heifer", "Dry Cow", "Lactating Cow", "Other" | não informado | 467 |
| 3 | Peso ao nascimento | Fet_BWbrth | kg | | não informado | 467 |
| 4 | Peso corporal à maturidade | An_BWmature | kg | | não informado | 467 |
| 5 | Produção atual de proteína verdadeira do leite em 305 d | An_305RHA_MlkTP | kg/305 d | | não informado | 467 |
| 6 | Peso corporal | An_BW | kg | | não informado | 467 |
| 7 | Escore de condição corporal | An_BCS | escala 1 a 5 | | 1-5 | 467 |
| 8 | Idade | An_Age | dias | | não informado | 467 |
| 9 | Paridade | An_Parity | 0/1/2 | 0 bezerras e novilhas; 1 primípara; 2 multípara (nas Eqs. 20-21 usa-se valor real 1 a 2; média de grupo) | 0,1,2 | 467, 475 |
| 10 | Duração da gestação | An_GestLength | dias | (nas Eqs. aparece como An_DayGestLength) | não informado | 467 |
| 11 | Idade à 1ª concepção | An_AgeConcept1st | dias | **não usada** ("unused"; reservada p/ simulações de crescimento) | — | 467 |
| 12 | Dias em lactação na concepção | An_DIMConcept | dias | **não usada** (reservada p/ lactação completa) | — | 467 |
| 13 | Dias em gestação | An_GestDay | dias | (nas Eqs.: An_DayGest) | não informado | 467 |
| 14 | Dias em lactação | An_LactDay | dias | (nas Eqs.: An_DayLact) | não informado | 467 |
| 15 | Temperatura ambiente atual | Env_TempCurr | °C | | não informado | 467 |
| 16 | Distância piquete–sala de ordenha | Env_DistParlor | m/viagem | | não informado | 467 |
| 17 | Nº de idas piquete–ordenha | Env_TripsParlor | d^-1 | | não informado | 467 |
| 18 | Distância caminhada em subida/dia (só subida) | Env_Topo | m/d | | não informado | 467 |
| 19 | Ganho de frame alvo | Frm_GainTarget | kg/d | | não informado | 467 |
| 20 | Eq. de predição de ganho de frame | FrmGain_eqn | 0/1 | 0 = usar Frm_GainTarget; 1 = equação futura indefinida | 0 ou 1 | 467 |
| 21 | Ganho de reserva corporal alvo | Rsrv_GainTarget | kg/d | | não informado | 468 |
| 22 | Eq. de predição de ganho de reserva | RsrvGain_eqn | 0/1 | 0 = usar Rsrv_GainTarget; 1 = equação futura indefinida | 0 ou 1 | 468 |
| 23 | Produção de leite alvo | Trg_MilkProd | kg/d | | não informado | 468 |
| 24 | Lactose do leite alvo | Trg_MilkLacp | % | | não informado | 468 |
| 25 | Proteína verdadeira do leite alvo | Trg_MilkTPp | % | | não informado | 468 |
| 26 | Gordura do leite alvo | Trg_MilkFatp | % | | não informado | 468 |
| 27 | Eq. de predição de produção de leite | mProd_eqn | 0/1 | 0 = Trg_MilkProd; 1 = NRC 2021 | 0 ou 1 | 469 |
| 28 | Eq. de produção de proteína do leite | mPrt_eqn | 0/1 | 0 = Trg_MilkTP; 1 = NRC 2021 | 0 ou 1 | 469 |
| 29 | Eq. de produção de gordura do leite | mFat_eqn | 0/1 | 0 = Trg_MilkFat; 1 = NRC 2021 | 0 ou 1 | 469 |
| 30 | IMS alvo da dieta | Trg_Dt_DMI (nas Eqs.: Trg_Dt_DMIn / Trg_DMIn) | kg/d | | não informado | 469 |
| 31 | Eq. de IMS da dieta | DMIn_eqn | inteiro 0..11 | **Lista da p.469-472 (numeração 1-11, "0" = ingestão específica/integrada)**: 1 = alimento sólido p/ bezerra em dieta líquida (NRC 2021); 2 = todas as novilhas, "fatores do animal e dos alimentos" (NRC 2021) [texto impresso na p.469 diz exatamente isso; pelas Eqs. 20-23/20-10 deve ser só fatores do animal = Heif1, provável erro de tradução do livro; (corrigido na verificação)]; 3 = todas as novilhas, "fatores animais e fatores de alimentos" (NRC 2021); 4 = novilha Holandesa, fatores do animal, pré-parto p/ animal único; 5 = novilha Holandesa, animal + FDN da dieta, pré-parto animal único; 6 = novilhas Holandês×Jersey, fatores do animal, pré-parto animal único; 7 = idem 6 com FDN da dieta; 8 = vaca em lactação, PC e ECC (NRC 2021); 9 = vaca em lactação, animal e alimento (NRC 2021); 10 = vaca seca (NRC 2021); 11 = vaca seca (Hayirli et al. 2003). **Ver ⚠: a Eq. 20-23 (p.476) usa outra numeração (0-10).** | 0 a 11 | 469, 472 |
| 32 | Idade em que sólido é oferecido pela 1ª vez | An_AgeDryFdStart | dias | | não informado | 472 |
| 33 | Uso de digestibilidade in vitro da FDN | Use_DNDF_IV (nas Eqs.: Use_dcNDF_IV48) | 0/1/2 | 0 = não usar IV (usa lignina); 1 = IV ajusta FDN das forragens; 2 = IV ajusta FDN de todos | 0,1,2 | 472, 485 |
| 34 | Eq. de predição de PNDR | RUP_eqn | — | atualmente **não usada** | — | 472 |
| 35 | Efeito da monensina | Monensin_eqn | 0/1 | 0 = sem; 1 = com monensina | 0 ou 1 | 472 |
| 36 | Banco de dados de ingredientes (biblioteca de alimentos) | f, várias unidades | vários | concentrações de nutrientes por ingrediente (ver §2c) | — | 472 |
| 37 | Vetor de inclusão de alimentos (ordem = ingredientes f) | Fd_DMInp | % da MS | (ver ⚠: em algumas equações tratado como proporção kg/kg) | soma deveria ser 100 (não afirmado) | 472 |
| 38 | Vetor de infusões: taxas, coeficientes de digestibilidade e local | i, várias unidades | vários | locais: rúmen, abomaso, duodeno ou sangue; lidos de arquivo externo; **todas as infusões = 0 por padrão** | padrão 0 | 472 |
| 39 | Vetor de metas de eficiência de uso de AA e PM pós-absorção | Eff | fração 0 a 1 por AA | | faixa 0 a 1 | 472 |
| 40 | Rúmen subdesenvolvido em bezerro alimentado com leite (efeito na digestibilidade da dieta) | RumDevDisc_Clf | 0/1 | 0 = desenvolvido; 1 = subdesenvolvido | 0 ou 1 | 472 |
| 41 | Proteína não láctea em sucedâneo | NonMilkCP_ClfLiq | 0/1 | 0 = todas proteínas do leite; 1 = outras fontes | 0 ou 1 | 472 |

**Classificação dos animais** (para aplicação do modelo) [p.472]: bezerras até atingirem 16% do PC maduro; novilhas até o primeiro parto; vacas primíparas durante a 1ª lactação; multíparas depois. Vaca não lactante = "vaca seca". Machos seguem bezerras/novilhas e são "vacas secas" quando maduros.

## 2c. Entradas de biblioteca de alimentos exigidas pelas equações deste intervalo (por ingrediente f) [pp.473-485]
| Campo (como impresso) | Unidade | Usado em |
|---|---|---|
| Fd_Category (categoria) / Fd_Type_f,c (100 se na categoria c, 0 se não) | texto / 0-100 | Eq. 20-28, 20-39 |
| Fd_DM_f | % (matéria natural) | Eq. 20-27a |
| Fd_Ash, Fd_FA, Fd_CP | % MS | 20-6, 20-41, 20-42 |
| Fd_NDF, Fd_NDFIP, Fd_Lg, Fd_St | % MS | 20-29, 20-30, 20-41, 20-110 |
| Fd_Conc_f, Fd_For_f (indicadores 0/100) | % | 20-29, 20-60 |
| Fd_CPA_CP, Fd_CPB_CP, Fd_CPC_CP, Fd_NPN_CP | % da PB | 20-31 a 20-34 |
| Fd_AA(a)_CP (composição de AA do alimento) | g/100 g PB (bruto de hidrólise 24 h) | 20-48 |
| Fd_KdRUP_f | taxa de degradação da fração B (%/h; unidade não explicitada) | 20-60 |
| Fd_dcSt_f | % do amido | 20-88 (Tab. 3-1 cap. 3) |
| Fd_dcNDF_IV48 (digest. in vitro 48 h) | % da FDN | 20-111 |
| Fd_dcFA_f (citado p.467); Fd_dcrOMt (=96.1) | % | p.467; 20-99 |
| Fd_DMInp_f | % MS (entrada 37) | 20-5, 20-8, 20-9, 20-26, 20-28 |
Não definido neste intervalo: composição de NDIP (`Fd_NDFIP`: nome sugere PB insolúvel em FDN, % MS; ⚠), `Fd_KdRUP`.

---

## 4. EQUAÇÕES (ordem do livro)

### 4.1 Ingestão de água

**Eq. 20-1** [p.472] — An_WaIn (L/d), por An_StatePhys. Conferida em recorte 300 dpi.
```
An_WaIn (L/d) =
  Lactating Cow:   -91.1 + 2.93*Dt_DMIn + 0.61*Dt_DM + 2.49*Dt_CP
                   + 0.062*( Dt_Na/0.023 + (Dt_K/0.039)*10 )
                   + 0.76*Env_TempCurr
  Dry Cow / Heifer: 1.16*Dt_DMIn + 0.23*Dt_DM + 0.44*Env_TempCurr
                   + 0.061*(Env_TempCurr - 16.4)^2
  Other:           indefinido
```
- Dt_DMIn kg/d; Dt_DM = % MS da dieta (matéria seca da dieta como fornecida); Dt_CP % MS; Dt_Na e Dt_K % da MS (ver ⚠ de unidade); Env_TempCurr °C. Na vaca seca/novilha: sem intercepto. Novilhas: a equação de vaca seca aplica-se às novilhas **após o desmame** [p.472]. Bezerras e outros estados: indefinido.
- No livro o termo de Na/K é impresso `0.062 x (Dt_Na/0.023 + Dt_K/0.039 x 10)` com o "x 10" dentro do mesmo parêntese, aplicado ao termo do K. (A equivalente do cap. 9, Eq. 9-1, usa NaK em mEq/kg; ver ⚠.)
- Fonte: Appuhamy et al. 2016 (ver cap. 9, Eqs. 9-1 e 9-3). Estatísticas não citadas aqui.

### 4.2 Ingestão de matéria seca — conceitos [p.473]
- IMS pode ser **especificada pelo usuário** (observada ou meta `Trg_DMIn`, kg MS/d) ou estimada. O modelo calcula todas as equações independentemente de idade/estado; o usuário seleciona qual usar (Eq. 20-23). Equação de bezerra com vaca lactante é possível mas "não recomendado" [p.473].
- Estresse por calor (T > UCT) reduz a IMS, mas **só está refletido nas equações de bezerras**. Estímulo da IMS abaixo da LCT **não** está em nenhuma equação [p.473].

**Eq. 20-2** [p.473] — Temperatura mínima crítica (LCT, °C):
```
LCT = 15   se An_Age < 21 d
LCT = 5    se An_Age >= 21 d
```
**Eq. 20-3** [p.473] — Temperatura máxima crítica:
```
UCT (°C) = 25      (igual para todas as idades)
```
Zona termoneutra (TMZ) = UCT − LCT. LCT e TMZ não entram em outra equação do intervalo.

### 4.3 IMS de bezerras [pp.473-474]
IMS total = líquido (leite/sucedâneo; vem de Trg_DMIn e proporções) + concentrado inicial (predito) + forragem.

**Eq. 20-4** [p.473] — Dt_DMIn_Calf_StrtFd (kg MS/d de concentrado inicial). Conferida em recorte 300 dpi (imagem de baixa resolução); estrutura confirmada pela Eq. 10-1/10-2 do cap. 10 (p.221 do livro), que traz os mesmos coeficientes em g/d com mais casas decimais.
```
Se Env_Temp < UCT + 10   (isto é, < 35 °C):
  Dt_DMIn_Calf_StrtFd = ( 14.73*An_BW + 18.90*Dt_MEIn_Calf_LiqFd
                          + 73.3*(An_Age_DryFdStart/7)
                          + 13.50*(An_Age_DryFdStart/7)^2
                          - 29.61*(An_Age_DryFdStart/7)*Dt_MEIn_Calf_LiqFd
                          - 652.5 ) / 1000

Se Env_Temp >= UCT + 10:
  Dt_DMIn_Calf_StrtFd = ( 600.1 * [ 1 + 14864 * e^( -1.553 * (An_Age_DryFdStart/7) ) ]^(-1)
                          + 9.95*An_BW - 130.4*Dt_MEIn_Calf_LiqFd ) / 1000
```
- An_BW kg; An_Age_DryFdStart = idade (dias) em que o concentrado inicial é oferecido (entrada 32); /7 converte em semanas; Dt_MEIn_Calf_LiqFd = ME ingerida do alimento líquido, Mcal/d (Eq. 20-5); resultado kg/d (÷1000 de g/d). Texto cita também o ganho de PC alvo `Trg_BWgain` como fator, mas **ele não aparece na equação** impressa.
- Cap. 10 (g/d): `-652.525 + 14.734*PC + 18.896*EMIDL + 73.303*Tp + 13.496*Tp^2 - 29.614*Tp*EMIDL` (clima temperado) e `600.053*(1 + 14863.651*exp(-1.553*Tp))^-1 + 9.951*PC - 130.434*EMIDL` (subtropical, T > 35 °C). Tp em semanas. Cap. 10: RMSEP 262 e 222 g/d.
- A quebra de linha da imagem do cap. 20 sugere "(14.73×BW + 18.90) × MEIn" mas isso contradiz o cap. 10; adotado o cap. 10. ⚠

**Eq. 20-5** [p.473] — ME ingerida do alimento líquido (91% da energia bruta):
```
Dt_MEIn_Calf_LiqFd (Mcal/d) = SOMA_{f=1}^{N_f_Liq} ( Fd_DMInp_f_Liq * Trg_Dt_DMIn * Fd_GE_f * 0.91 )
```
- Fd_DMInp_f_Liq = proporção da MS de cada alimento líquido (usada sem /100 aqui: kg/kg; ver ⚠); Trg_Dt_DMIn kg/d; Fd_GE_f Mcal/kg (Eq. 20-6); 0.91 = ME/GE.

**Eq. 20-6** [p.473] — Energia bruta do alimento líquido:
```
Fd_GE_f (Mcal/kg) = [ (100 - Fd_Ash - Fd_FA - Fd_CP)*4.0 + Fd_FA*9.4 + Fd_CP*5.65 ] / 100
```
- Fd_Ash, Fd_FA, Fd_CP em % MS. Entalpias: 4.0 Mcal/kg p/ MO restante, 9.4 AG, 5.65 PB. Livro nota: lactose 3.95 e glicerol 4.3 Mcal/kg não são distinguidos (erro mínimo) [p.473].

**Eq. 20-7** [p.474] — IMS total de bezerra:
```
Dt_DMIn_Calf (kg/d) = Dt_DMIn_LiqFd + Dt_DMIn_StrtFd + Dt_DMIn_ForFd
```
**Eq. 20-8** [p.474]:
```
Dt_DMIn_Calf_LiqFd (kg/d) = SOMA_{f=1}^{N_f_Liq} ( Fd_DMInp_f_Liq * Trg_Dt_DMIn )
```
**Eq. 20-9** [p.474]:
```
Dt_DMIn_Calf_ForFd (kg/d) = SOMA_{f=1}^{N_f_For} ( Fd_DMInp_f_For * Trg_Dt_DMIn )
```
- Como o concentrado inicial é estimado pela Eq. 20-4 (não por Trg_DMIn × Fd_DMInp), as proporções finais da dieta **não coincidem** exatamente com as do usuário. Se o modelo usa `Trg_Dt_DMIn`, a ingestão do concentrado inicial é ajustada como a **diferença** entre o An_DMIn especificado e o líquido [p.474]. (Livro usa os nomes Dt_DMIn_LiqFd/StrtFd/ForFd na 20-7 e Dt_DMIn_Calf_LiqFd/ForFd nas 20-8/9.)

### 4.4 IMS de novilhas [p.474-475]
Dois conjuntos: (i) só fatores do animal, (ii) animal + dieta; mais variantes por raça (Holandesa, Holandês×Jersey — só comparação; as equações entre raças são as recomendadas) e para pré-parto, para animal individual (Ind) ou lote (Pen).

**Eq. 20-10** [p.474] — Novilha até 3 semanas pré-parto, só animal (Hoffman 2008 modificada; = Eq. 2-3 do cap. 2):
```
Dt_DMIn_Heif1_FarOff (kg/d) = 0.022 * An_BWmature * ( 1 - e^( -1.54*(An_BW/An_BWmature) ) )
```
**Eq. 20-11** [p.474] — Animal + dieta (= Eq. 2-4 do cap. 2):
```
Dt_DMIn_Heif2_FarOff (kg/d) = [ 0.0226 * An_BWmature * ( 1 - e^( -1.47*(An_BW/An_BWmature) ) ) ]
                              - [ 0.082 * ( Dt_NDF - { 23.1 + 56*(An_BW/An_BWmature)
                                                       - 30.6*(An_BW/An_BWmature)^2 } ) ]
```
- Dt_NDF em % da MS; PC em kg. Novilhas no fim da gestação (≤ 60 d do parto) também podem usar as equações de vacas secas/transição [p.474].

### 4.5 IMS no fim da gestação (pré-parto) [pp.474-475]
**Eq. 20-12** [p.474] — individual, % do PC (cap. 12):
```
Dt_DMIn_BW_LateGest_ind (% BW) = 1.47 - fDMIn_NDF * An_Wk_PrePart - 0.035 * An_Wk_PrePart^2
```
**Eq. 20-13** [p.474]:
```
fDMIn_NDF (% PC/semana) = 0.365 - 0.0028 * Dt_NDF          (Dt_NDF em % MS)
```
**Eq. 20-14** [p.474]:
```
An_Wk_PrePart (semanas, negativo) = ( An_Day_Gest - An_Day_GestLength ) / 7
```
- (An_Day_Gest = entrada 13; An_Day_GestLength = entrada 10). **Limites: An_Wk_PrePart ∈ [−3, 0]; Dt_NDF ∈ [30, 55] %** [p.474].

**Eq. 20-15** [p.475] — duração a integrar para um grupo (estado estacionário; 2× a média):
```
An_Wk_PrePartDurat = An_Wk_PrePart * 2
```
**Eq. 20-16** [p.475] — IMS do grupo (integral de An_Wk_PrePartDurat até 0), % do PC:
```
Dt_DMIn_BW_PrePart_Pen (% BW) =
   ( 1.47*An_Wk_PrePartDurat
     - (fDMIn_NDF/2) * An_Wk_PrePartDurat^2
     - (0.035/3)     * An_Wk_PrePartDurat^3 ) / An_Wk_PrePartDurat
```
- A função é não linear no tempo; usar a média do grupo na Eq. 20-12 enviesa; por isso integra-se [p.474-475]. Conferida em recorte 300 dpi.

**Eq. 20-17a/b** [p.475] — Novilhas, 3 sem pré-parto → parto: redução de 12% (Hayirli et al. 2003 era multíparas):
```
Dt_DMIn_Heif_Close_Ind (kg/d) = ( Dt_DMIn_BW_PrePart_Ind / 100 ) * An_BW * 0.88      (20-17a)
Dt_DMIn_Heif_Close_Pen (kg/d) = ( Dt_DMIn_BW_PrePart_Pen / 100 ) * An_BW * 0.88      (20-17b)
```
- O modelo calcula todas; "a Eq. 20-17 é usada para ajustes no fim da gestação pelo software" [p.475]. (Os nomes `..._PrePart_Ind` e `..._LateGest_ind` da Eq. 20-12 se referem à mesma quantidade; ver ⚠.)

**Eq. 20-18** [p.475] — Transição entre período distante e pré-parto (teste de mínimo; ponto exato de troca não especificado):
```
Dt_DMIn_Heif (kg/d) =
   Dt_DMIn_Heif_FarOff                                   se An_Wk_PrePart < -3
   min( Dt_DMIn_Heif1_Close , Dt_DMIn_Heif_FarOff )      se An_Wk_PrePart >= -3
```
(O livro imprime `Dt_DMIn_Heif1_Close` na linha do mínimo — provável referência à 20-17; ⚠.) `Dt_DMIn_Heif_FarOff` aqui = Heif1 ou Heif2 conforme escolhido.

### 4.6 IMS de vacas não lactantes [p.475]
**Eq. 20-19** [p.475] (individual) e **Eq. 20-20** [p.475] (grupo), baseadas no cap. 12:
```
Dt_DMIn_Dry_Ind (kg/d) = ( Dt_DMIn_BW_PrePart_Ind / 100 ) * An_BW      (20-19)
Dt_DMIn_Dry_Pen (kg/d) = ( Dt_DMIn_BW_PrePart_Pen / 100 ) * An_BW      (20-20)
```
- A 20-19 dá IMS constante para An_Wk_PrePart < −3 (por causa do limite); a 20-20 se aproxima de uma assíntota mais longe do parto. Multíparas.

### 4.7 IMS de vacas em lactação [pp.475-476]
**Eq. 20-21** [p.475] — só fatores do animal (= Eq. 2-1 do cap. 2). Conferida em recorte 300 dpi:
```
Dt_DMIn_Lact1 (kg/d) = ( 3.7 + 5.7*(An_Parity - 1) + 0.305*Milk_NEuse_Target + 0.022*An_BW
                         + (-0.689 - 1.87*(An_Parity - 1))*An_BCS )
                       * ( 1 - (0.212 + 0.136*(An_Parity - 1)) * e^( -0.053*An_DayLact ) )
```
- An_Parity: valor real de 1 a 2 (1 primíparas, 2 multíparas; para grupo = média). `Milk_NEuse_Target` (Mcal/d) = EL da produção de leite alvo (vem de `Trg_MilkProd` e composição; o livro cita "Equação 20-217" = erro de impressão; equação está na Parte B, fora deste intervalo). An_BW kg; An_BCS 1-5; An_DayLact dias.
- Parênteses impressos no livro de forma ambígua; leitura acima = a estruturalmente coerente e idêntica à do cap. 2 (⚠ menor).
- **Grupos com animais < 90 DEL**: a equação deve ser **integrada** no tempo do grupo (platô aos 90 DEL); para > 45 DEL o erro de usar o DEL médio é muito pequeno; de 0 a 45 DEL usar o DEL médio **superestima** a IMS do grupo [p.476].

**Eq. 20-22** [p.476] — animal + dieta (Allen et al. 2019; = Eq. 2-2 do cap. 2). Conferida em recorte 300 dpi; a diagramação do livro quebra linhas e perde parênteses; leitura estrutural pelo cap. 2:
```
Dt_DMIn_Lact2 (kg/d) = 12.0 - 0.107*Dt_fNDF + 8.17*(Dt_ADF/Dt_NDF)
                       + 0.0253*ForNDF48 - 0.328*(Dt_ADF/Dt_NDF - 0.602)*(ForNDF48 - 48.3)
                       + 0.225*Milk_Prod_Target + 0.00390*(ForNDF48 - 48.3)*(Milk_Prod_Target - 33.1)
```
- `Dt_fNDF` = FDN de forragem da dieta (% MS; equivale a Dt_ForNDF; ⚠ nome diferente); `ForNDF48` = digestibilidade in vitro 48 h da FDN de forragem, % (no cap. 2 é "DFDNf"; ⚠ não definido neste capítulo); Dt_ADF/Dt_NDF razão (fração); Milk_Prod_Target kg/d. Válida para vacas > 60 DEL (sem termo para o início de lactação) [p.476].

### 4.8 Seleção da IMS e razões
**Eq. 20-23** [p.476] — escolha por An_DMIeqn (tabela impressa, numeração 0 a 10):
```
An_DMIeqn:  0 -> Dt_DMIn_Target          1 -> Dt_DMIn_Calf
            2 -> Dt_DMIn_Heif1           3 -> Dt_DMIn_Heif2
            4 -> Dt_DMIn_BWLateGest_ind  5 -> Dt_DMIn_BWLateGest_pen
            6 -> Dt_DMIn_Dry             7 -> Dt_DMIn_BWPrePart_ind
            8 -> Dt_DMIn_BWPrePart_Pen   9 -> Dt_DMIn_Lact1
           10 -> Dt_DMIn_Lact2           => Dt_DMIn (kg/d)
```
- A escolha do estado fisiológico restringe a lista de equações oferecidas (ex.: Heifer → ingestão do usuário, Eq. 20-10 ou 20-11) [p.476]. Texto p.473 diz "oito equações"; a tabela tem 10 + a do usuário (⚠).

**Eq. 20-24** [p.476]: `Dt_DMIn_BW (kg/kg BW) = Dt_DMIn / An_BW`
**Eq. 20-25** [p.476]: `Dt_DMIn_MBW (kg/kg BW^0.75) = Dt_DMIn / An_BW^0.75`  (An_MBW = An_BW^0.75)


### 4.9 Ingestão e composição por alimento e dieta [pp.476-479]

**Eq. 20-26** [p.476]:
```
Fd_DMIn_f (kg/d) = Fd_DMInp_f * Dt_DMIn
```
Texto: o usuário especifica a proporção na MS (kg/kg); a entrada 37 diz "porcentagem da MS" e a Eq. 20-28 divide por 100 (⚠ inconsistência de escala; Eqs. 20-5, 20-8, 20-9, 20-26 usam sem /100).

**Eq. 20-27a** [p.477] — ingestão em matéria natural (AF = as fed):
```
Fd_AFIn_f (kg/d) = Fd_DMIn_f / ( Fd_DM_f / 100 )
```
**Eq. 20-27b** [p.477] — proporção em matéria natural:
```
Fd_AFInp_f (kg/kg) = Fd_AFIn_f / SOMA_{f=1}^{N_f} Fd_AFIn_f
```
- Fd_DM_f em % (matéria natural).

**Categorias de alimento** (Tabela 20-7, p.477) e definições: forragem **fresca** = < 71% de MS; forragem **seca** = ≥ 71% de MS [p.477]. As categorias são convertidas em porcentagens dietéticas (100 se pertence, 0 se não) para obter a proporção de cada categoria como variável contínua.

**Eq. 20-28** [p.477] — IMS por categoria c:
```
Dt_DMIn_c = SOMA_{f=1}^{N_f} ( Dt_DMIn * (Fd_DMInp_f/100) * (Fd_Type_f,c/100) )
```
- Fd_Type_f,c = 100 se o ingrediente f está na categoria c, 0 caso contrário.

**Eq. 20-29** [p.477] — FDN de forragem do alimento (% MS):
```
Fd_ForNDF_f = ( 1 - Fd_Conc_f/100 ) * Fd_NDF_f
```
(Fd_Conc_f = indicador 0/100 de "concentrado"; tudo que não é concentrado conta como forragem nesta fórmula; ⚠.)

**Eq. 20-30** [p.477]: `Fd_NDFnf_f (% MS) = Fd_NDF_f - Fd_NDFIP_f`   (o livro não define as siglas `NDFnf` nem `NDFIP`; pelo nome, NDFIP = PB insolúvel em FDN e NDFnf = FDN menos NDFIP; interpretação, não afirmada no texto ⚠)

**Eq. 20-31** [p.477]: `Fd_CPA_f (% MS) = Fd_CP_f * Fd_CPA_CP_f / 100`
**Eq. 20-32** [p.477]: `Fd_CPB_f (% MS) = Fd_CP_f * Fd_CPB_CP_f / 100`
**Eq. 20-33** [p.477]: `Fd_CPC_f (% MS) = Fd_CP_f * Fd_CPC_CP_f / 100`
**Eq. 20-34** [p.477]: `Fd_NPNCP_f (% MS) = Fd_CP_f * Fd_NPN_CP_f / 100`
**Eq. 20-35** [p.477]: `Fd_NPN_f (% MS) = Fd_NPNCP_f / 6.25`
**Eq. 20-36** [p.478]: `Fd_NPNDM_f (% MS) = Fd_NPNCP_f / 2.81`
**Eq. 20-37** [p.478]: `Fd_TP_f (% MS) = Fd_CP_f - Fd_NPNCP_f`
**Eq. 20-38** [p.478]: `Fd_N_f (% MS) = Fd_CP_f / 6.25`
- Fd_CPA_CP, Fd_CPB_CP, Fd_CPC_CP, Fd_NPN_CP = % da PB (biblioteca). 6.25 g PB/g N; 2.81 = fator PB equivalente por MS de fonte NPN (ex.: ureia, 281% PB).

**Eq. 20-39** [p.478] — fator de hidratação dos AG (g/g):
```
Fd_fHydr_FA_f = 1          se Fd_Category = "FA Supplement"
Fd_fHydr_FA_f = 1/1.06     para todas as outras categorias
```
(AG livres já hidratados não precisam de correção; AG em triglicerídeos são hidratados ao serem clivados. Os AG são entrada do modelo, não triglicerídeos.)

**Eq. 20-40a–d** [p.478] — grupos de AG ingeridos (kg/d):
```
Dt_UFAIn   = Dt_C16.1In + Dt_C18.1tIn + Dt_C18.1cIn + Dt_C18.2In + Dt_C18.3In       (20-40a)
Dt_MUFAIn  = Dt_C16.1In + Dt_C18.1tIn + Dt_C18.1cIn                                  (20-40b)
Dt_PUFAIn  = Dt_C18.2In + Dt_C18.3In                                                  (20-40c)
Dt_SatFAIn = Dt_FAIn - Dt_UFAIn                                                       (20-40d)
```
**Eq. 20-41** [p.478] — MO residual do alimento (% MS):
```
Fd_rOM_f = 100 - Fd_Ash_f - Fd_NDF_f - Fd_St_f - (Fd_FA_f * Fd_fHydr_FA_f) - Fd_TP_f - Fd_NPNDM_f
```
(rOM = MO residual; nos outros capítulos aparece como ROM. rOM = sobra após subtrair cinzas, FDN, amido, AG, proteína verdadeira e NPN da MS.)

**Eq. 20-42** [p.478] — Carboidrato não fibroso (CNF; "para propósitos históricos"):
```
Fd_NFC_f = 100 - Fd_Ash_f - Fd_NDF_f - Fd_TP_f - Fd_NPNDM_f - Fd_FA_f * Fd_fHydr_FA_f
```
**Eq. 20-43** [p.478] — Ingestão de nutriente (Nut(i)) do alimento:
```
Fd_Nut(i)In_f (kg/d) = ( Fd_Nut(i)_f / 100 ) * Fd_DMIn_f
```
(Forragem e concentrado: mesma fórmula.)
**Eq. 20-44** [p.478] — nutrientes expressos como fração do nutriente original (FDN de forragem, frações da PB, AA, AG):
```
Fd_NutFrac(i)In_f (% de Fd_Nut) = Fd_Nut(i)In_f * Fd_NutFrac(i)_f / 100
```
**Eq. 20-45** [p.479] — soma na dieta (n = nº de ingredientes):
```
Dt_Nut(i)In (kg/d) = SOMA_{f=1}^{n} Fd_Nut(i)In_f
```
**Eq. 20-46** [p.479] — concentração na dieta:
```
Dt_Nut(i) (% MS) = ( Dt_Nut(i)In / Dt_DMIn ) * 100
```
(Mesmo cálculo para concentrados e forragem da dieta. Vitaminas e minerais: ajuste estequiométrico às unidades da Tab. 20-6 [o livro imprime "Tabela 20-2" na p.479, provável erro de numeração do livro; unidades de minerais/vitaminas estão na Tab. 20-6; (anotado na verificação)], fórmula não dada.)

**Eq. 20-47** [p.479] — Ingestão de AA (g/d) do alimento:
```
Fd_AAt(a)In_f (g/d) = ( Fd_AAt(a)_CP_f / 100 ) * ( Fd_CP_f / 100 ) * Fd_DMIn_f * 1000
```
**Eq. 20-48** [p.479] — AA "verdadeiro" (corrigido pela recuperação em hidrólise ácida):
```
Fd_AAt(a)_CP_f (% PB) = Fd_AA(a)_CP_f / RecAA(a)
```
- a = cada um dos 10 AAE; Fd_AA(a)_CP = valor da biblioteca (g/100 g PB, observado); RecAA(a) = Tabela 20-8.

**Eq. 20-49** [p.479]: `Dt_AAt(a)In (g/d) = SOMA_{f=1}^{n} Fd_AAt(a)In_f`

### Tabela 20-7 — Categorias de ingredientes [p.477] (conferida a 400 dpi)
| Categoria (como impressa na tradução) | Descrição |
|---|---|
| Aditivo | Compostos que não fornecem nutrientes conhecidos |
| Proteína Animal | Fonte de proteína animal |
| Sub-produto/outro | Subproduto do processamento de ingredientes ou outros ingredientes não categorizados |
| Alimento líquido para bezerras | Alimento líquido para bezerra, sucedâneo lácteo ou leite |
| Alimento líquido para bezerras | Leite e sucedâneos lácteos alimentados na forma líquida |
| Fonte energética | Grãos com alto amido e baixa proteína |
| Suplementos de gordura | Suplementos de AG livres |
| Suplementos de gordura | Gordura suplementar como triglicerídeos |
| Forragens com grãos | Milho e forragens de planta inteira com grãos pequenos |
| Gramíneas e leguminosas forrageiras | Gramíneas ou leguminosas forrageiras |
| Pastagem | Pastejo (necessário para estimar ingestão em vacas de pastagem) |
| Proteína Vegetal | Fonte de proteína vegetal |
| Açúcar/Álcool | Mono e dissacarídeos e glicerol |
| Vitaminas/Minerais | Vitaminas e minerais |
Obs.: os nomes "Alimento líquido para bezerras" e "Suplementos de gordura" aparecem DUAS vezes (duas linhas diferentes no original; a tradução repetiu o rótulo; na Eq. 20-39 só "FA Supplement" tem valor 1, correspondente aos "AG livres"). ⚠ Os rótulos originais em inglês dessas linhas não estão impressos na tradução. O livro avisa: "usuários devem escolher a categoria correta".

### Tabela 20-8 — Recuperação fracional (RecAA) e fator de hidratação [p.479] (conferida a 300 dpi)
RecAA = g observado / g verdadeiro (hidrólise ácida 24 h); Hidratação = g AA anidro / g AA hidratado.
| Aminoácido | Recuperação | Hidratação |
|---|---|---|
| Arginina | 0.943 | 0.8967 |
| Histidina | 0.932 | 0.884 |
| Isoleucina | 0.893 | 0.8628 |
| Leucina | 0.939 | 0.8628 |
| Lisina | 0.938 | 0.8769 |
| Metionina | 0.952 | 0.8794 |
| Fenilalanina | 0.943 | 0.891 |
| Treonina | 0.937 | 0.849 |
| Triptofano | 0.943 | 0.9118 |
| Valina | 0.907 | 0.8464 |
Texto [p.479]: a soma de todos os AA relatados (corrigidos p/ recuperação) seria ~115% da massa de proteína, a diferença sendo a água adicionada na hidrólise. O comitê **calcula os fluxos de AA na forma hidratada**, para casar com análises de AA de proteína hidrolisada corrigidas para recuperação; o mesmo vale para exportação de AA no leite — **deve-se corrigir a hidratação ao usar AA absorvidos para síntese de proteínas**. Neste intervalo só `RecAA` entra em equações (20-48, 20-87); o fator de hidratação é usado na Parte B.

### 4.10 Infusões [pp.479-480]
Infusões entram como `Inf_Xxx`; total do animal `An_` = dieta + infusão; locais: rúmen, abomaso, duodeno, sangue (padrão 0).
**Eq. 20-50** [p.480]: `An_XxxIn (kg/d) = Dt_XxxIn + Inf_XxxIn`
**Eq. 20-51** [p.480]: `An_DigXxxIn (kg/d) = Dt_DigXxxIn + Inf_DigXxxIn`
(Sem documentação adicional: "variáveis autoexplicativas".)

### 4.11 Digestão ruminal de FDN e amido [p.480] (cap. 6, Eqs. 6-4a/b)
Todas as concentrações abaixo são da dieta total (dieta + infusão ruminal), % da MS; `Dt_ForWet` e `Dt_ForNDF` em % da MS.

**Eq. 20-52** [p.480] — Rum_dcNDF (% da FDN). Conferida em recorte 300 dpi:
```
Rum_dcNDF (%) = -31.9
  + 0.721 * ( (Dt_NDFIn + Inf_NDFIn[Rum]) / (Dt_DMIn + Inf_DMIn[Rum]) * 100 )
  - 0.247 * ( (Dt_StIn  + Inf_StIn[Rum])  / (Dt_DMIn + Inf_DMIn[Rum]) * 100 )
  + 6.63  * ( (Dt_CPIn  + Inf_CPIn[Rum])  / (Dt_DMIn + Inf_DMIn[Rum]) * 100 )
  - 0.211 * ( (Dt_CPIn  + Inf_CPIn[Rum])  / (Dt_DMIn + Inf_DMIn[Rum]) )^2
  - 0.387 * [ ( (Dt_ADFIn + Inf_ADFIn[Rum]) / (Dt_DMIn + Inf_DMIn[Rum]) * 100 )
            / ( (Dt_NDFIn + Inf_NDFIn[Rum]) / (Dt_DMIn + Inf_DMIn[Rum]) * 100 ) ] * 100
  - 0.121 * Dt_ForWet
  + 1.51  * ( Dt_DMIn + Inf_DMIn[Rum] )
```
- ATENÇÃO (conferido na imagem): no termo quadrático da PB, o livro imprime a razão **sem "×100"**: `-0.211 × (CPIn/DMIn)^2` com a razão como FRAÇÃO (ao passo que o termo linear usa %). No cap. 6 (Eq. 6-4a) a PB entra em % nos dois termos (CP^2 com CP em %). Conferir com a fonte do código R; ⚠.
- O termo da FDA é `0.387 × (FDA%/FDN%) × 100` = 38.7 × (FDA/FDN) (cap. 6 usa 38.7).
- Dt_DMIn kg/d; Inf_..[Rum] = infusão ruminal.

**Eq. 20-53** [p.480] — Rum_dcSt (% do amido). Conferida em recorte 300 dpi:
```
Rum_dcSt (%) = 70.6 - 1.45*( Dt_DMIn + Inf_DMIn[Rum] )
  + 0.424 * Dt_ForNDF
  + 1.39  * ( (Dt_St + Inf_StIn[Rum]) / (Dt_DMIn + Inf_DMIn[Rum]) * 100 )
  - 0.0219 * ( (Dt_St + Inf_StIn[Rum]) / (Dt_DMIn + Inf_DMIn[Rum]) * 100 )^2
  - 0.154 * Dt_ForWet
```
- O numerador impresso é `Dt_St + Inf_StIn_Rum` (mistura "Dt_St" concentração com "Inf_StIn" ingestão; muito provavelmente deveria ser `Dt_StIn`; ⚠). O cap. 6 imprime 71.2 como intercepto (Eq. 6-4b); este capítulo imprime **70.6** (⚠ divergência; usar 70.6 = código R segundo o texto, mas conferir).
- **Limites**: ambos coeficientes de digestão limitados a **[0, 100]**; valores médios de **37.6 % (FDN) e 65.6 % (amido)** do nutriente original são adotados "se este estiver faltando" [p.480] (leitura literal; ⚠ ambígua).

**Eq. 20-54** [p.480]: `Rum_DigNDFIn (kg/d) = Rum_dcNDF/100 * ( Dt_NDFIn + Inf_NDFIn[Rum] )`
**Eq. 20-55** [p.480]: `Rum_DigStIn (kg/d) = Rum_dcSt/100 * ( Dt_StIn + Inf_StIn[Rum] )`
**Eq. 20-56** [p.480] (passagem de FDN por diferença): `Du_NDFPas (kg/d) = Dt_NDFIn + Inf_NDFIn[Rum] - Rum_DigNDFIn`
**Eq. 20-57** [p.480]: `Du_StPas (kg/d) = Dt_StIn + Inf_StIn[Rum] - Rum_DigStIn`
- Dietas só com gramíneas imaturas dão passagem de amido ligeiramente negativa → **restrita e fixada em 0** [p.480].

### 4.12 PDR, PNDR e AA da PNDR [pp.480-482] (cap. 6; taxas de passagem estáticas)
**Eq. 20-58** [p.480] — PNDR da fração A:
```
Fd_RUPAIn_f (kg/d) = ( Fd_CPAIn_f - Fd_NPNCPIn_f ) * fCPAdu
```
**Eq. 20-59** [p.480] — PNDR da fração B:
```
Fd_RUPBIn_f (kg/d) = Fd_CPBIn_f * ( 1 - Rum_dcCPB_f/100 )
```
**Eq. 20-60** [p.481] — degradação ruminal da fração B (%). Conferida em recorte 300 dpi:
```
Rum_dcCPB_f (%) = 100 - [ Fd_For_f  * Kp_For  / ( Fd_KdRUP_f + Kp_For )
                         + Fd_Conc_f * Kp_Conc / ( Fd_KdRUP_f + Kp_Conc ) ]
```
(Fd_For_f e Fd_Conc_f = indicadores 0/100 da classe do alimento; se o alimento não é nem forragem nem concentrado, ambos zeram e Rum_dcCPB = 100 → PNDR da fração B = 0; ⚠ não discutido.)
**Eq. 20-61** [p.481] — PNDR total do alimento:
```
Fd_RUPIn_f (kg/d) = Fd_RUPAIn_f + Fd_RUPBIn_f + Fd_CPCIn_f + ( IntRUP / refCPIn ) * Fd_CPIn_f
```
Constantes [p.481]:
| Símbolo | Valor | Unidade | Significado |
|---|---|---|---|
| Kp_Conc | 5.28 | %/h | taxa de passagem da proteína em concentrados |
| Kp_For | 4.87 | %/h | taxa de passagem da proteína em forragens |
| fCPAdu | 0.064 | kg/kg da fração A da PB | escape fracional da fração A do rúmen |
| IntRUP | −0.086 | kg/d (nível de dieta) | intercepto da regressão de fluxo ruminal (cap. 6) |
| refCPIn | 3.39 | kg/d | ingestão média de PB do banco de fluxo ruminal |
O intercepto é distribuído aos alimentos dividindo por refCPIn e multiplicando pela PB ingerida de cada ingrediente (erro < 1% vs. nível dieta). Fd_KdRUP_f: taxa de degradação da fração B da biblioteca (não definida neste intervalo).

**Eq. 20-62** [p.481] — AA da PNDR:
```
Fd_AARUP(a)In_f (g/d) = ( Fd_AAt(a)_CP_f / 100 ) * Fd_RUPIn_f * 1000
```
**Eq. 20-63** [p.481]: `Dt_RUPIn (kg/d) = SOMA_{f=1}^{n} Fd_RUPIn_f`
**Eq. 20-64** [p.481]: `An_RUPIn (kg/d) = Dt_RUPIn + InfRum_RUPIn`
**Eq. 20-65** [p.481]: `An_RUP_CP (% da PB) = An_RUPIn / ( Dt_CPIn + InfRum_CPIn ) * 100`
**Eq. 20-66** [p.481]: `Dt_RDPIn (kg/d) = Dt_CPIn - Dt_RUPIn`   (PDR por diferença)
**Eq. 20-67** [p.481]: `Dt_RDP (% da MS) = Dt_RDPIn / Dt_DMIn * 100`
**Eq. 20-68** [p.481]: `Dt_RDP (% da PB) = Dt_RDP / Dt_CP * 100`   (como impresso; numerador é a concentração em % MS)
**Eq. 20-69** [p.481]: `An_RDPIn (kg/d) = Dt_RDPIn + InfRum_RDPIn`
**Eq. 20-70** [p.481]: `An_RDP_CP (% da PB) = An_RDPIn / ( Dt_CPIn + InfRum_CPIn ) * 100`
**Eq. 20-71** [p.481]: `Dt_AARUP(a)In (g/d) = SOMA_{f=1}^{n} Fd_AARUP(a)In_f`
**Eq. 20-72** [p.481]: `An_AARUP(a)In (g/d) = Dt_AARUP(a)In + InfRum_AARUP(a)In`
**Eq. 20-73** [p.482] — fração do AA do alimento capturada na PNDR (apenas relatório):
```
AARUP(a)_AADt(a) (%) = Dt_AARUP(a)In / Dt_AA(a)In * 100
```
(O livro imprime `Dt_AA(a)In`, enquanto a 20-49 define `Dt_AAt(a)In`; ⚠ nomenclatura.)

### 4.13 Proteína microbiana ruminal [p.482] (cap. 6, Eq. 6-3)
**Eq. 20-74** [p.482] — N microbiano que sai do rúmen. Conferida em recorte 300 dpi:
```
Du_MiN_g (g/d) = MiN_Vm / ( 1 + MiN_Km_rdNDF / Rum_DigNDFIn + MiN_Km_rdSt / Rum_DigStIn )
```
**Eq. 20-75** [p.482]:
```
MiN_Vm (g/d) = MiN_Vm_Int + MiN_Vm_RDPSlp * An_RDPIn
```
| Constante | Valor |
|---|---|
| MiN_Vm_Int | 100.8 |
| MiN_Vm_RDPSlp | 81.56 |
| MiN_Km_rdNDF (impresso "MiN_Km_RDNDF") | 0.0939 |
| MiN_Km_rdSt (impresso "MiNKm_rdSt") | 0.0274 |
- Rum_DigNDFIn, Rum_DigStIn (kg/d) = Eqs. 20-54/20-55; An_RDPIn (kg/d) = Eq. 20-69. **O efeito da PDR foi limitado: não gera resposta adicional acima de 12% de PDR na dieta** [p.482] (isto é, An_RDPIn efetivo na 20-75 ≤ 12% da IMS; forma exata não impressa).
- O cap. 6 imprime estrutura multiplicativa `(1+B2/RDNDF)*(1+B3/RDS)` e B0=101, B1=82.6; o cap. 20 imprime estrutura **aditiva** e 100.8 / 81.56 (⚠ divergência cap. 6 × cap. 20).

**Eq. 20-76** [p.482]: `Du_MiCP (kg/d) = Du_MiN_g * 6.25 / 1000`
**Eq. 20-77** [p.482]: `Du_MiTP (kg/d) = Du_MiCP * 0.824`
- Coeficientes estequiométricos estáticos: 6.25 g PB/g N; 0.824 g PV/g PB. "A PB microbiana máxima foi definida baseada na ingestão de PDR" [p.482] (limite; sem equação impressa ⚠).
**Eq. 20-78** [p.482]: `Rum_RDPbal (kg/d) = An_RDPIn - Du_MiCP`
**Eq. 20-79** [p.482] — AA microbianos:
```
Du_AAMic(a) (g/d) = Du_MiTP * 1000 * AA(a)_MiTP / 100
```
(AA(a)_MiTP = g AA/100 g de proteína verdadeira microbiana, Tabela 6-2 do cap. 6; a = 10 AAE.)

### 4.14 Proteína endógena e fluxo total ruminal [pp.482-483]
**Eq. 20-80** [p.482]: `Du_EndCP (kg/d) = ( 96.1 + 7.54 * ( Dt_DMIn + InfRum_DMIn ) ) / 1000`
(≈ cap. 6: 15.4 + 1.21×DMI g N/d × 6.25. Endógena = custo de mantença, não é adição líquida ao aporte.)
**Eq. 20-81** [p.482]: `Du_AAEndCP(a) (g/d) = Du_EndCP * 1000 * AA(a)_DuEndCP / 100`   (composição: Tabela 6-5 do cap. 6)
**Eq. 20-82** [p.482]: `Du_NAN (g/d) = ( Du_MiCP + An_RUPIn + Du_EndCP ) / ( 6.25 * 1000 )`   (como impresso; ver ⚠ de unidade)
**Eq. 20-83** [p.483]: `Du_NANMN (g/d) = ( An_RUPIn + Du_EndCP ) / ( 6.25 * 1000 )`   (como impresso)
- Texto: o fluxo de amônia não está representado claramente; por diferença, ~5% da PDR passa e contém amônia, então Du_NANMN é mais provavelmente "N não microbiano"; é comparado com NANMN da literatura só para avaliação [p.483].
**Eq. 20-84** [p.483]: `Du_AA(a) (g/d) = Dt_AARUP(a)In + Inf_AARUP(a)In + Du_AAMic(a) + Du_AAEndP(a)`   (impresso `Du_AAEndP(a)`; é o Du_AAEndCP(a) da 20-81; ⚠)
**Eq. 20-85** [p.483]: `DuAA(a)_DtAA(a) (%) = Du_AA(a) / ( Dt_AA(a)In + Inf_AA(a)In ) * 100`
**Eq. 20-86** [p.483]: `Du_EAA (g/d) = Du_Arg + Du_His + Du_Ile + Du_Leu + Du_Lys + Du_Met + Du_Phe + Du_Thr + Du_Trp + Du_Val`
**Eq. 20-87** [p.483] — fluxo não corrigido (só comparação com literatura; "não possui outra função no modelo"):
```
Du_AA(a)_24h (g/d) = Du_AA(a) * RecAA(a)
```

### 4.15 Digestão e absorção de carboidratos no trato total [pp.483-484]

**Amido** (digestibilidade base por ingrediente, Tabela 3-1 do cap. 3, ajustada pelo nível de ingestão):
**Eq. 20-88** [p.483]: `Fd_DigSt_Base_f (% da MS) = Fd_St_f * Fd_dcSt_f / 100`
**Eq. 20-89** [p.483]: `Fd_DigStIn_Base_f (kg/d) = Fd_DigSt_Base_f / 100 * Fd_DMIn_f`
**Eq. 20-90** [p.483]: `Dt_DigStIn_Base (kg/d) = SOMA_{f=1}^{N_f} Fd_DigStIn_Base_f`
**Eq. 20-91** [p.483]: `TT_dcSt_Base (% do amido) = Dt_DigStIn_Base / Dt_StIn * 100`
**Eq. 20-92** [p.483] — ajuste pela IMS (centrado em 3.5% do PC):
```
TT_dcSt (% do amido) = TT_dcSt_Base - ( 1.0 * ( An_DMI_BW - 0.035 ) ) * 100
```
- **Limitado a 0 no extremo inferior** [p.483]. `An_DMI_BW` = IMS/PC (kg/kg; a 20-24 define Dt_DMI_BW; ⚠ prefixo An_ não definido). A cada +1 ponto percentual de IMS/PC acima de 3.5%, a digestibilidade cai 1 ponto percentual.
**Eq. 20-93** [p.483]: `Dt_DigStIn (kg/d) = Dt_StIn * TT_dcSt / 100`
**Eq. 20-94** [p.483]: `Dt_DigSt (% da MS) = Dt_DigStIn / Dt_DMIn * 100`
**Eq. 20-95** [p.484] — amido digestível total (com infusão). Conferida a 300 dpi:
```
An_DigStIn (kg/d) = Dt_DigStIn + Inf_StIn * Inf_ttdcSt / 100
```
(Inf_ttdcSt = digestibilidade do amido infundido no trato total, %; entrada do vetor de infusões.)
**Eq. 20-96** [p.484]: `An_dcSt (% do amido) = An_DigStIn / ( Dt_StIn + Inf_StIn ) * 100`
**Eq. 20-97** [p.484]: `An_DigSt (% da MS) = ( An_DigStIn / ( Dt_DMIn + Inf_RumDMIn + Inf_SIDMIn ) ) * 100`
**Eq. 20-98** [p.484]: `Fe_St (kg/d) = Dt_StIn + Inf_StIn - An_DigStIn`

**MO residual (rOM)**:
Digestibilidade **verdadeira** da rOM: `Dt_dcrOMt = 96.1 %` (fixa); excreção endógena fecal = 3.43% da Dt_DMIn (cap. 3) [p.484].
**Eq. 20-99** [p.484]: `Fd_DigrOMt_f (% da MS) = Fd_dcrOMt / 100 * Fd_rOM_f`   (Fd_dcrOMt = 96.1)
**Eq. 20-100** [p.484]: `Fe_rOMend (kg/d) = 0.034 * Dt_DMIn`   (texto: 3.43%; as Eqs. 20-100 e 20-101 usam 0.034 e 3.43; ⚠ 0.034 vs 0.0343)
**Eq. 20-101** [p.484]: `Fd_DigrOMa_f (% da MS) = Fd_DigrOMt_f - 3.43`   (aparente, por alimento)
**Eq. 20-102** [p.484]: `Fd_DigrOMaIn_f (kg/d) = Fd_DigrOMa_f / 100 * Fd_DMIn_f`
- Pode dar valores **negativos** para alimentos com rOM muito baixa (fontes minerais); a soma na dieta é confiável [p.484].
**Eq. 20-103** [p.484]: `Fd_DigrOMtIn_f (kg/d) = Fd_DigrOMt_f / 100 * Fd_DMIn_f`
**Eq. 20-104** [p.484]: `Dt_DigrOMtIn (kg/d) = SOMA_{f=1}^{N_f} Fd_DigrOMtIn_f`
**Eq. 20-105** [p.484]: `Dt_DigrOMaIn (kg/d) = Dt_DigrOMtIn - Fe_rOMend`
**Eq. 20-106** [p.484] — com infusões (conferida a 300 dpi):
```
An_DigrOMaIn (kg/d) = Dt_DigrOMaIn + ( Inf_GlcIn + Inf_AcetIn + Inf_PropIn + Inf_ButrIn ) * ( fRum + fSI )
```
(Glc = glicose, Acet = acetato, Prop = propionato, Butr = butirato infundidos; `fRum`, `fSI` = fatores de local de infusão (rúmen / intestino delgado), **não definidos** no texto; ⚠.)
**Eq. 20-107** [p.484]: `An_DigrOMa (% da MS) = ( An_DigrOMaIn / ( Dt_DMIn + InfRum_DMIn + InfSI_DMIn ) ) * 100`
**Eq. 20-108** [p.484]: `An_dcrOMa (% da rOM) = An_DigrOMaIn / ( Dt_rOMaIn + ( Inf_GlcIn + Inf_AcetIn + Inf_PropIn + Inf_ButrIn ) * ( fRum + fSI ) ) * 100`
**Eq. 20-109** [p.484]: `Fe_rOMout (kg/d) = An_rOMIn - An_DigrOMaIn`

### 4.16 Contexto: p.485 (continuação, NÃO detalhada; fora do intervalo)
A p.485 continua "Digestão de FDN no trato total": Eq. 20-110 (Fd_dcNDF_Lg, estimativa pela lignina: `0.75*(Fd_NDF-Fd_Lg)*(1-(Fd_Lg/Fd_NDF)^0.667)/Fd_NDF*100`), Eq. 20-111 (Fd_dcNDF_IV48 = 12 + 0.61*Fd_dcNDF_IV48h), Eq. 20-112 (seleção por Use_dcNDF_IV48: 0 lignina; 1 forragem IV48 / concentrado lignina; 2 todos IV48), Eqs. 20-113/114 (base na dieta), Eq. 20-115 (Dt_dcNDF com ajuste −1.1 por (DMI/BW−0.035) e −0.59 por (amido−0.26)), Eqs. 20-116 a 20-120 (Dt_DigNDFIn, An_DigNDFIn, Dt_DigNDF, An_DigNDF, Fe_NDF) e início de "Proteína" (Dt_idRUPIn). Esses itens ficam para o bloco ch20B (p.485 em diante); transcrição aqui NÃO foi conferida em detalhe.

---

## 5. Parâmetros e tabelas — resumo de localização
Tabelas 20-1 a 20-6 (dicionário): §2a. Tabela 20-7 (categorias) e 20-8 (RecAA/hidratação): §4.9. Constantes numéricas das equações estão em linha (ver cada equação); constantes agrupadas: Kp/fCPAdu/IntRUP/refCPIn (§4.12), MiN_* (§4.13), UCT=25 e LCT=15/5 (§4.2), 96.1% e 3.43% rOM (§4.15), 37.6/65.6% (§4.11).

## 6. Regras de decisão / restrições para o otimizador
- Limites de variáveis nas equações: `An_Wk_PrePart` ∈ [−3, 0] semanas; `Dt_NDF` ∈ [30, 55] % (apenas dentro de 20-12/20-13) [p.474]. `Rum_dcNDF`, `Rum_dcSt` ∈ [0, 100] [p.480]. `Du_StPas` ≥ 0 [p.480]. `TT_dcSt` ≥ 0 [p.483]. Efeito da PDR sobre MiN limitado a 12% de PDR na dieta [p.482]. PB microbiana máxima limitada pela ingestão de PDR [p.482].
- Validade das equações de IMS: Eq. 20-22 só para vacas > 60 DEL; Eq. 20-21 integrar para grupos < 90 DEL (erro pequeno > 45 DEL) [p.476]; Eq. 20-1 só vaca em lactação, vaca seca, novilha pós-desmame; bezerras e "Other" indefinidos [p.472]; Eq. 20-4 troca de ramo em Env_Temp ≥ 35 °C [p.473].
- Estado fisiológico limita as equações de IMS oferecidas (Eq. 20-23) [p.476]. Categoria de alimento correta é obrigatória para energia e outras variáveis [p.477].
- Nenhum mínimo/máximo nutricional de formulação (FDN mínimo etc.) neste intervalo; "não informado".

## 7. Lógica e fluxo (ordem de cálculo e dependências)
1. Entradas (§2b) + biblioteca de alimentos (§2c) + inclusão Fd_DMInp (e infusões, padrão 0).
2. **Água**: An_WaIn (20-1) ← Dt_DMIn (passo 3), Dt_DM, Dt_CP, Dt_Na, Dt_K (passo 4), Env_TempCurr.
3. **IMS**: escolher An_DMIeqn (20-23): 0 = Trg_Dt_DMIn (usuário); 1 = bezerra (20-4 a 20-9; usa Eq. 20-5/20-6 e Trg_Dt_DMIn); 2/3 = novilhas (20-10/20-11; 20-11 usa Dt_NDF do passo 4 → ciclo: IMS ↔ composição, resolver com a proporção Fd_DMInp, que independe da IMS); fim de gestação (20-12 a 20-18, 20-19/20-20; usam Dt_NDF, An_GestDay, An_GestLength); lactação (20-21 usa Milk_NEuse_Target da Parte B; 20-22 usa Dt_ForNDF, Dt_ADF/Dt_NDF, Milk_Prod_Target). Depois 20-24/20-25.
4. **Composição por alimento** (20-26 a 20-42): Fd_DMIn (20-26) → Fd_AFIn (20-27) → categorias (20-28) → frações de PB/NPN (20-31 a 20-38) → AG (20-39, 20-40) → Fd_rOM (20-41), NFC (20-42) → ingestões Fd_Nut(i)In (20-43/44) → somas Dt_ (20-45) → concentrações Dt_ (20-46) → AA (20-47 a 20-49). Para qualquer nutriente: An_ = Dt_ + Inf_ (20-50/51).
5. **Rúmen**: Rum_dcNDF (20-52), Rum_dcSt (20-53) ← Dt_ composição + infusão ruminal → Rum_DigNDFIn/StIn (20-54/55) → Du_NDFPas/StPas (20-56/57).
6. **PNDR/PDR**: Fd_RUPAIn (20-58) + Fd_RUPBIn (20-59 ← Rum_dcCPB 20-60) + Fd_CPCIn + intercepto → Fd_RUPIn (20-61) → AA da PNDR (20-62) → somas (20-63, 20-71) → An_ (20-64, 20-69, 20-72) → % (20-65 a 20-68, 20-70, 20-73). Dt_RDPIn = Dt_CPIn − Dt_RUPIn (20-66).
7. **Microbiana**: MiN_Vm (20-75 ← An_RDPIn) → Du_MiN_g (20-74 ← Rum_DigNDFIn, Rum_DigStIn) → Du_MiCP (20-76) → Du_MiTP (20-77) → Rum_RDPbal (20-78), AA microbianos (20-79).
8. **Endógena e fluxo ruminal**: Du_EndCP (20-80), AA (20-81), Du_NAN/NANMN (20-82/83), Du_AA(a) (20-84 ← 20-71/72, 20-79, 20-81), % (20-85), Du_EAA (20-86), 24h (20-87).
9. **Trato total**: amido (20-88 a 20-98 ← Fd_dcSt, An_DMI/BW), rOM (20-99 a 20-109), FDN (20-110 em diante, p.485), PNDR digerida e AA (p.485+; Parte B do bloco).
- Entradas vindas de outros capítulos: Eqs. 2-1 (=20-21), 2-2 (=20-22), 2-3/2-4 (=20-10/11), 10-1/10-2 (=20-4), 12-1/12-2 (=20-12, 20-17), 9-1/9-3 (=20-1), 6-3/6-4 (=20-74, 20-52/53), 6-2 (=20-80), Tab. 3-1 (Fd_dcSt), Tab. 6-2 (AA microbiano), Tab. 6-5 (AA endógeno), cap. 3 (rOM 96.1%/3.43%).

## 8. Limitações, incertezas e mudanças vs. NRC 2001
- O texto do capítulo foi escrito transcrevendo o código R; "caso haja diferenças... o código R é mais provável de estar correto" (verificado ao longo de 4 anos) [p.472].
- Estresse por calor só em IMS de bezerras; sem efeito de LCT em nenhuma equação [p.473].
- NANMN (20-83) não representa amônia claramente [p.483].
- Equação de ganho de frame/reserva e de predição de leite/proteína/gordura alternativas: "undefined future prediction equation" (entradas 20, 22); RUP_eqn não usada; An_AgeConcept1st e An_DIMConcept não usadas [pp.467, 472].
- Mudanças vs. NRC 2001: PDR/PNDR por dados in situ com taxas de passagem estáticas em vez do modelo de taxa de passagem anterior [p.480]; entradas de carboidratos e AG expandidas [p.467]; infusões acomodadas; AA calculados na forma hidratada [p.479].

## 9. Conceitos e evidências relevantes
- Equações de IMS de novilhas pré-parto já incorporam a redução de 12% em relação a multíparas [p.475].
- Soma de AA relatados após correção de recuperação ≈ 115% da proteína (água de hidrólise) [p.479].
- Digestibilidade verdadeira da rOM 96.1% com perda fecal endógena 3.43% da IMS [p.484].
- Excesso de IMS (> 3.5% PC) reduz digestibilidade do amido 1 ponto % por ponto de IMS/PC [p.483].

## 10. Dúvidas / riscos de OCR (⚠) — itens a conferir
1. ⚠ **Numeração de DMIn_eqn**: entrada 31 (pp.469-472) lista 1-11 (4-7 = novilhas pré-parto por raça, 8-9 = lactação, 10-11 = seca), mas a Eq. 20-23 (p.476) lista 0-10 com mapeamento diferente (4/5 = BWLateGest ind/pen, 6 = Dry, 7/8 = BWPrePart ind/pen, 9/10 = Lact1/Lact2). Texto diz "oito equações" (p.473). Resolver com código R.
2. ⚠ **Fd_DMInp**: entrada 37 = % da MS; Eqs. 20-5, 20-8, 20-9, 20-26 usam sem /100 (proporção kg/kg segundo o texto); 20-28 divide por 100.
3. ⚠ **Eq. 20-1**: unidade de Dt_Na/Dt_K (provavelmente % da MS → 0.023 e 0.039 = massas molares em kg/mol...) e posição do "×10" (impresso dentro do mesmo parêntese, aplicado ao termo do K). Cap. 9 define NaK em mEq/kg: dieta 0.4% Na e 1.3% K → 507.2 mEq/kg, o que corresponde a (Na/0.023 + K/0.039)×10 (cap. 9), diferente da leitura literal do cap. 20 (`Na/0.023 + (K/0.039)*10`). Provável erro de parênteses; usar a forma do cap. 9 (parênteses cobrindo ambos) até confirmar.
4. ⚠ **Eq. 20-4**: baixa resolução; estrutura confirmada pelo cap. 10 (coef. 14.734, 18.896, 73.303, 13.496, 29.614, 652.525; 600.053, 14863.651, 1.553, 9.951, 130.434). Trg_BWgain citado no texto mas ausente da equação. Quebra de linha ambígua "(14.73×BW+18.90)×MEIn".
5. ⚠ **Eq. 20-18**: impresso "Dt_DMIn_Heif1_Close" na linha do min (provável 20-17, Heif_Close).
6. ⚠ **Eq. 20-12 / 20-17 / 20-19**: nomes diferentes para a mesma quantidade (Dt_DMIn_BW_LateGest_ind vs Dt_DMIn_BW_PrePart_Ind); 20-15 dobra a média (−6 sem) mas o limite de −3 é aplicado a An_Wk_PrePart.
7. ⚠ **Eq. 20-21**: parênteses ambíguos (resolvido pelo cap. 2); referência "Equação 20-217" no texto p.476 é erro de impressão (EL do leite alvo, Parte B).
8. ⚠ **Eq. 20-22**: `Dt_fNDF` (= ForNDF da dieta?) e `ForNDF48` (= digest. IV 48 h da FDN de forragem?) não definidos neste capítulo; layout do livro perdeu parênteses (leitura pelo cap. 2).
9. ⚠ **Eq. 20-29**: usa Fd_Conc_f como indicador; todo alimento não concentrado conta como forragem.
10. ⚠ **Eq. 20-30**: NDFnf, NDFIP não definidos.
11. ⚠ **Tabela 20-7**: rótulos duplicados na tradução ("Alimento líquido para bezerras", "Suplementos de gordura").
12. ⚠ **Eq. 20-52**: termo da PB ao quadrado sem ×100 (fração), enquanto o termo linear usa %; cap. 6 usa %. **Eq. 20-53**: numerador "Dt_St + Inf_StIn_Rum" (provável Dt_StIn); intercepto 70.6 (cap. 6: 71.2). Limites 37.6/65.6 "se faltando" ambíguo. Definição de ForWet: <71% MS (p.477) vs. ">20% MS" no cap. 6.
13. ⚠ **Eq. 20-60**: Fd_KdRUP não definido neste intervalo; classes For/Conc só; alimentos fora de ambas dão Rum_dcCPB = 100.
14. ⚠ **Eqs. 20-74/75**: forma aditiva e constantes (100.8; 81.56) diferem do cap. 6 (101; 82.6; multiplicativa). Limite 12% PDR sem fórmula; "PB microbiana máxima = PDR" sem fórmula.
15. ⚠ **Eqs. 20-82 e 20-83**: dividem kg/d por (6.25×1000) mas rotuladas g/d; para g N/d o fator seria ×1000/6.25 (se as entradas estão em kg/d). Transcritas como impressas.
16. ⚠ **Eq. 20-73, 20-84**: nomes `Dt_AA(a)In` (vs `Dt_AAt(a)In`) e `Du_AAEndP(a)` (vs `Du_AAEndCP(a)`).
17. ⚠ **Eq. 20-92**: `An_DMI_BW` não definido (a 20-24 define Dt_DMI_BW).
18. ⚠ **Eq. 20-100**: 0.034 vs 3.43% (0.0343) usado em 20-101.
19. ⚠ **Eqs. 20-106 e 20-108**: fRum, fSI não definidos; `Dt_rOMaIn` na 20-108 (provável Dt_rOMIn).
20. ⚠ Leituras de OCR corrigidas pela imagem (símbolos): Tabela 20-1 em OCR trazia "Envy", "ci2", "Cl&.1c" etc. — corrigidas para Env, C12, C18.1c; Eq. 20-1 (OCR errou a posição de parênteses); Eq. 20-4, 20-52 etc. totalmente reconstruídas da imagem (corrigido pela imagem).

COBERTURA: páginas lidas 466–484 (completas, nas imagens e no OCR) + p.485 apenas como contexto. Todas as equações Eq. 20-1 a 20-109 (incluindo 20-17a/b, 20-27a/b, 20-40a–d) foram transcritas e conferidas contra a imagem; Tabelas 20-1 a 20-8 transcritas na íntegra. Ficaram de fora: equações 20-110 em diante (p.485+; resumidas só como contexto, sem conferência), e as fórmulas citadas mas não impressas neste intervalo (Milk_NEuse, ajuste estequiométrico de minerais/vitaminas, limite de 12% PDR, limite de PB microbiana). Itens ⚠: 20 grupos (ver §10).

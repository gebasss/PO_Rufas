# NASEM 2021 (Exigências Nutricionais de Bovinos Leiteiros, 8ª ed., PT-BR) — Notas técnicas: Cap. 1, 2 e 3

**Capítulos e páginas impressas cobertas:** Sumário do livro (p.1–3, só contexto); Cap. 1 "Definindo Exigências" (p.4–7); Cap. 2 "Ingestão de Matéria Seca" (p.8–22; texto p.8–18, referências p.19–22); Cap. 3 "Energia" (p.23–44; texto p.23–41, referências p.41–44).

**Usado diretamente no modelo? (por capítulo)**
- Cap. 1 — **não** (conceitual). Define a terminologia (exigência = EME; Ingestão Adequada = IA) que condiciona como saídas/restrições do simulador devem ser rotuladas e interpretadas. Nenhuma equação numérica.
- Cap. 2 — **sim** (Eq. 2-1 e 2-2 vacas em lactação; Eq. 2-3 e 2-4 novilhas). O restante do capítulo (fisiologia, manejo, clima) é discussão, **não** entra no modelo. Nenhuma equação de IMS para vacas secas neste intervalo (estão no Cap. 12, fora do escopo).
- Cap. 3 — **sim** (todo o sistema de energia: ED/EM/ELL da dieta e exigências de mantença, lactação, prenhez, crescimento de frame, reservas corporais). Atividade em confinamento e efeitos ambientais **não** têm equação (só discussão); pastejo está no Cap. 13.

Convenções: separador decimal ponto, milhar vírgula. Equações transcritas com `^` expoente, `_` subscrito, `*` multiplicação. Os nomes de variáveis nas equações do livro estão em inglês (códigos do software); a tradução PT está entre parênteses. `[p.N]` = página impressa. Tudo marcado "(corrigido pela imagem)" divergiu do OCR; vale a imagem.

Glossário PT↔código EN usado nas equações: IMS=DMI; PC=BW; PCMat=MatBW (peso corporal à maturidade); ECC=BCS; DEL/DIM=dias em lactação; PL=MY/milk yield; FDN=NDF; FDA=ADF; FDNf=forage NDF (FDN de forragem); DFDNf=digestibilidade da FDN de forragem; AG=FA; PB=CP; PDR=RDP; PNDR=RUP; PNDRd=dRUP; MOR=ROM; EB=GE; ED=DE; EM=ME; ELL=NEL; EBG=ganho de peso vazio; GMD=ADG; ER=RE (energia retida); NNP=NPN; EPBNNPs=sNPNCPE.

---

## 0. Contexto — Sumário do livro (p.1–3) [só contexto]
O "Sumário" (na verdade um resumo executivo, não um índice) descreve o escopo de cada capítulo. Pontos que amarram o resto do spec: [p.1] o software estima IMS usando só fatores do animal OU animal + dieta; [p.1–2] em energia o sistema ELL foi mantido, mas o método de ELL da dieta mudou (desconto por nível de ingestão), ED é calculada por alimento mas EM e ELL **só para a dieta completa**, mantença subiu ~20%; [p.2] Cap. 10 = bezerras (<18% do PC adulto ≈125 kg Holandês), Cap. 11 = novilhas (>18% do PC adulto até 60 ou 21 dias pré-parto conforme entrada do usuário), Cap. 12 = transição/IMS de vacas secas e pré-parto; [p.3] Cap. 13 sistemas (pasto: exigência de energia maior), Cap. 14 metano (equação também usada para EM) e excreção de N/P, Cap. 18 ensaios, Cap. 19 composição de alimentos, Cap. 20 lista todas as equações do modelo, Cap. 21 tabelas de recomendação. Cap. 15–17 não são usados diretamente no modelo. Errata: correções factuais foram feitas nas páginas 41, 64, 74, 87, 257 e 434 (já incorporadas) [p.1, nota].

---

# CAPÍTULO 1 — Definindo Exigências (p.4–7)

### 1.1 Papel no simulador
Define semanticamente o que o simulador chama de "exigência": quantidade média diária de nutriente (EME) para um animal saudável sem variação de reservas, mais a reposição de reservas mobilizadas na lactação. Nutrientes sem dados suficientes são expressos como Ingestão Adequada (IA), não como exigência. Define que a maioria das exigências é expressa em nutriente absorvido (minerais) ou metabolizável (energia, proteína, aminoácidos), e que o sistema é fatorial. Não fornece números ao cálculo.

### 1.2 Entradas / Saídas
Nenhuma entrada ou saída numérica. Conceitos de saída: cada nutriente deve ser rotulado como "exigência" (EME) ou "IA".

### 1.3 Equações
Nenhuma. Única relação numérica citada (do sistema humano DRI, usada só como analogia): IDR = EME + 2 DP; quando DP não é estimável, IDR = 1.2 × EME (CV de ~20% no metabolismo energético humano) [p.5].

### 1.4 Parâmetros e definições (transcrição)
Definições adotadas (sistema DRI/IOM 2006, termos como aparecem na tradução; siglas da tradução são inconsistentes) [p.4–5]:

| Termo (PT, sigla) | Equivalente EN | Definição | Pág. |
|---|---|---|---|
| Exigência Média Estimada (EME) | EAR | ingestão média diária estimada para atender às exigências de metade dos indivíduos saudáveis | p.4 |
| Ingestão Diária Recomendada (IDR) | RDA | ingestão suficiente para quase todos (97–98%); = EME + 2 DP; = 1.2×EME se DP não estimável | p.4–5 |
| Ingestão Adequada (IA) | AI | ingestão média determinada por especialistas que deve atender ou exceder as exigências do grupo, com dados experimentais limitados; usada quando IDR/EME não podem ser determinadas | p.5 |
| Nível Máximo Tolerável de Ingestão (aparece como "MT", "MNIT", "NMT") | UL | maior ingestão média diária que provavelmente não traz risco adverso; inclui "fator de incerteza" (fica abaixo do NMT animal, que é o nível em que efeito adverso foi observado) | p.5 |

Definição de exigência adotada pelo comitê: "exigência" = EME; reservada a nutrientes cuja exigência média é conhecida com confiança [p.5]. "Exigência mínima" é termo obsoleto [p.4]. O comitê **não** especifica equivalente a IDR (fator de segurança de 2 DP) para bovinos leiteiros (dados limitados, economia, e risco de exceder o NMT, excreção ambiental e, para energia, ECC alto) [p.5].

### 1.5 Regras de decisão / restrições para o otimizador
- Não aplicar margem de segurança de 2 DP: alimentar para a exigência média (EME) [p.5]. Consequência para o otimizador: restrições de nutrientes devem ser tratadas como médias, não como pisos de 97–98% da população [p.5].
- Saúde não tem exigência própria: a preservação da saúde é componente da mantença [p.4].
- Mobilização de reservas no pós-parto é fisiológica; a reposição posterior é considerada exigência [p.4].
- Exigência energética total = soma de mantença + crescimento + reprodução (prenhez) + lactação (sistema fatorial); extra de atividade só se pastejo (topografia e distância ao centro de ordenha) [p.6].
- Formulação estocástica (probabilidade de atender restrições) é mencionada como possibilidade **futura**, não implementada [p.6].

### 1.6 Lógica e fluxo
Exigências fatoriais: mantença (função do PC), crescimento (taxa e composição do ganho), reprodução (estágio de gestação, tamanho do feto/útero), lactação (quantidade e composição do leite) [p.6]. Variabilidade da composição de ingredientes e das exigências entre animais deve ser considerada (amostragem frequente de ingredientes variáveis; maior fonte de variação da MS da dieta é dia-a-dia; para outros nutrientes, fazenda, mês e amostragem) [p.6].

### 1.7 Limitações e incertezas
Respostas reais a nutrientes são curvilíneas (retornos decrescentes), logo o "ótimo" é econômico, não um ponto fixo (análise de ponto de ruptura é só uma aproximação) [p.4]. Variabilidade reportada depende do delineamento experimental (maior em DIC que em quadrado latino ou com covariável) e inclui erro de medida [p.6]. Para vitaminas e alguns microelementos usa-se IA [p.5].

### 1.8 Dúvidas / riscos de OCR
- ⚠ p.5: o OCR corrompeu a definição de IA ("IngestãorAdequadas(iAa)", "deveratendemomexceder"); recuperada pela imagem. Siglas da tradução (RDI/RID, IDR/TDR, MNIT/NMT/MT) são inconsistentes; usei EME/IDR/IA/NMT.

---

# CAPÍTULO 2 — Ingestão de Matéria Seca (p.8–22)

### 2.1 Papel no simulador
Fornece a IMS (kg/d) que alimenta o cálculo de ED/EM/ELL (via IMS/PC), de energia gasosa, de energia urinária e do balanço energético. Equação primária de vacas lactantes só com fatores do animal (Eq. 2-1); equação alternativa com fatores da dieta para avaliar efeito de enchimento (Eq. 2-2); novilhas: Eq. 2-3 (sem FDN) e 2-4 (com FDN da dieta). O texto do capítulo é discussão fisiológica e de manejo, sem equação além das quatro.

### 2.2 Entradas

| Variável | Símbolo/sigla (no livro) | Unidade | Definição | Faixa / valores típicos do conjunto de dados | Pág. |
|---|---|---|---|---|---|
| Energia líquida do leite | ELeite (NEL_milk) | Mcal/d | energia do leite produzida por dia (= kg leite/d × Mcal/kg de Eq. 3-14; ligação inferida, ver §Lógica) | 29.9 ± 6.23 (média ± DP) | p.14 |
| Peso corporal | PC (BW) | kg | peso vivo atual | 624 ± 80.2 (Eq. 2-1); 643 ± 59 (Eq. 2-2) | p.14,14 |
| Escore de condição corporal | ECC (BCS) | 1 a 5 | 1=magro, 5=obeso | 3.03 ± 0.459 | p.14 |
| Paridade | Paridade | adimensional 0–1 | 0 = todas primíparas; 1 = todas multíparas | 1,462 primíparas e 1,681 multíparas no ajuste | p.14 |
| Dias em lactação | DIM (DEL) | d | dias pós-parto | 1 a 368; média 105 ± 50 | p.14 |
| Altura | — | cm | média 149 ± 5.28; **não usada** na Eq. 2-1 | só descritivo | p.14 |
| Mudança de PC | — | kg/d | média 0.021 ± 1.22; **não usada** na Eq. 2-1 | só descritivo | p.14 |
| FDN de forragem da dieta | FDNf | % da MS | FDN proveniente de forragem | 23.9 ± 5.7 | p.14–15 |
| Relação FDA/FDN da dieta | FDA/FDN | fração (g/g) | proxy de fragilidade da forragem; leguminosas ~0.8, gramíneas perenes ≤ ~0.6 | 0.600 ± 0.083 | p.14–15 |
| Digestibilidade da FDN de forragem | DFDNf | % da FDN | ensaio in vitro ou in situ, de uma forragem ou da principal | 52.0 ± 12.3 | p.14–15 |
| Produção de leite | PL | kg/d | produção na lactação | 32.0 ± 7.5 (média dentro do estudo) | p.14 |
| PC da novilha | PC | kg | peso corporal atual | 58–588 kg (faixa citada para validação do NRC 2001; faixa do dado de Hoffman não informada) | p.15 |
| PC à maturidade | PCMat (MatBW) | kg | PC adulto esperado; Holandês presumido 700 kg | 700 (Holandês) | p.16 |
| FDN da dieta (novilhas) | FDN | % da MS | concentração de FDN total da dieta | não informado | p.16 |
| Outros dados descritivos do conjunto da Eq. 2-2 | PB 17.8 ± 1.6; FDN 34.1 ± 4.6; FDA 20.5 ± 4.0 (% MS); IMS 23.0 ± 2.8 kg/d; DEL 60–309 (média 107 ± 48) | | **não** entram na equação final (PB, FDN, FDA, PC foram removidos pela seleção backward) | | p.14–15 |

### 2.3 Saídas

| Variável | Unidade | Definição | Pág. |
|---|---|---|---|
| IMS (vacas, animal) | kg/d | Eq. 2-1 | p.14 |
| IMS (vacas, animal+dieta) | kg/d | Eq. 2-2, válida só >60 DEL | p.15 |
| IMS (novilhas) | kg/d | Eq. 2-3 ou 2-4 | p.16 |

### 2.4 Equações

**Eq. 2-1** [p.14] — IMS de vacas Holandesas em lactação (equação primária do modelo; só fatores do animal). Imagem conferida (OCR ok).
```
IMS (kg/d) = [ (3.7 + Paridade*5.7) + 0.305*ELeite(Mcal/d) + 0.022*PC(kg)
             + (-0.689 - 1.87*Paridade)*ECC ]
           * [ 1 - (0.212 + Paridade*0.136) * e^(-0.053*DIM) ]
```
Como impresso (não corrigido): `IMS (kg/d) = [3.7 + Paridade x 5.7) + 0.305 ELeite (Mcal/d) + 0.022 x PC (kg) + (-0.689 - 1.87 x Paridade) x ECC] x [1 - (0.212 + Paridade x 0.136) x e^(-0.053 x DIM)]` — o livro tem parênteses desbalanceados (falta "(" antes de 3.7 e ")" após DIM); a leitura acima é a estruturalmente coerente (⚠ ver §10).
- IMS kg/d; ELeite Mcal/d; PC kg; ECC escala 1–5; DIM dias; Paridade 0 (primípara) a 1 (multípara) (fator "que varia de 0 (todas primíparas) a 1 (todas multíparas)", sugerindo fração de multíparas em grupo; para vaca individual 0 ou 1) [p.14].
- Dados: 31,635 observações semanais, 3,143 lactações (1,462 primíparas + 1,681 multíparas) de 2,791 vacas, 11 estações de pesquisa dos EUA, 2007–2016 (de Souza et al., 2019); vacas só Holandesas, confinadas, TMR 1×/d, ordenhadas 2–3×/d [p.14].
- Desempenho (validação cruzada entre estudos no conjunto de modelagem): RMSEP = 2.61 kg; viés médio = 0.008 kg; "erro médio, porcentagem do MSE = 6.9"; "viés de intercepto, % do MSE = 2.28"; coeficiente de correlação de concordância (CCC) = 0.80 [p.14].
- Validação independente: 9,050 observações semanais; superior à equação do NRC 2001, principalmente pós-pico [p.14].
- Efeito do ECC embutido: IMS cai 0.70 kg/d (primíparas) e 2.6 kg/d (multíparas) por unidade de ECC; o ajuste de início de lactação é maior para multíparas [p.14]. Comparada ao NRC 2001: menos IMS por unidade de energia do leite; coeficiente de mantença semelhante (interpretar: PC 0.022) [p.14–15].
- Raça: desenvolvida com Holandesas; estimou razoavelmente vacas cruzadas Jersey×Holandesa em um conjunto limitado de médias de tratamento da literatura [p.15]. Para Jersey o NRC 2001 remete a Holter et al. (1996) (não detalhado aqui) [p.13].

**Eq. 2-2** [p.15] — IMS de vacas lactantes com fatores de enchimento da dieta e PL (Allen et al., 2019). Imagem conferida.
```
IMS (kg/d) = 12.0 - 0.107*FDNf + 8.17*(FDA/FDN)
           + 0.0253*DFDNf - 0.328*(FDA/FDN - 0.602)*(DFDNf - 48.3)
           + 0.225*PL + 0.00390*(DFDNf - 48.3)*(PL - 33.1)
```
- IMS kg/d; FDNf = FDN de forragem da dieta, % MS; FDA/FDN = FDA como fração da FDN da dieta; DFDNf = digestibilidade da FDN de forragem in vitro ou in situ, %; PL = produção de leite, kg/d.
- Dados: 134 médias de tratamento, 34 experimentos, 32 artigos, 1990–2015; vacas Holandesas 60–309 DEL. Modelo completo com termos lineares e quadráticos de PB, FDA, FDN, FDNf, FDA/FDN, DFDNf, interações com PC e PL média; reduzido por backward stepwise (menor BIC); validação cruzada 5 vezes. PC não foi significativo e saiu da equação [p.14–15].
- Desempenho: intercepto observado vs estimado = −0.05 kg; inclinação = 1.006; viés médio 0.00 kg/d; RMSEP (RQMEP) = 1.55; CCC = 0.83 [p.15].
- Direção dos efeitos: IMS ↑ com PL e FDA/FDN; ↓ com FDNf; IMS×DFDNf positiva em PL alta e negativa em PL baixa; IMS cresce mais com PL quando DFDNf é alta; DFDNf e FDA/FDN interagem (efeito de FDA/FDN some quando DFDNf é alta) [p.15].
- Validade (condições): usar **somente após 60 DEL** (dados de início de lactação ausentes; controle metabólico domina pós-parto); só Holandesas (adequação a Jersey/cruzadas **desconhecida**, PC não entrou); conjunto não incluiu FFNF (fibra de não forragem) em grande variação nem forragens moídas/picadas — "avaliação de grandes mudanças em FFNF não é recomendada"; forragens moídas, peletizadas ou muito picadas **não** devem ser classificadas como forragem para esta equação; dietas do conjunto tinham uma forragem única ou outras com pouca participação [p.15].
- Dieta com múltiplas forragens: usar **média ponderada** de DFDNf; se DFDNf não disponível, usar a média do conjunto, **52.0%**; DFDNf deve ser medida pelo mesmo método e tempo de incubação, de preferência no mesmo lote ou corrigida pelo mesmo padrão laboratorial [p.15–16].

**Eq. 2-3** [p.16] — IMS de novilhas, sem FDN da dieta (Hoffman et al., 2008, modificada para PCMat). Imagem conferida.
```
IMS (kg/d) = 0.022 * PCMat * ( 1 - e^( -1.54 * (PC/PCMat) ) )
```
- PC kg (atual); PCMat kg (esperado da novilha; Holandês presumido 700 kg). Recomendada quando a FDN da dieta **não** é conhecida [p.16].

**Eq. 2-4** [p.16] — IMS de novilhas, com FDN da dieta. Imagem conferida em dpi 250 (corrigido: não há erro de OCR relevante, apenas os parênteses/chaves).
```
IMS (kg/d) = [ 0.0226 * PCMat * ( 1 - exp( -1.47 * (PC/PCMat) ) ) ]
           - [ 0.082 * ( FDN - ( 23.1 + 56*(PC/PCMat) - 30.6*(PC/PCMat)^2 ) ) ]
```
- FDN = concentração de FDN da dieta, % da MS. Recomendada quando a FDN da dieta é conhecida [p.16].
- Origem: Hoffman et al. (2008), banco de IMS diário de 44 lotes de novilhas Holandesas e 30 lotes de cruzadas, 28 meses; incluir FDN aumentou modestamente o R², diminuiu erros padrão e eliminou o viés em relação ao PC; temperatura teve efeito significativo mas pequeno, e **não** foi incluída; RMSE/R² numéricos não informados [p.15–16].
- Ambas (2-3 e 2-4) dependem apenas de PC/PCMat: adequadas a todas as raças via PCMat [p.16]. O texto incentiva medir IMS real em vez de depender das estimativas [p.16].

**Vetores de teste (cálculo meu a partir das equações transcritas; NÃO são do livro):** Eq. 2-1: multípara, PC 650 kg, ELeite 30 Mcal/d, ECC 3, DEL 105 → 25.14 kg/d; multípara, ELeite 25, DEL 7 → 17.97; primípara, PC 560, ELeite 20, DEL 7 → 17.12. Eq. 2-2 com as médias do conjunto (FDNf 23.9, FDA/FDN 0.600, DFDNf 52.0, PL 32.0) → 22.85 kg/d. Eq. 2-3: PC 400, PCMat 700 → 9.01 kg/d; Eq. 2-4 (FDN 40%) → 9.41 kg/d; PC 200 → 5.48 (2-3) e 5.15 (2-4).

### 2.5 Parâmetros e tabelas
Não há tabela numérica de coeficientes no Cap. 2 (os coeficientes estão nas equações). Valores numéricos de respostas da literatura (não usados em equação do modelo, úteis como regras/faixas) estão em §2.6 e §2.9.

### 2.6 Regras de decisão / restrições para o otimizador
- Eq. 2-1 é a equação primária (só animal). Eq. 2-2 é opcional "para avaliar" efeito de dieta; limitar a vacas >60 DEL, Holandesas [p.15].
- Ajuste (não em equação, qualitativo, "usar com cautela"): fontes de gordura com insaturadas (óleo, sebo, sais de cálcio de palma, sais de cálcio de AGCL) reduzem a IMS em média −0.41 kg/d por 1% de gordura adicionada (Weld e Armentano, 2017) [p.15]. Não há recomendação quantitativa para PB dietética nem para propionato ruminal por falta de dados e variação por estado fisiológico [p.15].
- Clima: **sem fator de ajuste de temperatura/umidade** nas equações de IMS (dados insuficientes fora da zona termoneutra); durante estresse térmico a IMS real tende a ser menor do que a prevista a partir de PL [p.18; também p.34–35].
- Novilhas: Eq. 2-3 sem FDN conhecida; Eq. 2-4 com FDN conhecida; PCMat obrigatório [p.16].
- Manejo (informativo): ≥46 cm de cocho por vaca (Albright 1993); novilhas jovens (4–8 meses) mantiveram crescimento rápido com 15 cm; aos 17–21 meses precisam ~47 cm [p.17]; acesso ao alimento limitado a 8 h/d reduz PL em 5–7% [p.16–17]; agrupar primíparas separadamente (+725 kg leite/305 d em Phelps e Drew 1992; sem efeito em IMS/PL em ordenha robótica, Bach 2005) [p.18]; vacas pós-parto em grupo separado, dieta com maior enchimento e amido moderadamente fermentável até a distensão limitar a IMS; início/meio de lactação (limitadas por distensão) se beneficiam de menor enchimento e mais amido; vacas no fim da lactação, após recuperar reservas, dieta com menos amido para não ganhar ECC em excesso [p.18].

### 2.7 Lógica e fluxo
1. Se o simulador conhece PL e composição (ELeite via Eq. 3-14 × PL), calcular IMS com Eq. 2-1 (precisa de PC, ECC, paridade, DEL). Observação: Eq. 2-1 usa ELeite como entrada, portanto **não há circularidade** com a dieta; a dieta só entra pela Eq. 2-2 (opcional). Se o simulador predisser o leite a partir da dieta, será preciso iterar (não descrito no livro).
2. IMS/PC (kg/kg) alimenta Eq. 3-5a/3-5b (digestibilidade de FDN e amido) e Eq. 3-9 (gás), 3-10a (N urinário), 3-6b, 3-7 (Cap. 3).
3. Novilhas: PC e PCMat → Eq. 2-3/2-4; saída entra no mesmo cálculo de energia (que para novilhas usa EM, Caps. 10 e 11; ver Cap. 3 §Lógica).
4. IMS de vacas secas e pré-parto: **não** está neste intervalo (Cap. 12) [Sumário p.2].

### 2.8 Limitações, incertezas e mudanças vs. NRC 2001
- NRC 2001: equação empírica (Rayburn e Fox 1993 × ajuste de semana de lactação de Roseler et al. 1997) para Holandesas, só fatores do animal; avaliada contra dados semanais; sem ajuste por paridade (PC e PL explicariam). A Eq. 2-1 nova inclui ECC, paridade e sua interação e um ajuste de início de lactação dependente da paridade; IMS menor por unidade de energia do leite que NRC 2001 (atribuído a melhorias de produção e alimentação em 20 anos) [p.13–15].
- Novilhas: NRC 2001 usava equação de bezerras do NRC corte (1996), validada com 2,727 observações (58–588 kg) sem estatísticas e subestimando progressivamente a IMS de 2 para 12 kg/d; substituída pelas equações de Hoffman et al. (2008) adaptadas com PCMat [p.15–16].
- A precisão da IMS é limitada por interações dieta × estado fisiológico; efeitos de dieta em IMS não são plenamente modelados; IMS estimada é "média dos efeitos das dietas dos estudos" [p.13–14].
- Eq. 2-2 não deve ser usada em início de lactação nem para raças pequenas/cruzadas (desconhecido) [p.15].
- Heat stress não modelado [p.18].

### 2.9 Conceitos e evidências relevantes (curtos)
- Controle da IMS: sinais estimuladores (status energético, fatores sensoriais, sociais, circadianos) e inibitórios (distensão ruminal, osmolaridade, endócrinos, detecção de combustível) [p.8]. Pós-parto imediato: balanço energético negativo sem distensão limitante; distensão passa a limitar com o aumento de PL e no pico; com a queda de PL domina o controle por combustíveis específicos [p.8–9].
- Distensão: receptores no retículo/saco cranial; adicionar enchimento inerte reduz IMS em 112 g/kg de peso e 157 g/L de volume (Schettini 1999); volume de reserva ~16 L (Dado e Allen 1995) [p.8–9]. Abomaso também pode limitar [p.9].
- FDN de forragem tem maior efeito de enchimento que FDN de FFNF (casca de soja, polpa de beterraba, DDG), logo FDNf é melhor preditor que FDN total; substituir concentrado por FFNF tem pouco efeito na IMS [p.9]. +1 unidade de DFDN da forragem → +0.17 kg/d de IMS e +0.25 kg/d de leite corrigido para gordura (Oba e Allen 1999b) [p.9]. DFDN in vitro só compara dentro do mesmo tipo de forragem; gramíneas têm maior enchimento (maior retenção) e menor IMS que leguminosas; FDA/FDN usada como proxy de fragilidade [p.9, 14].
- Controle metabólico (teoria da oxidação hepática, HOT; Allen et al. 2009): propionato é o principal sinal de saciedade; amido muito fermentável reduz IMS; açúcares não são hipofágicos; glicose infundida não afeta IMS de ruminantes; gorduras insaturadas e AGCM reduzem IMS (Weld e Armentano 2017: saturadas de AGCL tendem a +0.7 kg/d por 3% de gordura adicionada; maioria das outras −0.8 a −1.3 kg/d por 3%; AGCM −3.5 kg/d por 3%; saturadas com muito palmítico sem efeito) [p.10–11].
- Proteína: aumento de PB dietética aumentou IMS em média 0.6 kg/d por ponto percentual de PB em 7 das 25 comparações (Allen 2000) (corrigido pela imagem: OCR leu "77 das 25"); NNP excessivo ou excesso/desequilíbrio de aminoácidos reduz IMS; resposta marginal cai com PB crescente [p.11–12].
- Estado fisiológico: ECC no parto correlaciona-se negativamente com IMS pós-parto; maior mobilização de gordura → maior queda de IMS e maior balanço energético negativo [p.12]. Amido: efeitos dependem de fermentabilidade e de FDNf (ex.: aumentar amido substituindo FFNF reduziu IMS em 1.5 kg/d, Dann e Nelson 2011, 21→25.5% de amido; efeito nulo em McCarthy 2015, 21.5→26%) [p.12–13].
- Pico: PL em 4–8 semanas; pico de IMS ~10 semanas pós-parto (NRC 1989) [p.13].
- Comportamento: vacas início de lactação comem ~5 h/d, 9–13 refeições (média 11) de ~29 min, cada refeição ~10% da IMS diária (Dado e Allen 1994) [p.16]. Frequência de fornecimento tem pouco efeito em IMS (Hart 2014: 30.6, 29.7 e 31.1 kg/d para 1, 2 e 3 vezes/d em multíparas); fornecer entre ordenhas tendeu a reduzir IMS (27.2 vs 26.5 kg/d, P<0.10) com melhor eficiência (1.83 vs 1.67 kg de leite 4% /kg IMS; King 2016); fornecimento à noite no verão reduziu IMS e digestibilidade [p.17]. Água na TMR: reduzir MS de 81→64% sem efeito em IMS/PL (Leonardi 2005); no verão (56→51 ou 44% de MS) aumentou seleção e reduziu IMS [p.17]. Vacas selecionam contra partículas longas, primíparas mais que multíparas [p.17–18].
- Clima: zona termoneutra ~5–20 °C; estresse por calor agudo com THI 72 vs 57 diminuiu IMS em 11.5% (Collier 2018); pode reduzir IMS >50% (NRC 1981); redução maior com PL maior; atraso de 24–48 h; West et al. (2003): IMS −0.85 kg/d por °C de temperatura média do ar (2 dias antes, faixa 25–32 °C) e PL −0.88 kg/d por unidade de THI (faixa 73–83), vacas Holandesas; período frio <21 °C minimiza a queda de PL (Igono 1992); a redução de IMS explica só ~50% da queda de PL (Wheelock 2010) [p.18].

### 2.10 Dúvidas / riscos de OCR
- ⚠ Eq. 2-1: parênteses desbalanceados no original; transcrição segue a estrutura matemática coerente. Confirmar contra de Souza et al. (2019) se possível.
- ⚠ Eq. 2-4: expoente "²" em (PC/PCMat)² conferido na imagem (dpi 250); chaves `{}` do original equivalem a parênteses.
- ⚠ O texto diz "RMSEP = 2.61 kg" e para Eq. 2-2 "RQMEP de 1.55" sem unidade explícita (presumivelmente kg/d). A frase "erro médio, porcentagem do MSE = 6.9" é como impressa; não é possível afirmar qual componente do MSE ela representa.
- ⚠ p.14 e p.15: "ELeite" (Mcal/d) é chamado "energia líquida do leite"; a conversão leite→ELeite não está nesta equação (ver Eq. 3-14).
- OCR corrigido pela imagem: p.11 "77 das 25"→"7 das 25". Demais números narrativos conferidos nas imagens p.8, 9, 11, 12, 18 e 37.

---

# CAPÍTULO 3 — Energia (p.23–44)

### 3.1 Papel no simulador
Núcleo energético: (a) converte a composição da dieta em ED, EM e ELL (Mcal/kg MS) da **dieta total** a partir de frações (FDN, amido, AG, PB, cinzas, MOR), digestibilidades basais ajustadas para IMS/PC e amido, perdas fecais endógenas, gás e urina; (b) calcula as exigências de ELL (mantença, lactação, prenhez, crescimento de frame, reservas corporais, atividade) e o balanço energético. Valores de EM/ELL **não** são válidos por alimento; ED por alimento (Tab. 19-1) só vale nas condições basais.

### 3.2 Entradas

| Variável | Símbolo/sigla | Unidade | Definição | Faixa / valores típicos | Pág. |
|---|---|---|---|---|---|
| IMS | IMS (DMI) | kg/d | do Cap. 2 | — | p.29–31 |
| Peso corporal | PC (BW) | kg | atual | — | p.29,32 |
| PC à maturidade | PCMat (MatBW) | kg | ~700 Holandês | 700 | p.36,39 |
| IMS/PC | IMS_PC (DMI_BW) | kg/kg | base de ajuste de digestibilidade | base = 0.035 (3.5%) | p.28–29 |
| FDN da dieta | NDF_DM | % MS | | — | p.26 |
| Lignina da dieta | Lignin_DM | % MS | para Eq. 3-3a (tipo de lignina não informado) | — | p.26 |
| DIVFDN 48 h | IVNDFD | proporção da FDN | alternativa à lignina (Eq. 3-3b) | — | p.26 |
| Amido | Starch_DM | % MS | | base 26% | p.28 |
| Ácidos graxos | FA_DM | % MS | AG com >4 C; exclui AG voláteis e lático | — | p.24 |
| Proteína bruta | CP_DM | % MS | N × 6.25 | — | p.24 |
| PDR / PNDRd | RDP_DM, dRUP_DM | % MS | do Cap. 6 | — | p.27 |
| PB equiv. do NNP suplementar | sNPNCPE_DM | % MS | separado de PB | — | p.24 |
| Cinzas | Ash_DM | % MS | | — | p.24 |
| Digestibilidade basal do amido por alimento | dStarch_Starch_base | proporção | Tabela 3-1 | 0.77–0.96 | p.27 |
| Digestibilidade dos AG de suplementos de gordura | dFA_FA | proporção | Tabela 4-1 (Cap. 4); AG basais 0.73 | — | p.27 |
| Proteína microbiana | Microbial CP | g/d | do Cap. 6 | — | p.30 |
| PB do leite; ganho de proteína corporal | Milk CP, Body gain CP | kg/d | p/ N urinário | — | p.31 |
| Composição do leite | gordura, PB (ou PV), lactose | kg/kg leite ou % | p/ ELL do leite | lactose default 0.0485 kg/kg | p.33–34 |
| Produção de leite | PL | kg/d | multiplica ELL/kg do leite | — | p.14,33 |
| ECC, variação de ECC / PC | ECC, ΔPC | kg/d | mobilização/reposição | ECC 2–4 constante de composição | p.38 |
| Dias de gestação | DayGest | d | 12–280 | gestação 280 d | p.35 |
| Dias de lactação | DayLact | d | involução uterina | 0.2/d, completa ~21 d | p.35 |
| Peso do bezerro ao nascer | Calf birth weight | kg | entrada; ver pesos médios por raça | 44 Holandês | p.35 |
| GMD, EBG | ADG, EBG | kg/d | crescimento de frame | EBG/ADG=0.85 novilhas | p.39 |
| Distância ao centro de ordenha, nº de ordenhas | — | km, n/d | atividade em confinamento | 0.2 km, 3×/d | p.34 |

### 3.3 Saídas

| Variável | Unidade | Definição | Pág. |
|---|---|---|---|
| EB da dieta/alimento (GE_DM) | Mcal/kg MS | Eq. 3-2 | p.26 |
| Digestibilidades dNDF_NDF, dStarch_Starch | proporção | Eq. 3-3, 3-5 | p.26–29 |
| Digestibilidade aparente de MOR, PB, MO (adROM_ROM, adCP_CP, adOM_OM) | proporção | Eq. 3-7a,b,c | p.30 |
| ED (DE_DM) | Mcal/kg MS | Eq. 3-8 | p.30 |
| Energia gasosa (GasE_DM) | Mcal/kg IMS | Eq. 3-9 | p.30 |
| N urinário (UN) | g/d | Eq. 3-10a | p.31 |
| Energia urinária (UE_DM) | Mcal/kg IMS | Eq. 3-10b | p.31 |
| EM (ME_DM) | Mcal/kg MS | Eq. 3-11 | p.31 |
| ELL da dieta (NEL_DM) | Mcal/kg MS | Eq. 3-12 | p.31 |
| ELL de mantença | Mcal/d | Eq. 3-13 | p.32 |
| ELL do leite | Mcal/kg leite | Eq. 3-14a/b/c | p.33–34 |
| ELL de gestação | Mcal/d | Eq. 3-18 | p.36 |
| Ganho de peso de útero gravídico; peso do útero | kg, kg/d | Eq. 3-15 a 3-17 | p.35–36 |
| ELL para ganho/perda de reservas | Mcal/kg ganho; Mcal/kg perda | Eq. 3-19 | p.38 |
| ER, EM e ELL de ganho de frame | Mcal/kg ADG | Eq. 3-20 | p.39 |
| Eficiência alimentar | adimensional (energia/energia) | Eq. 3-21 | p.40 |

### 3.4 Equações

**Eq. 3-1** [p.24] — Matéria orgânica residual (MOR). Imagem conferida.
```
ROM = 100 - Ash - NDF - Starch - (FA / FatFactor) - (CP - 0.64*sNPNCPE)
```
Todas as frações em % da MS. FatFactor = 1 se tipo de alimento = ácido graxo ou sabão de AG; 1.06 para todos os outros alimentos (TG: massa hidrolisada de AG + glicerol = 106% da massa de TG) [p.24–25]. 0.64 = 181/281 (ureia: 281% PB e −181% MOR; sem a correção a ureia teria EB de 8.6 em vez de 2.5 kcal/g) [p.24]. MOR contém carboidratos solúveis, ácidos de fermentação (acético, butírico, lático), glicerol, fibra solúvel (pectinas, gomas) e outros (taninos, ceras) [p.24]. FDN usada em vez de FDN livre de PB e cinzas, mesmo havendo dupla contagem de cinzas e PB insolúveis em detergente neutro; justificativas p.25 (FDN livre de PB e cinzas ≈ 94% da FDN em dietas totais; erro <0.1% na soma FDN digerida+MOR digerida) [p.25].

**Eq. 3-2** [p.26] — Energia bruta do alimento ou dieta. Imagem conferida.
```
GE_DM (Mcal/kg MS) = 0.042*NDF_DM + 0.0423*Starch_DM + 0.040*ROM_DM
                   + 0.094*FA_DM + 0.0565*(CP_DM - sNPNCPE_DM) + 0.0089*sNPNCPE_DM
```
Frações em % da MS. Coeficientes = calores de combustão (Mcal/kg): amido 4.23; AG 9.4; FDN 4.2; MOR 4.0 (estimativa do comitê); PB (sem NNP suplementar) 5.65; EPBNNPs 0.89 (ureia 2.5 Mcal/kg ÷ 2.81) [p.25–26].

**Eq. 3-3a** [p.26] — Digestibilidade basal da FDN (método da lignina; padrão do modelo; vem da 7ª edição). Imagem conferida (dpi 250).
```
dNDF_NDF_base = { 0.75*NDF_DM - Lignin_DM) * [ 1 - (Lignin_DM / NDF_DM)^0.667 ] } / NDF_DM
```
(Transcrição do impresso, com parênteses desbalanceados. A leitura estruturalmente provável é `{0.75*(NDF_DM - Lignin_DM) * [1 - (Lignin_DM/NDF_DM)^0.667]} / NDF_DM`; ⚠ ver §10.) Nutrientes em % da MS; resultado = proporção da FDN. Condição base: IMS 3.5% do PC, 26% de amido [p.26]. O usuário pode optar por Eq. 3-3b ou informar diretamente a digestibilidade de FDN [p.26].

**Eq. 3-3b** [p.26] — Alternativa por DIVFDN 48 h (Lopes et al., 2015).
```
dNDF_NDF_base = 0.12 + 0.61*IVNDFD
```
IVNDFD = digestão in vitro de 48 h, em proporção da FDN. 48 h foi melhor que 30 h para prever digestibilidade in vivo em vacas ad libitum (~24 kg IMS/d); dados in vivo×in vitro insuficientes para comparar robustamente 3-3a e 3-3b [p.26].

**Eq. 3-4** [p.27] — Proteína digerida (verdadeira, trato total). Imagem conferida.
```
dCP_CP = (RDP_DM + dRUP_DM) / CP_DM
```
RDP, dRUP, CP em % da MS. Independe da IMS (modelo proteico; Cap. 6) [p.27].

Valores basais: dROM_ROM_base = 0.96 (digestibilidade verdadeira da MOR calculada com FDN; teste de Lucas, Tebbe et al. 2017) [p.27]. dFA_FA_base = 0.73 para a maioria dos alimentos; suplementos de gordura usam Tabela 4-1 (Cap. 4) [p.27]. Digestibilidade de amido basal: Tabela 3-1 [p.27]. Digestibilidade basal da proteína: Eq. 3-4 [p.27].

**Eq. 3-5a** [p.28] — Digestibilidade da FDN ajustada por amido da dieta e IMS (de Souza et al. 2018, modificada). Imagem conferida.
```
dNDF_NDF = dNDF_NDF_base - 0.0059*(Starch_DM - 26) - 1.1*(DMI_BW - 0.035)
```
Starch_DM em % da MS; DMI_BW = IMS/PC em kg/kg (fração, não %). dNDF_NDF_base de Eq. 3-3a/b. O coeficiente 1.1 = média da inclinação marginal (1ª derivada da curva de de Souza et al.) de IMS = 3.5% até 5.5% do PC (limite dos dados); o comitê removeu a depressão em ingestões <3.5% do PC mantendo a depressão em ingestões maiores [p.28]. Referências cruzadas: White et al. (2017) −7 pontos percentuais por unidade de IMS/PC, sem efeito do amido; Ferraretto et al. (2013) −0.5 ponto percentual por ponto de amido, sem efeito de IMS [p.28]. Sem efeito de fermentabilidade do amido (dados insuficientes) nem de tamanho de partícula da fonte de FDN nem de PDR deficiente [p.28–29]. Limites inferior/superior para a digestibilidade ajustada: não informado. Observação (implícita): com IMS_PC <0.035 a equação linear aumenta a digestibilidade (explícito para o amido, p.29).

**Eq. 3-5b** [p.29] — Digestibilidade do amido ajustada por IMS.
```
dStarch_Starch = dStarch_Starch_base - 1.0*(DMI_BW - 0.035)
```
DMI_BW em kg/kg. Quando IMS_PC > 0.035 a proporção de amido digerido diminui 1 ponto percentual por ponto de IMS/PC; quando <0.035 aumenta [p.29]. Fontes: de Souza et al. (2018) −1 ponto/ponto; Ferraretto et al. (2013) −0.24 pontos por kg de IMS (≈ −1.3 por unidade de IMS_PC). Dados muito enviesados para milho moído seco; o ajuste pode subestimar a digestibilidade de amido muito fermentável em alta IMS [p.29].

**Eq. 3-6a** [p.30] — PB metabólica fecal (MFCP, endógena). Imagem conferida (OCR leu "MFCE").
```
MFCP (g/kg IMS) = 11.62 + 0.134*NDF_DMI
```
NDF da dieta em % da MS. No cálculo da tabela de alimentos (Cap. 19) usa-se FDN da dieta = 30%: MFCP = 15.6 g/kg MS = 0.088 Mcal/kg IMS [p.30].

**Eq. 3-6b** [p.30] — PB microbiana fecal (não digerida).
```
fMCP (g/kg IMS) = ( Microbial_CP (g/d) * 0.2 ) / IMS (kg/d)
```
Assume 20% da PB microbiana não digerida. Valor médio usado na tabela de alimentos: 16.5 g/kg IMS = 0.093 Mcal/kg [p.30]. Cap. 6 detalha MFCP e proteína microbiana [p.29].

Valor usado para MOR fecal endógena (efROM): 34.3 g/kg IMS = 0.137 Mcal/kg IMS (Tebbe et al. 2017). Energia fecal endógena total na tabela: 0.088 + 0.093 + 0.137 = 0.318 Mcal/kg IMS [p.30]. Entalpias: 5.65 Mcal/kg (PB) e 4.0 Mcal/kg (MOR) [p.30].

**Eq. 3-7a** [p.30] — Digestibilidade aparente da MOR.
```
adROM_ROM = [ (ROM*0.96) - 3.43 ] / ROM
```
ROM em % da MS (3.43% = efROM 34.3 g/kg) [p.30].

**Eq. 3-7b** [p.30] — Digestibilidade aparente da PB.
```
adCP_CP = [ (RDP + dRUP) - (fMCP + MFCP) ] / CP
```
"todas as variáveis em kg/d" [p.30]. Atenção a unidades: RDP, dRUP e CP em kg/d; fMCP e MFCP (calculadas em g/kg IMS) devem ser convertidas para kg/d (× IMS/1000) (⚠ ver §10).

**Eq. 3-7c** [p.30] — Digestibilidade aparente da MO. Imagem conferida.
```
adOM_OM = ( NDF*dNDF_NDF + Starch*dStarch_Starch + FA*dFA_FA + RDP + dRUP
          + 0.96*ROM - MFCP - fMCP - efROM ) / OM
```
Todas as variáveis em kg/d [p.30–31]. Usadas para comparar saídas com dados in vivo [p.30].

**Eq. 3-8** [p.30] — Energia digestível da dieta (ou do alimento nas condições basais). Imagem conferida.
```
DE_DM (Mcal/kg MS) = 0.042*NDF_DM*dNDF_NDF
                   + 0.0423*Starch_DM*dStarch_Starch
                   + 0.0940*FA_DM*dFA_FA
                   + 0.0565*(RDP_DM - sNPNCPE_DM + dRUP_DM)
                   + 0.0089*sNPNCPE_DM
                   + 0.040*ROM_DM*0.96
                   - 0.00565*MFCP - 0.00565*fMCP - 0.0040*efROM_DM
```
Frações dos alimentos em % da MS; frações endógenas (MFCP, fMCP, efROM) em g/kg MS; digestibilidades em proporção [p.30]. Interpretação: nutrientes verdadeiramente digeridos × calor de combustão, menos energia fecal endógena e bactérias não digeridas; NNP suplementar tem o valor da ureia [p.30]. Base de cálculo: IMS = 3.5% do PC e dieta com 26% de amido, PDR adequada e FDN de forragem suficiente (não há dados para modelar PDR nem forragem sobre digestibilidade) [p.26].

**Eq. 3-9** [p.30] — Perda de energia gasosa (metano; Cap. 14). Imagem conferida.
```
GasE_DM (Mcal/kg IMS) = ( 0.294*DMI - 0.347*FA_DM + 0.0409*dNDF_DM ) / DMI
```
DMI em kg/d; FA_DM e dNDF_DM em % da MS da dieta [p.31]. dNDF_DM = FDN digestível em % da MS (= NDF_DM × dNDF_NDF; inferido, não explicitado). Metano em Mcal/d = numerador.

**Eq. 3-10a** [p.31] — N urinário.
```
UN (g/d) = ( DMI*CP_DM*adCP_CP - Milk_CP - Body_gain_CP ) * 1,000 / 6.25
```
DMI, Milk CP e Body gain CP em kg/d; CP_DM e adCP_CP em proporção [p.31]. Se o animal **não está em lactação e está dentro de 60 dias pré-parto**, "PB do leite" é substituído por `0.00014 * Mature BW` (kg/d; proteína retida no útero gravídico aos 250 d com base no peso de bezerros Holandês e Jersey) [p.31]. Ganho de proteína corporal em vacas lactantes pode ser ignorado (100 g/d mudariam EM <0.5%); para novilhas é estimado como no Cap. 11 [p.31].

**Eq. 3-10b** [p.31] — Energia urinária.
```
UE_DM (Mcal/kg IMS) = ( 0.0146 * UN ) / DMI
```
0.0146 Mcal/g de N urinário (Morris et al., 2021) [p.31].

**Eq. 3-11** [p.31] — Energia metabolizável da dieta.
```
ME_DM (Mcal/kg IMS) = DE_DM - GasE_DM - UE_DM
```
Válida só para dieta total; ao usar AG para estimar metano, a eficiência ED→EM sobe em dietas ricas em gordura (substitui a correção do NRC 2001 para 100% de eficiência da gordura) [p.31–32].

**Eq. 3-12** [p.31] — ELL da dieta. (corrigido na verificação: página era p.32; a equação e o texto da eficiência 0.66/IC 0.64–0.69 estão na p.31)
```
NEL_DM (Mcal/kg MS) = 0.66 * ME_DM
```
0.66 = média 1974–1995 de Beltsville reavaliada por Moraes et al. (2015), IC 95% 0.64–0.69; sem correção por gordura dietética [p.31].

**Eq. 3-13** [p.32] — Exigência de ELL de mantença. Imagem conferida.
```
NELmaint (Mcal/d) = 0.10 * BW^0.75        (BW em kg)
```
IC 95% do coeficiente ±0.06 (Moraes et al. 2015). Adiciona ~2.5 Mcal/d a uma vaca Holandesa média vs 0.080 [p.32]. Mesmo valor para vaca seca e lactante (ver §3.9). Faixa individual: até ~10% entre vacas semelhantes (Van Es 1961); RFI mostra variação de 7% (Tempelman 2015) [p.32].

**Eq. 3-14a** [p.33] — ELL do leite, quando só PB (N×6.38) é conhecida.
```
NEL (Mcal/kg leite) = 9.29*kg_Gordura/kg_Leite + 5.5*kg_PB/kg_Leite + 3.95*kg_Lactose/kg_Leite
```
**Eq. 3-14b** [p.33] — com proteína verdadeira medida.
```
NEL (Mcal/kg leite) = 9.29*kg_Gordura/kg_Leite + 5.85*kg_ProteínaVerdadeira/kg_Leite + 3.95*kg_Lactose/kg_Leite
```
Calores de combustão (kcal/g = Mcal/kg): gordura 9.29; proteína verdadeira 5.71; NNP equivalente PB 2.21; lactose 3.95. PB do leite = 6.38×N contém 5–6% de NNP; com 6% NNP e 94% proteína verdadeira, 5.5 kcal/g (checagem: 0.94×5.71 + 0.06×2.21 = 5.50). No caso 3-14b o NNP é assumido 5.5% da PB do leite com calor da ureia (2.5 Mcal/kg): 5.71 + 0.055×2.5 = 5.85 [p.33]. Lactose: se não medida, fixar em 0.0485 kg/kg de leite (cerca de 4.85%) [p.33].

**Eq. 3-14c** [p.34] — só gordura do leite medida (Tyrrell e Reid, 1965).
```
NEL (Mcal/kg leite) = 0.360 + 0.0969 * Gordura(%)
```
ELL do leite (Mcal/d) = Mcal/kg × kg leite/d (relação implícita; o livro não a escreve como equação).

**Eq. 3-15a e b** [p.35] — Pesos do útero gravídico e do útero ao parto. Imagem conferida.
```
GrUter_Wt(t=parto) = Calf_birth_weight * 1.825
Uter_Wt(t=parto)   = Calf_birth_weight * 0.2288
```
Calf birth weight em kg. Pesos médios ao nascer (kg) de bezerros de vacas multíparas: Holandês 44, Jersey 26, Ayrshire 38, Pardo Suíço 48, Guernsey 36, Shorthorn leiteiro 36; bezerros de novilhas ≈ 91% desses pesos. Alternativa: 0.063×PCMat (vaca) ou 0.058×PCMat (novilha). Gestação completa aos 280 d (também no software) [p.35].

**Eq. 3-16a e b** [p.35] — Crescimento logístico do útero gravídico e involução pós-parto. Imagem conferida em dpi 300 (corrigido pela imagem: o OCR leu "9.0243"; o valor correto é 0.0243).
```
GrUter_Wt = GrUter_Wt(t=parto) * e^( -(0.0243 - (0.0000245*DayGest)) * (280 - DayGest) )
UterWt    = ( Uter_Wt(t=parto) - 0.204 ) * e^( -0.2*DayLact ) + 0.204
```
DayGest = dias de gestação (deve estar entre 12 e 280); UterWt(t=parto) = peso (kg) do útero imediatamente após o parto (peso ao nascer × 0.2288). Taxa de involução 0.2/d (não conhecida com certeza) → involução essencialmente completa até o DEL 21. Regressão não linear (função logística) com dados de Bell et al. (1995) e House e Bell (1993); involução segundo Hanigan et al. (2009) [p.35].

**Eq. 3-17a e b** [p.35–36] — Taxas diárias de deposição de tecido úmido. Imagem conferida (dpi 300).
```
Durante gestação:  GrUter_Wt_gain = ( 0.0243 - (0.0000245*DayGest) ) * GrUter_Wt
Durante involução: GrUter_Wt_gain = -0.2 * DayLact * (Uter_Wt - 0.204)        [como impresso, ⚠]
```
Unidade kg/d. Na versão impressa a segunda equação aparece como "GrUter_Wt_Gain =t −0.2 × DayLact × (Uter_Wt − 0.204)" (um "t" subscrito solto e o fator DayLact); a derivada analítica da Eq. 3-16b seria −0.2×(Uter_Wt − 0.204) (⚠ ver §10).
Verificação numérica minha (peso do bezerro 44 kg, GrUter_Wt(parto)=80.3 kg), usando 3-16a, 3-17a e 3-18: dia 200 → 1.37 Mcal/d; 220 → 2.03; 250 → 3.52; 275 → 5.37; esses valores reproduzem a Tabela 3-3 coluna "Atual", logo a forma 3-17a como impressa está coerente com a tabela.

**Eq. 3-18** [p.36] — ELL de gestação.
```
Gest_NEL (Mcal/d) = GrUter_Wt_gain * (0.882/0.14) * 0.66 = GrUter_Wt_gain * 4.16
```
GrUter_Wt_gain em kg/d (Eq. 3-17a); 0.882 Mcal/kg = energia do tecido uterino gravídico (House e Bell 1993; Bell et al. 1995); 0.14 = eficiência EM→gestação (Ferrell et al. 1976; NRC 2001); 0.66 = EM→ELL [p.36]. (0.882/0.14×0.66 = 4.158.)

**Eq. 3-19a, b, c** [p.38] — ELL para ganho ou perda de reservas corporais (variação de ECC). Imagem conferida.
```
Em lactação (ganho):    NEL (Mcal/kg ganho de PC) = 6.3 Mcal ER/kg * 0.89 = 5.6 Mcal ELL/kg ganho de PC      (3-19a)
Não lactante (ganho):   NEL (Mcal/kg ganho de PC) = 6.3 Mcal ER/kg * 1.10 = 6.9 Mcal ELL/kg ganho de PC      (3-19b)
ELL disponível (perda): NEL_disponível (Mcal/kg perda de PC) = 6.3 Mcal ER/kg * 0.89 = 5.6 Mcal ELL/kg perda  (3-19c)
```
6.3 Mcal ER/kg = valor energético do ganho/perda de PCV em vacas com ECC 2–4 (62.2% gordura, 27.6% água, 8.1% proteína, 2.1% cinzas; gordura 9.4 e proteína 5.55 Mcal/kg). Fatores (Tabela 3-2): 0.89 = ER→ELL em lactação (inverso de 1.12); 1.10 ≈ 1/0.91 (ELL→ER quando seca 0.91) [p.32,38]. Como 1 kg de PC = 1 kg de PCV para variação de ECC, nenhuma correção de digesta [p.37–38].

**Eq. 3-20a, b, c** [p.39] — Composição e ER do ganho de frame. Imagem conferida.
```
Fat_ADG (g/g)     = ( 0.067 + 0.375*(BW/MatBW) ) * EBG/ADG
Protein_ADG (g/g) = ( 0.201 - 0.081*(BW/MatBW) ) * EBG/ADG
RE_FADG (Mcal/kg) = 9.4*Fat_ADG + 5.55*Protein_ADG
```
BW/MatBW = fração do PC adulto; EBG = ganho de peso corporal vazio; ADG = ganho médio diário (de PC). Novilhas: EBG/ADG = 0.85 (85% tecido, 15% digesta). Vacas imaturas: enchimento do trato = 18% do PC ou ganho de PC (EBG/ADG = 0.82) [p.37,39]. Justificativa e descrição no Cap. 11 (não lido aqui) [p.39].
**Eq. 3-20d, e** [p.39]
```
ME_FADG  (Mcal/kg) = RE_FADG / 0.4
NEL_FADG (Mcal/kg) = RE_FADG / 0.61
```
0.40 = eficiência média EM→ELg (NRC 2001) e 0.40/0.66 = 0.61 (ELL→ELg) [p.39]. Vetor de teste (meu): BW/MatBW=0.5, EBG/ADG=0.85 → Fat 0.216, Prot 0.136 kg/kg ADG, RE 2.79 Mcal/kg ADG, EM 6.98, ELL 4.58 Mcal/kg ADG.

**Eq. 3-21** [p.40] — Eficiência alimentar (definição, não é entrada do modelo).
```
Feed_efficiency = ( Milk_energy + Change_in_body_energy ) / Feed_energy_input
```

**Relações não numeradas** (a implementar, com página):
- U1. Conteúdo do trato digestório (vacas em lactação) ≈ 5.2 × IMS (kg); a 3.5% do PC = 18% do PC. 1 kg de ganho de frame de vaca = 0.82 kg PCV + 0.18 kg digesta [p.37].
- U2. Variação de PC por unidade de ECC = 9.4% do PC (média de estudos com óxido de deutério: 63 kg a 667 kg; 59 kg a 634 kg; 56 kg a 640, 558 e 597 kg), assumida 100% PCV (sem mudança de digesta). Se digesta fosse 18% do PC → 11.5% do PC por unidade de ECC (vaca ECC 3; maior em vaca magra, menor em gorda) [p.37]. NRC 2001: −14% do PC por ECC (~80 kg) com 18% de enchimento [p.37].
- U3. 1 ECC (vaca 650 kg) = 61 kg de massa corporal = 385 Mcal ER e 5.0 kg de proteína; ganhar 1 ECC requer 520 Mcal de EM (385/0.74) = 343 Mcal ELL da dieta; perder 1 ECC fornece 343 Mcal ELL (≈490 kg de leite a 3.5% de gordura) [p.38]. (Verificação minha: 650×0.094 = 61.1 kg; ×6.3 = 384.9 Mcal; /0.74 = 520; ×0.66 = 343.)
- U4. Perda esperada de 0.5 ECC nos primeiros 60 dias pós-parto [p.38].
- U5. Atividade: caminhar em superfície plana custa ≈ 0.35 kcal ELL/kg PC/km (Brosh 2006, 2010; Aharoni 2009). Exemplo do livro: centro de ordenha a 200 m, vaca 650 kg, 3 ordenhas/d → ~0.3 Mcal/d (≈2% da mantença) [p.34]. Verificação: 0.35×650×(0.2 km × 2 sentidos × 3) = 273 kcal = 0.27 Mcal/d. Mantença já inclui atividade normal de confinamento [p.34]. Pastejo: Cap. 13.
- U6. Estresse por frio: queda média de 1.8 pontos percentuais na digestibilidade da MS por cada 10 °C abaixo de 20 °C (Young 1976) — só discussão [p.34].
- U7. Eficiência energética (ilustrativa): vaca com leite a 3× a mantença usa 25% da ingestão de ELL para mantença e 75% para leite; a 4×, 80% para leite. Vaca média opera a ~3× mantença [p.41].

### 3.5 Parâmetros e tabelas

**Tabela 3-1** [p.27] — Proporção de amido digestível basal (dStarch_Starch_base). Imagem conferida (OCR "0.9]" = 0.91 corrigido). 16 linhas:

| Alimento | dStarch_Starch_base |
|---|---|
| Padrão | 0.91 |
| Grão de milho, seco, moagem fina (<1,250 µm) (nota b) | 0.92 |
| Grão de milho, seco, moagem média (1,500 a 3,250 µm) | 0.89 |
| Grão de milho, seco, moagem grossa (>3,500 µm) | 0.77 |
| Grão úmido de milho, moagem fina (2,000 µm, média = 1,450 µm) | 0.96 |
| Grão úmido de milho, moagem grossa (>2,500 µm, média = 3,630 µm) | 0.90 |
| Grão de milho, floculado | 0.94 |
| Grão de sorgo, seco, moído | 0.83 |
| Grão de sorgo, seco floculado | 0.94 |
| Silagem de milho < 30% MS | 0.91 |
| Silagem de milho 32–37% MS | 0.89 |
| Silagem de milho >40% MS | 0.85 |
| Silagem de sorgo (nota c) | 0.85 |
| Cevada, prensada | 0.94 |
| Cevada, moída | 0.91 |
| Trigo | 0.93 |

Notas: (a) coeficientes derivados de experimentos, revisões e metanálises com vacas em lactação (Bal et al. 1997; Cammell et al. 2000a,b; Firkins et al. 2001; Ferraretto et al. 2013). (b) devido à escassez de dados, a classificação de tamanho de partícula do milho não é contínua; para tamanhos não listados, extrapolações podem ser usadas (note-se a lacuna entre 3,250 e 3,500 µm, e entre 1,250 e 1,500 µm). (c) baseado em dados de bovinos de corte (Gutierrez et al. 1982; Hart 1987) [p.27].

**Tabela 3-2** [p.32] — Parâmetros energéticos da reanálise de Beltsville (Moraes et al. 2015), 7ª edição e edição atual (colunas: 1963–1995 | 1974–1995 | 7ª ed. | 8ª ed.). Imagem conferida.

| Parâmetro | 1963–1995 | 1974–1995 | 7ª Edição | 8ª Edição |
|---|---|---|---|---|
| EM para mantença (Mcal/kg^0.75 PC/d) | 0.14 | 0.16 | 0.13 | 0.15 |
| ELL para mantença (Mcal/kg^0.75 PC/d) | 0.086 | 0.10 | 0.080 | 0.10 |
| Eficiência EM→ELL | 0.63 | 0.66 | 0.64 | 0.66 |
| EM→ER durante a lactação | 0.70 | 0.74 | 0.75 | 0.74 |
| ELL→ER durante a lactação (nota b) | 1.11 | 1.12 | 1.17 | 1.12 |
| ER→ELL (nota b) | 0.89 | 0.89 | 0.82 | 0.89 |
| EM→ER quando seca (nota b) | (vazio) | (vazio) | 0.60 | 0.60 |
| ELL→ER quando seca (nota b) | (vazio) | (vazio) | 0.94 | 0.91 |

Notas [p.32]: (a) toda exigência de energia deve ser convertida em ELL dietético para uso no modelo; ELL de mantença = EM × conversão EM→ELL; ER = energia retida (tecidos acumulados ou perdidos). (b) A ELL exigida para ER durante lactação ou quando seca = (EM→ER)/(EM→ELL); como a EM é convertida em tecido mais eficientemente que em leite, os valores são >1 (menos de 1 Mcal de ELL do alimento para acumular 1 Mcal de tecido); a menor eficiência para vacas secas é possivelmente devida à dieta de alta fibra (maior calor de fermentação, termogênese induzida pela dieta). Conferência interna: 0.74/0.66 = 1.12; 0.60/0.66 = 0.91.

**Tabela 3-3** [p.35] — Comparação de exigências de gestação NRC 2001 vs modelo atual (peso do bezerro ao nascer = 44 kg). Imagem conferida (corrigido pela imagem: OCR leu "14", "54", "215").

| Dias de gestação | ELL gestação NRC 2001 (Mcal/d) | ELL gestação Atual (Mcal/d) | PB gestação NRC 2001 (g/d) | PB gestação Atual (g/d) |
|---|---|---|---|---|
| 50 | 0 | 0.04 | 0 | 3 |
| 100 | 0 | 0.1 | 0 | 13 |
| 150 | 0 | 0.5 | 0 | 43 |
| 200 | 2.7 | 1.4 | 199 | 125 |
| 220 | 3.0 | 2.0 | 245 | 185 |
| 250 | 3.4 | 3.5 | 306 | 320 |
| 275 | 3.8 | 5.4 | 357 | 489 |

Nota: proteína detalhada no Cap. 6. Em um período seco de 60 dias a exigência total é essencialmente igual entre NRC 2001 e o novo modelo; menor longe do parto e maior perto do parto no modelo novo [p.36].

**Constantes consolidadas (todas com página):**

| Constante | Valor | Pág. |
|---|---|---|
| Calor de combustão: amido; AG; FDN; MOR; PB; EPBNNPs (Mcal/kg) | 4.23; 9.4; 4.2; 4.0; 5.65; 0.89 | p.25–26 |
| Base de digestibilidade (IMS/PC; amido) | 3.5% do PC; 26% | p.24,26,28 |
| dROM_ROM_base; dFA_FA_base | 0.96; 0.73 | p.27 |
| MFCP (a NDF=30%); fMCP; efROM (g/kg IMS) | 15.6; 16.5; 34.3 | p.30 |
| Energia fecal endógena total (Mcal/kg IMS) | 0.318 (0.088+0.093+0.137) | p.30 |
| N urinário → energia (Mcal/g N) | 0.0146 | p.31 |
| EM→ELL | 0.66 (IC 95% 0.64–0.69) | p.31 (corrigido na verificação) |
| Mantença ELL (Mcal/kg^0.75) | 0.10 (±0.06) | p.32 |
| Calor de combustão gordura, proteína verd., NNP-PB, lactose do leite (kcal/g) | 9.29; 5.71; 2.21; 3.95 | p.33 |
| Lactose default (kg/kg leite) | 0.0485 | p.33 |
| Duração da gestação | 280 d | p.35 |
| Peso GrUter ao parto / peso bezerro; Uter ao parto / peso bezerro | 1.825; 0.2288 | p.35 |
| Taxa de involução uterina; assíntota do útero | 0.2/d; 0.204 kg | p.35 |
| Energia do tecido uterino gravídico; eficiência EM→gestação | 0.882 Mcal/kg; 0.14 | p.36 |
| Composição do ganho/perda de PCV (ECC 2–4) | 62.2% gordura, 27.6% água, 8.1% proteína, 2.1% cinzas; 6.3 Mcal/kg | p.38 |
| Calor de combustão gordura corporal; proteína corporal (Mcal/kg) | 9.4; 5.55 | p.38 |
| Mudança de PC por unidade de ECC | 9.4% do PC | p.37 |
| Digesta | 5.2×IMS (18% do PC a 3.5%); 15% do ganho em novilhas, 18% em vacas imaturas | p.37,39 |
| Eficiência EM→ELg; ELL→ELg | 0.40; 0.61 | p.39 |
| Custo de caminhada em piso plano | 0.35 kcal ELL/kg PC/km | p.34 |
| Moraes: mantença aparente por período (Mcal/kg^0.75) e EM→ELL | 1963–73: 0.073 (0.60); 1974–83: 0.087 (0.62); 1984–95: 0.122 (0.69) | p.32 |
| Outros estudos de ELm (Mcal/kg^0.75, com EM→ELL 0.66) | 0.096 (Kirkland e Gordon 1999), 0.09 (Birkelo 2004), 0.11 (Xue 2011), 0.11 (Dong 2015), 0.14 (Foth 2015), 0.10 (Morris e Kononoff 2021); 0.098 vaca não lactante em jejum (Birnie 2000); calor de jejum de vacas secas 0.073 (Flatt 1965) | p.32 |

**Figuras (conteúdo qualitativo):** Fig. 3-1 [p.25] fluxograma: alimento → frações (FDN, amido, AG, MOR [×0.96], PDR, PNDR, com ajuste IMS/PC em FDN e amido) → frações digeríveis (FDNd, Amidod, AGsd, MORd, EPBNNPs, PBd) → ED, subtraindo MORfe e PBef; ED → EU e Egas → EM → ELL. Fig. 3-2 [p.28] efeito do amido na ED (gráfico, ED 2.6–3.1 Mcal/kg MS para amido 15–35%; dieta de teste 16% PB, 3% AG, 14% MOR, 5% cinzas, FDN+amido 62%, dFDN base 0.46 e dAmido 0.91, digestibilidades aparentes 0.65 PB, 0.73 AG, 0.70 MOR): ED sem ajuste cresce com amido; com ajuste (3-5a/3-5b) o ganho é menor; ingestão afeta menos a ED que o amido. Fig. 3-3 [p.36] escala de ECC 1–5 (Edmonson et al. 1989; M'hamdi et al. 2012): extremamente magra, esqueleto visível, esqueleto e cobertura equilibrados, esqueleto menos visível, extremamente gorda; vértebra dorsal, vista traseira dos íleos, vista lateral íleo–ísquio, cavidade base da cauda–ísquios.

### 3.6 Regras de decisão / restrições para o otimizador
- ED por alimento só vale nas condições basais (IMS 3.5% PC; 26% de amido); **EM e ELL só são válidas para a dieta total**; ELL de alimentos individuais não é fornecida [p.24–25,31]. O modelo é "para avaliação, deve ser usado com cautela para formulação" [p.23]. Implicação: o otimizador não pode usar ELL por ingrediente linear; deve avaliar a dieta completa a cada iteração (equações não lineares em IMS/PC e amido).
- Premissa de validade da ED: PDR adequada e FDN de forragem suficiente; se PDR for insuficiente o valor energético é superestimado; FDN de forragem baixa (risco de acidose) reduz digestibilidade de FDN e energia vs estimado; parte do efeito está no ajuste do amido [p.26]. Recomendações de FDN/FDNf e PDR: Caps. 5 e 6 (fora do escopo).
- Dietas para animais com IMS restrita (especialmente novilhas): as equações podem subestimar a digestibilidade de FDN, amido, AG e MO [p.29].
- Balanço de energia = ingestão de ELL − (mantença + lactação + gestação + crescimento) [p.39]. A reserva corporal mobilizada fornece 5.6 Mcal ELL/kg de perda de PC; o ganho de reservas custa 5.6 (lactação) ou 6.9 (seca) Mcal ELL/kg [p.38].
- Dieta para vaca seca: ED/ELL ≈ 10% maior que no NRC 2001 (1.4 → 1.55 Mcal ELL/kg); exigência de uma vaca seca de 700 kg a 20 d pré-parto +30%; balanço ELL de vaca seca −2.8 Mcal/d vs sistema antigo [p.39].
- Partição de energia (qualitativa, não em equação): amido alto no início da lactação ajuda PL máxima com mínima perda de reservas; no fim da lactação, com reservas recuperadas, trocar amido por fibra digestível evita ganho excessivo; substituir milho por casca de soja aumenta gordura do leite e reduz PC; amido alto aumenta risco de depressão de gordura do leite (CLA trans-10 cis-12) [p.40–41]. Efeitos de dieta na partição "não podem ser quantificados" no modelo [p.41].
- Eficiência alimentar: maximizar leite/alimento raramente é objetivo valioso; dietas ricas em gordura, amido e proteína e baixas em fibra elevam leite:alimento mas não necessariamente lucro, saúde e sustentabilidade [p.41].

### 3.7 Lógica e fluxo (ordem de cálculo)
1. Composição do alimento (Cap. 19/18): FDN, amido, AG, PB, cinzas, lignina ou DIVFDN, PDR, PNDR (e PNDRd), NNP suplementar → MOR por diferença (Eq. 3-1) → EB (Eq. 3-2, opcional).
2. IMS (Cap. 2: Eq. 2-1 ou 2-4/2-3) → IMS_PC = IMS/PC.
3. Digestibilidades: base (3-3a ou 3-3b; Tabela 3-1; 0.96; 0.73; Eq. 3-4) → ajuste por IMS_PC e amido (3-5a, 3-5b). Proteína sem ajuste.
4. Fezes endógenas: MFCP (3-6a), fMCP (3-6b, precisa de PB microbiana do Cap. 6), efROM = 34.3 g/kg.
5. ED da dieta (Eq. 3-8). Opcionais para comparar com dados: Eq. 3-7a/b/c.
6. Gás (3-9) e urina (3-10a/b; precisa de PB do leite, ganho de proteína corporal; adCP de 3-7b) → EM (3-11) → ELL da dieta (3-12).
7. Exigências em ELL: mantença (3-13), lactação (3-14a/b/c × PL), gestação (3-15 a 3-18; DayGest, peso do bezerro), reservas (3-19a/b/c; ΔECC × 9.4% do PC × fator), crescimento de frame (3-20; Cap. 11 detalha), atividade (0.35 kcal/kg/km), pastejo (Cap. 13).
8. Balanço = ELL ofertada (IMS × NEL_DM) − soma das exigências. Para novilhas e bezerras as exigências são em EM (Caps. 10–11); para elas ED→EM vem desta seção.
Dependências de outros capítulos: Cap. 4 (Tabela 4-1, AG de suplementos de gordura); Cap. 6 (PDR, PNDR, PNDRd, MCP, PB do leite, proteína de gestação, proteína de ganho); Cap. 14 (equação de metano, base da Eq. 3-9); Cap. 11 (ganho de frame, composição); Cap. 12 (IMS de seca; ECC e exigências na transição); Cap. 13 (pastejo); Cap. 18 (ensaios de FDN, lignina, DIVFDN); Cap. 19 (composição e Tabela 19-1, ED basal).

### 3.8 Limitações, incertezas e mudanças vs. NRC 2001
Mudanças declaradas [p.23–24,31]: (i) o desconto de digestibilidade com a ingestão era grande demais no NRC 2001 (Huhtanen 2009; White 2017; de Souza 2018) e estava confundido com o teor de TDN/amido; agora o desconto vale só para FDN e amido, com forma linear; (ii) o desconto era aplicado à dieta inteira; (iii) PB tinha EM superestimada (usando ED 5.65 vs 4.2 do amido) — agora a proteína usa o sistema proteico; (iv) interceptos negativos nas conversões ED→EM e EM→ELL (subestimavam dietas de baixa energia) removidos; (v) nível de ingestão era múltiplo da mantença (circularidade) — agora IMS/PC; (vi) CNF e TDN abandonados; (vii) base de ED passou de vaca em mantença (~1.2% do PC) para IMS = 3.5% do PC e 26% de amido; (viii) ED→EM calculado de urina e metano da dieta/animal (eficiência variável), com ELL = 0.66×EM sem correção de gordura. Exigências: mantença 0.08→0.10 Mcal/kg^0.75; eficiência EM→leite 0.64→0.66; crescimento simplificado (relativo a PCMat, composição do ganho não muda com dieta); composição da variação de ECC constante; atividade atualizada; gestação refeita com função logística e peso do bezerro como entrada [p.31,35]. Comparação novo vs 2001: ELL da dieta de lactação +8% em média (6 a 12%; 1.53–1.63 → 1.65–1.77 Mcal/kg), maior a alta ingestão (+10%) e em dietas ricas em amido; secas ~+10% (1.4 → 1.55); exigências +8% em média (+6% para vaca 650 kg a 55 kg de leite; +11% a 30 kg); balanço de ELL lactante +0.6 Mcal/d (~1.5%) [p.39].
Limitações admitidas: sem ajuste por fermentabilidade do amido, tamanho de partícula da fonte de FDN, PDR deficiente [p.28–29]; digestibilidade de MOR e proteína não afetada pela IMS (pouco dado) [p.27,29]; dados de digestibilidade vs IMS vêm de variação entre vacas ad libitum, não de experimentos delineados (como Tyrrell e Moe 1975) [p.29]; DIVFDN vs lignina: dados in vivo insuficientes [p.26]; **estresse por calor não incluído** em mantença (7–25% por NRC 1981; Kurihara 1996: calor de jejum +5%, EM de mantença +10% a 36 vs 18 °C; Lamp 2015 não achou aumento de mantença com THI 75) [p.34–35]; estresse por frio pouco relevante em vacas leiteiras alojadas (digestibilidade −1.8 pontos/10 °C abaixo de 20 °C) [p.34]; mantença não ajustada por ECC nem por estado de lactação nem raça (decisão consciente; Birnie 2000: mesmo ELm/vaca com ECC 1.3 vs 4.7 e PC 467 vs 692 kg; ajustado a ECC 3.0 assumindo 1 ECC = 10% do PC é o mesmo por PCM) [p.33–34]; NASEM (2016) corte usaria 0.095×PCM, fator de raça 1.2 e mantença 20% maior em lactantes — **não** adotado (custo de órgãos viscerais atribuído à perda de calor incremental EM→ELL) [p.33]; eficiências diferenciais EM→componentes do leite não adotadas [p.34]; dados de ECC×PC×digesta×composição escassos, vacas de transição mascaram a perda real de PC por enchimento do trato [p.37]; composição do ganho de novilhas não responde à taxa de ganho (dados insuficientes) e ECC não é usado em novilhas [p.38–39]; vacas em primeira e segunda lactação: o modelo computacional aceita simultaneamente ganho de frame e variação de ECC, novilhas só frame [p.39]. Eficiência alimentar global (insumos humanos vs não humanos, ambiente) só discussão [p.40–41].

### 3.9 Conceitos e evidências relevantes (curtos)
- Unidade ELL: única unidade para mantença e leite; ED e EM do modelo são valores esperados para a vaca e a dieta (não máximos potenciais) [p.23]. Eficiências: EM→mantença 0.62 e EM→leite 0.64 (Beltsville histórico), 0.66 com os últimos 20 anos (Moraes) [p.23].
- Mantença do último período da reanálise (1984–95) subiu para 0.122; justificativa: vacas modernas produzem 3× mais leite que nos anos 1960 e têm maior taxa metabólica; ELm antigo 0.080 = 0.073 (jejum) + 10% de atividade [p.32].
- Valores de ELm vs lactantes/secas: o comitê reconhece que lactantes têm maior massa de fígado e vísceras mais ativas, mas atribui isso ao custo da produção de leite [p.33].
- Ganho de frame vs reservas vs prenhez: frame = crescimento esquelético normal com ECC constante e não prenhe; reservas = tecidos perdidos/acumulados (principalmente lipídio); prenhez = feto, placenta, mama. Todas as exigências de crescimento do modelo assumem ganho de PC = ganho de frame [p.36–37].
- Valores do ECC: sistema de 5 pontos (Wildman 1982; Edmonson 1989, oito locais); só dois locais ("entre íleos" e "entre íleos e ísquios") tiveram o menor erro de avaliador [p.37]. ECC está inversamente associado à IMS [p.37].
- Início da lactação: vaca mobiliza reservas; vacas gordas têm menos IMS e mais risco de distocia e doenças; magras têm menos leite e emprenham tarde [p.37].
- Efeito da ingestão na ED: ED de uma dieta formulada com valores de tabela (Cap. 19) provavelmente difere do estimado pelo modelo, mesmo com a mesma composição [p.25].
- Valores de MS na gordura: AG nos TG incluem uma molécula de água na hidrólise (massa de AG+glicerol = 106% da massa de TG) [p.24].
- Eficiência alimentar: eficiência máxima em ~21,000–24,000 kg/ano para Holandesas de PCMat 625 kg (VandeHaar 1998); mantença 25% maior exige produção 25% maior para atingir máxima eficiência; seleção para RFI negativo [p.41].

### 3.10 Dúvidas / riscos de OCR (⚠ itens consolidados para conferência humana)
Ver lista consolidada abaixo (§ Itens ⚠).

---

# Itens ⚠ (conferência humana) — consolidado

1. ⚠ **Eq. 2-1 [p.14]**: parênteses desbalanceados no original; a transcrição usa `[(3.7 + Paridade*5.7) + …] * [1 − (0.212 + Paridade*0.136)*e^(−0.053*DIM)]`. O fator "e^(−0.053×DIM)" no livro não tem o parêntese de fechamento. Interpretação estrutural, sem fonte externa.
2. ⚠ **Eq. 3-3a [p.26]**: impresso `{0.75 × NDF_DM − Lignin_DM) × [1 − (Lignin_DM / NDF_DM)^0.667]} / NDF_DM` (parênteses desbalanceados). Dúvida sobre se é `0.75*(NDF−Lignin)` ou `(0.75*NDF − Lignin)`. Leitura mais provável: `0.75*(NDF−Lignin)`. Para NDF 30 e lignina 3.5% dá 0.504 vs 0.482 na outra leitura. Tipo de lignina (ex.: ácido sulfúrico) não informado.
3. ⚠ **Eq. 3-17b [p.36]**: impresso "GrUter_Wt_Gain =_t −0.2 × DayLact × (Uter_Wt − 0.204)", com subscrito "t" solto; a derivada de 3-16b seria −0.2×(Uter_Wt−0.204). Não é informado como a energia/proteína liberada na involução entra no balanço (Eq. 3-18 é de gestação).
4. ⚠ **Eq. 3-9 [p.30–31]**: unidades mistas (DMI kg/d; FA e dNDF em % MS); dNDF_DM não é definida explicitamente (assumido = NDF_DM × dNDF_NDF). Conferir com Cap. 14 (equação de metano).
5. ⚠ **Eq. 3-7b/3-7c [p.30]**: o livro diz "todas as variáveis em kg/d", mas MFCP e fMCP são calculadas em g/kg IMS (Eq. 3-6) e RDP/dRUP/CP em % MS (Eq. 3-4, 3-8). Conversões de unidades devem ser explicitadas na implementação.
6. ⚠ **Tabela 3-2 [p.32]**: células em branco (1963–1995 e 1974–1995) nas linhas "quando seca"; valor 0.82 (ER→ELL, 7ª ed.) não é o inverso de 1.17 (=0.85); transcrito como impresso. Valores 0.94 e 0.91 conferem com 0.60/0.64 e 0.60/0.66.
7. ⚠ **EBG/ADG**: o texto dá 0.85 (novilhas, p.39) e 0.82 (digesta 18% para vacas, p.37 e p.39); a equação 3-20 usa "EBG/ADG" sem valor numérico explícito no equacionamento; confirmar no Cap. 11 como EBG é obtido.
8. ⚠ **Mantença em fêmeas jovens**: a Eq. 3-13 é "de bovinos leiteiros adultos"; mantença de novilhas e bezerras é em EM (Caps. 10 e 11), não lida aqui.
9. ⚠ **Eq. 3-10a**: condição "não está em lactação e dentro de 60 dias pré-parto" é ambígua (E ou OU); interpretada como E (seca e ≤60 d pré-parto) [p.31].
10. ⚠ **Estatísticas Eq. 2-1 [p.14]**: "erro médio, porcentagem do MSE = 6.9" e "viés de intercepto % do MSE = 2.28" copiados como impressos; unidade do RMSEP 2.61 e do RQMEP 1.55 não explicitada (presumido kg/d).
11. ⚠ **p.4–5**: OCR corrompeu a definição de IA e siglas (RDI/IDR/NMT/MT/MNIT) da tradução; recuperado pela imagem p.5.
12. OCR corrigido pela imagem (registrado): Eq. 3-16a (9.0243→0.0243); Tabela 3-3 (14→1.4; 54→5.4; 215→275); p.24 "IMS = 3.59% do PC"→3.5%; p.11 "77 das 25"→"7 das 25"; Tabela 3-1 ("0.9]"→0.91); Eq. 3-6a (rótulo "MFCE"→MFCP). Valores de tabelas e equações do cap. 3 foram todos conferidos nas imagens p.24–40.

**Itens do escopo pedido que NÃO estão nas p.4–44:** equação de IMS para vacas secas e pré-parto (Cap. 12); exigências de mantença/crescimento de novilhas e bezerras em EM (Caps. 10–11); atividade em pastejo (Cap. 13); equação de metano completa (Cap. 14); Tabela 4-1 (Cap. 4); Tabela 19-1 (Cap. 19). Esses dependem de outros blocos.

---

COBERTURA: páginas lidas 1–44 (texto OCR integral de todas, incluindo referências p.6–7, 19–22, 41–44, que não foram detalhadas por serem apenas bibliografia). Imagens conferidas: p.5, 8, 9, 11, 12, 14, 15, 16 (com recortes dpi 250), 18, 24, 25, 26 (recorte dpi 250), 27–40 (p.35 com recortes dpi 300), 37; p.10, 13, 17, 19–23, 41–44 só por OCR (texto corrido/referências, sem equações). O que ficou de fora: detalhes bibliográficos; estatísticas de estudos citados no texto narrativo além dos números transcritos; Fig. 3-2 e 3-3 descritas qualitativamente (valores do gráfico não extraídos).

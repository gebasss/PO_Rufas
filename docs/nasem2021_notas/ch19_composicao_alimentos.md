# NASEM 2021 (Bovinos Leiteiros, 8ª ed., trad. PT-BR) — Notas técnicas: Cap. 19 Composição Nutricional dos Alimentos

**Cobertura:** Capítulo 19, páginas impressas 393–465 (texto 393–396; Tabela 19-1 pp. 397–442; Tabela 19-2 pp. 443–458; Tabela 19-3 pp. 459–464; Referências p. 465). Página do PDF = impressa + 20.
**Usado diretamente no modelo? Cap. 19: SIM** — é a BIBLIOTECA DE ALIMENTOS (entradas de composição por ingrediente). Quase só tabelas; o texto (pp. 393–396) fixa a metodologia, as convenções de unidade/base e 4 equações de ED base (Eq. 19-1 a 19-4).

> Convenções de leitura: decimal = ponto; milhar = vírgula (no arquivo de dados abaixo, N sem separador de milhar). "MS" = matéria seca. `⚠` = item para conferência humana. `(corrigido pela imagem)` = OCR e imagem divergiam; vale a imagem. As páginas de texto 394 (coluna direita inteira) e 395 foram lidas **da imagem** porque o OCR da p. 394 perdeu a coluna direita.

---

## 1. Papel no simulador
Fornece, para cada alimento (ingrediente) selecionável na dieta: composição de macronutrientes, frações de carboidrato/fibra, frações de proteína (A, B, C, Kd, PNDR, dPNDR), ED padronizada ("ED base"), minerais, e (Tab. 19-2) perfis de aminoácidos e de ácidos graxos; a Tab. 19-3 dá a composição e o coeficiente de absorção das fontes minerais inorgânicas. A dieta é uma combinação linear (ponderada pela MS) destes valores; os cálculos de energia (Cap. 3), proteína/AA (Cap. 6), AG (Cap. 4) e minerais (Cap. 7) consomem estes campos.
O texto diz que a "biblioteca eletrônica de alimentos" do modelo também traz suplementos comerciais com campos **em branco** (AA protegidos da degradação ruminal, minerais orgânicos) para o usuário preencher [p.395].

## 2. Metodologia COMPLETA (texto pp. 393–396)

### 2.1 Fonte dos dados [pp.393–394]
- Histórico: o NRC publica tabelas de composição desde a década de 1950 (NRC 1945, 1956, 1958, 1971, 1982; Fontenot et al., 1995). Dados deste relatório preparados com o Comitê de Composição de Alimentos do Programa Nacional de Nutrição Animal (NRSP-9, iniciado em 2010; https://animalnutrition.org) [p.393].
- Rede Internacional de Centros de Informação listou 17,000 alimentos em 1978 (Tran e Lapierre, 1997); o comitê construiu tabelas só para alimentos comuns de bovinos leiteiros da América do Norte. Umidade, processamento, teor e prática de colheita **refletem-se no nome** [p.393].
- **Tabela 19-1:** dados doados por 4 laboratórios comerciais: Cumberland Valley Analytical Services (Waynesboro, PA; antes Hagerstown, MD), Rock River Laboratory (Watertown, WI — o OCR leu "WD"; corrigido pela imagem), Dairyland Laboratories (Arcadia, WI), Dairy One (Ithaca, NY). **Cinco anos** de dados solicitados a cada laboratório na primavera de 2015 [p.393].
- **Tabela 19-2** (AA e AG individuais): fornecida pela Cornell University (Higgs et al., 2015). Dados de AA **não corrigidos** para contaminação microbiana de resíduos isolados usados para estimar o escape ruminal (Paz et al., 2014) [p.393]. Rodapé da 19-2: fonte única, por isso N e DP não são apresentados [p.458].
- Pequeno número de valores vem de outras fontes (literatura, NASEM Beef 2016, dados não publicados de universidades): **identificáveis quando há média sem N e sem DP** [p.393].
- Os métodos podem não seguir todos os métodos do Cap. 18. Dados de química úmida e de NIRS **não puderam ser diferenciados** e foram usados juntos; **dados de minerais são só de química analítica** [pp.393–394].
- Nomes e classificações são exclusivos do relatório (não seguem o sistema internacional de nomes e números de rações, Harris et al., 1980), mas tentam ser consistentes com AAFCO (2016) [pp.393–394].

### 2.2 Classes e tipos de alimento [p.393]
- **Classe (12):** proteína animal; ração para bezerros; subproduto/outros; fonte de energia; forragem de grãos; forragem de gramíneas/leguminosas; sabões de cálcio; óleo; nitrogênio não proteico; proteína vegetal; pastagem; vitaminas/minerais.
- **Tipo (3):** forragem seca; forragem úmida; concentrado.
- "Este esquema de classificação é usado em várias equações dentro do modelo" [p.393]. **⚠ Importante:** classe e tipo **NÃO são impressos** em nenhuma tabela do Cap. 19 (só nome e código NRC16Fxxx). O implementador terá de atribuir classe/tipo por alimento (a partir das regras dos Caps. 6, 3, 4 etc.) — ver parecer na seção 9.
- Cálculo de PNDR depende da classificação do alimento ("calculos diferentes com base na classificação") [p.396].

### 2.3 Análise estatística e geração dos dados [p.394 — texto da coluna direita lido da imagem]
1. Laboratórios classificam alimentos pelo nome fornecido pelo usuário; por ambiguidade de nomes, "geralmente são classificados incorretamente". Por isso usou-se método estatístico para rastrear e classificar (Yoder et al., 2014), modificado para rodar em **Python (v. 2.7; Tran et al., 2020)**.
2. **2.761 × 10^6 registros** dos 4 laboratórios usados para desenvolver os procedimentos e construir a tabela.
3. Nomes e variáveis padronizados; pontos obviamente errados e amostras duplicadas removidos.
4. Histogramas e análise univariada para remover **outliers com nutrientes-chave fora de média ± (3.5 × DP)**. Nutrientes-chave = analitos usados na análise de agrupamento dentro do laboratório: normalmente MS, PB, FDN, cinzas e, às vezes, lignina, amido, GB e hemicelulose. Para alguns alimentos, **carboidratos solúveis em etanol (extração 80 %)** entraram no agrupamento (embora CSA esteja listado na 19-1).
5. Duas análises multivariadas (componentes principais + agrupamento) eliminaram outliers adicionais e identificaram subpopulações: **amostras com escore de componente principal > 3.5 × DP do escore médio foram removidas**.
6. Análise de agrupamento (cluster) para identificar subpopulações de alimentos dentro de um mesmo alimento; em alguns casos usou-se a experiência de membros do comitê. Analitos usados descritos em Tran et al. (2020). A etapa de agrupamento foi programada em Python para rodar o **SAS** automaticamente; todas as etapas foram automáticas, seguidas de **avaliação manual da matriz de correlação de Pearson** e dos agrupamentos resultantes.
7. Os dados de entrada de cada um dos 4 laboratórios continham **42, 94, 162 e 270 alimentos** e **28 a 37 nutrientes**. O banco resultante tem **173 alimentos (1.489 × 10^6 registros)**; **111 alimentos tinham mais de um agrupamento/subpopulação**. (As tabelas impressas têm 184 entradas porque incluem também valores de outras fontes — ver 3.1.)
8. A soma dos analitos não totaliza necessariamente 100 % (contaminação da FDN por cinzas; tamanhos de amostra distintos por nutriente). Proteínas de origem animal, ricas em PB, geralmente somam **> 100 %**: fator N × 6.25 superestima a proteína real (Mariotti et al., 2008).
9. **Estatísticas de variação:** o texto diz que a novidade é fornecer mínimo, máximo, percentil 10 e percentil 90, e orienta avaliar (média, DP, mín., máx., P10, P90) antes de usar a média. **Nas tabelas impressas só há Média, DP e N**; mín./máx./P10/P90 **não aparecem** (não informado se existem na biblioteca eletrônica). Exemplo do texto: farelo de alfafa, Fe = 951 mg/kg, DP 680; mínimo a 1.4 DP da média, máximo a 4.1 DP; **mediana 726 mg/kg (~24 % abaixo da média)** → distribuição assimétrica [p.394]. Verificado: Fe farinha de alfafa = 951 / 680.4 / 288 [p.397].
10. Usaram-se **médias para todos os nutrientes** por consistência, embora algumas variáveis não sejam normais [p.393]. N pode diferir entre analitos dentro do mesmo alimento (fonte de inconsistência por covariância; Sauvant e Ponter, 2004) [p.394].
11. Fontes de variação listadas: metodologia/variação analítica, subamostragem, variedade, clima, solo, tempo de armazenagem, processamento (St-Pierre e Cobanov, 2007; St-Pierre e Weiss, 2015). As tabelas "não se destinam a substituir testes analíticos" [p.394].

### 2.4 Convenções de unidade, base e células vazias [pp.393–394, 442]
- **Todos os dados em base livre de umidade (% MS ou mg/kg MS) exceto a própria MS, que é % da matéria natural** [pp.393–394].
- Célula em **branco abaixo da média**: sem dado. **"0"**: analito medido, mas concentração zero/abaixo do limite de detecção. **N e DP em branco**: média de fonte única [nota a, p.442].
- **Itálico** nas linhas "PNDR, % PB" e "ED base, Mcal/kg" = valor **calculado** conforme o texto (notas c e i, p.442). As demais linhas de fração A/B/C, Kd e dPNDR vêm de compilação da literatura.
- "ED base" = ED padronizada; **valores de energia dependem da composição da dieta e da ingestão, não do ingrediente**; o modelo recalcula ED, EM e ELL da dieta com as equações do Cap. 3 [p.395].
- Arredondamento: não há regra impressa. Observado nas imagens: MS, cinzas, PB, FDA, FDN, amido, CSA, minerais macro (% MS: 2 casas), AG/GB (2 casas na maioria dos casos), PNDR/dPNDR/frações A, B, C inteiros, Kd 1 casa, ED 2 casas, Fe/Mn/Zn mg/kg inteiros (média) com DP 1 casa, Cu/Mo 2 casas; Tab. 19-2 sempre 2 casas (exceção: bagaço de tomate, 1 casa [p.456]). N com separador de milhar vírgula (às vezes ausente/vírgula decimal por erro: "2,011.07" [p.440, ⚠]).
- Co, Cr e I **não** estão na 19-1 (dados confiáveis indisponíveis). Mo só "em referência à disponibilidade de Cu" [p.396].
- CSA (carboidrato solúvel em água) e proteína solúvel: listados **só para referência**; **não usados** em nenhum cálculo do modelo. GB também não é usada (usa-se AG total) [pp.395–396]. Lignina e cinzas são usadas **só para estimar energia** (lignina majoritariamente por ácido sulfúrico — LDA) [p.395]. Fibra bruta não é apresentada [p.395]. CSA faz parte da fração MOR [pp.395–396].
- Valores de FDA, FDN, CSA, amido e lignina de **proteínas animais foram ajustados para ZERO** (detecção = artefato analítico); por isso a composição de uma mistura contendo proteína animal por análise direta pode diferir da calculada pela 19-1 [p.396]. (Verificado: farinha de sangue FDA/FDN/lignina/amido/CSA = 0.0 [p.402]; farinha de penas idem [p.416].)
- **MOR (matéria orgânica residual)** = 100 − (cinzas + AG + PB + FDN + amido); pode ser negativa em raras situações e foi mantida "para compensar parcialmente a energia fornecida pelo excesso de nutrientes calculado" [p.395].

### 2.5 Valores faltantes: como são gerados/derivados [pp.395–396]
- **AG total (AGT):** quando há dado real de laboratório, usa-se; senão **AGT ≈ GB − 1** (sem N nem DP); para **forragens**, essa estimativa é imprecisa e usa-se a regressão **AGT = GB × 0.5678** (Daley et al., 2018) (média reportada sem N/DP) [p.395].
- **PNDR (% PB)** de cada alimento: calculado como no Cap. 6 para **vaca-padrão de 650 kg consumindo 23 kg de MS (3.5 % do PC)**, com cálculos diferentes conforme a classe do alimento; parâmetros A, B, C, Kd e **dPNDR (PNDRd)** vêm de valores compilados da literatura e outras fontes. **Quando faltavam frações, atribuíram-se as de alimentos comparáveis**; mesmos valores foram atribuídos a **todas as classes de maturidade** de uma forragem (diferenças de maturidade podem afetar mas faltam dados) [p.396]. Observável: ex. silagens de cevada (mat. média e vegetativa) têm A/B/C/Kd/PNDR/dPNDR idênticos [p.400]; todas as silagens de milho idem [p.411].
- **ED base:** calculada a partir dos dados médios de nutrientes (equações do Cap. 3 para alimentos gerais; Eq. 19-1 a 19-4 abaixo para lipídios, proteínas animais e açúcares/glicerol) [p.395].
- **Energia endógena (valor base):** IMS = 3.5 % PC, amido na dieta 26 %, FDN da dieta 30 %: PB fecal endógena = 15.6 g/kg MS = 0.088 Mcal/kg MS; PB bacteriana não digerida = 16.5 g/kg MS = 0.093 Mcal/kg (proteína microbiana média 1,875 g/d no conjunto de dados da equação de síntese microbiana, IMS média 22.7 kg/d); MOR endógena = 34.3 g/kg MS = 0.137 Mcal/kg IMS; **energia endógena total = 0.088 + 0.093 + 0.137 = 0.318 Mcal/kg IMS** [p.395] (este 0.318 é o termo subtraído em todas as Eq. 19-1 a 19-4).
- Valores com dados insuficientes (ex. proteína animal, sabão de cálcio, óleos) ficam em branco nas colunas de fibra/proteína [pp.402–403, 414–416].

### 2.6 Nomes, maturidade e agrupamento de forragens [p.396]
- Nomes comuns. Gramíneas de estação fria (C3) combinadas numa só classificação (composição de macronutrientes pouco varia entre espécies perenes; Cheney et al., 1993); leguminosas comuns (alfafa, trevo) numa só classificação (feno/silagem de leguminosas).
- Classes de maturidade determinadas por **análise de agrupamento**: imatura, meia-maturidade (Mat. Média) e madura. Forragens menos maduras tendem a menor FDN, mas condições de crescimento alteram; **não se usaram valores de corte fixos de FDN** (diferente da edição anterior) — há sobreposição de FDN entre classes.
- Forragens mistas gramíneas+leguminosas: separadas por **hemicelulose = FDN − FDA** (Van Soest et al., 1991): misturas de gramíneas (> 70 % gramíneas; **> 17 a 22 % hemicelulose**), proporções ~iguais (**> 13 a 17 %**) e principalmente leguminosas (> 70 %; **10 a 13 %**) (corrigido pela imagem: o OCR grafava "177%"). Maturidade das mistas também pela FDN.
- **Maturidade da silagem de milho estimada pela MS** (planta madura = MS maior; Wiersma et al., 1993).
- Soja: três produtos distintos na biblioteca: (1) farelo de soja extraído com solvente 48 % PB; (2) farelo de soja extrusado; (3) farelo de soja expellers (várias marcas de "expellers 48 % PB" não são diferenciadas). Extrusado tem muito mais gordura que o extraído com solvente (Giallongo et al., 2015) [p.396]. (O texto traduzido diz "óleo de soja pode ser obtido..." — erro de tradução; trata-se de soja/farelo.)

## 3. Esquema de cada tabela

### 3.1 Tabela 19-1 — "Composição Nutricional, Digestibilidade e Variabilidade de Alguns Alimentos Comumente Fornecidos às Vacas Leiteiras" [pp.397–442]
**Layout (importante para digitalização):** TRANSPOSTA — **alimentos nas COLUNAS (4 alimentos por página), analitos nas LINHAS (33 linhas)**. Cabeçalho por alimento: "Nome", "Cód. alimento" (NRC16Fn) e 3 subcolunas **Média | DP | N**. 46 páginas × 4 = 184 posições de alimento; **a p. 406 impressa é uma DUPLICATA da p. 407** (conteúdo idêntico, verificado na imagem); portanto o PDF contém **180 alimentos únicos** e **faltam 4 alimentos** (conteúdo da p. 406 original, ver seção 6.1 e ⚠ 1 da seção 10).

| # | Linha (rótulo PT) | Sigla/código usado nas notas | Unidade | Base | Definição / observação |
|---|---|---|---|---|---|
| 1 | MS, % matéria natural | MS | % da matéria natural | NATURAL (única) | matéria seca |
| 2 | Cinzas, % MS | CZ | % MS | MS | usada só p/ energia |
| 3 | PB, % MS | PB (CP) | % MS | MS | N×6.25; ureia = 281.0 (equivalente protéico); p/ proteína animal soma >100 % |
| 4 | Fração A, % de PB (b) | A | % PB | PB | fração A de desaparecimento ruminal (Cap. 6) |
| 5 | Fração B, % de PB (b) | B | % PB | PB | fração B (Cap. 6) |
| 6 | Fração C, % de PB (b) | C | % PB | PB | fração C (não degradável) (Cap. 6) |
| 7 | Kd de B, %/h (b) | KD | %/h | — | taxa de degradação da fração B |
| 8 | PNDR, % PB (c, itálico) | PNDR (RUP) | % PB | PB | **calculada** (vaca 650 kg, 23 kg MS) |
| 9 | dPNDR, % de PNDR (d) | DPNDR (PNDRd) | % da PNDR | PNDR | digestibilidade intestinal da PNDR |
| 10 | Proteína solúvel, % PB | PSOL | % PB | PB | **só referência**, não usada |
| 11 | PIDA, % MS (e) | PIDA | % MS | MS | proteína insolúvel em detergente ácido |
| 12 | PIDN, % MS (f) | PIDN | % MS | MS | proteína insolúvel em detergente neutro |
| 13 | FDA, % MS | FDA | % MS | MS | zero p/ proteína animal |
| 14 | FDN, % MS | FDN | % MS | MS | zero p/ proteína animal |
| 15 | DIVFDN48, % de FDN (g) | DIVFDN | % da FDN | FDN | digestibilidade in vitro da FDN, 48 h |
| 16 | Lignina, % MS | LIG | % MS | MS | majoritariamente LDA (ác. sulfúrico) |
| 17 | Amido, % MS | AMIDO | % MS | MS | |
| 18 | CSA, % MS (h) | CSA (WSC) | % MS | MS | **só referência**; parte da MOR |
| 19 | AG total, % MS | AGT (TFA) | % MS | MS | **usado**; real (lab) ou estimado GB−1 / GB×0.5678 (forragem) |
| 20 | Gordura bruta, % MS | GB (EE) | % MS | MS | reportada, **não usada** |
| 21 | ED base, Mcal/kg (i, itálico) | ED | Mcal/kg MS | MS | calculada; padrão (IMS 3.5 % PC, amido 26 %, FDN 30 %) |
| 22–28 | Ca, P, Mg, K, Na, Cl, S, % MS | CA, P, MG, K, NA, CL, S | % MS | MS | só química analítica |
| 29–33 | Cu, Fe, Mn, Zn, Mo, mg/kg MS | CU, FE, MN, ZN, MO | mg/kg MS | MS | Mo só p/ disponibilidade de Cu |

Rodapés [p.442, verificados na imagem]: (a) N = nº de amostras e DP = desvio padrão; célula em branco abaixo da média = sem dados; 0 = abaixo do limite de detecção; N e DP em branco = média de fonte única. (b) frações A, B, C e taxa Kd de B de desaparecimento ruminal de proteína. (c) itálico = valor calculado conforme o texto. (d) dPNDR = digestibilidade intestinal da proteína indegradável no rúmen. (e) PIDA. (f) PIDN. (g) DIVFDN48 = digestibilidade in vitro da FDN 48 h. (h) CSA = carboidrato solúvel em água. (i) padrão de ED; itálico = calculado.
Tradução: "Far." = Farinha (ex. "Far. Sangue" = Farinha de Sangue, confirmado pela Tab. 19-2).

### 3.2 Tabela 19-2 — "AA, AG Total, e Conteúdo de AG de Alguns Alimentos Comumente Fornecidos às Vacas Leiteiras" [pp.443–458]
**Layout:** alimentos nas COLUNAS, **2 blocos por página, 6 alimentos por bloco (12/página)**, 22 linhas por bloco; **sem DP nem N** (fonte única, Cornell). 15 páginas × 12 + 4 na p. 458 = **184 alimentos** (mesma contagem de 184 posições da 19-1).

| Linha | Sigla | Unidade | Base |
|---|---|---|---|
| PB, % MS | PB | % MS | MS |
| Arg, His, Ile, Leu, Lys, Met, Phe, Thr, Trp, Val, % PB | ARG HIS ILE LEU LYS MET PHE THR TRP VAL | % da PB (g AA/100 g PB) | PB |
| AG total, % MS | AGT | % MS | MS |
| C12:0, C14:0, C16:0, C16:1, C18:0, C18:1 trans, C18:1 cis, C18:2, C18:3, Outros, % AG TOTAL | C12 C14 C16 C161 C18 C181t C181c C182 C183 OUT | % do AG total | AG total |
Nota [p.458]: "Os dados de AA e AG individuais foram fornecidos pela Cornell University (Higgs et al., 2015). Como os dados são provenientes de uma única fonte, o número de amostras e o desvio padrão não são apresentados." Os 11 AA (Arg…Val) = 10 AAE; **Cis/Tyr não aparecem**. Observações: perfis de AA/AG são frequentemente **copiados entre alimentos similares** (ex. todas as silagens de milho têm o mesmo AA/AG; polpa de beterraba seca/melaço/úmida; todos os óleos só têm AG); linhas vazias = sem dado; levedura de cerveja tem "Outros = 100.00". A soma das % de AG (C12…Outros) fecha em 100 ± 0.02 nos blocos transcritos (verificação na seção 7.2). PB da 19-2 **difere levemente** da PB da 19-1 em muitos alimentos (fontes diferentes), ex. farinha de sangue 96.97 vs 95.1; farelo de canola 41.49 vs 41.5; feno de gramíneas temperadas mat. média 13.28 vs 13.3.

### 3.3 Tabela 19-3 — "Composição de minerais de fonte inorgânica e coeficientes de absorção de elementos para bovinos leiteiros com base em 100 % MS" [pp.459–464]
Colunas: **Fonte mineral** (nome, fórmula, código NRC16F10xx) | **Mineral** (símbolo do elemento; linhas "Mineral primário", "Mineral secundário", "Mineral de menor relevância 1/2/3") | **%** (concentração do elemento na fonte, % da MS) | **Coeficiente de Absorção** (fração absorvida; "N/A" = não aplicável). Organizada por elemento: Cálcio, Cloreto, Cobalto, Cobre, Iodo, Ferro, Magnésio, Manganês, Fósforo, Potássio, Selênio, Sódio, Enxofre, Zinco (**uma mesma fonte aparece em mais de uma seção**, ex. CaCl2 em Ca e Cl; KCl em Cl e K; NaCl em Cl e Na; farinha de ossos em Ca e P).
Rodapés [p.464, verificados]: (a) MS = 100 % exceto ácido fosfórico = 75 %. (b) concentrações minerais < 1 % não mostradas. (c) N/A = não aplicável. (d) para Mg, os coeficientes de absorção **assumem 1.2 % de K na dieta**. (e) cinzas = 100 % para todas as fontes exceto: farinha de ossos = 79 %; fosfato de amônio dibásico = 36 %; fosfato de amônio monobásico = 36 %; sulfato de amônio = 33 %. (f) alimentos com N detectável têm PB: farinha de ossos = 13.2 %; fosfato de amônio dibásico = 115,9 %; monobásico = 70,9 %; sulfato de amônio = 134,1 % (vírgula decimal no original); **assume-se PB 100 % Fração A**.

## 4. Equações (texto p. 395; verificadas na imagem a 170 dpi)

Notação: ED em Mcal/kg MS; AGT, PB, Cinzas em % da MS; PDR e PNDR em % da PB; coeficiente de digestibilidade da gordura em % (Cap. 4, Tab. 4-1); PNDRd = digestibilidade intestinal da PNDR. **0.318 Mcal/kg = energia endógena total (0.088+0.093+0.137)** [p.395]. Constantes numéricas das equações (o livro não as rotula; significado **inferido** por mim, coeficientes por 1 % da MS ⇒ Mcal/kg MS): 0.094 = 9.4 Mcal/kg de AG; 0.043 = 4.3 Mcal/kg (glicerol puro, citado no texto); 0.056 = 5.6 Mcal/kg de proteína digestível; 0.04 = 4.0 Mcal/kg de carboidrato/MOR (citado no texto para açúcares); 0.96 = fator de digestibilidade da MOR; 0.73 = digestibilidade assumida dos AG de produtos animais; 1.06 = fator AG→TG (massa de TG = 1.06 × AG; o termo é impresso como AGT/1.06) ⚠.

**Eq. 19-1** — suplementos lipídicos que contêm essencialmente só AG (não TG) [p.395]:
```
ED_base = AGT * (CoefDigGordura / 100) * 0.094 - 0.318
```
**Eq. 19-2** — suplementos lipídicos compostos principalmente de TG [p.395]:
```
ED_base = (AGT * (CoefDigGordura / 100) * 0.094) + ((100 - Cinzas - (AGT / 1.06)) * 0.96 * 0.043) - 0.318
```
**Eq. 19-3** — alimentos de proteína de origem animal (amido e FDN excluídos; "equações de base do Cap. 3") [p.395]:
```
ED_base = (0.73 * AGT * 0.094)
        + ((PB * (PDR / 100) + (PB * (PNDR / 100) * PNDRd)) * 0.056)
        + (0.96 * (100 - AGT/1.06 - PB - Cinzas) * 0.04) - 0.318
```
Nota do livro: AGT e PB em % da MS; PDR e PNDR em % da PB; **PNDRd "em porcentagem da PNDR"** — **⚠ na prática, PNDRd entra como FRAÇÃO (0–1)** (com PNDRd = 85 a conta explode); com PNDRd/100 a equação reproduz a tabela (testes abaixo). PDR = 100 − PNDR (assumido; não impresso explicitamente).
**Eq. 19-4** — açúcares, glicerol bruto e outros álcoois de açúcar [p.395]:
```
ED_base = (100 - Cinzas) * 0.040 * 0.96 - 0.318
```
Nota: a entalpia de açúcares e glicerol difere (glicerol puro = 4.3 Mcal/kg; sacarose = 4.0 Mcal/kg); usou-se 4 Mcal/kg para todos.

**Equação de regressão para AGT de forragens** [p.395] (Daley et al., 2018):
```
AGT = GB * 0.5678            (forragens, quando não há AGT medido; % MS)
AGT = GB - 1                 (demais alimentos sem AGT medido)
MOR = 100 - (Cinzas + AGT + PB + FDN + Amido)       (% MS)
```
Resultados dos testes numéricos que fiz contra os valores impressos (valores de entrada da Tab. 19-1, imagem):

| Alimento (pág.) | Eq. | ED calculada | ED impressa | Δ | Comentário |
|---|---|---|---|---|---|
| Farinha de penas [p.416] | 19-3 | 4.11 | 4.12 | −0.01 | reproduz |
| Farinha de subprod. de aves [p.427] | 19-3 | 4.25 | 4.25 | 0.00 | reproduz |
| Farinha de carne e ossos suínos [p.422] | 19-3 | 3.21 | 3.25 | −0.04 | ≈ |
| Farinha de sangue alta dPNDR [p.402] | 19-3 | 4.43 | 4.56 | −0.13 | ⚠ PNDR/dPNDR impressos são arredondados |
| Farinha de sangue baixa dPNDR [p.402] | 19-3 | 3.71 | 3.82 | −0.11 | ⚠ idem |
| Farinha de peixe [p.416] | 19-3 | 3.43 | 3.63 | −0.20 | ⚠ |
| Glicerol [p.417] | 19-4 | 3.27 | 3.29 | −0.02 | ≈ (cinzas 6.7) |
| Melaço [p.423] | 19-4 | 2.91 | 3.07 | −0.16 | ⚠ melaço provavelmente NÃO usa 19-4 (tem PB 9.3) |
| Óleos (soja, girassol…) [pp.414–416] | 19-2 (d=0.70, cinzas=0) | 6.17 | 6.22 | −0.05 | ≈; todos os óleos = 6.22 |
| Sebo / Banha [pp.415–416] | 19-2 | 6.01 (d=0.68) | 5.80 | +0.21 | ⚠ d implícito ≈ 0.655 |
| Sabão de cálcio [p.403] | 19-1 | 5.72 (d=0.76) | 5.42 | +0.30 | ⚠ d implícito ≈ 0.72 |
Conclusão: as equações estão corretas na forma; diferenças residuais vêm de entradas arredondadas (PNDR, dPNDR, cinzas ausentes nos óleos) e do coeficiente de digestibilidade do Cap. 4 usado por alimento (não impresso aqui). **Recomendação: usar o ED base da tabela como valor dado; recalcular só para alimentos novos/editados.**

## 5. Parâmetros e tabelas
Esquemas de colunas: seção 3 (19-1, 19-2, 19-3). Listas completas de alimentos/fontes: seção 6. Valores transcritos e verificados na imagem: seção 7 (19-1: 30 alimentos no corpo do arquivo + 88 no CSV de apoio; 19-2: 22 + 60 no CSV de apoio; 19-3: **completa**). Arquivos de apoio (dados): `/tmp/claude-0/nasem/notes/ch19_dados/` (`tab19-1_parcial_88alimentos.csv`, `tab19-2_parcial_60alimentos.csv`, `tab19-3_completa.csv`).


## 6. Listas completas de alimentos e fontes (rótulos como impressos; categorias atribuídas por mim)

### 6.1 Tabela 19-1 — 184 posições de impressão = 180 alimentos legíveis + 4 posições da p.406 original ausente

Ordem de impressão = ordem alfabética aproximada do nome em inglês (não é ordem por código). Código = NRC16F + número; a numeração tem falhas (códigos 35, 36, 53, 54, 76, 78 e 141 não aparecem em nenhuma posição legível; 3 deles ficam sem alimento). Os 4 alimentos ausentes têm nome inferido da Tab. 19-2 (mesma ordem), mas o **código** deles não é recuperável ⚠. A coluna "categoria" **não existe no livro** (o texto cita 12 classes e 3 tipos, mas não os imprime por alimento).

| # | pág. | código | nome impresso (PT) | categoria (minha atribuição) |
|---|---|---|---|---|
| 1 | 397 | NRC16F1 | Far. Alfafa | Forragem seca (farinha de alfafa desidratada) |
| 2 | 397 | NRC16F2 | Casca de Amêndoas | Subproduto fibroso |
| 3 | 397 | NRC16F3 | Bagaço de Maçã Úmido Subproduto | Subproduto |
| 4 | 397 | NRC16F5 | Subproduto de Padaria Descarte de Pão | Subproduto (padaria) |
| 5 | 398 | NRC16F6 | Subproduto de Padaria, Cereal | Subproduto (padaria) |
| 6 | 398 | NRC16F7 | Subproduto de Padaria, Cookies | Subproduto (padaria) |
| 7 | 398 | NRC16F4 | Farinha de Rosca | Subproduto (padaria) |
| 8 | 398 | NRC16F8 | Grão de Cevada Moído Seco | Grão/cereal |
| 9 | 399 | NRC16F1074 | Grão de Cevada, Laminado a Vapor | Grão/cereal |
| 10 | 399 | NRC16F9 | Feno de Cevada | Forragem seca (feno) |
| 11 | 399 | NRC16F10 | Broto de Malte de Cevada | Subproduto |
| 12 | 399 | NRC16F11 | Silagem de Cevada, c/ Sementes | Forragem úmida (silagem) |
| 13 | 400 | NRC16F12 | Silagem de Cevada, Mat. Média | Forragem úmida (silagem) |
| 14 | 400 | NRC16F13 | Silagem de Cevada, Vegetativo | Forragem úmida (silagem) |
| 15 | 400 | NRC16F14 | Polpa de Beterraba Seca | Subproduto (polpa) |
| 16 | 400 | NRC16F15 | Polpa de Beterraba Seca com Melaço | Subproduto (polpa) |
| 17 | 401 | NRC16F16 | Polpa de Beterraba Úmida | Subproduto (polpa) |
| 18 | 401 | NRC16F17 | Feno de Capim Bermuda | Forragem seca (feno) |
| 19 | 401 | NRC16F18 | Silagem de Capim Bermuda, Madura | Forragem úmida (silagem) |
| 20 | 401 | NRC16F19 | Silagem de Capim Bermuda, Mat. Média | Forragem úmida (silagem) |
| 21 | 402 | NRC16F1000 | Far. Sangue, Alta dPNDR | Proteína animal |
| 22 | 402 | NRC16F20 | Far. Sangue, Baixa dPNDR | Proteína animal |
| 23 | 402 | NRC16F21 | Resíduo de Cervejaria, Seco | Subproduto (cervejaria) |
| 24 | 402 | NRC16F22 | Resíduo de Cervejaria, Úmido | Subproduto (cervejaria) |
| 25 | 403 | NRC16F23 | Levedura de Cervejaria Seca | Subproduto (levedura) |
| 26 | 403 | NRC16F24 | Levedura de Cervejaria Úmida | Subproduto (levedura) |
| 27 | 403 | NRC16F25 | Sabão de Cálcio | Gordura (sabão de Ca) |
| 28 | 403 | NRC16F26 | Subproduto de Doces (Não Chocolate) | Subproduto (doces) |
| 29 | 404 | NRC16F27 | Subproduto de Doces, Alta Proteína | Subproduto (doces) |
| 30 | 404 | NRC16F28 | Farelo de Canola, Extraído com Solvente | Proteína vegetal |
| 31 | 404 | NRC16F29 | Semente de Canola Moída | Proteína vegetal (oleaginosa) |
| 32 | 404 | NRC16F30 | Subproduto de Chocolate | Subproduto (chocolate) |
| 33 | 405 | NRC16F31 | Polpa Cítrica Seca | Subproduto (polpa cítrica) |
| 34 | 405 | NRC16F32 | Polpa Cítrica Úmida | Subproduto (polpa cítrica) |
| 35 | 405 | NRC16F33 | Feno de Gramíneas Temperadas, Maduro | Forragem seca (feno) |
| 36 | 405 | NRC16F34 | Feno de Gramíneas Temperadas, Mat. Média | Forragem seca (feno) |
| 37 | (406 orig.) | ⚠ ? | [ausente no PDF] provável: Silagem de Gramíneas Temperadas | — |
| 38 | (406 orig.) | ⚠ ? | [ausente no PDF] provável: Milho, Espiga com Casca e Sabugo, Ensilado, Alto Teor de Fibra | — |
| 39 | (406 orig.) | ⚠ ? | [ausente no PDF] provável: Milho, Espiga com Casca e Sabugo, Ensilado, Baixo Teor de Fibra | — |
| 40 | (406 orig.) | ⚠ ? | [ausente no PDF] provável: Farinha de Milho e Sabugo, Seca | — |
| 41 | 407 | NRC16F37 | Espiga de Milho | Grão/cereal (espiga) |
| 42 | 407 | NRC16F38 | Gérmen de Milho | Subproduto (milho) |
| 43 | 407 | NRC16F39 | Far. Gérmen de Milho | Subproduto (milho) |
| 44 | 407 | NRC16F40 | Glúten de Milho, Seco | Subproduto (milho) |
| 45 | 408 | NRC16F41 | Glúten de Milho Úmido | Subproduto (milho) |
| 46 | 408 | NRC16F42 | Far. de Glúten de Milho | Subproduto (milho) |
| 47 | 408 | NRC16F1071 | Milho Seco Moído Grosso | Grão/cereal |
| 48 | 408 | NRC16F1070 | Milho Seco Moído Fino | Grão/cereal |
| 49 | 409 | NRC16F44 | Milho Seco Moagem Média | Grão/cereal |
| 50 | 409 | NRC16F1072 | Milho Grão Alta Umidade, Moagem Grossa | Grão/cereal (alta umidade) |
| 51 | 409 | NRC16F45 | Milho Grão Alta Umidade, Moagem Fina | Grão/cereal (alta umidade) |
| 52 | 409 | NRC16F43 | Varredura de Milho | Subproduto (milho) |
| 53 | 410 | NRC16F46 | Milho Grão Floculado a Vapor | Grão/cereal |
| 54 | 410 | NRC16F47 | Canjica de Milho | Subproduto (milho) |
| 55 | 410 | NRC16F49 | Silagem de Milho, Imatura | Forragem úmida (silagem) |
| 56 | 410 | NRC16F50 | Silagem de Milho, Madura | Forragem úmida (silagem) |
| 57 | 411 | NRC16F48 | Silagem de Milho Típica | Forragem úmida (silagem) |
| 58 | 411 | NRC16F52 | Silagem de Milho sem Espiga, Alta MS | Forragem úmida (silagem) |
| 59 | 411 | NRC16F51 | Silagem de Milho sem Espiga, Baixa MS | Forragem úmida (silagem) |
| 60 | 411 | NRC16F55 | Descarte de Algodão | Subproduto (algodão) |
| 61 | 412 | NRC16F57 | Cascas de Algodão | Subproduto fibroso (algodão) |
| 62 | 412 | NRC16F58 | Farelo de Algodão | Proteína vegetal |
| 63 | 412 | NRC16F56 | Caroço de Algodão com Línter | Proteína vegetal (oleaginosa) |
| 64 | 412 | NRC16F59 | Grãos de Destilaria e Solúveis, Secos, c/ Alto Teor de Gordura | Subproduto (destilaria) |
| 65 | 413 | NRC16F60 | Grãos de Destilaria e Solúveis, Secos, c/ Alto Teor de Proteína | Subproduto (destilaria) |
| 66 | 413 | NRC16F61 | Grãos de Destilaria e Solúveis, Secos, c/ Baixo Teor de Gordura | Subproduto (destilaria) |
| 67 | 413 | NRC16F62 | Grãos e Solúveis de Destilaria, Úmida Modificada | Subproduto (destilaria) |
| 68 | 413 | NRC16F63 | Grãos e Solúveis de Destilaria, Úmido | Subproduto (destilaria) |
| 69 | 414 | NRC16F64 | Solúveis de Destilaria | Subproduto (destilaria) |
| 70 | 414 | NRC16F65 | Óleo de Canola, Gordura | Gordura/óleo |
| 71 | 414 | NRC16F66 | Óleo de Milho, Gordura | Gordura/óleo |
| 72 | 414 | NRC16F67 | Óleo de Algodão, Gordura | Gordura/óleo |
| 73 | 415 | NRC16F69 | Óleo de Linhaça, Gordura | Gordura/óleo |
| 74 | 415 | NRC16F68 | Banha, Gordura | Gordura/gordura animal |
| 75 | 415 | NRC16F70 | Óleo de Cártamo, Gordura | Gordura/óleo |
| 76 | 415 | NRC16F71 | Óleo de Soja, Gordura | Gordura/óleo |
| 77 | 416 | NRC16F72 | Óleo de Girassol, Gordura | Gordura/óleo |
| 78 | 416 | NRC16F73 | Sebo, Gordura | Gordura/gordura animal |
| 79 | 416 | NRC16F74 | Farinha de Penas | Proteína animal |
| 80 | 416 | NRC16F75 | Farinha de Peixe | Proteína animal |
| 81 | 417 | NRC16F96 | Linhaça | Proteína vegetal (oleaginosa) |
| 82 | 417 | NRC16F97 | Farinha de Linhaça | Proteína vegetal |
| 83 | 417 | NRC16F77 | Subproduto de Frutas e Legumes, Úmido | Subproduto (frutas/legumes) |
| 84 | 417 | NRC16F1075 | Glicerol | Fonte de energia (glicerol) |
| 85 | 418 | NRC16F79 | Varredura de Grãos, Fonte Desconhecida | Subproduto/outros |
| 86 | 418 | NRC16F80 | Feno de Sorgo Granífero | Forragem seca (feno) |
| 87 | 418 | NRC16F81 | Silagem de Sorgo Granífero, Madura | Forragem úmida (silagem) |
| 88 | 418 | NRC16F82 | Silagem de Sorgo Granífero, Mat. Média | Forragem úmida (silagem) |
| 89 | 419 | NRC16F89 | Mistura de Gramíneas e Leguminosas, Feno Misto | Forragem seca (feno) |
| 90 | 419 | NRC16F90 | Mistura de Gramíneas e Leguminosas, Silagem Mista | Forragem úmida (silagem) |
| 91 | 419 | NRC16F85 | Feno de Mistura de Gramíneas e Leguminosas, Gramíneas Predominantes, Maduras | Forragem seca (feno) |
| 92 | 419 | NRC16F84 | Feno de Mistura de Gramíneas e Leguminosas, Gramíneas Predominantes, Mat. Média | Forragem seca (feno) |
| 93 | 420 | NRC16F83 | Silagem de Mistura de Gramíneas e Leguminosas, Gramíneas Predominantes | Forragem úmida (silagem) |
| 94 | 420 | NRC16F87 | Feno de Mistura de Gramíneas e Leguminosas, Leguminosas Predominantes, Imaturas | Forragem seca (feno) |
| 95 | 420 | NRC16F86 | Feno de Mistura de Gramíneas e Leguminosas, Leguminosas Predominantes, Maduras | Forragem seca (feno) |
| 96 | 420 | NRC16F88 | Silagem de Mistura de Gramíneas e Leguminosas, Leguminosas Predominantes | Forragem úmida (silagem) |
| 97 | 421 | NRC16F91 | Feno de Leguminosa, Imaturo | Forragem seca (feno) |
| 98 | 421 | NRC16F92 | Feno de Leguminosa, Maduro | Forragem seca (feno) |
| 99 | 421 | NRC16F93 | Feno de Leguminosa, Mat. Média | Forragem seca (feno) |
| 100 | 421 | NRC16F94 | Silagem de Leguminosa, Imatura | Forragem úmida (silagem) |
| 101 | 422 | NRC16F95 | Silagem de Leguminosa, Imatura [sic; rótulo repetido de F94] | Forragem úmida (silagem) |
| 102 | 422 | NRC16F98 | Farinha de Carne e Ossos, Suínos | Proteína animal |
| 103 | 422 | NRC16F99 | Feno de Milheto | Forragem seca (feno) |
| 104 | 422 | NRC16F100 | Silagem de Milheto | Forragem úmida (silagem) |
| 105 | 423 | NRC16F101 | Melaço | Fonte de energia (melaço) |
| 106 | 423 | NRC16F102 | Grão de Aveia, Laminado | Grão/cereal |
| 107 | 423 | NRC16F103 | Feno de Aveia | Forragem seca (feno) |
| 108 | 423 | NRC16F104 | Cascas de Aveia | Subproduto fibroso |
| 109 | 424 | NRC16F105 | Silagem de Aveia, Imatura | Forragem úmida (silagem) |
| 110 | 424 | NRC16F106 | Silagem de Aveia, Mat. Média | Forragem úmida (silagem) |
| 111 | 424 | NRC16F107 | Feno de Ervilha | Forragem seca (feno) |
| 112 | 424 | NRC16F108 | Silagem de Ervilha | Forragem úmida (silagem) |
| 113 | 425 | NRC16F109 | Feno de Amendoim | Forragem seca (feno) |
| 114 | 425 | NRC16F110 | Cascas de Amendoim | Subproduto fibroso |
| 115 | 425 | NRC16F111 | Farelo de Amendoim, Expellers | Proteína vegetal |
| 116 | 425 | NRC16F112 | Pele de Amendoim | Subproduto fibroso |
| 117 | 426 | NRC16F113 | Amendoim | Proteína vegetal (oleaginosa) |
| 118 | 426 | NRC16F114 | Ervilha | Grão/leguminosa |
| 119 | 426 | NRC16F115 | Resíduos de Conservas de Abacaxi | Subproduto (frutas) |
| 120 | 426 | NRC16F116 | Farinha de Subproduto de Batatas | Subproduto (batata) |
| 121 | 427 | NRC16F117 | Farinha de Subprodutos de Aves | Proteína animal |
| 122 | 427 | NRC16F123 | Grãos de Arroz | Grão/cereal |
| 123 | 427 | NRC16F118 | Farelo de Arroz | Subproduto (arroz) |
| 124 | 427 | NRC16F119 | Farelo de Arroz Desengordurado | Subproduto (arroz) |
| 125 | 428 | NRC16F120 | Cascas de Arroz | Subproduto fibroso (arroz) |
| 126 | 428 | NRC16F121 | Silagem de Arroz, c/ Grãos | Forragem úmida (silagem) |
| 127 | 428 | NRC16F122 | Silagem de Arroz, Vegetativo | Forragem úmida (silagem) |
| 128 | 428 | NRC16F1002 | Lisina Protegida da Degradação Ruminal | AA protegido (Lys) |
| 129 | 429 | NRC16F1001 | Metionina Protegida da Degradação Ruminal | AA protegido (Met) |
| 130 | 429 | NRC16F124 | Azevém Anual Fresco, Imaturo | Forragem fresca/pastagem |
| 131 | 429 | NRC16F125 | Azevém Anual Fresco, Mat. Média | Forragem fresca/pastagem |
| 132 | 429 | NRC16F126 | Feno de Azevém Anual, Imaturo | Forragem seca (feno) |
| 133 | 430 | NRC16F127 | Feno de Azevém Anual, Maduro | Forragem seca (feno) |
| 134 | 430 | NRC16F131 | Feno de Azevém Anual, Mat. Média | Forragem seca (feno) |
| 135 | 430 | NRC16F128 | Silagem de Azevém Anual, Imatura | Forragem úmida (silagem) |
| 136 | 430 | NRC16F129 | Silagem de Azevém Anual, Madura | Forragem úmida (silagem) |
| 137 | 431 | NRC16F130 | Silagem de Azevém Anual, Mat. Média | Forragem úmida (silagem) |
| 138 | 431 | NRC16F132 | Grão de Azevém [19-2: Grão de Centeio] | Grão/cereal |
| 139 | 431 | NRC16F133 | Farelo de Cártamo | Proteína vegetal |
| 140 | 431 | NRC16F135 | Silagem de Sorgo Forrageiro, Imatura | Forragem úmida (silagem) |
| 141 | 432 | NRC16F136 | Silagem de Azevém Anual, Mat. Média [sic; 19-2: Silagem de Sorgo Forrageiro, Maduro] | Forragem úmida (silagem) |
| 142 | 432 | NRC16F137 | Sorgo Grão Moído | Grão/cereal |
| 143 | 432 | NRC16F1073 | Grão de Sorgo, Floculado a Vapor | Grão/cereal |
| 144 | 432 | NRC16F138 | Feno de Sorgo | Forragem seca (feno) |
| 145 | 433 | NRC16F139 | Silagem de Soja e Sorgo | Forragem úmida (silagem) |
| 146 | 433 | NRC16F142 | Feno de Sorgo e Capim Sudão | Forragem seca (feno) |
| 147 | 433 | NRC16F140 | Silagem de Sorgo e Capim Sudão | Forragem úmida (silagem) |
| 148 | 433 | NRC16F143 | Feno de Soja | Forragem seca (feno) |
| 149 | 434 | NRC16F144 | Casquinha de Soja | Subproduto fibroso (soja) |
| 150 | 434 | NRC16F145 | Farelo de Soja Expellers | Proteína vegetal |
| 151 | 434 | NRC16F146 | Farelo de Soja, Extrusado | Proteína vegetal |
| 152 | 434 | NRC16F134 | Farelo de Soja, Extraído com Solvente, 48% PB | Proteína vegetal |
| 153 | 435 | NRC16F147 | Silagem de Soja | Forragem úmida (silagem) |
| 154 | 435 | NRC16F148 | Soja, Integral Crua | Proteína vegetal (oleaginosa) |
| 155 | 435 | NRC16F149 | Soja, Integral Tostada | Proteína vegetal (oleaginosa) |
| 156 | 435 | NRC16F150 | Grãos de Trigo | Grão/cereal |
| 157 | 436 | NRC16F151 | Feno de Capim Sudão, Maduro | Forragem seca (feno) |
| 158 | 436 | NRC16F152 | Feno de Capim Sudão, Mat. Média | Forragem seca (feno) |
| 159 | 436 | NRC16F153 | Silagem de Capim Sudão, Maduro | Forragem úmida (silagem) |
| 160 | 436 | NRC16F154 | Silagem de Capim Sudão, Mat. Média | Forragem úmida (silagem) |
| 161 | 437 | NRC16F155 | Feno de Bagaço de Cana | Forragem seca (feno) |
| 162 | 437 | NRC16F156 | Silagem de Bagaço de Cana | Forragem úmida (silagem) |
| 163 | 437 | NRC16F157 | Farelo de Girassol | Proteína vegetal |
| 164 | 437 | NRC16F158 | Semente de Girassol | Proteína vegetal (oleaginosa) |
| 165 | 438 | NRC16F159 | Silagem de Girassol | Forragem úmida (silagem) |
| 166 | 438 | NRC16F160 | Resíduos de Conservas de Milho Doce | Subproduto (milho doce) |
| 167 | 438 | NRC16F161 | Tapioca (Cassava) | Fonte de energia (raiz) |
| 168 | 438 | NRC16F162 | Bagaço de Tomate | Subproduto (tomate) |
| 169 | 439 | NRC16F163 | Grão de Triticale | Grão/cereal |
| 170 | 439 | NRC16F164 | Feno de Triticale | Forragem seca (feno) |
| 171 | 439 | NRC16F165 | Silagem de Triticale + Ervilha [19-2: Silagem de Triticale] | Forragem úmida (silagem) |
| 172 | 439 | NRC16F166 | Silagem de Triticale, Madura | Forragem úmida (silagem) |
| 173 | 440 | NRC16F167 | Silagem de Triticale, Mat. Média | Forragem úmida (silagem) |
| 174 | 440 | NRC16F168 | Uréia | NNP (ureia) |
| 175 | 440 | NRC16F169 | Farelo de Trigo | Subproduto (trigo) |
| 176 | 440 | NRC16F170 | Grão de Trigo, Moído | Grão/cereal |
| 177 | 441 | NRC16F171 | Feno de Trigo, c/ Grãos | Forragem seca (feno) |
| 178 | 441 | NRC16F172 | Feno de Trigo, Vegetativo | Forragem seca (feno) |
| 179 | 441 | NRC16F173 | Farelo Remoído de Trigo [19-2: Sêmola de Trigo] | Subproduto (trigo) |
| 180 | 441 | NRC16F174 | Silagem de Trigo, c/ Grãos | Forragem úmida (silagem) |
| 181 | 442 | NRC16F175 | Silagem de Trigo, Vegetativa | Forragem úmida (silagem) |
| 182 | 442 | NRC16F176 | Palha de Trigo | Forragem seca (palha) |
| 183 | 442 | NRC16F177 | Soro de Leite, Seco | Subproduto (lácteo) |
| 184 | 442 | NRC16F178 | Soro de Leite, Úmido | Subproduto (lácteo) |

Notas: (i) a p.406 impressa é **idêntica** à p.407 (verificado na imagem: mesmos 4 alimentos, F37–F40); por isso as posições 37–40 (p.406 original) não existem no PDF; (ii) "Far." = Farinha (confirmado pela Tab. 19-2: "Farinha de Sangue", "Farinha de Alfafa"); (iii) rótulos suspeitos de erro tipográfico ⚠: F95 (igual a F94, "Imatura"; deveria ser outra maturidade), F136 ("Silagem de Azevém Anual, Mat. Média" repete F130; a Tab. 19-2 traz "Silagem de Sorgo Forrageiro, Maduro" nessa posição), F132 ("Grão de Azevém" vs "Grão de Centeio" na 19-2), F165 ("Triticale + Ervilha" vs "Triticale" na 19-2), F173 ("Farelo Remoído de Trigo" vs "Sêmola de Trigo"), F170 ("Grão de Trigo, Moído" vs "Laminado" na 19-2), F55 ("Descarte de Algodão" vs "Resíduos de Caroço de Algodão"); (iv) códigos F1000–F1002 e F1070–F1075 fogem da numeração 1–178 (provavelmente acrescentados depois; não informado pelo livro) (1000: sangue alta dPNDR; 1001/1002: Met e Lys protegidas; 1070/1071: milho seco fino/grosso; 1072: milho alta umidade grosso; 1073: sorgo floculado; 1074: cevada laminada; 1075: glicerol).

### 6.2 Tabela 19-2 — 184 alimentos (12 por página, 2 blocos de 6; p.458 só 4)

A ordem é a mesma da 19-1 (posição n da 19-2 ≈ posição n da 19-1), com 2 exceções de rótulo/ordem anotadas. Sem códigos NRC na 19-2: a ligação com a 19-1 é **por posição** (coluna "cód. 19-1"). Alimentos sem AA/AG na 19-2 aparecem com células vazias.

| # | pág. | nome impresso na 19-2 | cód. 19-1 (por posição) |
|---|---|---|---|
| 1 | 443 | Farinha de Alfafa | NRC16F1 |
| 2 | 443 | Cascas de Amêndoas | NRC16F2 |
| 3 | 443 | Subproduto de Maçã, Úmido | NRC16F3 |
| 4 | 443 | Subproduto de Padaria, Resíduos de Pão | NRC16F5 |
| 5 | 443 | Subproduto de Padaria, Cereal | NRC16F6 |
| 6 | 443 | Subproduto de Padaria, Cookies | NRC16F7 |
| 7 | 443 | Farinha de Rosca | NRC16F4 |
| 8 | 443 | Grão de Cevada, Moído, Seco | NRC16F8 |
| 9 | 443 | Grão de Cevada, Laminado a Vapor | NRC16F1074 |
| 10 | 443 | Feno de Cevada | NRC16F9 |
| 11 | 443 | Brotos de Malte de Cevada | NRC16F10 |
| 12 | 443 | Silagem de Cevada c/ Grãos | NRC16F11 |
| 13 | 444 | Silagem de Cevada, Mat. Média | NRC16F12 |
| 14 | 444 | Silagem de Cevada, Vegetativa | NRC16F13 |
| 15 | 444 | Polpa de Beterraba, Seca | NRC16F14 |
| 16 | 444 | Polpa de Beterraba com Melaço | NRC16F15 |
| 17 | 444 | Polpa de Beterraba, Úmida | NRC16F16 |
| 18 | 444 | Feno de Capim Bermuda | NRC16F17 |
| 19 | 444 | Silagem de Capim Bermuda, Maduro | NRC16F18 |
| 20 | 444 | Silagem de Capim Bermuda, Mat. Média | NRC16F19 |
| 21 | 444 | Farinha de Sangue, Alta dPNDR | NRC16F1000 |
| 22 | 444 | Farinha de Sangue, Baixa dPNDR | NRC16F20 |
| 23 | 444 | Resíduo de Cervejaria, Seco | NRC16F21 |
| 24 | 444 | Resíduo de Cervejaria, Úmido | NRC16F22 |
| 25 | 445 | Levedura de Cerveja, Seca | NRC16F23 |
| 26 | 445 | Levedura de Cerveja, Úmida | NRC16F24 |
| 27 | 445 | Sabão de Cálcio | NRC16F25 |
| 28 | 445 | Subprodutos de Doces (não chocolate) | NRC16F26 |
| 29 | 445 | Subprodutos de Doces, Alta Proteína | NRC16F27 |
| 30 | 445 | Farelo de Canola, Extraído com Solvente | NRC16F28 |
| 31 | 445 | Semente de Canola, Moída | NRC16F29 |
| 32 | 445 | Subproduto de Chocolate | NRC16F30 |
| 33 | 445 | Polpa Cítrica, Seca | NRC16F31 |
| 34 | 445 | Polpa Cítrica, Úmida | NRC16F32 |
| 35 | 445 | Feno de Gramíneas Temperadas, Maduras | NRC16F33 |
| 36 | 445 | Feno de Gramíneas Temperadas, Mat. Média | NRC16F34 |
| 37 | 446 | Silagem de Gramíneas Temperadas | ⚠ (p.406 ausente) |
| 38 | 446 | Milho, Espiga com Casca e Sabugo, Ensilado, Alto Teor de Fibra | ⚠ (p.406 ausente) |
| 39 | 446 | Milho, Espiga com Casca e Sabugo, Ensilado, Baixo Teor de Fibra | ⚠ (p.406 ausente) |
| 40 | 446 | Farinha de Milho e Sabugo, Seca | ⚠ (p.406 ausente) |
| 41 | 446 | Espigas de Milho | NRC16F37 |
| 42 | 446 | Gérmen de Milho | NRC16F38 |
| 43 | 446 | Farelo de Gérmen de Milho | NRC16F39 |
| 44 | 446 | Glúten de Milho, Seco | NRC16F40 |
| 45 | 446 | Glúten de Milho, Úmido | NRC16F41 |
| 46 | 446 | Farelo de Glúten de Milho | NRC16F42 |
| 47 | 446 | Milho Grão Moído Seco, Moagem Grossa | NRC16F1071 |
| 48 | 446 | Milho Grão Moído Seco, Moagem Fina | NRC16F1070 |
| 49 | 447 | Milho Grão Moído Seco, Moagem Média | NRC16F44 |
| 50 | 447 | Milho Grão com Alta Umidade, Moído Grosso | NRC16F1072 |
| 51 | 447 | Milho Grão com Alta Umidade, Moído Fino | NRC16F45 |
| 52 | 447 | Varredura de Milho | NRC16F43 |
| 53 | 447 | Milho Grão, Floculado a Vapor | NRC16F46 |
| 54 | 447 | Canjica de Milho | NRC16F47 |
| 55 | 447 | Silagem de Milho, Imaturo | NRC16F49 |
| 56 | 447 | Silagem de Milho, Maduro | NRC16F50 |
| 57 | 447 | Silagem de Milho, Típica | NRC16F48 |
| 58 | 447 | Silagem de Milho sem Espigas, Alta MS | NRC16F52 |
| 59 | 447 | Silagem de Milho sem Espigas, Baixa MS | NRC16F51 |
| 60 | 447 | Resíduos de Caroço de Algodão | NRC16F55 |
| 61 | 448 | Casca de Caroço de Algodão | NRC16F57 |
| 62 | 448 | Farelo de Algodão | NRC16F58 |
| 63 | 448 | Caroço de Algodão com Línter | NRC16F56 |
| 64 | 448 | Grãos de Destilaria e Solúveis, Secos, com Alto Teor de Gordura | NRC16F59 |
| 65 | 448 | Grãos de Destilaria e Solúveis, Secos, com Baixo Teor de Gordura | NRC16F61 |
| 66 | 448 | Grãos de Destilaria e Solúveis, Secos, com Alto Teor de Proteína | NRC16F60 |
| 67 | 448 | Grãos de Destilaria e Solúveis, Secos, com Umidade Modificada | NRC16F62 |
| 68 | 448 | Grãos de Destilaria e Solúveis, Úmidos | NRC16F63 |
| 69 | 448 | Solúveis da Destilaria | NRC16F64 |
| 70 | 448 | Óleo de Canola, Gordura | NRC16F65 |
| 71 | 448 | Óleo de Milho, Gordura | NRC16F66 |
| 72 | 448 | Óleo de Algodão, Gordura | NRC16F67 |
| 73 | 449 | Óleo de Linhaça, Gordura | NRC16F69 |
| 74 | 449 | Banha, Gordura | NRC16F68 |
| 75 | 449 | Óleo de Cártamo, Gordura | NRC16F70 |
| 76 | 449 | Óleo de Soja, Gordura | NRC16F71 |
| 77 | 449 | Óleo de Girassol, Gordura | NRC16F72 |
| 78 | 449 | Sebo, Gordura | NRC16F73 |
| 79 | 449 | Farinha de Penas | NRC16F74 |
| 80 | 449 | Farinha de Peixe | NRC16F75 |
| 81 | 449 | Linhaça | NRC16F96 |
| 82 | 449 | Farelo de Linhaça | NRC16F97 |
| 83 | 449 | Subproduto de Frutas e Vegetais, Úmido | NRC16F77 |
| 84 | 449 | Glicerol | NRC16F1075 |
| 85 | 450 | Varredura de Grãos, Fonte Desconhecida | NRC16F79 |
| 86 | 450 | Feno de Sorgo Granífero | NRC16F80 |
| 87 | 450 | Silagem de Sorgo Granífero Maduro | NRC16F81 |
| 88 | 450 | Silagem de Sorgo Granífero Mat. Média | NRC16F82 |
| 89 | 450 | Feno de Mistura de Gramíneas e Leguminosas | NRC16F89 |
| 90 | 450 | Silagem de Mistura de Gramíneas e Leguminosas | NRC16F90 |
| 91 | 450 | Feno de Misturas de Gramíneas e Leguminosas, Predominantemente Gramíneas, Maduras | NRC16F85 |
| 92 | 450 | Feno de Misturas de Gramíneas e Leguminosas, Predominantemente Gramíneas, Mat. Média | NRC16F84 |
| 93 | 450 | Silagem de Misturas de Gramíneas e Leguminosas, Predominantemente Gramíneas | NRC16F83 |
| 94 | 450 | Silagem [sic] de Misturas de Gramíneas e Leguminosas, Predominantemente Leguminosas, Imaturas | NRC16F87 |
| 95 | 450 | Feno de Misturas de Gramíneas e Leguminosas, Predominantemente Leguminosas, Maduras | NRC16F86 |
| 96 | 450 | Silagem de Misturas de Gramíneas e Leguminosas, Predominantemente Leguminosas, (cabeçalho cortado) | NRC16F88 |
| 97 | 451 | Feno de Leguminosas, Imaturas | NRC16F91 |
| 98 | 451 | Feno de Leguminosas, Maduras | NRC16F92 |
| 99 | 451 | Feno de Leguminosas, Mat. Média | NRC16F93 |
| 100 | 451 | Silagem de Leguminosas, Imaturas | NRC16F94 |
| 101 | 451 | Silagem de Leguminosas, Mat. Média | NRC16F95 |
| 102 | 451 | Farinha de Carne e Ossos, Suínos | NRC16F98 |
| 103 | 451 | Feno de Milheto | NRC16F99 |
| 104 | 451 | Silagem de Milheto | NRC16F100 |
| 105 | 451 | Melaço | NRC16F101 |
| 106 | 451 | Grão de Aveia, Laminado | NRC16F102 |
| 107 | 451 | Feno de Aveia | NRC16F103 |
| 108 | 451 | Cascas de Aveia | NRC16F104 |
| 109 | 452 | Silagem de Aveia, Imatura | NRC16F105 |
| 110 | 452 | Silagem de Aveia, Mat. Média | NRC16F106 |
| 111 | 452 | Feno de Ervilha | NRC16F107 |
| 112 | 452 | Silagem de Ervilha | NRC16F108 |
| 113 | 452 | Feno de Amendoim | NRC16F109 |
| 114 | 452 | Cascas de Amendoim | NRC16F110 |
| 115 | 452 | Farelo de Amendoim, Expellers | NRC16F111 |
| 116 | 452 | Pele de Amendoim | NRC16F112 |
| 117 | 452 | Amendoins | NRC16F113 |
| 118 | 452 | Ervilhas | NRC16F114 |
| 119 | 452 | Resíduos de Conservas de Abacaxi | NRC16F115 |
| 120 | 452 | Farelo de Subproduto de Batatas | NRC16F116 |
| 121 | 453 | Farinha de Subproduto de Aves | NRC16F117 |
| 122 | 453 | Arroz em Grãos | NRC16F123 |
| 123 | 453 | Farelo de Arroz | NRC16F118 |
| 124 | 453 | Farelo de Arroz, Desengordurado | NRC16F119 |
| 125 | 453 | Casca de Arroz | NRC16F120 |
| 126 | 453 | Silagem de Arroz com Grãos | NRC16F121 |
| 127 | 453 | Silagem de Arroz, Vegetativo | NRC16F122 |
| 128 | 453 | Lisina Protegida da Degradação Ruminal | NRC16F1002 |
| 129 | 453 | Metionina Protegida da Degradação Ruminal | NRC16F1001 |
| 130 | 453 | Azevém Anual Fresco, Imaturo | NRC16F124 |
| 131 | 453 | Azevém Anual Fresco, Mat. Média | NRC16F125 |
| 132 | 453 | Feno de Azevém Anual, Imaturo | NRC16F126 |
| 133 | 454 | Feno de Azevém Anual, Maduro | NRC16F127 |
| 134 | 454 | Feno de Azevém Anual, Mat. Média | NRC16F131 |
| 135 | 454 | Silagem de Azevém Anual, Imaturo | NRC16F128 |
| 136 | 454 | Silagem de Azevém Anual, Maduro | NRC16F129 |
| 137 | 454 | Silagem de Azevém Anual, Mat. Média | NRC16F130 |
| 138 | 454 | Grão de Centeio | NRC16F132 |
| 139 | 454 | Farelo de Cártamo | NRC16F133 |
| 140 | 454 | Silagem de Sorgo Forrageiro, Imaturo | NRC16F135 |
| 141 | 454 | Silagem de Sorgo Forrageiro, Maduro | NRC16F136 |
| 142 | 454 | Grão de Sorgo Seco, Moído | NRC16F137 |
| 143 | 454 | Grão de Sorgo, Floculado a Vapor | NRC16F1073 |
| 144 | 454 | Feno de Sorgo | NRC16F138 |
| 145 | 455 | Silagem de Sorgo e Soja | NRC16F139 |
| 146 | 455 | Feno de Sorgo e Capim Sudão | NRC16F142 |
| 147 | 455 | Silagem de Sorgo e Capim Sudão | NRC16F140 |
| 148 | 455 | Feno de Soja | NRC16F143 |
| 149 | 455 | Casca de Soja | NRC16F144 |
| 150 | 455 | Farelo de Soja, Expellers | NRC16F145 |
| 151 | 455 | Farelo de Soja, Extrusado | NRC16F146 |
| 152 | 455 | Farelo de Soja, Extraído com Solvente, 48% PB | NRC16F134 |
| 153 | 455 | Silagem de Soja | NRC16F147 |
| 154 | 455 | Soja Integral Crua | NRC16F148 |
| 155 | 455 | Soja Integral Tostada | NRC16F149 |
| 156 | 455 | Grãos de Trigo | NRC16F150 |
| 157 | 456 | Feno de Capim Sudão, Maduro | NRC16F151 |
| 158 | 456 | Feno de Capim Sudão, Mat. Média | NRC16F152 |
| 159 | 456 | Silagem de Capim Sudão, Maduro | NRC16F153 |
| 160 | 456 | Silagem de Capim Sudão, Mat. Média | NRC16F154 |
| 161 | 456 | Feno de Bagaço de Cana | NRC16F155 |
| 162 | 456 | Silagem de Bagaço de Cana | NRC16F156 |
| 163 | 456 | Farelo de Girassol | NRC16F157 |
| 164 | 456 | Semente de Girassol | NRC16F158 |
| 165 | 456 | Silagem de Girassol | NRC16F159 |
| 166 | 456 | Resíduo de Conserva e Milho Doce | NRC16F160 |
| 167 | 456 | Tapioca (Cassava) | NRC16F161 |
| 168 | 456 | Bagaço de Tomate | NRC16F162 |
| 169 | 457 | Grão de Triticale | NRC16F163 |
| 170 | 457 | Feno de Triticale | NRC16F164 |
| 171 | 457 | Silagem de Triticale | NRC16F165 |
| 172 | 457 | Silagem de Triticale Madura | NRC16F166 |
| 173 | 457 | Silagem de Triticale Mat. Média | NRC16F167 |
| 174 | 457 | Uréia | NRC16F168 |
| 175 | 457 | Farelo de Trigo | NRC16F169 |
| 176 | 457 | Grão de Trigo, Laminado | NRC16F170 |
| 177 | 457 | Feno de Trigo, com Grãos | NRC16F171 |
| 178 | 457 | Feno de Trigo, Vegetativo | NRC16F172 |
| 179 | 457 | Sêmola de Trigo | NRC16F173 |
| 180 | 457 | Silagem de Trigo, com Grãos | NRC16F174 |
| 181 | 458 | Silagem de Trigo, Vegetativa | NRC16F175 |
| 182 | 458 | Palha de Trigo | NRC16F176 |
| 183 | 458 | Soro de Leite, Seco | NRC16F177 |
| 184 | 458 | Soro de Leite, Úmido | NRC16F178 |

Notas: (i) nas posições 65–66 a 19-2 traz "Baixo Teor de Gordura" (PB 30.97) antes de "Alto Teor de Proteína" (PB 38.99), ao contrário da 19-1 (F60 alto proteína PB 39.0 antes de F61 baixo gordura PB 31.0) — a correspondência acima já troca F60/F61 pelo PB ⚠; (ii) pos. 94 ("Silagem de Misturas… Predominantemente Leguminosas, Imaturas") corresponde na 19-1 a F87 que é **feno** ⚠ rótulo trocado; (iii) pos. 96: o cabeçalho impresso está cortado ("...Predominantemente Leguminosas,") e corresponde a F88 "Silagem… Leguminosas Predominantes"; (iv) pos. 37–40 (nomes inferidos da 19-2) não existem na 19-1 legível.

### 6.3 Tabela 19-3 — 74 entradas (61 fontes únicas; 138 linhas elemento) por seção de elemento

Seções e págs.: Cálcio 459 (14) | Cloreto 460 (5) | Cobalto 460 (4) | Cobre 460–461 (3) | Iodo 461 (3) | Ferro 461 (4) | Magnésio 461 (6) | Manganês 462–463 (6) | Fósforo 463 (10) | Potássio 463–464 (4) | Selênio 464 (2) | Sódio 464 (4) | Enxofre 464 (5) | Zinco 464 (4). Lista completa com valores na seção 7.3.


## 7. Transcrição VERIFICADA NA IMAGEM (160–170 dpi) — amostra representativa

### 7.1 Tabela 19-1 — somente as MÉDIAS de 30 alimentos (de 88 transcritos; 22 páginas × 4). Vazio = célula em branco no livro. "cod" = NRC16Fnnn.

Por que só as médias: DP e N de cada célula estão no arquivo de apoio `/tmp/claude-0/nasem/notes/ch19_dados/tab19-1_parcial_88alimentos.csv` (mesmos 88 alimentos, colunas `<analito>_media`, `_dp`, `_n`). Valores de página: ver código→página na seção 6.1. Arredondamento mantido como impresso (MS/CZ/PB/FDA/FDN/amido: 1 casa; frações A/B/C/PNDR/dPNDR: inteiro; Kd: 1 casa; PIDA/PIDN/lignina: 2–3 casas no livro, aqui 2; AG/GB/ED: 2 casas; minerais macro: 2 casas; Fe/Mn/Zn: inteiro).

Bloco A — matéria seca, cinzas, proteína e frações de PB (MS em % da matéria natural; demais em % MS ou % PB conforme seção 3.1)

```csv
cod  , alimento              , MS  , CZ  , PB   , A  , B , C , KD  , PNDR, DPNDR, PSOL , PIDA, PIDN
F1   , Far.Alfafa            , 90.7, 11.7, 19.5 , 28 , 66, 6 , 6.7 , 36  , 75   , 37.0 , 1.62, 3.97
F34  , Feno gram.temp. MM    , 88.3, 8.6 , 13.3 , 30 , 56, 14, 5.5 , 42  , 60   , 30.5 , 1.43, 4.85
F93  , Feno legum. MM        , 88.1, 10.8, 20.7 , 45 , 45, 9 , 17.8, 22  , 65   , 34.6 , 0.74, 1.85
F94  , Silag.legum.imat.     , 41.6, 11.1, 22.1 , 62 , 29, 9 , 13.1, 21  , 70   , 55.2 , 1.60, 2.68
F48  , Silag.milho tipica    , 35.4, 3.8 , 7.7  , 60 , 24, 16, 4.1 , 33  , 70   , 51.8 , 0.82, 1.23
F1071, Milho seco grosso     , 86.9, 1.5 , 8.5  , 23 , 70, 7 , 5.4 , 43  , 73   , 22.1 , 0.52, 0.91
F8   , Cevada grao moido     , 88.7, 2.8 , 11.8 , 30 , 61, 9 , 22.7, 22  , 85   , 25.3 , 0.70, 1.38
F170 , Trigo grao moido      , 85.7, 2.1 , 13.5 , 31 , 54, 15, 19.1, 28  , 88   , 28.4 , 0.45, 1.59
F102 , Aveia laminada        , 89.3, 3.2 , 12.2 , 72 , 20, 8 , 26.4, 16  , 72   , 27.1 , 0.77, 1.21
F28  , Canola extr.solv.     , 89.1, 7.9 , 41.5 , 22 , 71, 7 , 10.5, 32  , 74   , 25.0 , 2.50, 4.75
F134 , Soja extr.48%PB       , 89.3, 7.2 , 52.6 , 18 , 79, 2 , 9.0 , 33  , 91   , 23.1 , 0.63, 1.00
F145 , Soja expellers        , 91.2, 6.7 , 47.6 , 9  , 91, 0 , 2.4 , 63  , 93   , 14.7 , 0.91, 3.61
F58  , Farelo algodao        , 89.9, 7.6 , 46.7 , 25 , 56, 19, 7.2 , 44  , 83   , 14.5 , 1.72, 2.22
F14  , Polpa beterraba seca  , 92.3, 5.2 , 9.9  , 5  , 90, 5 , 2.0 , 71  , 80   , 20.6 , 1.30, 5.46
F31  , Polpa citrica seca    , 88.2, 7.1 , 7.2  , 42 , 53, 5 , 7.4 , 30  , 80   , 40.3 , 1.03, 1.78
F59  , DDGS alto gord.       , 89.1, 5.4 , 30.2 , 26 , 62, 12, 5.0 , 47  , 75   , 15.7 , 2.85, 3.83
F118 , Farelo de arroz       , 92.4, 10.0, 14.8 , 31 , 45, 24, 3.4 , 53  , 85   , 30.5 , 0.78, 2.18
F169 , Farelo de trigo       , 90.1, 5.5 , 17.4 , 43 , 51, 6 , 24.2, 18  , 69   , 39.9 , 0.61, 3.10
F1000, Sangue alta dPNDR     , 90.9, 3.3 , 95.1 , 10 , 61, 29, 1.9 , 85  , 85   , 19.5 , 4.25, 5.67
F74  , Far.penas             , 92.9, 2.3 , 90.6 , 24 , 30, 45, 0.8 , 72  , 68   , 9.9  , 9.28, 12.70
F75  , Far.peixe             , 92.0, 21.1, 69.2 , 36 , 38, 26, 1.9 , 76  , 76   , 22.4 , 1.04, 4.05
F98  , Far.carne-ossos suinos, 96.1, 26.2, 56.6 , 32 , 42, 26, 8.8 , 44  , 61   , 14.9 , 2.84, 11.83
F117 , Far.subprod.aves      , 95.5, 14.2, 65.6 , 5  , 91, 5 , 2.0 , 71  , 90   , 28.2 , 3.89, 30.34
F71  , Oleo de soja          , 99.0,     ,      ,    ,   ,   ,     ,     ,      ,      ,     ,
F73  , Sebo                  , 99.8,     ,      ,    ,   ,   ,     ,     ,      ,      ,     ,
F25  , Sabao de Ca           , 95.3, 15.5,      ,    ,   ,   ,     ,     ,      ,      ,     ,
F168 , Ureia                 , 99.0,     , 281.0, 100, 0 , 0 , 0.0 , 0   ,      , 100.0,     ,
F101 , Melaco                , 65.4, 16.0, 9.3  , 74 , 26, 0 , 3.2 , 21  , 100  , 95.9 , 0.00, 0.00
F1075, Glicerol              , 80.0, 6.7 , 0.8  , 100, 0 , 0 , 0.0 , 0   , 100  , 100.0, 0.00, 0.00
F177 , Soro leite seco       , 92.6, 9.7 , 17.8 , 90 , 10, 0 , 5.0 , 11  , 95   , 91.1 , 0.22, 0.53
```

Bloco B — fibras, amido, açúcar, lipídios e energia

```csv
cod  , alimento              , FDA , FDN , DIVFDN, LIG , AMIDO, CSA , AGT  , GB    , ED
F1   , Far.Alfafa            , 33.9, 42.9, 49.1  , 7.55, 1.8  , 8.3 , 1.61 , 2.35  , 2.50
F34  , Feno gram.temp. MM    , 35.5, 58.0, 67.8  , 4.17, 2.2  , 15.2, 1.58 , 3.23  , 2.53
F93  , Feno legum. MM        , 32.1, 41.1, 52.4  , 6.64, 1.5  , 9.0 , 1.50 , 2.08  , 2.63
F94  , Silag.legum.imat.     , 32.0, 38.7, 53.3  , 6.55, 1.9  , 7.3 , 1.98 , 3.22  , 2.70
F48  , Silag.milho tipica    , 24.3, 40.9, 52.0  , 3.05, 32.9 , 3.0 , 2.35 , 2.92  , 2.93
F1071, Milho seco grosso     , 3.6 , 9.8 , 62.3  , 1.37, 70.4 , 2.9 , 3.84 , 3.84  , 3.10
F8   , Cevada grao moido     , 7.3 , 18.6, 51.5  , 1.72, 56.7 , 4.9 , 1.31 , 2.31  , 3.36
F170 , Trigo grao moido      , 4.2 , 12.5, 55.7  , 1.52, 63.0 , 5.9 , 1.78 , 1.98  , 3.56
F102 , Aveia laminada        , 14.5, 28.6, 35.9  , 3.20, 44.7 , 2.9 , 4.80 , 5.68  , 3.27
F28  , Canola extr.solv.     , 20.3, 29.0, 49.4  , 8.51, 1.6  , 11.0, 2.51 , 3.51  , 3.14
F134 , Soja extr.48%PB       , 7.2 , 11.1, 85.7  , 1.08, 1.9  , 13.0, 1.08 , 1.82  , 3.99
F145 , Soja expellers        , 10.1, 19.6,       , 2.06, 1.8  , 11.8, 6.12 , 7.12  , 3.90
F58  , Farelo algodao        , 19.2, 28.1,       , 7.01, 1.1  , 8.5 , 3.06 , 3.60  , 3.32
F14  , Polpa beterraba seca  , 28.2, 46.9, 79.0  , 3.88, 0.6  , 5.7 , 0.63 , 1.06  , 2.75
F31  , Polpa citrica seca    , 20.1, 24.1, 86.5  , 2.49, 1.3  , 23.0, 1.72 , 2.55  , 3.02
F59  , DDGS alto gord.       , 14.6, 32.1, 71.5  , 4.17, 4.5  , 4.6 , 11.39, 12.54 , 3.49
F118 , Farelo de arroz       , 13.8, 23.1, 23.3  , 4.94, 22.2 , 8.0 , 12.00, 18.50 , 3.22
F169 , Farelo de trigo       , 13.8, 40.1, 43.3  , 4.15, 20.8 , 8.0 , 4.02 , 4.39  , 3.06
F1000, Sangue alta dPNDR     , 0.0 , 0.0 ,       , 0.00, 0.0  , 0.0 , 1.31 , 1.69  , 4.56
F74  , Far.penas             , 0.0 , 0.0 ,       , 0.00, 0.0  , 0.0 , 7.85 , 8.92  , 4.12
F75  , Far.peixe             ,     ,     ,       ,     ,      ,     , 6.44 , 10.48 , 3.63
F98  , Far.carne-ossos suinos,     ,     ,       ,     ,      ,     , 7.45 , 11.90 , 3.25
F117 , Far.subprod.aves      ,     , 0.0 ,       , 0.00, 0.0  , 0.0 , 11.78, 12.78 , 4.25
F71  , Oleo de soja          ,     ,     ,       ,     ,      ,     , 88.00, 100.00, 6.22
F73  , Sebo                  ,     ,     ,       ,     ,      ,     , 88.00, 99.80 , 5.80
F25  , Sabao de Ca           ,     ,     ,       ,     ,      ,     , 84.50, 84.50 , 5.42
F168 , Ureia                 ,     , 0.0 ,       , 0.00, 0.0  ,     ,      ,       , 2.21
F101 , Melaco                , 0.2 , 0.6 ,       , 0.00, 0.8  , 60.0, 0.00 , 0.61  , 3.07
F1075, Glicerol              , 0.0 , 0.0 , 0.0   , 0.00, 0.0  , 1.4 , 5.24 , 6.24  , 3.29
F177 , Soro leite seco       , 0.3 , 0.6 ,       , 0.23, 1.4  , 56.1, 5.27 , 6.27  , 3.62
```

Bloco C — minerais (macro % MS; micro mg/kg MS)

```csv
cod  , alimento              , CA  , P   , MG  , K   , NA  , CL  , S   , CU   , FE  , MN , ZN , MO
F1   , Far.Alfafa            , 1.50, 0.27, 0.30, 2.33, 0.12, 0.67, 0.26, 8.83 , 951 , 50 , 23 , 1.71
F34  , Feno gram.temp. MM    , 0.48, 0.28, 0.23, 2.26, 0.10, 0.78, 0.20, 9.21 , 217 , 86 , 27 , 1.69
F93  , Feno legum. MM        , 1.40, 0.28, 0.32, 2.39, 0.21, 0.76, 0.18, 9.69 , 421 , 38 , 26 , 2.53
F94  , Silag.legum.imat.     , 1.30, 0.35, 0.33, 2.79, 0.16, 0.80, 0.22, 11.44, 685 , 62 , 30 , 3.51
F48  , Silag.milho tipica    , 0.24, 0.23, 0.17, 0.99, 0.03, 0.26, 0.10, 6.22 , 165 , 30 , 27 , 1.11
F1071, Milho seco grosso     , 0.04, 0.31, 0.13, 0.56, 0.02, 0.10, 0.10, 2.07 , 39  , 7  , 23 , 0.91
F8   , Cevada grao moido     , 0.12, 0.38, 0.14, 0.59, 0.02, 0.15, 0.14, 5.53 , 89  , 20 , 34 , 1.05
F170 , Trigo grao moido      , 0.10, 0.36, 0.13, 0.47, 0.01, 0.13, 0.15, 4.45 , 71  , 43 , 32 , 1.00
F102 , Aveia laminada        , 0.13, 0.38, 0.14, 0.56, 0.01, 0.14, 0.16, 6.58 , 129 , 53 , 33 , 1.36
F28  , Canola extr.solv.     , 0.79, 1.15, 0.62, 1.36, 0.08, 0.10, 0.77, 5.78 , 253 , 73 , 64 , 1.12
F134 , Soja extr.48%PB       , 0.40, 0.74, 0.33, 2.42, 0.02, 0.06, 0.41, 16.06, 187 , 41 , 53 , 4.32
F145 , Soja expellers        , 0.34, 0.72, 0.31, 2.24, 0.01, 0.06, 0.40, 15.12, 196 , 39 , 53 , 2.72
F58  , Farelo algodao        , 0.25, 1.31, 0.70, 1.74, 0.17, 0.08, 0.48, 12.48, 208 , 23 , 66 , 1.76
F14  , Polpa beterraba seca  , 0.77, 0.08, 0.26, 0.49, 0.11, 0.08, 0.20, 8.10 , 588 , 78 , 21 , 1.00
F31  , Polpa citrica seca    , 1.86, 0.12, 0.14, 1.06, 0.06, 0.11, 0.10, 6.85 , 108 , 10 , 13 , 1.37
F59  , DDGS alto gord.       , 0.12, 0.88, 0.34, 1.26, 0.21, 0.19, 0.67, 4.15 , 94  , 18 , 64 , 1.11
F118 , Farelo de arroz       , 0.78, 1.77, 0.78, 1.40, 0.02, 0.13, 0.17, 8.64 , 216 , 183, 61 , 1.14
F169 , Farelo de trigo       , 0.13, 1.05, 0.43, 1.22, 0.03, 0.11, 0.19, 10.76, 163 , 133, 77 , 1.37
F1000, Sangue alta dPNDR     , 0.13, 0.28, 0.05, 0.43, 0.42, 0.35, 0.74, 6.05 , 2267, 4  , 33 ,
F74  , Far.penas             , 0.50, 0.32, 0.04, 0.18, 0.16, 0.23, 1.78, 9.12 , 347 , 12 , 87 , 1.00
F75  , Far.peixe             , 5.56, 3.16, 0.24, 0.93, 0.82, 1.06, 0.88, 6.02 , 804 , 44 , 92 , 1.48
F98  , Far.carne-ossos suinos, 9.29, 4.59, 0.28, 0.91, 0.74, 0.49, 0.51, 20.01, 451 , 24 , 160,
F117 , Far.subprod.aves      , 4.31, 2.48, 0.16, 0.89, 0.38, 0.55, 0.74, 14.14, 233 , 45 , 122, 1.20
F71  , Oleo de soja          ,     ,     ,     ,     ,     ,     ,     ,      ,     ,    ,    ,
F73  , Sebo                  ,     ,     ,     ,     ,     ,     ,     ,      ,     ,    ,    ,
F25  , Sabao de Ca           ,     ,     ,     ,     ,     ,     ,     ,      ,     ,    ,    ,
F168 , Ureia                 ,     ,     ,     ,     ,     ,     ,     ,      ,     ,    ,    ,
F101 , Melaco                , 0.73, 0.26, 0.28, 4.49, 1.51, 2.02, 0.64, 36.71, 216 , 74 , 112,
F1075, Glicerol              , 0.08, 0.19, 0.07, 0.53, 2.48, 4.49, 1.18, 5.08 ,     , 22 , 7  ,
F177 , Soro leite seco       , 0.92, 0.89, 0.14, 2.60, 0.74, 1.65, 0.24, 1.24 , 11  , 1  , 5  ,
```

Bloco D — Média;DP;N para 8 alimentos (PB, FDN, amido, Ca, P, Fe) — exemplo do formato completo

```csv
cod  , PB            , FDN            , AMIDO          , CA              , P               , FE    # célula = Média;DP;N
F1   , 19.5;2.0;705  , 42.9;4.7;707   , 1.8;1.0;660    , 1.50;0.29;619   , 0.27;0.05;618   , 951;680.4;288
F8   , 11.8;1.7;2421 , 18.6;3.4;2400  , 56.7;4.3;2417  , 0.12;0.19;1780  , 0.38;0.06;1862  , 89;54.2;716
F28  , 41.5;1.6;3437 , 29.0;2.8;1503  , 1.6;0.8;554    , 0.79;0.12;1211  , 1.15;0.11;1212  , 253;96.3;894
F134 , 52.6;1.7;1400 , 11.1;3.1;1220  , 1.9;1.1;403    , 0.40;0.10;983   , 0.74;0.07;985   , 187;112.8;654
F48  , 7.7;0.9;536303, 40.9;4.8;536939, 32.9;6.4;536519, 0.24;0.05;336426, 0.23;0.03;337092, 165;108.4;60879
F14  , 9.9;1.4;54    , 46.9;4.3;54    , 0.6;0.4;48     , 0.77;0.25;51    , 0.08;0.01;50    , 588;262.2;50
F1000, 95.1;3.1;845  , 0.0;;          , 0.0;;          , 0.13;0.16;166   , 0.28;0.16;172   , 2267;476.5;133
F170 , 13.5;2.4;2120 , 12.5;2.7;2044  , 63.0;4.4;2038  , 0.10;0.16;1694  , 0.36;0.08;1727  , 71;63.2;557
```

Validações automáticas feitas nos 88 alimentos transcritos: (a) A+B+C = 100 ± 1 em **todos** os alimentos com frações (os óleos/gorduras e a ureia não têm frações); (b) PB da 19-1 vs PB da 19-2: coincidem (|Δ| ≤ 0.15) em todos os alimentos comuns, exceto farinha de sangue (95.1 vs 96.97, ambas dPNDR) e resíduo de cervejaria seco (25.3 vs 25.49); (c) AG total da 19-1 = AG total da 19-2 em todos os alimentos comuns; (d) ED e AGT conferidos com Eq. 19-1 a 19-4 (seção 4).


### 7.2 Tabela 19-2 — 22 alimentos (de 60 transcritos nas pp.443, 444, 445, 449, 455), valores conferidos na imagem; soma dos AG conferida

Colunas: `pos` = posição na 19-2 (seção 6.2); PB em % MS; Arg…Val em % da PB; AGT em % MS; C12:0…Outros em % do AG total. Vazio = célula em branco no livro. Os 60 alimentos transcritos (59 com perfil de AG; glicerol só tem AG total) têm soma de AG (C12:0…Outros) entre 99.99 e 100.02; arquivo completo de apoio: `/tmp/claude-0/nasem/notes/ch19_dados/tab19-2_parcial_60alimentos.csv`.

Bloco A — PB e aminoácidos (% PB)

```csv
pos, alimento                                     , PB   , Arg , His , Ile , Leu  , Lys , Met , Phe , Thr , Trp , Val
1  , Farinha de Alfafa                            , 19.51, 4.04, 1.87, 3.80, 6.57 , 4.40, 1.27, 4.40, 3.92, 1.63, 4.82
2  , Cascas de Amêndoas                           , 5.25 , 2.23, 0.86, 2.35, 4.05 , 2.74, 0.90, 2.80, 2.70, 1.00, 3.53
8  , Grão de Cevada, Moído, Seco                  , 11.81, 4.91, 2.22, 3.43, 6.76 , 3.61, 1.67, 5.09, 3.33, 1.20, 4.81
18 , Feno de Capim Bermuda                        , 10.99, 3.88, 1.63, 3.32, 6.22 , 3.49, 1.30, 3.92, 3.60, 1.24, 4.51
21 , Farinha de Sangue, Alta dPNDR                , 96.97, 4.20, 6.00, 1.08, 12.40, 8.77, 1.15, 6.79, 4.55, 1.58, 8.32
23 , Resíduo de Cervejaria, Seco                  , 25.49, 5.80, 2.28, 4.02, 8.30 , 3.55, 2.14, 5.54, 3.59, 1.34, 5.47
25 , Levedura de Cerveja, Seca                    , 50.72, 0.85, 0.45, 0.71,      , 0.65, 0.34, 0.67, 0.60, 0.13, 0.81
27 , Sabão de Cálcio                              , 0.00 ,     ,     ,     ,      ,     ,     ,     ,     ,     ,
29 , Subprodutos de Doces, Alta Proteína          , 14.63, 2.25, 1.57, 3.60, 6.52 , 2.25, 1.57, 3.82, 3.82, 0.67, 5.84
30 , Farelo de Canola, Extraído com Solvente      , 41.49, 5.93, 2.66, 3.93, 6.92 , 5.51, 1.97, 4.00, 4.43, 1.34, 5.11
33 , Polpa Cítrica, Seca                          , 7.19 , 3.72, 1.70, 2.88, 5.25 , 2.72, 1.04, 3.62, 2.94, 0.95, 3.85
35 , Feno de Gramíneas Temperadas, Maduras        , 9.23 , 4.10, 1.94, 3.96, 7.39 , 4.85, 1.64, 4.78, 4.10, 2.09, 5.22
76 , Óleo de Soja, Gordura                        ,      ,     ,     ,     ,      ,     ,     ,     ,     ,     ,
78 , Sebo, Gordura                                ,      ,     ,     ,     ,      ,     ,     ,     ,     ,     ,
79 , Farinha de Penas                             , 90.55, 6.56, 1.21, 4.60, 8.13 , 2.60, 0.70, 4.77, 4.53, 0.76, 7.01
80 , Farinha de Peixe                             , 69.19, 5.63, 2.35, 3.89, 6.74 , 6.82, 2.53, 3.73, 3.89, 0.96, 4.59
83 , Subproduto de Frutas e Vegetais, Úmido       , 13.62, 4.00, 2.94, 3.50, 12.70, 2.78, 2.50, 4.72, 3.59, 0.69, 4.78
84 , Glicerol                                     ,      ,     ,     ,     ,      ,     ,     ,     ,     ,     ,
150, Farelo de Soja, Expellers                    , 47.60, 7.29, 2.62, 4.54, 7.59 , 6.12, 1.34, 5.05, 3.90, 1.34, 4.73
152, Farelo de Soja, Extraído com Solvente, 48% PB, 52.64, 7.29, 2.64, 4.54, 7.63 , 6.16, 1.38, 5.03, 3.95, 1.38, 4.76
154, Soja Integral Crua                           , 39.98, 7.25, 2.61, 4.53, 7.58 , 6.14, 1.33, 5.03, 3.89, 1.33, 4.72
156, Grãos de Trigo                               , 12.90, 4.79, 2.15, 3.45, 6.54 , 2.76, 1.54, 4.45, 2.95, 1.36, 4.44
```

Bloco B — AG total e perfil de AG (% do AG total)

```csv
pos, alimento                                     , AGT  , C12:0, C14:0, C16:0, C16:1, C18:0, C18:1t, C18:1c, C18:2, C18:3, Outros
1  , Farinha de Alfafa                            , 1.61 , 1.17 , 0.58 , 20.10, 1.71 , 3.35 ,       , 3.02  , 21.07, 44.93, 4.09
2  , Cascas de Amêndoas                           , 1.26 , 0.22 , 0.05 , 14.49, 0.26 , 3.91 ,       , 50.82 , 23.39, 3.25 , 3.61
8  , Grão de Cevada, Moído, Seco                  , 1.31 ,      , 0.32 , 22.97, 0.05 , 1.53 ,       , 13.54 , 55.93, 4.34 , 1.32
18 , Feno de Capim Bermuda                        , 1.25 , 2.82 , 1.18 , 30.30, 1.42 , 3.99 , 1.14  , 3.32  , 18.79, 20.75, 16.29
21 , Farinha de Sangue, Alta dPNDR                , 1.31 , 0.11 , 1.48 , 21.62, 1.02 , 21.66, 5.13  , 26.47 , 14.89, 0.46 , 7.16
23 , Resíduo de Cervejaria, Seco                  , 8.31 , 0.14 , 0.73 , 26.69, 0.20 , 2.24 ,       , 14.60 , 48.87, 4.57 , 1.95
25 , Levedura de Cerveja, Seca                    , 0.11 ,      ,      ,      ,      ,      ,       ,       ,      ,      , 100.00
27 , Sabão de Cálcio                              , 84.50, 0.20 , 1.60 , 50.80,      , 4.10 ,       , 35.70 , 7.00 , 0.20 , 0.40
29 , Subprodutos de Doces, Alta Proteína          , 11.11, 6.54 , 5.13 , 18.24, 0.14 , 18.81, 9.08  , 30.81 , 7.78 , 0.58 , 2.89
30 , Farelo de Canola, Extraído com Solvente      , 2.51 ,      , 0.19 , 9.76 , 0.90 , 2.24 , 0.61  , 45.21 , 31.45, 7.71 , 1.92
33 , Polpa Cítrica, Seca                          , 1.72 , 0.67 , 0.56 , 26.85, 0.59 , 4.93 , 0.05  , 23.30 , 34.92, 6.42 , 1.70
35 , Feno de Gramíneas Temperadas, Maduras        , 0.95 , 0.89 ,      , 15.22, 1.48 , 1.29 ,       , 2.52  , 16.62, 55.50, 6.49
76 , Óleo de Soja, Gordura                        , 88.00, 0.11 , 0.11 , 10.83, 0.14 , 3.89 ,       , 22.82 , 53.75, 8.23 , 0.13
78 , Sebo, Gordura                                , 88.00, 0.09 , 3.00 , 24.43, 3.79 , 17.92, 3.99  , 41.62 , 1.09 , 0.53 , 3.54
79 , Farinha de Penas                             , 7.85 , 0.34 , 1.09 , 24.33, 6.51 , 8.27 , 1.09  , 32.51 , 13.19, 0.54 , 12.13
80 , Farinha de Peixe                             , 6.44 ,      , 10.35, 28.46, 13.01, 6.00 , 0.20  , 10.97 , 1.09 , 0.96 , 28.96
83 , Subproduto de Frutas e Vegetais, Úmido       , 6.13 ,      , 0.26 , 13.57, 0.19 , 1.83 ,       , 25.99 , 55.08, 1.64 , 1.44
84 , Glicerol                                     , 5.24 ,      ,      ,      ,      ,      ,       ,       ,      ,      ,
150, Farelo de Soja, Expellers                    , 6.12 ,      , 0.07 , 11.55, 0.09 , 3.71 , 1.42  , 18.13 , 54.77, 9.52 , 0.75
152, Farelo de Soja, Extraído com Solvente, 48% PB, 1.08 ,      , 0.83 , 17.28,      , 4.45 , 0.43  , 13.22 , 54.16, 8.43 , 1.20
154, Soja Integral Crua                           , 16.99, 0.58 , 0.20 , 11.93, 0.08 , 4.05 ,       , 21.99 , 52.43, 7.59 , 1.17
156, Grãos de Trigo                               , 1.66 ,      , 0.23 , 19.50,      , 1.08 ,       , 14.66 , 60.20, 4.32 ,
```

Observações verificadas na imagem: (i) óleos/gorduras (pos. 73–78): AG total = 88.00 % MS em todos, sem PB/AA; (ii) glicerol (pos. 84): **só** AG total = 5.24; (iii) levedura de cerveja (pos. 25–26): AA impressos muito baixos (Arg 0.85 % da PB etc.) e AG só "Outros = 100.00" ⚠ (valores atípicos; provável unidade/escala diferente); (iv) sabão de cálcio (pos. 27): PB 0.00 e AG total 84.50, perfil de AG de palma (C16:0 50.80; C18:1 cis 35.70); (v) pos. 83 (subproduto de frutas/vegetais úmido): Leu = 12.70 % da PB ⚠ fora da faixa dos demais alimentos (2–9 %); (vi) perfis de AA e AG idênticos entre alimentos relacionados (cevada: pos. 8, 9, 11; oleaginosas: canola; soja; polpa de beterraba) — são **copiados**, não medidos por alimento; (vii) Farinha de sangue alta e baixa dPNDR têm perfis idênticos (pos. 21/22).

### 7.3 Tabela 19-3 — transcrição COMPLETA (74 entradas), verificada na imagem das pp.459–464

Colunas: seção do elemento | pág. | código | fonte | mineral primário `elem/%/coef` | secundário | menor 1 | menor 2 | menor 3. `%` = concentração do elemento na fonte (% MS, base 100 % MS, exceto ácido fosfórico a 75 % MS); `coef` = coeficiente de absorção (fração); N/A = não aplicável. Arquivo de apoio em formato longo (138 linhas elemento): `/tmp/claude-0/nasem/notes/ch19_dados/tab19-3_completa.csv`.

```csv
secao   , pag, codigo    , fonte                                                        , primario      , secundario  , menor1     , menor2     , menor3
Cálcio  , 459, NRC16F1011, Farinha de ossos                                             , Ca/31.0/0.60  , P/12.9/0.80 , Na/5.7/1.00, Fe/2.7/0.01, S/2.5/N/A
Cálcio  , 459, NRC16F1003, Carbonato de cálcio, CaCO3                                   , Ca/39.4/0.50  ,             ,            ,            ,
Cálcio  , 459, NRC16F1004, Cloreto de cálcio anidro, CaCl2                              , Ca/36.1/0.60  , Cl/63.9/0.92,            ,            ,
Cálcio  , 459, NRC16F1005, Cloreto de cálcio dihidrato, CaCl2·2H2O                      , Ca/27.5/0.60  , Cl/48.2/0.92,            ,            ,
Cálcio  , 459, NRC16F1006, Hidróxido de cálcio, Ca(OH)2                                 , Ca/54.1/0.60  ,             ,            ,            ,
Cálcio  , 459, NRC16F1009, Óxido de cálcio, CaO                                         , Ca/71.5/0.33  ,             ,            ,            ,
Cálcio  , 459, NRC16F1007, Fosfato de cálcio (dibásico), CaHPO4                         , Ca/22.0/0.60  , P/19.3/0.75 , Fe/1.4/0.01,            ,
Cálcio  , 459, NRC16F1008, Fosfato de cálcio (monobásico), Ca(H2PO4)2                   , Ca/16.4/0.60  , P/21.6/0.80 , Fe/1.6/0.01,            ,
Cálcio  , 459, NRC16F1010, Sulfato de cálcio dihidratado, CaSO4·2H2O                    , Ca/23.3/0.60  , S/23.5/N/A  ,            ,            ,
Cálcio  , 459, NRC16F1012, Calcário dolomítico (magnésio)                               , Ca/22.3/0.45  , Mg/10.0/0.12,            ,            ,
Cálcio  , 459, NRC16F1013, Pedra calcária, moída                                        , Ca/35.0/0.45  , Mg/1.0/0.12 ,            ,            ,
Cálcio  , 459, NRC16F1014, Ostra, moída                                                 , Ca/38.0/0.50  ,             ,            ,            ,
Cálcio  , 459, NRC16F1024, Fosfato, Curaçao                                             , Ca/35.1/0.45  , P/14.1/0.85 ,            ,            ,
Cálcio  , 459, NRC16F1025, Fosfato, defluorado                                          , Ca/32.0/0.45  , P/18.0/0.65 , Na/4.9/1.00,            ,
Cloreto , 460, NRC16F1069, Cloreto de amônio, NH4Cl                                     , Cl/66.3/0.92  ,             ,            ,            ,
Cloreto , 460, NRC16F1004, Cloreto de cálcio anidro, CaCl2                              , Cl/63.9/0.92  , Ca/36.1/0.60,            ,            ,
Cloreto , 460, NRC16F1015, Cloreto de magnésio hexahidratado, MgCl2·6H2O                , Cl/34.9/0.92  , Mg/12.0/0.27,            ,            ,
Cloreto , 460, NRC16F1016, Cloreto de potássio, KCl                                     , Cl/50.0/0.92  , K/50.0/1.00 ,            ,            ,
Cloreto , 460, NRC16F1017, Cloreto de sódio (sal), NaCl                                 , Cl/60.7/0.92  , Na/39.3/1.00,            ,            ,
Cobalto , 460, NRC16F1038, Carbonato de cobalto, CoCO3                                  , Co/46.0/N/A   ,             ,            ,            ,
Cobalto , 460, NRC16F1039, Carbonato de cobalto hexahidratado, CoCO3·6H2O               , Co/25.9/N/A   ,             ,            ,            ,
Cobalto , 460, NRC16F1040, Cloreto de cobalto hexahidratado, CoCl2·6H2O                 , Co/24.8/N/A   , Cl/29.8/0.92,            ,            ,
Cobalto , 460, NRC16F1041, Sulfato de cobalto heptahidratado, CoSO4·7H2O                , Co/21.0/N/A   , S/11.4/N/A  ,            ,            ,
Cobre   , 460, NRC16F1043, Cloreto de cobre dihidratado, CuCl2·2H2O                     , Cu/37.2/0.05  , Cl/41.7/0.92,            ,            ,
Cobre   , 460, NRC16F1045, Óxido de cobre, CuO                                          , Cu/79.9/0.005 ,             ,            ,            ,
Cobre   , 461, NRC16F1044, Sulfato de cobre pentahidratado, CuSO4·5H2O                  , Cu/25.5/0.05  , S/12.8/N/A  ,            ,            ,
Iodo    , 461, NRC16F1048, Iodato de cálcio, Ca(IO3)2                                   , I/63.5/N/A    , Ca/10.0/0.60,            ,            ,
Iodo    , 461, NRC16F1047, Dihidroiodeto de etilenodiamina (EDDI)                       , I/80.3/N/A    ,             ,            ,            ,
Iodo    , 461, NRC16F1031, Iodeto de potássio, KI                                       , I/68.8/N/A    , K/21.0/1.00 ,            ,            ,
Ferro   , 461, NRC16F1051, Carbonato ferroso, FeCO3                                     , Fe/38.0/0.10  ,             ,            ,            ,
Ferro   , 461, NRC16F1049, Sulfato ferroso heptahidratado, FeSO4·7H2O                   , Fe/21.8/0.20  , S/12.4/N/A  ,            ,            ,
Ferro   , 461, NRC16F1050, Sulfato ferroso monohidrato, FeSO4·H2O                       , Fe/32.9/0.20  , S/18.9/N/A  ,            ,            ,
Ferro   , 461, NRC16F1052, Óxido de ferro, FeO                                          , Fe/60.0/0.01  ,             ,            ,            ,
Magnésio, 461, NRC16F1012, Calcário dolomítico (magnésio)                               , Mg/10.0/0.12  , Ca/22.0/0.45,            ,            ,
Magnésio, 461, NRC16F1018, Carbonato de magnésio, MgCO3                                 , Mg/30.8/0.23  ,             ,            ,            ,
Magnésio, 461, NRC16F1015, Cloreto de magnésio hexahidratado, MgCl2·6H2O                , Mg/12.0/0.27  , Cl/34.9/0.92,            ,            ,
Magnésio, 461, NRC16F1019, Hidróxido de magnésio, Mg(OH)2                               , Mg/41.7/0.23  ,             ,            ,            ,
Magnésio, 461, NRC16F1020, Óxido de magnésio, MgO                                       , Mg/56.2/0.23  , Ca/<1/0.45  ,            ,            ,
Magnésio, 461, NRC16F1021, Sulfato de magnésio heptahidratado, MgSO4·7H2O               , Mg/9.8/0.27   , S/13.3/N/A  ,            ,            ,
Manganês, 462, NRC16F1056, Carbonato de manganês, MnCO3                                 , Mn/47.8/0.0015,             ,            ,            ,
Manganês, 462, NRC16F1054, Cloreto de manganês, MnCl2                                   , Mn/43.0/0.005 , Cl/56.3/0.92,            ,            ,
Manganês, 462, NRC16F1055, Cloreto de manganês tetrahidratado, MnCl2·4H2O               , Mn/27.7/0.005 , Cl/35.8/0.92,            ,            ,
Manganês, 463, NRC16F1059, Óxido de manganês, MnO                                       , Mn/77.5/0.003 ,             ,            ,            ,
Manganês, 463, NRC16F1057, Sulfato de manganês monohidratado, MnSO4·H2O                 , Mn/32.5/0.005 , S/19.0/N/A  ,            ,            ,
Manganês, 463, NRC16F1058, Sulfato de manganês pentahidratado, MnSO4·5H2O               , Mn/22.8/0.005 , S/13.3/N/A  ,            ,            ,
Fósforo , 463, NRC16F1022, Fosfato de amônio (dibásico), (NH4)2HPO4                     , P/20.6/0.80   ,             , S/2.2/N/A  , Fe/1.2/0.01,
Fósforo , 463, NRC16F1023, Fosfato de amônio (monobásico), (NH4)H2PO4                   , P/24.7/0.80   ,             , S/1.5/N/A  , Fe/1.7/0.01,
Fósforo , 463, NRC16F1011, Farinha de ossos                                             , P/12.9/0.80   , Ca/31.0/0.60, Na/5.7/1.00, Fe/2.7/0.01, S/2.5/N/A
Fósforo , 463, NRC16F1007, Fosfato de cálcio (dibásico), CaHPO4                         , P/19.3/0.75   , Ca/22.0/0.60, Fe/1.4/0.01,            ,
Fósforo , 463, NRC16F1008, Fosfato de cálcio (monobásico), Ca(H2PO4)2                   , P/21.6/0.80   , Ca/16.4/0.60, Fe/1.6/0.01,            ,
Fósforo , 463, NRC16F1024, Fosfato, curaçao                                             , P/14.1/0.85   , Ca/35.1/0.45,            ,            ,
Fósforo , 463, NRC16F1025, Fosfato defluorado                                           , P/18.0/0.65   , Ca/32.0/0.45, Na/4.9/1.00,            ,
Fósforo , 463, NRC16F1026, Fosfato monossódico, NaH2PO4·H2O                             , P/22.5/0.90   , Na/16.7/1.00,            ,            ,
Fósforo , 463, NRC16F1027, Ácido fosfórico, H3PO4                                       , P/31.6/0.90   ,             ,            ,            ,
Fósforo , 463, NRC16F1028, Tripolifosfato de sódio, Na5P3O10                            , P/25.0/0.75   , Na/31.0/1.00,            ,            ,
Potássio, 463, NRC16F1029, Bicarbonato de potássio, KHCO3                               , K/39.1/1.00   ,             ,            ,            ,
Potássio, 463, NRC16F1030, Carbonato de potássio, K2CO3                                 , K/56.6/1.00   ,             ,            ,            ,
Potássio, 464, NRC16F1016, Cloreto de potássio, KCl                                     , K/50.0/1.00   , Cl/50.0/0.92,            ,            ,
Potássio, 464, NRC16F1032, Sulfato de potássio, K2SO4                                   , K/41.8/1.00   , S/17.4/N/A  ,            ,            ,
Selênio , 464, NRC16F1061, Selenito de sódio, Na2SeO3                                   , Se/45.6/N/A   , Na/36.6/1.00,            ,            ,
Selênio , 464, NRC16F1062, Selenato de sódio decahidrato, Na2SeO4·10H2O                 , Se/21.4/N/A   , Na/12.5/1.00,            ,            ,
Sódio   , 464, NRC16F1033, Bicarbonato de sódio, NaHCO3                                 , Na/27.0/1.00  ,             ,            ,            ,
Sódio   , 464, NRC16F1034, Carbonato de sódio monohidrato, Na2CO3·H2O (impresso "NaCO3"), Na/37.1/1.00  ,             ,            ,            ,
Sódio   , 464, NRC16F1017, Cloreto de sódio (sal), NaCl                                 , Na/39.3/1.00  , Cl/60.7/0.92,            ,            ,
Sódio   , 464, NRC16F1035, Sesquicarbonato de sódio desidratado, Na2CO3+NaHCO3·2H2O     , Na/30.5/1.00  ,             ,            ,            ,
Enxofre , 464, NRC16F1037, Sulfato de amônio, (NH4)2SO4                                 , S/24.1/N/A    ,             ,            ,            ,
Enxofre , 464, NRC16F1010, Sulfato de cálcio dihidratado, CaSO4·2H2O                    , S/23.5/N/A    , Ca/23.3/0.60,            ,            ,
Enxofre , 464, NRC16F1021, Sulfato de magnésio heptahidratado, MgSO4·7H2O               , S/13.3/N/A    , Mg/9.8/0.27 ,            ,            ,
Enxofre , 464, NRC16F1032, Sulfato de potássio, K2SO4                                   , S/17.4/N/A    , K/41.8/1.00 ,            ,            ,
Enxofre , 464, NRC16F1036, Sulfato de sódio, Na2SO4                                     , S/10.0/N/A    , Na/14.3/1.00,            ,            ,
Zinco   , 464, NRC16F1064, Carbonato de zinco, ZnCO3                                    , Zn/52.1/0.20  ,             ,            ,            ,
Zinco   , 464, NRC16F1065, Cloreto de zinco, ZnCl2                                      , Zn/48.0/0.20  , Cl/52.0/0.92,            ,            ,
Zinco   , 464, NRC16F1066, Óxido de zinco, ZnO                                          , Zn/78.0/0.16  ,             ,            ,            ,
Zinco   , 464, NRC16F1067, Sulfato de zinco monohidratado, ZnSO4·H2O                    , Zn/36.4/0.20  , S/17.7/N/A  ,            ,            ,
```

Notas de verificação da 19-3: (a) farinha de ossos: Fe = 2.7 % e coeficiente impresso "00.1" na p.463 (corrigido pela imagem/p.459 = **0.01**); (b) a OCR leu "2.1" e "4718" (corrigido pela imagem: Fe 2.7; MnCO3 Mn 47.8); (c) calcário dolomítico: p.459 traz Ca 22.3 e Mg 10.0; p.461 traz Mg 10.0 e Ca 22.0 ⚠ (divergência de 0.3 pt na mesma fonte); (d) KCl impresso K 50.0 / Cl 50.0 (soma 100; teórico 52.4/47.6) e KI com I 68.8 / K 21.0 (soma 89.8; teórico 76.4/23.6) ⚠ composições "comerciais", não estequiométricas; (e) "NaCO3·H2O" na p.464 é **Na2CO3·H2O** (erro de impressão do índice); (f) óxido de magnésio: Ca = "<1" (impresso como texto; coef 0.45); (g) coeficientes de Mg dependem de K da dieta = 1.2 % (nota d, p.464); coeficiente de Cl = 0.92 em todas as fontes; Na e K = 1.00; Ca 0.60 (fontes puras), 0.45–0.50 (calcários/fosfatos naturais), 0.33 (CaO); P 0.75–0.90 (0.65 defluorado); Cu 0.05 (0.005 óxido); Zn 0.20 (0.16 óxido); Mn 0.005 (0.0015 carbonato; 0.003 óxido); Fe 0.20 (sulfatos), 0.10 carbonato, 0.01 óxido e Fe traço das fosfatadas; Co, I e Se = N/A (sem coeficiente de absorção; Co/Cr/I só nesta tabela, não nos alimentos); (h) códigos NRC16F10xx não impressos: 1042, 1046, 1053, 1060, 1063, 1068 (faixa 1003–1069); (i) Tab. 19-3 não tem DP/N (valores de composição química ideal/comercial).


## 8. Regras, lógica no simulador, limitações e conceitos

### 8.1 Regras para uso da biblioteca (restrições/convenções que o simulador deve respeitar)
1. **Tudo em base MS, exceto MS (% da matéria natural)**; o simulador converte a dieta pela ingestão de MS de cada ingrediente (Cap. 20: `Fd_DMInp_f`, ver `ch20A_modelo_p466-484.md`) [pp.393–394].
2. **Branco ≠ 0**: célula vazia = sem dado (não usar 0); "0" = analito medido abaixo do limite de detecção; média sem DP/N = fonte única/literatura [p.442, nota a].
3. **Proteínas de origem animal**: FDA, FDN, CSA, amido e lignina são **fixados em 0** (artefato analítico); a soma dos componentes de um alimento animal pode passar de 100 % (PB = N × 6.25 superestima) [pp.395–396].
4. **Gordura**: o modelo usa **AG total (AGT)**, não GB; AGT estimado = GB − 1 (concentrados) ou GB × 0.5678 (forragens) quando não medido [p.395]. Nos óleos/gorduras AGT impresso = 88.00 % MS (GB 100 ou 99.8; MS 99.0 ou 99.8), isto é, AGT < GB; o restante da MS entra como TG/glicerol na Eq. 19-2 [pp.414–416, 449] (interpretação).
5. **CSA e proteína solúvel**: só referência (não entram em equação) [pp.395–396]; GB, idem. Fibra bruta não existe na tabela [p.395].
6. **Matéria orgânica residual (MOR)** = 100 − (cinzas + AG + PB + FDN + amido): pode ser negativa (ex.: farinha de penas = −0.8 pelos dados impressos) e **é mantida** [p.395]. (Cap. 20 calcula `Fd_rOM` por outra expressão: ver notas ch20A.)
7. **ED base é um valor padrão** (IMS 3.5 % PC; amido 26 %; FDN 30 %); o simulador **recalcula** ED/EM/ELL da dieta com as equações do Cap. 3 (efeito da ingestão e da composição da dieta) [p.395]. Para alimentos novos ou editados pelo usuário, aplicar as equações do Cap. 3 (alimentos gerais) ou 19-1…19-4 (lipídios, proteína animal, açúcares/glicerol) com energia endógena 0.318 Mcal/kg.
8. **PNDR (% PB) impressa é calculada** para vaca de 650 kg a 23 kg MS; no simulador a PNDR por alimento deve ser **recalculada** pelas equações do Cap. 6/20 com Kd da fração B (coluna "Kd de B"), A, B, C e a taxa de passagem da dieta (`Fd_KdRUP`, `Fd_dcRUP`; interpretação a partir das notas ch20A: a coluna dPNDR da 19-1 = `Fd_dcRUP`, % da PNDR) [p.396, p.442] ⚠ confirmar com ch06/ch20.
9. **Classes (12) e tipos (3) do alimento** governam várias equações (p.393), mas **não são impressas por alimento**. O Cap. 20 define 14 "categorias de ingrediente" (Tab. 20-7, p.477: aditivo, proteína animal, subproduto/outro, alimento líquido p/ bezerras, fonte energética, suplementos de gordura [AG livres e TG], forragem com grãos, gramínea/leguminosa forrageira, pastagem, proteína vegetal, açúcar/álcool, vitaminas/minerais) e o indicador `Fd_Type_f,c` (forragem seca, forragem úmida, concentrado). O implementador deve atribuir categoria/tipo a cada linha da biblioteca (minha sugestão de categoria na seção 6.1 é só orientação).
10. **Médias para todos os nutrientes**; antes de usar a média o texto recomenda olhar DP, mín., máx., P10 e P90 (estes quatro **não estão** nas tabelas impressas); N difere entre analitos do mesmo alimento (cuidado com covariância) [pp.393–394].
11. **Biblioteca eletrônica ≠ tabela impressa**: o texto cita suplementos comerciais com campos em branco para o usuário preencher (AA protegidos da degradação ruminal, minerais orgânicos) [p.395]; a tabela traz só Lys e Met protegidas (F1002/F1001, ambas verificadas: MS 98.0; PB 75.0; A/B/C = 25/0/75; PNDR 78; dPNDR 98 [pp.428–429]).
12. **Conversões úteis a jusante (outros capítulos, só referência)**: DIVFDN48 (% FDN) → digestibilidade de FDN no trato total por `Fd_dcNDF_IV48 = 12 + 0.61 × Fd_dcNDF_IV48h` (ver ch20B, Eq. 20-111); AA "observado" → "verdadeiro" por RecAA (Tab. 20-8, p.479).

### 8.2 Lógica e fluxo
- Biblioteca (esta tabela) → composição da dieta (média ponderada pela MS) → Cap. 3 (energia), Cap. 4–5 (AG, carboidratos), Cap. 6 (PB, PNDR, AA), Cap. 7 (minerais; **Tab. 19-3** dá a composição e o coeficiente de absorção das fontes inorgânicas), Cap. 20 (equações do modelo). Nenhum valor da Tab. 19-1 é "saída": todas as colunas são entradas.
- Mapeamento coluna → variável do Cap. 20 (de acordo com ch20A; os que não puderam ser confirmados estão com ⚠): Cinzas = `Fd_Ash`; PB = `Fd_CP`; A/B/C = `Fd_CPA_CP`/`Fd_CPB_CP`/`Fd_CPC_CP`; Kd de B = `Fd_KdRUP` ⚠; dPNDR = `Fd_dcRUP`; FDN = `Fd_NDF`; PIDN = `Fd_NDFIP` ⚠ (interpretação); lignina = `Fd_Lg`; amido = `Fd_St`; AG total = `Fd_FA`; AA (19-2) = `Fd_AA(a)_CP`; ureia usa `Fd_NPN_CP`; PIDA e FDA: uso no modelo não identificado ⚠.

### 8.3 Limitações, incertezas e mudanças vs. NRC 2001 (só o que o texto do cap. 19 afirma)
- **Mudou:** não se usam mais valores de corte fixos de FDN para definir maturidade de forragens (diferente da edição anterior) [p.396]; tabelas trazem DP e N (e o texto anuncia mín./máx./P10/P90 na biblioteca eletrônica); estatísticas vêm de milhões de registros de 4 laboratórios comerciais (não de compilação de literatura) [pp.393–394]; ED é "ED base" calculada por equação, e o modelo recalcula (o NRC 2001 trazia TDN/ED/EM/ELL tabelados — comparação de conhecimento geral, **não** afirmada no cap. 19).
- **Admitido como incerto:** classificação automática de alimentos por análise de agrupamento (nomes ambíguos nos laboratórios); NIRS e química úmida misturados; fatores de variação (variedade, clima, solo, armazenagem, processamento); PNDR calculada para uma única vaca-padrão; frações A/B/C/Kd/dPNDR copiadas de alimentos "comparáveis" ou entre classes de maturidade; AA sem correção de contaminação microbiana; AA/AG de fonte única (sem DP); minerais só por química analítica; Co, Cr, I ausentes [pp.393–396].
- **Não está no modelo (só discussão/referência):** CSA, proteína solúvel, GB, hemicelulose como coluna, fibra bruta.

### 8.4 Conceitos e evidências
- Distribuição assimétrica: Fe da farinha de alfafa = 951 mg/kg (DP 680.4; N 288); mediana = 726 (~24 % abaixo da média); mínimo a 1.4 DP e máximo a 4.1 DP [p.394, p.397].
- Soja: três produtos distintos (extraído com solvente 48 % PB; extrusado; expellers); o extrusado tem muito mais gordura (Giallongo et al., 2015): AGT 15.08 vs 1.08 % MS [p.396, p.455].
- Gramíneas de estação fria agrupadas numa só classificação; leguminosas (alfafa, trevo) idem; misturas separadas por hemicelulose (FDN − FDA): >17–22 % (gramíneas), >13–17 % (mista), 10–13 % (leguminosas) [p.396].
- Maturidade da silagem de milho estimada pela MS da planta [p.396]; as silagens de milho típica, sem espiga alta MS e sem espiga baixa MS (e, pelo mesmo padrão, as demais) têm A/B/C/Kd/PNDR/dPNDR idênticos = 60/24/16/4.1/33/70 (verificado em F48, F52, F51 [p.411]); idem silagens de cevada F12/F13 = 57/33/10/7.0/27/83 [p.400].
- Perfis de AA e AG da Tab. 19-2 repetem-se entre alimentos parecidos (ex.: todas as silagens de milho; polpas de beterraba; cevada em grão/laminada/brotos): são valores copiados, não medidos para cada alimento [pp.443–458].

## 9. Parecer: viabilidade de digitalizar TODAS as tabelas

**Resumo:** viável, sem bloqueio técnico, mas **só com leitura a partir da imagem** (render ≥160–200 dpi, recorte por coluna de alimento, conferência por regras de validação). O OCR de texto corrido é bom; o OCR das tabelas acerta a maioria dos números isolados, **mas perde a atribuição linha/coluna** (células em branco desaparecem) e erra pontos decimais, de modo que não serve como fonte final. O livro é um PDF escaneado (sem camada de texto; o texto que temos vem de tesseract).

| Tabela | págs | alimentos/entradas | linhas × colunas | células numéricas (estim.) | qualidade do OCR (medida nas minhas transcrições) | já digitado por mim |
|---|---|---|---|---|---|---|
| 19-1 | 397–442 (46) | 184 posições (**180 legíveis**; 4 ausentes) | 33 linhas × 3 (Média, DP, N); 8 linhas só com média (A, B, C, Kd, PNDR, dPNDR, AGT, ED) → ~83 células/alimento no máx.; ~70 preenchidas | **~12 900** preenchidas (máx. ~15 300) | ruim para uso direto: 95.5 % dos valores aparecem como "token" em algum lugar da página (limite superior, sem checar coluna); erros típicos: ponto decimal perdido (7.48→748; 1.74→174), "SNS)" no lugar de DP, N com separador trocado, cabeçalhos truncados/ilegíveis (p.403, 413) e códigos "NRCI6FIO" | 88 alimentos / 22 págs (**6.159 células**; 48 %) — faltam 23 págs (92 alimentos): 399, 401, 409, 410, 413, 418–420, 424–426, 428–433, 435–439, 441 |
| 19-2 | 443–458 (16) | 184 alimentos (12 por pág.; p.458 só 4) | 22 linhas × 1 (sem DP/N); sem código | **~3 460** preenchidas (~18.8/alimento; máx. 4.048) | razoável: 98.6 % dos valores batem exatamente com algum token da página, mas as linhas ficam desalinhadas quando há célula vazia (ex. "Lys 4.05 1") e há mistura de colunas | 60 alimentos / 5 págs (1.129 células; 33 %) — faltam 124 alimentos (pp.446–448, 450–454, 456–458) |
| 19-3 | 459–464 (6) | 74 entradas (61 fontes) | 138 linhas elemento × (%, coef.) | ~280 | bom no texto; números com poucos erros (47.8→"4718", 2.7→"2.1", "LO"=1.0, "00.1") | **completa** (74/74) |

**Esforço estimado para fechar tudo:** 19-1: 23 págs × 4 alimentos (≈ 6.500 células) e 19-2: 10 págs (≈ 2.300 células). Cada página exige 1 imagem (160–170 dpi) + transcrição + validação automática. A p.406 original **não pode ser digitalizada** com este PDF (ver ⚠ 1).

**Regras de validação que funcionaram (e que recomendo automatizar na digitação do restante):**
1. 19-1: A + B + C = 100 ± 1 (passou nos 78 alimentos com frações); DP em branco ⇔ N em branco (1 exceção em 6.159 células); FDA ≤ FDN, lignina ≤ FDA, PIDA ≤ PIDN ≤ PB, AGT ≤ GB, MS ≤ 100 (violações reais do livro: levedura seca FDA 3.6 > FDN 1.6 [p.403]; MOR < 0 na farinha de penas).
2. 19-2: soma de C12:0…Outros = 100 ± 0.05 (passou nos 59 alimentos com perfil; faixa 99.99–100.02) — **checksum gratuito** que detecta quase todo erro de digitação nas 10 colunas de AG; AGT da 19-2 = AGT da 19-1 (passou nos alimentos comuns); PB 19-2 ≈ PB 19-1 ± 0.15 (discrepâncias reais: farinha de sangue 96.97 vs 95.1; resíduo de cervejaria seco 25.49 vs 25.3).
3. ED: recalcular com Eq. 19-1…19-4 para lipídios, proteína animal e açúcares (tolerância ±0.05–0.2; ver seção 4) e com Cap. 3 para os demais.
4. 19-3: |soma dos % dos elementos| ≤ 100; coeficientes por elemento constantes (Cl 0.92; Na/K 1.00 etc., seção 7.3).
5. Perfis repetidos (AA/AG) devem ser idênticos entre alimentos relacionados: divergência indica erro de digitação (ou erro do livro).

**Riscos principais:** (i) página 406 ausente (4 alimentos sem dados e sem código); (ii) rótulos de alimento com erros de tradução/tipografia e divergências entre 19-1 e 19-2 (seção 6, ⚠ 4–8); (iii) valores **calculados em itálico** (PNDR, ED) não se distinguem pelo OCR; (iv) classe/tipo de alimento não impressos (precisam ser atribuídos); (v) mín./máx./P10/P90 não impressos; (vi) vírgula/ponto: N usa vírgula de milhar ("2,011.07" em F170 é provavelmente 2,011 — ⚠), nota (f) da 19-3 usa vírgula decimal; (vii) 19-2 sem identificador: a junção com a 19-1 é por **posição** (frágil se a p.406 original reaparecer com ordem diferente); (viii) duas fontes distintas para PB (19-1 × 19-2) → não "corrigir" uma pela outra.

## 10. Dúvidas / riscos de OCR e de conteúdo (⚠ — conferência humana)
1. ⚠ **Página 406 original ausente do PDF**: a p.406 impressa é cópia exata da p.407 (F37–F40). 4 alimentos (posições 37–40) sem valores; nomes prováveis (da Tab. 19-2): Silagem de Gramíneas Temperadas; Milho Espiga com Casca e Sabugo Ensilado de Alto Teor de Fibra; idem de Baixo Teor de Fibra; Farinha de Milho e Sabugo Seca.
2. ⚠ Códigos NRC16F sem alimento legível: 35, 36, 53, 54, 76, 78 e 141 (7 códigos para 4 alimentos ausentes); não é possível atribuir códigos aos 4 ausentes.
3. ⚠ Classe e tipo de alimento (12 + 3) citados no texto mas não impressos por alimento [p.393].
4. ⚠ F95 rotulado "Silagem de Leguminosa, Imatura" (idêntico a F94) [p.422].
5. ⚠ F136 rotulado "Silagem de Azevém Anual, Mat. Média" (repete F130); a 19-2 traz "Silagem de Sorgo Forrageiro, Maduro" [p.432, p.454].
6. ⚠ F132 "Grão de Azevém" na 19-1 vs "Grão de Centeio" na 19-2 [p.431, p.454].
7. ⚠ Rótulos 19-1 × 19-2 divergentes: F165 "Silagem de Triticale + Ervilha" vs "Silagem de Triticale"; F170 "Grão de Trigo, Moído" vs "Laminado"; F173 "Farelo Remoído de Trigo" vs "Sêmola de Trigo"; F55 "Descarte de Algodão" vs "Resíduos de Caroço de Algodão".
8. ⚠ 19-2: ordem de F60/F61 trocada (Baixo Teor de Gordura antes de Alto Teor de Proteína); pos. 94 rotulada "Silagem…" mas corresponde ao feno F87; cabeçalho da pos. 96 cortado.
9. ⚠ 19-2, pos. 92 (feno de mistura, gramíneas predominantes, mat. média): PB = 4.28 % MS é incompatível com os demais (9–20 %); **não conferido** com a 19-1 (p.419 não transcrita) [p.450].
10. ⚠ Levedura de cerveja (19-2, pos. 25–26): AA < 1 % da PB e AG só "Outros = 100.00" [p.445]; provável escala diferente.
11. ⚠ Subproduto de frutas e vegetais úmido (19-2, pos. 83): Leu = 12.70 % da PB (faixa dos demais: 2–9) [p.449].
12. ⚠ F170 (grão de trigo moído): N de MS = "2,011.07" (ponto decimal no N) com DP de MS = 16.69, que é implausível para MS [p.440].
13. ⚠ Eq. 19-3: o livro diz PNDRd "em porcentagem da PNDR", mas a equação só reproduz a tabela se PNDRd entrar como fração (÷100); PDR = 100 − PNDR não é dito explicitamente [p.395].
14. ⚠ Resíduos de ED entre equação e tabela: sangue alta/baixa dPNDR (−0.13/−0.11), farinha de peixe (−0.20), melaço (−0.16; provavelmente não usa a Eq. 19-4), sebo/banha (+0.21), sabão de cálcio (+0.30): coeficientes de digestibilidade da gordura do Cap. 4 (Tab. 4-1: óleo 0.70; sebo TG 0.68; sais de Ca de AG de palma 0.76) não reproduzem os valores impressos; implícitos ≈ 0.655 (sebo/banha) e ≈ 0.72 (sabão) [pp.403, 415–416].
15. ⚠ ED da ureia = 2.21 (impresso); a origem não está no cap. 19 (ver Cap. 3) [p.440].
16. ⚠ Levedura seca (F23): FDA 3.6 > FDN 1.6 (N = 11 vs 38) [p.403] — inconsistência do próprio livro.
17. ⚠ MOR da farinha de penas = −0.8 pelos dados impressos (permitido pelo texto) [p.416].
18. ⚠ PB 19-1 × 19-2 diferem em farinha de sangue (95.1 vs 96.97) e resíduo de cervejaria seco (25.3 vs 25.49): fontes distintas [pp.402, 444].
19. ⚠ Texto: a tradução de p.396 diz "óleo de soja pode ser obtido…", mas o contexto é soja/farelo (erro de tradução); "Far." = Farinha; o texto traduzido de p.394 omitiu a coluna direita no OCR (lida pela imagem).
20. ⚠ O texto anuncia mín., máx., P10 e P90 por nutriente, mas só Média, DP e N estão impressos [p.394].
21. ⚠ Tab. 19-3, farinha de ossos: coeficiente do Fe impresso "00.1" (p.463), "0.01" na p.459 (adotado 0.01); Fe 2.7 % (OCR leu 2.1).
22. ⚠ Tab. 19-3, calcário dolomítico: Ca 22.3 (p.459) vs 22.0 (p.461).
23. ⚠ Tab. 19-3, composições não estequiométricas: KCl K 50.0/Cl 50.0; KI I 68.8/K 21.0; nota f com vírgula decimal ("115,9 %", "70,9 %") e "NaCO3" em vez de Na2CO3 [p.464].
24. ⚠ Tab. 19-3, óxido de magnésio: Ca = "<1" (texto) e coeficientes de Mg dependem de K da dieta = 1.2 % (nota d) [pp.461, 464].
25. ⚠ NÃO-VERIFICADO: o mapeamento PIDN→`Fd_NDFIP`, Kd→`Fd_KdRUP` e o uso de PIDA/FDA no Cap. 20 (seção 8.2) vem das notas ch20A, não conferido no Cap. 6/20 por mim.
26. ⚠ NÃO-VERIFICADO (dupla leitura): os 88 alimentos da 19-1 e os 60 da 19-2 nos CSV de apoio foram lidos uma única vez da imagem (160–170 dpi). As validações automáticas (A+B+C = 100, soma de AG = 100, AGT 19-1 × 19-2, PB 19-1 × 19-2, FDA ≤ FDN etc., e comparação "o valor existe no OCR da página": 95.5 % na 19-1 e 98.6 % na 19-2) não revelaram erros além dos itens acima, mas DP, N, minerais e Fe/Mn/Zn não têm checksum e merecem conferência amostral humana.
27. ⚠ NÃO-VERIFICADO: as páginas **não** transcritas (19-1: 399, 401, 409, 410, 413, 418–420, 424–426, 428–433, 435–439, 441; 19-2: 446–448, 450–454, 456–458) têm lista de nomes/códigos (e, na 19-1, cabeçalhos lidos da imagem), mas **nenhum valor** transcrito.

COBERTURA: páginas lidas 393–465 (texto 393–396 e referências p.465 percorridas; 19-1 pp.397–442 com cabeçalhos/códigos/nomes de **todas** as páginas lidos na imagem; 19-2 pp.443–458 com nomes de todos os 184 alimentos; 19-3 pp.459–464 integral). Valores verificados na imagem: 19-1 = 88 alimentos de 184 posições (22 de 46 págs.; 6.159 células), 19-2 = 60 de 184 alimentos (5 de 16 págs.; 1.129 células), 19-3 = 74/74 entradas. Ficaram de fora, por limite de esforço e não por ilegibilidade: valores de 92 alimentos legíveis da 19-1 e de 124 da 19-2 (só nomes/códigos); no corpo do arquivo a 19-1 mostra só as médias de 30 alimentos (DP e N dos 88 estão no CSV de apoio); p.406 original inexistente no PDF (4 alimentos). Equações 19-1 a 19-4 transcritas e testadas numericamente.

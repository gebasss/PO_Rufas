# NASEM 2021 (Bovinos Leiteiros, 8ª ed., tradução PT-BR) — Notas técnicas: Capítulo 6 "Proteína"

**Páginas impressas cobertas:** 76–115 (texto técnico: 76–107; referências: 107–115, apenas percorridas).
**Usado diretamente no modelo? Capítulo 6: SIM** (é o núcleo do módulo de proteína/AA: aporte de PM e AAE, exigências/recomendações, predição de proteína do leite). Partes só discursivas (não entram no cálculo): AA protegidos/isômeros/análogos de Met, proteína x IMS, reprodução, reciclagem de ureia (ver seção 8/9).

Convenções usadas nestas notas: `^` expoente, `_` subscrito, `*` multiplicação. Símbolos PT do livro: PB=proteína bruta (=N x 6.25), PVer=proteína verdadeira (TP), PM=proteína metabolizável (MP), PDR=proteína degradável no rúmen (RDP), PNDR=proteína não degradável no rúmen (RUP), PNDRd=digestibilidade intestinal da PNDR, Pmic=PB microbiana, NNANM=N não amoniacal não microbiano, NE=N endógeno, PL=proteína líquida (NP, net protein), PMF=proteína metabólica fecal (MFP), PPL=produção de proteína do leite, AAE=aminoácidos essenciais, AANE=não essenciais, AA-PR=AA protegido da degradação ruminal, ESPM=eficiência de síntese de proteína microbiana, NUP=N ureico plasmático, NUL=N ureico do leite, IEDnp (DEInp)=ingestão de ED não proteica, DEL=dias em lactação. As equações do livro estão com nomes de variáveis em inglês (DMI, BW, NDF, St, CP, ForWet, ...); mantive-os nas transcrições.

Verificação: todas as equações (6-1 a 6-14d) e as Tabelas 6-1 a 6-5 foram conferidas contra a imagem da página (dpi 150-300). Além disso, **reproduzi numericamente a Tabela 6-5 a partir das Eqs. 6-7a, 6-8a-c, 6-9a-c, 6-14a-b e das Tabelas 6-2 e 6-4** (resultado na seção 5, subitem Tabela 6-5): bateu em todas as células (±1 g de arredondamento). Isso confirma, de forma independente, as transcrições dessas equações e tabelas e o fluxo de cálculo.

---

## 1. Papel no simulador
O capítulo define (a) como converter a dieta em **aporte líquido de PM e de AAE metabolizáveis** (PDR/PNDR, Pmic, digestibilidades, composição de AA), (b) as **demandas líquidas de proteína/AA** por função (descamação, perda urinária endógena, PMF, leite, gestação, crescimento/reservas), (c) a **eficiência-alvo** de uso de PM/AAE (Tabela 6-4) para transformar demanda líquida em **recomendação** de PM/AAE (Eqs. 6-14), e (d) uma **equação de resposta aditiva e não linear de produção de proteína do leite** a AAE e energia (Eq. 6-6). No simulador: entradas = composição da dieta (PB, frações A/B/C, kd, PNDRd, perfil de AA dos ingredientes — Cap. 19), IMS, PC, nível de produção/proteína do leite, estágio de gestação, ganho; saídas = Pmic, PNDR, PM, AAE metabolizáveis, PPL predita, recomendações de PM/AAE, eficiências observadas vs. alvo, alertas de PDR.

---

## 2. Entradas (do ponto de vista do módulo de proteína)

| Variável | Símbolo/sigla | Unidade | Definição | Faixa/valores típicos | Pág. |
|---|---|---|---|---|---|
| Proteína bruta do ingrediente | PB (CP) | % MS ou g/d | N x 6.25 | do Cap. 19 | 76 |
| Frações de N in situ | A, B, C | % da PB | A=solúvel (lavagem), C=indegradável, B=A,B,C pela diferença | Cap. 19 | 77 |
| Taxa de degradação da fração B | kd (Kd_c) | %/h | por ingrediente; média ponderada por classe | Cap. 19 | 77, 80 |
| N não proteico degradável (parte da fração A) | CPA_NPN (NNP x 6.25) | g/d | equivalente PB | — | 80 |
| Digestibilidade intestinal da PNDR | PNDRd | % da PNDR | biblioteca de alimentos | Cap. 19 | 77, 85 |
| Composição de AA do ingrediente | — | g AA/100 g PB (corrigido p/ hidrólise) | Tabela 19-2 corrigida por fatores de recuperação (Lapierre et al. 2019, Cap. 18) | Cap. 19 | 85, 87 |
| Ingestão de matéria seca | IMS (DMI) | kg/d | — | Cap. 2 | 81 |
| PDR ingerida | RDP | kg/d | derivada de PB, A, B, C, kd e kp (Eq. 6-1) | min 10 %, max 12 % da MS | 82 |
| FDN, FDN de forragem, FDA, amido, PB da dieta | NDF, fNDF, ADF, St, CP | % da MS | — | — | 82 |
| Forragem úmida (>20 % MS) na dieta | ForWet | % da MS | — | — | 82 |
| Peso corporal | PC (BW) | kg | — | ex.: 612 (média do banco de dados), 650 (Tab. 6-5) | 90, 93 |
| FDN digestível | dNDF | % da MS | vem do módulo de digestão (Cap. 3) — não calculado aqui | média do banco: 17.06 | 90 |
| ED ingerida e PM | DEI, MP | Mcal/d, g/d | para DEInp (Eq. 6-5) | — | 89 |
| Proteína verdadeira do leite (ou concentração) | PPL / NP-milk | g/d | PPL predita (Eq. 6-6) ou informada pelo usuário | ex.: 1,000-1,400 (Tab. 6-5); média do banco 920 | 91, 94 |
| Relação PVer/PB do leite | — | fração | se desconhecida usar 0.951 (NNP do leite 4.9 %) | 0.951 | 94 |
| Ganho do útero gravídico | Gain_GrUter | kg/d | do Cap. 3, a partir do peso ao nascer do bezerro | — | 95 |
| Ganho de peso do "frame" (crescimento estrutural) | Frame weight gain | g/d | valor-padrão editável pelo usuário | ver seção 6 | 96 |
| Ganho/perda de reservas corporais | — | g/d | teor de proteína no ganho = 8.0 % | — | 96 |
| Peso à maturidade | — | kg | Holandesa 700, Jersey 520 (exemplos do texto) | — | 96 |
| Status fisiológico | — | — | lactante-não-gestante / gestante / seca / novilha: define Eq. 6-13 vs 6-14a-d | — | 96-98 |

## 3. Saídas

| Variável | Sigla | Unidade | Definição | Pág. |
|---|---|---|---|---|
| PNDR da dieta | Dt_RUP | g/d (base PB) | Eq. 6-1 | 80 |
| N endógeno duodenal | Du_EndN | g N/d | Eq. 6-2 (NÃO entra no aporte líquido; só ajusta o NNANM) | 81 |
| N microbiano / Pmic | Microbial N | g N/d (x6.25 = PB) | Eq. 6-3 | 81-82 |
| Aporte líquido de PM | MP supply | g/d | PM da PNDR + PM da Pmic | 77 |
| Aporte de AAE metabolizáveis (His, Ile, Leu, Lys, Met, Phe, Thr, Trp, Val) | — | g/d | método fatorial (ver seção 7) | 78, 85-87 |
| PPL predita | Milk Protein | g/d | Eq. 6-6 | 90 |
| PL por função (descamação, urinária endógena, PMF, leite, gestação, crescimento) | NP-* | g/d | Eqs. 6-7 a 6-12 | 93-96 |
| AA líquido por função | NetAA-* | g/d | idem | 93-96 |
| Eficiência observada de uso de PM/AA | Eff_MP, Eff_AA | fração | Eqs. 6-13a/b | 97 |
| Recomendação de PM e de AAE | Recommended MP supply / EAA digestible flow | g/d | Eqs. 6-14a-d | 98 |

---

## 4. Equações

### 4.1 PNDR (proteína não degradável no rúmen) — Eq. 6-1 [p.80] (verificada na imagem)
```
Dt_RUP = SUM_{c=1}^{N_c} [ (1 - DCa_c) * (Dt_CPAIn_c - Dt_CPAIn_NPN,c)
                           + ( Kp_c / (Kp_c + Kd_c) ) * Dt_CPBIn_c
                           + Dt_CPCIn_c ]
```
- Dt_ = ingestão total da dieta do nutriente especificado; c = classe de alimento (forragem [úmida e seca] ou concentrado); N_c = nº de classes.
- DCa_c = degradabilidade ruminal da fração A na classe c. O texto fala em "escape" de 6.4 +/- 4 % da proteína da fração A, ou seja, 1-DCa = 0.064 (DCa = 0.936) — interpretação minha a partir do texto [p.80]; o livro não escreve o valor de DCa explicitamente. ⚠
- CPAIn_c = ingestão de PB da fração A; CPAIn_NPN,c = ingestão de NNP x 6.25 degradável (parte da A), subtraída (NNP é 100 % degradado); CPBIn_c = PB da fração B; CPCIn_c = PB da fração C (todo escapa).
- Kp_c = kp (taxa de passagem) ESTÁTICO da classe c; Kd_c = média ponderada do kd in situ (fração B) dos alimentos da classe c.
- Resultado em base PB (g/d ou kg/d, conforme as ingestões). Ajustada contra NNANM pós-ruminal observado menos N endógeno estimado, x 6.25 [p.80].
- Origem: abordagem Bayesiana hierárquica (Moraes et al. 2018b), modelo derivado de Seo et al. (2006); banco de dados de fluxos pós-ruminais (Roman-Garcia et al. 2016; White et al. 2017b). Estatísticas: CCC 0.54; RMSE 40.9 % da média; vieses de intercepto e de inclinação 0.1 % e 3.8 % do MSE [p.80].
- **Parâmetros estimados:** Kp estático da fração B = 5.28 +/- 0.63 %/h (concentrados) e 4.87 +/- 0.33 %/h (forragens) (o texto diz "para concentrados e forragens, respectivamente") ; escape da fração A = 6.4 +/- 4 % [p.80]. Não afetados por fatores dietéticos (diferente do NRC 2001, em que kp aumentava com IMS, %FDN e %concentrado).

### 4.2 N endógeno duodenal — Eq. 6-2 [p.81] (verificada na imagem)
```
Du_EndN (g N/d) = 15.4 (+/- 2.6) + 1.21 (+/- 0.24) * DMI
```
- DMI em kg/d. Os valores "+/-" são erros-padrão de intercepto e inclinação (ambos P <= 0.01). Impressa no livro como "15.4 ± 2.6 + 1.21 ± 0.24 x DMI".
- Banco de dados: Tabela 6-1 (12 linhas, vacas leiteiras e bovinos em crescimento; estado fisiológico não foi significativo).
- Comparação: NRC (2001) usava 1.9 g N/kg IMS; subestimaria NE para IMS < 22.3 kg/d e superestimaria acima disso [p.81].
- Uso: o N endógeno é SUBTRAÍDO do fluxo observado de NNANM para derivar PNDR (Eq. 6-1) e Pmic; NÃO entra no aporte líquido de PM/AA [pp.77, 80].

### 4.3 N microbiano — Eq. 6-3 [p.81-82] (verificada na imagem)
```
Microbial N (g N/d) = [ B0 + (B1 * RDP) ] / [ (1 + B2/RDNDF) * (1 + B3/RDS) ]
```
- RDP = PDR ingerida, kg/d (calculada com a abordagem kd/kp da Eq. 6-1); RDNDF = FDN degradável no rúmen, kg/d (Eq. 6-4a); RDS = amido degradável no rúmen, kg/d (Eq. 6-4b, chamado RStDig no livro; ver ⚠).
- **Parâmetros (média +/- EP):** B0 = 101 +/- 11 (g N/d); B1 = 82.6 +/- 4.2 (g N/kg PDR); B2 = 0.094 +/- 0.028 (kg/d, FDN); B3 = 0.027 +/- 0.010 (kg/d, amido) [p.82].
- Multiplicar por 6.25 para obter Pmic em base PB [p.82].
- Forma: integral assintótica de Michaelis-Menten (Thornley e France 2007); ajuste Bayesiano (Moraes et al. 2018a), mesmos estudos de White et al. (2017b); **580 médias de tratamento** (Fig. 6-1).
- Desempenho: RMSE do modelo 29.7 % e da validação cruzada 29.8 % da média (278 g N/d); CCC 0.52 / 0.50 [p.82].
- Propriedade: como B0 > 0, a Pmic máxima estimada é igual ao aporte de PDR [p.82] (observação do texto; o livro não explica o limite como cláusula explícita).
- Não ajustada para gordura, sincronização, fibras solúveis/açúcares, nem para reciclagem de NUP (ver seção 8).

### 4.4 FDN degradável e amido degradável no rúmen — Eqs. 6-4a/6-4b [p.82] (verificadas na imagem, com 1 problema de parênteses)
Como impresso (Eq. 6-4a):
```
RDNDF = [-31.9 + (0.721*NDF) - (0.247*St) + (6.63*CP) - (0.211*CP^2) - (38.7*ADF/NDF)
         - (0.121*ForWet) + (1.51*DMI) * ((NDF/100) * DMI)] / 100
```
⚠ Os parênteses impressos estão incompletos (falta o parêntese que fecha o grupo de coeficientes). Pela estrutura da Eq. 6-4b e por análise dimensional/teste numérico, a leitura correta é:
```
RDNDF (kg/d) = [ (-31.9 + 0.721*NDF - 0.247*St + 6.63*CP - 0.211*CP^2 - 38.7*(ADF/NDF)
                  - 0.121*ForWet + 1.51*DMI) * ((NDF/100) * DMI) ] / 100          (interpretação)
```
O termo entre parênteses é a % de FDN degradada no rúmen; (NDF/100)*DMI é a ingestão de FDN em kg/d. Teste numérico próprio (NDF 32, St 25, CP 16.5, ADF/NDF 0.62, ForWet 10, DMI 24) dá ~48 % de FDN degradada (plausível) e Pmic ~290 g N/d (média do banco: 278).

Eq. 6-4b (impressa):
```
RStDig = [ (71.2 - (1.45*DMI) + (0.424*fNDF) + (1.39*St) - (0.0219*St^2) - (0.154*ForWet))
           * (St/100) * DMI ] / 100
```
- RStDig (= RDS da Eq. 6-3) em kg/d; o termo entre parênteses é % do amido degradado no rúmen. Teste numérico próprio (DMI 24, fNDF 20, St 25, ForWet 10): ~64 % (plausível).
- Unidades: DMI kg/d; NDF, St, CP, ADF, fNDF, ForWet em % da MS da dieta. ForWet = concentração de forragem úmida (>20 % de MS) na dieta, % da MS [p.82].
- "Amido" nos dados de origem = ensaio enzimático que inclui açúcares [p.84]. A inclinação negativa do amido em 6-4a reflete efeitos associativos negativos (White et al. 2016).
- Equações preveem degradabilidades percentuais (não absolutas); por isso a Pmic estimada deve ser ponderada pela IMS [p.82].

### 4.5 Equações de PPL — Eq. 6-5 (forma geral avaliada) [p.89] (verificada)
```
Milk Protein (g/d) = Arg + His + Ile + Leu + Lys + Met + Phe + Thr + Trp + Val + NEAA
                     + SUM(EAA^2) + DEInp + dFA + dNDF + BW + Parity + PubID
```
- Forma EXPLORATÓRIA (conjunto de termos candidatos; coeficientes não dados). DEInp (Mcal/d) = ED ingerida menos energia da PM a 5.65 kcal/g de PM; AA individuais = AA metabolizáveis (g/d); NEAA = AANE absorvidos (g/d); SUM(EAA^2) = soma dos quadrados dos aportes; dFA e dNDF em % da MS; BW em kg; Parity contínua 0-1 (0=primíparas, 1=multíparas); PubID = efeito aleatório de estudo [p.89].
- Seleção "todos os modelos" (Burnham e Anderson 2002), 5,000 melhores modelos por AIC. Duas formas alternativas (AAE em % do AAE total; AAE como razão da IEDnp) foram descartadas por inconsistência/inferioridade [pp.89-90]. Termos excluídos por instabilidade/sinal não biológico: Arg (essencialidade condicional), Phe, Thr, Trp, Val, AGd e paridade [p.90].

### 4.6 Eq. 6-6 — Proteína verdadeira do leite permissível (PL-leite) [p.90] (verificada na imagem a 300 dpi)
```
Milk Protein (g/d) = -97.0 + 1.68*His + 0.885*Ile + 0.466*Leu + 1.15*Lys + 1.84*Met
                     + 0.077*OthAA - 0.00215 * SUM_{i=1}^{N_EAA} (EAAb_a,i)^2
                     + 10.8*DEInp - 4.60*(dNDF - 17.06) - 0.420*(BW - 612)
```
- His, Ile, Leu, Lys, Met = aporte metabolizável (absorvido) de cada AAE, g/d (corrigido para hidrólise incompleta; ver seção 7).
- OthAA (g/d) = aporte absorvido de AANE + Arg + Phe + Thr + Trp + Val.
- SUM(EAAb^2) = soma dos quadrados dos aportes absorvidos dos cinco AAE presentes na equação (His, Ile, Leu, Lys, Met), o subscrito "a" no livro; N_EAA = 5 (termo quadrático, retornos decrescentes).
- DEInp em Mcal/d (= ED ingerida - 5.65 kcal/g x PM; ver Eq. 6-5); dNDF em % da MS, centralizado em 17.06 %; BW em kg, centralizado em 612 kg.
- Interpretação: PPL = proteína VERDADEIRA do leite em g/d, que o animal PODE produzir com essa dieta ("PL-leite").
- **Desempenho (Tabela 6-3):** N = 926, RMSE 133 g/d (14.4 % da média), CCC 0.75, viés médio ≈ 0, viés de inclinação 3.1 % do MSE. Correlação entre estimativas de coeficientes: Leu-Lys 0.67; OthAA-Ile -0.51; Lys-His -0.43; demais < 0.32 em módulo [p.90].
- **Validade:** coeficientes de referência para um grupo que produz em média **920 g/d** de proteína do leite; para rebanhos de maior produção há conjunto de equações algébricas para reescalar os coeficientes linear e quadrático dos AAE pela média do rebanho (**Capítulo 20**) [p.91]. Banco de dados: 1,149 médias de tratamento de 275 experimentos; 898 tratamentos de 216 estudos com leite e proteína informados [p.88].
- Resíduos sem relação com AGd, FDNd, Ad (amido digestível), PC etc.; únicos efeitos residuais: DEL (-0.79 g/d por dia) e gordura do leite (-0.96 g/d por unidade percentual de gordura) (corrigido na verificação: estava +0.96; a imagem p.91 mostra sinal negativo, conferido a 300 dpi) — NÃO incluídos no modelo (DEL por 3 estudos pouco confiáveis; gordura problemática para raças de alta gordura) [p.91].

### 4.7 Proteína de descamação — Eqs. 6-7a e 6-7b [p.93] (verificadas)
```
NP-scurf (g/d) = 0.20 * BW^0.60 * 0.85 = 0.17 * BW^0.60                       (Eq. 6-7a)
NetAA-scurf (g/d) = NP-scurf * [AA_corr-Scurf] / 100                           (Eq. 6-7b)
```
- BW em kg; 0.85 = razão PVer/PB da descamação; [AA_corr-Scurf] em g AA/100 g PVer (Tabela 6-2, coluna "Descamação").
- Origem: Swanson (1977) (>2,400 observações de calorimetria), ajustada de base PB para base PVer. (O expoente 0.60 foi lido na imagem — o OCR do bloco da equação estava ilegível; não confundir com o PC^0.75 das purinas urinárias.) Composição AA: cabeça, couro, pés e cauda (Williams 1978; van Amburgh et al. 2015) [p.93].

### 4.8 Perda urinária endógena — Eqs. 6-8a, 6-8b, 6-8c [p.93-94] (verificadas)
```
NP-endogenous urinary (g/d) = 53 * 6.25 * BW * 0.001                           (Eq. 6-8a)

NetAA-endogenous urinary, "todos os AAE exceto His" (Eq. 6-8b, COMO IMPRESSA):
  NetHis-endogenous urinary (g/d) = (0.010 * 6.25 * BW * [His_corr-WholeEmptyBody] / 100)
                                    + (7.82 + 0.55*BW) / 1,000

Para His (Eq. 6-8c, COMO IMPRESSA, idêntica à 6-8b):
  NetHis-endogenous urinary (g/d) = (0.010 * 6.25 * BW * [His_corr-WholeEmptyBody] / 100)
                                    + (7.82 + 0.55*BW) / 1,000
```
- ⚠ **Erro de impressão:** a Eq. 6-8b aparece com o rótulo/nome "NetHis" e IGUAL à 6-8c, incluindo o termo de 3-metil-His. Pelo texto ("para todos os AAE, exceto His, a excreção de ureia endógena (0.010 g N/kg PC/d) é usada ... assumindo composição de corpo vazio") a Eq. 6-8b correta é:
```
NetAA-endogenous urinary (g/d) = 0.010 * 6.25 * BW * [AA_corr-WholeEmptyBody] / 100     (todos os AAE exceto His)
```
  e só His acrescenta (7.82 + 0.55*BW)/1000 (3-metil-His). **Confirmado numericamente:** só assim a Tabela 6-5 é reproduzida (His = 55 g/d no caso de 1,000 g PPL).
- BW em kg; [AA_corr-WholeEmptyBody] em g AA/100 g PVer (Tabela 6-2, "Corpo Vazio Inteiro"); 7.82 + 0.55*BW = mg/d de His como 3-metil-His, dividido por 1,000 para g/d.
- Base: 53 mg N/kg PC (média), vs 50 mg N/kg PC do INRA (2018); Swanson (1977) usava 2.75 g PB/kg BW^0.50. Componentes (por kg PC): ureia endógena 10 mg N, creatinina 9.46 mg N (25.5 mg), creatina 0.37 da creatinina (3.5 mg N), purinas endógenas 27.1 mg N/PC^0.75 (sic), 3-metil-His (7.82 + 0.55 PC mg/d); o restante (46 % da fração "mensurada") assumido ácido hipúrico [p.93]. PVer/PB = 1.0 (N urinário tratado como PB padrão, N x 6.25).
- Eficiência de uso = 1.0 (perda sem retorno; produto final do metabolismo) [pp.96-97].

### 4.9 Proteína metabólica fecal (PMF) — Eqs. 6-9a, 6-9b, 6-9c [p.94] (verificadas)
```
CP-MFP (g/d) = (11.62 + 0.134 * NDF_%DM) * DMI                                 (Eq. 6-9a)
NP-MFP (g/d) = CP-MFP * 0.73                                                    (Eq. 6-9b)
NetAA-MFP (g/d) = NP-MFP * [AA_corr-MFP] / 100                                  (Eq. 6-9c)
```
- NDF_%DM = FDN da dieta, % da MS; DMI em kg/d; 0.73 = PVer/PB da PMF; [AA_corr-MFP] em g AA/100 g PVer (Tabela 6-2, "Fecal Metabólico").
- Origem: adaptação da regressão de Marini et al. (2008) (intercepto 30 g PB/kg IMS = PMF + bactérias não digeridas de ureia), ajustada ao fluxo ileal endógeno de Ouellet et al. (2002, 2007, 2010) + secreção endógena do intestino posterior (ovinos, Sandek et al. 2001) com 5.1 g PB/kg IMS no íleo, metade proteína endógena/metade ureia (Lapierre et al. 2020) [pp.94].
- NRC (2001) usava PMF (g PM/d) = [(IMS x 30) - 0.50 x ((PM bacteriana/0.80) - PM bacteriana)], sem converter para PVer e sem eficiência [p.94]. Agora a PMF tem a mesma eficiência-alvo de leite/descamação.
- Composição AA: Orskov et al. (1986) e fluxo ileal endógeno em suínos (Jansman et al. 2002); o comitê assumiu 70 % da PMF vinda do fluxo duodenal não digerido e 30 % do intestino [p.94] (como entra no cálculo da composição: não detalhado).

### 4.10 Leite — Eq. 6-10 [p.95] (verificada)
```
NetAA-Milk (g/d) = NP-Milk (g/d) * [AA_calc-Milk] / 100
```
- NP-Milk = produção de PVer do leite (g/d); [AA_calc-Milk] em g AA/100 g PVer (Tabela 6-2, "Leite", calculada da estrutura primária das proteínas do leite; não precisa de correção de hidrólise).
- Fator N->PB do leite = **6.34** (não 6.38); se PVer/PB desconhecida: NNP do leite = 4.9 % da PB (DePeters e Cant 1992) e **PVer/PB = 0.951** [p.94].
- Composição proteica do leite usada: 82.4 % caseína (35.2 % as1, 7.6 % as2, 30.9 % beta, 8.7 % kappa) e 17.6 % soro (3.7 % alfa-lactalbumina, 10.5 % beta-lactoglobulina, 1.04 % albumina, 1.64 % IgG1, 0.18 % IgG2, 0.04 % IgA, 0.33 % IgM, 0.21 % lactoferrina), de 15 manuscritos 1980-2012 [p.95]. Composição AA do leite assumida constante.

### 4.11 Gestação — Eqs. 6-11a, 6-11b [p.95] (verificadas)
```
NP-Gestation (g/d) = Gain_GrUter * 125                                          (Eq. 6-11a)
NetAA-Gestation (g/d) = NP-Gestation * [AA_corr-WholeEmptyBody] / 100            (Eq. 6-11b)
```
- Gain_GrUter = ganho diário em massa do útero gravídico (kg/d), do Cap. 3 (baseado no peso do bezerro ao nascer; modelo de Koong et al. 1975 ajustado a Bell et al. 1995); 125 g de proteína/kg de peso úmido (Bell et al. 1995). Corpo vazio total como composição AA.
- Involução uterina pós-parto: completa em 4 semanas (Cap. 3); AA do tecido involutivo contribuem para o aporte de PL [p.95].
- Eficiência de uso (PM -> PL gestação) = **0.33** (mantida do NRC 2001; outros comitês: 0.50 [NRC 1989] e 0.65 [NASEM 2016]) [p.96].

### 4.12 Crescimento (frame e reservas) — Eqs. 6-12a, 6-12b [p.96] (verificadas)
```
NP-growth (g/d) = Frame weight gain (g/d) * 0.11 * 0.86                          (Eq. 6-12a)
NetAA-growth (g/d) = NP-growth * [AA_corr-WholeEmptyBody] / 100                  (Eq. 6-12b)
```
- Válida "durante a lactação". 0.11 = fração de proteína no ganho de PC vazio associado ao frame (média de 11.2 % e 10.6 % para 1ª e 2ª lactação, via Cap. 11, PC a 82 % e 92 % do PC maduro); 0.86 = razão PVer/PB (p.96) (⚠ na p.97 o mesmo 0.86 é descrito como "PC vazio/PC"; inconsistência do livro).
- Ganho de PC vazio do crescimento do frame = 85 % do ganho de PC em vacas [p.96].
- Se a mudança de PC NÃO for crescimento do frame (reservas corporais), o teor de proteína no ganho = **8.0 %**; NP-growth total = frame + reservas (a equação para reservas não é escrita explicitamente) [p.96].
- Metas de ganho de frame: Holandesa (maturidade 700 kg) 0.19 kg/d (1ª lactação) e 0.15 (2ª); Jersey (520 kg) 0.14 e 0.11 kg/d; PC pós-parto 82 % e 92 % da maturidade; PVer para crescimento ~13-18 g/d [pp.96-97].

### 4.13 Eficiência observada de PM/AA — Eqs. 6-13a, 6-13b [p.97] (verificadas)
```
Eff_MP = (NP-scurf + NP-MFP + NP-milk + NP-growth) / (MP supply - NP-endogenous urinary)    (Eq. 6-13a)
Eff_AA = (NetAA-scurf + NetAA-MFP + NetAA-Milk + NetAA-growth)
         / (metabolizable AA - NetAA-endogenous urinary)                                      (Eq. 6-13b)
```
- ⚠ Na impressão da 6-13a o sinal "+" antes de NP-growth está ausente na quebra de linha; restaurado pela consistência com a 6-13b.
- Válidas para vacas lactantes NÃO gestantes (gestação = 0). Usa eficiência combinada (descamação + PMF + leite + crescimento) e 100 % para urinária endógena. Banco: 921 médias de tratamento (após exclusões a priori: análogos de Met, infusões intravenosas) [pp.97].

### 4.14 Recomendações de PM e AAE — Eqs. 6-14a a 6-14d [p.98] (verificadas)
```
Recommended MP supply = [ (NP-scurf + NP-MFP + NP-milk + NP-growth) / Target_Eff_MP ]
                        + (NP-gestation / 0.33) + NP-endogenous urinary                       (6-14a)

Recommendation for individual EAA digestible flow =
      [ (NetAA-scurf + NetAA-MFP + NetAA-Milk + NetAA-growth) / Target_Eff_AA ]
      + (NetAA-gestation / 0.33) + AA-endogenous urinary                                       (6-14b)

Para "vacas em final de lactação e novilhas" (texto do livro) [ver ⚠]:
Recommendation for MP supply = (NP-scurf + NP-MFP) / Target_Eff_MP
                               + (NP-gestation / 0.33) + (NP-growth / 0.40)
                               + NP-endogenous urinary                                         (6-14c)

Recommendation for individual EAA digestible flow =
      [ (NetAA-scurf + NetAA-MFP) / Target_Eff_AA ] + (NetAA-gestation / 0.33)
      + (NetAA-growth / 0.40) + AA-endogenous urinary                                          (6-14d)
```
- Target_Eff_MP e Target_Eff_AA: Tabela 6-4. Eficiência de gestação 0.33; de crescimento (heifers/secas) 0.40 [pp.96, 98]; urinária endógena sem divisão (eficiência 1.0).
- Detalhe: as equações de PM (14a, 14c) usam NP (base PB para dados originais) enquanto as de AA usam NetAA (base PVer x composição); "as exigências de PM (mas não as de AA) são calculadas como" 14a/14c [p.98].
- ⚠ "final de lactação" nas Eqs. 6-14c/d: o contexto (p.96 e p.98) indica não lactantes (vacas secas) e novilhas; "final de lactação" pode ser erro de tradução (o original deve ser "late-gestation"/non-lactating). Conferir com o original em inglês. (Verificação na imagem p.98: "final de lactação" aparece impresso duas vezes: "Para vacas em final de lactação e novilhas, as equações são..." e "A PL para gestação de vacas em final de lactação e baixa produção de leite pode ser substancial; portanto, sua eficiência foi mantida em 0.33"; já a p.96 diz que a eficiência de crescimento 0.40 não vale para "novilhas em crescimento ou vacas secas". Ambíguo: dúvida mantida, nada alterado.)
- Não há exigência para o fluxo duodenal endógeno (não é parte do aporte) [p.99].

---

## 5. Parâmetros e tabelas

### Tabela 6-1 — Fluxo de NE duodenal (g N/d) reportado para bovinos [p.81] (verificada)
| Animal | IMS, kg/d* | PC | NE | Metodologia | Referência |
|---|---|---|---|---|---|
| 2 vacas leiteiras | 8.34 | 500 | 18.8 | 15N | Brandt et al. (1980) |
| 2 vacas leiteiras | 0 (3.4) | 675 | 15.4 | Inf. de AGVs no rúmen | Orskov et al. (1986) |
| 4 vacas leiteiras | 14.4 | 625 | 34.0 | Diluição de 15N-Leucina | Ouellet et al. (2002) |
| 4 vacas leiteiras | 17.6 | 607 | 40.0 | Diluição de 15N-Leucina | Ouellet et al. (2010) |
| Vacas leiteiras | 18.0 | 600 | 40.9 | Meta-análise | Marini et al. (2008) |
| Vacas leiteiras | 17.9 | 597 | 29.5 | Meta-análise | Sauvant et al. (2013) |
| 3 bois | 2.86 | 300 | 23.0 | Dietas livres em PDR | Hart et al. (1990) |
| 2 bois | 0 (2.2) | 278 | 11.6 | Inf. de AGVs no rúmen | Orskov et al. (1986) |
| 4 bois | 0 (1.8) | 278 | 13.3 | Inf. de AGVs no rúmen | Orskov et al. (1986) |
| 4 bois | 3.14 | 424 | 24.4 | Dietas livres de PDR | Hannah et al. (1991) |
| 4 bois | 3.37 | 372 | 26.2 | Dietas livres de PDR | Lintzenich et al. (1995) |
| Bovinos em crescimento | 6.82 | 359 | 24.2 | Meta-análise | Marini et al. (2008) |

*Quando AGVs são infundidos, IMS = 0 e o valor entre parênteses = kg de MS infundida no rúmen. (OCR: "PC 424/372", "Orskov" e "AGVs" corrigidos pela imagem.)

### Tabela 6-2 — Composição de AA das frações de PB e PVer [p.87] (verificada na imagem a 200 dpi)
Colunas: Endógeno duodenal = g AA_corr/100 g **PB**; Microbiano, Descamação, Corpo Vazio Inteiro, Fecal Metabólico = g AA_corr/100 g **PVer (TP)**; Leite = g AA_calc/100 g PVer. Todas na forma hidratada (somam > 100). Microbiano adaptado de Sok et al. (2017) com fatores de Lapierre et al. (2019); tabela modificada de Lapierre et al. (2020).

| AA | Endógeno Duodenal (/100 g PB) | Microbiano | Descamação | Corpo Vazio Inteiro | Fecal Metabólico | Leite |
|---|---|---|---|---|---|---|
| Ala | 4.69 | 7.38 | 9.17 | 8.59 | 6.32 | 3.59 |
| Arg | 4.61 | 5.47 | 9.60 | 8.20 | 5.90 | 3.74 |
| Asx | 4.75 | 13.39 | 8.39 | 9.61 | 7.56 | 8.14 |
| Cys | 2.58 | 2.09 | 2.70 | 1.74 | 3.31 | 0.93 |
| Glx | 11.31 | 14.98 | 14.69 | 15.76 | 15.67 | 22.55 |
| Gly | 5.11 | 6.26 | 21.08 | 14.46 | 8.45 | 2.04 |
| His | 2.90 | 2.21 | 1.75 | 3.04 | 3.54 | 2.92 |
| Ile | 4.09 | 6.99 | 2.96 | 3.69 | 5.39 | 6.18 |
| Leu | 7.67 | 9.23 | 6.93 | 8.27 | 9.19 | 10.56 |
| Lys | 6.23 | 9.44 | 5.64 | 7.90 | 7.61 | 8.82 |
| Met | 1.26 | 2.63 | 1.40 | 2.37 | 1.73 | 3.03 |
| Phe | 3.98 | 6.30 | 3.61 | 4.41 | 5.28 | 5.26 |
| Pro | 4.64 | 4.27 | 12.35 | 9.80 | 8.43 | 10.33 |
| Ser | 5.24 | 5.40 | 6.45 | 5.73 | 7.72 | 6.71 |
| Thr | 5.18 | 6.23 | 4.01 | 4.84 | 7.36 | 4.62 |
| Trp | 1.29 | 1.37 | 0.73 | 1.05 | 1.79 | 1.65 |
| Tyr | 3.62 | 5.94 | 2.62 | 3.08 | 4.65 | 5.83 |
| Val | 5.29 | 6.88 | 4.66 | 5.15 | 7.01 | 6.90 |

Somas de controle (minhas, para conferência pelo implementador): 84.44 | 116.46 | 118.74 | 117.69 | 116.91 | 113.80.
(corrigidos pela imagem em relação ao OCR: Asx endógeno "4.15" -> 4.75; Gly endógeno "5.1" -> 5.11; Cys fecal "331" -> 3.31; Met corpo vazio "237" -> 2.37; Phe corpo vazio "441" -> 4.41; Ser fecal "77" -> 7.72; Thr fecal "736" -> 7.36; Tyr descamação "262" -> 2.62 e Tyr fecal "465" -> 4.65; Pro microbiano "427" -> 4.27; Phe leite "526" -> 5.26; Trp microbiano "137" -> 1.37; Cys endógeno/microbiano "2.58/2.09" conferidos.)
Uso: coluna Endógeno duodenal = perfil da proteína endógena que é removida do fluxo duodenal observado (derivada de Orskov et al. 1986; para Leu só valor ruminal) [p.87]; Microbiano = perfil da PVer da Pmic (média ponderada: bactérias associadas a fluido e a partículas e protozoários, 33.4/50.1/16.5 %) [pp.85-86]; Descamação, Corpo Vazio, Fecal Metabólico, Leite = demandas líquidas (Eqs. 6-7b, 6-8b/c, 6-11b, 6-12b, 6-9c, 6-10).

### Tabela 6-3 — Análises residuais de estimativas de PPL: NRC (2001) vs. Eq. 6-6 [p.88] (verificada na imagem)
| | NRC 2001: ELL | NRC 2001: PM | NRC 2001: Mínimo entre ELL e PM | Equação 6-6 |
|---|---|---|---|---|
| N | 922 | 926 | 922 | 926 |
| Média observada, g/d | 922 | 921 | 922 | 921 |
| Média estimada, g/d | 953 | 890 | 831 | 924 |
| CCC | 0.77 | 0.65 | 0.71 | 0.75 |
| RMSE, g/d | 194 | 228 | 210 | 133 |
| RMSE, % da média | 21.0 | 24.9 | 22.8 | 14.4 |
| Viés médio, % do MSE | 3 | 2 | 19 | 0.0 |
| Viés de inclinação, % do MSE | 38 | 32 | 21 | 3.1 |
| Viés médio, g/d | -31 | 31 | 91 | -2.7 |
| Viés de inclinação, g/g | -0.38 | -0.44 | -0.34 | 0.156 |
| P (viés médio) | 0.0001 | 0.0002 | 0.0001 | 0.54 |
| P (viés de inclinação) | 0.0001 | 0.0001 | 0.0001 | 0.0001 |
Notas: estimativas não ajustadas para efeito aleatório de estudo; PPL estimada pelo NRC (2001) (g/d) = leite permissível (kg/d) x proteína do leite observada (%) x 10. Viés = observado menos estimado. ⚠ Divergências texto vs tabela (pp.88): o texto cita RMSE 22.9 % (mínimo ELL/PM; tabela 22.8), 21.3 % (ELL; tabela 21.0), subestimativa de 28 g/d (PM; tabela 31) e superestimativa de 32 g/d (ELL; tabela 31). Vale a tabela (imagem). ⚠ P do viés de inclinação da Eq. 6-6 = 0.0001 apesar de viés pequeno (3.1 % do MSE) — como impresso.

### Tabela 6-4 — Eficiências-alvo propostas de PM e AAE [p.97] (verificada)
| PM ou AA | Valor-alvo | Média | Erro padrão | Mínimo | Máximo |
|---|---|---|---|---|---|
| PM (MP) | 0.69 | 0.66 | 0.102 | 0.35 | 1.00 |
| His | 0.75 | 0.78 | 0.141 | 0.34 | 1.21 |
| Ile | 0.71 | 0.61 | 0.088 | 0.36 | 0.93 |
| Leu | 0.73 | 0.67 | 0.120 | 0.24 | 1.01 |
| Lys | 0.72 | 0.67 | 0.106 | 0.35 | 1.05 |
| Met | 0.73 | 0.71 | 0.120 | 0.36 | 1.13 |
| Phe | 0.60 | 0.54 | 0.087 | 0.23 | 0.82 |
| Thr | 0.64 | 0.58 | 0.078 | 0.35 | 0.86 |
| Trp | 0.86 | 0.77 | 0.125 | 0.42 | 1.20 |
| Val | 0.74 | 0.66 | 0.099 | 0.37 | 1.01 |
- Estimadas com rma.mv (pacote metafor, R); dados ponderados por raiz de n; termos linear e quadrático significativos (P < 0.02); eficiência-alvo = eficiência quando a soma exportação + acreção de PL (ou AAE) é máxima (primeira derivada) [p.97]. Para a análise assumiu-se crescimento médio 0.19 kg/d (18 g PVer/d; Holandesa 1ª lactação) ou 0.14 kg/d (13 g; Jersey) e gestação = 0.
- A alvo de Phe foi aumentada de 0.57 para 0.60 (estudos de eliminação); Phe e Thr podem estar ligeiramente subestimadas (preferiu-se subestimar eficiência a subestimar a recomendação) [pp.97-98]. Arg não tem recomendação. Para uso do alvo em diagnóstico de dietas ver seção 6.

### Tabela 6-5 — Exemplo de aportes adequados de AAE: vaca adulta não gestante, 650 kg PC, 26 kg/d de dieta com 34 % de FDN [p.99] (verificada)
| PPL, g/d | His | Ile | Leu | Lys | Met | Phe | Thr | Trp | Val | PM |
|---|---|---|---|---|---|---|---|---|---|---|
| g/d: 1,000 | 55 | 112 | 187 | 159 | 50 | 117 | 110 | 26 | 125 | 2,122 |
| g/d: 1,200 | 63 | 130 | 216 | 183 | 58 | 134 | 124 | 30 | 144 | 2,411 |
| g/d: 1,400 | 71 | 147 | 245 | 208 | 67 | 152 | 139 | 34 | 162 | 2,701 |
| %PM: 1,000 | 2.60 | 5.29 | 8.83 | 7.48 | 2.35 | 5.51 | 5.19 | 1.23 | 5.89 | — |
| %PM: 1,200 | 2.61 | 5.37 | 8.97 | 7.60 | 2.42 | 5.57 | 5.16 | 1.24 | 5.96 | — |
| %PM: 1,400 | 2.62 | 5.44 | 9.08 | 7.69 | 2.46 | 5.63 | 5.14 | 1.25 | 6.01 | — |
(OCR trazia "no" para 110 e "q" para 71; corrigido pela imagem.)
**Reprodução numérica (caso de teste para o implementador):** BW 650, DMI 26, NDF 34 %: NP-scurf = 0.17*650^0.60 = 8.28 g; CP-MFP = (11.62+0.134*34)*26 = 420.6; NP-MFP = 307.0 g; NP-endogenous urinary = 53*6.25*650*0.001 = 215.3 g. PM(1,000) = (1,000+8.28+307.0)/0.69 + 215.3 = 2,121.5 (livro 2,122); PM(1,200) = 2,411.4 (2,411); PM(1,400) = 2,701.3 (2,701). Para cada AA: Rec = (PPL*[leite]/100 + NP-scurf*[desc]/100 + NP-MFP*[MFP]/100)/Eff_alvo + 0.010*6.25*BW*[corpo vazio]/100 (+ (7.82+0.55*BW)/1000 só para His); exemplo Lys @1,000: (88.2+0.47+23.4)/0.72 + 3.2 = 158.9 -> 159. Reprodução de todas as 27 células de g/d: iguais, exceto Phe a 1,200 g (135 calculado vs 134 do livro, arredondamento). Sem gestação nem crescimento no exemplo.

### Valores e constantes fixos do capítulo (resumo)
| Constante | Valor | Pág. |
|---|---|---|
| N x fator PB | 6.25 (leite: 6.34) | 76, 94 |
| PVer/PB da Pmic | 0.824 (82.4 %); NRC 2001: 0.80 | 85 |
| Digestibilidade verdadeira da PVer microbiana (todos os AAE) | 0.80 | 86 |
| Conversão Pmic -> PM | 0.824 x 0.80 = 0.659 (NRC 2001: 0.64) | 86 |
| Contribuição ao fluxo microbiano: bactérias associadas ao fluido / às partículas / protozoários | 33.4 / 50.1 / 16.5 % (a ordem dos dois primeiros segue a frase "fluidos e partículas"; protozoários = 16.5 % está explícito na p.86) | 85-86 |
| Recuperação de AA com hidrólise 24 h; 1 g PVer -> ~1.15 g AA hidratado | fatores no Cap. 18 | 85 |
| PVer/PB: descamação 0.85; urinária endógena 1.0; PMF 0.73; leite 0.951 (se PVer/PB desconhecida); crescimento 0.86 | — | 93-96 |
| Perfil AA e digestibilidade da PNDR | mesma do ingrediente (perfil) e = digestibilidade da PB (PNDRd) para todos os AA | 86-87 |
| Proteína no ganho: frame 0.11 (ver 4.12); reservas 0.08 | — | 96 |
| Proteína do útero gravídico | 125 g/kg ganho úmido | 95 |
| Eficiências fixas: gestação 0.33; crescimento (secas/novilhas) 0.40; urinária endógena 1.0 | — | 96-98 |
| ED da PM (para IEDnp) | 5.65 kcal/g PM | 89 |
| Equivalente: síntese de novo de Arg estimada | ~30 g/d | 78 |

---

## 6. Regras de decisão / restrições para o otimizador

1. **PDR da dieta: mínimo 10.0 % da MS (valor derivado da abordagem atual, geralmente maior que o NRC 2001) e máximo 12.0 % da MS** para otimizar o fluxo de Pmic [p.82]. Fluxo de N microbiano maximizado em 12 % de PDR e decresce linearmente abaixo de 12 % (IC maior abaixo de 10 %); IMS e PPL máximas em ~12.2 e 12.3 % PDR (Reynal e Broderick 2005). PDR deficiente deprime IMS [pp.82].
2. **Prioridade de balanceamento: AAE individuais, não PM.** "A ênfase deve ser colocada no cumprimento das recomendações de AAE em vez das de PM"; PM só como guia geral/histórica; recomendações de PM são em média menores que as do NRC (2001) [pp.99-100]. Foco em AAE exceto Arg [p.102]. Não há recomendação de Arg. Dados de Trp são muito limitados: aporte e recomendação devem ser interpretados com cautela [p.78].
3. **Recomendações de AAE** = Eq. 6-14b/d com eficiências-alvo da Tab. 6-4; **não há razão única AA:PM** (ela muda com a proporção de leite no total de demandas) [p.99]. Não há exigência fixa (resposta quadrática/aditiva): todo AAE tem retorno decrescente; um único conjunto de exigências não pode ser definido a partir da Eq. 6-6, por isso as recomendações são "diretrizes" calculadas fatorialmente [p.91].
4. **Uso da eficiência-alvo como diagnóstico** [p.98]: eficiência observada > alvo => AAE provavelmente limitante (suprimento baixo) e pode reduzir PPL; eficiência < alvo => AAE tendendo ao excesso (custo econômico/ambiental, não necessariamente prejudicial exceto desequilíbrio grave). O AAE com maior diferença entre eficiência observada e alvo é o de menor oferta relativa (ranking), mesmo que o valor absoluto seja incerto.
5. **PPL máxima**: Eq. 6-6 tem forma quadrática com máximo; para vacas de maior produção usar reescalonamento do Cap. 20 [p.91].
6. **Energia fermentável + PDR**: devem ser complementares; evitar ao mesmo tempo PDR em excesso e déficit de carboidrato degradável [pp.99, 107]. Ureia substituindo proteína verdadeira da PDR deprime Pmic, IMS e PPL (Broderick e Reynal 2009) [p.82].
7. **Estresse térmico**: fornecer para atender, mas não exceder, as exigências de PDR e AA (dados limitados) [pp.107].
8. **Vacas secas** (texto, p.95-96): exigência de PM para gestação (baseada em feto de 44 kg ao nascer; Tabela 3-3, Cap. 3) ~25 % menor aos 60 d pré-parto e ~37 % maior aos 5 d pré-parto vs NRC 2001; **PM necessária 829 g/d (9.6 % PB) aos 60 d pré-parto e 956 g/d (13.5 % PB) aos 5 d pré-parto** (IMS típica de seca; eficiência gestação 0.33; 60 % da PB retida como PM). Para PDR ~10 % da MS e digestão, dieta de secas ~ **12 % PB (recomendação do comitê)**; 11 % PB parece adequado (Cap. 12), mas poucos estudos < 10 %; novilhas no fim da gestação provavelmente se beneficiam de mais (>= 14.5 % PB em meta-análise, Cap. 12). Colostro (> 1 kg de proteína na 1ª ordenha) NÃO está incluído nos cálculos.
9. **Fertilidade**: o comitê NÃO apoia o papel do excesso de proteína (dentro de fator de segurança razoável) na redução de fertilidade, a menos que NUP alto resulte de energia insuficiente e mobilização corporal; NUL pode ser indicador de manejo (faixa 9-18 mg/dL em Guo et al. 2004) mas varia entre vacas/rebanhos [pp.106-107]. Evitar dietas com excesso de PM em relação à EM [p.106].
10. **Mantença**: o livro troca "mantença" por "funções não produtivas" (descamação, urinária endógena, PMF). PMF é a maior parte e depende da IMS/FDN; não é exigência basal [pp.92-93].
11. **Ressalvas de uso**: His é o AAE mais provável de limitar quando a Pmic é grande parcela da PM (dietas de baixa PB, silagem de milho/capim); Pmic é baixa em His [p.100]. Dietas de baixa PB podem ter múltiplas deficiências de AAE, visíveis quando se avalia AAE metabolizável [p.100]. Cys, Tyr, Pro, Gln: sem evidência clara de limitação [p.102].
12. **AA protegidos** (informação para parâmetros de produto, não do cálculo): biodisponibilidade de AA-PR = escape ruminal x digestibilidade intestinal; apenas Lys e Met comerciais; métodos no Cap. 18 [p.103]. HMTBA: biodisponibilidade pós-absortiva estimada em 18 % da dose ingerida (Lobley et al. 2006), absorção portal média 13 % (Lapierre et al. 2007b) [p.104]; DL-Met: >= 75 % do D-Met convertido em L-Met [p.103]; Zanton et al. (2014): PPL +2.23 g proteína/g Met metabolizável até um ponto de interrupção, semelhante à inclinação de Met na Eq. 6-6 (1.84) [p.104].

---

## 7. Lógica e fluxo (ordem de cálculo)

1. **Dieta -> PNDR e PDR (por ingrediente/classe):** PB, A, B, C, kd (Cap. 19) + kp estático (4.87 forragem / 5.28 concentrado %/h) + DCa (escape A 6.4 %) -> Dt_RUP (Eq. 6-1). **PDR = PB - PNDR** (relação implícita; o livro não escreve a subtração explicitamente, mas usa "PDR (kg/d) ... modificada para refletir a abordagem kd/kp" [p.81]) ⚠.
2. **Carboidratos degradáveis:** RDNDF (6-4a) e RStDig/RDS (6-4b).
3. **Pmic:** Eq. 6-3 -> N microbiano (g/d) x 6.25 = Pmic (PB). A PDR (kg/d) entra no numerador e RDNDF/RDS no denominador.
4. **N endógeno duodenal (Eq. 6-2):** usado para ajustar NNANM observado (calibração e comparação com fluxos); **não entra no aporte líquido** nem nas recomendações.
5. **Aporte líquido de PM = PM da PNDR + PM da Pmic** [p.77]:
   - PM_Pmic = Pmic(PB) x 0.824 (PVer/PB) x 0.80 (digestibilidade) = Pmic x 0.659.
   - PM_PNDR = PNDR (PB) x PNDRd (digestibilidade intestinal, Cap. 19) — o texto define PM como "PVer digerida após o rúmen"; a relação PVer/PB da PNDR e a fórmula explícita de agregação NÃO estão no Cap. 6 (ver Cap. 19/20). ⚠
6. **Aporte de AAE metabolizáveis (método fatorial)** [pp.78, 86-87]: AA_PNDR = PNDR x PNDRd x perfil de AA do ingrediente (Tabela 19-2 corrigida; mesmo perfil antes e depois do rúmen e mesma digestibilidade da PB para todos AA) + AA_Pmic = Pmic x 0.824 x 0.80 x perfil microbiano da Tabela 6-2 (g AA/100 g PVer). A fórmula escrita não aparece no capítulo — implementar conforme este texto e conferir com o Cap. 20. ⚠ Fluxos duodenais "de apresentação" são reconvertidos para base não corrigida; equações internas usam AA corrigido.
7. **Predição de PPL (Eq. 6-6)** com AA metabolizáveis (His, Ile, Leu, Lys, Met), OthAA, soma de quadrados, DEInp, dNDF, BW.
8. **Demandas líquidas** (por função): descamação (6-7), urinária endógena (6-8), PMF (6-9), leite (6-10; PPL da Eq. 6-6 ou informada), gestação (6-11), crescimento (6-12).
9. **Eficiência:** observada (6-13) para diagnóstico; alvo (Tab. 6-4) para **recomendação** (6-14a/b para lactantes, 6-14c/d para não lactantes/novilhas).
10. **Comparação aporte vs. recomendação** por AAE e PM, com eficiências observadas vs. alvo (item 4 da seção 6).
- **De outros capítulos:** IMS (Cap. 2), ED/EM/ELL e dNDF, peso do útero gravídico/bezerro (Cap. 3), proteína no ganho de PC vazio (Cap. 11), dietas de secas (Cap. 12), métodos laboratoriais e fatores de recuperação de AA (Cap. 18), biblioteca de alimentos (A, B, C, kd, PNDRd, AA; Caps. 19), reescalonamento da Eq. 6-6 (Cap. 20), excreção de N (Cap. 14).

---

## 8. Limitações, incertezas e mudanças vs. NRC 2001

**Mudanças principais vs. NRC 2001** [pp.76-78, 82, 85-87, 93-99]:
- PDR/PNDR: mantém A, B, C e kd in situ, mas kp passa a ser **estático** (forragem 4.87, concentrado 5.28 %/h) + escape da fração A (6.4 %); NRC 2001 tinha 3 equações de kp dependentes de IMS/FDN/% concentrado (uma com erro de coeficiente corrigido por Seo et al. 2006). Viés do NRC 2001: intercepto 19 % e inclinação 22 % do MSEP frente ao NNANM; após correção de dados 7 % cada, viés 120 g/d e -0.31 g/g [pp.78-79]. Exemplo de insensibilidade: farelo de soja, prensado e tostado (não tratado) com PNDR 0.28, 0.30 e 0.28 g/g PB [p.79]; o kd ainda é necessário para que processamentos aumentem a PNDR.
- Pmic: de NDT (descontado) para função **Michaelis-Menten de PDR, FDN e amido degradáveis** (6-3, 6-4a/b); PDR não é mais convertida com eficiência fixa 1/1.18 (NRC 2001; NRC 1989: 0.9; NASEM 2016 corte: 100 %). A Pmic máxima = PDR.
- N endógeno duodenal: de 1.9 g N/kg IMS para regressão com intercepto (6-2).
- Pmic -> PM: PVer/PB 0.80 -> **0.824**; digestibilidade 0.80 mantida; conversão 0.64 -> 0.659.
- AAE: de regressões semi-empíricas por PNDR (NRC 2001) para **método fatorial** (Pmic, PNDR, PB endógena); composição AA corrigida por recuperação da hidrólise; perfil microbiano inclui protozoários (16.5 %, mais Lys) e fases líquida/partícula (Sok et al. 2017).
- Exigências: de **proporcional** (AA como % da PM, razões ideais Lys:Met) para **fatorial** (Net AA / eficiência-alvo); 
- Eficiências: antes PM->leite fixa 0.67; agora **variável** e alvo 0.69 (PM) e 0.60-0.86 (AAE); PMF e descamação agora com a mesma eficiência-alvo; urinária endógena com 1.0.
- PMF: antes IMS x 30 menos ajuste bacteriano; agora (11.62 + 0.134 FDN) x IMS, x 0.73.
- Gestação: modelo de Koong et al. (1975) ajustado a Bell et al. (1995), com peso do bezerro; eficiência 0.33 mantida.
- Crescimento: eficiência de conversão de PM para PL de crescimento agora em função do PC/PC maduro (Cap. 11); em lactantes recebe a mesma eficiência-alvo.
- Leite: relação PM -> PPL passou de linear com eficiência fixa a quadrática/aditiva (Eq. 6-6); RMSE 14.4 % vs 21-25 %.
- Biblioteca: PNDRd muito mais completa (antes em incrementos de 5 pontos); 24 h de incubação in situ de farinha de peixe removida (insuficiente para a fração C).
- Fator de conversão N-PB do leite: 6.34.

**O que o texto admite não saber / limitações:**
- Equação de Pmic (6-3): CCC apenas 0.52, RMSE ~30 %; banco sub-representa raças pequenas e IMS > 30 kg/d; mais pesquisa para novilhas e vacas secas (PDR muito baixa) [p.82]. Não considera fibras solúveis e açúcares extra (pode subestimar Pmic com grandes quantidades), gordura suplementar, sincronização energia-proteína, nem reciclagem de NUP (embora implícita nos dados) [pp.82-84].
- kp estático/kd: CCC 0.54, RMSE 40.9 %; kd in situ (contaminação bacteriana, até 5 pontos percentuais de PDR; lavagem de partículas) [pp.79-80].
- Digestibilidade intestinal AA a AA na PNDR assumida igual à da PB; evidências in vivo (isótopos) indicam que está incorreta; AA da PNDR assumido com o perfil do ingrediente original [pp.86-87].
- AA-específicos de degradabilidade e digestibilidade microbiana: dados insuficientes [p.86].
- Composição AA do leite assumida constante (pode ser falsa em estudos de deleção) [p.95].
- Eficiência de gestação 0.33 sem suporte (propostas 0.50, 0.33, 0.65); requisitos de colostro, imunidade, reprodução, mobilização/recuperação corporal NÃO incluídos [pp.96, 98].
- Eq. 6-6: limitada à população de 920 g/d; Trp, Val, Phe, Thr, Arg não entram individualmente (instáveis); AANE e demais AA agrupados em OthAA; DEL e gordura do leite sem efeito incluído [pp.90-91]. Necessários experimentos com delineamento composto central [p.89].
- Os requisitos de AA além de síntese proteica (gliconeogênese, mTOR, metilação) não quantificados [p.100].
- Eficiências-alvo de Phe e Thr possivelmente subestimadas [p.98].
- Sem efeito de gordura/protozoários, nem NUP explícito no modelo de Pmic; sem calor adicional da excreção de N (a energia da perda urinária de N é descontada no Cap. 3) [p.107].

---

## 9. Conceitos e evidências relevantes

- **PM** = PVer digerida após o rúmen; aporte líquido = PM da PNDR + PM da Pmic; proteína endógena duodenal não é suprimento novo (sintetizada de AA já absorvidos) [pp.76-77].
- **AAE** (9): His, Ile, Leu, Lys, Met, Phe, Thr, Trp, Val; Arg condicionalmente essencial (síntese de novo ~30 g/d; retirada de Arg da infusão não afetou PPL; presente em 68 % das melhores equações); AANE: Ala, Asn, Asp, Cys, Glu, Gln, Gly, Pro, Ser, Tyr [p.78, 101].
- **Resposta aditiva e não linear a vários AAE e energia** (em vez de "primeiro limitante"): suportada por sinalização mTOR/tecido mamário (Met, Leu, Ile, Thr, insulina, acetato) [pp.89, 100]. Exemplos: excluir His, Lys ou Met da mistura infundida reduziu PPL em 20 % sem mudar a PM; excluir His ou Phe -23 %; excluir Phe -16 % [p.100]. AA-PR (His+Lys+Met) permitiram reduzir PM em 450 g/d (Lee 2012a; Giallongo 2016) e 375 g/d (Haque 2015) mantendo PPL [p.100].
- Grupos de AAE (Mepham 1982): Grupo 1 (His, Met, Phe+Tyr, Trp) = captação mamária estequiométrica à proteína do leite, extração hepática alta; Grupo 2 (Ile, Leu, Lys, Val; Arg e Thr) = captação mamária maior que a secretada (excedente usado para AANE, p.ex. Arg -> Pro) [p.101]. Em vacas secas gestantes a remoção hepática de AA do grupo 1 é ~2x a de lactantes [p.95].
- Proporções observadas: Cys/(Cys+Met): leite 0.23, Pmic 0.46, ingredientes > 0.40; Tyr/(Tyr+Phe): leite 0.53, Pmic 0.48 [p.102]. AAE/PM em tratamentos controle: 42-48 % (média 45.4 %) [p.100].
- Reciclagem de ureia: 60-85 % do N digerido vira ureia hepática; 15-30 % do N microbiano ruminal vem do NUP (Li et al. 2019); NMU média 14.6 % (EPM 2.1 %) em 4 estudos com PB 12.5-18.6 % (Fig. 6-2); Batista et al. 2017: 21 % do N ureico reciclado com 15 % PB [pp.83, 107]. O comitê NÃO incluiu a transferência de NUP explicitamente [p.77].
- Proteína microbiana: composição constante; ácidos nucleicos (~14 % do N total) respondem pela fração não PVer; glucosamina ~1 % da PB [p.85]. Protozoários têm até 2x mais Lys que bactérias [p.86].
- Comparação com outros sistemas: PDI francês, DVE/OEB2010 holandês, CNCPS (todos usam o perfil de AA do ingrediente para a PNDR) [p.86].
- IMS e proteína: PB dietética associada positivamente à IMS; His-PR mostrou maior resposta de IMS entre AA-PR; PDR de 9.4 -> 10.3 % aumentou IMS e 11.0 -> 12.1 % diminuiu (Mutsvangwa 2016) [p.105].
- Reprodução, transição, metionina protegida na transição (neutrófilos, estresse oxidativo, gordura hepática) [pp.104-106]; nutrição proteica adequada na transição (poupar proteína corporal, maior pico) [p.106].
- Meta-análises citadas sobre AA-PR: Vyas e Erdman (2009): eficiência marginal 39 -> 25 % (Lys) e 44 -> 22 % (Met); Patton (2010): Met-PR +0.07 pontos % e +27 g/d de proteína do leite; Zanton (2014): +2.23 g proteína/g Met metabolizável [p.104].

---

## 10. Dúvidas / riscos de OCR (itens ⚠ para conferência humana)

1. ⚠ **Eq. 6-4a**: parênteses impressos incompletos; usei a leitura (coeficientes) x (FDN em kg/d)/100; confirmar com o original em inglês. [p.82]
2. ⚠ **Eq. 6-8b**: impressa idêntica à 6-8c (inclui 3-metil-His e rotula "NetHis"); a versão correta para os demais AAE é a sem o termo 3-MH (confirmada pela reprodução da Tabela 6-5). [pp.93-94]
3. ⚠ **Eq. 6-13a**: sinal "+" ausente antes de NP-growth na quebra de linha. [p.97]
4. ⚠ **Eqs. 6-14c/d**: texto diz "vacas em final de lactação e novilhas"; contexto sugere vacas secas/não lactantes e novilhas. [p.98]
5. ⚠ **Eq. 6-12a**: o 0.86 é descrito como PVer/PB (p.96) e como PC vazio/PC (p.97). Valor numérico igual (0.86); semântica inconsistente. Também a fração de ganho de PC vazio é 85 % (p.96) vs 0.86 no cálculo.
6. ⚠ **Eq. 6-3 vs 6-4b**: o texto de 6-3 chama o amido degradável de "RDS"; a Eq. 6-4b chama de "RStDig"; o parágrafo introdutório mistura "amido degradável no rúmen (FDNDR, RDNDEF)". Tratar RDS = RStDig; RDNDF = FDN degradável.
7. ⚠ **Eq. 6-1**: DCa descrito como degradabilidade da fração A, mas o valor estimado é de "escape" (6.4 +/- 4 %); implementação deve usar (1 - DCa) = 0.064 (a confirmar). Kp estático: frase "5.28 e 4.87 para concentrados e forragens, respectivamente" — ordem assumida literalmente. Número de classes c (forragem seca/úmida e concentrado?) ambíguo ("forragens úmidas e secas e concentrados" no texto de p.80, mas só 2 valores de kp são dados).
8. ⚠ **Eq. 6-2**: "±" impresso entre intercepto/inclinação; interpretados como EP. Confirmado na imagem.
9. ⚠ **Eq. 6-6**: o símbolo do termo quadrático "EAAb_a" impresso com subscrito "a" ambíguo; definido no texto como a soma dos quadrados dos 5 AAE (His, Ile, Leu, Lys, Met).
10. ⚠ **Tabela 6-3**: P do viés de inclinação da Eq. 6-6 (0.0001) com viés de inclinação de 3.1 % do MSE; viés de inclinação impresso como "0.156" g/g (sem sinal, ao contrário dos três NRC, negativos) — conferir; divergências entre texto e tabela (ver seção 5).
11. ⚠ **Tabela 6-2**: OCR errou Asx (4.15), Ser fecal ("77"), Gly e vários decimais; corrigidos pela imagem. Somas de controle na seção 5.
12. ⚠ **Purinas urinárias**: "27.1 mg N/PC^0.75" no texto (expoente 0.75) — não entra em equação.
13. ⚠ Aporte de PM/AAE: a fórmula explícita de agregação (PNDR x PNDRd; PVer/PB da PNDR; AA do ingrediente) não está no Cap. 6; conferir no Cap. 20/19. A forma de obter **PDR (kg/d)** e a PM da PNDR deve ser conferida lá.
14. ⚠ Texto/figuras: Figuras 6-1 a 6-4 (resíduos da Pmic, razão NMU, resíduos de PPL) vistas só pelo OCR/legendas (nenhum valor numérico de modelo); não reproduzidas.
15. ⚠ Contagem de estudos/N: "1,149 médias de tratamento de 275 experimentos; 898 de 216 estudos" [p.88] vs N = 926 na Tabela 6-3 (subconjunto com PM/ELL calculável) — não explicada no texto.

---

COBERTURA: páginas lidas 76–115. Texto técnico integral (OCR + conferência por imagem de pp.80-82, 87-90, 93-99; figuras pp.83-84, 91-92 só por OCR/legendas) lido nas pp.76-107; pp.107-115 (referências) apenas percorridas (pp.107-110 lidas por OCR; pp.111-115 só o início de cada página, confirmando que são só referências; o Cap. 7 de Minerais começa na p.116), sem conteúdo técnico. Tabelas 6-1 a 6-5 e Eqs. 6-1 a 6-14d (26 equações) conferidas contra imagem; Tabela 6-5 reproduzida numericamente. Ficaram de fora: valores individuais de kd/PNDRd/AA por ingrediente (Caps. 18-19), o reescalonamento da Eq. 6-6 (Cap. 20) e dados dos gráficos (Figs. 6-1 a 6-4).

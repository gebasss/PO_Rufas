# NASEM 2021 (Exigências Nutricionais de Bovinos Leiteiros, 8ª ed., PT-BR) — Notas técnicas: Cap. 13, 14, 15 e 16

**Capítulos e páginas impressas cobertas:** Cap. 13 "Sistemas de Produção de Leite" (p.316–324 texto; referências p.324–327); Cap. 14 "Nutrição dos Bovinos Leiteiros e o Meio Ambiente" (p.328–337 texto; referências p.338–342); Cap. 15 "Subprodutos" (p.343–355 texto; referências p.355–361); Cap. 16 "Aditivos" (p.362–366 texto; referências p.366–368).

**Usado diretamente no modelo? (por capítulo)**
- Cap. 13 — **parcial/sim**: só a parte de **pastejo** gera equações (Eq. 13-1 IMS de forragem em pasto sem suplemento; Eq. 13-2 e constantes de locomoção para a exigência de atividade em ELL). TMR, agrupamento, ordenha robotizada, orgânico e culturas GM são discussão (sem equação; só regras de manejo).
- Cap. 14 — **sim/parcial**: Eq. 14-1a (metano; é a mesma base da Eq. 3-9 do Cap. 3) entra no modelo de energia. Eq. 14-15a/b/c (esterco total) são declaradas como "usadas no software". O próprio software calcula excreção de N por **balanço de massa**; as Eq. 14-4 a 14-14 são "fornecidas para análise entrada-saída" (alternativas empíricas) [p.332]. Eq. 14-1b/c, 14-2 e 14-3 são recomendadas pelo livro mas o texto não diz que estão no software. Mitigação, N2O, NH3, COV, qualidade da água = discussão.
- Cap. 15 — **não** (só discussão; composição dos alimentos está no Cap. 19). O livro declara que NÃO recomenda taxas de inclusão ótimas [p.343].
- Cap. 16 — **não** diretamente; **exceção numérica:** o modelo aplica um ajuste para monensina (+2% ED, −5% energia de CH4 → +2.7% EM, +2.5% ELL) [p.363]. Demais aditivos = discussão.

Convenções: decimal ponto, milhar vírgula; `^` expoente, `_` subscrito, `*` multiplicação; `[p.N]` = página impressa. "(corrigido pela imagem)" = OCR divergiu e vale a imagem. Valores entre parênteses nas equações do livro são erros-padrão dos coeficientes (nas Eq. 14-1a, 14-2, 14-3 aparecem como ±; em 14-1b/c e 14-5 a 14-14 o livro os traz entre parênteses ou com ±; o texto nunca os rotula, mas pela magnitude são EP). Glossário PT↔EN: IMS=DMI; PC=BW; PL=milk yield; ELL=NEL; EM=ME; ED=DE; IEB=GEI (ingestão de energia bruta); AG=FA (ácidos graxos); GB/FB=gordura bruta/extrato etéreo (ver ⚠); FDNd=FDN digestível; HC=hemicelulose; PB=CP; OF=oferta de forragem (PA, pasture allowance); AMS=ordenha robotizada; PMR=ração parcialmente misturada.

---

# CAPÍTULO 13 — Sistemas de Produção de Leite (p.316–324)

## 13.1 Papel no simulador
Para vacas em TMR **não há ajuste** de exigências [p.316]. Para pastejo, as exigências de todos os nutrientes são iguais às de confinamento, **exceto energia (e talvez proteína)**: soma-se à exigência de ELL um termo de **atividade de pastejo** (locomoção horizontal piquete↔sala de ordenha + locomoção vertical + custo de colher o alimento) [p.319]. A IMS de vaca a pasto exclusivo tem equação própria (Eq. 13-1); com concentrado, usa-se a Eq. 2-1 (Cap. 2) [p.318]. O caminhar *dentro* do piquete é assumido igual ao do galpão e já está embutido na mantença [p.319].

## 13.2 Entradas (pastejo)
| Variável | Símbolo/sigla | Unidade | Definição | Faixa/valores típicos | Pág. |
|---|---|---|---|---|---|
| Oferta de forragem | OF (PA) | kg MS/vaca/d | Forragem consumível oferecida por vaca por unidade de área | patamar da IMS em ~108–110 | 317–318 |
| Peso corporal | PC (BW) | kg | Peso da vaca | exemplo 650 | 319–320 |
| Distância horizontal total percorrida piquete↔centro de ordenha | — | km/d | Soma de todas as viagens (ida e volta) no dia; no exemplo 0.6 km × 4 viagens de ida | exemplo 2.4 km/d | 319–320 |
| Distância vertical positiva (ganho de elevação) | — | km/d | Informada pelo usuário OU escolhida por classe qualitativa | leve 0.05; moderado ≈0.2; severo ≈0.5 | 319 |
| IMS que não vem de pastagem | — | kg MS/d | Concentrado, silagem de milho, feno etc. consumidos | exemplo 6 (concentrado) | 319–320 |
| Concentrado suplementar (sim/não, quantidade) | — | kg MS/d | Define qual equação de IMS usar (13-1 sem suplemento; 2-1 com) | — | 318 |

## 13.3 Saídas
| Variável | Unidade | Definição | Pág. |
|---|---|---|---|
| IMS de forragem (vaca a pasto sem suplemento) | kg/d | Saída da Eq. 13-1 | 318 |
| Exigência de ELL de locomoção horizontal | Mcal ELL/d | 0.00035 × PC × km | 319–320 |
| Exigência de ELL de locomoção vertical | Mcal ELL/d | 0.0067 × PC × km vertical | 319–320 |
| Exigência de ELL de colheita do alimento (pastejo) | Mcal ELL/d | Eq. 13-2 | 320 |
| Exigência total de atividade em pastejo | Mcal ELL/d | soma dos três termos | 320 |

## 13.4 Equações

**Eq. 13-1** [p.318] — IMS de forragem de vacas em pastejo **sem outros alimentos como suplemento**. Imagem conferida (OCR tinha "<108" e "OF?"; imagem: "≤ 108" e "OF^2" — corrigido pela imagem).
```
Se OF <= 108:   IMS_forragem = 7.79 + 0.26*OF - 0.0012*OF^2
Caso contrário: IMS_forragem = 21.9
```
- IMS_forragem em kg/d; OF em kg MS/vaca (por dia). 
- Origem: meta-análise de Bargo et al. (2003); n de estudos, R² e RMSE **não informados**. A IMS cresce quadraticamente com OF e atinge platô em ≈110 kg MS/vaca/d no texto (limiar 108 na equação) [p.318]. Verificação aritmética (minha): em OF=108 a equação dá 21.87 ≈ 21.9 (contínua no limiar).
- Validade: vacas Holandesas médias pastando forragem de alta qualidade, **sem outros alimentos**. PC médio do banco não foi apresentado; a equação **superestima IMS de Jersey** [p.318].
- Com concentrado suplementar: **usar a Eq. 2-1 (Cap. 2)** para IMS total (NRC 2001 considerada aceitável por Bargo et al. 2003). A equação mais complexa de Caird e Holmes (1986) (altura do pasto, OF, concentrado) também foi precisa, mas não é a recomendada [p.318].

**Eq. 13-2** [p.320] — ELL diária para colheita do alimento no pastejo (apreensão, mastigação, caminhada durante o pastejo). Imagem conferida (OCR tinha "PCº?3"; imagem: PC^0.75).
```
ELL_pastejo (Mcal/d) = (0.0075 * PC^0.75) * (600 - (12 * IMS_nao_pasto)) / 600
```
- 0.0075 Mcal/kg PC^0.75/d = média do custo de colher alimento com **nenhum** concentrado (faixa medida 0.003–0.025; Di Marco 1996; Aharoni 2009; Brosh 2010); animais pastejavam ≈10 h/d (=600 min) [p.319].
- 12 = minutos de pastejo reduzidos por kg de MS de concentrado fornecido (Bargo 2003) [p.319]. 600 = minutos de pastejo/dia sem suplemento.
- IMS_nao_pasto em kg MS/d (o texto fala em "alimento que não seja pastagem": silagem de milho, feno, concentrado etc.) [p.319]. Efeito ilustrativo: passar de 2 para 12 kg/d reduz o gasto em ≈0.2 Mcal para vaca de 650 kg [p.319–320] (conferido: 0.0075×650^0.75×(120/600)=0.19).
- O livro não diz o que fazer se 12×IMS_nao_pasto > 600 (IMS não-pasto > 50 kg/d); sugestão de implementação (não do livro): limitar o fator a ≥0.

**Constantes de locomoção (não numeradas como equação)** [p.319–320]:
```
ELL_horizontal (Mcal/d) = 0.00035 * PC * distancia_horizontal_total (km/d)
ELL_vertical   (Mcal/d) = 0.0067  * PC * distancia_vertical_positiva (km/d)
ELL_atividade_total     = ELL_horizontal + ELL_vertical + ELL_pastejo(Eq. 13-2)
```
- 0.00035 Mcal ELL/kg PC/km: derivado de vacas de corte (Brosh 2006, 2010; Aharoni 2009); faixa medida 0.0003–0.0004; **−22% vs NRC 2001 (0.00045)**; possivelmente ainda superestimado [p.319]. É o mesmo valor (0.35 kcal ELL/kg PC/km) usado no Cap. 3 para o deslocamento à sala de ordenha em confinamento.
- 0.0067 Mcal ELL/kg PC/km vertical: literatura indica 9–19× o custo horizontal; o comitê escolheu o valor **mais alto** (19×0.00035 ≈ 0.0067) [p.319–320]. Substancialmente menor que o NRC 2001 (que usou eficiência incorreta: vaca 650 kg, 0.2 km vertical → 0.9 Mcal/d agora vs 3.9 no NRC 2001; o valor corrigido do NRC 2001 seria 1.4) [p.319].
- Classes qualitativas de distância vertical (para uso quando o usuário não informa km): leve 0.05 km/d → 0.2 Mcal/d; moderado ≈0.2 km/d → 0.9 Mcal/d; severo ≈0.5 km/d → 2.2 Mcal/d (todos para vaca de 650 kg) [p.319]. Conferência (minha): 0.05×0.0067×650=0.218; 0.2→0.871; 0.5→2.18.
- Novilhas: o custo energético de pastejo "não é conhecido"; sem equação [p.320]. Em terreno plano o custo seria pequeno; maior em terreno montanhoso/pasto ralo.

**Exemplo do livro** [p.320] (vaca 650 kg, 6 kg de concentrado, pasto a 0.6 km da sala, 0.2 km de elevação [moderado], 4 viagens de ida/dia):
```
Horizontal: (0.6 km x 4 viagens) x 0.00035 x 650 kg = 0.54 Mcal ELL/d
Vertical:   (0.2 km) x 0.0067 x 650 kg               = 0.87 Mcal ELL/d
Pastejo:    0.0075 x 650^0.75 x 0.88                  = 0.91 Mcal ELL/d   (como impresso)
Total                                                 = 2.32 Mcal/d
```
⚠ **Inconsistência do livro:** recalculando, 650^0.75 = 128.7; 0.0075×128.7×0.88 = **0.85** (não 0.91); o total correto seria ≈2.26 Mcal/d. O fator 0.88 = (600−12×6)/600 confere. Diferença de 0.06 Mcal/d (≈2.6%); provável erro de arredondamento/impressão do livro. Implementar a fórmula (Eq. 13-2), não o número do exemplo.

## 13.5 Parâmetros e tabelas
Nenhuma tabela numerada no Cap. 13. Constantes consolidadas na seção 13.4. Valores de referência (narrativos): NRC 2001 horizontal 0.00045; vertical NRC 2001 → 3.9 Mcal/d (exemplo), corrigido 1.4 [p.319–320].

## 13.6 Regras de decisão / restrições para o otimizador (Cap. 13)
- **Pastejo sem suplemento:** limitar IMS de forragem pela Eq. 13-1 (máx. 21.9 kg/d; Holandês). Para Jersey, reduzir (a equação superestima; o livro não dá fator) [p.318].
- **Taxa de substituição concentrado→forragem em pasto:** 0.2–0.7 kg de MS de forragem a menos por kg de MS de concentrado (Bargo 2003); aumenta com OF e é maior com concentrado rico em amido que fibroso; concentrado misturado à forragem tem substituição semelhante [p.318]. Concentrado aumenta IMS total e leite, mas IMS segue < TMR [p.318].
- **Retorno decrescente:** ganho de EM ingerida torna-se marginal quando >8.5 kg MS/d de suplemento rico em amido (Doyle 2005) [p.318].
- Concentrado (principalmente amido) reduz digestibilidade da FDN na maioria dos estudos, com pouco ou nenhum ganho de digestibilidade energética da dieta total (ED ingerida sobe) [p.318–319].
- Fornecer o concentrado misturado à forragem estabiliza mais o rúmen (pH, AGV) sem digestibilidade consistentemente melhor [p.318].
- **Vitaminas em pasto:** forragens frescas têm β-caroteno e α-tocoferol altos → menor necessidade de suplementar vit. E, β-caroteno e A; maior exposição solar → menor necessidade de vit. D (sem números) [p.318]. Mg: absorção possivelmente baixa por K alto, não pelo pastejo em si [p.318–319].
- **Agrupamento (formulação de dieta de lote):** para PM, formular para a produção média do lote **+1 desvio-padrão**; para ELL, formular para a **produção média** do lote (evita vacas obesas) (Stallings e McGilliard 1984; Kalantari 2015) [p.317]. Formular para a vaca média causa perda de produção do grupo [p.317]. Agrupar para reduzir variação de exigência de PM e ELL é geralmente ótimo economicamente [p.317]. Separar primíparas de multíparas aumenta produção e melhora comportamento (benefício menor com >70 vacas/lote, confundido) [p.316]. Resposta marginal típica: **≈2 kg leite por kg de aumento de IMS** (Bach 2020, excluindo pós-parto imediato) [p.317]. Correlação IMS–produção é fraca no início e forte no fim da lactação [p.317].
- **TMR:** não ajustar exigências; MS da TMR 45–65% não afeta consistentemente a seleção; melaço líquido ≈4% da MS reduziu seleção; partículas longas são mais selecionadas (contra); seleção contra partículas grandes aumenta ingestão de energia, mas risco de acidose [p.316–317].
- **AMS (robô):** média norte-americana 15.9 kg de concentrado por 100 kg de leite (Tremblay 2016) [p.321]; acima de 4 kg de concentrado oferecido num evento de ordenha, aumenta o concentrado recusado [p.321]; razão de substituição PMR por concentrado do robô: 1.58 kg PMR a menos por kg (Hare 2018); varia 0.84–1.58 entre estudos (Paddick 2019) [p.321]; subir concentrado no robô de 2 para 6 kg/d reduziu PMR com efeito marginal no leite e aumentou a variabilidade [p.321–322]; minerais e vitaminas devem ser somados das duas fontes (robô + PMR) [p.321].
- **Orgânico:** exigências **não diferem** do convencional; muda o suprimento (menos concentrado, menos subprodutos, pastejo obrigatório em parte do ano → exigência de pastejo vale); composição de macronutrientes dos alimentos essencialmente igual [p.322–323]. Exemplo: melaço substituindo farelo de milho em dieta orgânica de baixo amido (10→2%) reduziu leite linearmente, ao contrário de dietas convencionais (23–31% amido; ~6% melaço aumentou leite) [p.322].

## 13.7 Lógica e fluxo (Cap. 13)
1. Se vaca em pasto exclusivo → IMS_forragem = Eq. 13-1(OF). Se com suplemento → IMS total = Eq. 2-1 (Cap. 2) e forragem = IMS − suplemento (taxa de substituição só informativa).
2. ELL_atividade = horizontal + vertical + Eq. 13-2 (usando IMS não-pasto da dieta definida). Soma-se às demais exigências de ELL (mantença Cap. 3, etc.; a mantença já inclui atividade de confinamento) [p.319, Cap. 3].
3. Demais exigências (PM, minerais, vitaminas) = as dos Caps. 6–8 sem alteração.
- Entradas vindas de outros capítulos: IMS (Cap. 2), PC, mantença/ELL (Cap. 3).

## 13.8 Limitações, incertezas e mudanças vs. NRC 2001 (Cap. 13)
- Custo horizontal −22% vs NRC 2001; custo vertical bem menor (NRC 2001 usara eficiência incorreta) [p.319–320]. Custo de colheita é novo (NRC 2001 não tinha termo equivalente numérico no texto lido).
- "Dados limitados e altamente variáveis"; distância vertical raramente conhecida; precisão geral limitada pela entrada [p.320]. Possível aumento da exigência de proteína em pasto: provavelmente pequeno, **sem quantificação** [p.320].
- Equação de IMS para vaca em pasto: base Holandesa; sem n, R², RMSE [p.318].
- D'Hour (1994): caminhar +6.4 km/d em terreno plano não alterou leite; a queda começou com +10 km/d [p.319].
- Estudo com novilhos Angus: gasto de pastejo 3.3× maior em pasto de 148 vs 228 g MS/m² (sem suplemento) [p.319]. Em pasto sem suplemento, OF é o maior determinante da IMS [p.317–318].
- Novilhas em pasto: adaptação leva 5–8 d; caminharam 2–5.5 km em 9 h nos primeiros 8 dias (Lopes 2013) [p.320].
- Ordenha robotizada/orgânico: faltam pesquisas (quantidade/composição da recompensa, peletização) [p.321–322].

## 13.9 Conceitos e evidências relevantes (Cap. 13)
- Melhores resultados econômicos com agrupamento por exigência de PM e ELL (simulações) [p.317]. Estágio de lactação como critério de agrupamento ajuda a controlar ECC (interação dieta × estágio na IMS, Cap. 2) [p.317].
- Eficiência de N (g N leite/g N ingerido) em pasto costuma ser menor que em TMR, mas reflete a composição da dieta, não o sistema; amido no concentrado reduz N urinário e aumenta eficiência [p.318]. Eficiência de síntese de proteína microbiana (g/g MO digerida) em pasto semelhante à de TMR por estimativas indiretas (alantoína); Silva 2014 mediu menor que o NRC 2001 (sem controle TMR) [p.318].
- Culturas GM: sem diferença de composição ou de produção/composição do leite vs isolinhas (meta-análise Ferraretto e Shaver 2015); sem transgenes/proteínas GM detectáveis no leite; milho com α-amilase e soja alto-oleico (aumentou gordura do leite e reduziu trans) com resultados iniciais; alfafa de baixa lignina com maior DIVFDN in vitro, sem estudo em vacas [p.323–324]. Cap. 13 não tem número de modelagem aqui.
- Dados brasileiros no texto: 52.8 milhões de ha de culturas GM no Brasil (2019) [p.323].

## 13.10 ⚠ Dúvidas/riscos de OCR (Cap. 13)
- ⚠ Exemplo p.320: 0.91 Mcal vs 0.85 recalculado (ver acima). Equações 13-1 e 13-2 e as constantes foram conferidas na imagem (p.318, 319, 320).
- ⚠ Páginas p.316, 317, 321 (números narrativos 15.9, 4 kg, 1.58, 0.84–1.58, 2 kg leite/kg IMS, >70 vacas) conferidos na imagem apenas p.321 e p.317 como OCR; p.317 narrativa **só OCR** (baixo risco). p.322–324 só OCR (texto corrido; números: 6% melaço, 10→2% amido, 23–31%, 71.5/52.8/24.0/12.5/11.9 Mha) — ⚠ NÃO-VERIFICADO na imagem, sem impacto no modelo.

---

# CAPÍTULO 14 — Nutrição dos Bovinos Leiteiros e o Meio Ambiente (p.328–337)

## 14.1 Papel no simulador
Fornece (i) a equação de **metano entérico** de vacas em lactação (Eq. 14-1a — a mesma usada para a energia gasosa na Eq. 3-9 do Cap. 3), com alternativas para novilhas e vacas não lactantes (14-1b/c); (ii) equações de **sólidos voláteis** do esterco (14-2, 14-3) para estimar CH4 do manejo de esterco pelo método IPCC (2006); (iii) equações empíricas de **excreção de N** (14-4 a 14-11) e de **P fecal** (14-12 a 14-14) — o software usa **balanço de massa** para N, e estas equações servem a análises entrada-saída; (iv) equações de **produção de esterco total** (14-15a/b/c) declaradamente usadas no software [p.332, 337].

## 14.2 Entradas
| Variável | Símbolo/sigla | Unidade | Definição | Faixa/valores típicos | Pág. |
|---|---|---|---|---|---|
| Ingestão de matéria seca | IMS | kg/d | Do Cap. 2 | — | 330–337 |
| FDN da dieta | FDN | % MS | — | — | 330–337 |
| FDN digestível da dieta | FDNd | % MS | FDN × digestibilidade da FDN (a Eq. 3-9 do Cap. 3 usa o mesmo termo, "dNDF_DM") | — | 330 |
| Ácidos graxos da dieta | AG | % MS | — | — | 330 |
| Gordura bruta / extrato etéreo da dieta | "FB" no texto (ver ⚠) | % MS | usado só na Eq. 14-1c | — | 330 |
| Ingestão de energia bruta | IEB | Mcal/d | — | — | 330 |
| Proteína bruta da dieta | PB | % MS | — | — | 330–337 |
| FDA da dieta / Hemicelulose | FDA / HC = FDN − FDA | % MS | — | — | 331 |
| Produção de leite | Leite (PL) | kg/d | — | — | 332, 336 |
| Proteína bruta do leite | PBleite | % | Eq. 14-4 (fator 6.38) | — | 332 |
| Ingestão de N | Ingestão de N | g/d | = IMS(kg)×PB(%)×10/6.25 (derivado do próprio livro: Eq. 14-4 usa /0.625) | — | 332 |
| Ingestão de P | ingestão de P | g/d | — | dietas comuns 0.45–0.50% P | 336 |
| Peso corporal | PC | kg | Eq. 14-15a/b | — | 337 |

## 14.3 Saídas
| Variável | Unidade | Pág. |
|---|---|---|
| Metano entérico | Mcal/d | 330 |
| Sólidos voláteis do esterco / sólidos voláteis digestíveis | kg/d | 330–331 |
| N do esterco, N urinário, N fecal, N do leite | g/d | 332 |
| P fecal | g/d | 336 |
| Produção de esterco (urina + fezes úmidas) | kg/d | 337 |

## 14.4 Equações

**Eq. 14-1a** [p.330] — Metano entérico, **vacas em lactação** (versão modificada de Nielsen et al. 2013; melhor modelo para América do Norte na avaliação de Appuhamy et al. 2016, 38 modelos). Imagem conferida.
```
Metano (Mcal/d) = 0.294 (±0.019) * IMS - 0.347 (±0.093) * AG + 0.0409 (±0.012) * FDNd
```
- IMS em kg/d; AG em % MS; FDNd em % MS. Saída em Mcal/d. Equivalência com Cap. 3: GasE_DM = (0.294*DMI − 0.347*FA_DM + 0.0409*dNDF_DM)/DMI (Mcal/kg IMS).
- Valores entre parênteses = EP dos coeficientes (±). n, R² e RMSE **não informados** no livro.
- Verificação de plausibilidade (minha, não do livro): IMS 22, AG 3.5, FDNd 18 → 6.0 Mcal/d (≈450 g CH4/d).
- Valores de referência do texto: IEB→CH4 = **3.8–7.4% (média 5.6%)** da IEB em vacas dos EUA (Kebreab 2008a) (corrigido pela imagem: OCR leu 7.49 e 5.69) [p.328]; IPCC nível 2: Ym 6.0% (versão anterior; melhor aderência a dados norte-americanos 5.7±0.9) vs 6.5% (versão atualizada) [p.330].

**Eq. 14-1b** [p.330] — Metano, **novilhas** (Moraes et al. 2014; 414 registros de calorimetria indireta). Imagem conferida.
```
Metano (Mcal/d) = -0.038 (0.071) + 0.051 (0.001) * IEB + 0.0091 (0.0014) * FDN
```
IEB em Mcal/d; FDN em % MS.

**Eq. 14-1c** [p.330] — Metano, **vacas leiteiras não lactantes** (Moraes et al. 2014; 591 registros). Imagem conferida.
```
Metano (Mcal/d) = 0.69 (0.048) + 0.053 (0.001) * IEB - 0.045 (0.012) * FB
```
IEB em Mcal/d; "FB" em % MS (⚠ ver riscos: o texto diz "FDN e FB estão em % MS" e FB não é definido; a magnitude (−0.045 Mcal/% ) coincide com o efeito de gordura da dieta descrito na p.329).

**Eq. 14-2** [p.330] — Sólidos voláteis do esterco (Appuhamy 2014, 2018), vacas em lactação. Imagem conferida.
```
Sólidos voláteis (kg/d) = 0.364 (±0.007) * IMS + 0.026 (±0.004) * FDN - 0.078 (±0.008) * PB
```
IMS em kg/d; FDN e PB em % MS.

**Eq. 14-3** [p.331] — Sólidos voláteis **digestíveis** (= SV − lignina; só a MO digestível gera CH4) (Appuhamy 2018), vacas em lactação. Imagem conferida.
```
Sólidos voláteis digestíveis (kg/d) = 0.334 (±0.007) * IMS + 0.029 (±0.006) * HC - 0.058 (±0.008) * PB
```
IMS em kg/d; HC = FDN − FDA, % MS; PB % MS. Recomendação: usar 14-2/14-3 para prever CH4 do manejo de esterco pelo método IPCC (2006); a fórmula IPCC (SV × fator de emissão por sistema de manejo) **não está no livro** [p.330–331].

**Eq. 14-4** [p.332] — N do esterco por **balanço de massa**, vacas em lactação. Imagem conferida.
```
N do esterco (g/d) = (IMS * PBdieta) / 0.625 - (Leite * PBleite) / 0.638 - 5
```
- IMS e Leite em kg/d; PBdieta e PBleite em %. O fator 0.625 (=6.25×0.1) converte kg×% em g de N; 0.638 (=6.38×0.1) é o fator de PB do leite. O "5" (g N/d) é estimativa de crescimento corporal ao longo de três lactações (150 kg em 915 dias).
- N do esterco = N fecal + N urinário (não inclui N do leite). Exemplo de conferência (meu): IMS 22, PB 17%, leite 35 kg a 3.2% → 598.4 − 175.5 − 5 = **417.9 g/d** (consistente com Eq. 14-7: 412.7 para ingestão de N de 598.4 g/d).

**Eq. 14-5 a 14-8** [p.332] — Johnson et al. (2016; avaliaram 45 modelos) — **vacas em lactação**, quando a proteína do leite **não** é conhecida. Imagem conferida.
```
Eq. 14-5  N da urina (g/d)       = 12.0 (±5.80)  + 0.333 (±0.011) * Ingestão de N (g/d)
Eq. 14-6  N fecal (g/d)          = -18.5 (±3.59) + 10.1 (±0.169)  * IMS (kg/d)
Eq. 14-7  N total do esterco (g/d)= 20.3 (±4.72)  + 0.654 (±0.009) * Ingestão de N (g/d)
Eq. 14-8  N do leite (g/d)       = -19.0 (±3.21) + 8.13 (±0.245)  * IMS (kg/d)
```

**Eq. 14-9 a 14-11** [p.332] — **Novilhas e vacas não lactantes**. Imagem conferida.
```
Eq. 14-9   N da urina (g/d)        = 14.3 (±3.18) + 0.51 (±0.12)   * Ingestão de N (g/d)
Eq. 14-10  N fecal (g/d)           = 0.35 (±1.73) + 0.32 (±0.0064) * Ingestão de N (g/d)
Eq. 14-11  N total do esterco (g/d)= 15.1 (±2.50) + 0.83 (±0.018)  * Ingestão de N (g/d)
```
- RMSEP (% da média observada) para as Eq. 14-5 a 14-11, respectivamente: **25, 16, 11, 14, 36, 17 e 13%** (imagem conferida; OCR tinha "14,36") [p.332].
- Verificação de consistência (minha): ingestão de N 600 g/d, IMS 22 → urina 211.8 + fecal 203.7 = 415.5 vs 14-7 = 412.7 g/d; leite 14-8 = 159.9 g/d.
- Contexto: vacas secretam 21–33% do N ingerido no leite (Calsamiglia 2010); Reed (2015): excreção total média no esterco = **69%** da ingestão de N [p.331].

**Eq. 14-12, 14-13, 14-14** [p.336] — **P fecal** (Alvarez-Fuentes et al. 2016; 14-12 de Weiss e Wyatt 2004, 14-13 de Klop et al. 2013, 14-14 modelo novo). Imagem conferida.
```
Eq. 14-12  P fecal (g/d) = -2.3 (±4.2) + 0.63 (±0.046) * ingestão de P (g/d)
Eq. 14-13  P fecal (g/d) = 19.9 (±5.07) + 0.79 (±0.060) * ingestão de P (g/d) - 1.04 (±0.127) * Produção de leite (kg/d)
Eq. 14-14  P fecal (g/d) = 0.73 (±0.03) * ingestão de P (g/d) - 0.37 (±0.08) * Produção de leite (kg/d)
```
- "Qualquer um dos três modelos é recomendado, dependendo da disponibilidade de dados"; os que usam ingestão de P + leite (14-13, 14-14) tiveram desempenho semelhante entre si e ligeiramente melhor que o só-ingestão (14-12) [p.336–337]. Sem RMSE/R² numéricos.
- Verificação de consistência (minha): ingestão de P 88 g/d, leite 35 kg → 14-12: 53.1; 14-13: 53.0; 14-14: 51.3 g/d.
- Não há equação no capítulo para P urinário (texto: <1 g/d, a menos que a dieta exceda a exigência em 20–30%) nem para P total excretado (= ingestão − P do leite − retenção; P do leite no Cap. 7, não lido aqui) [p.335].

**Eq. 14-15a, b, c** [p.337] — **Produção de esterco total** (urina + fezes úmidas), kg/d, **"usadas no software"**. Imagem conferida.
```
Eq. 14-15a  Novilhas em crescimento (Nennich et al. 2005): Esterco (kg/d) = 4.16 * IMS - PC * 0.0246
Eq. 14-15b  Vacas secas (Wilkerson et al. 1997):          Esterco (kg/d) = 0.00711 * PC + 0.324 * PB + 0.259 * FDN + 8.05
Eq. 14-15c  Vacas em lactação (Nennich et al. 2005):      Esterco (kg/d) = 2.63 * IMS + 9.4
```
- IMS em kg/d; PC em kg; PB e FDN em % MS da dieta. Esterco = principalmente água, MS geralmente <15%.
- Fatores que mandam na produção de esterco: IMS, digestibilidade, ingestão de Na e K (impulsionam o fluxo de água), PB. Equações de novilhas e secas derivam de dados limitados. **Não são adequadas para fins regulatórios** [p.337].
- Verificação de plausibilidade (minha): lactante IMS 22 → 67.3 kg/d; novilha IMS 8, PC 400 → 23.4 kg/d.

## 14.5 Parâmetros e tabelas
Nenhuma tabela numerada no Cap. 14. Valores de referência consolidados (todos narrativos, não usados em cálculo):

| Item | Valor | Pág. |
|---|---|---|
| GWP-100: CH4 / N2O vs CO2 | 28 / 265 | 328, 333 |
| Emissões do setor leiteiro dos EUA em 2008 | 134 Tg CO2e = 1.9% do total EUA; CH4 44%, N2O 13%, CO2 41% | 328 |
| CH4 entérico: % da IEB | 3.8–7.4% (média 5.6%) | 328 |
| CH4 produzido no trato inferior / retal | 13% / 2–3% do CH4 total | 328 |
| IMS explica da variação do CH4 | 60–80% | 328 |
| CH4 sob frio prolongado vs termoneutro | 5.2% vs 7.1% da IEB | 329 |
| Efeito da gordura da dieta no CH4 | −0.045 a −0.09 Mcal (−0.19 a −0.38 MJ) por 1% de gordura (Moraes 2014) | 329 |
| Intensidade de CH4 (g/kg leite corrigido p/ energia) por 1% de GB da dieta, por fonte lipídica (Knapp 2014) | lipídeos não degradados no rúmen −0.78±0.20; sementes −0.71±0.20; óleo −1.12±0.20; fontes endógenas −1.01±0.38 | 329 |
| Monensina no CH4 | −12±6 g CH4/d (média de CH4 338 g/d) (Appuhamy 2013) | 329 |
| 3-nitrooxipropanol | −39% de CH4 a 81 mg/kg MS (11 estudos) | 329 |
| Nitrato | até −50% de CH4 | 329 |
| Asparagopsis | até −60% de CH4 com 1% da MO | 329 |
| Potencial combinado de mitigação (manejo atual) / aditivos eficazes | 15–30% / >50% da intensidade de CH4 | 330 |
| Mudanças maiores IMS, CNE, qualidade da forragem | −5 a −15% da fermentação entérica | 329 |
| Eficiência máxima teórica de N (650 kg, 40 kg LCGP) | 43% | 331 |
| Perdas de AA na absorção / remoção hepática | 35% / 45% dos AA absorvidos (Lapierre 2005) | 332 |
| Reciclagem de ureia com ingestão baixa de N | ≈100% da ureia hepática | 332 |
| NH3: origem | ≈90% do N urinário, resto fezes, em 10 d | 333 |
| NH3 por vaca | média 59 g/d (DP 65); a céu aberto 120–150 g/d; freestall 10–100 g/d | 333 |
| NH3 em pasto | 25% do N excretado no esterco; 3–15% do N urinário no campo (4–52% no local da micção) | 333 |
| Queda de 1 mg/dL no NUL → emissão de NH3 do esterco | −7 a −12% | 333 |
| N2O: fração do N do esterco perdida | geralmente <2–3% (até 10%); a céu aberto 19–33 g/d; freestall 5–37 g/d | 333 |
| P excretado no esterco | >55% do P ingerido | 335 |
| Dietas comuns (EUA/Canadá) | 0.45–0.50% de P, acima da exigência; mediana na Califórnia 1.3× NRC 2001 | 336 |
| Amido vs fibra: P excretado | até −15% com carboidratos prontamente disponíveis (Kebreab 2005a) | 336 |
| Excesso mineral mediano em dietas da Califórnia (39 fazendas) vs NRC 2001 | Ca 1.4×; Mg 10.6×; Na 10.5×; Cl 13.6×; K 1.6×; S 1.4×; Cu 1.8×; Fe 24.7×; Mn 42.0×; Se 1.5×; Zn 1.6× | 337 |
| Excreção mineral (% da ingestão) | Ca 68–85; K 86–93; Mg 95–98; Na 45–95; Cl 58–87 | 337 |

## 14.6 Regras de decisão / restrições para o otimizador (Cap. 14)
- **Reduzir PB da dieta** é a estratégia mais eficaz para reduzir N excretado e NH3 (N urinário cresce mais rápido que o fecal com a ingestão de N); reduzir N abaixo da exigência prejudica produção [p.331, 333].
- **Não formular P além da exigência** (a ingestão de P é o principal preditor do P fecal; efeitos menores: FDN ↑ P fecal, PB e leite ↓) [p.336].
- Excreção mineral acompanha a ingestão; evitar excessos de minerais (Cu e Zn acumulam no solo; Mg alto inibe cristalização de fosfato em solos arenosos; S precursor de H2S) [p.337].
- **Compensações entre perdas:** reduzir PB trocando por fibra aumenta CH4 e reduz N2O; trocar proteína por amido reduz CH4; +0.30 g CH4 por g de N urinário reduzido (Dijkstra 2011); restrições de CH4 em programação linear aumentaram as perdas de N (Moraes 2012) [p.335]. Para um otimizador multi-objetivo isso indica que metas simultâneas de N e CH4 são conflitantes.
- Pasto/esterco: ver também p.333 (NH3 25% do N do esterco em pasto).

## 14.7 Lógica e fluxo (Cap. 14)
- Metano (14-1a) depende de IMS (Cap. 2) e de AG e FDNd da dieta (Cap. 3/19); o resultado entra em EM (Eq. 3-9 → 3-11). Para novilhas/secas, 14-1b/c usam IEB, que vem do Cap. 3 (EB da dieta × IMS).
- Excreção de N: o software usa balanço de massa (ingestão de N − N do leite − retenção [crescimento]) — as equações 14-4 a 14-11 são alternativas entrada-saída. Eq. 14-4 usa os valores de PB do leite e leite do usuário.
- Esterco total: 14-15a/b/c (IMS, PC, PB, FDN).
- Eq. 14-2/14-3 → sólidos voláteis → CH4 de esterco por IPCC 2006 (fora do livro).

## 14.8 Limitações, incertezas e mudanças vs. NRC 2001 (Cap. 14)
- Modelos de CH4 gerais "simples" tiveram pior desempenho que os que representam a composição da dieta (Ellis 2010) [p.329]. Efeito do estresse térmico no CH4 não quantificado ("mais pesquisas necessárias") [p.329].
- Fatores de emissão estáticos do IPCC (2006) para N2O dão alta incerteza, inadequados para avaliar mitigação [p.334].
- MUN como proxy de N urinário tem ressalvas (peso, volume urinário, minerais da dieta) [p.333].
- Equações de esterco inadequadas para fins regulatórios; faltam dados para novilhas/secas [p.337].
- RMSEP elevado em 14-5 (25%) e 14-9 (36%) [p.332].
- NRC 2001 não é comparado numericamente neste capítulo; NRC 2001 referenciado apenas para N (estratégias de mitigação) e exigências de P/minerais.

## 14.9 Conceitos e evidências relevantes (Cap. 14)
- Mitigação de CH4 (manipulação de alimentos, modificadores ruminais, aumento de produtividade; diluição da mantença: 1990–2012, leite +36%, vacas −2%, CH4/leite −22%) [p.329–330]. Mitigação de N: PB da dieta, balancear AA protegidos, energia, sincronia; efeito da energia da dieta na eficiência de N (Reed 2014) [p.331–332]. Nitrato (qualidade da água), COV (silagem; maior emissão nas primeiras 12 h após abertura), abordagens integradas (LCA) [p.334–335]. Pastejo rotacionado reduziu carga de P no escoamento em 64% (Haan 2006) [p.336].
- Harter et al. (2002): carga mínima média anual de NO3-N e sal em campos com esterco 280 e 4,300 kg/ha; lixiviação 0.8 m/ano; atender padrões de água exigiria >70% de redução [p.334].

## 14.10 ⚠ Dúvidas/riscos de OCR (Cap. 14)
- ⚠ **Eq. 14-1c: variável "FB"** não definida (texto: "FDN e FB em % MS"). Pelo contexto (efeito de −0.045 Mcal/1% de gordura, p.329, e equação original de Moraes 2014), provavelmente gordura bruta/extrato etéreo — **interpretação, não afirmada pelo livro**.
- ⚠ Eq. 14-15a: "4.16 × IMS − PC × 0.0246" transcrita exatamente conforme impresso (imagem conferida); sinal e termos como no livro (sem verificação na fonte original Nennich 2005).
- ⚠ Eq. 14-4: o "5" tem unidade g N/d; a explicação (150 kg/915 d) é do livro; não verificada.
- OCR corrigidos pela imagem: "3.8 a 7.49% (5.69%)" → "3.8 a 7.4% (5.6%)"; "±" lidos como "+" no OCR de 14-1a, 14-2, 14-3, 14-5 a 14-14; "14,36" → "14, 36".
- Páginas p.329, 330, 331, 332, 333, 335, 336, 337 conferidas na imagem. p.334 (qualidade da água, COV), p.338–342 (referências) só OCR.

---

# CAPÍTULO 15 — Subprodutos (p.343–355)

## 15.1 Papel no simulador
**Não usado diretamente no modelo.** Serve como guia de restrições/avisos para o otimizador (limites de inclusão observados em estudos, contaminantes, variabilidade) e de contexto sobre origem/nomenclatura dos alimentos listados no Cap. 19 (composição química). O livro **deliberadamente não recomenda "taxas ótimas de inclusão"** (justificativa multifatorial) e afirma que o uso seguro deve seguir as recomendações gerais de alimentação do livro [p.343]. Efeitos associativos positivos (ex.: pH ruminal mais alto quando amido é trocado por fibra digestível) não são contabilizados em muitos modelos [p.343].

## 15.2 Tabela compacta: números-chave por subproduto (restrições/avisos) — extração de texto, nenhuma é recomendação formal
Todos os números foram conferidos na imagem das páginas indicadas (p.344, 346, 347, 348, 350, 354, 355) salvo indicação.

| Subproduto (categoria do livro) | Número/aviso-chave | Pág. |
|---|---|---|
| **Fibra pouco digestível** — resíduo de milho (estrutura) | 21% espigas, 54% talos, 22% folhas, 13% palha da espiga; espiga substituindo parte da silagem de alfafa manteve leite; substituindo milho reduziu leite (menos ED); álcali (NaOH, NH3, Ca(OH)2, KOH, CaO) melhora digestibilidade | 344 |
| Casca de caroço de algodão | 8% da MS reduziu ruminação e aumentou ingestão; exigir mais energia (milho) para manter leite; bezerros jovens sensíveis a gossipol | 344 |
| Lixo de descaroçador de algodão | baixa qualidade, rico em lignina e cinzas (solo), risco histórico de dissulfoton; substituindo cubos de alfafa reduziu leite | 344 |
| Casca de aveia | muito lignificada; tratamento com H2O2 alcalino melhora, mas não adotado (cáustico) | 344 |
| Casca/pele de amendoim | risco de aflatoxina (exigir análise); DMS ruminal da casca 25% → 40% com NH3/NaOH; pele rica em taninos | 344–345 |
| Resíduo de abacaxi | baixa MS, perecível; fresco ou ensilado | 345 |
| Casca de arroz | pobre em proteína, rica em fibra e cinzas, digestibilidade ruim, raramente usada | 345 |
| Bagaço de cana | ≈80% FDN, baixa digestibilidade (sílica, lignina); tratamento químico melhora | 345 |
| Bagaço de tomate | ≈5% pectina; semente separada, rica em gordura e proteína, pode substituir caroço de algodão integral sem afetar leite | 345 |
| **Energia digestível** (classe) | amido reduzido de 27 para 18% com polpa de beterraba + resíduo de cervejaria sem afetar fluxo de proteína microbiana | 345 |
| Casca de amêndoa | mantém leite como substituto parcial de forragem em 1 de 2 estudos; armazenar seco (mofo, lixiviação de açúcares); composição varia com variedade e detritos | 345–346 |
| Polpa de beterraba | substituindo grão úmido de milho **até 24% da MS** manteve leite e eficiência de N microbiano; fibra de fermentação rápida; melaço adicionado dilui FDN; micotoxinas baixas em 20% das silagens (França), sem risco | 346 |
| Polpa cítrica | pobre em proteína; seca é rica em **Ca** e pobre em **P** (CaO/Ca(OH)2 na desidratação); mantém leite quando substitui milho/amido; citrinina em polpa mofada; hipersensibilidade tipo IV letal em poucas vacas; fresca não armazenar por muito tempo | 346 |
| Glicerol bruto | substitui energia mantendo ou aumentando leite; contém água, cinzas, minerais, AG livres e metanol (**sem % de inclusão no texto**) | 346 |
| Resíduo de frutas e hortaliças | composição muito variável; amostrar/analisar; perecível, pode ser ensilado | 346–347 |
| Resíduo de batata | MS baixa, ensilável; amido ≈25% amilose/75% amilopectina, menos fermentável que grãos; glicoalcaloides em batata verde/brotada; **asfixia** com batata inteira ou picada grosseira | 347 |
| Casca de soja | ≈8% da MS do grão; PB ≈10%; trocar milho (40→1%) por casca de soja manteve leite; **até 30% da MS da dieta** sem efeito negativo em fermentação, digestibilidade e produção; fibra de passagem rápida (digestão in vivo < in vitro) | 347 |
| Farelo remoído de trigo (wheat middlings) | energético (mais amido e fibra), proteína altamente degradável no rúmen, bom em P; partículas pequenas reduzem efetividade da fibra; **micotoxinas até 8× as da farinha** | 347–348 |
| Farelo de trigo | menos usado que o remoído; maior valor que farelo de arroz | 348 |
| **Alimentos proteicos** — produtos de origem animal | 30–50% de cada animal é renderizado; ricos em AA essenciais (Lys). **FDA proíbe materiais de risco bovino na alimentação de todos os animais; nota do tradutor: no Brasil o MAPA proíbe quaisquer produtos de origem animal na alimentação de ruminantes — respeitar a legislação brasileira** (restrição obrigatória no otimizador para o público brasileiro) | 348 (e nota de rodapé) |
| Farinha de sangue | rica em PB, PNDR, Lys; higroscópica: processar com **<12% MS** e armazenar seco; método de secagem afeta disponibilidade de AA | 348 |
| Farinha de peixe | rica em PNDR e Met, mas PNDR varia muito entre fontes; digestibilidade intestinal alta; Na varia; pode reduzir palatabilidade da TMR; menos disponível (pet food, aquicultura) | 348–349 |
| Farinha de penas | 5–7% do PC das aves; hidrolisada; rica em PB e AA sulfurados, pobre em His, Lys e Met; S usado como indicador de hidrólise; combina bem com farinha de sangue | 349 |
| Farinha de carne e ossos suína | rica em PNDR e AA essenciais; menor proteína entre as animais; rica em Ca e P | 349 |
| Farinha de subprodutos de aves | proteína, gordura, P, Ca e AA essenciais; pouca disponibilidade | 349 |
| Soro de leite | rico em umidade, lactose, Na; ↑ micção, diarreia, erosão dentária; soro ácido: menos proteína, mais Ca; permeado: baixo em proteína | 349–350 |
| Farelo de canola | canola = <2% ácido erúcico e <30 µmol glucosinolatos/g de MS livre de óleo (convencional: 25–45% erúcico, 50–100 µmol); goitrogênicos reduzem transferência de iodo ao leite (Cap. 7); taninos 1.5–3.0%; meta-análises: ≥ farelo de soja | 350 |
| Farelo de algodão | ≥36% PB (AAFCO); leite semelhante ao de soja/canola; proteína do leite pode cair (menos Lys; gossipol liga Lys) | 350 |
| Farelo de soja | discutido no Cap. 19 | 350 |
| Farelo de girassol | rico em Cu (risco para ovelhas), pobre em Lys, rico em AA sulfurados; mais proteína degradável que soja/canola; substitui soja sem afetar leite | 350–351 |
| Farelo de cártamo | amargo (glicosídeos fenólicos), proteína resistente à degradação ruminal | 351 |
| **Proteico/energéticos** — DDGS e derivados (moagem a seco) | >30% do milho dos EUA vai para etanol; proteína, gordura e a maioria dos minerais **≈3× o grão**; Na, S e Ca podem ser maiores (adição exógena); **micotoxinas podem aumentar 3× no produto final**; 235 amostras de DDGS: nenhuma acima das recomendações FDA para aflatoxinas/DON; fermentação ≈50–60 h, mosto ≈15% de etanol; vinhaça fina 5–10% sólidos | 351–353 |
| Moagem úmida (glúten, farelo de glúten, farinha de gérmen, licor de maceração) | maceração em solução diluída de SO2 ≈40 h; produtos ricos em proteína zeína (farelo de glúten); solúveis sem gordura alta (gérmen removido) | 354 |
| Resíduo de cervejaria | **9 e 17% da MS** (em lugar de forragem) não afetou leite; PNDR menor que WDG; secagem aumenta PNDR; úmido é instável | 354 |
| Varredura de panificação | alta energia, rica em amido (biscoito: gordura e sacarose); substituto parcial de grãos | 354 |
| Caroço de algodão (upland / Pima) | Pima ≈5.5% da produção EUA, mais gordura, proteína e gossipol; upland inteiro é ótima fibra efetiva e aumenta gordura do leite; **15% da MS** substituindo silagem de milho ou alfafa não afetou leite; testar gossipol e micotoxinas; armazenar seco | 355 |
| Gorduras animais | sebo (título >40 °C), banha/graxa (≤40 °C); suscetíveis a oxidação (antioxidantes) | 355 |
| Farelo de arroz | convencional e desengordurado podem ser fornecidos com sucesso | 355 |

## 15.3 Tabela 15-1 [p.351] — Principais subprodutos da moagem de milho de grão seco (descritiva; imagem conferida)
| Nome | Descrição (resumo fiel) |
|---|---|
| Destilados condensados solúveis | remoção do etanol por destilação da fermentação do grão com levedura, condensando a vinhaça a estado semi-sólido |
| Farelo de milho | quando a usina descasca e degermina o grão **após** a fermentação; não passou pela fermentação |
| Gérmen de milho | mesmo processo; contém grande parte da gordura e da fibra do milho; rico em gordura |
| Grãos de destilaria secos desengordurados com solúveis | extração do óleo com solventes dos DDGS; gordura pode ser tão baixa quanto 3% (matéria natural); "extraído com solventes" não é exigido pela AAFCO (2016) |
| Grãos de destilaria secos com solúveis (DDGS) | remoção do etanol; condensando e secando ≥75% dos sólidos da vinhaça integral |
| Solúveis de destilaria secos | separação da fração mais grosseira do grão da vinhaça integral e secagem |
| Grãos de destilaria secos de alta proteína | permanece após descascar/degerminar e fermentar; solúveis normalmente não adicionados (se adicionados: "destilados de alta proteína com solúveis"); proteína semelhante à do farelo de soja; menos P que DDGS tradicional |
| Grãos de destilaria úmidos modificados com solúveis | parcialmente secos; ≈50–54% de umidade (Mello 2012) |
| Grãos de destilaria secos com baixo teor de gordura com solúveis | solúveis centrifugados antes de serem adicionados aos grãos |
| Grãos de destilaria úmidos | remoção do etanol por destilação da fermentação dos grãos |
| Grãos de destilaria úmidos com solúveis | remoção do etanol; condensando e secando ≥75% dos sólidos da vinhaça integral |

**Figuras 15-1 [p.352] e 15-2 [p.353]:** esquemas de processo (moagem a seco e moagem úmida de milho); sem números de modelo. OCR do texto das figuras é ilegível/incompleto; não transcritas.

## 15.4 Conclusões principais (Cap. 15)
- Subprodutos são fontes econômicas de proteína e energia, convertem alimento não comestível por humanos em alimento humano de alta qualidade; composição varia por fabricante, região, tempo e processo (ex.: aquecimento excessivo na secagem reduz valor) [p.343].
- Categorias usadas: fibra pouco digestível, energia digestível, alimentos proteicos, subprodutos proteico/energéticos, subprodutos com alto teor de gordura [p.343–355].
- Principais riscos: micotoxinas (amendoim, DDGS, trigo, gossipol no algodão), perecibilidade (alta umidade), variabilidade de composição (amostrar/analisar), toxicidade específica (batata, citrus, cobre em girassol), restrições legais (proteína de origem animal).
- Usar a composição do Cap. 19; este capítulo não traz composição.

## 15.5 Limitações (Cap. 15)
- Inclusões citadas vêm de estudos de substituição, não de recomendações; muitos usam taxas altas para ilustrar adaptabilidade da vaca [p.343]. Sem limites numéricos formais.

## 15.6 ⚠ Riscos de OCR (Cap. 15)
- Tabela 15-1: OCR perdeu alinhamento nome↔descrição; reconstruída pela imagem (p.351).
- Figuras 15-1/15-2: só descritas.
- Referências p.355–361: leitura integral do OCR de p.355–360; p.361 apenas início; sem importância para o modelo.
- Todos os números da tabela 15.2 conferidos na imagem exceto os de p.345, 349, 351–353 (OCR) — OCR consistente, baixo risco: 25→40% casca de amendoim, >30% etanol, 3× nutrientes, 5–10% sólidos, 50–60 h, 15% etanol, 40 h SO2, 5–7% penas.

---

# CAPÍTULO 16 — Aditivos (p.362–366)

## 16.1 Papel no simulador
Só um ajuste numérico está no modelo: **monensina** (+2% ED, −5% energia de CH4 ⇒ +2.7% EM ⇒ +2.5% ELL) quando incluída na faixa de ≈200–450 mg/d [p.363]. As equações de IMS **não** incluem fator de monensina (banco de dados inadequado) [p.363]. Todos os demais aditivos são discussão.

## 16.2 Regra numérica do modelo (não é equação numerada)
```
Se monensina na dieta entre ~200 e 450 mg/d (faixa de Duffield 2008b):
  ED_dieta   = ED_dieta * 1.02            (Fairfield et al., 2007)
  Energia de CH4 = Energia de CH4 * 0.95  (-5%; Odongo et al., 2007)
  => aumento aproximado de EM de 2.7%  =>  aumento de 2.5% em ELL
```
- Imagem conferida (p.363). A derivação 2% + (−5% de CH4) → 2.7% EM e 2.5% ELL **não é mostrada** no texto; "ED +2%" parece ser aplicado à ED da dieta antes do cálculo EM; ordem exata de aplicação na cadeia do Cap. 3 **não informada** (⚠).
- Meta-análise (Duffield 2008a,b,c): 36 artigos, >9,600 vacas: monensina **reduziu IMS em 2.3%, aumentou leite em 2.3%**, reduziu % de gordura e % de proteína do leite (aumentou produção de proteína; sem efeito na produção de gordura); eficiência energética (energia do leite + variação corporal/ingestão de energia) **+2.5%** [p.363].

## 16.3 Tabela compacta: efeitos médios e avisos por aditivo
| Aditivo | Número/efeito-chave | Pág. |
|---|---|---|
| Monensina (ionóforo) — aprovada nos EUA para vacas secas e em lactação (rótulo: eficiência alimentar); lasalocida só novilhas/bezerros | IMS −2.3%; leite +2.3%; eficiência energética +2.5%; digestibilidade MS/MO/energia +0 a ≈3%; CH4: −12±6 g/d (Cap. 14, p.329), efeito menor e mais variável em leite que em corte; perfil de AGV geralmente não muda em leite; risco de cetose, mastite e deslocamento de abomaso menores no periparto; BHB e AGNE pós-parto reduzidos; PUN geralmente ↑; amônia ruminal ↓ | 362–363 |
| Monensina e gordura do leite | geralmente reduz % de gordura (heterogêneo); mais provável com dietas ricas em C18:3; efeito exacerbado com ~30% da MS de grãos de destilaria (dieta rica em C18:2, S alto, DCAD baixo); aumenta AG trans incl. CLA trans-10 cis-12 | 363 |
| Ionóforos em novilhas | consumo não reduzido em novilhas leiteiras; GMD/eficiência frequentemente ↑ mas nem sempre significativo; sem efeito ou efeito negativo em bezerros recém-desmamados (~12 semanas) | 363–364 |
| Leveduras e probióticos (S. cerevisiae, DFM bacterianos) | cultura de levedura aumenta leite e gordura (2 meta-análises); IMS ↑ (uma) ou ↑ só no início da lactação (<70 DEL) e ↓ depois (outra); resposta de leite dose-dependente; pH ruminal e AGV ligeiramente ↑; MO digerida no trato total **+1.19%**; M. elsdenii ↑ propionato sem efeito em leite/IMS/pH; propionibactérias ↑ eficiência/leite em 3 de 4 estudos | 364 |
| Inoculantes de silagem | BAL homofermentativa: mais leite (↑IMS) em meta-análise (Oliveira 2017), digestibilidade e eficiência geralmente não afetadas; L. buchneri: sem efeito em IMS (39 fazendas, sem efeito em leite) | 365 |
| Enzimas exógenas | respostas modestas e variáveis: fibrolíticas ↑ digestibilidade MS e fibra, pequenos ↑ de consumo e leite (Arriola 2017); amilases: melhorias modestas em digestibilidade/eficiência/leite; vacas em início de lactação respondem mais; quadrado latino responde menos que ensaios longos | 365 |
| Óleos essenciais e fitonutrientes | in vitro: ↓ CH4 e ↓ MS desaparecida, ↓ amônia e AGV; in vivo respostas inconsistentes, maioria sem efeito em ingestão/leite; efeito de CH4 de óleos essenciais desapareceu após 2 semanas (Klop 2017); 15 d para ↑ leite (Blanch 2016) | 365–366 |

## 16.4 Conclusões principais (Cap. 16)
- Aditivos não são essenciais; só os aprovados nos EUA (2019) e com pesquisa revisada por pares em vacas leiteiras entram [p.362]. Aditivos que são nutrientes (tampões, Cr: Cap. 7; niacina, biotina, β-caroteno: Cap. 8) são tratados nos respectivos capítulos [p.362].
- Monensina é o único com efeito quantitativo no modelo. Para Brasil: o capítulo trata de aprovação nos EUA; ionóforos para vacas em lactação têm legislação própria — o livro não discute regulamentação brasileira.

## 16.5 ⚠ Riscos de OCR (Cap. 16)
- p.363 conferida na imagem (200–450 mg/d; 2%; 5%; 2.7%; 2.5%; 36 artigos; 9,600 vacas; 2.3%; 2.5%). p.362, 364, 365, 366 só OCR (texto corrido; números: 1.19%, 0–3%, 70 DEL, 15 dias, 2 semanas) — ⚠ NÃO-VERIFICADO na imagem, baixo risco.
- A ordem de aplicação do ajuste de monensina (antes/depois do cálculo de EM/ELL) não é explicitada.

---

## Dependências cruzadas com outros blocos
- Eq. 14-1a ≡ numerador da Eq. 3-9 (Cap. 3, bloco ch01-03).
- Atividade em confinamento (0.35 kcal ELL/kg PC/km × distância à sala de ordenha) está no Cap. 3; Cap. 13 acrescenta apenas os termos de pastejo.
- Eq. 2-1 (IMS de lactantes) → Cap. 2.
- P do leite, minerais e exigências de P → Cap. 7; composição dos alimentos → Cap. 19; lista completa de equações do modelo → Cap. 20 (não lido aqui; confrontar a numeração).

COBERTURA: páginas impressas lidas 316–368. Texto integral por OCR de todas as páginas de texto (316–324, 328–337, 343–355, 362–366); referências (324–327, 338–342, 355–361, 366–368) apenas percorridas — p.355–360 e p.366–368 lidas por OCR, p.325, 326, 338–342 e 361 apenas por início/contagem de termos (nenhuma equação/tabela encontrada neles). Imagens conferidas: p.317–321, 328–333, 335–337, 344, 346–348, 350, 351, 354, 355, 363. Só por OCR (texto corrido): p.316, 322–324, 334, 343, 345, 349, 352, 353, 356 em diante (referências), 362, 364–366. Não transcrito: figuras 15-1 e 15-2 (esquemas de processo, OCR ilegível; descritas em uma linha). O que ficou de fora: textos narrativos de COV, qualidade da água e culturas GM foram resumidos, sem equações; bibliografia.

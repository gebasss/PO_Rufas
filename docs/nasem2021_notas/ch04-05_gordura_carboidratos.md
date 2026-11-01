# NASEM 2021 (8a ed., PT-BR) — Notas técnicas: Cap. 4 (Gordura) e Cap. 5 (Carboidratos)

**Páginas IMPRESSAS cobertas:** 45–75 (Cap. 4 = pp. 45–62, texto pp. 45–59 e referências pp. 59–62; Cap. 5 = pp. 63–75, texto pp. 63–73 e referências pp. 73–75).
**Método de verificação:** todas as tabelas (4-1, 4-2, 5-1, 5-2) e as duas equações impressas (p.50 e p.56) foram conferidas contra a imagem (dpi 150–220). Narrativa numérica conferida contra imagem nas pp. 47, 49, 50, 51 (tabela), 52, 56, 64, 65, 66, 67, 69, 70, 71, 72, 73. Páginas 45, 46, 48, 53–55, 57–59, 68 foram lidas só pelo OCR (texto corrido; ver seção 10).

- **Cap. 4 — Gordura — Usado diretamente no modelo? PARCIAL.** Entra no modelo: apenas o coeficiente de digestibilidade total de AGs por categoria de alimento (Tabela 4-1) e o limite máximo de AG na dieta. O restante (biohidrogenação, composição da gordura do leite, reprodução, saúde humana) é discussão, sem equação de simulação.
- **Cap. 5 — Carboidratos — Usado diretamente no modelo? PARCIAL.** Entram como regras/recomendações: Tabela 5-1 (FDNf mínimo, FDN total mínimo, amido máximo) e Tabela 5-2 (sistema FDNfa, consulta tabelada). As **equações de digestibilidade ruminal de amido e FDN NÃO estão impressas neste capítulo**: o texto só cita "equações empíricas ... (White et al., 2016) ... usadas para estimar a produção de proteína microbiana (ver Capítulo 6)" [p.68]. Também **não há equação impressa do sistema FDNfa** (só a Tabela 5-2 e a Figura 5-3) [pp.71–72].

> **Aviso ao implementador:** nos pp. 45–75 NÃO existe nenhuma equação numerada (nem "Eq. 4-x" nem "Eq. 5-x"). As equações abaixo recebem identificadores internos (E4-A, E5-A etc.) criados por este relator para referência; o número do livro é "não informado" em todas.

---

# CAPÍTULO 4 — GORDURA (pp. 45–62)

## 1. Papel no simulador
Define o coeficiente de digestibilidade total de ácidos graxos (AGs) por categoria de fonte de gordura, que permite calcular AG digestível da dieta como soma ponderada dos alimentos (modelo aditivo, sem efeito de IMS ou de concentração de AG) [p.48]. Fornece também o teto de AG na dieta (7 % da MS) e advertências para o otimizador sobre depressão de IMS, fibra e gordura do leite. A conversão de AG digestível em ED/EM acontece no capítulo de energia (fora do intervalo; o texto só diz que o modelo foi feito "consistente com o modelo para energia", p.48).

## 2. Entradas

| Variável | Símbolo/sigla | Unidade | Definição | Faixa/valores típicos | Pág. |
|---|---|---|---|---|---|
| AG total do alimento | [AG]_i | % da MS | Ácidos graxos totais do alimento i (não é gordura bruta/EE). Se desconhecido, pode ser estimado a partir de GB (Daley et al., 2020) — equação **não impressa aqui**, o texto remete ao Cap. 19 | Dieta típica ≈ 3 % MS; forragem vegetativa/pasto pode ser >3–4 % | 46, 45 |
| Categoria da fonte de AG | cat_i | categórica | Uma das 11 linhas da Tabela 4-1 | ver Tab. 4-1 | 49 |
| Composição de AG (para classificar suplementos de TG) | AGPI, AGMI, AGI | % do AG | Critério da Tab. 4-1 para alocar suplementos de triglicerídeo à categoria | ver Tab. 4-1 | 49 |
| Ingestão do alimento i | IMS_i | kg MS/d | Entrada de outro capítulo (formulação) | — | 48 |
| Digestibilidade de AG definida pelo usuário | — | fração | "A digestibilidade de AGs para alimentos individuais pode ser alterada a critério do usuário" | — | 48 |

## 3. Saídas

| Variável | Unidade | Definição | Pág. |
|---|---|---|---|
| AG digestível por alimento | kg/d | coef_cat × AG ingerido | 48–49 |
| Digestibilidade total do trato do AG da dieta | fração | Média ponderada (pelo AG ingerido) das digestibilidades dos alimentos | 48 |
| AG total da dieta | % MS | Para checar o limite de 7 % | 46, 59 |

## 4. Equações
(Nenhuma tem número no livro. Identificadores E4-x são internos.)

**E4-A — Modelo de digestão total de AGs (RECONSTRUÇÃO do relator do texto da p.48; não é equação impressa)**
```
AGint_i (kg/d)  = IMS_i (kg/d) * [AG]_i (% MS) / 100
AGdig_i (kg/d)  = coef_cat(i) * AGint_i              # intercepto = 0 (fixado)
AGdig_dieta     = SOMA_i ( AGdig_i )
Dig_AG_dieta    = AGdig_dieta / SOMA_i ( AGint_i )   # média ponderada dos alimentos
```
- coef_cat: Tabela 4-1 (digestibilidade verdadeira = aparente, pois AG fecal endógeno foi fixado em 0).
- Texto original: "digestibilidade total dos AGs da dieta [é] a média ponderada dos alimentos individuais" [p.48]; "intercepto (e a secreção endógena de AG) foi fixado em 0" [p.48]; "constante para a IMS e concentração de AGs da dieta dentro de uma determinada categoria, mas pode diferir entre categorias" [pp.48–49].
- Origem: meta-regressão de AG aparentemente digerido (kg/d) × AG ingerido por categoria, intercepto fixo em 0, estudo como efeito aleatório, observações ponderadas pelos erros-padrão reportados, **30 estudos publicados, 11 categorias** (Daley et al., 2020) [p.52–53]. IMS e concentração de AG da dieta, incluídas como termos adicionais, foram não significativas (P = 0.65; ver Fig. 4-1) [pp.48–49, 53]. R²/RMSE: não informados.

**E4-B — Digestibilidade intestinal (pós-ruminal) aparente de AG (Boerman et al., 2015a)** [p.50]. Transcrita do texto, conferida na imagem:
```
Dig_intestinal (%) = 82.5 - 0.0088 * FluxoDuodenal_AG (g/d)
```
- Faixa de validade dos dados: fluxo duodenal de AG de 100 a 1800 g/d; digestibilidade estimada cai de 81 para 67 % nessa faixa [p.50] (verificação aritmética do relator: 82.5−0.88 = 81.6; 82.5−15.84 = 66.7, consistente).
- **Não é usada no modelo adotado** (que é de trato total); serve de evidência de que a digestibilidade cai com o fluxo de AG. Unidade de saída: %. n/R²: não informados.

**E4-C — Regressões de fluxo duodenal × consumo de AG (parâmetros, sem equação impressa)** [p.47]
```
Doreau e Ferlay (1994):  FluxoDuodenal_AG (g/kg IMS) = 0.8 * AGconsumo (g/kg IMS) + 9.3
Boerman et al. (2015a):  FluxoDuodenal_AG (g/d)      = 0.84 * AGconsumo (g/d) + 93
```
(Forma de equação reconstruída pelo relator; o livro dá só "coeficiente de inclinação" e "intercepto".) Interpretação do livro: intercepto = síntese ruminal endógena líquida de AG; inclinação 0.8 → taxa verdadeira de desaparecimento ruminal de 20 %; 0.84 → 16 %. Com endógeno fixado em 15 g/kg MO digerida no rúmen (livre de lipídios) e decrescente linearmente com o consumo, a digestibilidade ruminal verdadeira seria < 8 % (Jenkins, 1993) [p.47].
Consequência numérica citada: com 9.3 g/kg IMS e 20 % de desaparecimento, a digestibilidade ruminal aparente é 0 % a 4.6 % de AG na MS, negativa abaixo disso, ~7 % a 7 % de AG [p.47]. (Conferido: Dig_ap = 0.20 − 9.3/AGconsumo(g/kg); zera em 46.5 g/kg = 4.65 %; a 70 g/kg = 6.7 %.)

**E4-D — Digestibilidade intestinal de C16 e C18 (Schmidely et al., 2008)** [p.51]
```
Desaparecimento intestinal de C16 total = 0.73 * FluxoDuodenal_C16          # taxa constante, 73 %
Desaparecimento intestinal de C18 total = 0.85 * FluxoDuodenal_C18 - 0.0017 * FluxoDuodenal_C18^2
```
Unidades do fluxo (provavelmente g/kg IMS, pois o texto cita absorção "por kg IMS" para Glasser 2008b): **não informado** ⚠. Resultado do texto: quando o consumo total de C18 > 3.8 % da MS, a digestibilidade intestinal de C18 cai abaixo da do C16. Não usada no modelo final.

**E4-E — Efeito dos AGs de óleos vegetais sobre a digestibilidade total de FDN (Weld e Armentano, 2017)** [p.47]
Texto: "suplementação de AG através de óleos vegetais a 3 % ... corresponde a uma queda de cerca de 1,3 unidades percentuais de FDN digestível, e essa resposta parece ser linear."
```
Delta_DigFDN_trato_total (pontos percentuais) ≈ -1.3 * (AG_suplementado_via_oleo_vegetal / 3)     # derivação do relator, ~ -0.43 pp por 1 % de AG
```
Não é equação do modelo; é diretriz. Efeito muito maior para AG saturados C12 e C14 (láurico/mirístico); nenhum efeito para outras fontes; C16:0 sem efeito em Weld e Armentano mas estudos posteriores (de Souza e Lock, 2019; Western et al., 2020) mostraram AUMENTO de digestibilidade de FDN com gorduras ricas em C16:0 [pp.47–48]. Digestão ruminal de FDN parece não reduzir com óleos (poucos estudos) [p.47].

**E4-F — Concentração de proteína do leite × gordura da dieta (Wu e Huber, 1994)** [p.56]. Transcrita e conferida na imagem:
```
y = 101.1 - 0.638*x + 0.0141*x^2
```
- y = concentração de proteína do leite em % relativo ao controle: [(tratadas/controle, %) x 100] (texto: "concentração de proteína no leite [(tratadas/controle, %) × 100]").
- x = % de gordura total da dieta (% da MS — o texto diz "% de gordura total da dieta"; base MS implícita ⚠).
- Origem: revisão de 83 comparações (suplementação de gordura vs controle). R²/RMSE: não informados. Faixa de x: não informada.
- Cálculo do relator (não impresso): x=3 → y≈99.3; x=5 → ≈98.3; x=7 → ≈97.3 (a queda de proteína desacelera com mais gordura, como diz o texto).

**E4-G — Relação do ponto de aplicação do Modelo "Lucas" (conceito)**: digestibilidade do suplemento = estimada pela diferença entre digestibilidade aparente de AG da dieta basal e da dieta suplementada [p.48]. Sem fórmula impressa.

## 5. Parâmetros e tabelas

### Tabela 4-1 [p.49] — Coeficientes de digestibilidade total de AGs (verificada na imagem a 220 dpi)
Coeficiente = digestibilidade verdadeira = aparente no trato total (intercepto fixo em 0); "Erro padrão" do coeficiente.

| Categoria da fonte de AG | Coef. dig. trato total | Erro padrão | Composição de AG (% de AG) |
|---|---|---|---|
| Alimentos comuns | 0.73 | 0.026 | — |
| Oleaginosas | 0.73 | 0.041 | — |
| Óleo | 0.70 | 0.033 | AGPI >20 %, AGI >65 % |
| Blend de triglicerídeos | 0.63 | 0.027 | AGPI <20 %, AGI >56 % |
| Triglicerídeo de sebo | 0.68 | 0.029 | AGMI >36 %, AGI <56 % |
| Triglicerídeos enriquecidos com ácidos graxos saturados | 0.61 | 0.037 | AGMI >25 %, AGI <36 % |
| Triglicerídeos altamente saturados | 0.44 | 0.030 | AGMI <20 %, AGI <25 % |
| Sais de cálcio de ácido graxo de palma | 0.76 | 0.027 | AGMI >30 % |
| Ácido graxo saturado enriquecido com ácido graxo não esterificado | 0.69 | 0.022 | AGMI <15 %, AGI <20 % |
| Ácido palmítico, ~85 % | 0.73 | 0.077 | — |
| Ácido palmítico ou esteárico >90 % | 0.31 | 0.046 | AGI <2 % |

Notas da tabela (impressas): (a) coeficiente verdadeiro; intercepto 0 ⇒ verdadeiro = aparente (Daley et al., 2020). (b) "As classificações resultam em categorias únicas entre os suplementos de triglicerídeos reportados neste banco de dados **ao alocar a fonte de gordura à primeira linha correspondente**" (ordem de cima para baixo). AGMI = monoinsaturados; AGPI = poli-insaturados; AGI = insaturados.
- "Alimentos comuns" = padrão para a maioria dos alimentos: 0.73 [p.48].
- A categoria "Ácido palmítico, ~85 %" aparece na imagem com til ("~85%"); o OCR perdeu o símbolo (corrigido pela imagem).
- As faixas de composição só valem para alocar *suplementos de triglicerídeo* deste banco de dados; "não necessariamente essas classificações se estendem além desse banco de dados" [p.53]. Nem todos os suplementos da regressão têm alimento equivalente nas tabelas do livro; estão no modelo para melhorar a estimativa dos demais [p.53].
- Valores como o 0.31 (palmítico/esteárico >90 %) vêm de 3 exemplos (1 palmítico, 2 esteáricos), agrupados "principalmente para excluí-los de outras categorias" e "provavelmente impediriam seu uso como suplementos comerciais" [p.53].

### Tabela 4-2 [p.51] — Efeito da quantidade de suplementação de gordura sobre a digestibilidade de AG no suplemento (verificada na imagem; 2 dígitos do OCR corrigidos)
Cabeçalhos: "Baixo, % MS da dieta": [primeira concentração do suplemento de gordura adicionado; digestibilidade dos AGs no suplemento]. "Alto, % MS da dieta": [concentração total de gordura suplementada no segundo nível; digestibilidade dos AGs no suplemento; digestibilidade dos AGs do segundo incremento de suplementação].

| Suplemento | Baixo: conc. (% MS) | Baixo: dig. AG (%) | Alto: conc. total (% MS) | Alto: dig. AG (%) | Dig. AG do 2º incremento (%) | Referência |
|---|---|---|---|---|---|---|
| Sebo^a | 1.80 | 90.3 | 5.00 | 72.9 | 60.7 | Weisbjerg et al., 1992 |
| Sebo moderadamente hidrogenado | 1.80 | 39.7 | 5.7 | 52.8 | 58.8 | Drackley e Elliott, 1993 |
| Sais de cálcio de palma | 1.60 | 93.0 | 3.40 | 87.9 | 82.8 | Weiss e Wyatt, 2004 |
| Sais de cálcio de palma | 2.70 | 88.0 | 4.80 | **77.5** | **63.4** | Wu et al., 1991 |
| Canola triturada | 2.30 | 74.7 | 4.70 | 69.7 | 65.0 | Murphy et al., 1987 |
| Palma hidrogenada | 1.7 | 38.4 | 3.4 | 36.5 | 34.5 | Weiss e Wyatt, 2004 |
| Blend de gorduras | 2.00 | 80.6 | 3.90 | 70.1 | 75.2 | Wu et al., 1991 |

(corrigido pela imagem: OCR leu "71.5" e "634" na linha de sais de Ca de palma/Wu 1991; a imagem mostra 77.5 e 63.4.) ^a "Este estudo avaliou digestibilidade intestinal (e não no trato total)." Leitura do livro: a digestibilidade do suplemento cai com a inclusão em 5 de 7 comparações [p.50]. **O modelo adotado ignora esse efeito** ⇒ em níveis muito elevados de suplementação a digestibilidade de AG e o teor energético da dieta podem ser SUPERESTIMADOS [p.50].

### Figuras de apoio (somente gráficas)
- **Fig. 4-1 [p.49]** — resíduos do modelo final vs AG total da dieta (eixo x: 2.0 a 9.5 % MS, corrigido pela imagem; o OCR leu "20 25 ... 95"). Efeito da concentração de AG da dieta sobre os resíduos: positivo, não significativo (P = 0.65); intercepto 0.005; inclinação 0.002 (unidades não informadas ⚠). Conclusão: sem queda de digestibilidade de AG com o aumento do AG da dieta.
- **Fig. 4-2 [p.50]** — digestibilidade intestinal aparente (linha cheia; E4-B) vs digestibilidade total aparente (tracejada, curvilínea) em função da concentração de AG da dieta (eixo 1.0–7.0 %; eixo y 65–85 %). Apenas ilustrativa; sem valores tabelados.

### Outros parâmetros numéricos citados no texto (não usados em cálculo)
- Escape ruminal de linoleico 5–30 % (média 20 %); linolênico 0–15 % (média 8 %) [p.47]. Fluxo duodenal de C18:2 médio 2.3 g/kg IMS (0–12.7); linoleico = 5.4–98.4 % do 18:2 (média 65.3 % em dietas basais, 80.3 % com lipídio); C18:3 0–3.5 g/kg IMS (média 0.5) [p.47].
- Desaparecimento ruminal de AGPI 60–90 %; perda de oleico/linoleico/linolênico em gorduras não protegidas 86/82/86 % [p.46].
- AG que saem do rúmen: 85–90 % livres, 10–15 % fosfolipídios microbianos [p.47].
- Digestibilidade intestinal aparente (Boerman 2015a): 65.3–83.8 % para AG de cadeia longa; média 77.1 % (C16:0), 72.8 % (C18:0), 74.5 % (todos); dietas pobres em gordura 76.7 % (C16) e 77.8 % (total) [p.50].
- Western et al. (2020): dieta basal 76.7 % → 67.6 % (suplemento com 33.1 % C16:0, 53.3 % C18:0, 5.2 % C18:1 cis-9) ou 76.3 % (84.3 % C16:0, 4.1 % C18:0, 8.7 % C18:1 cis-9); digestibilidade calculada dos suplementos 55 % e 77 % [p.51].
- Valor de iodo (VI): digestibilidade de AG pode ser baixa com VI < 40; sebo hidrogenado 40→15 % C18:1 (VI 45.0→16.4) reduz a digestibilidade; VI óleo de palma hidrogenado 7 vs AG de palma 74 [pp.51–52].
- Forma física: sebo hidrogenado peletizado 77 % (n=8) vs floculado 69 % (n=5); pellets de TG ou de AG = 77 ou 73 % do controle sem gordura; pellets de 284–325 µm sem efeito, 600 µm aumentam a digestibilidade (suplemento com 85 % palmítico) [p.52].
- AG fecal endógeno alternativo (White et al., 2017): 1.7 ou 2.0 g/kg IMS (não adotado) [p.48].

## 6. Regras de decisão / restrições para o otimizador
1. **Teto de AG da dieta: ≤ 7 % da MS** ("dietas com mais do que 7 % de AGs totais não são recomendadas", NRC 2001) [p.46]; reafirmado no Resumo: "não devem ser alimentadas com dietas contendo mais de 7 % da MS como AGs, e o ponto ótimo econômico pode ser consideravelmente menor" [p.59].
2. **Início de lactação: limitar AG da dieta a < 5 % da MS pode ser prudente** (depressão de IMS observada com gordura nesse período) [p.59]. Recomendação qualitativa (soft).
3. Concentrações mais altas de gordura podem reduzir IMS mesmo com efeito mínimo na fermentação/digestibilidade de fibra; redução de IMS pode anular a vantagem de densidade energética [p.59]. O efeito da fonte de gordura sobre IMS "deve ser considerado" [p.52], mas o livro **não fornece equação** de IMS × gordura neste capítulo.
4. Grãos de cereais e forragens contêm ≈ 3 % de AG; oleaginosas e blends animal/vegetal são suplementos aceitáveis, mas em níveis elevados a escolha da fonte deve evitar depressão de gordura do leite ou de IMS [p.59].
5. Sem suplemento de gordura exógeno, ainda assim a depressão de gordura do leite pode ocorrer; efeito de AGs insaturados ocorre mesmo com AG total < 3 % (adicionar 1.7 % de óleo a base com 1.2 % de AG, efeito linear com a concentração de AG insaturado) [p.55] — sem regra numérica de restrição.
6. Para suplementos de gordura (especialmente saturados) a digestibilidade deve ser medida empiricamente em dois níveis acima do basal [p.52]; usuário pode substituir o coeficiente da Tabela 4-1 [p.48].
7. Ao reduzir amido por fibra + gordura palmítica manteve-se a ingestão de energia com maior produção de energia do leite (útil para reduzir ganho de CC no final de lactação) [p.52]. Gordura com digestibilidade < metade da do carboidrato substituído não eleva muito a ED mas reduz a carga fermentativa ruminal [p.52].
8. Moagem/processamento de oleaginosas: melhora digestibilidade de AG, mas processamento muito fino de sementes ricas em linoleico pode aumentar depressão de gordura do leite [p.52].

## 7. Lógica e fluxo
1. Obter [AG]_i (% MS) e a categoria de cada alimento (biblioteca de alimentos — Cap. 19; fora deste intervalo).
2. AGint_i = IMS_i × [AG]_i; AGdig_i = coef_cat × AGint_i (E4-A).
3. Somar para a dieta; digestibilidade da dieta = AGdig/AGint total.
4. AG digestível alimenta o cálculo de ED/EM (Cap. 3, fora do intervalo; apenas implícito) — não verificável aqui.
5. Verificar teto de 7 % MS (e <5 % no início da lactação, se aplicável).
6. Dependências: nenhuma dependência de IMS ou de concentração de AG dentro do cálculo de digestibilidade (por construção).

## 8. Limitações, incertezas e mudanças vs. NRC 2001
- Modelo "o mais simples possível" e "possivelmente simplifica demasiadamente a biologia" [p.48].
- AG fecal endógeno fixado em 0 é biologicamente incorreto mas adotado por ajuste da regressão (intercepto livre dava valor positivo impossível) [pp.48, 53].
- Não modela queda de digestibilidade do suplemento com o aumento da inclusão (observado em 5 de 7 comparações da Tab. 4-2) ⇒ superestimativa em níveis muito altos [p.50]. Se houver queda generalizada não detectada, os coeficientes dos suplementos estão subestimados; mas, se a queda ocorrer, ela já está incorporada nos coeficientes [p.49].
- Digestibilidade individual de C16 e C18 "é possível e desejável" mas não está no modelo; a biohidrogenação faz a digestibilidade total de C18 insaturado ser superestimada e a do C18:0 subestimada [p.50]. Não existe coeficiente por AG individual.
- Mudança vs NRC 2001: modelo anterior tinha "ajuste inadequado" mesmo reestimando parâmetros e incluindo IMS; White et al. (2017) derivaram modelos superiores (incluindo efeitos de concentração de AG e IMS), mas o comitê escolheu o de Daley et al. (2020) por "base biológica, simplicidade e acurácia geral" [pp.49–50].
- Digestibilidade é por AG (não por gordura bruta); a GB não-AG é menos digerível que AG, então a digestibilidade de GB pode subir com suplemento mesmo que a de AG caia [pp.51–52].
- Prever digestibilidade a partir de composição de AG e estado de esterificação é "arriscado" [p.52].
- Efeitos não modelados (só discussão): biohidrogenação, fluxo duodenal de AG, depressão de gordura do leite, perfil de AG do leite, transferência de C16:0 (eficiência marginal aparente 15–35 %) [p.54], efeitos reprodutivos, saúde humana.

## 9. Conceitos e evidências relevantes (curtos)
- Definição: "gordura" nutricional = componentes predominantemente AG; usar AG total, não EE/GB (diferentes métodos dão valores diferentes) [p.45]. Glicerol de TG e parte dos fosfolipídios/galactolipídios equivalem a carboidrato [p.45].
- AGs principais: C16:0, C18:0, C18:1 cis-9, C18:2 cis-9,12, C18:3 cis-9,12,15 [p.45].
- Biohidrogenação ruminal completa reduz o suprimento pós-ruminal dos AGs essenciais; incompleta gera CLA e trans-18:1; CLA trans-10 cis-12 reduz a secreção de gordura do leite; trans-10 18:1 correlaciona com a queda, causalidade em debate; CLA cis-9 trans-11 não reduz [p.46].
- Condições que favorecem AG bioativos depressores: fermentação rápida de carboidratos, pH ruminal baixo, fonte de AG insaturados; balanço cátion-aniônico também modifica o potencial (ver Cap. 7) [p.54].
- Digestão intestinal exige bile e lipase pancreática (não induzível, pode ser limitante); emulsificação envolve lisolecitina e AG monoinsaturados; oleato é anfifílico importante (CMC 0.55–0.60 mM) [pp.47–48 — OCR].
- Composição da gordura do leite: >400 AGs, ~14 acima de 1 g/100 g; AG de síntese de novo C4–C14 e parte do C16; os 6 AG < C16 ≈ 1/4 do peso dos AG do leite; C16:0 ≈ 1/3 do peso (pode passar de 50 % com suplementação de C16:0); oleico 20–30 %; C18:0 9–14 %; monoenoicos < C18:1 ≈ 3 %; CV da maioria dos AG até 15 % [pp.53–54].
- Resposta por estágio (Chilliard, 1993): início (+4.5 pp de GB) 0.31 kg/d de leite corrigido (ns); pico (+3.6 pp) 0.72 kg/d (significativa); médio-final (+3.4 pp) 0.65 kg/d (ns). Produção média < 35 kg/d; resposta em >40 kg/d não definida [p.55].
- Gordura reduz % de proteína do leite (ver E4-F) mas a produção de proteína em geral não cai (57 de 83 comparações sem alteração ou aumento) [p.56].
- Reprodução: taxa de concepção ao 1º serviço subiu em 11 de 20 estudos (+17 pp na média); efeitos confundidos e "difíceis de interpretar" [p.56]. Mistura de CLA melhorou reprodução até 10 g/d [p.56].
- Gordura do leite e saúde humana, trans-AG (>5 % da gordura do leite pode exceder 0.5 g/porção de 10 g — exigência de rotulagem FDA) e potencial de modificação da gordura do leite: discussão sem uso no simulador [pp.57–59].
- Pastagens e silagem: AG 1.1–4.0 % (silagem de milho), azevém 2.2–4.4 % (1.1–3.2 % linolênico), pastagem >4 % não rara, gramíneas >2.5 % AG insaturado totais [p.55].

## 10. Dúvidas / riscos de OCR (Cap. 4)
- ⚠ Tab. 4-1: OCR escreveu "AGPE>20%" e "AGMI' >36%" (superscritos); imagem confirma AGPI >20 % e AGMI. Valores numéricos idênticos aos do OCR.
- ⚠ Tab. 4-2: duas células corrigidas pela imagem (77.5 e 63.4).
- Pontos de fusão dos AGs (p.46: oleico 7–16 °C, palmítico 63 °C, esteárico 71 °C): CONFIRMADO na imagem pela verificação independente; não é parâmetro do modelo.
- ⚠ Valores de concentração micelar crítica e taxas de saturação (p.48) lidos só do OCR; não usados em cálculo.
- ⚠ E4-D: unidades do fluxo duodenal (0.85 e −0.0017) não informadas; coeficiente quadrático impresso "− 0.0017" (OCR com vírgula decimal "0,85" misturada com ponto; padrão do livro é ponto).
- ⚠ E4-F: x em "% de gordura total da dieta" (base MS não explícita).
- ⚠ p.47 chama 0.84 de "16 % de digestibilidade verdadeira no rúmen" (texto original; consistente com 1 − 0.84).
- ⚠ Fig. 4-1: unidades de intercepto e inclinação (0.005; 0.002) não informadas.
- ⚠ Digestibilidade intestinal "VI de 14e 12 % de C18:1" e "VI de 8e9 % C18:1" (pp.51–52): OCR de espaços ("14 e 12 %"); interpretação VI=14 com 12 % C18:1 e VI=8 com 9 % C18:1.
- ⚠ Tab. 4-1: "Alimentos comuns" não define quais alimentos; usar a biblioteca de alimentos (Cap. 19).

---

# CAPÍTULO 5 — CARBOIDRATOS (pp. 63–75)

## 1. Papel no simulador
Define as frações de carboidratos (FDN, FDNf, FDNnf, CSDN = amido + CSA + FSDN), as faixas de digestão, e fornece **restrições de formulação**: FDNf mínimo, FDN total mínimo e amido máximo (Tabela 5-1) e um sistema opcional de FDN fisicamente ajustada (FDNfa; Tabela 5-2) baseado no Separador de Partículas Penn State (SPPS). A digestibilidade ruminal de amido/FDN é tratada como estimativa por equações empíricas de outro capítulo (Cap. 6; White et al., 2016) — **não impressas aqui**.

## 2. Entradas

| Variável | Símbolo/sigla | Unidade | Definição | Faixa/valores típicos | Pág. |
|---|---|---|---|---|---|
| FDN total da dieta | FDN | % MS | Fibra insolúvel em detergente neutro (Fig. 5-1) | Mínimo 25 (Tab. 5-1) | 63, 70 |
| FDN de forragem | FDNf | % MS | FDN proveniente de forragem; principal característica de formulação (substitui FDN total) | Mín. 15–19; ótimo 17–27 | 69–70 |
| FDN não-forragem | FDNnf | % MS | FDN de fontes de fibra não forragem (no texto, "FFNF" = fonte de fibra não-forragem) | Efetividade ≈ 50 % da FDNf (média); 30–80 % em estudos | 69–70 |
| Amido | — | % MS | Fração CSDN | Dietas de lactação: <20 a >30 | 64 |
| FDA/FDN | razão | adimensional | Para dieta/FDNfa | Média da base 0.63; ≈0.8 leguminosas; ≈0.6 gramíneas; Fig. 5-3 usa 0.50 e 0.75 | 71–73 |
| % da MS da TMR na peneira de 19 mm (SPPS) | — | % MS | Distribuição de partículas | 3, 9, 15 (Tab. 5-2); 6, 12 (Fig. 5-3) | 71–73 |
| % da MS da TMR na peneira de 8 mm (SPPS) | — | % MS | Partículas da TMR na peneira de 8 mm do SPPS (SPPS com apenas duas peneiras, 19 e 8 mm, e o fundo; Tab. 5-2, nota a). Se o valor é "retido na peneira de 8 mm" isoladamente ou acumulado (19 + 8 mm) NÃO é explicitado no texto ⚠ | ver Tab. 5-2 | 71–72 |
| % de forragem da TMR | — | % MS | Entrada para FDNfa | 40, 50, 60 | 72 |
| Alvo de pH ruminal médio | — | pH | Meta do sistema FDNfa | 6.0 ou 6.1 (somente esse intervalo é "confiável") | 71 |
| PB da dieta | — | % MS | Premissa fixa recomendada para uso do FDNfa | 17 | 71 |
| PC | — | kg | Premissa fixa recomendada | 630 | 71 |
| Digestibilidade ruminal do amido por fonte | — | % | Trigo 79, cevada 71, milho 54, etc. (ver seção 5) | <30 a >90 | 65 |

## 3. Saídas

| Variável | Unidade | Definição | Pág. |
|---|---|---|---|
| FDNf mínimo | % MS | Tab. 5-1 | 70 |
| FDN total mínimo | % MS | Tab. 5-1 | 70 |
| Amido máximo | % MS | Tab. 5-1 | 70 |
| % mínimo da MS da TMR retido na peneira de 8 mm | % MS | Tab. 5-2 / Fig. 5-3 (para manter pH médio ≥6.0 ou ≥6.1) | 72–73 |

## 4. Equações / definições
(Não há equação numerada no Cap. 5. Abaixo, as definições transcritas do texto; códigos E5-x são internos.)

**E5-A — Carboidratos não fibrosos (CNF)** [p.64]. Texto: "calculada como 100 % da MS menos a soma de FDN, PB, EE e cinzas; às vezes os resíduos de PB e cinzas na FDN são subtraídos da FDN" (NRC, 2001).
```
CNF (% MS) = 100 - ( FDN + PB + EE + cinzas )          # opcionalmente FDN corrigida: FDN - PB_na_FDN - cinzas_na_FDN
```
**Uso não recomendado** para formulação (soma erros analíticos; sugere pool uniforme de CSDN) [p.64].

**E5-B — Fibra solúvel em detergente neutro (FSDN)** [p.64] (Hall et al., 1999):
```
FSDN = ResiduoInsolubilEtanol80% - FDN - Amido          # ResiduoInsolubilEtanol e FDN expressos livres de cinzas e PB
```
Etanol 80 % (em vez de água) remove algumas frutanas de cadeia curta da FSDN [p.64].

**E5-C — FDN potencialmente digestível** [p.66]:
```
FDNpd = FDN - FDNi            # FDNi = fração indigestível, positivamente relacionada à lignina; ambas em % MS ou % FDN
```
Equação de FDNi: não informada neste capítulo.

**E5-D — FDN fisicamente efetiva (FDNfe), proposta de Mertens (1997)** [p.69]:
```
FDNfe = FDN_dieta * ( proporção da MS da TMR retida em peneira de 1.18 mm )
```
O livro **critica** esta formulação: (i) assume FDN igualmente distribuída entre peneiras; (ii) o valor sobe ao adicionar qualquer fonte de FDN, mesmo de efetividade zero [p.69]. Zebeli et al. (2012) sugerem usar a concentração de FDN das frações acima do corte, mas o dado não era reportado/rotineiro [p.69]. **Não é a abordagem recomendada.**

**E5-E — Relação do livro para FDNf, FDN total e amido (Tab. 5-1) [p.70]**. Texto: "Para cada 1 unidade percentual diminuída em FDN de forragem (em % da MS da dieta) abaixo de 19 %, a concentração recomendada de FDN total foi aumentada em 2 unidades percentuais, e o amido máximo foi diminuído em 2 unidades percentuais." Verificado: reproduz exatamente as linhas da Tab. 5-1.
```
Para FDNf <= 19 (% MS):
  FDN_total_min = 25 + 2 * (19 - FDNf)
  Amido_max     = 30 - 2 * (19 - FDNf)
```
(Forma algébrica = derivação do relator, validada nas 5 linhas da tabela, FDNf = 15 a 19; extrapolação fora de 15–19: não informada.)

**E5-F — Taxas e relações citadas no texto (não são equações do modelo):**
- Digestibilidade ruminal do amido vs total do trato: "cada unidade de aumento na digestibilidade de amido no trato total correspondeu a um aumento de 3.4 unidades percentuais na digestibilidade ruminal do amido" (Ferraretto et al., 2013) [p.66].
- Digestibilidade de FDN no trato total cai 4.4 pontos percentuais quando a IMS sobe de 2.5 para 5.0 % do PC (meta-análise de Souza et al., 2018, Holandesas em lactação) [p.67] (derivação do relator: ≈ −1.76 pp por 1 % de PC; **não impresso**).
- Taxa de degradação in vitro da FDNpd: "≈4 %/h em pH 6.5 para ≈1 %/h em pH 5.7" (Oba e Allen, 2003b; o sinal "~" foi lido como "−" pelo OCR; a imagem mostra "~") [p.66].
- A digestibilidade ruminal da FDN responde por >90 % da digestibilidade da FDN no trato total [p.66].
- Redução de PDR diminui IMS quadraticamente (especialmente abaixo de 9.2 % da MS) [p.66].

**Equações de digestibilidade ruminal de carboidratos (amido, FDN): NÃO impressas neste capítulo.** O texto apenas informa: "Equações empíricas têm sido desenvolvidas para estimar a degradação ruminal de amido e FDN com base na composição da dieta e IMS (White et al., 2016) e são usadas para estimar a produção de proteína microbiana (ver Capítulo 6)" [p.68]. O implementador deve buscá-las no Cap. 6.

## 5. Parâmetros e tabelas

### Tabela 5-1 [p.70] — Teores mínimos de FDNf e FDN total e amido máximo, vacas em lactação (verificada na imagem a 220 dpi; OCR leu "3" no primeiro valor de amido → 30, corrigido pela imagem)
Condições de validade impressas: dieta fornecida como **TMR**, forragem com **tamanho de partículas adequado**, **milho moído seco** é a fonte predominante de amido.

| FDNf mínimo (% MS) | FDN total mínimo (% MS) | Amido máximo (% MS) |
|---|---|---|
| 19 | 25 | 30 |
| 18 | 27 | 28 |
| 17 | 29 | 26 |
| 16 | 31 | 24 |
| 15 | 33 | 22 |

Observações do texto: FDN total mínimo definido em 25 % com base em estudos do NRC (2001); "efetividade média da FDN de FFNF definida em 50 % da efetividade da FDN de forragem"; mínimo de FDNf "possivelmente varia entre 15 e 19 %" e depende de FDN total, amido e talvez outros CSDN; faltam dados sobre efeito de CSA e FSDN [pp.69–70].

### Figura 5-2 [p.70] — Fatores que afetam a concentração ótima de FDNf (esquema)
Faixa "ótima" 17–27 % da MS (17 ← maior ingestão de MS ... 27). Itens e sentido da seta (→ aumentar FDNf ótimo; ← diminuir), conforme imagem:
- Maior ingestão de matéria seca ← (puxa para 17).
- Taxa de remoção ruminal mais rápida da FDNf →; forragens finamente picadas →; dieta com amido alto e baixa FFNF →; alta degradabilidade do amido →.
- Tamponantes suplementares ←.
- Grãos fornecidos separadamente com baixa frequência →; espaço de cocho limitado/slug feeding →; ampla variação diária na composição da dieta →.
Sem valores numéricos além de 17 e 27.

### Tabela 5-2 [p.72] — % mínimo da MS da TMR na peneira de 8 mm (SPPS) para manter pH ruminal médio ≥ 6.0 ou ≥ 6.1 (verificada na imagem a 220 dpi; 25 linhas)
Título impresso: "...para manter o pH ruminal médio ≥ 6.0 ou ≥ 6.1 para vacas em lactação alimentadas com TMR variando em composição" (o OCR leu ">" ). Colunas: composição da TMR (% MS) = Forragem | Amido | FDN | FDNf; depois "% TMR na peneira 19 mm" = 3 | 9 | 15 para cada alvo de pH. Células em branco = ver nota c.

| Forragem | Amido | FDN | FDNf | pH 6.0: 19mm=3 | 9 | 15 | pH 6.1: 19mm=3 | 9 | 15 |
|---|---|---|---|---|---|---|---|---|---|
| 40 | 35 | 25 | 19 | 20 | 13 | 12 | 53 | 43 | 33 |
| 40 | 30 | 28 | 19 | 26 | 17 | 14 | 53 | 42 | 33 |
| 40 | 25 | 30 | 22 | (branco) | (branco) | (branco) | 17 | 10 | 11 |
| 40 | 25 | 30 | 19 | 19 | 12 | 11 | 36 | 26 | 19 |
| 40 | 25 | 30 | 17 | 32 | 23 | 17 | 50 | 40 | 31 |
| 40 | 20 | 33 | 17 | 11 | 10 | 10 | 19 | 12 | 11 |
| 40 | 20 | 33 | 15 | 24 | 15 | 12 | 32 | 22 | 16 |
| 40 | 20 | 33 | 14 | 30 | 21 | 15 | 39 | 29 | 21 |
| 40 | 15 | 35 | 13 | (branco) | (branco) | (branco) | 17 | 10 | 10 |
| 50 | 35 | 25 | 20 | 25 | 17 | 13 | 40 | 30 | 22 |
| 50 | 35 | 25 | 18 | 40 | 31 | 23 | 59 | 48 | 38 |
| 50 | 30 | 28 | 22 | 12 | 10 | 10 | 23 | 14 | 12 |
| 50 | 30 | 28 | 20 | 26 | 17 | 13 | 38 | 28 | 20 |
| 50 | 30 | 28 | 18 | 41 | 31 | 23 | 54 | 44 | 34 |
| 50 | 25 | 30 | 22 | (branco) | (branco) | (branco) | 17 | 10 | 10 |
| 50 | 25 | 30 | 20 | (branco) | (branco) | (branco) | 31 | 22 | 15 |
| 50 | 25 | 30 | 18 | 24 | 15 | 12 | 46 | 36 | 27 |
| 50 | 20 | 33 | 19 | (branco) | (branco) | (branco) | 18 | 10 | 10 |
| 50 | 20 | 33 | 17 | (branco) | (branco) | (branco) | 32 | 22 | 16 |
| 60 | 30 | 28 | 23 | (branco) | (branco) | (branco) | 42 | 32 | 23 |
| 60 | 30 | 28 | 22 | (branco) | (branco) | (branco) | 51 | 41 | 31 |
| 60 | 25 | 30 | 24 | (branco) | (branco) | (branco) | 22 | 13 | 10 |
| 60 | 25 | 30 | 23 | (branco) | (branco) | (branco) | 30 | 20 | 14 |
| 60 | 25 | 30 | 22 | (branco) | (branco) | (branco) | 38 | 28 | 19 |
| 60 | 20 | 33 | 20 | (branco) | (branco) | (branco) | 26 | 17 | 12 |

Notas impressas da Tabela 5-2:
- (a) TMR no SPPS "com apenas duas peneiras e o fundo" (White et al., 2017a,b). As duas metas de pH são exemplos, "e essa abordagem não tem a intenção de ser usada para estimar o pH ruminal".
- (b) FDNf = FDN de forragem. Outras variáveis do modelo mantidas nos valores médios (White 2017a). Razão FDA/FDN média = 0.63 (DP = 0.26) na base geral (usada para esta tabela) e 0.56 (0.07), 0.63 (0.14), 0.63 (0.08) para 40, 50 e 60 % de forragem, respectivamente.
- (c) "Quando uma linha está em branco, pH 6.0 é estimado para ser alcançado em todas as combinações possíveis de porcentagens de tamanho de partículas; ou seja, não há mínimo na peneira de 8 mm para predizer pH ruminal médio de 6.0." (Aplica-se ao pH 6.0, que é onde aparecem as células em branco.)
- Valores 10 aparecem repetidamente como menor número da tabela (observação do relator; o livro não explica se 10 % é um piso do modelo; Fig. 5-3 também mostra um platô próximo de 10 %).
- A linha 40/25/30/22 do pH 6.1 mostra 17, 10, 11 (não monotônica entre 9 e 15 %); a imagem confirma "11" ⚠ (ver seção 10).

**Como o livro manda usar a tabela [p.71]:** "Os resultados de retenção de partículas podem ser interpolados para dietas com características variadas (proporção de forragem, amido, FDN e FDNf)." Em cada valor discreto de 3, 9 e 15 % da MS retida na peneira de 19 mm, a tabela dá o % mínimo na peneira de 8 mm. Texto qualitativo: menos FDNf é necessária para manter o pH à medida que o amido diminui; forragem mais grosseira ⇒ maior % nas peneiras de 19 e 8 mm ⇒ FDNf pode ser reduzida; forragem mais fina ⇒ aumentar FDNf; usar porcentagem mais conservadora (mais alta) na peneira de 19 mm quando a digestibilidade ruminal do amido for maior que a média (processamento extenso) [pp.71–72].
(O livro cita erroneamente "Tabela 5-1" na p.71 ao descrever esse padrão; é a Tabela 5-2. Ver seção 10.)

### Figura 5-3 [p.73] — efeito da razão FDA/FDN no modelo FDNfa (gráfico; pH 6.1)
Quatro quadrantes: colunas = % da TMR na peneira de 19 mm fixada em 6 % da MS (esquerda) ou 12 % da MS (direita); linhas = razão FDA:FDN 0.50 (cima) ou 0.75 (baixo). Eixo y = % mínimo da MS da TMR na peneira de 8 mm; eixo x = FDNf da dieta (10–30 % MS). Curva = modelo agrupado (ensemble); faixa sombreada = mín–máx dos membros do ensemble. Leitura gráfica aproximada do relator (não numérica no livro): o mínimo cai de ~60–80 % em FDNf=10 % até um platô de ~10 % a partir de FDNf ≈ 20–25 %; com FDA/FDN maior (0.75), a curva fica deslocada para exigir mais partículas ≥8 mm quando FDNf <20 % [texto p.71]. Texto: "com a diminuição da FDNf abaixo de 20 %, uma maior porcentagem de partículas na peneira de 8 mm é necessária com o aumento da razão FDA/FDN" [p.71]. ⚠ Os valores lidos do gráfico são apenas indicativos.

### Parâmetros de composição, taxas e digestibilidade (texto, referência para alimentos)
| Item | Valor | Pág. |
|---|---|---|
| Carboidratos na dieta | 60–70 % da dieta | 63 |
| Melaço (cana/beterraba) — açúcares | 50–60 % MS | 64–65 |
| Forragens frescas — açúcares | 2–10 % MS | 65 |
| Polpas vegetais — açúcares | 14–20 % MS | 65 |
| Estaquiose / rafinose (soja) | 2–7 % / 1–2 % MS | 65 |
| Frutanas (gramíneas temperadas) | 0–30 % MS | 65 |
| FSDN em polpa cítrica | até 40 % MS | 64 |
| Taxa fracional ruminal de glicose, sacarose, lactose | > 250 %/h | 65 |
| Frutana de Dactylis glomerata (in vitro) | 62 %/h | 65 |
| FSDN (polpa cítrica, beterraba, alfafa) in vitro | 20–40 %/h | 65 |
| Digestibilidade ruminal do amido de grãos | <30 % a >90 % | 65 |
| Digest. ruminal do amido (Ferraretto et al., 2013) | trigo 79 %; cevada 71 %; milho 54 % | 65 |
| Digest. do amido no trato total | 93–94 % (sem diferença entre trigo, cevada, milho) | 65 |
| Milho ensilado (grão úmido) | 64 % de digest. ruminal do amido | 65 |
| Milho floculado/laminado a vapor | 59 % | 65 |
| Milho moído seco | 54 % | 65 |
| Digest. do amido no trato total (faixa observada na meta-análise) | <84 % a >98 % | 66 |
| DIVA de silagem de grão úmido de milho | +9 pp de outubro a agosto seguinte | 65 |
| Vitreosidade do endosperma do milho | 0 % a >75 % na maturidade completa | 65 |
| Atividade amilolítica ruminal, dieta com 21 % amido vs 32 % | ≈ 68 % | 66 |
| DIV amido 6 h: inóculo de dieta 50:50 conc:feno vs só feno | 32 % vs 7 % | 66 |
| FDN: efetividade física da FDN de FFNF vs FDNf (atividade mastigatória) | 30–80 % | 69 |
| Caroço de algodão: efetividade física vs silagem de alfafa corte longo (9.5 mm) / curto (4.8 mm) | 50 % / 127 % | 69 |
| Limiar de tamanho de partícula de forragem sobre tempo de ruminação | 0.3 cm (tamanho médio do poro da peneira) | 69 |
| FDNfe>8 mm: ponto de quebra para pH, tempo de pH<5.8 e ruminação | 18.5 % | 69 (corrigido na verificação; estava p.70) |
| FDNfe>8 mm acima do qual a IMS diminui | 14.9 % ⇒ faixa sugerida 14.9–18.5 % (maximizar ingestão ↔ pH) | 69 |
| AGVs podem fornecer | até 70 % da energia exigida | 67 |

(Os valores acima conferem com a imagem nas pp. 64–67, 69.)

## 6. Regras de decisão / restrições para o otimizador
1. **Restrições principais (Tab. 5-1)**, para TMR, forragem de tamanho adequado, milho moído seco como amido predominante: para um dado FDNf (15–19 % MS) respeitar FDN total ≥ valor da tabela e amido ≤ valor da tabela [p.70]. Piso absoluto de FDN total: 25 % MS [p.70].
2. **FDNf é a variável principal**, não FDN total ("maior relação positiva com o pH ruminal e maior relação negativa com a IMS") [p.69].
3. FDNnf (FFNF) conta ≈ 50 % da efetividade da FDNf (valor médio adotado) [p.70].
4. **FDNf ótima para maximizar ingestão de energia é maior que o mínimo anti-acidose** e provavelmente varia de 17 a 27 % MS, em função da produção de leite, capacidade de consumo e demais fatores da Fig. 5-2 [pp.70, 69].
5. **Ajustes qualitativos de FDNf** (sem coeficientes): aumentar quando há alta proporção de amido altamente fermentável (silagem de grão úmido, trigo, cevada), grãos fornecidos separadamente, slug feeding, alta variação na composição não corrigida na formulação; reduzir com tamponantes suplementares; TMR permite menos FDNf e mais amido que ingredientes separados [p.70].
6. Reduzir a fermentabilidade da dieta (substituir amido por FFNF ou milho moído seco no lugar de trigo/cevada/silagem de grão úmido) dá margem de formulação a uma dada FDNf [p.70].
7. **Sistema FDNfa (opcional)** — ver seção 7 e 8: consulta de % mínimo na peneira de 8 mm (Tab. 5-2), alvo de pH 6.0 ou 6.1 somente; assumir 17 % PB e PC 630 kg; não usar para dietas ricas em forragem (vacas secas) nem para estimar IMS ou tempo de ruminação nesse caso [p.71].
8. FDNfe (por estimulação de mastigação) deve ser tratada como **faixa ótima**, não como mínimo que pode ser excedido sem consequências (FDNfe excessiva reduz IMS por enchimento ruminal, e a seleção no cocho aumenta com partículas muito longas) [p.69].
9. Análises: forragens devem ser analisadas rotineiramente para MS e FDN; amido em silagens de milho/cereais de inverno; cada lote de FFNF variável (ex.: grãos de destilaria) antes da inclusão [p.72]. Gramíneas causam mais enchimento que leguminosas; analisar FDA para estimar proporção gramínea/leguminosa (FDA/FDN ≈ 0.8 leguminosas, ≈ 0.6 gramíneas) [p.73].
10. CNF **não deve ser usado** para formulação [p.64].
11. Digestibilidade in vitro de FDN de forragens: usar para alocar forragens a grupos, resolver problemas, ou critério de compra; comparar dentro de uma rodada [pp.72–73, 68]. Não substitui a digestibilidade in vivo (viés de +7 pp no trato total; Lopes et al., 2015) [p.68].

## 7. Lógica e fluxo
1. Entradas de formulação: composição por ingrediente (FDN, FDNf, FDNnf, amido; biblioteca Cap. 19) → totais da dieta (% MS).
2. Verificar Tab. 5-1: dado FDNf da dieta (entre 15 e 19 %), checar FDN total ≥ mínimo e amido ≤ máximo; fora de 15–19 % FDNf, extrapolação **não informada**.
3. (Opcional) FDNfa: calcular % MS da TMR retida em 19 e 8 mm (SPPS) da TMR real; para o alvo de pH (6.0 ou 6.1), consultar/interpolar a Tab. 5-2 usando proporção de forragem, amido, FDN, FDNf e % em 19 mm; exigir % na peneira de 8 mm ≥ valor lido. Células em branco para pH 6.0 = sem mínimo.
4. Digestibilidade ruminal de amido e FDN: calculada pelo capítulo de proteína microbiana (Cap. 6), que usa equações empíricas de White et al. (2016) com composição da dieta e IMS — fora deste intervalo.
5. O texto sinaliza efeitos cruzados: ↑amido ⇒ ↓digestibilidade da FDN (ruminal e total); ↑IMS ⇒ ↓digestibilidade da FDN; PDR baixa ⇒ ↓IMS e digestibilidade da FDN; ↑amido ⇒ ↑digestibilidade ruminal do amido [pp.66–67]. Não há coeficientes numéricos impressos aqui (exceto os de E5-F).

## 8. Limitações, incertezas e mudanças vs. NRC 2001
- O sistema FDNfa "é novo e não foi submetido a testes de campo rigorosos" [p.71]; foi desenvolvido para ilustrar como composição química e forma física afetam o pH, e não para estimar o pH ruminal [pp.71–72].
- Resultados do FDNfa "aparentam ser confiáveis apenas entre pH 6.0 e 6.1"; faixa de pH nos estudos: 5.44–6.83; o modelo é sensível a PC e PB (afetam IMS usada para tempo de ruminação) ⇒ premissa 17 % PB e 630 kg [p.71]. Baseado principalmente em vacas alimentadas individualmente (pouca seleção de partículas); não reflete superlotação/slug feeding [p.71]. Não usar em dietas ricas em forragem (vacas secas) [p.71]. Efeito de tamponantes e minerais sobre o pH não está no sistema [p.71].
- O comitê **recomenda FDNf como a opção principal** (NRC 2001 concluíra que a aplicação de fibra efetiva era limitada pela falta de padrão e métodos validados); a recomendação de FDNfa é uma "potencial opção" em combinação com outros fatores [pp.69, 71]. (O texto da p.69 diz "recomenda o uso de FNFf" — erro de tradução; ver seção 10.)
- Dados faltam sobre efeito de CSA e FSDN nas exigências de FDN [p.70]. A efetividade 50 % da FDNnf é uma média; varia entre experimentos e é relativa à forragem usada [pp.69–70].
- O mínimo de 25 % FDN total vem do NRC (2001) e tem ressalvas (forragem de tamanho adequado, milho seco moído, TMR) [p.70].
- Valores de digestibilidade ruminal de FDN e amido de biblioteca de alimentos não capturam variação de cultivo, genética, conservação e processamento [p.67]. Modelos mecanísticos (Molly, CNCPS) são menos acurados por conhecimento incompleto, grande número de entradas e falta de dados de parametrização; equações empíricas foram adotadas em favor da acurácia [p.68].
- Incubações de tempo único (in vitro/in situ) servem para comparação relativa, não para estimar digestibilidade in vivo [pp.67–68].
- A degradabilidade do amido ruminal não segue cinética de primeira ordem (depende da população microbiana) [p.66].
- Limitações do FDNfe tradicional: sem padrão metodológico de peneiramento; SPPS é método comum na fazenda; FDNfe é função do corte e da mistura (vagão vertical reduz partículas); seleção no cocho [p.69].
- O que **não** está no modelo (só discussão): efeitos de AGV específicos, lactato, glicogênio microbiano, taxa fracional de degradação por fonte, efeito de pH sobre taxa de degradação (apenas valores citados), digestão pós-ruminal compensatória.

## 9. Conceitos e evidências relevantes (curtos)
- Classificação (Fig. 5-1, p.64): FDN (hemicelulose, celulose, lignina; subdividida em FDNf e FDNnf; FDA é componente da FDN) e CSDN = amido + CSA (açúcares: monossacarídeos, dissacarídeos; oligossacarídeos; frutanas) + FSDN (substâncias pécticas, betaglucanos).
- Animal digere por enzimas próprias: amido, lactose, glicogênio microbiano e trealose; todo o resto (inclusive sacarose e FDN) depende de microrganismos [p.63].
- FDNfe (por mastigação): mat ruminal retém partículas com FDNpd, aumenta digestibilidade da FDN, tamponamento, motilidade, ruminação; também reduz risco de deslocamento de abomaso e ajuda a manter euglicemia [pp.64, 68].
- A digestibilidade da FDN é negativamente associada à lignina dentro de cada tipo de alimento; lignina não afeta CSDN; LDA aumenta com a maturidade, maior em leguminosas que gramíneas, maior em gramíneas tropicais que temperadas [pp.63–64].
- Gramíneas C3: maior FDN, menor lignina e FDNi, taxa de digestão da FDNpd mais lenta, mas digestibilidade ruminal geralmente maior (mais FDNpd e maior tempo de retenção) [p.66].
- Maior IMS ⇒ menor tempo de retenção ⇒ menor digestibilidade de FDN; forragem fina/peletizada e FFNF reduzem retenção; fibra mais digestível (BMR, gramíneas e alfafa imaturas) ⇒ menor retenção; gramíneas retidas por mais tempo que alfafa [p.67].
- Açúcares substituindo amido geralmente aumentam ou não alteram o pH ruminal (menos ácido por mol de hexose, glicogênio microbiano); açúcares aumentam butirato; pectina produz principalmente acetato; amido em lugar de FDN aumenta propionato sem afetar acetato/butirato; com mais amido e pH menor, aumentam bactérias produtoras e utilizadoras de lactato [pp.65, 67].
- Concentrações ruminais de AGV isoladamente não indicam produção (faltam volume de líquido, passagem e absorção) [p.67].
- FDNfa: o sistema usa variáveis de tamanho de partícula, composição da dieta, carboidratos degradáveis no rúmen como entradas para estimar IMS, tempo de ruminação e pH ruminal; o foco é só manter o pH médio selecionado [p.71]. Nome FDNfa escolhido para evitar confusão com FDNfe [p.71].
- Yoder et al. (2013): variar FDNf intencionalmente não afetou respostas em vacas de início/meio de lactação, mas as dietas tinham média 23.2 % de FDNf e sempre >21 %; perto do mínimo, variação não corrigida tende a causar depressão de gordura do leite e menor digestão da FDN [p.70].

## 10. Dúvidas / riscos de OCR (Cap. 5)
- ⚠ **p.69 "FNFf"**: o texto impresso (imagem conferida) traz "recomenda o uso de FNFf como uma das opções para estimar a adequação da forma física da dieta". Em contexto (seção seguinte trata de FDNf e FDNfa) é provável erro de tradução para FDNfa ou FDNfe. Não resolvido; a recomendação principal é FDNf (p.69–70).
- ⚠ **p.71 cita "Tabela 5-1"** ao descrever "menos FDNf é necessária para manter qualquer pH médio à medida que o amido diminui"; pelo contexto, é a Tabela 5-2 (confirmado pelo conteúdo). Erro do livro.
- ⚠ Tab. 5-1: OCR leu "3" na primeira linha de amido; imagem = 30 (corrigido pela imagem).
- ⚠ Tab. 5-2: OCR tinha dígitos corrompidos ("Bi!", "q", "I4", "IO", "2" etc.) e várias linhas deslocadas; **toda a tabela foi relida da imagem a 220 dpi**. Pendência: linha 40/25/30/22 (pH 6.1: 17, 10, 11) — o 11 parece não monotônico mas é o que a imagem mostra. Conferência humana recomendada nas células em branco (cada linha com pH 6.0 em branco foi lida como branco na imagem).
- ⚠ Tab. 5-2: o título usa "≥" (OCR escreveu ">"); manter ≥.
- ⚠ Fig. 5-3: valores lidos do gráfico são aproximados (sem números no livro).
- ⚠ Sigla "FFNF" = fonte de fibra não-forragem (≈ "FDNnf"); aparece como "FENF", "FENFs", "FFNFs" no OCR em vários pontos; padronizado aqui como FFNF/FDNnf.
- ⚠ OCR "FDNTf/FDNÍ/FDNÍf" = FDNf; "FDNtfe/FDNTfe" = FDNfe.
- ⚠ p.66 "FDA" vs "FDN" na frase sobre PDR e digestibilidade ruminal ("tendeu a diminuir a digestibilidade ruminal da FDA linearmente") — texto impresso diz FDA (imagem conferida); manter.
- ⚠ Digestibilidade ruminal do amido "(Ferraretto et al., 2013)": 79/71/54 % e 93–94 % conferidos na imagem p.65.
- ⚠ Equações de digestibilidade ruminal: **ausentes** (ver aviso); não é erro de OCR.
- ⚠ p.68 (não conferida na imagem): digestibilidade in vitro 48 h r = 0.55 (P=0.01), 21 dietas de 7 experimentos, viés de 7 pp (OCR).

---

COBERTURA: páginas lidas 45–75 (todas, incluindo referências 59–62 e 73–75, estas lidas só para identificar fontes e confirmar ausência de equações). Conferidas contra a imagem: Tabelas 4-1, 4-2, 5-1, 5-2; equações impressas (p.50 intestinal; p.56 proteína do leite); Figuras 4-1, 4-2, 5-1, 5-2, 5-3 (esquemas/gráficos); páginas de texto 47, 52, 64, 65, 66, 67, 69, 70, 71, 73. NÃO conferidas contra a imagem (somente OCR): narrativa das pp. 45, 46, 48, 53, 54, 55, 57, 58, 59, 68. FICOU DE FORA / NÃO EXISTE no intervalo: (1) equações de digestibilidade ruminal de amido e FDN (White et al., 2016), remetidas ao Cap. 6; (2) equação do sistema FDNfa (White et al., 2017a,b), apenas Tab. 5-2 e Fig. 5-3; (3) equação de estimativa de AG a partir de GB (Daley et al., 2020), remetida ao Cap. 19; (4) qualquer numeração de equação "Eq. 4-x/5-x" (o livro não numera equações nestes capítulos).

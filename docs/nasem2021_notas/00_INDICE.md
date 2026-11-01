# NASEM 2021 (8ª ed., tradução PT-BR) — Notas técnicas para o simulador/otimizador

Livro de origem: *Exigências Nutricionais de Bovinos Leiteiros, 8ª edição revisada* (NASEM, 2021), tradução Santafé Agroinstituto. PDF escaneado, 562 páginas.
Objetivo destas notas: servir de especificação para implementar um simulador (ENTRADAS: animal, dieta, ambiente → cálculo → SAÍDAS: ingestão, energia, proteína/aminoácidos, minerais, vitaminas, água, desempenho previsto, excreção) e um otimizador de dietas.

## 1. Como as notas foram feitas
- O PDF não tinha texto. Foi feito OCR em português (Tesseract, 300 dpi) das 562 páginas.
- O livro foi lido INTEIRO por leitores independentes, um por capítulo ou bloco. Equações e tabelas foram conferidas contra a imagem da página. As páginas de referências bibliográficas foram só percorridas.
- Depois, outros agentes que não escreveram as notas fizeram uma auditoria por amostragem, comparando as notas com as imagens (ver §6).
- **Numeração de páginas:** todas as notas usam a página IMPRESSA no livro entre colchetes, `[p.N]`. Página do PDF = impressa + 20.
- **Convenções do livro:** separador decimal é PONTO e de milhar é VÍRGULA. Equações com códigos tipo `Local_Nutriente_Modificador` (ex.: `Dt_DMIn`) estão em inglês, com tradução dos termos. A errata de ago/2022 já está incorporada (caps. 6, 7, 10, 20 e 21).
- **Fonte de verdade do cálculo:** o texto do cap. 20 foi escrito transcrevendo o código R do modelo, e o livro diz que, em caso de divergência, o código R prevalece [p.472]. Recomenda-se conferir a implementação final contra o código R oficial.

## 2. Mapa de arquivos
| Arquivo | Capítulos (pp. impressas) | Conteúdo central | Uso direto no modelo |
|---|---|---|---|
| ch01-03_ingestao_energia.md | 1 Definindo exigências, 2 Ingestão de MS, 3 Energia (4–44) | equações de IMS; ED/EM/EL; mantença, lactação, prenhez, atividade, escore de condição | sim |
| ch04-05_gordura_carboidratos.md | 4 Gordura, 5 Carboidratos (45–75) | digestibilidade de ácidos graxos; recomendações de FDN, FDN de forragem, amido, FDNfa | sim |
| ch06_proteina.md | 6 Proteína (76–115) | proteína microbiana, PDR/PNDR, PM e aminoácidos, eficiências-alvo, Eq. 6-6 | sim |
| ch07_minerais.md | 7 Minerais (116–179) | exigências, coeficientes de absorção, limites | sim |
| ch08-09_vitaminas_agua.md | 8 Vitaminas, 9 Água (180–218) | IAs de vitaminas A, D, E; ingestão de água; qualidade da água | sim / parcial |
| ch10_bezerras.md | 10 Bezerras (219–277) | IMS, energia, proteína, minerais, vitaminas; Tabelas 10-1 a 10-18 | sim |
| ch11-12_crescimento_transicao.md | 11 Crescimento, 12 Vacas secas e transição (278–315) | composição do ganho; metas de peso; IMS de secas; DCAD | sim |
| ch13-16_sistemas_ambiente_subprodutos_aditivos.md | 13–16 (316–368) | pastejo; metano; excreção de N e P; esterco; subprodutos; aditivos | cap. 13 e 14 sim; 15 e 16 não |
| ch17-18_toxicos_analises.md | 17 Tóxicos, 18 Análise dos alimentos (369–392) | alertas de toxinas; análises que alimentam cada entrada | não / referência |
| ch19_composicao_alimentos.md + ch19_dados/*.csv | 19 Composição dos alimentos (393–465) | biblioteca de alimentos: metodologia e tabelas (parcial, ver §5) | sim (dados) |
| ch20A_modelo_p466-484.md | 20 Modelo, parte A (466–484) | dicionário de variáveis; ENTRADAS; Eq. 20-1 a 20-109 (água, IMS, composição, digestão ruminal, proteína microbiana) | **núcleo** |
| ch20B_modelo_p485-503.md | 20 Modelo, parte B (485–503) | Eq. 20-110 a 20-282 (digestão no trato total, PM e AA, AG, energia; proteína e gordura do leite; gestação; crescimento; mantença) | **núcleo** |
| ch20C_modelo_p504-528.md | 20 Modelo, parte C (504–528) | Eq. 20-271 a 20-496 (mantença, balanço, produção permitida, dejetos, água, minerais, vitaminas); avaliação do modelo; variação; aplicação no R | **núcleo** |
| ch21_apendices.md | 21 Tabelas de exigências, Apêndices A–C (529–542) | 3 tabelas de exigências geradas pelo modelo; glossário de siglas (174 linhas) | referência / testes |
| verify_*.md | — | relatórios da auditoria independente | — |

## 3. Arquitetura do modelo (ordem de cálculo, conforme o cap. 20)
1. **Entradas** (animal, alimentos/dieta, ambiente, manejo): ch20A §2b e §2c; 41 entradas listadas; análises de laboratório que as alimentam: ch17-18.
2. **Água e ingestão de MS**, por estado fisiológico (bezerra, novilha, pré-parto, não lactante, lactante) e seleção entre equações: ch20A §4.1–4.8 (base: caps. 2, 9, 10, 12).
3. **Composição e ingestão por alimento e dieta, infusões:** ch20A §4.9–4.10 (usa a biblioteca do cap. 19).
4. **Digestão ruminal** de FDN e amido, PDR/PNDR, proteína microbiana e endógena, fluxo de aminoácidos: ch20A §4.11–4.14 (base: cap. 6).
5. **Digestão no trato total** de carboidratos, proteína, aminoácidos, ácidos graxos e MO; energia bruta e digestível: ch20A §4.15 e ch20B §1–6 (base: caps. 3, 4, 5).
6. **EM e EL** (inclui perda de energia por metano): ch20B §6 e ch20C §4.3 (base: caps. 3, 14).
7. **Utilização de nutrientes:** proteína, gordura, volume e energia do leite; gestação; crescimento e reservas; mantença de energia, proteína e aminoácidos: ch20B §7–14 e ch20C §4.1–4.2 (base: caps. 3, 6, 10, 11, 12).
8. **Balanço e produção permitida** (leite permitido por energia e por PM): ch20C §4.4–4.5.
9. **Dejetos, água e eficiências; minerais; vitaminas:** ch20C §4.6–4.9 (base: caps. 7, 8, 9, 14).
10. **Avaliação, sensibilidade e aplicação no R:** ch20C §5 e §11.

## 4. Pontos de atenção para quem vai implementar (consolidado dos leitores)
Os itens abaixo são problemas do PRÓPRIO LIVRO (erros de impressão, ambiguidades) ou divergências entre capítulos, não erros de transcrição. Cada um está detalhado, com página, na seção ⚠ do arquivo correspondente.

**Equações com erro de impressão ou ambiguidade**
- Eq. 2-1 e 3-3a: parênteses desbalanceados. Eq. 3-17b: "×DayLact" e "t" soltos. Unidades mistas nas Eq. 3-7 e 3-9.
- Eq. 6-4a (faltam parênteses); 6-8b idêntica à 6-8c (a versão correta, confirmada pela Tabela 6-5, não tem o termo de 3-metil-His); 6-13a (falta um "+").
- Eq. 7-4: erro-padrão impresso ±0.73, provavelmente 0.073. Eq. 7-6: unidade e sinal "=" ausentes. Mn de crescimento: texto 0.7, Eq. 7-40 usa 2.0.
- Eq. 10-1: o sinal entre os termos quadráticos não aparece (usou-se "+"). Eq. 10-16: parentização de "Cinzas × 4" ambígua. Zn: denominador 0.25 na Eq. 10-27 e 0.20 na Tabela 10-12.
- Eq. 11-12b (impressão inconsistente; há versão reconstruída e validada contra a Tabela 11-3) e 11-12e (parênteses ambíguos).
- Eq. 14-1c: a variável "FB" não é definida. Exemplo de pastejo do cap. 13 (p.320): o livro imprime 0.91 Mcal e a Eq. 13-2 dá 0.85; implementar a equação, não o exemplo.
- Cap. 20: Eq. 20-1 (parênteses do termo Na/K, possivelmente o ×10 cobre os dois termos); Eq. 20-82 e 20-83 (unidade inconsistente); Eq. 20-200 e 20-210 (erros de impressão); Eq. 20-209 usa 0.077 e a 20-185 usa 0.0773; Eq. 20-241 tem uma linha de critério inalcançável; Eq. 20-246 conta o PC duas vezes; Eq. 20-266 (imagem de baixa resolução; coeficiente 0.56 incerto, o cap. 10 usa 0.55); Eq. 20-388 (expoente embaralhado na impressão); Eq. 20-395 (estrutura da absorção de Mg ambígua); Mn da dieta sólida 0.005 no texto e 0.05 na Eq. 20-467.

**Divergências entre capítulos ou entre texto e tabela**
- Cap. 6 × cap. 20: constantes da proteína microbiana, intercepto 70.6 vs 71.2, estrutura aditiva vs multiplicativa. Prevalece o cap. 20 (que reflete o código R).
- Energia do útero gravídico: fórmula dá 83.9 Mcal, Tabela 20-10 imprime 88.6.
- Tabela 20-16: rótulos de linha deslocados no livro (reconstruídos e validados numericamente). Alguns CCC e RMSE do texto divergem das tabelas.
- Tabelas 10-9 (seis células) e 10-17 (uma célula) têm erros de impressão. Tabela 10-2: limiares de temperatura diferem entre tabela, rodapé e texto.
- Tabela 11-2: pesos Jersey de pré e pós-parto do 1º parto parecem trocados. Tabela 12-1: macrominerais rotulados mg/kg, mas são g/kg. PB das últimas colunas das Tabelas 11-3 e 11-4 não bate com a PM somada.
- Tabela 9-1: o texto diz "sete alternativas" e a tabela lista 11. "DEL" na Eq. 9-2 não é definido.
- Cap. 17, p.374: DON "66 mg/kg" incoerente com o limite de 5 mg/kg (a imagem confirma o impresso; não usar como referência).
- Cap. 21: PC da Jersey adulta 520 kg (Tab. 21-2) e 525 kg (Tab. 21-3); PM de 14.0% na novilha Holandesa de 600 d.

**Lacunas do próprio livro** (não são falhas das notas)
- Não há equação de IMS de vacas secas nos caps. 2 a 3 (está no cap. 12, Eq. 12-1/12-2).
- O sistema FDNfa tem só a Tabela 5-2 e a Figura 5-3, sem equação impressa. As equações de digestibilidade ruminal de amido e FDN são remetidas ao cap. 6.
- A seção "Aplicação do modelo no R" (p.527) não dá funções, parâmetros nem formato de entrada e saída.
- O cap. 17 não dá limite de nitrato em alimento; o cap. 18 não dá faixas aceitáveis de composição.
- Efeitos de aditivos, monensina e Mg com gordura são discutidos, mas NÃO estão no modelo.

## 5. O que NÃO foi capturado ou ficou incompleto
- **Biblioteca de alimentos (cap. 19):** capturadas a metodologia completa, 4 equações, o esquema de colunas e a lista de alimentos. Valores transcritos e verificados: Tabela 19-3 completa (74 de 74); Tabela 19-1 só 88 de 180 alimentos; Tabela 19-2 só 60 de 184. Faltam valores de 92 alimentos da 19-1 e 124 da 19-2. A p.406 impressa é cópia da p.407, então 4 alimentos não são recuperáveis (códigos incluídos). Classe e tipo dos alimentos não estão impressos. O OCR sozinho NÃO serve como fonte final nas tabelas, porque perde a atribuição de linha e coluna. O parecer de viabilidade está no §9 do arquivo do cap. 19: para uma biblioteca completa é preciso digitalizar com conferência visual.
- **Referências bibliográficas** de cada capítulo: só percorridas.
- **Figuras:** descritas quando relevantes (por exemplo 9-1, 20-1, 20-2), não reproduzidas.
- **Narrativa sem equação ou tabela:** algumas páginas foram lidas só pelo OCR, sem conferência na imagem (listadas em cada arquivo, seção ⚠ ou COBERTURA).
- **Apêndice C** (biografias do comitê): só registrado.

## 6. Verificação independente (auditoria por amostragem contra as imagens)
| Bloco | Equações conferidas | Células de tabela / linhas | Erros confirmados nas notas |
|---|---|---|---|
| Cap. 20A + 20B | todas as numeradas dos dois arquivos (≈109 + ≈177) | ≈250 células, 30 tabelas, 41 entradas | 4 erros de texto (nenhum numérico), todos corrigidos |
| Cap. 20C + 21 | as 226 (20-271 a 20-496) | ≈1.375 (tab. 20-11 a 20-21) + ≈880 (tab. 21-1 a 21-3) + 174 do glossário | 2 erros de texto, corrigidos |
| Cap. 7 a 19 | ≈150 fórmulas | ≈1.100 células + 30 alimentos (≈1.500 células) | 0 |
| Cap. 1 a 6 | 77 (todas, não só amostra) | 668 células + 39 afirmações numéricas de texto | 3 erros, corrigidos: um sinal (efeito da gordura do leite nos resíduos da Eq. 6-6 era −0.96, não +0.96, p.91) e duas páginas citadas erradas |

Dúvidas não resolvidas: coeficiente de líquido na Eq. 20-266 (imagem de 106 ppi), expoente da Eq. 20-388, parênteses das Eq. 20-4 e 20-271.
Limites da auditoria: foi por amostragem. Os CSVs parciais do cap. 19 só foram verificados nas linhas amostradas; a p.462 (Mn da Tab. 19-3) não foi aberta.

## 7. Próximos passos sugeridos
1. Conferir a implementação contra o código R oficial do modelo (o livro afirma que ele prevalece).
2. Digitalizar com conferência visual o resto da biblioteca de alimentos (cap. 19), que alimenta as entradas do simulador.
3. Usar as Tabelas 21-1 a 21-3 e os exemplos numéricos das notas como vetores de teste (casos de referência para validar as saídas do simulador).
4. Resolver os itens ⚠ de maior impacto (§4) com o código R ou com o ajuste de um valor de referência.

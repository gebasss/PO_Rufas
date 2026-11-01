# Notas técnicas — NASEM 2021 — Cap. 21 e Apêndices A, B, C

**Páginas impressas cobertas:** 529-542 (pdf 549-562).
- Cap. 21 "Tabelas de Exigências Nutricionais" (pp. 529-532)
- Apêndice A "Declaração da Tarefa" (p. 533)
- Apêndice B "Acrônimos e Abreviações" (pp. 534-538)
- Apêndice C "Biografias dos Membros do Comitê" (pp. 539-541; p. 542 é página em branco)

Usado diretamente no modelo?
- Cap. 21: **parcial** — não é cálculo; é saída-resumo (concentrações-alvo na MS e exigências em g/d para animais-tipo). Serve como (a) conjunto de testes/validação (valores de referência do simulador para os animais-tipo), (b) fonte de limites padrão para o otimizador (faixas de FDN, FDNf, amido, DCAD-S mínimo, S).
- Apêndice A: **não** (escopo oficial do relatório; contexto).
- Apêndice B: **sim, como glossário de variáveis** (siglas PT/EN; padronizar nomes de variáveis do código).
- Apêndice C: **não** (existe; não detalhado).

---

# CAPÍTULO 21 — Tabelas de Exigências Nutricionais [pp. 529-532]

## 1. Papel no simulador
Apresenta três tabelas-resumo (21-1 Holandesa, 21-2 Jersey, 21-3 proteína/aminoácidos Holandesa e Jersey) com as **concentrações de nutrientes na MS** que a dieta deve ter para atender às exigências mínimas de animais-tipo em vários estágios. Não define equações novas: todos os valores foram gerados pelas equações dos capítulos individuais. O texto afirma que são "um guia geral" e que as estimativas mais precisas vêm de software de dieta [p.529]. Para o simulador: usar como **casos de teste de regressão** (rodar o modelo com o animal-tipo e comparar) e como **valores-padrão de restrição** do otimizador.

## 2. Entradas (como as tabelas foram geradas — animal-exemplo, premissas)

| Variável | Símbolo | Unidade | Definição / premissa | Valores nas tabelas | Pág. |
|---|---|---|---|---|---|
| Raça | — | — | Holandesa (21-1, 21-3) e Jersey (21-2, 21-3) | 2 raças | [p.530-532] |
| Idade (bezerras/novilhas) | — | dias | pontos de crescimento | 30, 100, 225, 350, 475, 600 | [p.530-531] |
| Peso corporal bezerras/novilhas | PC | kg | Holandesa: 65, 120, 230, 330, 420, 530; Jersey: 45, 90, 175, 245, 310, 400 | ver tabelas | [p.530-531] |
| Taxa de crescimento | — | kg/d | Holandesa: 0.7, 0.7, 0.9, 0.8, 0.7, 0.9; Jersey: 0.5, 0.6, 0.7, 0.6, 0.7, 0.7 | ver tabelas | [p.530-531] |
| Vacas secas — dias pré-parto | — | d | duas classes: 60-21 d e <21 d pré-parto | 60–21 d; <21 d | [p.530-531] |
| PC vaca seca | PC | kg | Holandesa 740 kg (ambas classes); Jersey 555 kg | 740 / 555 | [p.530-531] |
| Taxa de crescimento vaca seca | — | kg/d | Holandesa 0.1 e 0.1; Jersey 0.6 e 0.06 (⚠ ver item 10) | — | [p.530-531] |
| Paridade e PC vaca em lactação | PC | kg | Holandesa: primíparas 570 kg, adultas 700 kg. Jersey: primíparas 425 kg, adultas 520 kg (Tab. 21-2) / **525 kg** (Tab. 21-3) | ⚠ discrepância Jersey adulta 520 vs 525 | [p.530-532] |
| Dias em lactação | DEL | d | Primíparas: 15 e 150; adultas: 20, 100 e 200 | 15, 150, 20, 100, 200 | [p.530-532] |
| Produção de leite | PL | kg/d | Holandesa: 33, 39, 53, 55, 43; Jersey: 22, 27, 35, 37, 31 | ver tabelas | [p.530-532] |
| Gordura do leite | — | % | Holandesa: 3.9, 3.6, 3.7, 3.5, 3.8; Jersey: 4.9, 4.9, 5.0, 4.8, 4.8 | ver tabelas | [p.530-531] |
| Proteína do leite | — | % | Tab. 21-1: 3.1, 3.0, 2.8, 2.8, 3.3 (1 casa); Tab. 21-3 (2 casas): 3.06, 3.02, 2.76, 2.83, 3.26; Jersey 21-2: 3.9, 3.7, 3.5, 3.5, 3.7; 21-3: 3.90, 3.70, 3.49, 3.46, 3.69 | — | [p.530-532] |
| Ajuste p/ crescimento da vaca | — | kg/d | Nota de rodapé "a": exigências de energia e proteína de vacas secas e em lactação foram ajustadas para crescimento de **0.19 e 0.1 kg/d (Holandesa)** e **0.14 e 0.06 kg/d (Jersey)**, "para primíparas versus vacas adultas" | — | [p.530-531] |
| Variação de reservas de energia | — | kg/d (conforme rodapé; grandeza exata não definida) | Rodapé: "alterações nas reservas de energia" **Holandesa: -0.36, -1.00, 0.20, -1.70, 0.21 e 0.21 kg/d; Jersey: -0.24, -0.75, 0.15, -1.28, 0.16 e 0.16 kg/d**, "para os respectivos grupos, iniciando com vacas secas com menos de 21 dias pré-parto". São 6 valores: interpretação (inferência minha, não escrita pelo livro): vaca seca <21 d, primípara 15 DEL, primípara 150 DEL, adulta 20 DEL, adulta 100 DEL, adulta 200 DEL. O grupo seca 60-21 d não tem valor informado. | — | [p.530-531] |
| Dias de gestação | — | d | "definidos em 10, 60 e 110 para vacas com 100, 150 e 200 DEL" (rodapé; DEL=100→10 d, DEL=150→60 d, DEL=200→110 d; leitura direta da ordem dos números) | 10, 60, 110 | [p.530-531] |

Dieta-exemplo: **não há dieta com ingredientes** nos cap. 21. As tabelas dão concentrações-alvo, não composição. Premissas de dieta explícitas no texto e tabelas:
- A IMS usada como denominador vem das equações de estimativa do Cap. 2 (novilhas e vacas), do Cap. 10 (bezerras) e do Cap. 12 (vacas secas e em transição) [p.529].
- Concentração de nutriente = quantidade exigida do nutriente / IMS estimada [p.529].
- Exigências de energia e proteína para crescimento: Cap. 11 [p.529].
- **PNDR** foi estimada como PB da dieta − PDR; PB da dieta baseada "na relação esperada de proteína metabolizável para PB total da dieta" [p.529] (corrigido na verificação: pág. 529). Não há exigência específica de PNDR [p.529].
- Foram incluídas provisões de mobilização e reposição de reservas corporais para energia e proteína ao longo da lactação [p.529] (corrigido na verificação: pág. 529).
- Padrões empíricos observados nas tabelas (não declarados pelo texto; verificados na imagem): PDR = 10.0 % da MS em todas as classes (exceto bezerras de 30 d, sem valor); em Tab. 21-3 PDR g/d = 100 × IMS (ex.: 20.8 kg × 100 = 2,080 g/d); Ingestão de proteína g/d = PB % × IMS (ex.: 16.2 % × 20.8 = 3,370); PNDR g/d = PB g/d − PDR g/d.

## 3. Saídas (colunas das tabelas)
Tab. 21-1 e 21-2 (unidades na MS): IMS (kg/d), EM (Mcal/kg), ELL (Mcal/kg), PDR (%), PNDR (%), PB (%), PM (%), FDN mín. (% MS), FDN de forragem mín. (% MS), amido máx. (% MS), macrominerais Ca, P, Mg, K, Na, Cl, S (%), DCAD-S mín. (mEq/kg), microminerais Cu, Co, I, Fe, Mn, Se, Zn (mg/kg), vitaminas A, D, E (UI/kg).
Tab. 21-3: proteína do leite (% e g/d), IMS, ingestão de proteína (g/d), PDR (g/d), PNDR (g/d), proteína líquida (g/d), PM (g/d; eficiência 0.69), metas de absorção de 9 aminoácidos essenciais (g/d) e metas de eficiência.

## 5. Parâmetros e tabelas (transcrição integral, conferida contra a imagem rotacionada a 220 dpi)

Convenção: "—" = célula vazia/traço no livro. Ponto decimal; vírgula como milhar. "(sic)" = valor impresso como está.

### TABELA 21-1 — Holandesa [p.530]
Título: "Concentrações Estimadas de Nutrientes (base na MS) Necessárias para Atender às Exigências Nutricionais para Bovinos da Raça Holandesa em Diferentes Estágios de Lactação e de Maturidade". (A tabela está impressa na página girada.)

Parte A — Bezerras/novilhas em crescimento e vacas secas

| Variável | 30 d | 100 d | 225 d | 350 d | 475 d | 600 d | Seca 60–21 d pré-parto | Seca <21 d pré-parto |
|---|---|---|---|---|---|---|---|---|
| PC, kg | 65 | 120 | 230 | 330 | 420 | 530 | 740 | 740 |
| Taxa de crescimento, kg/d | 0.7 | 0.7 | 0.9 | 0.8 | 0.7 | 0.9 | 0.1 | 0.1 |
| IMS, kg/d | 1.4 | 3.9 | 6.6 | 8.5 | 9.8 | 11.0 | 13.9 | 12.3 |
| EM, Mcal/kg | 3.68 | 2.26 | 2.09 | 1.95 | 1.92 | 2.12 | 1.93 | 2.25 |
| ELL, Mcal/kg | — | — | — | — | — | — | 1.28 | 1.49 |
| PDR, % | — | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 |
| PNDR, % | — | 6.6 | 4.4 | 2.6 | 1.7 | 2.7 | 1.9 | 4.3 |
| PB, % | 21.0 | 16.6 | 14.4 | 12.6 | 11.7 | 12.7 | 11.9 | 14.3 |
| PM, % | 16.5 | 9.5 | 8.1 | 6.8 | 6.1 | 14.0 ⚠ | 5.2 | 6.7 |
| FDN, % mín. | — | 25–33 | 25–33 | 25–33 | 25–33 | 25–33 | 25–33 | 25–33 |
| FDN de forragem, % mín. | — | 19–25 | 19–25 | 19–25 | 19–25 | 19–25 | 19–25 | 19–25 |
| Amido máx., % (varia) | — | 15–20 | 15–20 | 15–20 | 15–20 | 15–20 | 15–20 | 15–20 |
| Ca, % | 0.59 | 0.78 | 0.58 | 0.44 | 0.37 | 0.39 | 0.31 | 0.39 |
| P, % | 0.45 | 0.32 | 0.26 | 0.21 | 0.18 | 0.19 | 0.19 | 0.21 |
| Mg, % | 0.15 | 0.14 | 0.12 | 0.12 | 0.12 | 0.10 | 0.13 | 0.14 |
| K, % | 1.00 | 0.51 | 0.52 | 0.54 | 0.56 | 0.60 | 0.62 | 0.69 |
| Na, % | 0.35 | 0.17 | 0.16 | 0.16 | 0.15 | 0.16 | 0.16 | 0.17 |
| Cl, % | 0.28 | 0.14 | 0.14 | 0.13 | 0.13 | 0.13 | 0.13 | 0.14 |
| S, % | — | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 |
| DCAD-S, mEq/kg mín. | — | 39 | 42 | 45 | 50 | 60 | 66 | -100 |
| Cu, mg/kg | 5 | 16 | 16 | 15 | 15 | 17 | 18 | 19 |
| Co, mg/kg | — | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 |
| I, mg/kg | 0.78 | 0.69 | 0.58 | 0.54 | 0.53 | 0.54 | 0.51 | 0.54 |
| Fe, mg/kg | 90 | 61 | 46 | 32 | 24 | 28 | 13 | 15 |
| Mn, mg/kg | 50 | 49 | 44 | 40 | 38 | 43 | 38 | 43 |
| Se, mg/kg | 0.3 | 0.3 | 0.3 | 0.3 | 0.3 | 0.3 | 0.3 | 0.3 |
| Zn, mg/kg | 70 | 47 | 41 | 36 | 34 | 35 | 30 | 32 |
| Vitamina A, UI/kg | 5,218 | 3,390 | 3,829 | 4,265 | 4,698 | 5,288 | 5,850 | 6,630 |
| Vitamina D, UI/kg | 1,518 | 924 | 1,044 | 1,163 | 1,281 | 1,442 | 1,595 | 1,810 |
| Vitamina E, UI/kg | 86 | 49 | 25 | 28 | 31 | 35 | 85 | 181 |

Parte B — Vacas Holandesas em lactação (primíparas 570 kg; adultas 700 kg)

| Variável | Prim. 15 DEL | Prim. 150 DEL | Adulta 20 DEL | Adulta 100 DEL | Adulta 200 DEL |
|---|---|---|---|---|---|
| Leite, kg | 33 | 39 | 53 | 55 | 43 |
| Gordura do leite, % | 3.9 | 3.6 | 3.7 | 3.5 | 3.8 |
| Proteína do leite, % | 3.1 | 3.0 | 2.8 | 2.8 | 3.3 |
| IMS, kg/d | 20.8 | 23.9 | 25.8 | 29.4 | 27.4 |
| EM, Mcal/kg | 2.39 | 2.61 | 2.58 | 2.73 | 2.60 |
| ELL, Mcal/kg | 1.58 | 1.72 | 1.70 | 1.80 | 1.73 |
| PDR, % | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 |
| PNDR, % | 6.2 | 7.0 | 7.5 | 7.4 | 7.5 |
| PB, % | 16.2 | 16.0 | 17.5 | 17.4 | 17.5 |
| PM, % | 9.8 | 9.8 | 10.9 | 10.2 | 10.1 |
| FDN, % mín. | 25–33 | 25–33 | 25–33 | 25–33 | 25–33 |
| FDN de forragem, % mín. | 19–25 | 19–25 | 19–25 | 19–25 | 19–25 |
| Amido máx., % (varia) | 22–30 | 22–30 | 22–30 | 22–30 | 22–30 |
| Ca, % | 0.57 | 0.57 | 0.64 | 0.60 | 0.58 |
| P, % | 0.35 | 0.35 | 0.39 | 0.37 | 0.35 |
| Mg, % | 0.17 | 0.17 | 0.18 | 0.18 | 0.17 |
| K, % | 1.03 | 0.97 | 1.10 | 1.00 | 0.99 |
| Na, % | 0.21 | 0.21 | 0.23 | 0.22 | 0.21 |
| Cl, % | 0.29 | 0.30 | 0.34 | 0.32 | 0.29 |
| S, % | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 |
| DCAD-S, mEq/kg mín. | 148 | 130 | 157 | 135 | 137 |
| Cu, mg/kg | 9 | 8 | 10 | 8 | 10 |
| Co, mg/kg | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 |
| I, mg/kg | 0.46 | 0.42 | 0.47 | 0.42 | 0.41 |
| Fe, mg/kg | 16 | 16 | 21 | 19 | 16 |
| Mn, mg/kg | 28 | 26 | 31 | 28 | 27 |
| Se, mg/kg | 0.3 | 0.3 | 0.3 | 0.3 | 0.3 |
| Zn, mg/kg | 57 | 58 | 66 | 62 | 61 |
| Vitamina A, UI/kg | 3,021 | 2,796 | 3,687 | 3,303 | 3,103 |
| Vitamina D, UI/kg | 1,099 | 954 | 1,085 | 952 | 1,021 |
| Vitamina E, UI/kg | 22 | 19 | 22 | 19 | 20 |

Nota "a" (rodapé): ver seção 2 (ajuste de crescimento 0.19 e 0.1 kg/d; reservas -0.36, -1.00, 0.20, -1.70, 0.21 e 0.21 kg/d; gestação 10, 60, 110 d para 100, 150, 200 DEL).

### TABELA 21-2 — Jersey [p.531]
Título: "Concentrações de Nutrientes Estimadas (base na MS) Necessárias para Atender às Exigências Nutricionais para Bovinos da Raça Jersey em Diferentes Estágios de Lactação e de Maturidade".

Parte A — Bezerras/novilhas em crescimento e vacas secas

| Variável | 30 d | 100 d | 225 d | 350 d | 475 d | 600 d | Seca 60–21 d pré-parto | Seca <21 d pré-parto |
|---|---|---|---|---|---|---|---|---|
| PC, kg | 45 | 90 | 175 | 245 | 310 | 400 | 555 | 555 |
| Taxa de crescimento, kg/d | 0.5 | 0.6 | 0.7 | 0.6 | 0.7 | 0.7 | 0.6 ⚠ | 0.06 |
| IMS, kg/d | 1.0 | 3.0 | 5.1 | 6.5 | 7.4 | 8.3 | 10.4 | 9.4 |
| EM, Mcal/kg | 3.69 | 2.41 | 2.16 | 2.02 | 2.13 | 2.25 | 2.04 | 2.19 |
| ELL, Mcal/kg | — | — | — | — | — | — | 1.36 | 1.44 |
| PDR, % | — | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 |
| PNDR, % | — | 7.8 | 4.4 | 3.1 | 3.1 | 2.9 | 1.8 | 3.7 |
| PB, % | 22.9 | 17.8 | 14.4 | 13.1 | 13.1 | 12.9 | 11.8 | 13.7 |
| PM, % | 18.2 | 10.6 | 8.2 | 7.2 | 6.9 | 6.6 | 5.5 | 6.1 |
| FDN, % mín. | — | 25–33 | 25–33 | 25–33 | 25–33 | 25–33 | 25–33 | 25–33 |
| FDN de forragem, % mín. | — | 19–25 | 19–25 | 19–25 | 19–25 | 19–25 | 19–25 | 19–25 |
| Amido máx., % (varia) | — | 15–20 | 15–20 | 15–20 | 15–20 | 15–20 | 15–20 | 15–20 |
| Ca, % | 0.75 | 0.84 | 0.58 | 0.44 | 0.43 | 0.39 | 0.31 | 0.38 |
| P, % | 0.55 | 0.34 | 0.26 | 0.21 | 0.20 | 0.19 | 0.21 | 0.23 |
| Mg, % | 0.15 | 0.14 | 0.12 | 0.12 | 0.12 | 0.10 | 0.13 | 0.14 |
| K, % | 1.20 | 0.50 | 0.52 | 0.53 | 0.56 | 0.60 | 0.62 | 0.68 |
| Na, % | 0.43 | 0.17 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.17 |
| Cl, % | 0.34 | 0.14 | 0.14 | 0.13 | 0.13 | 0.13 | 0.12 | 0.14 |
| S, % | — | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 |
| DCAD-S, mEq/kg mín. | — | 39 | 40 | 43 | 50 | 60 | 66 | -100 |
| Cu, mg/kg | 6 | 17 | 15 | 15 | 16 | 17 | 18 | 19 |
| Co, mg/kg | — | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 |
| I, mg/kg | 1.08 | 0.77 | 0.64 | 0.61 | 0.60 | 0.61 | 0.58 | 0.62 |
| Fe, mg/kg | 110 | 68 | 46 | 32 | 32 | 29 | 13 | 15 |
| Mn, mg/kg | 60 | 52 | 44 | 39 | 42 | 44 | 38 | 43 |
| Se, mg/kg | 0.3 | 0.3 | 0.3 | 0.3 | 0.3 | 0.3 | 0.3 | 0.3 |
| Zn, mg/kg | 84 | 49 | 41 | 36 | 36 | 35 | 30 | 32 |
| Vitamina A, UI/kg | 6,084 | 3,286 | 3,745 | 4,162 | 4,592 | 5,273 | 5,850 | 6,510 |
| Vitamina D, UI/kg | 1,770 | 896 | 1,021 | 1,135 | 1,252 | 1,438 | 1,595 | 1,774 |
| Vitamina E, UI/kg | 90 | 48 | 25 | 28 | 30 | 35 | 85 | 177 |

Parte B — Vacas Jersey em lactação (primíparas 425 kg; adultas 520 kg)

| Variável | Prim. 15 DEL | Prim. 150 DEL | Adulta 20 DEL | Adulta 100 DEL | Adulta 200 DEL |
|---|---|---|---|---|---|
| Leite, kg | 22 | 27 | 35 | 37 | 31 |
| Gordura do leite, % | 4.9 | 4.9 | 5.0 | 4.8 | 4.8 |
| Proteína do leite, % | 3.9 | 3.7 | 3.5 | 3.5 | 3.7 |
| IMS, kg/d | 16.5 | 19.4 | 20.5 | 23.5 | 21.9 |
| EM, Mcal/kg | 2.41 | 2.72 | 2.67 | 2.80 | 2.68 |
| ELL, Mcal/kg | 1.59 | 1.79 | 1.76 | 1.85 | 1.78 |
| PDR, % | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 |
| PNDR, % | 6.8 | 7.6 | 8.0 | 8.0 | 7.6 |
| PB, % | 16.8 | 17.6 | 18 (sic) | 18 (sic) | 17.6 |
| PM, % | 10.2 | 10.0 | 11.1 | 10.5 | 10.2 |
| FDN, % mín. | 25–33 | 25–33 | 25–33 | 25–33 | 25–33 |
| FDN de forragem, % mín. | 19–25 | 19–25 | 19–25 | 19–25 | 19–25 |
| Amido máx., % (varia) | 22–30 | 22–30 | 22–30 | 22–30 | 22–30 |
| Ca, % | 0.56 | 0.56 | 0.63 | 0.60 | 0.57 |
| P, % | 0.33 | 0.34 | 0.37 | 0.35 | 0.34 |
| Mg, % | 0.16 | 0.16 | 0.17 | 0.17 | 0.16 |
| K, % | 0.96 | 0.89 | 1.01 | 0.92 | 0.93 |
| Na, % | 0.20 | 0.20 | 0.21 | 0.21 | 0.20 |
| Cl, % | 0.27 | 0.27 | 0.31 | 0.29 | 0.27 |
| S, % | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 |
| DCAD-S, mEq/kg mín. | 133 | 114 | 140 | 119 | 124 |
| Cu, mg/kg | 9 | 8 | 9 | 8 | 8 |
| Co, mg/kg | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 |
| I, mg/kg | 0.45 | 0.41 | 0.46 | 0.41 | 0.41 |
| Fe, mg/kg | 13 | 14 | 17 | 16 | 14 |
| Mn, mg/kg | 25 | 23 | 28 | 25 | 25 |
| Se, mg/kg | 0.3 | 0.3 | 0.3 | 0.3 | 0.3 |
| Zn, mg/kg | 53 | 54 | 59 | 56 | 53 |
| Vitamina A, UI/kg | 2,836 | 2,405 | 2,796 | 2,520 | 2,616 |
| Vitamina D, UI/kg | 1,031 | 875 | 1,017 | 884 | 951 |
| Vitamina E, UI/kg | 21 | 17 | 20 | 18 | 19 |

Nota "a" (rodapé): ajuste de crescimento 0.14 e 0.06 kg/d; reservas -0.24, -0.75, 0.15, -1.28, 0.16 e 0.16 kg/d; gestação 10, 60, 110 d para 100, 150, 200 DEL.

### TABELA 21-3 — Exigências estimadas de proteína e aminoácidos, Holandesa e Jersey [p.532]
Título: "Exigências Estimadas de Proteína e Aminoácidos para Vacas Primíparas e Adultas das Raças Holandesa e Jersey em Diferentes Dias em Lactação".
Cabeçalho do grupo Jersey nesta tabela: primíparas (425 kg), adultas (**525 kg**) (⚠ Tab. 21-2 diz 520 kg).

| Variável | Hol. Prim. 15 | Hol. Prim. 150 | Hol. Ad. 20 | Hol. Ad. 100 | Hol. Ad. 200 | Jer. Prim. 15 | Jer. Prim. 150 | Jer. Ad. 20 | Jer. Ad. 100 | Jer. Ad. 200 |
|---|---|---|---|---|---|---|---|---|---|---|
| Paridade (PC, kg) | Prim. (570) | Prim. (570) | Ad. (700) | Ad. (700) | Ad. (700) | Prim. (425) | Prim. (425) | Ad. (525) | Ad. (525) | Ad. (525) |
| Dias em lactação | 15 | 150 | 20 | 100 | 200 | 15 | 150 | 20 | 100 | 200 |
| Leite, kg/d | 33 | 39 | 53 | 55 | 43 | 22 | 27 | 35 | 37 | 31 |
| Proteína do leite, % | 3.06 | 3.02 | 2.76 | 2.83 | 3.26 | 3.90 | 3.70 | 3.49 | 3.46 | 3.69 |
| Proteína do leite, g/d | 1,010 | 1,178 | 1,463 | 1,557 | 1,402 | 858 | 999 | 1,222 | 1,280 | 1,144 |
| IMS, kg/d | 20.8 | 23.9 | 25.8 | 29.4 | 27.4 | 16.5 | 19.4 | 20.5 | 23.5 | 21.9 |
| Ingestão de proteína, g/d | 3,370 | 4,063 | 4,515 | 5,116 | 4,795 | 2,772 | 3,414 | 3,690 | 4,230 | 3,854 |
| PDR, g/d | 2,080 | 2,390 | 2,580 | 2,940 | 2,740 | 1,650 | 1,940 | 2,050 | 2,350 | 2,190 |
| PNDR, g/d | 1,290 | 1,673 | 1,935 | 2,176 | 2,055 | 1,122 | 1,474 | 1,640 | 1,880 | 1,664 |
| Proteína líquida, g/d | 1,462 | 1,667 | 2,005 | 2,141 | 1,968 | 1,207 | 1,382 | 1,644 | 1,749 | 1,586 |
| Proteína metabolizável, g/d (efic. = 0.69) | 2,034 | 2,333 | 2,802 | 2,999 | 2,757 | 1,686 | 1,942 | 2,306 | 2,457 | 2,228 |

Metas de absorção de aminoácidos essenciais (g/d); a coluna "Meta de Eficiência" é a eficiência-alvo de uso do AA absorvido:

| Aminoácido | Meta de eficiência | Hol. Prim. 15 | Hol. Prim. 150 | Hol. Ad. 20 | Hol. Ad. 100 | Hol. Ad. 200 | Jer. Prim. 15 | Jer. Prim. 150 | Jer. Ad. 20 | Jer. Ad. 100 | Jer. Ad. 200 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Histidina | 0.75 | 53 | 61 | 73 | 79 | 72 | 39 | 54 | 50 | 67 | 61 |
| Isoleucina | 0.69 | 108 | 126 | 152 | 164 | 149 | 88 | 113 | 117 | 142 | 127 |
| Leucina | 0.74 | 182 | 211 | 254 | 273 | 249 | 137 | 183 | 179 | 229 | 206 |
| Lisina | 0.70 | 154 | 179 | 216 | 232 | 212 | 120 | 162 | 156 | 202 | 183 |
| Metionina | 0.70 | 49 | 57 | 69 | 74 | 68 | 39 | 52 | 52 | 66 | 59 |
| Fenilalanina | 0.60 | 113 | 131 | 157 | 169 | 154 | 87 | 114 | 115 | 143 | 129 |
| Treonina | 0.60 | 104 | 120 | 143 | 155 | 142 | 80 | 107 | 103 | 133 | 121 |
| Triptofano | 0.63 | 25 | 29 | 35 | 38 | 34 | 19 | 26 | 25 | 32 | 29 |
| Valina | 0.85 | 120 | 139 | 168 | 181 | 165 | 96 | 127 | 127 | 159 | 143 |

(Corrigido pela imagem, onde o OCR errou: Leucina Hol. 150 DEL = 211 (OCR "24"); Fenilalanina Hol. 150 DEL = 131 (OCR "331"); Isoleucina Jersey 150/20 DEL = 113/117 (OCR "n3 n7"); Fenilalanina Jersey 150/20 DEL = 114/115 (OCR "14 ns"); Ingestão de proteína Jersey 15 DEL = 2,772 (OCR "2772."); Hol. IMS 200 DEL = 27.4 (OCR "274"); Tab. 21-2 PB Jersey 18 sem decimal é como impresso.)

## 6. Regras de decisão / restrições para o otimizador (valores padrão do cap. 21)
- **FDN mínimo:** 25–33 % da MS para todas as classes ≥100 d de idade e todas as vacas (secas e em lactação); sem valor para bezerras de 30 d [p.530-531]. O texto não explica o que determina a posição na faixa 25–33 (⚠ ver cap. de carboidratos).
- **FDN de forragem mínimo:** 19–25 % da MS (mesmos grupos) [p.530-531].
- **Amido máximo:** 15–20 % (novilhas e vacas secas) e 22–30 % (vacas em lactação); a coluna chama-se "Amido máx., % (varia)" — o valor varia com outros fatores (não informado aqui) [p.530-531].
- **Enxofre (S):** 0.20 % da MS em todas as classes (exceto bezerras de 30 d, sem valor) [p.530-531].
- **Cobalto (Co):** 0.20 mg/kg; **Selênio (Se):** 0.3 mg/kg em todas as classes (Co sem valor aos 30 d) [p.530-531].
- **DCAD-S mínimo** (mEq/kg): novilhas 39–60 (cresce com a idade); vacas secas 60–21 d: 66; secas <21 d: -100 (ambas as raças); vacas em lactação: Holandesa 130–157, Jersey 114–140 [p.530-531]. O texto do cap. 21 não explica o "-100" (provável dieta aniônica pré-parto; explicação deve estar no cap. de minerais — não verificado aqui). ⚠ Sinal conferido na imagem: impresso "-100" (um traço); OCR leu "=100".
- **PDR:** 10.0 % da MS fixo; **PNDR:** valor residual (PB − PDR); sem exigência de PNDR específica [p.529] (corrigido na verificação).
- Faixas e valores representam concentrações **mínimas** para o animal-tipo com IMS estimada; desvio da IMS exige recálculo [p.529] (corrigido na verificação).
- Premissa-chave do próprio livro: as concentrações reais requeridas dependem de IMS e da composição dos ingredientes (excreção fecal metabólica e disponibilidade variam), portanto as tabelas não substituem o cálculo completo [p.529] (corrigido na verificação).

## 7. Lógica e fluxo
1. Entradas por animal-tipo: raça, PC, idade/DEL/paridade, PL, % gordura e proteína do leite, crescimento, reservas, dias de gestação.
2. IMS estimada pelas equações do Cap. 2 (vacas, novilhas), Cap. 10 (bezerras), Cap. 12 (secas/transição).
3. Exigências por nutriente calculadas nos capítulos próprios do livro (o texto cita explicitamente apenas os Caps. 2, 10, 11 e 12 [p.529]; a atribuição dos demais nutrientes aos capítulos de energia, proteína, minerais e vitaminas é inferência).
4. Concentração = exigência ÷ IMS; PNDR = PB − PDR com PB a partir da razão esperada PM:PB.
5. Tab. 21-3 mostra a decomposição em g/d: ingestão de PB, PDR, PNDR, proteína líquida, PM (eficiência de conversão PL→PM = 0.69) e metas de absorção de AA com eficiência por aminoácido.

## 8. Limitações, incertezas e mudanças vs. NRC 2001
- O livro recomenda software de dieta para estimativas precisas [p.529] (corrigido na verificação).
- Não há exigência de PNDR; PNDR é derivada [p.529] (corrigido na verificação).
- Tabelas cobrem apenas Holandesa e Jersey.
- Mudança vs. NRC 2001: o texto do cap. 21 não discute mudanças (não informado).

## 9. Conceitos e evidências relevantes
- Tab. 21-3 usa eficiência de PM → proteína líquida de 0.69 e metas de eficiência por AA (0.60 a 0.85) [p.532].
- Valores de IMS em 21-1/21-2 para vacas de mesma raça variam com DEL e produção (ex.: Holandesa adulta 100 DEL: 29.4 kg/d, PL 55 kg) [p.530].

## 10. Dúvidas/riscos de OCR
- ⚠ Tab. 21-1, novilha 600 d, PM = 14.0 % (conferido na imagem; fisicamente incoerente com PB 12.7 % e PM Jersey 6.6 % para a mesma idade; provável erro de impressão, p. ex. 4.0). Registrado como impresso.
- ⚠ Tab. 21-2, vaca seca 60–21 d, taxa de crescimento "0.6" (imagem confirma 0.6); nota "a" cita 0.06 kg/d; provável 0.06 (compare Holandesa 0.1/0.1).
- ⚠ Rodapé 21-2: PC Jersey adulta 520 kg (Tab. 21-2) vs 525 kg (Tab. 21-3).
- ⚠ Jersey PB adultas 20 e 100 DEL impressa "18" sem casa decimal.
- ⚠ Mapeamento dos 6 valores de variação de reservas para os grupos é inferência minha.
- Rodapé 21-1: "Dias em Lactação 15 150 20 100 200" estão em ordem primíparas, depois adultas.

---

# APÊNDICE A — Declaração da Tarefa [p.533]

## 1. Papel no simulador
Define o escopo oficial do trabalho do comitê (contexto de requisitos). Não contém dados nem equações.

## 9. Conceitos — escopo oficial (transcrição fiel em tópicos) [p.533]
- Produto: um relatório que **revisa a literatura científica** sobre nutrição de bovinos leiteiros e **atualiza as exigências nutricionais do NRC 2001** (*Nutrient Requirements of Dairy Cattle*).
- Análise abrangente de pesquisas recentes sobre alimentação e nutrição, incluindo as quantidades necessárias de **aminoácidos, lipídios, fibras, carboidratos, minerais, vitaminas e água** para bovinos leiteiros **em aleitamento, em crescimento, em reprodução e em lactação**.
- Avaliar novas informações para melhorar a **acurácia da predição do desempenho a partir dos nutrientes** e da **predição dos nutrientes a partir do desempenho, quando este é conhecido** (isto é: o modelo deve funcionar nos dois sentidos).
- Considerar variáveis que afetam as exigências: **condições ambientais** e **tipo de sistema de produção**.
- Abordar: efeitos de **micotoxinas** e outras toxinas; pesquisas recentes sobre **utilização de energia**; **composição dos alimentos, suplementos minerais e aditivos** usados rotineiramente; **subprodutos da indústria de biocombustíveis**; **acurácia da estimativa de energia de forragens** pela equação de predição do NRC.
- Novas informações sobre: metabolismo e utilização de nutrientes, antioxidantes, **efeitos do processamento de grãos** na taxa de fermentação do amido e local de digestão, **aditivos que alteram o metabolismo ruminal e o pós-absortivo**, moduladores ruminais e metabólicos.
- Revisar estratégias nutricionais que **minimizem perdas de nutrientes no esterco** e **reduzam a produção de gases de efeito estufa**; discussão do efeito da alimentação na **qualidade nutricional e segurança dos produtos lácteos**.
- **Futuras áreas de pesquisa** serão identificadas.
- "Dependendo da extensão das novas informações disponíveis, uma **atualização do modelo computacional atual** para calcular as necessidades nutricionais pode ser desenvolvida. Serão realizados **testes e análises adequadas de qualquer novo modelo** desenvolvido." [p.533]

## 8. Observação para o simulador
O mandato prevê explicitamente um modelo computacional atualizado com testes/validação: o simulador deve prever desempenho a partir de nutrientes e nutrientes a partir de desempenho, incluindo ambiente, sistema de produção e excreção (N, P, GEE).

---

# APÊNDICE B — Acrônimos e Abreviações [pp. 534-538]

## 1. Papel no simulador
É o **glossário de variáveis**: sigla PT (usada na tradução), definição PT, sigla EN (usada na literatura/modelos) e definição EN. Recomenda-se nomear variáveis do código pela sigla EN (compatível com equações e software) e manter a sigla PT na interface.

Transcrição integral, conferida contra as imagens das páginas (140 dpi). Ordem e grafia como no livro. Observações do livro/tradução: algumas siglas PT estão duplicadas com significados diferentes (AGT, NMT, PL) — ver lista de ambiguidades ao final.

Colunas: Sigla PT | Definição PT | Sigla EN | Definição EN

### p.534 (A–B)

| Sigla PT | Definição PT | Sigla EN | Definição EN |
|---|---|---|---|
| AA | Aminoácido | AA | amino acid |
| AAE | Aminoácido essencial | EAA | essential amino acid |
| AANE | Aminoácido não essencial | NEAA | nonessential amino acid |
| ACT | Água corporal total | TBW | total body water |
| ACV | Água no corpo vazio | EBWtr | empty body water |
| Ad | Amido digestível | dSt | digested starch |
| ADH | Hormônio antidiurético | ADH | antidiuretic hormone |
| AEA | Eficiência aparente da absorção de IgG | AEA | apparent efficiency of IgG absorption |
| AFE | Água do fluido extracelular | ECW | extracellular fluid water |
| AFI | Água do fluido intracelular | ICW | intracellular fluid water |
| AG | Ácido graxo | FA | fatty acid |
| AGCL | Ácidos graxos de cadeia longa | LCFA | long-chain fatty acid |
| AGCM | Ácidos graxos de cadeia média | MCFA | medium-chain fatty acid |
| AGd | Ácido graxo digestível | dFA | digested fatty acid |
| AGI | Ácido graxo insaturado | UFA | unsaturated fatty acid |
| AGM | Ácido graxo monoinsaturado | MUFA | monounsaturated fatty acid |
| AGNE | Ácido graxo não esterificado | NEFA | nonesterified fatty acid |
| AGPI | Ácido Graxo Poliinsaturado | PUFA | polyunsaturated fatty acid |
| AGT | Ácidos graxos totais | TFA | total fatty acid |
| AGT | Índice de temperatura e umidade | THI | temperature humidity index |
| AGV | Ácidos graxos voláteis | VFA | volatile fatty acid |
| ALI | Água livre ingerida | FWI | free water intake |
| AMS | Sistema de ordenha robotizada | AMS | automatic milking system |
| AOAC | Association of Official Analytical Chemists | AOAC | Association of Official Analytical Chemists |
| ATC | Ácido tricarboxílico | TCA | tricarboxylic acid |
| BHBA | β-hidroxibutirato | BHBA | β-hydroxybutyric acid |
| BRIX | Unidade de medida da concentração de açúcar em solução aquosa | BRIX | unit of measurement of sugar concentration in an aqueous solution |

### p.535 (C–E)

| Sigla PT | Definição PT | Sigla EN | Definição EN |
|---|---|---|---|
| CA | Coeficiente de absorção | AC | absorption coefficient |
| CCK | Colecistoquinina | CCK | cholecystokinin |
| CCS | Contagem de células somáticas | SCC | somatic cell count |
| CLA | Ácido linoleico conjugado | CLA | conjugated linoleic acid |
| CNF | Carboidrato não fibroso | NFC | nonfiber carbohydrate |
| CoA | Coenzima A | CoA | coenzyme A |
| COV | Composto orgânico volátil | VOC | volatile organic compound |
| CSA | Carboidratos solúveis em água | WSC | water-soluble carbohydrates |
| CSDN | Carboidrato solúvel em detergente neutro | NDSC | neutral detergent soluble carbohydrates |
| CV | Coeficiente de variação | CV | coefficient of variation |
| DA | Deslocamento de abomaso | DA | displaced abomasum |
| DAP | Proteína aparentemente digestível | ADP | apparently digestible protein |
| DCAD | Diferença cátion-aniônica da dieta com Na, K e Cl | DCAD | diet cation–anion difference calculated with Na, K, and Cl |
| DCAD-S | Diferença cátion-aniônica da dieta com Na, K, Cl e S | DCAD-S | dietary cation–anion difference calculated with Na, K, Cl, and S |
| DCJ | Doença de Creutzfeldt–Jakob | CJD | Creutzfeldt–Jakob disease |
| DCJv | Variante da Doença de Creutzfeldt–Jakob | vCJD | variant CJD |
| DDGS | Grãos de destilaria secos com solúveis | DDGS | dried distillers grains with solubles |
| DEInp | IED não proteica | DEInp | nonprotein DEI |
| DEL | Dias em lactação | DIM | days in milk |
| DFDNf | Digestibilidade do FDN de forragem in vitro ou in situ | fNDFD | digestibility of forage NDF measured in vitro or in situ |
| DFM | Probiótico | DFM | direct-fed microbial |
| DGL | Depressão da gordura do leite | MFD | milk fat depression |
| DIVA | Digestibilidade in vitro do amido | IVSD | in vitro starch digestibility |
| DIVFDN | Digestibilidade in vitro do FDN | IVNDFD | in vitro NDF digestibility |
| DIVFDN48 | Digestibilidade in vitro do FDN em 48 horas | IVNDFD48 | IVNDFD after 48-hour incubation |
| DOM-1 | De-epoxi -desoxinivalenol | DOM-1 | de-epoxy DON |
| DON | Desoxinivalenol/ vomitoxina | DON | deoxynivalenol/vomitoxin |
| Dpur | Derivados da purina | PD | purine derivatives |
| EB | Energia bruta | GE | gross energy |
| ECC | Escore de condição corporal | BCS | body condition score |
| ED | Energia digestível | DE | digestible energy |
| EDDI | Di-hidroiodeto de etilenodiamina | EDDI | ethylenediamine dihydriodide |
| EEB | Encefalopatia espongiforme bovina – "Doença da vaca louca" | BSE | bovine spongiform encephalopathy; "mad cow disease" |
| EET | Encefalopatia espongiforme transmissível | TSE | transmissible spongiform encephalopathy |
| Egas | Energia gasosa | GasE | gaseous energy |
| ELl | Energia líquida de lactação (grafado "ELl" no apêndice; ELL no restante do livro/tabelas) | NEL | net energy for lactation |
| ELLeite | Energia líquida do leite | MilkE | milk net energy |

### p.536 (E–I)

| Sigla PT | Definição PT | Sigla EN | Definição EN |
|---|---|---|---|
| ELm | Energia líquida de mantença | NEm | net energy for maintenance |
| EM | Energia Metabolizável | ME | metabolizable energy |
| EME | Exigência média estimada | EAR | estimated average requirement |
| EMg | Energia Metabolizável para ganho de peso | MEg | ME for gain |
| EMm | Energia Metabolizável para mantença | MEm | ME requirement for maintenance |
| EPBNNPs | Equivalente em proteína bruta oriundo de nitrogênio não proteico suplementar | sNPNCPE | supplemental nonprotein nitrogen on a crude protein-equivalent basis |
| ER | Energia retida | RE | retained energy |
| ERO | Espécies reativas ao oxigênio | ROS | reactive oxygen species |
| EU | Energia urinária | UE | urinary energy |
| FAD | Flavina Adenina Dinucleotídeo | FAD | flavin adenine dinucleotide |
| FDA | Fibra em detergente ácido | ADF | acid detergent fiber |
| FDN | Fibra em detergente neutro | NDF | neutral detergent fiber |
| FDNd | Digestibilidade da FDN | dNDF | digested NDF |
| FDNf | FDN de forragem | fNDF | forage NDF |
| FDNfa | FDN fisicamente ajustado | paNDF | physically adjusted NDF |
| FDNfe | FDN fisicamente efetivo | peNDF | physically effective NDF |
| FDNi | FDN indigestível | iNDF | indigestible NDF |
| FDNnf | FDN não oriundo de forragem | nfNDF | nonforage NDF |
| FDNpd | FDN potencialmente digestível | pdNDF | potentially digestible NDF |
| FFNF | Fonte de fibra não forragem (subprodutos fibrosos) | NFFS | nonforage fiber sources |
| FMN | Flavina Mononucleotídeo | FMN | flavin mononucleotide |
| FSDN | Fibra solúvel em detergente neutro | NDSF | neutral detergent soluble fiber |
| GB | Gordura bruta | CF | crude fat |
| GCV | Ganho corporal vazio | EBG | empty body gain |
| GEE | Gás de efeito estufa | GHG | greenhouse gas |
| GM | Geneticamente modificado | GM | genetically modified |
| GMD | Ganho médio diário | ADG | average daily gain |
| GPx/GSHpx | Glutationa peroxidases | GPx/GSHpx | glutathione peroxidases |
| HCl | Ácido clorídrico | HCl | hydrochloric acid |
| HCN | Ácido cianídrico/ Ácido prussico | HCN | prussic acid/hydrocyanic acid |
| HMBi | Éster isopropílico de HMTBA | HMBi | isopropyl ester of HMTBA |
| HMTBA/HMB | Análogo da metionina; DL-2-hidroxi-4-metilthiobutanoato | HMTBA/HMB | DL-2-hydroxy-4-methylthiobutanoate |
| IA | Ingestão adequada | AI | adequate intake |
| IDR | Ingestão diária recomendada | RDA | Recommended Dietary Allowance |
| IEB | Ingestão de energia bruta | GEI | gross energy intake |
| IED | Ingestão de energia digestível | DEI | digestible energy intake |
| IEM | Ingestão de energia metabolizável | MEI | ME intake |

### p.537 (I–P)

| Sigla PT | Definição PT | Sigla EN | Definição EN |
|---|---|---|---|
| Ig | Imunoglobulina | Ig | immunoglobulin |
| IMS | Ingestão de matéria seca | DMI | dry matter intake |
| IMSAS | Ingestão de matéria seca de alimentos sólidos | SFDMI | solid feed DMI |
| IVM | Infravermelho médio | MIR | mid-infrared |
| k_d | Taxa de degradação | k_d | degradation rate |
| k_p | Taxa de passagem | k_p | rate of passage |
| LCGP | Leite corrigido para gordura e proteína | FPCM | fat- and protein-corrected milk |
| LDA | Lignina em detergente ácido | ADL | acid detergent lignin |
| Mn-SOD | Manganês Superóxido dismutase | Mn-SOD | manganese superoxide dismutase |
| MO | Matéria orgânica | OM | organic matter |
| MOR | Matéria orgânica residual | ROM | residual organic matter |
| MORd | Matéria orgânica residual digestível | dROM | digested residual organic matter |
| MORe | MOR endógena | eROM | endogenous ROM |
| MOS | Manano-oligossacarídeos | MOS | maltooligosaccharides, oligosaccharides containing mannose (sic) |
| MS | Matéria seca | DM | dry matter |
| NDT | Nutrientes digestíveis totais | TDN | total digestible nutrients |
| Nmic | Nitrogênio microbiano | MicN | microbial N |
| NMNU | N microbiano derivado do N urinário | MNU | microbial N derived from urinary urea-N |
| NMT | Nível máximo tolerável | MTL | maximum tolerable level |
| NMT | Máximo nível de ingestão tolerável | UL | tolerable upper intake level |
| NNA | Nitrogênio não amoniacal | NAN | nonammonia nitrogen |
| NNANM | Nitrogênio não amoniacal e não microbiano | NANMN | nonammonia-nonmicrobial N |
| NNP | Nitrogênio não proteico | NPN | nonprotein nitrogen |
| NU | Nitrogênio urinário | UN | urinary nitrogen |
| NUL | Nitrogênio ureico do leite | MUN | milk urea N |
| NUP | N-ureico plasmático | BUN | blood urea N |
| OE | Óleo essencial | EO | essential oil |
| OF | Oferta de forragem | PA | pasture availability |
| PB | Proteína bruta | CP | crude protein |
| PBd | Proteína bruta digestível | dCP | digested crude protein |
| PC | Peso corporal | BW | body weight |
| PCA | Proteína carreadora de acila | ACP | acyl carrier protein |
| PCa | Produção de calor | HP | heat production |
| PCM | Peso corporal metabólico | MBW | metabolic body weight |
| PCMat | Peso corporal à maturidade | MatBW | mature body weight |
| PCV | Peso corporal vazio | EBW | empty body weight |

### p.538 (P–W)

| Sigla PT | Definição PT | Sigla EN | Definição EN |
|---|---|---|---|
| PDR | Proteína degradável no rúmen | RDP | rumen-degradable protein |
| PEM | Poliencefalomalácea | PEM | polioencephalomacia (sic) |
| PIDA | Proteína insolúvel em detergente ácido | ADIP | acid detergent insoluble protein |
| PIDN | Proteína insolúvel em detergente neutro | NDIP | neutral detergent insoluble protein |
| PL | Produção de leite média | MY | mean milk yield |
| PL | Proteína líquida | NP | net protein |
| PM | Proteína Metabolizável | MP | metabolizable protein |
| PMF | PB Metabólica Fecal | MFP | metabolic fecal protein |
| Pmic | Proteína microbiana | MCP | microbial crude protein |
| Pmol | Peso molecular | MW | molecular weight |
| PMR | Dieta parcial misturada | PMR | parcial mixed ration (sic: "parcial") |
| PNDR | Proteína não degradável no rúmen | RUP | rumen-undegradable protein |
| PNDRd | Proteína não degradável no rúmen digestível no intestino | dRUP | intestinally digested rumen-undegraded protein |
| PPL | Produção de proteína do leite | MPY | milk protein yield |
| PR | Protegido da degradação ruminal | RP | rumen protected |
| PSPS | Separador de partículas da Penn State | PSPS | Penn State Particle Separator |
| PTH | Paratormônio | PTH | parathyroid hormone |
| PVer | Proteína Verdadeira | TP | true protein |
| MSE | Quadrado Médio do erro | MSE | mean squared error |
| MSPE | Quadrado Medio do Erro da Predição | MSPE | mean squared prediction error |
| qPCR | Reação em cadeia da polimerase quantitativa | qPCR | quantitative polymerase chain reaction |
| RID | Referência de Ingestão Diária | DRI | Dietary Reference Intake |
| RMSE | Raiz Quadrada do Quadrado Médio do Erro | RMSE | root mean squared error |
| RMSEP | Raiz Quadrada do Quadrado Médio do Erro da Predição | RMSEP | root mean squared error of prediction |
| Ta | Temperatura do ar | Ta | air temperature |
| TMD-1 | Transportador de metais divalentes – 1 | DMT1 | divalent metal transporter 1 |
| TMR | Dieta total misturada | TMR | total mixed ration |
| Tpconc | Tempo relativo para oferta de concentrado para bezerras | FPstarter | time relative to first offer of starter |
| TRx | Tiorredoxinas redutases | TRx | thioredoxin reductases |
| TSD | Total de sólidos dissolvidos | TDS | total dissolved solids |
| TSH | Hormônio estimulador da tireóide | TSH | thyroid-stimulating hormone |
| UI | Unidade internacional | IU | international unit |
| UR | Umidade relativa | RH | relative humidity |
| VB | Valor biológico | BV | biological value |
| VDP | vísceras drenadas pela veia porta | PDV | portal-drained viscera |
| VI | Valor de iodo | IV | iodine value |
| WDG | Grãos de destilaria úmidos | WDG | wet distillers grains |

## 8. Ambiguidades e inconsistências do glossário (para o desenvolvedor)
- **AGT** (PT) tem dois significados: Ácidos graxos totais (TFA) e Índice de temperatura e umidade (THI) [p.534]. A sigla PT correta de THI provavelmente é diferente (ex.: ITU), mas o livro imprime AGT; no código usar EN (TFA / THI).
- **NMT** (PT): "Nível máximo tolerável" (MTL) e "Máximo nível de ingestão tolerável" (UL) [p.537]. Usar MTL e UL.
- **PL** (PT): "Produção de leite média" (MY) e "Proteína líquida" (NP) [p.538]. Usar MY e NP; PL no resto do livro costuma designar produção de leite — ⚠ verificar no contexto de cada capítulo.
- **PMR** em EN impresso "parcial mixed ration" (grafia do livro).
- "ELl" é a grafia no apêndice para ELL (energia líquida de lactação); ELLeite = MilkE.
- Siglas PT iguais a EN e sem tradução: AA, ADH, AEA, AMS, AOAC, CCK, CLA, CoA, CV, DA, DCAD, DCAD-S, DDGS, DEInp, DFM, DOM-1, DON, FAD, FMN, GM, GPx/GSHpx, HCl, HCN, HMBi, HMTBA/HMB, Ig, kd, kp, Mn-SOD, MOS, MSE, MSPE, PEM, PMR, PSPS, PTH, qPCR, RMSE, RMSEP, Ta, TMR, TRx, TSH, WDG.
- Siglas de uso direto no simulador (principais): IMS/DMI, PC/BW, PCV/EBW, PCMat/MatBW, PCM/MBW, DEL/DIM, ECC/BCS, LCGP/FPCM, PL/MY, PPL/MPY, ED/DE, EM/ME, ELL/NEL, ELm/NEm, EMm/MEm, EMg/MEg, ER/RE, EB/GE, EU/UE, Egas/GasE, NDT/TDN, PB/CP, PDR/RDP, PNDR/RUP, PM/MP, PL(proteína líquida)/NP, Pmic/MCP, PMF/MFP, PIDA/ADIP, PIDN/NDIP, FDN/NDF, FDNf/fNDF, FDNfe/peNDF, FDNfa/paNDF, FDNi/iNDF, FDNpd/pdNDF, FDNnf/nfNDF, CNF/NFC, CSDN/NDSC, CSA/WSC, DFDNf/fNDFD, kd, kp, DCAD, DCAD-S, NUL/MUN, NU/UN, NUP/BUN, ALI/FWI, ACT/TBW, ACV/EBWtr, UR/RH, Ta, AGT(THI), NNA/NAN, NNANM/NANMN, MO/OM, MOR/ROM, MORd/dROM, MORe/eROM, IED/DEI, IEM/MEI, IEB/GEI, GMD/ADG, GCV/EBG, TMR, PMR, RMSE/RMSEP.

---

# APÊNDICE C — Biografias dos Membros do Comitê [pp. 539-541]
Existe: biografias dos 12 membros do comitê (informações atualizadas quando o comitê foi formado em 2014, conforme nota de rodapé da p.539), incluindo os co-presidentes R. A. Erdman e W. P. Weiss. Sem relevância para o simulador; não detalhado. A p.542 está em branco (página de imagem sem texto; "OCR NOT READY" persistente é porque não há conteúdo).

---

# Dúvidas/riscos de OCR adicionais (Apêndice B)
- OCR leu "TEA" para TFA (corrigido pela imagem), "ELI" para "ELl" (corrigido), "=100" para "-100" (corrigido), "Ul/kg" para UI/kg.
- Colunas das pp.535-538 vieram desalinhadas no OCR (colunas separadas); alinhamento refeito pelas imagens.
- ⚠ Não conferidos item a item os acentos de 'Ácido cianídrico/ Ácido prussico' (reproduzido como impresso).

COBERTURA: páginas lidas 529–542 (pdf 549–562). Cap. 21 (pp.529-532): texto e as 3 tabelas numéricas transcritas e conferidas contra imagem rotacionada/ampliada a 220 dpi. Apêndice A (p.533): escopo transcrito. Apêndice B (pp.534-538): 174 linhas de glossário transcritas integralmente e conferidas contra as imagens. Apêndice C (pp.539-541): só registrada a existência (conforme instruído). p.542: em branco (sem OCR por não haver conteúdo; imagem conferida). Nada ficou de fora.

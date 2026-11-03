# Sistema de design e roteiro da repaginação

**Versão 0.2 (03/11/2026).** Define a linguagem visual do sistema (tokens, componentes, gráficos), registra as decisões de
produto da repaginação e o roteiro por etapas. As etapas D1 (tokens, estrutura e componentes-base) e D2 (tela Vaca leiteira) estão implementadas; as demais
estão descritas na seção 7. Código: `web/src/app/globals.css`, `web/src/components/`. Complementa o `DESIGN.md` (descrição detalhada do que existe).

## 1. Princípios

- **Simulador, não painel de vendas.** O fluxo é **configurar → executar → analisar → comparar**; cada tela de simulação segue o mesmo esqueleto.
- **Gráfico antes da tabela.** A tabela continua, para conferir números, mas a análise começa num gráfico; todo gráfico terá a opção "ver como tabela" (acessibilidade).
- **Só o dado de interesse chama atenção:** nos gráficos, tudo em verde apagado e só o escolhido (cenário ótimo, melhor dieta) em verde vivo, com o valor sobre a barra.
- **Estado nunca só em cor:** ícone e texto acompanham cor (regra do FSD A.4.1, vale para todo o sistema).
- **Escuro por padrão**, com tema claro equivalente.

## 2. Tokens (implementados)

| Token | Escuro | Claro | Uso |
|---|---|---|---|
| `--background` | `#0A0B0D` | `#F5F6F4` | fundo da página |
| `--card` | `#111417` | `#FFFFFF` | cartões, cabeçalho (com 80% de opacidade) |
| `--surface` | `#171B1F` | `#F0F2EF` | superfícies elevadas |
| `--border` | `rgb(255 255 255 / 7%)` | `#E3E6E2` | contornos de 1 px, sem sombra |
| `--foreground` / `--muted-foreground` | `#F3F5F6` / `#8B949E` | `#12161A` / `#5F6B76` | texto e texto secundário |
| `--primary` | `#F3F5F6` (texto `#0A0B0D`) | `#12161A` (texto `#F3F5F6`) | botão primário **claro** |
| `--brand` | `#10B981` | `#059669` | acento esmeralda: destaque, estado ativo, indicadores |
| `--brand-dim` / `--chart-dim` | `#14513F` | `#A7D9C6` | barras e séries "apagadas" |
| `--info` / `--violet` / `--destructive` / `--warning` | `#3B82F6` / `#8B5CF6` / `#EF4444` / `#F59E0B` | `#2563EB` / `#7C3AED` / `#DC2626` / `#D97706` | secundárias dos ícones, deltas e alertas |
| `--chart-1..8` | esmeralda, âmbar, azul, vermelho, roxo, ciano, lima, rosa | tons mais escuros | séries de gráficos |

- **Tipografia:** Geist Sans, com números tabulares. Título de página 24/32 px (30 px em telas largas) bold; título de cartão 18 px semibold; número de KPI 24/32 px extra-bold; corpo 14 px; legenda 12 px.
- **Espaçamento:** base de 4 px; padding de cartão 24 px (20 px no celular); vão entre cartões 24 px (16 px no celular).
- **Raios** (`--radius` = 12 px): cartão 20 px, botão e campo 12 px, pill e barra superior 999 px, quadrado de ícone 12 px.

## 3. Componentes

| Componente | Regras |
|---|---|
| Cartão (`ui/card`) | fundo `--card`, borda de 1 px, sem sombra, raio de 20 px |
| Botão (`ui/button`) | `default` claro; `brand` esmeralda; `outline` com contorno fino e fundo transparente; altura de 40 px |
| Campo (`ui/input`) | altura de 40 px, contorno fino, fundo igual ao do cartão, foco esmeralda |
| Pill (`ui/badge`) | `secondary` = esmeralda a 12% (atende, viável); `destructive` = vermelho a 12%; `warning` = âmbar a 12%; `neutral` = cinza |
| Tabela (`ui/table`) | cabeçalho de 12 px em caixa-alta e cinza, linhas de ~52 px, hover a 3%, linha selecionada em esmeralda a 10% |
| `IconTile` e `DeltaPill` (`components/shared`) | ícone em quadrado com a cor a 12%; variação em pill, verde quando melhora e vermelho quando piora (`better` diz se subir é bom) |
| `KpiCard` | ícone, valor grande, delta, dica e mini gráfico de tendência (`Sparkline`) em linha própria, na largura do cartão |
| `RunButton` | botão Executar com os quatro estados: pronto (claro), executando (barra de progresso dentro do botão, "n de N"), concluído (esmeralda, "ver resultados", com "executar de novo") e erro (vermelho, "tentar de novo") |
| `ChartCard` | cartão de gráfico com a alternância **gráfico / tabela** (mesmo dado, para conferir números e por acessibilidade) |
| `Tabs` (`ui/tabs`) | abas em pílula; a aba ativa ganha o fundo do cartão |
| `EmptyState` e `ResultsSkeleton` | estado vazio (ícone, título e os passos do fluxo) e esqueleto dos resultados enquanto a execução roda |
| `Bullet` (`charts`) | valor sobre as faixas ok, atenção e alerta; o valor sempre vem também em texto |
| `DivergingBars`, `TimeSeries`, `SeriesLegend` (`charts`) | barras divergentes a partir do zero; áreas e linhas no tempo (podem empilhar, com eixo direito); legenda fora do gráfico |
| Barra superior | pílula flutuante: alternar sidebar, tela atual, busca `Ctrl K` / `⌘K` (paleta de comandos), **Tarefas** (simulações e otimizações em andamento), tema, estado da conexão |
| Sidebar | flutuante e recolhível; item ativo em esmeralda a 12% |

## 4. Gráficos por saída

| Saída | Gráfico | Destaque |
|---|---|---|
| Margem por cenário (sensibilidade) | barras verticais (`HighlightBars`) | cenário ótimo vivo; linha tracejada do base |
| Quantidades do quadro | barras (`HighlightBars`) | alimento de maior quantidade |
| Distribuição das margens | histograma | marcas do base e do ótimo |
| Efeito dos fatores | tornado ordenado por \|ρ\| | maior efeito |
| Leite, custo da ração, exigência × consumo | áreas e linhas no tempo | marcos do RuFaS (PEV, secagem) |
| Ração média | barras horizontais ordenadas; área empilhada por intervalo | maior participação |
| Balanço nutricional | barras divergentes em % da exigência | déficit em vermelho |
| Verificações V1 a V5 | bullet charts contra as faixas ok, atenção e alerta | estado |
| Ranking de dietas | barras horizontais de custo | melhor viável viva; inviáveis hachuradas; linha da dieta ótima |
| Erro de linearização | barras por restrição com a linha da tolerância | acima da tolerância |
| Dieta ótima × SLSQP | pontos por semente com a linha do LP; composição a 100% lado a lado | o LP |
| Busca do LP (opcional) | mapa de calor do custo por TDN% × consumo | ponto ótimo e regime de 60% |

## 5. Estados e responsividade

- **Vazio:** ícone, uma frase e o próximo passo como botão. **Carregando:** *skeleton* com o formato final dos cartões. **Erro:** alerta com "tentar de novo" e o detalhe recolhível. **Resultado desatualizado:** opacidade reduzida e faixa explicativa. **Sem conexão:** parâmetros desabilitados com a instrução.
- **≥ 1280 px:** parâmetros fixos à esquerda e resultados à direita. **768 a 1279 px:** parâmetros no topo, recolhíveis. **< 768 px:** botão Executar fixo no rodapé, KPIs em duas colunas, tabelas com a primeira coluna fixa e a barra superior compacta.

## 6. Decisões de produto (03/11/2026)

| Decisão | Escolha |
|---|---|
| O que é uma "execução" | **qualquer execução**: simulação do RuFaS, análise de sensibilidade, avaliação de dietas e dieta ótima, num histórico único, com o tipo numa coluna |
| Onde guardar o histórico | **arquivos no servidor** (pasta local do projeto, ao lado do cache do RuFaS): sobrevive a recarregar a página e a reiniciar o servidor |
| Cenário-base dos deltas | **o que o usuário marcar** (estrela na tabela de execuções); sem marcação, a primeira execução do histórico |
| Fonte do mini gráfico dos KPIs | **a série da própria simulação** (intervalos de 30 dias, leite diário), que existe desde a primeira execução |
| Adaptações da referência | sem avatar (não há login): entra o estado da conexão; "notificações" viram **Tarefas**; a busca `⌘K` é uma paleta de comandos |

## 7. Roteiro por etapas (um PR por etapa)

| Etapa | Conteúdo | Situação |
|---|---|---|
| D1 | Tokens, barra superior em pílula, sidebar flutuante, paleta de comandos, menu Tarefas, `KpiCard` com ícone e tendência, `HighlightBars`, cartões, botões, campos, pills e tabelas | **Feita (03/11/2026)** |
| D2 | Tela Vaca leiteira: painel de parâmetros fixo, botão Executar com quatro estados, gráficos de ração (barras horizontais), balanço (barras divergentes), verificações (bullet), série de custo e de leite | **Feita (03/11/2026)** |
| D3 | Histórico de execuções no servidor (API, tabela com busca, filtro, status, ações e paginação), estrela do cenário-base, tela de detalhe e deltas dos KPIs | Planejada |
| D4 | Sensibilidade: histograma, tornado e comparação de cenários com o base; tabela de cenários com o padrão da D3 | Planejada |
| D5 | Avaliar dietas: ranking, erro de linearização, comparação com o RuFaS e dieta ótima em gráficos | Planejada |
| D6 | Exercício do quadro e Curva de lactação, estados vazio, carregando e erro, "ver como tabela" em todos os gráficos | Planejada |

## 8. Tela Vaca leiteira (D2)

- **Painel de parâmetros** à esquerda (24 rem), fixo ao rolar em telas largas, com a rolagem só na lista de alimentos e o botão **Executar simulação** sempre visível no rodapé do painel. Abaixo de 1280 px o botão vira uma barra fixa na parte de baixo da tela.
- **Estado da execução:** o botão acompanha pronto → executando → concluído → erro. Se os parâmetros mudam depois da simulação, o botão volta a "Executar simulação" e os resultados ficam esmaecidos com uma faixa de aviso (a chave dos parâmetros fica no `AppProvider`, `simKey`).
- **Resultados em abas:**
  - **Visão geral:** KPIs com mini gráfico, alertas, **ração média** (barras horizontais, o ingrediente principal em verde vivo), **balanço nutricional** (barras divergentes da oferta em relação à exigência, cortadas em +150% com o valor real no rótulo), **leite do rebanho** (área com as vacas em lactação em linha tracejada no eixo direito) e **custo da ração por vaca**.
  - **Ração:** ração ao longo do tempo (áreas empilhadas) e composição média.
  - **Nutrição:** verificações V1 a V5 com a faixa (bullet) abaixo do nome, balanço em tabela e exigências.
- Cada gráfico novo tem a alternância **gráfico / tabela**. Sem simulação, a tela mostra o estado vazio com os três passos do fluxo; enquanto a primeira roda, o esqueleto dos resultados.
- Não feito nesta etapa: o delta dos KPIs (depende do cenário-base da D3) e o botão Cancelar da simulação (o RuFaS roda em outro processo e o servidor só cancela tarefas na fila).

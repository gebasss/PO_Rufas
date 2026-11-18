---
name: Dieta Ótima com RuFaS
colors:
  background:         '#f5f6f4'
  foreground:         '#12161a'
  card:               '#ffffff'
  surface:            '#f0f2ef'
  secondary:          '#eef0ee'
  border:             '#e3e6e2'
  input:              '#d5dad6'
  ring:               '#059669'
  muted-foreground:   '#5f6b76'
  primary:            '#12161a'
  primary-foreground: '#f3f5f6'
  brand:              '#059669'
  brand-foreground:   '#ffffff'
  brand-dim:          '#a7d9c6'
  destructive:        '#dc2626'
  success:            '#059669'
  warning:            '#d97706'
  warning-text:       '#b45309'
  info:               '#2563eb'
  violet:             '#7c3aed'
  chart-1:            '#059669'
  chart-2:            '#d97706'
  chart-3:            '#2563eb'
  chart-4:            '#dc2626'
  chart-5:            '#7c3aed'
  chart-6:            '#0891b2'
  chart-7:            '#65a30d'
  chart-8:            '#db2777'
colors-dark:
  background:         '#0a0b0d'
  foreground:         '#f3f5f6'
  card:               '#111417'
  surface:            '#171b1f'
  secondary:          '#1a1f24'
  border:             'branco a 7%'
  input:              'branco a 12%'
  ring:               '#10b981'
  muted-foreground:   '#8b949e'
  primary:            '#f3f5f6'
  primary-foreground: '#0a0b0d'
  brand:              '#10b981'
  brand-foreground:   '#04130d'
  brand-dim:          '#14513f'
  destructive:        '#ef4444'
  success:            '#10b981'
  warning:            '#f59e0b'
  warning-text:       '#fbbf24'
  info:               '#3b82f6'
  violet:             '#8b5cf6'
  chart-1:            '#10b981'
  chart-2:            '#f59e0b'
  chart-3:            '#3b82f6'
  chart-4:            '#ef4444'
  chart-5:            '#8b5cf6'
  chart-6:            '#06b6d4'
  chart-7:            '#84cc16'
  chart-8:            '#ec4899'
typography:
  font-principal: Geist Sans (variável)
  font-mono: Geist Mono (variável, registrada; sem uso atual)
  corpo:
    fontSize: 14px
  page-title:
    fontSize: 24px (30px a partir de 640px)
    fontWeight: '700'
    letterSpacing: -0.025em
  card-title:
    fontSize: 18px
    fontWeight: '600'
    letterSpacing: -0.025em
  kpi-valor:
    fontSize: 24px
    fontWeight: '800'
    fontVariantNumeric: tabular-nums
  legenda:
    fontSize: 12px
  cabecalho-tabela:
    fontSize: 12px
    fontWeight: '500'
    textTransform: uppercase
rounded:
  base: 12px
  sm: 7px
  md: 10px
  lg: 12px
  xl: 17px
  2xl: 22px
  card: 20px
  pill: 999px
spacing:
  margem-pagina: 12px (24px a partir de 640px)
  topo-pagina: 24px
  base-pagina: 32px
  gap-blocos: 24px
  gap-indicadores: 12px
  padding-card: 24px (20px abaixo de 640px)
  padding-card-sm: 16px
  altura-campo: 40px
  altura-botao: 40px (sm 36px, lg 44px, xs 24px)
largura-conteudo-max: 1440px
largura-barra-lateral: 256px (aberta), 48px (ícones), 288px (gaveta no celular)
largura-painel-lateral: 384px
---

## Contexto

Este documento descreve o padrão visual **atualmente implementado** na interface web do Dieta Ótima com RuFaS
(`web/`, publicada em `frontend/`). A interface é um site estático gerado pelo Next.js a partir do template AdminCN
(shadcn/ui), servido pelo servidor Python local. Todos os tokens vivem em `web/src/app/globals.css`; os componentes
usam classes do Tailwind e variantes do shadcn/ui, e não há CSS espalhado por componente.

Este arquivo é a **única fonte das regras visuais**. Ele incorpora o que valia do antigo roteiro da repaginação
(princípios, tokens, componentes, gráficos por saída, estados e decisões de produto de 03/11/2026), hoje guardado só
como registro histórico em [arquivo/DESIGN_REPAGINACAO.md](arquivo/DESIGN_REPAGINACAO.md). As lacunas conhecidas estão
na seção _Limitações_. O comportamento de cada tela, passo a passo, está nos guias em [guias/](guias/), e o que cada
tela deve fazer (requisitos), no [FSD](FSD.md).

**Versão do documento:** 1.0 (consolidado em 16/11/2026, sobre o código da época: 6 telas, tema escuro por padrão) ·
**Autor(es):** _[a preencher]_ · **Relacionado:** [PRD](PRD.md) · [FSD](FSD.md)

**Estrutura.** As nove primeiras seções (Contexto a Estados do Sistema) seguem o modelo de DESIGN.md. As seguintes
foram acrescentadas porque o produto tem telas, gráficos e uma origem em template que o modelo não cobre: _Telas_,
_Visualização de Dados_, _Padrões de Interação e Conteúdo_, _Acessibilidade_, _Responsividade_, _Arquitetura e
Origem_, _Persistência e Privacidade_, _Decisões de Design_, _Limitações_, _Licenças_, _Manutenção_ e dois apêndices.

## Brand & Estilo

A interface é um **simulador analítico de uso desktop** para nutricionistas, produtores de leite e para o professor
que avalia a modelagem. O fluxo de toda tela de simulação é **configurar → executar → analisar → comparar**. O estilo
é **escuro por padrão, sóbrio e orientado a dados**: fundo quase preto (ou off-white no tema claro), cartões de 20 px
com borda fina e sem sombra, cinzas neutros e **uma única cor de marca, o esmeralda**. A prioridade é ler números com
unidade, comparar cenários e perceber quando o modelo alterou algo por conta própria; ornamento é mínimo.

A cor tem função: esmeralda (`brand`) para destaque, estado ativo e efeito positivo; âmbar para aviso do modelo (leite
perdido); vermelho para erro, inviabilidade e efeito negativo; azul e violeta apenas como cores secundárias de ícones
e séries. O botão primário **não** é verde: é claro no tema escuro e escuro no tema claro (`--primary`), e o esmeralda
fica reservado ao destaque e ao botão `brand` (estado "concluído" do botão de executar).

### Princípios

| # | Princípio | O que significa na prática |
|---|---|---|
| P1 | **Mostrar a unidade sempre** | Todo número tem unidade visível (US$/kg MS, kg MS/vaca/dia, Mcal/dia). Valores em formato pt-BR. |
| P2 | **Não esconder o que o modelo fez** | Falhas aparecem como "falhou"; leite reduzido pelo RuFaS aparece como "leite perdido", com alerta. Nunca um zero silencioso. |
| P3 | **Rotular o que é ilustrativo** | Preços iniciais não são cotações: o aviso está no rodapé, na tela de premissas e nos textos de apoio. |
| P4 | **Resultado primeiro** | Nas telas de simulação, os indicadores e o gráfico principal vêm no topo (aba "Visão geral"); os detalhes vêm nas outras abas. |
| P5 | **Tarefa longa com progresso** | Simulações levam de 30 s a vários minutos: a tela mostra progresso, não trava e permite continuar navegando; o menu **Tarefas** lista o que está rodando. |
| P6 | **Um sistema, dois temas** | Escuro por padrão e claro equivalente, com a mesma estrutura. O contraste medido está em _Acessibilidade_. |
| P7 | **Reuso antes de invenção** | Componentes do shadcn/ui; só se cria algo novo quando não existe equivalente. |
| P8 | **Gráfico antes da tabela, tabela a um clique** | A análise começa num gráfico; todo gráfico de resultado tem a alternância **gráfico / tabela** (mesmo dado, para conferir números e por acessibilidade). |
| P9 | **Só o dado de interesse chama atenção** | Nos gráficos, tudo em verde apagado (`chart-dim`) e só o escolhido (cenário ótimo, melhor dieta) em verde vivo, com o valor sobre a barra. |
| P10 | **Estado nunca só em cor** | Ícone e texto acompanham a cor (regra do FSD A.4.1, vale para todo o sistema). |

## Cores

Tokens em hexadecimal, definidos em `web/src/app/globals.css` e expostos ao Tailwind (`bg-card`,
`text-muted-foreground`, `text-brand` etc.). O front matter e o [Apêndice A](#apêndice-a-tokens-de-cor) trazem os
mesmos valores. O tema escuro **não é uma inversão**: cada token tem valor próprio, mais claro nas cores de realce
para manter o contraste.

| Token | Escuro | Claro | Uso |
|---|---|---|---|
| `--background` | `#0A0B0D` | `#F5F6F4` | Fundo da página |
| `--card` | `#111417` | `#FFFFFF` | Cartões, barra superior (com 80% de opacidade), sidebar (`#0D0F11` no escuro, `#FFFFFF` no claro) |
| `--surface` | `#171B1F` | `#F0F2EF` | Superfícies elevadas |
| `--secondary`, `--muted`, `--accent` | `#1A1F24` | `#EEF0EE` | Fundo de _hover_, abas, linhas alternadas |
| `--border` / `--input` | branco a 7% / 12% | `#E3E6E2` / `#D5DAD6` | Contornos de 1 px (sem sombra) e bordas de campos |
| `--foreground` / `--muted-foreground` | `#F3F5F6` / `#8B949E` | `#12161A` / `#5F6B76` | Texto e texto secundário (descrições, dicas, rótulos) |
| `--primary` (texto) | `#F3F5F6` (`#0A0B0D`) | `#12161A` (`#F3F5F6`) | Botão primário **claro** no escuro e escuro no claro |
| `--brand` (texto) | `#10B981` (`#04130D`) | `#059669` (`#FFFFFF`) | Acento esmeralda: destaque, estado ativo, indicadores, foco (`--ring`) |
| `--brand-dim` / `--chart-dim` | `#14513F` | `#A7D9C6` | Barras e séries "apagadas" |
| `--destructive` | `#EF4444` | `#DC2626` | Erro, "inviável", "falhou", conexão perdida, efeito negativo |
| `--warning` / `--warning-text` | `#F59E0B` / `#FBBF24` | `#D97706` / `#B45309` | Aviso do modelo. Dois tokens porque o âmbar de fundo não tem contraste suficiente como **texto** |
| `--success` | `#10B981` | `#059669` | Confirmações e efeito positivo |
| `--info` / `--violet` | `#3B82F6` / `#8B5CF6` | `#2563EB` / `#7C3AED` | Cores secundárias de ícones, variações e séries |
| `--chart-1` a `--chart-8` | esmeralda, âmbar, azul, vermelho, roxo, ciano, lima, rosa | tons mais escuros das mesmas famílias | Séries de gráficos (valores no Apêndice A) |

O tema inicial é **escuro** (`defaultTheme='dark'` em `app/layout.tsx`); o botão da barra superior alterna entre
escuro e claro, e a escolha fica no `localStorage` (`theme`).

## Tipografia

- **Fonte principal:** Geist Sans (variável), pelo pacote `geist` com arquivos locais (sem Google Fonts). Geist Mono
  está registrada (`--font-mono`) mas **não é usada** por nenhum componente.
- **Corpo e descrições:** 14 px (`text-sm`); legendas, dicas e rótulos pequenos 12 px (`text-xs`); 11 px só nas
  etiquetas de atalho (`kbd`) e em campos compactos.
- **Título da página (`h1`, `PageHeader`):** 24 px (30 px a partir de 640 px), bold, `tracking-tight`; a descrição
  abaixo tem 14 px, cor secundária e largura máxima de 48 rem.
- **Título de cartão (`CardTitle`):** 18 px, semibold, `tracking-tight` (14 px nos cartões `size='sm'`).
- **Indicadores (`KpiCard`):** rótulo em 12 px, valor em 24 px **extra-bold**, dica em 12 px.
- **Cabeçalho de tabela:** 12 px, caixa alta, `tracking-wide`, cor secundária; linhas de cerca de 52 px.
- **Números:** `tabular-nums` (dígitos de largura fixa) em tabelas, campos numéricos e indicadores, para alinhar casas.
  Formato pt-BR (vírgula decimal, ponto de milhar).

## Layout & Espaçamento

- **Container:** conteúdo centralizado com `max-w-360` (**1.440 px**), margens laterais de 12 px (celular) e 24 px a
  partir de 640 px, 24 px acima e 32 px abaixo do conteúdo.
- **Estrutura da tela:** sidebar flutuante recolhível, barra superior em pílula (fixa no topo), conteúdo e rodapé.

```
┌───────────────┬──────────────────────────────────────────────────────────────┐
│  Marca        │  ( ☰  Tela atual   Buscar… Ctrl K   Tarefas  ☀  ● conectado )│  barra superior (pílula)
│               ├──────────────────────────────────────────────────────────────┤
│  ANÁLISE      │  Título da página                                            │
│   Ruminante   │  Descrição                                                   │
│   Vaca        │  ┌─────────────┐ ┌──────────────────────────────────────┐    │
│   Curva       │  │ Parâmetros  │ │ Resultados em abas                   │    │
│   Sensibil.   │  │ (fixo, 24rem)│ │ (indicadores, gráficos, tabelas)     │    │
│   Execuções   │  │ [Executar]  │ │                                      │    │
│  PROJETO      │  └─────────────┘ └──────────────────────────────────────┘    │
│   Premissas   ├──────────────────────────────────────────────────────────────┤
│  RuFaS · NRC  │  Rodapé: RuFaS v1.0.6 (GPLv3) · NRC · NASEM · preços ilustrativos │
└───────────────┴──────────────────────────────────────────────────────────────┘
```

- **Grades de conteúdo:**

| Padrão | Uso |
|---|---|
| Painel lateral de 24 rem + resultados (`xl:grid-cols-[24rem_minmax(0,1fr)]`), painel fixo ao rolar (`xl:sticky`) com rolagem só na lista | Vaca leiteira e Sensibilidade |
| Indicadores: 1 coluna (celular), 2 (≥ 640 px), 3 (≥ 1.536 px) | Resultados da Vaca leiteira (`sm:grid-cols-2 2xl:grid-cols-3`) |
| Pares de gráficos lado a lado a partir de 1.536 px (`2xl:grid-cols-2`) | Composição × exigências; efeito × margem |

- **Espaçamento:** base de 4 px; 24 px entre blocos (`gap-6`); 12 px entre indicadores; padding interno de cartão de
  24 px (20 px abaixo de 640 px) ou 16 px (`size='sm'`, usado nos indicadores).
- **Tabelas largas** rolam na horizontal dentro do cartão.

### Barra lateral

| Propriedade | Valor |
|---|---|
| Largura | 16 rem (aberta), 3 rem (só ícones), 18 rem (gaveta no celular) |
| Grupos | **Análise**: Ruminante Singular (`/`), Vaca leiteira (`/vaca`), Curva de lactação (`/curva`), Sensibilidade (`/sensibilidade`) e Execuções (`/execucoes`). **Projeto**: Premissas e limites (`/sobre`) |
| Ícones (Lucide) | `CalculatorIcon`, `MilkIcon`, `TrendingUpIcon`, `SlidersHorizontalIcon`, `HistoryIcon`, `InfoIcon` |
| Item ativo | Fundo esmeralda a 12% e texto `brand`; a comparação ignora a barra final da rota |
| Recolher | Botão na barra superior ou `Ctrl/Cmd + B`; no modo ícones aparece dica (_tooltip_) com o nome; o estado fica no cookie `sidebar_state` (7 dias) |
| Rodapé | "RuFaS v1.0.6 · NRC 2001 · NASEM 2021" (some no modo ícones) |
| Abaixo de 1.280 px | Vira gaveta (`Sheet`) aberta pelo botão da barra superior e fecha ao navegar |

### Barra superior

Pílula flutuante (`sticky top-3`, `rounded-full`, `bg-card/80` com desfoque, largura do conteúdo) com, da esquerda para
a direita: botão da sidebar, **tela atual**, **busca** (`Ctrl K` ou `⌘K`, abre a paleta de comandos para ir a qualquer
tela), **Tarefas** (simulações e otimizações em andamento, com progresso), botão de tema e **estado da conexão**
(_conectando…_, _conectado · N alimentos NRC_ e _sem conexão com o servidor_, este em vermelho). Não há avatar nem menu de
perfil, porque não há login.

## Elevação & Profundidade

A hierarquia é construída por **camadas tonais** (fundo → cartão → superfície) e **bordas de 1 px**, não por sombra.
Cartões não têm sombra; o anel de foco usa `ring` esmeralda. Camadas flutuantes (gaveta, _tooltip_, lista do `Select`,
diálogo, paleta de comandos) usam o estilo padrão do shadcn. A barra fixa de execução no celular usa fundo
`card/90` com desfoque.

Há uma animação de pulso (`heartbeat`) definida em `globals.css` e herdada do template; nenhuma tela a usa.

## Formas (Border Radius)

Base `--radius: 0.75rem` (12 px) e derivados calculados em `globals.css`:

| Token | Fator | Valor | Uso |
|---|---|---|---|
| `sm` | 0,6× | 7 px | Detalhes pequenos |
| `md` | 0,8× | 10 px | Botões `xs` |
| `lg` | 1× | 12 px | Botões, campos, quadrado de ícone (`IconTile`) |
| `xl` | 1,4× | 17 px | Itens da sidebar, painéis internos |
| `2xl` | 1,8× | 22 px | Barra fixa de execução no celular |
| cartão | fixo | 20 px (`rounded-[1.25rem]`) | `Card` |
| pílula | 999 px | | Barra superior, abas, selos, alternância gráfico/tabela |

## Componentes

### Do shadcn/ui

Em `web/src/components/ui/`, sobre Base UI: `Alert`, `Badge`, `Breadcrumb`, `Button`, `Card`, `Chart` (envolve o
Recharts), `Checkbox`, `Dialog`, `Input`, `Label`, `Popover`, `Progress`, `Select`, `Separator`, `Sheet`, `Sidebar`,
`Skeleton`, `Sonner` (avisos), `Table`, `Tabs` e `Tooltip` (21 arquivos). Seguem o código do template, com as regras
visuais abaixo.

| Componente | Regras |
|---|---|
| `Card` | Fundo `--card`, borda de 1 px, sem sombra, raio de 20 px; padding de 24 px (20 px no celular); `size='sm'` reduz para 16 px |
| `Button` | Variantes: `default` (claro no escuro e escuro no claro), `brand` (esmeralda), `outline` (contorno fino, fundo transparente), `secondary`, `ghost`, `destructive` (vermelho a 10%) e `link`. Tamanhos: `default` 40 px, `sm` 36 px, `lg` 44 px, `xs` 24 px e versões `icon` |
| `Input` | Altura de 40 px, contorno fino, fundo igual ao do cartão, foco esmeralda; inválido com borda destrutiva |
| `Badge` (selo) | `secondary` = esmeralda a 12% (atende, viável); `destructive` = vermelho a 12%; `warning` = âmbar a 12% (texto `warning-text`); `neutral` = cinza; também `default`, `outline`, `ghost` e `link` |
| `Table` | Cabeçalho de 12 px em caixa alta e cinza (altura 44 px), linhas de cerca de 52 px, _hover_ a 3%, linha selecionada em esmeralda a 10% |
| `Tabs` | Abas em pílula; a aba ativa ganha o fundo do cartão e o contorno |
| `Alert` | Variantes `default` e `destructive`; usado para avisos de resultado e de falha |
| `Progress` | Barra determinada ou indeterminada (valor nulo) |
| `Skeleton` | Retângulos pulsantes; usados só dentro de `EmptyState`/`ResultsSkeleton` |
| `Dialog` | Nome e nota da execução (`RunNameDialog`) e paleta de comandos (`Ctrl K`) |
| `Sonner` | _Toast_ no tema do sistema, para sucesso e erro de tarefa |

### Do projeto

| Componente | Arquivo | Função |
|---|---|---|
| `AppShell`, `AppSidebar`, `Header`, `Footer`, `ModeToggle`, `CommandPalette`, `TasksMenu` | `components/layout/` | Estrutura da tela, busca `Ctrl K` e menu de tarefas |
| `PageHeader` | `shared.tsx` | Título, descrição e ações da página |
| `KpiCard` | `shared.tsx` | Indicador com ícone, rótulo, valor grande, variação (`DeltaPill`), dica e mini gráfico de tendência (`Sparkline`, 36 px) em linha própria; tons `default`, `primary` (fundo esmeralda a 5%, borda a 40%, valor em `brand`) e `warning` (leite perdido) |
| `IconTile`, `DeltaPill` | `shared.tsx` | Ícone em quadrado com a cor a 12%; variação em pílula, verde quando melhora e vermelha quando piora (o parâmetro `better` diz se subir é bom) |
| `NumberInput` | `shared.tsx` | Campo numérico controlado (vazio vira `NaN`; ver `finite()`); aceita `aria-label` |
| `JobProgress` | `shared.tsx` | Barra de progresso com texto "n de N simulações"; hoje sem uso (o progresso vive no `RunButton`) |
| `heat()` | `shared.tsx` | Cor de fundo proporcional ao valor, para tabelas de cenários (8% a 40% da cor, ver _Acessibilidade_) |
| `RunButton` | `RunButton.tsx` | Botão de executar com quatro estados: pronto (claro), executando (barra de progresso dentro do botão, "n de N"), concluído (esmeralda, "ver resultados", com "executar de novo") e erro (vermelho, "tentar de novo") |
| `ChartCard` | `ChartCard.tsx` | Cartão de gráfico com a alternância **gráfico / tabela** |
| `EmptyState`, `ResultsSkeleton` | `EmptyState.tsx` | Estado vazio (ícone, título e os passos do fluxo) e esqueleto dos resultados enquanto a execução roda |
| `Segmented` | `Segmented.tsx` | Alternador de opções em pílula (por exemplo, a dieta em detalhe) |
| `FeedPicker` | `FeedPicker.tsx` | Busca, lista com caixas de seleção e cartões dos alimentos selecionados |
| `PriceImport`, `ScenarioFile`, `ExportButtons` | `components/` | Importar preços de planilha, salvar e abrir cenários, exportar resultados |
| Gráficos (`CHART`, `ChartTip`, `Sparkline`, `HighlightBars`, `DivergingBars`, `TimeSeries`, `SeriesLegend`, `Bullet`, `ScatterPlot`, `ToneBars`, `StatusGrid`, `ShareBars`) | `charts.tsx` | Ver _Visualização de Dados_ |
| `AppProvider` | `providers/AppProvider.tsx` | Estado compartilhado |

### Padrões dos componentes do projeto

- **Cartão de alimento selecionado:** nome completo (quebra de linha, sem corte), três campos (`US$/kg MS`,
  `mín. kg/dia`, `máx. kg/dia`) com rótulos visíveis e botão de remover com nome acessível.
- **Mapa de calor (`heat`):** a célula usa de **8% a 40%** da cor (`color-mix` sobre transparente); o teto de 40%
  garante contraste de texto. Dependendo do campo, a escala pode ser invertida.
- **Ícones:** Lucide, 16 a 20 px, estilo de linha.
- **Campos numéricos:** sem as setas de incremento do navegador (ocultadas em `globals.css`).

## Estados do Sistema (Erro / Sucesso / Aviso / Carregando / Vazio)

| Estado | Tratamento |
|---|---|
| **Vazio** | Ícone, uma frase e os três passos do fluxo (`EmptyState`); o próximo passo é o botão de executar |
| **Carregando** | Esqueleto com o formato final dos cartões (`ResultsSkeleton`) e `RunButton` em "executando", com barra de progresso e "n de N" |
| **Sucesso** | `RunButton` esmeralda ("ver resultados") e aviso breve (_toast_) |
| **Erro de tarefa ou de rede** | `RunButton` vermelho ("tentar de novo") e aviso com a primeira linha da mensagem; detalhe completo em `runs/<id>/console.log` |
| **Aviso do modelo** | Âmbar: indicador "Leite perdido" e alerta "A ração não atendeu a todas as exigências" |
| **Problema de dados** | Dentro da tabela ou do bloco, em cor destrutiva: "inviável", "falhou" (a causa fica na dica) |
| **Resultado desatualizado** | Os parâmetros mudaram depois da execução: resultados com opacidade reduzida e faixa explicativa; o botão volta a "Executar" (chaves `simKey`, `sensKey` e `resultKey`) |
| **Sem conexão** | Selo vermelho na barra superior; parâmetros e botões de execução desabilitados com a instrução |

A cor **nunca é o único canal**: os estados também têm texto ("falhou", "inviável", "leite perdido"), símbolo ou número.

## Telas

Seis telas, uma por rota. As páginas em `app/*/page.tsx` apenas renderizam a _view_ correspondente. O passo a passo
de cada uma está nos guias em `guias/`; os requisitos, no FSD.

| Rota | Tela | Arquivo |
|---|---|---|
| `/` | Ruminante Singular | `views/ExerciseView.tsx` e `views/ModuleView.tsx` (com `views/module/`) |
| `/vaca/` | Vaca leiteira (RuFaS) | `views/CowView.tsx` (com `views/cow/`) |
| `/curva/` | Curva de lactação | `views/CurveView.tsx` |
| `/sensibilidade/` | Sensibilidade (RuFaS) | `views/SensitivityView.tsx` (com `views/sensitivity/`) |
| `/execucoes/` | Execuções | `views/HistoryView.tsx` (com `views/history/`) |
| `/sobre/` | Premissas e limites | `views/AboutView.tsx` |

### Ruminante Singular (`/`)

**Objetivo:** avaliar dietas já montadas para uma vaca real e comparar com a dieta de menor custo. O modo de exercício
simples (PL de arroz e milho) foi retirado em 11/11/2026. **Entradas** em abas (Vaca, Dietas, Preços e limites) e uma
barra de execução com o `RunButton` **Avaliar dietas**, a lista do que falta preencher e o aviso de resultado
desatualizado. **Resultados** em abas, com o botão de exportar no cabeçalho:

| Aba | Conteúdo |
|---|---|
| Ranking | Indicadores (melhor dieta, dietas viáveis, menor custo com o desvio contra a dieta ótima, custo da dieta ótima); **custo por dieta** (`ToneBars`: melhor viável em verde vivo, outras viáveis em verde apagado, inviáveis em vermelho, linha tracejada da dieta ótima); detalhe da dieta escolhida |
| Restrições | **Mapa de restrições** (`StatusGrid`: uma linha por restrição e uma coluna por dieta; cada célula com símbolo e texto para leitor de tela além da cor); **folga** da dieta escolhida em % da exigência (`DivergingBars`); tabela completa |
| Linearização | Indicadores da comparação; **erro por dieta** e **erro por restrição** (`ToneBars` com a linha da tolerância; restrições exatas em cinza) |
| Dieta ótima | Indicadores; **composição** do LP contra a melhor execução do RuFaS (`ShareBars`, barras empilhadas a 100%); **custo de cada execução do RuFaS** (`ScatterPlot` com a linha do LP); folga; preços-sombra em tabela |

### Vaca leiteira (`/vaca/`)

**Objetivo:** simular com o RuFaS e ver ração, custo, leite e margem.

- **Painel de parâmetros** à esquerda (24 rem), fixo ao rolar em telas largas, com rolagem só na lista de alimentos e o
  `RunButton` **Executar simulação** sempre visível no rodapé do painel. Abaixo de 1.280 px o botão vira uma barra
  fixa na parte de baixo da tela. O painel reúne preço do leite, período (1 ou 2 anos), redução máxima de leite,
  **Conjunto base** e **Lista ampla**, busca na biblioteca (até 60 resultados por vez, com tipo, PB, FDN e NEL),
  alimentos selecionados, importação de preços e cenário em arquivo.
- **Resultados em abas:**

| Aba | Conteúdo |
|---|---|
| Visão geral | Indicadores com mini gráfico (e variação contra a simulação-base); alertas; **ração média** (barras horizontais, o ingrediente principal em verde vivo); **balanço nutricional** (barras divergentes da oferta em relação à exigência, cortadas em +150% com o valor real no rótulo); **leite do rebanho** (área, com as vacas em lactação em linha tracejada no eixo direito); **custo da ração por vaca** |
| Ração | Ração ao longo do tempo (áreas empilhadas) e composição média |
| Nutrição | Verificações V1 a V5 com a faixa (`Bullet`) abaixo do nome, balanço em tabela e exigências |
| Ração linear | Botão **Comparar com a ração linear** (`RunButton` com Cancelar), cinco indicadores (custo do RuFaS e do LP em dois consumos, e a diferença do rebanho), **custo da ração por intervalo** (três linhas, com tabela), **ração média** e o quadro "Como ler esta comparação" (`views/cow/LinearRationCard.tsx`) |

Não há botão Cancelar: o RuFaS roda em outro processo e o servidor só cancela tarefas na fila.

### Curva de lactação (`/curva/`)

**Objetivo:** reproduzir o gráfico do quadro (produção × dias, PEV e gestação). Cartão do ciclo reprodutivo (PEV,
gestação, secagem) com a frase do parto e da secagem previstos; indicadores por paridade com o mini gráfico da própria
curva; **produção por dia** (`TimeSeries` com faixa verde da gestação e marcas tracejadas do PEV, da secagem e do
parto) e **produção acumulada em 305 dias**. Sem simulação prévia usa os parâmetros de referência da API; depois de
uma simulação, os calibrados pelo RuFaS (indicado por selo). Sem parâmetros (servidor fora do ar), estado vazio.

### Sensibilidade (`/sensibilidade/`)

**Objetivo:** variar preços e ver o efeito na margem. **Painel de fatores** fixo à esquerda (uma linha por alimento
selecionado e uma para o preço do leite, com mínimo e máximo; método e níveis; estimativa de cenários, simulações e
tempo; `RunButton` no rodapé). **Resultados em abas:**

| Aba | Conteúdo |
|---|---|
| Visão geral | Indicadores (melhor margem com variação contra a simulação-base, pior, amplitude, cenários com resultado); **margem por cenário** (barras, o ótimo em verde vivo e a linha tracejada do base); **distribuição das margens** (histograma); ração do cenário ótimo |
| Fatores | **Efeito de cada fator** em tornado (barras divergentes ordenadas por \|ρ\| de Spearman; verde sobe a margem, vermelho reduz); **margem em função de um fator** (dispersão com um ponto por cenário, com seletor do fator) |
| Cenários | Tabela de cenários, com o ótimo destacado e **Res** em mapa de calor |
| Ração linear | Botão **Comparar com a ração linear** (`RunButton` com Cancelar), quatro indicadores (economia média, melhor caso, pior caso e empates), **economia do LP no custo da ração, por simulação** (barras divergentes de −1% a +1%, verde = o linear custa menos, com tabela) e o quadro "Como ler esta comparação" (`views/sensitivity/LinearRationCard.tsx`) |

A linha tracejada e a variação só aparecem quando há uma simulação-base **com o mesmo período** (a margem cresce com os
anos). Cenário que falha mostra "falhou" (causa na dica); leite perdido aparece em âmbar.

### Execuções (`/execucoes/`)

**Objetivo:** histórico de tudo o que foi executado (simulação, sensibilidade, avaliação de dietas e dieta ótima),
guardado em arquivos no servidor. Tabela com busca, filtros de tipo e estado, linhas por página, **estrela do
cenário-base**, selos de tipo e estado, nome e nota da execução, resultado principal, data, ações (ver, duplicar,
exportar, excluir) e paginação; painel de armazenamento com limpeza das pastas de simulação. O **detalhe** (`?id=`)
mostra os parâmetros usados à esquerda e os resultados à direita, reaproveitando as telas de resultado da simulação e
da sensibilidade. Especificação: FSD, seção A.12.

### Premissas e limites (`/sobre/`)

Cartões de texto: como o sistema funciona, o que o modelo assume, o que ele não faz, leitura dos resultados e créditos
e licenças. Serve de resposta rápida à pergunta "posso confiar neste número?". É a única _view_ estática (sem
`'use client'`).

## Visualização de Dados

Recharts, por meio do wrapper `chart.tsx` do shadcn, usando as cores `--chart-1` a `--chart-8`. Os gráficos
próprios do projeto estão em `components/charts.tsx`.

| Token | Cor (claro) | Papel típico |
|---|---|---|
| `chart-1` | esmeralda `#059669` | Série principal; ingrediente mais usado; efeito positivo |
| `chart-2` | âmbar `#d97706` | 2ª série; marco de secagem |
| `chart-3` | azul `#2563eb` | 3ª série |
| `chart-4` | vermelho `#dc2626` | Efeito negativo; marco de parto |
| `chart-5` a `chart-8` | violeta, ciano, lima, rosa | 5ª a 8ª série |
| `chart-dim` | esmeralda apagado `#a7d9c6` | Tudo o que não é o dado de interesse |

### Gráficos por saída

| Saída | Gráfico | Destaque |
|---|---|---|
| Margem por cenário (sensibilidade) | Barras verticais (`HighlightBars`) | Cenário ótimo vivo; linha tracejada do base |
| Distribuição das margens | Histograma | Marcas do base e do ótimo |
| Efeito dos fatores | Tornado (`DivergingBars`) ordenado por \|ρ\| | Maior efeito; eixo fixo de −1 a +1 |
| Margem × fator | Dispersão (`ScatterPlot`) | Ponto ótimo em verde vivo |
| Leite, custo da ração | Áreas e linhas no tempo (`TimeSeries`) | Marcos do RuFaS (PEV, secagem, parto) |
| Exigência × consumo | Linhas, dois eixos | NEL e DMI à esquerda (Mcal e kg), proteína metabolizável à direita (g) |
| Ração média | Barras horizontais ordenadas | Maior participação em verde vivo |
| Ração por intervalo | Áreas empilhadas (`TimeSeries`) | Uma cor por alimento; no máximo 8 faixas (os menores somam-se em "Outros", em cinza); o balão lista de cima para baixo, com 2 casas decimais e o total |
| Balanço nutricional | Barras divergentes em % da exigência | Déficit em vermelho |
| Verificações V1 a V5 | `Bullet` contra as faixas ok, atenção e alerta | Estado; o valor também em texto |
| Ranking de dietas | `ToneBars` de custo | Melhor viável viva; inviáveis em vermelho; linha da dieta ótima |
| Erro de linearização | `ToneBars` por restrição com a linha da tolerância | Acima da tolerância |
| Dieta ótima × RuFaS | `ShareBars` a 100% e `ScatterPlot` por execução com a linha do LP | O LP |
| Curva de lactação | Linhas com marcos e faixas | Marcos em esmeralda (PEV), âmbar (secagem) e vermelho (parto) |
| Mini gráfico dos indicadores | `Sparkline` | Série da própria simulação (intervalos de 30 dias, leite diário) |

Regras gerais: eixo com unidade ou título quando a unidade não é óbvia; dica (_tooltip_) com valores ao passar o
mouse; legenda só quando há mais de uma série (fora do gráfico, `SeriesLegend`); cor nunca é o único canal (marcos
têm rótulo de texto e as células de calor mostram o número); barras sempre começam em zero; as linhas usam escala
automática. Os traços do eixo vão de 1, 2 ou 5 vezes uma potência de 10 (0, 10, 20, 30...), calculados em
`web/src/lib/scale.ts`. Eixos de valores em US$ aparecem em milhares ("450 mil") para não quebrar a linha, e os
rótulos e balões mostram o valor inteiro. As linhas de referência estendem o eixo, então a tolerância (1%) aparece
mesmo quando todos os erros são menores.

## Padrões de Interação e Conteúdo

### Tarefas longas

Simulações, sensibilidades e otimizações são tarefas em segundo plano: o botão mostra o progresso ("n de N"), o
usuário pode trocar de tela sem perder a tarefa e acompanha pelo menu **Tarefas**; o resultado fica no estado
compartilhado e no histórico do servidor. O servidor executa uma tarefa por vez. A consulta do estado ocorre a cada
1,5 s (`lib/api.ts`, `runJob`).

### Formulários

Campos numéricos aceitam vazio durante a edição; antes de enviar, valores inválidos são trocados por um padrão
(`finite()`); nenhuma validação bloqueia o usuário a cada tecla. A validação final está no servidor.

### Conteúdo

- Idioma: português do Brasil; números no formato brasileiro (`Intl.NumberFormat`).
- Moeda: "US$"; massa em kg; energia em Mcal; proteína metabolizável em g.
- Termos técnicos mantêm a sigla e, na primeira ocorrência, o significado (PEV, NEL, DMI, MS).
- Mensagens dizem o que aconteceu e o que fazer ("Selecione pelo menos 3 alimentos (um volumoso, um concentrado e um
  mineral).").
- Preços e valores de exemplo são sempre apresentados como ilustrativos.

## Acessibilidade

### O que está implementado

| Item | Situação |
|---|---|
| Idioma do documento declarado (`lang='pt-BR'`) | Sim |
| Rótulos acessíveis em campos (`aria-label` ou `<label>`) | Sim, inclusive em campos dentro de tabelas e cartões |
| Botões só com ícone têm nome acessível (`Remover…`, `Alternar tema…`, `Ver como tabela`) | Sim |
| Alternância gráfico/tabela como grupo de rádio rotulado (`role='radiogroup'`) | Sim |
| Mapa de restrições com símbolo e texto para leitor de tela além da cor | Sim |
| Navegação por teclado e foco visível | Herdados do shadcn/Base UI (anel de foco); não foram testados por teclado nesta versão |
| Atalhos `Ctrl/Cmd + B` (barra lateral) e `Ctrl/Cmd + K` (busca) | Sim |
| Cor não é o único canal de informação | Sim (rótulos, números, símbolos e selos de texto) |
| Respeito ao tema | Escuro por padrão, com alternância; não segue o sistema operacional ao abrir pela primeira vez |

### Contraste medido (WCAG 2.1; mínimo 4,5:1 para texto normal, 3:1 para texto grande e elementos gráficos)

Razões calculadas em 16/11/2026 a partir dos tokens hexadecimais atuais:

| Par | Claro | Escuro |
|---|---|---|
| Texto sobre fundo | 16,8 | 18,0 |
| Texto sobre cartão | 18,2 | 16,9 |
| Texto secundário sobre cartão | 5,5 | 6,0 |
| Texto secundário sobre fundo | 5,0 | 6,4 |
| Texto sobre botão primário | 16,6 | 18,0 |
| Texto sobre botão `brand` | 3,8 | 7,5 |
| `brand` como texto sobre cartão | 3,8 | 7,3 |
| Destrutivo sobre cartão | 4,8 | 4,9 |
| `warning-text` sobre cartão | 5,0 | 11,1 |
| Azul (`info`) sobre cartão | 5,2 | 5,0 |
| Violeta sobre cartão | 5,7 | 4,4 |
| Selo `secondary` (texto `brand` sobre esmeralda a 12%) | 3,3 | 6,1 |
| Selo `warning` (`warning-text` sobre âmbar a 12%) | 4,4 | 9,1 |
| Selo `destructive` (vermelho sobre vermelho a 12%/15%) | 4,0 | 4,3 |
| Texto sobre mapa de calor, no máximo (40%) | 13,0 | 4,7 |

Contraste das cores de gráfico contra o cartão (elementos gráficos, mínimo de 3:1):

| Cor | Claro | Escuro |
|---|---|---|
| `chart-1` esmeralda | 3,8 | 7,3 |
| `chart-2` âmbar | 3,2 | 8,6 |
| `chart-3` azul | 5,2 | 5,0 |
| `chart-4` vermelho | 4,8 | 4,9 |
| `chart-5` violeta | 5,7 | 4,4 |
| `chart-6` ciano | 3,7 | 7,6 |
| `chart-7` lima | 3,1 | 9,4 |
| `chart-8` rosa | 4,6 | 5,2 |
| `chart-dim` (apagado, de propósito) | 1,6 | 2,0 |

### Problemas encontrados e corrigidos

| Problema | Antes | Correção |
|---|---|---|
| Texto de "leite perdido" no tema escuro usava a cor de primeiro plano do aviso (escura) | 1,7:1 | Token `warning-text` |
| Células de calor no máximo (50%) com texto branco, no tema escuro | 3,9:1 | Teto de 40% (4,7:1 no escuro; 13,0:1 no claro) |

### Lacunas conhecidas

- **No tema claro, o esmeralda como texto pequeno não atinge 4,5:1** (3,8:1 sobre o cartão; 3,3:1 no selo `secondary`;
  3,8:1 no texto do botão `brand`). Nos valores grandes dos indicadores (24 px, extra-bold) o mínimo de 3:1 é atendido.
  No tema escuro, que é o padrão, todos esses pares passam.
- Os selos `destructive` (4,0 e 4,3) e `warning` no claro (4,4) ficam pouco abaixo de 4,5:1.
- Entre as cores de gráfico, `chart-2` (3,2) e `chart-7` (3,1), no tema claro, passam de 3:1 por pouco; `chart-dim` é
  apagada de propósito e sempre vem com rótulo ou valor.
- Não foi feita auditoria com leitor de tela nem com ferramenta automatizada (axe, Lighthouse), e a cor das séries não
  foi validada para daltonismo.
- Os gráficos do Recharts não têm descrição alternativa em texto; a alternância "ver como tabela" dá os mesmos dados.
- Algumas dicas dependem de passar o mouse (nomes completos nas colunas de tabela).

## Responsividade

| Largura | Comportamento |
|---|---|
| ≥ 1.536 px | Indicadores da Vaca leiteira em 3 colunas; pares de gráficos lado a lado |
| ≥ 1.280 px | Sidebar fixa; parâmetros fixos à esquerda (24 rem) e resultados à direita |
| 768 a 1.279 px | Sidebar vira gaveta; parâmetros no topo, em coluna única; botão de executar em barra fixa na parte de baixo |
| ≥ 640 px | Margens de 24 px; título da página em 30 px; indicadores em 2 colunas |
| < 640 px | Indicadores em 1 coluna; padding de cartão de 20 px; tabelas rolam na horizontal |

O ponto de corte da sidebar e da barra fixa é 1.280 px (`MOBILE_BREAKPOINT` em `hooks/use-mobile.ts` e prefixo `xl:`).
**Verificado:** 1.440 px e cerca de 540 px no navegador embutido; 800 px nas telas dos guias. **Não verificado:**
tablets, celulares reais e telas acima de 1.600 px.

## Arquitetura e Origem

### Origem: o template AdminCN

**AdminCN Free 1.0.0** (shadcn/studio, MIT): painel administrativo com Next.js, React, Tailwind CSS v4, shadcn/ui
(estilo `base-vega`, sobre Base UI), Recharts e ícones Lucide. Vinha com páginas de pedidos, e-mail, calendário,
usuários, autenticação, formulários e tabelas, 42 componentes de interface e um tema neutro em cinza. Foi adaptado com
exportação estática (`output: 'export'`); o servidor Python serve o resultado.

| Categoria | Itens |
|---|---|
| **Reaproveitado (adaptado)** | Estrutura da tela (sidebar recolhível + cabeçalho + conteúdo + rodapé); componentes de `ui/`; sistema de tokens de cor em CSS; modo claro e escuro com `next-themes`; escala de raio e tipografia. |
| **Alterado** | Paleta (cinza → escuro com acento esmeralda, 5 → 8 cores de gráfico); idioma (pt-BR); sidebar flutuante com 6 destinos; barra superior em pílula com busca, tarefas e estado da conexão; fonte Geist via pacote `geist`; hook `use-mobile` (D7). |
| **Removido** | Páginas de demo; banco falso (`fake-db`); rotas de API e _server actions_; redirecionamentos do `next.config`; botão de estrelas do GitHub; botão de download; links promocionais; menu de perfil e de idioma; componentes de UI sem uso; 9 dependências (nuqs, react-hook-form, @hookform/resolvers, zod, @tanstack/react-table, cmdk, input-otp, date-fns, react-resizable-panels). |
| **Criado** | As 6 telas, o estado compartilhado, o cliente da API, o seletor de alimentos, os indicadores, o botão de executar, o cartão de gráfico, a paleta de comandos, o menu de tarefas, o histórico de execuções e os gráficos do domínio. |

O template tinha 269 arquivos e 22 dependências; a interface atual tem 84 arquivos de código (cerca de 11.500 linhas) e
14 dependências de produção.

### Fluxo de construção

```
 web/  (fontes: Next.js + React + Tailwind v4 + shadcn/ui)
   │  scripts/build-web.ps1
   │    1. copia as fontes para %LOCALAPPDATA%\dietopt-web-build
   │    2. npm install  e  npm run build   (exportação estática)
   │    3. publica out/ em frontend/
   ▼
 frontend/  (HTML + CSS + JS estáticos, cerca de 3,3 MB)
   │  servido por backend/dietopt/server.py  (http://127.0.0.1:8000)
   ▼
 /api/*  (JSON): alimentos, preços, simulação, sensibilidade, avaliação, histórico, tarefas
```

Quem só **usa** o sistema não precisa de Node; só quem **altera a interface** precisa de Node 20.9 ou superior. A
primeira versão da interface (HTML puro com Chart.js) ficou em `frontend_legacy/`.

### Pilha

| Camada | Tecnologia | Versão |
|---|---|---|
| Framework | Next.js (App Router, exportação estática, Turbopack) | 16.2.6 |
| UI | React | 19.2.4 |
| Estilo | Tailwind CSS (tokens em CSS) e `tw-animate-css` | 4 / 1.4.0 |
| Componentes | shadcn/ui sobre Base UI | `@base-ui/react` 1.6.0 |
| Gráficos | Recharts, via wrapper `chart.tsx` do shadcn | 3.8.0 |
| Ícones | Lucide | 1.24.0 |
| Tema | next-themes | 0.4.6 |
| Avisos | Sonner | 2.0.7 |
| Fonte | Geist Sans e Geist Mono (variáveis) | `geist` 1.7.2 |
| Linguagem | TypeScript, modo estrito | 5.9.3 |

### Estado

Um único `AppProvider` (`providers/AppProvider.tsx`) vive no layout raiz; por isso os dados **sobrevivem à
navegação** entre telas.

| Estado | Para que serve |
|---|---|
| `feeds`, `defaults`, `connection` | Biblioteca de alimentos, preços e preço do leite iniciais, estado da conexão |
| `selected`, `params` | Alimentos escolhidos (preço, mínimo e máximo em kg MS/vaca/dia) e parâmetros (preço do leite, período, redução máxima) |
| `sim`, `simKey`, `sens`, `sensKey`, `sensSetup` | Último resultado de simulação e de sensibilidade, as chaves que detectam resultado desatualizado e a configuração da sensibilidade |
| `moduleState` | Entradas e resultados da avaliação de dietas (Ruminante Singular) |
| `tasks`, `trackTask` | Tarefas em andamento, mostradas no menu **Tarefas** |
| `cowScenario`, `loadCowScenario` | Salvar e abrir cenários em arquivo |

### Contrato com a API

A lista de rotas, corpos e respostas está em [DOMINIO.md](DOMINIO.md) (seção 5.10) e no [FSD](FSD.md). Os tipos
TypeScript dos contratos estão em `web/src/lib/types.ts`; o cliente, em `web/src/lib/api.ts`.

## Persistência e Privacidade

| Tema | Detalhe |
|---|---|
| `localStorage` | `dietopt.v1` (alimentos selecionados e parâmetros) e `theme` (next-themes). Local ao navegador. |
| Servidor | O histórico de execuções fica em arquivos em `runs/_history` (decisão de produto D14); resultados de simulação ficam em `runs/` |
| Cookie | `sidebar_state` (estado da barra lateral, vem do template), 7 dias. |
| Dados enviados | Só para `127.0.0.1` (servidor local). Sem rastreamento, sem serviços externos em tempo de execução. |
| Tamanho | `frontend/` ocupa cerca de 3,3 MB (HTML, JS, CSS e fontes); funciona sem internet. |
| Pré-carregamento | O Next.js pré-carrega as outras rotas; o servidor responde a `HEAD` e mapeia os arquivos `*.__PAGE__.txt` (D8). |

## Decisões de Design

| ID | Decisão | Motivo | Alternativa descartada |
|---|---|---|---|
| D1 | Adaptar o template com **exportação estática** e servi-lo pelo servidor Python | Mantém a execução local simples (sem Node em tempo de uso) e reaproveita o back-end | Rodar um servidor Node junto, com duas portas e dois processos |
| D2 | Reescrever o nav, o cabeçalho e as páginas; **não** manter as páginas do demo | O demo tem e-mail, calendário e autenticação sem relação com o produto | Esconder as páginas do demo |
| D3 | Acento **esmeralda** sobre fundo escuro, botão primário claro | Identidade agropecuária, distinta do cinza do template; o destaque verde fica para o dado de interesse | Manter o tema neutro; botão primário verde |
| D4 | Recharts via wrapper do shadcn, no lugar de Chart.js | Já vem no template e integra com os tokens de cor e o tema | Manter o Chart.js |
| D5 | Estado em um `AppProvider` único | Dados sobrevivem à navegação, sem biblioteca de estado | Redux, Zustand ou estado por página |
| D6 | Build **fora do OneDrive** (`%LOCALAPPDATA%`) | Evita sincronizar centenas de MB de `node_modules` e o problema do "Á" no caminho | `node_modules` dentro do projeto |
| D7 | Corrigir `use-mobile` para medir a janela só **depois da montagem** | O original lia `window` no estado inicial, divergindo do HTML estático (erro de hidratação #418) | Desabilitar o aviso do React |
| D8 | Mapear no servidor `…__next.rota.__PAGE__.txt` → `…__next.rota/__PAGE__.txt` | No Windows o export grava com pasta e o navegador pede com ponto; evita 404 e perda de pré-carregamento | Desligar o pré-carregamento |
| D9 | Limite de 40% no mapa de calor e token `warning-text` | Contraste medido abaixo de 4,5:1 | Manter os valores do protótipo |
| D10 | Fonte via pacote `geist` | Funciona sem rede e sem baixar do Google no build | `next/font/google` |
| D11 | Guardar a interface antiga em `frontend_legacy/` | Permite voltar atrás e comparar resultados | Apagar |
| D12 | Selecionar alimentos com busca e lista de caixas, não com caixa combinada (`Combobox`) | 130 itens com 3 dados de apoio cada; a lista mostra tipo, PB, FDN e NEL de uma vez | Combobox do template |
| D13 | **Execução = qualquer execução** (simulação, sensibilidade, avaliação de dietas e dieta ótima), num histórico único com o tipo numa coluna | Um só lugar para consultar, comparar e repetir | Um histórico por tela |
| D14 | Histórico em **arquivos no servidor** (`runs/_history`), ao lado do cache do RuFaS | Sobrevive a recarregar a página e a reiniciar o servidor | `localStorage` do navegador |
| D15 | **Cenário-base = o que o usuário marcar** (estrela); sem marcação, a primeira execução do histórico. A comparação só vale com o mesmo período (e, nos totais do rebanho, o mesmo rebanho e anos) | A margem cresce com os anos; comparar períodos diferentes engana | Base fixo ou sempre a última execução |
| D16 | Mini gráfico dos indicadores = **série da própria simulação** (intervalos de 30 dias, leite diário) | Existe desde a primeira execução, sem depender de histórico | Tendência entre execuções |
| D17 | Sem avatar (não há login): entra o estado da conexão; "notificações" viram **Tarefas**; a busca `Ctrl K` é uma paleta de comandos | Adaptar a referência visual ao que o sistema tem | Manter os elementos da referência |
| D18 | Barra de execução fixa na parte de baixo da tela abaixo de 1.280 px | O botão de executar fica sempre ao alcance, mesmo com o painel de parâmetros rolando | Botão só no fim do painel |
| D19 | Tema escuro por padrão, com alternância para o claro | Leitura de números em tela por períodos longos; é a linguagem visual da referência escolhida | Seguir sempre o sistema operacional |

## Limitações

Estado atual, sem propostas:

1. **Sem testes automatizados de interface.** A verificação é manual (6 telas, tema claro e escuro, simulações
   reais); o back-end tem 261 testes.
2. **Acessibilidade parcial** (seção _Acessibilidade_): contraste do esmeralda como texto pequeno no tema claro abaixo
   de 4,5:1; sem auditoria automatizada nem leitor de tela; gráficos sem texto alternativo próprio.
3. **Telas pequenas pouco exercitadas:** o layout estreito foi visto em poucas larguras; tabelas de cenários exigem
   rolagem horizontal.
4. **A seleção de alimentos mostra só os 60 primeiros resultados** da busca; é preciso refinar o termo para ver os
   demais.
5. **Uma tarefa por vez** no servidor: se duas abas disparam simulações, a segunda espera na fila. Não há botão
   Cancelar para a simulação em andamento.
6. **O mapeamento do pré-carregamento é um contorno** de um comportamento do export do Next.js no Windows; pode deixar
   de ser necessário em versões futuras.
7. **Código herdado do template** (sidebar, wrapper de gráficos) é extenso e não foi revisado linha a linha; foi
   mantido sem alterações de comportamento, exceto o hook `use-mobile`.
8. **Cor de série nos gráficos não foi validada para daltonismo**; `chart-2` e `chart-7` ficam perto do mínimo de 3:1
   no tema claro.
9. **Fonte monoespaçada, animação `heartbeat` e componente `JobProgress`** estão definidos mas sem uso nas telas.
10. **Os guias (`docs/guias/`) mostram o visual da data em que foram feitos**; uma mudança de tela exige regenerar as
    figuras.

## Licenças

| Componente | Licença | Observação |
|---|---|---|
| AdminCN Free (shadcn/studio) | MIT | Aviso em `web/LICENSE-TEMPLATE.md`; crédito no rodapé e na tela de premissas |
| Next.js, React, Recharts, Tailwind CSS, Base UI, shadcn, next-themes, Sonner, tw-animate-css | MIT | Dependências do `package.json` |
| Lucide | ISC | Ícones |
| class-variance-authority | Apache-2.0 | Variantes de estilo |
| Geist (fonte) | SIL Open Font License | Pacote `geist` |
| RuFaS | GPLv3 | Usado sem modificações como simulador; ver o PRD |

## Manutenção

| Tarefa | Passos |
|---|---|
| **Instalar e compilar** | `powershell -ExecutionPolicy Bypass -File scripts\build-web.ps1` (cria a pasta de build, instala, compila e publica em `frontend/`). |
| **Desenvolver com recarga automática** | Em `%LOCALAPPDATA%\dietopt-web-build`, `npm run dev -- -p 3001`; as chamadas `/api/*` são encaminhadas ao servidor Python em `127.0.0.1:8000` (precisa estar de pé). Editar sempre em `web/` e sincronizar com o script. |
| **Adicionar uma tela** | Criar `web/src/views/XView.tsx`, `web/src/app/x/page.tsx` e registrar a rota em `components/layout/nav.ts`. |
| **Adicionar um componente do shadcn** | Copiar o arquivo de `components/ui/` do template (ou gerar com a CLI do shadcn) e importar só o que usar. |
| **Mudar uma cor** | Editar o token em `web/src/app/globals.css` (claro e escuro), atualizar o Apêndice A e o front matter deste arquivo, e refazer a conferência de contraste. |
| **Chamar um novo endpoint** | Tipar a resposta em `lib/types.ts`, expor em `lib/api.ts` e usar na _view_. |

---

## Apêndice A: tokens de cor

Valores de `web/src/app/globals.css`.

| Token | Claro | Escuro |
|---|---|---|
| `--background` | `#F5F6F4` | `#0A0B0D` |
| `--foreground` | `#12161A` | `#F3F5F6` |
| `--card` | `#FFFFFF` | `#111417` |
| `--popover` | `#FFFFFF` | `#14181C` |
| `--surface` | `#F0F2EF` | `#171B1F` |
| `--primary` / `--primary-foreground` | `#12161A` / `#F3F5F6` | `#F3F5F6` / `#0A0B0D` |
| `--secondary`, `--muted`, `--accent` | `#EEF0EE` | `#1A1F24` |
| `--muted-foreground` | `#5F6B76` | `#8B949E` |
| `--destructive` | `#DC2626` | `#EF4444` |
| `--border` | `#E3E6E2` | `rgb(255 255 255 / 7%)` |
| `--input` | `#D5DAD6` | `rgb(255 255 255 / 12%)` |
| `--ring`, `--brand` | `#059669` | `#10B981` |
| `--brand-foreground` | `#FFFFFF` | `#04130D` |
| `--brand-dim`, `--chart-dim` | `#A7D9C6` | `#14513F` |
| `--success` | `#059669` | `#10B981` |
| `--warning` / `--warning-text` | `#D97706` / `#B45309` | `#F59E0B` / `#FBBF24` |
| `--info` | `#2563EB` | `#3B82F6` |
| `--violet` | `#7C3AED` | `#8B5CF6` |
| `--chart-1` | `#059669` | `#10B981` |
| `--chart-2` | `#D97706` | `#F59E0B` |
| `--chart-3` | `#2563EB` | `#3B82F6` |
| `--chart-4` | `#DC2626` | `#EF4444` |
| `--chart-5` | `#7C3AED` | `#8B5CF6` |
| `--chart-6` | `#0891B2` | `#06B6D4` |
| `--chart-7` | `#65A30D` | `#84CC16` |
| `--chart-8` | `#DB2777` | `#EC4899` |
| `--sidebar` | `#FFFFFF` | `#0D0F11` |
| `--radius` | `0.75rem` | `0.75rem` |

## Apêndice B: mapa de arquivos

```
web/
├─ package.json, package-lock.json     dependências (14 de produção)
├─ next.config.ts                       exportação estática; encaminha /api em desenvolvimento
├─ tsconfig.json, postcss.config.mjs, components.json
├─ LICENSE-TEMPLATE.md                  aviso de copyright do template (MIT)
└─ src/
   ├─ app/
   │  ├─ layout.tsx                     raiz: fontes, tema (escuro por padrão), sidebar, estado
   │  ├─ globals.css                    tokens de cor, raio e utilitários
   │  ├─ page.tsx, vaca/, curva/, sensibilidade/, execucoes/, sobre/   rotas finas
   │  └─ not-found.tsx
   ├─ views/                            ExerciseView, ModuleView, CowView, CurveView, SensitivityView, HistoryView, AboutView
   │  └─ cow/, history/, module/, sensitivity/   partes de cada tela
   ├─ components/
   │  ├─ layout/                        AppShell, AppSidebar, Header, Footer, ModeToggle, CommandPalette, TasksMenu, nav.ts
   │  ├─ ui/                            21 componentes do shadcn
   │  ├─ charts.tsx, shared.tsx         gráficos do domínio; PageHeader, KpiCard, NumberInput etc.
   │  ├─ ChartCard, EmptyState, ExportButtons, FeedPicker, PriceImport, RunButton, ScenarioFile, Segmented, ThemeProvider
   ├─ providers/AppProvider.tsx         estado compartilhado
   ├─ hooks/use-mobile.ts               largura da janela (corrigido)
   └─ lib/                              api, cycle, download, format, herd, history, scale, sensitivity, types, utils
scripts/build-web.ps1                   build e publicação em frontend/
frontend/                               interface publicada (gerada; não editar)
frontend_legacy/                        primeira versão da interface (HTML puro)
docs/guias/                             guias em Word, um por tela
docs/arquivo/                           registro histórico (roteiros já concluídos)
```

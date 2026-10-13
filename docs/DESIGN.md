---
name: Dieta Ótima com RuFaS
colors:
  background:         '#ffffff'
  foreground:         '#0a0a0a'
  card:               '#ffffff'
  secondary:          '#f5f5f5'
  border:             '#e5e5e5'
  ring:               '#a1a1a1'
  muted-foreground:   '#737373'
  primary:            '#0c6944'
  primary-foreground: '#fafafa'
  destructive:        '#e7000b'
  success:            '#007d50'
  warning:            '#df911a'
  warning-text:       '#915200'
  chart-1:            '#007d50'
  chart-2:            '#df911a'
  chart-3:            '#1f74bf'
  chart-4:            '#da404e'
  chart-5:            '#8254c4'
  chart-6:            '#0f9293'
  chart-7:            '#8b8c27'
  chart-8:            '#d14e95'
colors-dark:
  background:         '#0a0a0a'
  foreground:         '#fafafa'
  card:               '#171717'
  secondary:          '#262626'
  border:             'branco a 10%'
  ring:               '#737373'
  muted-foreground:   '#a1a1a1'
  primary:            '#2fc183'
  primary-foreground: '#010f07'
  destructive:        '#ff6467'
  success:            '#2fc183'
  warning:            '#f5ae39'
  warning-text:       '#f0ba59'
  chart-1:            '#2fc183'
  chart-2:            '#f5ae39'
  chart-3:            '#53a3f2'
  chart-4:            '#f66b71'
  chart-5:            '#ae84f2'
  chart-6:            '#53c2c1'
  chart-7:            '#afbb52'
  chart-8:            '#f47db9'
typography:
  font-principal: Geist Sans (variável)
  font-mono: Geist Mono (variável, reservada; sem uso atual)
  body-base:
    fontSize: 16px
  texto-apoio:
    fontSize: 14px
  page-title:
    fontSize: 24px
    fontWeight: '600'
    letterSpacing: -0.025em
  card-title:
    fontSize: 16px
    fontWeight: '500'
  kpi-valor:
    fontSize: 24px
    fontWeight: '600'
    fontVariantNumeric: tabular-nums
  label-secao:
    fontSize: 12px
    textTransform: uppercase
    letterSpacing: 0.05em
  campo-compacto:
    fontSize: 11px
rounded:
  DEFAULT: 10px
  sm: 6px
  md: 8px
  lg: 10px
  xl: 14px
spacing:
  margem-pagina: 16px (24px a partir de 640px)
  espaco-vertical-pagina: 24px
  gap-blocos: 24px
  gap-indicadores: 12px
  padding-card: 24px
  padding-card-sm: 16px
  altura-campo-numerico: 32px
  altura-botao: 36px (sm 32px, xs 24px)
largura-conteudo-max: 1440px
largura-barra-lateral: 256px (aberta), 48px (ícones), 288px (gaveta no celular)
largura-painel-lateral: 368px
---

## Contexto

Este documento descreve o padrão visual **atualmente implementado** na interface web do Dieta Ótima com RuFaS
(`web/`, publicada em `frontend/`). A interface é um site estático gerado pelo Next.js a partir do template
AdminCN (shadcn/ui), servido pelo servidor Python local. Todos os tokens vivem em `web/src/app/globals.css`; os
componentes usam classes do Tailwind e variantes do shadcn/ui, e não há CSS espalhado por componente.

Este arquivo reflete o que existe hoje no código. Não contém propostas de redesign. As lacunas conhecidas estão na
seção _Limitações_.

**Versão do documento:** 0.2 (reescrito sobre a estrutura do modelo de DESIGN.md anexado) · **Data:** 12/10/2026 ·
**Autor(es):** _[a preencher]_ · **Relacionado:** [PRD](PRD.md)

**Estrutura.** As nove primeiras seções (Contexto a Estados do Sistema) seguem o modelo. As seguintes foram
acrescentadas porque o produto tem telas, gráficos e uma origem em template que o modelo não cobre: _Telas_,
_Visualização de Dados_, _Padrões de Interação e Conteúdo_, _Acessibilidade_, _Responsividade_, _Arquitetura e
Origem_, _Persistência e Privacidade_, _Decisões de Design_, _Limitações_, _Licenças_, _Manutenção_ e dois apêndices.

## Brand & Estilo

A interface é um **painel analítico de uso desktop** para nutricionistas, produtores de leite e para o professor que
avalia a modelagem. O estilo é **claro por padrão, sóbrio e orientado a dados**: fundo branco (ou quase preto no
tema escuro), cartões com borda fina, cinzas neutros e **uma única cor de marca, o verde**. A prioridade é ler
números com unidade, comparar cenários e perceber quando o modelo alterou algo por conta própria; ornamento é mínimo.

A cor tem função: verde para ação, destaque e efeito positivo; âmbar para aviso do modelo (leite perdido); vermelho
para erro, inviabilidade e efeito negativo. O verde foi escolhido pelo domínio agropecuário e para distinguir o
produto do cinza do template, sem competir com as cores dos gráficos.

### Princípios

| # | Princípio | O que significa na prática |
|---|---|---|
| P1 | **Mostrar a unidade sempre** | Todo número tem unidade visível (US$/kg MS, kg MS/vaca/dia, Mcal/dia). Valores em formato pt-BR. |
| P2 | **Não esconder o que o modelo fez** | Falhas aparecem como "falhou"; leite reduzido pelo RuFaS aparece como "leite perdido", com alerta. Nunca um zero silencioso. |
| P3 | **Rotular o que é ilustrativo** | Preços iniciais não são cotações: o aviso está no rodapé, na tela de premissas e nos textos de apoio. |
| P4 | **Resultado primeiro** | Na tela de simulação, a margem e os indicadores aparecem no topo; os detalhes (ração, exigências, leite) vêm depois. |
| P5 | **Tarefa longa com progresso** | Simulações levam de 30 s a vários minutos: a tela mostra progresso, não trava e permite continuar navegando. |
| P6 | **Um sistema, dois temas** | Claro e escuro com a mesma estrutura e contraste medido nos dois. |
| P7 | **Reuso antes de invenção** | Componentes do shadcn/ui; só se cria algo novo quando não existe equivalente. |

## Cores

Tokens em `oklch`, definidos em `web/src/app/globals.css` e expostos ao Tailwind (`bg-primary`,
`text-muted-foreground`, etc.). O front matter traz a **conversão para hexadecimal** (aproximada, para leitura); a
fonte de verdade é o `oklch` do [Apêndice A](#apêndice-a-tokens-de-cor).

- **Fundo e texto (`--background`, `--foreground`):** `#ffffff` / `#0a0a0a` no claro; `#0a0a0a` / `#fafafa` no escuro.
  Cor de base do `body`.
- **Cartão (`--card`):** `#ffffff` no claro, `#171717` no escuro (levemente mais claro que o fundo, para destacar a
  superfície). Também usado por `Alert`, `Sidebar` e _popovers_.
- **Secundária, apagada e de destaque (`--secondary`, `--muted`, `--accent`):** `#f5f5f5` / `#262626`. Fundo de
  _hover_, linhas alternadas e cabeçalhos de tabela.
- **Borda e campo (`--border`, `--input`):** `#e5e5e5` no claro; branco a 10% e 15% no escuro. Bordas de cartões,
  tabelas e campos.
- **Primária (`--primary`):** `#0c6944` (verde profundo) no claro, `#2fc183` (verde claro) no escuro. Botão principal,
  item ativo da barra lateral, margem em destaque, mapa de calor, ícone de marca. `--primary-foreground` é o texto
  sobre ela.
- **Sucesso (`--success`):** mesma família do verde; efeito positivo e confirmações.
- **Destrutiva (`--destructive`):** `#e7000b` / `#ff6467`. Erro, "inviável", "falhou", conexão perdida, efeito
  negativo.
- **Aviso (`--warning`, `--warning-text`):** âmbar `#df911a` / `#f5ae39` para fundo e contorno; `#915200` / `#f0ba59`
  para **texto** de aviso. Existem dois tokens porque o âmbar de fundo não tem contraste suficiente como texto. Usado
  no indicador "leite perdido" e no alerta de ração insuficiente.
- **Texto secundário (`--muted-foreground`):** `#737373` / `#a1a1a1`. Descrições, dicas, rótulos de campo.
- **Foco (`--ring`):** `#a1a1a1` / `#737373`; anel de foco dos componentes.
- **Gráficos (`--chart-1` a `--chart-8`):** oito cores com versão clara e escura (verde, âmbar, azul, rosa-vermelho,
  violeta, turquesa, oliva, rosa). Detalhes em _Visualização de Dados_.

O tema escuro **não é uma inversão**: cartões usam `oklch(0.205)` sobre fundo `oklch(0.145)`, e a cor primária, o
aviso e as cores de gráfico ficam mais claros para manter o contraste. O tema segue o sistema operacional por padrão
e pode ser trocado no cabeçalho.

## Tipografia

- **Fonte principal:** Geist Sans (variável), carregada pelo pacote `geist` com arquivos locais (sem Google Fonts).
- **Fonte monoespaçada:** Geist Mono está registrada (`--font-mono`), mas **não é usada** por nenhum componente atual.
- **Corpo base:** 16 px (padrão do navegador; o `body` não define tamanho). Descrições, tabelas e campos usam
  `text-sm` (14 px).
- **Título da página (`h1`):** 24 px (`text-2xl`), peso 600, `tracking-tight`.
- **Título de cartão:** 16 px (`text-base`), peso 500.
- **Texto de apoio:** 14 px, cor `--muted-foreground`; máximo de 48 rem de largura e `text-balance` no cabeçalho da
  página.
- **Rótulos pequenos e dicas:** 12 px (`text-xs`); 11 px (`text-[11px]`) em campos compactos de alimentos.
- **Título de seção dentro de cartão:** 12 px, caixa alta, `tracking-wider`, cor secundária.
- **Indicadores (`KpiCard`):** rótulo em 12 px, valor em 24 px peso 600, dica em 12 px.
- **Números:** `tabular-nums` (dígitos de largura fixa) em tabelas, campos numéricos e indicadores, para alinhar casas.
  Formato pt-BR (vírgula decimal, ponto de milhar).

## Layout & Espaçamento

- **Container:** conteúdo centralizado com `max-w-360` (**1.440 px**). Margens laterais de **16 px** (celular) e
  **24 px** (a partir de 640 px); 24 px de espaço vertical no topo e na base.
- **Estrutura da tela:** barra lateral recolhível + cabeçalho fixo + conteúdo + rodapé.

```
┌───────────────┬──────────────────────────────────────────────────────────────┐
│  Marca        │  ☰  Dieta Ótima › Página        [conectado · 130 alimentos] ☀ │  cabeçalho fixo
│               ├──────────────────────────────────────────────────────────────┤
│  ANÁLISE      │  Título da página                                            │
│   Exercício   │  Descrição                                                   │
│   Vaca        │  ┌──────────────┐ ┌─────────────────────────────────────┐   │
│   Curva       │  │  Painel de   │ │  Resultados (indicadores, gráficos) │   │
│   Sensibil.   │  │  parâmetros  │ │                                     │   │
│  PROJETO      │  └──────────────┘ └─────────────────────────────────────┘   │
│   Premissas   ├──────────────────────────────────────────────────────────────┤
│  RuFaS · NRC  │  Rodapé: RuFaS v1.0.6 (GPLv3) · NRC 2001 · preços ilustrativos │
└───────────────┴──────────────────────────────────────────────────────────────┘
```

- **Grades de conteúdo:**

| Padrão | Uso |
|---|---|
| Duas colunas iguais a partir de 1.280 px (`xl:grid-cols-2`) | Exercício do quadro |
| Painel lateral de 23 rem + resultados (`xl:grid-cols-[23rem_minmax(0,1fr)]`) | Vaca leiteira e Sensibilidade |
| Indicadores: 1 coluna (celular), 2 (≥ 640 px), 3 (≥ 1.280 px), 4 (≥ 1.536 px) | Resultados |
| Pares de gráficos lado a lado a partir de 1.536 px (`2xl:grid-cols-2`) | Composição × exigências; efeito × margem |

- **Espaçamento:** 24 px entre blocos (`gap-6`); 12 px entre indicadores; padding interno de cartão de 24 px
  (padrão) ou 16 px (`size='sm'`, usado nos indicadores).
- **Tabelas largas** rolam na horizontal dentro do cartão.

### Barra lateral

| Propriedade | Valor |
|---|---|
| Largura | 16 rem (aberta), 3 rem (só ícones), 18 rem (gaveta no celular) |
| Grupos | **Análise** (4 telas) e **Projeto** (1 tela) |
| Item ativo | Fundo `primary/10` e rótulo em destaque; a comparação ignora a barra final da rota |
| Recolher | Botão no cabeçalho ou `Ctrl/Cmd + B`; no modo ícones aparece dica (_tooltip_) com o nome |
| Rodapé | "RuFaS v1.0.6 · NRC 2001" (some no modo ícones) |
| Abaixo de 1.280 px | Vira gaveta (`Sheet`) aberta pelo botão do cabeçalho e fecha ao navegar |

### Cabeçalho

Botão da barra lateral, _breadcrumb_ de dois níveis ("Dieta Ótima › Página", oculto em telas muito estreitas),
indicador de conexão e botão de tema. O indicador tem três estados: _conectando…_, _conectado · N alimentos NRC_ e
_sem conexão com o servidor_ (destrutivo).

## Elevação & Profundidade

A hierarquia é construída por **camadas tonais** (fundo → cartão) e **bordas de 1 px**, não por sombra. Os cartões
usam um anel de 1 px (`ring-foreground/10`) e sombra mínima (`shadow-xs`); botões de contorno (`outline`) também têm
`shadow-xs`. Não há sombras maiores em cartões, painéis ou botões.

Há uma animação de pulso (`heartbeat`, com `box-shadow` que se expande e some) definida em `globals.css` e herdada
do template; nenhuma tela atual a usa. Camadas flutuantes (gaveta, _tooltip_, lista do `Select`) usam o estilo
padrão do shadcn.

## Formas (Border Radius)

Base `--radius: 0.625rem` (10 px) e derivados calculados em `globals.css`:

| Token | Fator | Valor |
|---|---|---|
| `sm` | 0,6× | 6 px |
| `md` | 0,8× | 8 px |
| `lg` | 1× | 10 px |
| `xl` | 1,4× | 14 px |

- **Cartões:** `rounded-xl` (14 px).
- **Botões e campos:** entre `md` e `lg` (8 a 10 px); botões `xs` e `sm` limitam o raio a 8 e 10 px.
- **Selos (`Badge`):** raio do tema.

## Componentes

### Do shadcn/ui

Em `web/src/components/ui/`, sobre Base UI, seguindo o código do template sem alterações de comportamento:
`Alert`, `Badge`, `Breadcrumb`, `Button`, `Card`, `Chart` (envolve o Recharts), `Checkbox`, `Input`, `Label`,
`Progress`, `Select`, `Separator`, `Sheet`, `Sidebar`, `Skeleton`, `Sonner` (avisos) e `Table`, `Tooltip`.

- **Botão (`Button`):** variantes `default` (fundo primário, texto `primary-foreground`, _hover_ a 80%), `outline`
  (borda e fundo do tema), `secondary`, `ghost`, `destructive` (fundo vermelho a 10% e texto vermelho) e `link`.
  Tamanhos `default` (36 px), `sm` (32 px), `xs` (24 px), `lg` (40 px) e versões `icon`. Nas telas aparecem `default`,
  `outline`, `ghost` e `secondary`, e o tamanho `sm`. O botão de executar leva o ícone `PlayIcon`.
- **Cartão (`Card`):** anel de 1 px, `rounded-xl`, padding de 24 px; `size='sm'` reduz para 16 px.
- **Campo (`Input`) e campo numérico (`NumberInput`):** ver abaixo; foco com anel (`ring-3`) e, em estado inválido,
  borda destrutiva.
- **Selo (`Badge`):** variantes `default`, `secondary`, `outline`, `ghost` e `link`; nas telas aparece como "mínimo
  ativo" / "máximo ativo" (`secondary`, exercício), origem dos parâmetros da curva (`outline`, verde se calibrados
  pelo RuFaS) e estado de conexão no cabeçalho.
- **Alerta (`Alert`):** variantes `default` e `destructive`; usado em "A ração não atendeu a todas as exigências"
  (tela da vaca). O "sem solução viável" do exercício é um bloco próprio (`border-destructive/40`,
  `bg-destructive/5`), não um `Alert`.
- **Progresso (`Progress`):** barra determinada ou indeterminada (valor nulo).
- **Esqueleto (`Skeleton`):** existe em `ui/`, mas nenhuma tela o usa hoje.
- **Aviso (`Sonner`):** _toast_ no tema do sistema, para sucesso e erro de tarefa.

### Do projeto

| Componente | Arquivo | Função |
|---|---|---|
| `AppShell`, `AppSidebar`, `Header`, `Footer`, `ModeToggle` | `components/layout/` | Estrutura da tela |
| `PageHeader` | `components/shared.tsx` | Título, descrição e ações da página |
| `KpiCard` | `components/shared.tsx` | Indicador com rótulo, valor grande e dica; tons `default`, `primary` e `warning` |
| `NumberInput` | `components/shared.tsx` | Campo numérico controlado (vazio vira `NaN`; ver `finite()`) |
| `JobProgress` | `components/shared.tsx` | Barra de progresso de tarefas, com texto "n de N simulações" e `aria-live` |
| `heat()` | `components/shared.tsx` | Cor de fundo proporcional ao valor, para tabelas de cenários |
| `FeedPicker` | `components/FeedPicker.tsx` | Busca, lista com caixas de seleção e cartões dos alimentos selecionados |
| `AppProvider` | `providers/AppProvider.tsx` | Estado compartilhado |

### Padrões dos componentes do projeto

- **`KpiCard`:** rótulo pequeno em cima, valor em 24 px peso 600, dica opcional embaixo. `primary` destaca a margem
  (fundo `primary/5`, anel `primary/30`, valor em verde); `warning` marca o leite perdido (fundo `warning/10`, anel
  `warning/40`).
- **`NumberInput`:** altura 32 px, texto à direita, dígitos tabulares. Aceita `aria-label`.
- **Cartão de alimento selecionado:** nome completo (quebra de linha, sem corte), três campos (`US$/kg MS`,
  `mín. kg/dia`, `máx. kg/dia`) com rótulos visíveis e botão de remover com nome acessível.
- **Mapa de calor (`heat`):** a célula usa de **8% a 40%** da cor primária (`color-mix` sobre transparente); o teto
  de 40% garante contraste de texto (seção _Acessibilidade_). Dependendo do campo, a escala pode ser invertida.
- **Selo de restrição ativa:** na tabela de nutrientes do exercício, o selo "mínimo ativo" e o preço-sombra
  identificam a restrição que limita o custo.
- **Ícones:** Lucide, 16 a 20 px, estilo de linha: `CalculatorIcon` (exercício), `MilkIcon` (vaca),
  `TrendingUpIcon` (curva), `SlidersHorizontalIcon` (sensibilidade), `InfoIcon` (premissas), `WheatIcon` (marca),
  `PlayIcon` (executar), `SearchIcon`, `PlusIcon`, `Trash2Icon`, `XIcon`, `SunIcon` e `MoonStarIcon`.

## Estados do Sistema (Erro / Sucesso / Aviso / Carregando)

O sistema usa cinco tratamentos distintos de estado, todos nos tokens de cor do tema:

| Estado | Cor base | Uso |
|---|---|---|
| **Sucesso** | Verde (`--success`, `--primary`) | Aviso "Simulação concluída." e "Análise concluída."; efeito positivo nos gráficos; indicador de conexão ativa |
| **Erro** | Vermelho (`--destructive`) | Bloco "Sem solução viável" e texto "inviável" nas linhas de cenário do exercício; "falhou" (causa na dica); aviso de erro de tarefa ou de rede; selo "sem conexão"; efeito negativo |
| **Aviso do modelo** | Âmbar (`--warning`, `--warning-text`) | Indicador "Leite perdido" e alerta "A ração não atendeu a todas as exigências" |
| **Carregando** | Primária + cinza | `Progress` com texto "n de N simulações do RuFaS concluídas" ou "Simulando no RuFaS…"; botão desabilitado "Simulando…" |
| **Vazio** | Cinza (`--muted-foreground`) | Texto orientando a próxima ação (por exemplo, "Clique em “Resolver”." no exercício; na tela da vaca, texto e ícone) |

### Padrões de feedback

| Situação | Padrão |
|---|---|
| Sucesso de tarefa | Aviso breve (_toast_) |
| Erro de tarefa ou de rede | Aviso com a primeira linha da mensagem; detalhe completo em `runs/<id>/console.log` |
| Problema de dados (inviável, falhou) | Dentro da tabela ou do bloco, em cor destrutiva (a causa de "falhou" fica na dica) |
| Alerta de modelo (leite perdido) | Indicador âmbar e alerta no topo dos resultados |
| Sem conexão | Selo vermelho no cabeçalho e botões de execução desabilitados |

A cor **nunca é o único canal**: os estados também têm texto ("falhou", "inviável", "leite perdido") ou número.

## Telas

Cinco telas, uma por rota. As páginas em `app/*/page.tsx` apenas renderizam a _view_ correspondente.

| Rota | Tela | Arquivo |
|---|---|---|
| `/` | Exercício do quadro | `views/ToyView.tsx` |
| `/vaca/` | Vaca leiteira (RuFaS) | `views/CowView.tsx` |
| `/curva/` | Curva de lactação | `views/CurveView.tsx` |
| `/sensibilidade/` | Sensibilidade (RuFaS) | `views/SensitivityView.tsx` |
| `/sobre/` | Premissas e limites | `views/AboutView.tsx` |

### Exercício do quadro (`/`)

**Objetivo:** reproduzir e explorar o problema de dieta de custo mínimo (PL).

| Bloco | Conteúdo |
|---|---|
| Problema | Tabela de alimentos (nome, custo, carboidrato, proteína; botão "+ Alimento" e remover) e tabela de nutrientes (mínimo e máximo); botão **Resolver** |
| Solução ótima | Indicadores (custo mínimo, alimentos usados); tabela de quantidades e custos; tabela de nutrientes com a restrição ativa (selo "mínimo ativo") e o preço-sombra; gráfico de barras |
| Cenários e sensibilidade | Dois fatores (alvo, de, até, níveis) e **Gerar cenários**; tabela `S1…SN` com a coluna `Res` em mapa de calor e a dieta ótima de cada linha |

**Estados:** resolve sozinho na primeira visita; _inviável_ aparece como bloco destrutivo ("Sem solução viável."); erro de rede vira aviso
(_toast_); fatores repetidos geram aviso ("Escolha dois fatores diferentes."). Valores iniciais: arroz (US$ 1,50;
0,77; 0,08), milho (US$ 2,23; 0,66; 0,14); carboidrato 6,0 a 9,5 kg; proteína 0,9 a 1,6 kg. Resultado esperado:
US$ 15,35/dia.

### Vaca leiteira (`/vaca/`)

**Objetivo:** simular com o RuFaS e ver ração, custo, leite e margem.

| Bloco | Conteúdo |
|---|---|
| Painel de cenário (esquerda, 23 rem) | Preço do leite; período (1 ou 2 anos); redução máxima de leite; **Conjunto base** e **Lista ampla**; busca na biblioteca (até 60 resultados por vez, com tipo, PB, FDN e NEL); alimentos selecionados; **Simular com o RuFaS** com progresso |
| Indicadores | Margem (destaque), receita, custo de alimentação do rebanho, custo da ração por vaca por dia, leite por vaca, leite total, e (se houver) leite perdido |
| Alerta | Aparece quando o RuFaS reduziu o leite: "A ração não atendeu a todas as exigências" |
| Ração | Barras empilhadas por intervalo de 30 dias (kg MS/vaca/dia); séries ordenadas pela quantidade média |
| Composição média | Tabela (kg MS/dia, % MS, US$/dia) com rodapé de total |
| Exigências | Linhas: NEL e DMI no eixo esquerdo, proteína metabolizável no direito |
| Leite do rebanho | Linha do leite diário e tracejado das vacas em lactação |

| Estado | Comportamento |
|---|---|
| Vazio | Ícone e texto "Escolha os alimentos e clique em Simular com o RuFaS. Cada simulação leva de 30 a 60 segundos." |
| Executando | Botão desabilitado ("Simulando…") e barra de progresso |
| Sucesso | Indicadores e gráficos; aviso "Simulação concluída." |
| Erro | Aviso com a primeira linha da mensagem; detalhe completo no servidor (`runs/<id>/console.log`) |
| Menos de 3 alimentos | Aviso pedindo volumoso, concentrado e mineral |

### Curva de lactação (`/curva/`)

**Objetivo:** reproduzir o gráfico do quadro (produção × dias, PEV e gestação).

| Bloco | Conteúdo |
|---|---|
| Selo | "parâmetros calibrados pela simulação RuFaS" ou "parâmetros de referência" |
| Campos | PEV (padrão 60 d), gestação (270 d), secagem antes do parto (60 d) |
| Gráfico | Três curvas (1ª, 2ª e 3ª ou mais lactação); linhas tracejadas verticais em PEV, secagem e parto; faixa sombreada de PEV até o parto, rotulada "gestação N d" |
| Resumo | Por paridade: pico (kg e dia) e produção em 305 dias |

Sem simulação prévia, usa parâmetros de referência da API; depois de uma simulação, usa os calibrados pelo RuFaS.

### Sensibilidade (`/sensibilidade/`)

**Objetivo:** variar preços e ver o efeito na margem.

| Bloco | Conteúdo |
|---|---|
| Fatores (esquerda) | Uma linha por alimento selecionado e uma para o preço do leite: caixa de seleção, nome completo, mínimo e máximo (padrão ±50% nos alimentos e ±20% no leite; arroz, milho e leite já marcados) |
| Opções | Método (grade ou hipercubo latino) e níveis/amostras |
| Estimativa | "N cenários, até M simulações do RuFaS (cerca de K min)" atualizada ao editar |
| Resultado | Tabela de cenários (fatores, **Res** em mapa de calor, US$/vaca/dia, leite perdido, ração principal), gráfico do efeito (Spearman) e gráfico da margem por cenário |

**Estados:** cenário que falha mostra "falhou" (com a causa na dica); leite perdido aparece em âmbar; o botão fica
desabilitado sem fatores marcados ou com menos de 3 alimentos.

### Premissas e limites (`/sobre/`)

Quatro cartões de texto: _Como o sistema funciona_, _O que o modelo assume_, _O que ele não faz_ e _Créditos e
licenças_. Serve de resposta rápida à pergunta "posso confiar neste número?". É a única _view_ estática (sem
`'use client'`).

## Visualização de Dados

Recharts, por meio do wrapper `chart.tsx` do shadcn, usando as cores `--chart-1` a `--chart-8`.

| Token | Cor (claro) | Papel típico |
|---|---|---|
| `chart-1` | verde `#007d50` | Série principal; ingrediente mais usado; efeito positivo |
| `chart-2` | âmbar `#df911a` | 2ª série; marco de secagem |
| `chart-3` | azul `#1f74bf` | 3ª série |
| `chart-4` | rosa-vermelho `#da404e` | Efeito negativo; marco de parto |
| `chart-5` a `chart-8` | violeta, turquesa, oliva, rosa | 5ª a 8ª série |

| Gráfico | Tipo | Regras |
|---|---|---|
| Ração por intervalo | Barras empilhadas | Uma cor por alimento; o de maior quantidade média recebe `chart-1`; legenda embaixo com nomes curtos |
| Exigências | Linhas, dois eixos | NEL e DMI no eixo esquerdo (Mcal e kg), proteína metabolizável no direito (g); eixo com `domain` automático |
| Leite do rebanho | Linhas, dois eixos | Leite sólido; vacas em lactação tracejado |
| Curva de lactação | Linhas com marcos e faixa de referência | Eixo X numérico (dias); marcos em verde (PEV), âmbar (secagem) e vermelho (parto) |
| Efeito sobre a margem | Barras horizontais | Verde para efeito positivo, vermelho para negativo; eixo fixo de −1 a +1 |
| Margem por cenário | Barras | Uma cor (série única) |
| Alimentos no exercício | Barras | Uma cor |

Regras gerais: eixo com unidade ou título quando a unidade não é óbvia; dica (_tooltip_) com valores ao passar o
mouse; legenda só quando há mais de uma série; cor nunca é o único canal (os marcos da curva também têm rótulo de
texto e as células de calor mostram o número); barras sempre começam em zero; as linhas usam escala automática, por
isso o eixo mostra a unidade e a variação deve ser lida com atenção.

## Padrões de Interação e Conteúdo

### Tarefas longas

Simulações e sensibilidades são tarefas em segundo plano: o botão fica desabilitado, aparece barra de progresso com
texto ("2 de 4 simulações do RuFaS concluídas" ou "Simulando no RuFaS…") e o usuário pode trocar de tela sem perder a
tarefa; o resultado fica no estado compartilhado. O servidor executa uma tarefa por vez. A consulta do estado ocorre
a cada 1,5 s (`lib/api.ts`, `runJob`).

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
| Botões só com ícone têm nome acessível (`Remover…`, `Alternar tema…`) | Sim |
| Progresso de tarefas anunciado (`role='status'`, `aria-live='polite'`) | Sim |
| Navegação por teclado e foco visível | Herdados do shadcn/Base UI (anel de foco `ring-3`); não foram testados por teclado nesta versão |
| Atalho `Ctrl/Cmd + B` para a barra lateral | Sim (do template) |
| Cor não é o único canal de informação | Sim (rótulos, números e selos de texto) |
| Respeito ao tema do sistema | Sim |

### Contraste medido (WCAG 2.1; mínimo 4,5:1 para texto normal)

Razões calculadas a partir dos tokens (conversão `oklch` → sRGB):

| Par | Claro | Escuro |
|---|---|---|
| Texto sobre fundo | 19,8 | 19,0 |
| Texto secundário sobre cartão | 4,7 | 6,9 |
| Primária como texto sobre cartão | 6,8 | 7,7 |
| Texto sobre botão primário | 6,5 | 8,4 |
| Destrutivo sobre cartão | 4,8 | 6,2 |
| **Texto de aviso (`warning-text`) sobre cartão** | 6,2 | 10,1 |
| Texto sobre mapa de calor, no máximo (40%) | 13,0 | 4,7 |

### Problemas encontrados e corrigidos

| Problema | Antes | Correção |
|---|---|---|
| Texto de "leite perdido" no tema escuro usava a cor de primeiro plano do aviso (escura) | 1,7:1 | Novo token `warning-text` (6,2:1 no claro e 10,1:1 no escuro) |
| Células de calor no máximo (50%) com texto branco, no tema escuro | 3,9:1 | Teto de 40% (4,7:1 no escuro; 13,0:1 no claro) |

### Lacunas conhecidas

- O contraste das **cores de gráfico** contra o fundo (mínimo de 3:1 para elementos gráficos) não foi medido.
- Não foi feita auditoria com leitor de tela nem com ferramenta automatizada (axe, Lighthouse).
- Os gráficos do Recharts não têm descrição alternativa em texto; a tabela de composição e as tabelas de cenários
  dão os mesmos dados, mas sem ligação explícita.
- Algumas dicas dependem de passar o mouse (nomes completos nas colunas de tabela).

## Responsividade

| Largura | Comportamento |
|---|---|
| < 1.280 px | Barra lateral vira gaveta; painéis lateral e de resultados empilham em uma coluna |
| ≥ 1.280 px | Barra lateral fixa; layout em duas colunas; indicadores em 3 colunas |
| ≥ 1.536 px | Indicadores em 4 colunas; pares de gráficos lado a lado |
| ≥ 640 px | Margens de 24 px e _breadcrumb_ visível |

**Verificado:** 1.440 px e cerca de 540 px, no navegador embutido. **Não verificado:** tablets, celulares reais e
telas acima de 1.600 px.

## Arquitetura e Origem

### Origem: o template AdminCN

**AdminCN Free 1.0.0** (shadcn/studio, MIT): painel administrativo com Next.js 16.2.6, React 19.2.4, Tailwind CSS v4,
shadcn/ui (estilo `base-vega`, sobre Base UI 1.6.0), Recharts 3.8.0 e ícones Lucide. Vem com páginas de pedidos,
e-mail, calendário, usuários, autenticação, formulários e tabelas, 42 componentes de interface e um tema neutro em
cinza. Foi adaptado com exportação estática (`output: 'export'`); o servidor Python serve o resultado.

| Categoria | Itens |
|---|---|
| **Reaproveitado (adaptado)** | Estrutura da tela (barra lateral recolhível + cabeçalho fixo + conteúdo + rodapé); 18 componentes de `ui/`; sistema de tokens de cor em `oklch`; modo claro e escuro com `next-themes`; escala de raio e tipografia. |
| **Alterado** | Cor primária (cinza → verde); paleta de gráficos (5 → 8 cores); idioma (pt-BR); barra lateral reescrita para 5 destinos; cabeçalho com breadcrumb simples, indicador de conexão e troca de tema; fonte Geist via pacote `geist`; hook `use-mobile` (D7). |
| **Removido** | Páginas de demo (pedidos, e-mail, calendário, usuários, autenticação, formulários, tabelas de dados); banco falso (`fake-db`); rotas de API e _server actions_; redirecionamentos do `next.config`; botão de estrelas do GitHub; botão de download; links promocionais; menu de perfil e de idioma; 24 componentes de UI sem uso; 9 dependências (nuqs, react-hook-form, @hookform/resolvers, zod, @tanstack/react-table, cmdk, input-otp, date-fns, react-resizable-panels). |
| **Criado** | As 5 telas, o estado compartilhado, o cliente da API, o seletor de alimentos, os indicadores (`KpiCard`), o campo numérico, a barra de progresso de tarefas, a tabela com mapa de calor e os gráficos do domínio. |

O template tem 269 arquivos e 22 dependências; a interface atual tem 47 arquivos de código, cerca de 2.400 linhas
próprias, 14 dependências e 6 de desenvolvimento.

### Fluxo de construção

```
 web/  (fontes: Next.js + React + Tailwind v4 + shadcn/ui)
   │  scripts/build-web.ps1
   │    1. copia as fontes para %LOCALAPPDATA%\dietopt-web-build
   │    2. npm install  e  npm run build   (exportação estática)
   │    3. publica out/ em frontend/
   ▼
 frontend/  (HTML + CSS + JS estáticos, 2,9 MB)
   │  servido por backend/dietopt/server.py  (http://127.0.0.1:8000)
   ▼
 /api/*  (JSON): feeds, defaults, lactation, toy, toy/sensitivity, jobs/simulate, jobs/sensitivity, jobs/<id>
```

Quem só **usa** o sistema não precisa de Node; só quem **altera a interface** precisa de Node 20.9 ou superior. A
primeira versão da interface (HTML puro com Chart.js) ficou em `frontend_legacy/`.

### Pilha

| Camada | Tecnologia | Versão |
|---|---|---|
| Framework | Next.js (App Router, exportação estática, Turbopack) | 16.2.6 |
| UI | React | 19.2.4 |
| Estilo | Tailwind CSS (tokens em CSS) e `tw-animate-css` | 4.3.3 / 1.4.0 |
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
| `feeds`, `defaults`, `connection` | Biblioteca NRC (130 alimentos), preços e preço do leite iniciais, estado da conexão |
| `selected` | Alimentos escolhidos, com preço e limites mínimo e máximo (kg MS/vaca/dia) |
| `params` | Preço do leite, período (1 ou 2 anos), redução máxima de leite |
| `sim`, `sens` | Último resultado de simulação e de sensibilidade |
| `toyFoods`, `toyBounds`, `toyResult`, `toySens` | Exercício do quadro |

### Contrato com a API

| Método e rota | Corpo | Resposta |
|---|---|---|
| `GET /api/feeds` | , | Lista de alimentos (id, nome, descrição, tipo, composição, `nel`, `default_price`, `default_max`) |
| `GET /api/defaults` | , | `milk_price` e `prices` |
| `GET /api/lactation` | , | Parâmetros de Wood de referência e marcos |
| `POST /api/toy` | alimentos e limites | Solução ótima, custo, totais, preços-sombra |
| `POST /api/toy/sensitivity` | problema e dois fatores | Colunas e linhas de cenários |
| `POST /api/jobs/simulate` | alimentos, preços, limites, preço do leite, período, redução máxima | Tarefa (`id`) |
| `POST /api/jobs/sensitivity` | o mesmo, mais fatores, método e níveis | Tarefa (`id`) |
| `GET /api/jobs/<id>` | , | Estado (`queued`, `running`, `done`, `error`), progresso e resultado |

Os tipos TypeScript dos contratos estão em `web/src/lib/types.ts`.

## Persistência e Privacidade

| Tema | Detalhe |
|---|---|
| `localStorage` | `dietopt.v1` (alimentos selecionados e parâmetros) e `theme` (next-themes). Tudo local ao navegador; resultados não são salvos. |
| Cookie | `sidebar_state` (estado da barra lateral, vem do template), 7 dias. |
| Dados enviados | Só para `127.0.0.1` (servidor local). Sem rastreamento, sem serviços externos em tempo de execução. |
| Tamanho | `frontend/` ocupa 2,9 MB (HTML, JS, CSS e fontes); funciona sem internet. |
| Construção | Compilar e publicar leva cerca de 15 s com as dependências já instaladas (cerca de 40 s a mais na primeira vez). |
| Pré-carregamento | O Next.js pré-carrega as outras rotas; o servidor responde a `HEAD` e mapeia os arquivos `*.__PAGE__.txt` (D8). |

## Decisões de Design

| ID | Decisão | Motivo | Alternativa descartada |
|---|---|---|---|
| D1 | Adaptar o template com **exportação estática** e servi-lo pelo servidor Python | Mantém a execução local simples (sem Node em tempo de uso) e reaproveita o back-end | Rodar um servidor Node junto, com duas portas e dois processos |
| D2 | Reescrever o nav, o cabeçalho e as páginas; **não** manter as páginas do demo | O demo tem e-mail, calendário e autenticação sem relação com o produto | Esconder as páginas do demo |
| D3 | Cor primária **verde** | Identidade agropecuária, distinta do cinza do template | Manter o tema neutro |
| D4 | Recharts via wrapper do shadcn, no lugar de Chart.js | Já vem no template e integra com os tokens de cor e o tema escuro | Manter o Chart.js |
| D5 | Estado em um `AppProvider` único | Dados sobrevivem à navegação, sem biblioteca de estado | Redux, Zustand ou estado por página |
| D6 | Build **fora do OneDrive** (`%LOCALAPPDATA%`) | Evita sincronizar 551 MB de `node_modules` e o problema do "Á" no caminho | `node_modules` dentro do projeto |
| D7 | Corrigir `use-mobile` para medir a janela só **depois da montagem** | O original lia `window` no estado inicial, divergindo do HTML estático (erro de hidratação #418) | Desabilitar o aviso do React |
| D8 | Mapear no servidor `…__next.rota.__PAGE__.txt` → `…__next.rota/__PAGE__.txt` | No Windows o export grava com pasta e o navegador pede com ponto; evita 404 e perda de pré-carregamento | Desligar o pré-carregamento |
| D9 | Limite de 40% no mapa de calor e token `warning-text` | Contraste medido abaixo de 4,5:1 | Manter os valores do protótipo |
| D10 | Fonte via pacote `geist` | Funciona sem rede e sem baixar do Google no build | `next/font/google` |
| D11 | Guardar a interface antiga em `frontend_legacy/` | Permite voltar atrás e comparar resultados | Apagar |
| D12 | Selecionar alimentos com busca e lista de caixas, não com caixa combinada (`Combobox`) | 130 itens com 3 dados de apoio cada; a lista mostra tipo, PB, FDN e NEL de uma vez | Combobox do template |

## Limitações

Estado atual, sem propostas:

1. **Sem testes automatizados de interface.** A verificação foi manual (5 telas, tema claro e escuro, uma simulação
   real e uma sensibilidade real). A regressão numérica foi conferida: a sensibilidade na interface nova reproduziu
   exatamente os resultados da antiga (por exemplo, US$ 289.712 e US$ 519.929).
2. **Acessibilidade parcial** (seção _Acessibilidade_): sem auditoria automatizada nem leitor de tela; gráficos sem
   texto alternativo.
3. **Telas pequenas pouco exercitadas:** o layout estreito foi visto em uma largura; tabelas de cenários exigem
   rolagem horizontal.
4. **A seleção de alimentos mostra só os 60 primeiros resultados** da busca; é preciso refinar o termo para ver os
   demais.
5. **Sem exportação** de tabelas e gráficos (PRD, RF-20) nem salvamento de cenários (RF-21).
6. **Sem o balanço de nutrientes** da ração obtida (PRD, RF-19), requisito importante para o usuário profissional.
7. **Uma tarefa por vez** no servidor: se duas abas disparam simulações, a segunda espera na fila.
8. **O mapeamento do pré-carregamento é um contorno** de um comportamento do export do Next.js no Windows; pode
   deixar de ser necessário em versões futuras.
9. **Código herdado do template** (barra lateral, wrapper de gráficos) é extenso (cerca de 1.500 linhas) e não foi
   revisado linha a linha; foi mantido sem alterações, exceto o hook `use-mobile`.
10. **Cor de série nos gráficos não foi validada para daltonismo**, e o contraste delas contra o fundo não foi medido.
11. **Fonte monoespaçada, animação `heartbeat` e componente `Skeleton`** estão definidos mas sem uso nas telas.
12. **Valores em hexadecimal do front matter são conversões aproximadas** dos tokens `oklch` (fonte de verdade).

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

Valores em `oklch(L C h)`. Fonte: `web/src/app/globals.css`.

| Token | Claro | Escuro |
|---|---|---|
| `--background` | `1 0 0` | `0.145 0 0` |
| `--foreground` | `0.145 0 0` | `0.985 0 0` |
| `--card` | `1 0 0` | `0.205 0 0` |
| `--primary` | `0.46 0.1 160` | `0.72 0.15 160` |
| `--primary-foreground` | `0.985 0 0` | `0.15 0.03 160` |
| `--secondary`, `--muted`, `--accent` | `0.97 0 0` | `0.269 0 0` |
| `--muted-foreground` | `0.556 0 0` | `0.708 0 0` |
| `--destructive` | `0.577 0.245 27.325` | `0.704 0.191 22.216` |
| `--border` | `0.922 0 0` | `1 0 0 / 10%` |
| `--input` | `0.922 0 0` | `1 0 0 / 15%` |
| `--ring` | `0.708 0 0` | `0.556 0 0` |
| `--success` | `0.52 0.12 160` | `0.72 0.15 160` |
| `--warning` | `0.72 0.15 70` | `0.8 0.15 75` |
| `--warning-text` | `0.5 0.12 65` | `0.82 0.13 80` |
| `--chart-1` | `0.52 0.12 160` | `0.72 0.15 160` |
| `--chart-2` | `0.72 0.15 70` | `0.8 0.15 75` |
| `--chart-3` | `0.55 0.14 250` | `0.7 0.14 250` |
| `--chart-4` | `0.6 0.19 20` | `0.7 0.17 20` |
| `--chart-5` | `0.55 0.17 300` | `0.7 0.16 300` |
| `--chart-6` | `0.6 0.1 195` | `0.75 0.1 195` |
| `--chart-7` | `0.62 0.12 110` | `0.76 0.13 115` |
| `--chart-8` | `0.62 0.18 350` | `0.74 0.16 350` |
| `--sidebar` | `0.985 0 0` | `0.205 0 0` |
| `--sidebar-primary` | `0.46 0.1 160` | `0.72 0.15 160` |
| `--radius` | `0.625rem` | `0.625rem` |

## Apêndice B: mapa de arquivos

```
web/
├─ package.json, package-lock.json     dependências (14 + 6 de desenvolvimento)
├─ next.config.ts                       exportação estática; encaminha /api em desenvolvimento
├─ tsconfig.json, postcss.config.mjs, components.json
├─ LICENSE-TEMPLATE.md                  aviso de copyright do template (MIT)
└─ src/
   ├─ app/
   │  ├─ layout.tsx                     raiz: fontes, tema, barra lateral, estado
   │  ├─ globals.css                    tokens de cor, raio e utilitários
   │  ├─ page.tsx, vaca/, curva/, sensibilidade/, sobre/   rotas finas
   │  └─ not-found.tsx
   ├─ views/                            ToyView, CowView, CurveView, SensitivityView, AboutView
   ├─ components/
   │  ├─ layout/                        AppShell, AppSidebar, Header, Footer, ModeToggle, nav.ts
   │  ├─ ui/                            18 componentes do shadcn (do template)
   │  ├─ FeedPicker.tsx, shared.tsx, ThemeProvider.tsx
   ├─ providers/AppProvider.tsx         estado compartilhado
   ├─ hooks/use-mobile.ts               largura da janela (corrigido)
   └─ lib/                              api.ts, types.ts, format.ts, utils.ts
scripts/build-web.ps1                   build e publicação em frontend/
frontend/                               interface publicada (gerada; não editar)
frontend_legacy/                        primeira versão da interface (HTML puro)
```

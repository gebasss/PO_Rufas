# DOCUMENTO DE ESPECIFICAÇÃO FUNCIONAL (FSD)

## Dieta Ótima com RuFaS

| Item | Valor |
|---|---|
| Versão do sistema descrita | Web 1.0 (protótipo acadêmico; o código não tem número de versão formal, o servidor se identifica como `DietOpt/1.0`) |
| Data de referência | 12/10/2026 (seções 1 a 28, sistema implementado); Anexos A e B revistos em 02/11/2026 (funcionalidades planejadas, não implementadas) |
| Natureza do documento | Especificação consolidada de um sistema **já implementado e verificado, ainda sem uso em produção**. Serve como documentação formal, base de manutenção e referência para reimplementação. |

Este documento é autossuficiente. Quando o comportamento da implementação atual diverge do que está especificado aqui, a divergência está catalogada na seção 26 (Desvios Conhecidos), com identificadores `D1`, `D2`, etc., referenciados ao longo do texto. Os requisitos `RF-24`, `RF-26` e `RF-27` estão especificados no **Anexo A**, e os requisitos `RF-28` a `RF-30` (módulo ampliado do Exercício do quadro, com modelo linear) no **Anexo B** e em `LINEARIZACAO.md` (todos planejados, **não implementados**). Os demais requisitos do PRD ainda não implementados (`RF-13`, `RF-19` a `RF-23`) **não** são especificados aqui: constam como pendentes na seção 27 e não devem ser inventados.

---

## 1. Visão Geral

**Nome do sistema:** Dieta Ótima com RuFaS.

**Objetivo principal:** formular a dieta de vacas leiteiras de custo mínimo e medir o efeito econômico dessa dieta ao longo da lactação (margem sobre o custo de alimentação), usando o simulador RuFaS e permitindo testar muitos cenários de preço sem editar arquivos nem usar linha de comando.

**Resumo do funcionamento:** o usuário abre uma aplicação web que roda na própria máquina. Em uma tela, resolve o exercício de dieta do quadro do professor (arroz e milho) por programação linear. Em outra, escolhe alimentos da biblioteca NRC 2001, informa preços e limites de inclusão e dispara uma simulação do RuFaS. O servidor local monta os arquivos de entrada do RuFaS, executa-o em um processo separado, lê os resultados e calcula custo, receita e margem. Uma terceira tela repete a simulação para combinações de preços (análise de sensibilidade) e mostra a tabela de cenários e o efeito de cada fator. Uma quarta desenha a curva de lactação de Wood com PEV e gestação.

**Público usuário:** nutricionista de rebanho leiteiro e produtor de leite; o professor de Pesquisa Operacional como avaliador. Perfil único e implícito, sem hierarquia.

**Contexto de uso:** local e individual, na própria máquina Windows do usuário. O servidor aceita conexões apenas da própria máquina por padrão; não há uso remoto nem uso simultâneo por vários usuários.

**Observações relevantes para implementação:**

- O sistema **não altera** o RuFaS (v1.0.6, GPLv3). Toda adaptação está em um módulo próprio que escreve cópias editadas dos arquivos de entrada.
- Não existe banco de dados, login, upload, exportação, relatório ou auditoria. A persistência é por arquivos (pasta `runs/`) e pelo armazenamento local do navegador.
- A ração das vacas é formulada **pelo otimizador do próprio RuFaS**; o leite é o **simulado pelo RuFaS**. O sistema informa alimentos, preços e limites e calcula a economia sobre o resultado.
- Os preços iniciais são **ilustrativos**, não cotações.
- Princípio transversal: **o sistema nunca esconde o que o modelo fez**. Uma simulação que falha é uma falha, nunca um resultado zerado; leite que o RuFaS reduziu aparece como "leite perdido".

### 1.1 Glossário

| Termo | Significado |
|---|---|
| RuFaS | *Ruminant Farm Systems*, simulador de fazenda leiteira de código aberto. Usado como caixa externa que recebe arquivos de entrada e devolve arquivos de saída. |
| NRC (2001) | *Nutrient Requirements of Dairy Cattle*, 7ª edição revisada: exigências e composição dos alimentos. Padrão nutricional usado. |
| NASEM (2021) | Edição mais recente do padrão de exigências. Não é oferecida. |
| MS | Matéria seca. Preços e limites são por kg de MS. |
| PB, FDN, EE, TDN | Proteína bruta, fibra em detergente neutro, extrato etéreo, nutrientes digestíveis totais (% da MS). |
| NEL | Energia líquida de lactação (Mcal). |
| DMI | *Dry matter intake*: consumo de matéria seca. |
| PM | Proteína metabolizável (g/dia). |
| Cenário | Conjunto de parâmetros que define uma simulação (`Scenario`). Também a linha `Sn` da tabela de sensibilidade. |
| Cache | Resultado de simulação guardado em disco, reutilizado quando o cenário é idêntico. |
| Tarefa (*job*) | Execução em segundo plano de uma simulação ou de uma sensibilidade. |
| Margem (`Res`) | Receita do leite menos o custo de alimentação do rebanho no período. |
| Leite perdido | Redução média de leite imposta pelo RuFaS porque a ração não atendeu às exigências. |
| Preço-sombra | Variação do custo ótimo por unidade adicional do limite mínimo de um nutriente. |
| PEV | Período de espera voluntário: dias após o parto antes da primeira inseminação (interpretação do autor). |
| Curva de Wood | `y(t) = l · t^m · e^(−n·t)`, produção diária de leite em função dos dias em lactação. |
| Mantenedor | Pessoa que altera o código e recompila a interface. Papel operacional, sem função dentro da ferramenta. |

---

## 2. Documentos do Projeto para Implementação

| Documento | Papel |
|---|---|
| `FSD.md` (este) | Fonte principal e autossuficiente. Em caso de divergência com qualquer outro documento, este prevalece. |
| `PRD.md` | Requisitos do produto, personas, métricas e questões em aberto. Fonte dos requisitos pendentes. |
| `DESIGN.md` | Referência visual complementar. O conteúdo visual relevante está consolidado na seção 10 deste FSD. |
| `DOMINIO.md` | Regras de negócio e mapeamento regra → arquivo → função → teste. Referência técnica de baixo nível. Inclui a seção 8, de fontes científicas. |
| `LINEARIZACAO.md` | Estudo da linearização das equações do otimizador do RuFaS (fórmulas, técnicas, verificação do erro). Base técnica do Anexo B. |
| `nasem2021_notas/` (local, não versionada) | Notas técnicas do livro NASEM 2021 (tradução PT-BR), usadas como referência científica do Anexo A. O código R do modelo oficial prevalece sobre o texto do livro. |
| `DECISOES_TECNICAS.md` | Decisões técnicas já tomadas, alertas e pendências. |
| `README.md` | Instruções de instalação e uso. |

O repositório contém também a implementação de referência que este FSD descreve (`backend/dietopt/`, `web/src/`). Ela é útil para consulta, mas **não** é fonte de verdade onde divergir do FSD: os pontos de divergência estão na seção 26.

---

## 3. Stack Definida

| Item | Definição |
|---|---|
| Sistema operacional | Windows 10 ou 11 (único testado) |
| Linguagem do servidor, do adaptador e dos cálculos | Python 3.12 (o RuFaS exige 3.12 ou 3.13) em ambiente virtual `.venv` |
| Servidor HTTP | `ThreadingHTTPServer` da biblioteca padrão do Python, escutando em `127.0.0.1:8000` por padrão |
| Cálculo numérico | NumPy 2.2.0 e SciPy 1.16.2 (PL com HiGHS e correlação de Spearman); pandas 2.3.2 é exigido pelo RuFaS |
| Simulador | RuFaS v1.0.6 em `vendor/RuFaS` (clone da tag), executado em subprocesso |
| Interface | TypeScript (modo estrito) com Next.js 16.2.6 (exportação estática), React 19.2.4, Tailwind CSS 4.3.3, shadcn/ui sobre Base UI 1.6.0, Recharts 3.8.0, Lucide, next-themes, Sonner |
| Fonte | Geist Sans (pacote `geist`, arquivos locais) |
| Ferramentas de build da interface | Node 20.9 ou superior e npm (observado: Node 24.18, npm 11.16); só para quem altera a interface |
| Dados de referência | Tabelas CSV e JSON do RuFaS (`NRC_comp.csv`, `user_feeds.csv`, exemplo `freestall`) e constantes do código |
| Instalação e execução | `scripts/setup.ps1` (PowerShell), `scripts/fetch_wheels.py`, `scripts/build-web.ps1`, `iniciar.bat` |
| Testes automatizados | `pytest`, 71 testes em `backend/tests/` |
| Banco de dados, ORM, framework web de backend, autenticação | Nenhum |

**Padrão arquitetural:** ponte local em três camadas. O navegador (site estático) comunica-se por HTTP/JSON com um servidor Python em loopback, que delega a simulação a um processo filho do RuFaS e a leitura de seus arquivos de saída.

**Restrições técnicas:**

- O RuFaS v1.0.6 exige Python 3.12 ou 3.13 e **todas** as dependências de desenvolvimento do seu `pyproject.toml`.
- O validador de caminhos do RuFaS rejeita caracteres acentuados (`[a-zA-Z0-9_\-\. ]`). Todo caminho passado ao RuFaS é **relativo a `vendor/RuFaS`**.
- O gerenciador de tarefas do RuFaS sai com código 0 mesmo quando a tarefa falha; o sucesso exige também a linha de resumo (seção 12.1).
- Cada simulação usa cerca de 1,2 GB de RAM; há no máximo 2 simulações simultâneas e uma tarefa por vez.
- A interface é um site estático (`output: 'export'`, `trailingSlash`): não há renderização no servidor nem rotas dinâmicas.
- O build da interface não deve rodar dentro do OneDrive nem em caminho com acento (usa `%LOCALAPPDATA%\dietopt-web-build`).
- O `pip` do Python 3.14 do sistema falha por TLS com `files.pythonhosted.org`; a instalação tem contorno com `curl`.

**Uso de bibliotecas:** nenhuma funcionalidade depende de internet em tempo de uso. A internet só é necessária durante a instalação (clone do RuFaS e pacotes) e para recompilar a interface (pacotes npm).

---

## 4. Arquitetura do Sistema

### 4.1 Componentes

| Componente | Local de execução | Responsabilidade |
|---|---|---|
| Interface web | Navegador | Cinco telas, estado compartilhado, chamadas à API, gráficos |
| Servidor local (`server.py`) | Processo Python de longa duração | API JSON, arquivos estáticos, montagem de cenários a partir das requisições |
| Gerenciador de tarefas (`jobs.py`) | Threads do servidor | Executa simulações e sensibilidades em segundo plano, uma por vez |
| Problema da dieta (`diet_lp.py`) | Servidor | PL do exercício do quadro, preços-sombra |
| Adaptador do RuFaS (`rufas_adapter.py`) | Servidor | Escreve entradas do RuFaS, executa-o, detecta falha |
| Leitor de saídas (`rufas_results.py`) | Servidor | Filtros de saída e conversão dos JSONs em `SimulationResult` |
| Economia e cache (`scenarios.py`) | Servidor | Preços padrão, receita, custo, margem, cache |
| Sensibilidade (`sensitivity.py`) | Servidor | Pontos, cenários S1..SN, efeitos de Spearman |
| Curva de lactação (`lactation.py`) | Servidor | Curva de Wood, marcos, pico, produção em 305 dias |
| Biblioteca de alimentos (`feeds.py`) | Servidor | Lê a biblioteca NRC do RuFaS; tetos padrão; NEL estimada |
| RuFaS | Processo filho, um por simulação | Simulação da fazenda e formulação da ração |
| Scripts de instalação e execução | Máquina do usuário | Ambiente, build da interface, início do servidor |

### 4.2 Modelo de processos

1. `iniciar.bat` abre o navegador em `http://127.0.0.1:8000` e inicia **um processo Python de longa duração** (o servidor), que o usuário deve manter aberto.
2. Cada requisição de simulação ou sensibilidade cria uma **thread** de tarefa. Um bloqueio global faz as tarefas esperarem em fila.
3. Para cada simulação, o adaptador cria `runs/<nome>/`, executa `main.py` do RuFaS em um **processo filho** (diretório de trabalho `vendor/RuFaS`) e lê os JSONs de saída. Numa sensibilidade, até 2 processos filhos rodam ao mesmo tempo.
4. No navegador, um único `AppProvider` guarda o estado compartilhado entre as telas.

### 4.3 Fluxo de dados de uma simulação

```
Usuário -> Interface -> POST /api/jobs/simulate -> Servidor (cria tarefa "queued", responde 202 com o id)
Interface -> GET /api/jobs/<id> a cada 1,5 s -> estado, progresso, resultado
Servidor (tarefa) -> scenario_from(params) -> evaluate(scenario)
   -> cache_key encontra runs/_cache/<chave>.json?  sim: devolve o resultado guardado
   -> não: build_scenario -> runs/<nome>/ -> subprocesso RuFaS (main.py) -> JSONs de saída
        -> parse_outputs -> SimulationResult -> grava o cache
Servidor -> receita, custo, margem -> resultado da tarefa -> Interface (tela)
```

### 4.4 Estado mantido

| Onde | Chave / variável | Conteúdo | Tempo de vida |
|---|---|---|---|
| `localStorage` do navegador | `dietopt.v1` | `{ selected, params }`: alimentos selecionados (preço, mínimo, máximo) e parâmetros da simulação | Até o usuário limpar os dados do site |
| `localStorage` do navegador | `theme` | Tema claro, escuro ou do sistema (next-themes) | Idem |
| Cookie | `sidebar_state` | Estado aberto ou recolhido da barra lateral | 7 dias |
| Memória da página | resultados de simulação e de sensibilidade, exercício do quadro (alimentos, nutrientes, solução, cenários) | Estado do `AppProvider` | Até recarregar a página (sobrevive à navegação entre telas) |
| Memória do servidor | tarefas (`JobManager`) | Estado, progresso e resultado de cada tarefa | Até reiniciar o servidor; nunca removidas enquanto o processo vive |
| Disco | `runs/<nome>/` | Entradas editadas do RuFaS, saídas, `console.log` | Permanente; não há limpeza automática |
| Disco | `runs/_cache/<chave>.json` | Resultado de simulações bem-sucedidas | Permanente |

O servidor **não** persiste dados do usuário além dos arquivos de cenário e do cache.

---

## 5. Estrutura de Diretórios e Distribuição

### 5.1 Estrutura do projeto

```
aplicacao RuFaS/
  iniciar.bat                 Abre o navegador e inicia o servidor (porta 8000)
  requirements-rufas.txt      Dependências Python exigidas pelo RuFaS (versões fixadas)
  README.md                   Instalação e uso
  .gitignore                  Exclusões previstas (.venv, wheelhouse, runs, caches)
  backend/
    dietopt/                  Pacote Python do sistema
      server.py               Servidor HTTP e API
      jobs.py                 Tarefas em segundo plano
      diet_lp.py              PL da dieta
      rufas_adapter.py        Cenário -> entradas do RuFaS; execução
      rufas_results.py        Filtros e leitura das saídas
      scenarios.py            Preços padrão, economia, cache
      sensitivity.py          Sensibilidade e Spearman
      lactation.py            Curva de Wood e marcos
      feeds.py                Biblioteca NRC e tetos padrão
    tests/                    71 testes (pytest)
  web/                        Fontes da interface (Next.js)
    src/app, src/views, src/components, src/providers, src/hooks, src/lib
    package.json, package-lock.json, next.config.ts, LICENSE-TEMPLATE.md
  frontend/                   Interface publicada (gerada; não editar)
  frontend_legacy/            Primeira versão da interface (HTML puro)
  scripts/                    setup.ps1, fetch_wheels.py, build-web.ps1
  vendor/RuFaS/               Clone do RuFaS v1.0.6 (não modificar)
  runs/                       Cenários, logs e cache (gerado)
  wheelhouse/                 Pacotes baixados com curl (gerado, se o pip falhar)
  .venv/                      Ambiente virtual Python 3.12 (gerado)
  docs/                       PRD, DESIGN, DOMINIO, DECISOES_TECNICAS, FSD
```

### 5.2 Instalação

- Pré-requisitos: Windows 10/11; Python 3.12 acessível por `py -3.12` (instalável com `winget install Python.Python.3.12`); Git; internet durante a instalação; cerca de 1 GB de disco (`.venv` ≈ 615 MB, `wheelhouse` ≈ 140 MB) e, para simular, pelo menos 2,5 GB de RAM livre.
- Executar uma vez, na raiz do projeto: `powershell -ExecutionPolicy Bypass -File scripts\setup.ps1`. O script exige `py -3.12`, clona o RuFaS v1.0.6 em `vendor/RuFaS` se a pasta não existir, cria `.venv` e instala `requirements-rufas.txt`. Se o `pip` falhar, baixa os pacotes com `scripts\fetch_wheels.py` para `wheelhouse/` e reinstala sem rede.
- Para usar: executar `iniciar.bat`.
- Para alterar a interface (opcional): instalar Node 20.9+ e executar `powershell -ExecutionPolicy Bypass -File scripts\build-web.ps1` (cerca de 15 s com dependências instaladas).
- Não há instalador, pacote nem processo de entrega formal.

### 5.3 Proteção de recursos internos

- O servidor serve arquivos estáticos **somente** de `frontend/`. Qualquer caminho que resolva fora dessa pasta responde 404. `runs/`, `vendor/` e `backend/` não são servidos.
- O servidor escuta em `127.0.0.1` por padrão. Pode ser alterado com `--host`, o que expõe o servidor sem autenticação (D5).
- As pastas de cenário contêm apenas dados de simulação; não há credenciais nem dados pessoais.

---

## 6. Escopo Funcional da Primeira Versão

### 6.1 Exercício do quadro (programação linear)

- **Objetivo:** reproduzir e explorar o problema de dieta de custo mínimo do professor.
- **Usuários:** professor, estudante, nutricionista.
- **Ações permitidas:** editar nome, custo e composição dos alimentos (carboidrato e proteína); adicionar e remover alimentos (mínimo de 2); editar mínimo e máximo de cada nutriente; resolver; gerar a tabela de cenários variando dois fatores.
- **Resultado esperado:** custo mínimo, quantidade e custo por alimento, total de cada nutriente com a restrição ativa e o preço-sombra, gráfico de barras e tabela `S1..SN` com a coluna `Res`.
- **Dependências:** servidor ativo.
- **Regras:** seção 14.1.

### 6.2 Seleção de alimentos, preços e limites

- **Objetivo:** montar o cenário da vaca leiteira.
- **Ações permitidas:** buscar na biblioteca NRC 2001; marcar e desmarcar alimentos; aplicar o "Conjunto base" ou a "Lista ampla"; editar preço, mínimo e máximo de cada alimento; definir preço do leite, período (1 ou 2 anos) e redução máxima de leite.
- **Resultado esperado:** configuração pronta para simular, guardada no navegador.
- **Regras:** seções 14.2 e 14.3.

### 6.3 Simulação da vaca leiteira com o RuFaS

- **Objetivo:** obter ração, custo, leite e margem de uma simulação.
- **Ações permitidas:** acionar "Simular com o RuFaS"; acompanhar o progresso; continuar navegando.
- **Resultado esperado:** seis indicadores (mais "leite perdido" quando houver), ração por intervalo de 30 dias, composição média, exigências e leite do rebanho.
- **Dependências:** servidor ativo; pelo menos 3 alimentos selecionados.
- **Regras:** seções 12.1, 14.4, 14.5 e 15.1.

### 6.4 Análise de sensibilidade

- **Objetivo:** ver como a margem reage a preços de alimentos e do leite.
- **Ações permitidas:** marcar fatores e informar faixas; escolher método (grade ou hipercubo latino) e níveis; rodar.
- **Resultado esperado:** tabela de cenários, efeito de Spearman de cada fator e margem por cenário.
- **Regras:** seção 15.2.

### 6.5 Curva de lactação

- **Objetivo:** reproduzir o gráfico do quadro (produção × dias, PEV, gestação).
- **Ações permitidas:** editar PEV, gestação e dias de secagem.
- **Resultado esperado:** curvas de Wood por paridade com marcos, pico e produção em 305 dias.
- **Regras:** seção 15.3.

### 6.6 Premissas e limites

- **Objetivo:** responder "posso confiar neste número?".
- **Resultado esperado:** quatro blocos de texto (funcionamento, premissas, limites, créditos).

### 6.7 Reaproveitamento por cache

- **Objetivo:** não repetir simulações idênticas.
- **Resultado esperado:** mudar só o preço do leite, ou repetir um cenário, devolve o resultado em segundos.
- **Regras:** seção 14.6.

### 6.8 Indicador de conexão

- **Objetivo:** informar se a interface alcança o servidor.
- **Resultado esperado:** três estados no cabeçalho: "conectando…", "conectado · N alimentos NRC" e "sem conexão com o servidor".
- **Regras:** seção 14.9.

---

## 7. Fora de Escopo

| Item | Observação |
|---|---|
| Balanço nutricional (oferta × exigência) da ração obtida | Requisito RF-19, pendente. Hoje só as exigências são exibidas. |
| Exportação de tabelas e relatórios; salvar e carregar cenários | RF-20 e RF-21, implementados em 03/11/2026 (A.10 e A.11). |
| Importação de preços (CEPEA ou CSV) | RF-22, pendente. Preços são digitados. |
| Mais nutrientes no exercício do quadro | RF-23, pendente. Os nutrientes são fixos (carboidrato e proteína). |
| Padrão NASEM 2021 | RF-24, pendente; especificado no Anexo A.3. O sistema usa só a NRC 2001. |
| Módulo ampliado do Exercício do quadro (avaliação de dietas montadas, modelo linear das equações do RuFaS) | RF-28 e RF-29, pendentes; especificados no Anexo B. |
| Sugestão e previsão da dieta ótima de uma vaca e fase (RF-30) | Fase 2, implementada em 03/11/2026 (Anexo B, B.8 e B.11; `LINEARIZACAO.md`, 7.6); falta o laço de redução de leite. |
| Ajuste do tamanho do rebanho pela interface | RF-13, implementado em 10/11/2026 (A.13): de 60 a 500 vacas, com o rebanho e as baias escalados juntos. |
| Dieta otimizada por fase da lactação | Depende da questão Q2 do PRD. A ração é formulada por grupo, pelo RuFaS. |
| Modelo próprio de resposta do leite à dieta | Depende da questão Q3 do PRD. O leite é o simulado pelo RuFaS. |
| Linha de comando e relatório em PDF | Fase seguinte à web. |
| Autenticação, perfis, auditoria | Não existem e não são requisitos. |
| Banco de dados | O sistema usa arquivos e `localStorage`. |
| Modificar o código do RuFaS | O RuFaS é usado como está. |
| Hospedagem em nuvem, vários usuários, várias fazendas | O sistema é local e individual. |
| CI/CD, ambiente de homologação, fluxo de revisão do repositório Git | Não existem (seção 27). |
| Testes automatizados de integração e de interface | Não existem; só os 71 testes do back-end. |

---

## 8. Perfis e Controle de Acesso

### 8.1 Perfil

| Perfil | Pode | Não pode |
|---|---|---|
| Usuário da aplicação (único, implícito) | Resolver o exercício; escolher alimentos, preços e limites; disparar simulações e sensibilidades; ver resultados e a curva; ler premissas | Nada é restrito dentro da ferramenta: não há papéis |

Marina (nutricionista), Carlos (produtor) e o professor são **personas de produto**, não perfis do sistema. O mantenedor não é um perfil dentro da ferramenta; atua sobre arquivos.

### 8.2 Autenticação e autorização

- **Não existe autenticação nem autorização.** O servidor atende toda requisição que receba.
- A única barreira é o endereço de escuta (`127.0.0.1` por padrão). Não há validação de `Host`, de `Origin` ou de `Referer`, token ou limite de requisições.
- A ferramenta não recebe, não pede e não armazena credenciais.
- Consequência: o servidor não deve ser exposto à rede (D5). Ver seção 21.

---

## 9. Dados: Fontes, Estruturas e Persistência

**Banco de dados:** não se aplica. **Migrations:** não se aplicam. O equivalente funcional para evoluir os dados de referência é o procedimento da seção 20.

### 9.1 Alimento da biblioteca (`FeedInfo`)

Lido de `vendor/RuFaS/input/data/feed/NRC_comp.csv` e `user_feeds.csv` por `load_feed_library`. Excluem-se as categorias `Calf Liquid Feed` e `Starter` e os tipos `Milk` e `Starter`. Restam 130 alimentos.

| Campo | Origem | Regra |
|---|---|---|
| `id` | `rufas_id` | Identificador do alimento no RuFaS |
| `name` | `Name` (`user_feeds.csv`) | Espaços das pontas removidos; formato de título |
| `description` | `feed_description` | O texto "no" (sem diferença de maiúsculas) é tratado como vazio na exibição |
| `kind`, `category` | `feed_type`, `Fd_Category` | `Forage`, `Conc`, `Mineral`…; `Vitamin/Mineral` |
| `dm`, `cp`, `ndf`, `ee`, `tdn` | Colunas do CSV | DM em % da matéria natural; demais em % da MS |
| `calcium`, `phosphorus` | Colunas do CSV | % da MS |
| `default_price` | `DEFAULT_PRICES` | US$/kg MS, ilustrativo; nulo para alimentos sem preço padrão |
| `default_max` (derivado) | Seção 14.2 | kg MS/vaca/dia |
| `nel` (derivado) | `0,0245 · tdn − 0,12` | Mcal/kg MS; informativo |

### 9.2 Alimento selecionado (navegador)

`{ price, min, max }` por id: `price` em US$/kg MS; `min` e `max` em kg MS/vaca/dia. Estado `selected`, gravado em `dietopt.v1`.

### 9.3 Parâmetros da simulação (navegador)

| Campo | Padrão | Observação |
|---|---|---|
| `milkPrice` | 0,45 (US$/kg) | Vem de `/api/defaults` |
| `years` | 1 | A interface oferece 1 ou 2 |
| `maxReduction` | 5 (kg/vaca/dia) | Redução máxima de leite tolerada |

### 9.4 Cenário (`Scenario`)

| Campo | Padrão | Significado |
|---|---|---|
| `name` | — | Nome da pasta em `runs/`. Cenários da web: `web_<id da tarefa>`; sensibilidade: `web_<id>_s001`, `_s002`… |
| `start_date`, `end_date` | `2013:1`, `2013:365` | Período; `end_date` = `<2012 + anos>:365` |
| `random_seed` | 42 | Semente |
| `nutrient_standard` | `NRC` | `NRC` ou `NASEM` (a aplicação usa `NRC`) |
| `cow_num` | `None` | Número de vacas (60 a 500); `None` ou 100 mantém o rebanho do exemplo `freestall`. O rebanho todo e as baias são escalados junto (A.13) |
| `lac_cow_ration`, `ration_tolerance` | `None` | Ração com percentuais fixos (não usado pela aplicação) |
| `lac_cow_feeds` | `None` | Alimentos permitidos às vacas em lactação |
| `feed_limits` | `{}` | `id → (mínimo, máximo)` em kg/vaca/dia |
| `feed_prices` | `{}` | `id → US$/kg MS` |
| `milk_reduction_maximum` | `None` | kg/vaca/dia |
| `filters` | `{}` | Filtros de saída (nome → expressões regulares) |

### 9.5 Resultado da simulação (`SimulationResult`)

| Campo | Conteúdo |
|---|---|
| `days`, `milk_kg`, `milking_cows`, `avg_dim`, `fat_kg`, `protein_kg` | Séries diárias do rebanho |
| `interval_days`, `ration_kg_per_cow`, `requirements`, `cows_in_pen` | Uma entrada por intervalo de formulação da ração (30 dias): id do alimento → kg/vaca/dia (mais `dry_matter_intake_total`); exigências médias do lote; vacas no lote |
| `purchase_cost`, `purchase_amount` | Por alimento e intervalo |
| `wood` | Parâmetros `l`, `m`, `n` por paridade (1, 2, 3) |
| `total_milk_kg` (derivado) | Soma de `milk_kg` |

Gravado em `runs/_cache/<chave>.json` (`result_to_dict`) e lido por `result_from_dict`.

### 9.6 Avaliação econômica (`Evaluation`)

`name`, `ok`, `seconds`, `milk_kg`, `milk_revenue`, `feed_cost`, `lac_cost_per_cow_day`, `margin`, `ration` (id → kg MS/vaca/dia, média dos intervalos), `reduction` (leite perdido), `result` e `detail` (motivo da falha). Linha resumida (`as_row`): `cenario`, `ok`, `leite_kg` (arredondado), `receita` (2 casas), `custo_alimentacao` (2), `custo_vaca_dia` (3), `margem` (2), `segundos` (1).

### 9.7 Tarefa (`Job`)

| Campo | Conteúdo |
|---|---|
| `id` | 10 caracteres hexadecimais |
| `kind` | `simulate` ou `sensitivity` |
| `params` | Corpo da requisição |
| `status` | `queued`, `running`, `done`, `error` |
| `done`, `total` | Progresso |
| `result` | Resultado (somente em `done`) |
| `error` | Tipo, mensagem e parte do *traceback* (somente em `error`) |
| `created`, `finished` | Instantes (segundos desde a época) |

### 9.8 Dados do exercício do quadro

`Food { name, cost (US$/kg), nutrients (kg por kg), max_amount (kg) }`; `NutrientBounds { minimum, maximum }`; `DietResult { feasible, status, cost, amounts, nutrient_totals, shadow_prices, reduced_costs }`.

Valores iniciais da tela: **Arroz** (custo 1,50; carboidrato 0,77; proteína 0,08), **Milho** (custo 2,23; carboidrato 0,66; proteína 0,14); **Carboidrato** 6,0 a 9,5 kg; **Proteína** 0,9 a 1,6 kg.

### 9.9 Dados de referência no código

| Dado | Onde | Conteúdo |
|---|---|---|
| `DEFAULT_PRICES` | `scenarios.py` | 19 alimentos, US$/kg MS: farinha de sangue (23) 1,10; milho grão moído (44) 0,28; silagem de milho imatura (50) 0,09; silagem de milho meio maturação (51) 0,10; feno gramínea-leguminosa maduro (95) 0,18; silagem gramínea-leguminosa (104) 0,11; silagem de leguminosa (110) 0,12; farelo de arroz (138) 0,25; farelo de soja expeller (164) 0,60; farelo de soja 44% (166) 0,50; farelo de soja 48% (167) 0,55; soja grão (169) 0,62; carbonato de cálcio (230) 0,10; trigo laminado (194) 0,30; cevada laminada (8) 0,30; grãos de cervejaria secos (24) 0,22; caroço de algodão (58) 0,35; farelo de trigo (193) 0,20; farinha de alfafa (1) 0,20 |
| `DEFAULT_MILK_PRICE` | `scenarios.py` | 0,45 US$/kg |
| `DEFAULT_WOOD` | `lactation.py` | Paridade 1: `l` 15,72, `m` 0,2433, `n` 0,002445; paridade 2: `l` 22,06, `m` 0,235, `n` 0,003642; paridade 3: `l` 21,92, `m` 0,2627, `n` 0,004041 |
| `NASEM_ONLY_TO_NRC` | `rufas_adapter.py` | 301 → 230; 302 → 167 |
| `PRESET_BASE` | `AppProvider.tsx` | 50, 110, 44, 167, 138, 230, 23 |
| `PRESET_WIDE` | `AppProvider.tsx` | 50, 51, 110, 104, 95, 44, 47, 138, 167, 164, 169, 58, 193, 194, 24, 1, 230, 23 |
| `FALLBACK_PRICE` | `AppProvider.tsx` | Forage 0,12; Conc 0,35; Mineral 0,15 |

### 9.10 Dados pessoais e retenção

O sistema não coleta dados pessoais. O navegador guarda localmente a seleção de alimentos, preços e parâmetros; o disco guarda cenários, logs e cache. Nada é enviado para fora da máquina.

---

## 10. Telas e Componentes de Interface

O sistema tem **cinco telas**, todas dentro da mesma estrutura (barra lateral, cabeçalho, conteúdo, rodapé). Tema claro e escuro; verde como cor de marca; português do Brasil; números no formato brasileiro (vírgula decimal, ponto de milhar).

### 10.1 Estrutura da página

1. **Barra lateral recolhível:** marca "Dieta Ótima / com RuFaS"; grupo **Análise** (Exercício do quadro `/`, Vaca leiteira `/vaca`, Curva de lactação `/curva`, Sensibilidade `/sensibilidade`) e grupo **Projeto** (Premissas e limites `/sobre`); rodapé "RuFaS v1.0.6 · NRC 2001". Largura 16 rem (aberta), 3 rem (ícones), 18 rem (gaveta no celular). Atalho `Ctrl/Cmd + B`. Abaixo de 1.280 px vira gaveta.
2. **Cabeçalho fixo:** botão da barra lateral; *breadcrumb* "Dieta Ótima › <página>" (oculto em telas muito estreitas); selo de conexão; botão de tema.
3. **Conteúdo:** título, descrição e blocos da tela, com largura máxima de 1.440 px e margens de 16 px (24 px a partir de 640 px).
4. **Rodapé:** "Simulador: RuFaS v1.0.6 (GPLv3) · Exigências e composição: NRC (2001) · Preços ilustrativos, não são cotações." e "Interface adaptada do template AdminCN (shadcn/studio, licença MIT)."

### 10.2 Selo de conexão

| Estado | Texto | Estilo |
|---|---|---|
| Conectando | "conectando…" | Contorno |
| Conectado | "conectado · N alimentos NRC" | Contorno verde |
| Sem conexão | "sem conexão com o servidor" | Destrutivo |

Sem conexão, os botões de execução ficam desabilitados.

### 10.3 Tela 1: Exercício do quadro (`/`)

Título: "Exercício do quadro". Duas colunas a partir de 1.280 px.

| Bloco | Conteúdo |
|---|---|
| **Problema** | Fórmula "Minimizar Σ custo × quantidade, com mín ≤ Σ nutriente × quantidade ≤ máx para cada nutriente." Tabela **Alimentos** (Alimento, Custo (US$/kg), Carboidrato (kg/kg), Proteína (kg/kg), remover — o botão de remover só aparece com mais de 2 alimentos); botão **+ Alimento** (cria "Alimento N", custo 1, carboidrato 0,5, proteína 0,1). Tabela **Nutrientes** (Mínimo (kg), Máximo (kg)). Botão **Resolver** ("Resolvendo…" durante a chamada) |
| **Solução ótima** | "Clique em “Resolver”." antes da primeira solução. Se inviável: bloco "**Sem solução viável.** Os limites mínimo e máximo são incompatíveis com os alimentos disponíveis." Se viável: indicadores "Custo mínimo por dia" (US$, 2 casas) e "Alimentos usados" (com "de N disponíveis"); tabela Alimento/Quantidade (kg, 3 casas)/Custo; tabela Nutriente/Total/Faixa/Restrição/Preço-sombra; nota "Preço-sombra: quanto o custo ótimo aumenta se o mínimo do nutriente subir 1 kg."; gráfico de barras "kg por dia" |
| **Cenários e sensibilidade** | Dois fatores (Fator 1 e Fator 2, cada um com seleção do alvo, **De**, **Até** e **Níveis**, mínimo 2); botão **Gerar cenários** ("Gerando…"); tabela com colunas `Sn`, um por fator, "Res (US$/dia)" em mapa de calor e "Dieta ótima" (texto "Alimento x,xx kg · …") |

Regras de exibição:

- Resolve sozinho na primeira visita, quando a conexão fica ativa e ainda não há solução.
- Restrição: "mínimo ativo" ou "máximo ativo" (selo) se o total difere do limite por menos de 1e-6; senão "folga". Preço-sombra mostrado como "US$ x,xx/kg" só para o mínimo (traço se zero ou ausente).
- Alvos disponíveis dos fatores: `Custo · <alimento>`, `Mínimo · <nutriente>`, `Máximo · <nutriente>`. Valores iniciais: Fator 1 = custo do Arroz, de 1 a 2, 3 níveis; Fator 2 = custo do Milho, de 1,8 a 2,6, 3 níveis.
- Linha inviável mostra "inviável" em vermelho na coluna `Res`.
- Máximo de nutriente vazio é enviado como 1e9 (sem limite superior prático).

### 10.4 Tela 2: Vaca leiteira (`/vaca`)

Título: "Vaca leiteira (RuFaS)". Painel lateral de 23 rem à esquerda; resultados à direita.

**Painel "Cenário"** (descrição "Preços em US$/kg de matéria seca; limites em kg de MS por vaca por dia."):

| Componente | Comportamento |
|---|---|
| Preço do leite (US$/kg) | Campo numérico; padrão 0,45 |
| Período simulado | Seleção: "1 ano" ou "2 anos" |
| Redução máxima de leite tolerada (kg/vaca/dia) | Campo numérico, passo 0,25, mínimo 0; texto de apoio: "Se a ração não atende às exigências, o RuFaS reduz o leite (0,25 kg por tentativa) até este limite; acima dele a simulação aborta." |
| Seletor de alimentos | Botões **Conjunto base** e **Lista ampla**; busca "Buscar alimento (soja, arroz, milho…)"; lista rolável (altura máxima 15 rem) com caixa de seleção, título do alimento e "tipo · PB x% · FDN x% · NEL x,xx Mcal/kg"; até 60 resultados, com a nota "Mostrando 60 de N. Refine a busca."; "Nenhum alimento encontrado." quando vazio |
| Selecionados (N) | Cartão por alimento com o nome completo, botão de remover e três campos: **US$/kg MS**, **mín. kg/dia**, **máx. kg/dia**. Sem seleção: "Nenhum alimento selecionado." |
| Botão **Simular com o RuFaS** | Largura total; "Simulando…" e desabilitado durante a execução; barra de progresso abaixo |

A busca casa o texto (sem diferença de maiúsculas) com o título do alimento ou o tipo. O título é "nome — descrição", ou só o nome se a descrição for vazia.

**Resultados** (após a primeira simulação; antes, um quadro com o ícone de trigo e o texto "Escolha os alimentos e clique em “Simular com o RuFaS”. Cada simulação leva de 30 a 60 segundos."):

| Bloco | Conteúdo |
|---|---|
| Indicadores | "Margem sobre custo de alimentação" (destaque verde, US$ sem casas); "Receita do leite"; "Custo de alimentação (rebanho)"; "Custo da ração, vaca em lactação" (US$ x,xx/dia); "Leite por vaca" (kg/dia, 1 casa); "Leite total" (t, sem casas); e, se a redução de leite for maior que 0,005, "Leite perdido por ração insuficiente" (−x,xx kg/vaca/dia; dica "O RuFaS reduziu o leite para fechar a ração.") |
| Alerta | Se houver leite perdido: "**A ração não atendeu a todas as exigências** — Para continuar a simulação, o RuFaS reduziu a produção de leite em média x,xx kg por vaca por dia (limite configurado: x,xx). Revise os alimentos, os preços e os limites." |
| **Ração das vacas em lactação** | Barras empilhadas por intervalo de 30 dias ("dia N"), kg de MS por vaca por dia; só alimentos com mais de 0,001 kg em algum intervalo; ordenados pela quantidade média (o maior recebe `chart-1`); legenda |
| **Composição média** | Tabela Alimento / kg MS/dia / % MS / US$/dia, ordenada por quantidade, só alimentos acima de 0,001 kg; rodapé "Total" (soma dos kg, 100%, custo da ração por vaca por dia) |
| **Exigências (NRC 2001)** | Linhas por intervalo: "NEL exigida (Mcal/dia)" e "DMI estimado (kg/dia)" no eixo esquerdo; "Proteína metabolizável (g/dia)" no direito |
| **Leite do rebanho** | Linha diária "Leite do rebanho (kg/dia)" e tracejado "Vacas em lactação" no eixo direito |

"Leite por vaca" = leite total ÷ (média de vacas em lactação × número de dias da série).

### 10.5 Tela 3: Curva de lactação (`/curva`)

| Bloco | Conteúdo |
|---|---|
| Cabeçalho | Selo no topo: "parâmetros calibrados pela simulação RuFaS" (verde) ou "parâmetros de referência" |
| Campos | **PEV (dias)** (padrão 60, mínimo 0), **Gestação (dias)** (270, mínimo 200), **Secagem antes do parto (dias)** (60, mínimo 0) |
| Gráfico | Uma curva por paridade ("1ª lactação", "2ª lactação", "3ª ou mais"); eixos "dias em lactação" e "kg/vaca/dia"; faixa sombreada do PEV ao parto rotulada "gestação N d"; linhas tracejadas "PEV (N d)", "secagem (N d)" e "parto (N d)"; dica "dia N" |
| Resumo | Um cartão por paridade: pico em kg e "pico no dia N · x,x t em 305 dias" |

Regras: PEV + gestação = dia do parto; secagem = parto − dias de secagem; eixo X vai até o maior entre 330 e parto + 15. Sem simulação, usa os parâmetros de `/api/lactation`; após uma simulação, usa os da simulação (`wood_from_rufas`). A descrição da página informa: "Rode uma simulação na aba Vaca leiteira para usar os parâmetros calibrados pelo RuFaS." quando não calibrado.

### 10.6 Tela 4: Sensibilidade (`/sensibilidade`)

Título: "Sensibilidade (RuFaS)". Painel "Fatores" à esquerda; resultados à direita.

| Componente | Comportamento |
|---|---|
| Lista de fatores | Uma linha por alimento selecionado na tela da vaca e uma para "Preço do leite (US$/kg)": caixa de seleção, nome, **De** e **Até**. Padrões: marcados apenas farelo de arroz (138), milho (44), se selecionados, e o leite; alimentos de ±50% do preço atual (De = 0,5×, Até = 1,5×); leite de ±20% (0,8× e 1,2×) |
| Método | "Grade (todas as combinações)" ou "Hipercubo latino" |
| Níveis / amostras | Campo numérico, padrão 3; efetivo limitado a 2–12 |
| Estimativa | "N cenários, até M simulações do RuFaS (cerca de K min)." ou "Marque ao menos um fator." |
| Botão **Rodar sensibilidade** | "Rodando…" durante a execução; desabilitado sem fatores marcados, sem conexão ou com menos de 3 alimentos selecionados; barra de progresso |

Resultados (antes: ícone e "Defina os fatores e rode a análise."):

| Bloco | Conteúdo |
|---|---|
| **Tabela de cenários** | Colunas: `Sn`, uma por fator, "Res (US$)" (mapa de calor), "US$/vaca/dia", "Leite perdido" (em âmbar, "−x,xx", ou traço), "Ração (kg MS/vaca/dia)" (até 4 alimentos de maior quantidade). Cenário falho: "falhou" em vermelho em `Res` (a causa na dica) e o erro na coluna da ração |
| **Efeito sobre a margem** | Barras horizontais de Spearman (−1 a +1), verde para efeito positivo e vermelho para negativo; fatores sem efeito calculável ficam de fora |
| **Margem por cenário** | Barras de `Res` por `Sn`, só cenários válidos |

Estimativa: pontos = `n^k` (grade, k = fatores marcados) ou `n` (latin); simulações = `n^(fatores de alimento)` (grade) ou `n` (latin); tempo = `⌈simulações × 17 s ÷ 60⌉` minutos, no mínimo 1 (D2).

### 10.7 Tela 5: Premissas e limites (`/sobre`)

Quatro cartões de texto, em duas colunas a partir de 1.280 px:

1. **Como o sistema funciona** — "Do cenário à margem."
2. **O que o modelo assume**
3. **O que ele não faz** — inclui "Os preços iniciais são ilustrativos, não cotações. Troque pelos seus.", ausência de balanço de nutrientes, de exportação e do NASEM, e a possibilidade de o otimizador não convergir ("falhou" ou "leite perdido", nunca resultado válido).
4. **Créditos e licenças** — RuFaS v1.0.6 (GPLv3, sem modificações), NRC 2001, template AdminCN (MIT).

### 10.8 Identidade visual consolidada

**Paleta (claro / escuro, em `oklch`; hexadecimal aproximado):**

| Papel | Claro | Escuro | Uso |
|---|---|---|---|
| Fundo | `oklch(1 0 0)` `#ffffff` | `oklch(0.145 0 0)` `#0a0a0a` | Página |
| Texto | `oklch(0.145 0 0)` `#0a0a0a` | `oklch(0.985 0 0)` `#fafafa` | Texto principal |
| Cartão | `oklch(1 0 0)` | `oklch(0.205 0 0)` `#171717` | Superfícies |
| Primária (verde) | `oklch(0.46 0.1 160)` `#0c6944` | `oklch(0.72 0.15 160)` `#2fc183` | Ações, destaque, margem, item ativo |
| Texto secundário | `oklch(0.556 0 0)` `#737373` | `oklch(0.708 0 0)` `#a1a1a1` | Descrições, dicas |
| Destrutiva | `oklch(0.577 0.245 27.325)` `#e7000b` | `oklch(0.704 0.191 22.216)` `#ff6467` | Erro, inviável, falhou |
| Aviso (fundo) | `oklch(0.72 0.15 70)` `#df911a` | `oklch(0.8 0.15 75)` `#f5ae39` | Indicador "leite perdido" |
| Aviso (texto) | `oklch(0.5 0.12 65)` `#915200` | `oklch(0.82 0.13 80)` `#f0ba59` | Texto de aviso legível |
| Gráficos 1 a 8 | verde, âmbar, azul, rosa-vermelho, violeta, turquesa, oliva, rosa | versões mais claras | Séries |

**Tipografia:** Geist Sans. Título da página 24 px, peso 600; título de cartão 16 px, peso 500; texto de apoio e tabelas 14 px; rótulos e dicas 12 px (11 px em campos compactos); valor de indicador 24 px, peso 600; números com dígitos tabulares.

**Forma e espaço:** raio base 10 px (cartões 14 px); espaço entre blocos 24 px; entre indicadores 12 px; padding de cartão 24 px (16 px nos indicadores); campo numérico com 32 px de altura. Hierarquia por camadas tonais e bordas de 1 px, sem sombras relevantes.

**Botões:** variantes `default` (verde sólido), `outline`, `ghost` e `secondary`; altura 36 px, 32 px (`sm`). O botão de executar leva o ícone de play.

**Mapa de calor (`Res`):** fundo de 8% a 40% da cor primária proporcional ao valor (o teto de 40% mantém o contraste de texto ≥ 4,5:1 no tema escuro). Na tela do exercício a escala é invertida (menor custo = mais intenso).

**Estados:** sucesso (verde), erro (vermelho), aviso do modelo (âmbar), carregamento (barra de progresso). A cor nunca é o único canal: os estados também têm texto ou número.

**Acessibilidade implementada:** idioma `pt-BR`; rótulos acessíveis em campos e botões de ícone; progresso anunciado (`role='status'`, `aria-live='polite'`); foco visível herdado do shadcn/Base UI; respeito ao tema do sistema.

### 10.9 Regras de exibição

- Antes da primeira conexão, a lista de alimentos está vazia e os botões de execução ficam desabilitados.
- Valores numéricos ausentes ou inválidos aparecem como "—".
- Resultados de simulação e de sensibilidade permanecem na tela até serem substituídos ou a página ser recarregada. **Não** indicam a que parâmetros correspondem (D1).
- Texto de cabeçalho e rótulos usam as grafias desta seção.

---

## 11. API Local

Servidor HTTP em `http://127.0.0.1:8000` (porta e endereço configuráveis por `--port` e `--host`). Corpos JSON em UTF-8 (`ensure_ascii=False`); todas as respostas levam `Cache-Control: no-store`. `NaN` e infinito são trocados por `null`.

### 11.1 Verificação de cada requisição

1. `HEAD` é tratado como `GET` sem corpo (o Next.js pré-carrega rotas com `HEAD`).
2. `GET` e `POST` são roteados pelo caminho (sem consulta). `POST` lê o corpo pelo `Content-Length` e o interpreta como JSON (vazio = `{}`).
3. Não há verificação de `Host`, `Origin`, token ou limite de requisições (D5).
4. Qualquer exceção durante o atendimento vira resposta 500 `{"error": "<Tipo>: <mensagem>"}`; o servidor continua atendendo.

### 11.2 Endpoints

| Método e rota | Corpo | Resposta de sucesso |
|---|---|---|
| `GET /api/feeds` | — | 200: lista ordenada por (tipo, nome) com `id`, `name`, `description`, `kind`, `category`, `dm`, `cp`, `ndf`, `ee`, `tdn`, `calcium`, `phosphorus`, `default_price`, `nel` (3 casas), `default_max` |
| `GET /api/defaults` | — | 200: `{ milk_price, prices }`, com `prices` indexado por id (texto) |
| `GET /api/lactation` | — | 200: `{ curves, wood, milestones }`; `curves` = paridade → 330 valores diários; `milestones` = `{ pev: 60, proximo_parto: 330, secagem: 270 }` |
| `GET /api/jobs` | — | 200: lista de tarefas sem resultado, da mais recente para a mais antiga |
| `GET /api/jobs/<id>` | — | 200: tarefa com `result`; 404 `{"error": "job não encontrado"}` |
| `POST /api/toy` | `{ foods: [{ name, cost, nutrients: { <nutriente>: <kg/kg> }, max? }], bounds: { <nutriente>: { min, max? } } }` | 200: `{ feasible, status, cost, amounts, nutrient_totals, shadow_prices, reduced_costs }` |
| `POST /api/toy/sensitivity` | `{ problem: <corpo de /api/toy>, factors: [{ target, low, high, n }] }`, com `target` = `cost:<alimento>`, `min:<nutriente>` ou `max:<nutriente>` | 200: `{ columns, rows }`; cada linha: `cenario`, um valor por alvo, `Res` (4 casas, ou `null`), `amounts` |
| `POST /api/jobs/simulate` | `{ feeds: [ids], prices?, limits?, milk_price?, years?, max_milk_reduction?, seed?, cow_num? }` | 202: tarefa (`id`, `kind`, `status`, `done`, `total`, `error`, `created`, `finished`), sem resultado |
| `POST /api/jobs/sensitivity` | O mesmo corpo de simulação mais `{ factors: [{ key, label, low, high }], method?, n?, workers? }` | 202: tarefa, sem resultado |
| qualquer outro `POST` | — | 404 `{"error": "rota não encontrada"}` |
| `GET` fora da API | — | Arquivo de `frontend/` ou 404 em texto "nao encontrado" |

**Parâmetros da simulação:** `feeds` é obrigatório (lista de ids); `prices` (id → US$/kg MS), `limits` (id → [mín, máx]); `milk_price` (padrão 0,45); `years` (padrão 1, limitado a 1–3); `max_milk_reduction` (padrão 5,0); `seed` (padrão 42); `cow_num` (opcional). Chave obrigatória ausente gera 500 com `KeyError`.

**Resultado de `simulate`:**

| Campo | Conteúdo |
|---|---|
| `summary` | `cenario`, `ok`, `leite_kg`, `receita`, `custo_alimentacao`, `custo_vaca_dia`, `margem`, `segundos`, `milk_price`, `reducao_leite`, `max_reducao` |
| `feeds` | `[{ id, label, price }]` dos alimentos que aparecem na ração |
| `daily` | `day`, `milk_kg`, `milking_cows`, `avg_dim` |
| `intervals` | `day`, `ration` (lista de id → kg), `cows`, `requirements` (`NEl_requirement`, `NEmaint_requirement`, `MP_requirement`, `Ca_requirement`, `P_req`, `DMIest_requirement`, `avg_BW`), `cost_per_cow_day` |
| `lactation` | `curves`, `wood`, `wood_from_rufas`, `milestones` |
| `average_ration` | id → kg MS/vaca/dia |

**Resultado de `sensitivity`:** `columns` (rótulos dos fatores + `Res`), `rows` (ver 15.2), `effects` (`[{ fator, spearman }]`), `feeds` (`[{ id, label }]` dos alimentos selecionados).

### 11.3 Códigos de erro

| Código | Corpo | Causa |
|---|---|---|
| 404 | `{"error": "job não encontrado"}` | Id de tarefa inexistente |
| 404 | `{"error": "rota não encontrada"}` | `POST` em rota desconhecida |
| 404 (texto) | `nao encontrado` | `GET` de arquivo inexistente ou fora de `frontend/` |
| 500 | `{"error": "<Tipo>: <mensagem>"}` | Exceção no atendimento (JSON inválido, chave ausente, valor inválido…) |

Os códigos 400, 401, 403, 421 e 429 não são usados.

---

## 12. Integrações Externas

### 12.1 RuFaS (simulador)

- **Natureza:** execução de `main.py` do RuFaS v1.0.6 em subprocesso, com `vendor/RuFaS` como diretório de trabalho e `PYTHONIOENCODING=utf-8`. Entrada e saída por arquivos. Não é uma API HTTP.
- **Comando:** `<python do .venv> main.py -p <task_manager_metadata> -g -s -o <runs/<nome>/out> -l <runs/<nome>/tm_logs>`, com todos os caminhos relativos a `vendor/RuFaS` e com barras normais. Tempo limite de 3600 s.
- **Arquivos de entrada escritos em `runs/<nome>/`:** `config.json`, `animal.json`, `feed.json`, `NRC_comp.csv`, `metadata.json`, `tasks.json`, `task_manager_metadata.json` e `filters/json_<grupo>.json` (um por grupo de filtro: `herd`, `lac_ration`, `purchases`, `lactation`). Partem das cópias do exemplo `freestall` (`example_freestall_config.json`, `example_freestall_animal.json`, `example_Midwest_feed.json`, `example_freestall_dairy_metadata.json`, `task_manager_metadata.json`) e da biblioteca `NRC_comp.csv` do RuFaS.
- **Edições feitas pelo adaptador:**
  - `config`: `start_date`, `end_date`, `random_seed`, `nutrient_standard`.
  - `animal`: `herd_information.cow_num` (se informado); `ration.user_input = (lac_cow_ration não nulo)`.
  - `feed`: para NRC, troca de ids 301 → 230 e 302 → 167 em todo campo `feed_type`, `purchased_feed` e `*_feeds`; `lac_cow_feeds` = alimentos escolhidos (ordenados); `purchased_feeds[].purchased_feed_cost` = preço (alimentos novos entram com `buffer` 0,15 e limites de compra `runtime`, `advance` e `planning` de 1000); `milk_reduction_maximum`.
  - `NRC_comp.csv`: colunas `lower_limit` e `limit` de cada alimento com limite definido (kg/animal/dia).
  - `tasks`: uma tarefa `SIMULATION_SINGLE_RUN`, `parallel_workers` 1, `log_verbosity` `errors`, diretórios de saída dentro de `runs/<nome>/`.
- **Sucesso:** código de saída 0 **e** a linha `Finished task: 1/1 with 0 error(s)` no console. A saída completa vai para `runs/<nome>/console.log`.
- **Falha:** o motivo é a última linha do console que começa com `...Error` ou `...Exception`; na falta, os últimos 300 caracteres.
- **Saídas lidas** (filtros `RESULT_FILTERS`, expressões regulares sobre `Classe.função.variável`):
  - `herd`: `daily_milk_production`, `milking_cow_num`, `avg_days_in_milk`, `herd_milk_fat_kg`, `herd_milk_protein_kg` (`report_herd_statistics_data`);
  - `lac_ration`: `ration_per_animal_for_LAC_COW`, `avg_rqmts_for_LAC_COW`, `ration_nutrient_amount_for_LAC_COW`;
  - `purchases`: `FeedManager.purchase_feed.ration_interval_*` (`_cost` e `_amount_purchased` por alimento);
  - `lactation`: `LactationCurve.__init__.parity_<n>_lactation_curve_parameter__<l|m|n>`.
- **Comportamento do RuFaS relevante:** o otimizador SLSQP formula a ração de custo mínimo; se inviável, reduz o leite em 0,25 kg por tentativa até `milk_reduction_maximum`; acima disso aborta. O leite segue a curva de Wood e só cai por esse mecanismo.

### 12.2 HiGHS (via SciPy)

Solucionador do PL do exercício do quadro (`scipy.optimize.linprog`, `method="highs"`). Execução local, sem rede.

### 12.3 Dados nutricionais (NRC 2001)

A composição dos alimentos vem das tabelas do RuFaS (`NRC_comp.csv`, `user_feeds.csv`). O PDF da NRC não é lido pelo sistema. O NASEM 2021 não é oferecido (especificado no Anexo A, RF-24).

### 12.4 Preços de mercado

Não há integração. Os preços iniciais são constantes ilustrativas; o usuário os digita.

### 12.5 Fonte tipográfica

Arquivos locais (pacote `geist`). Nenhuma requisição externa em tempo de uso.

---

## 13. Fluxos Funcionais

### F1. Instalar o ambiente

- **Perfil:** usuário (uma vez por máquina).
- **Pré-condições:** Windows; Python 3.12 (`py -3.12`); Git; internet.
- **Passo a passo:** executar `scripts\setup.ps1`: clona o RuFaS v1.0.6, cria `.venv`, instala as dependências (com contorno via `curl` se o `pip` falhar); a última linha é "Pronto. Inicie com iniciar.bat".
- **Resultado esperado:** `.venv` e `vendor/RuFaS` prontos.
- **Erros possíveis:** "Python 3.12 nao encontrado. Instale com: winget install Python.Python.3.12"; falha de rede.
- **Logs:** saída do PowerShell.

### F2. Iniciar o sistema

- **Perfil:** usuário.
- **Pré-condições:** F1 concluído; porta 8000 livre.
- **Passo a passo:** executar `iniciar.bat`; ele abre `http://127.0.0.1:8000` no navegador e inicia o servidor em `backend/`. O servidor escreve "Servidor em http://127.0.0.1:8000  (Ctrl+C para parar)" no console. A interface carrega `/api/feeds` e `/api/defaults`; com sucesso, o selo mostra "conectado · N alimentos NRC", a seleção anterior (ou o "Conjunto base") é aplicada e o exercício do quadro é resolvido.
- **Resultado esperado:** interface conectada.
- **Erros possíveis:** porta 8000 ocupada (o servidor não sobe); servidor fechado (selo "sem conexão com o servidor" e botões desabilitados; **não há nova tentativa automática**: é preciso iniciar o servidor e recarregar a página).
- **Logs:** console do servidor.

### F3. Resolver o exercício do quadro

- **Perfil:** professor, estudante.
- **Pré-condições:** servidor ativo.
- **Passo a passo:** abrir a tela 1 (resolve sozinha na primeira visita); editar custos, composição ou limites; acionar **Resolver**.
- **Resultado esperado:** com os valores iniciais, custo mínimo US$ 15,35 por dia, arroz 4,473 kg, milho 3,873 kg; carboidrato e proteína com "mínimo ativo".
- **Erros possíveis:** inviável (bloco "Sem solução viável."); erro de rede (aviso com a mensagem); nomes de alimento repetidos (D3).
- **Logs:** nenhum.

### F4. Gerar a tabela de cenários do quadro

- **Passo a passo:** escolher dois fatores diferentes, faixas e níveis; acionar **Gerar cenários**.
- **Resultado esperado:** `n₁ × n₂` linhas `S1…SN`, `Res` em mapa de calor e a dieta ótima de cada linha.
- **Erros possíveis:** fatores iguais ("Escolha dois fatores diferentes."); fator que aponta para alimento renomeado ou removido (D4).

### F5. Montar e simular uma vaca leiteira

- **Perfil:** nutricionista, produtor.
- **Pré-condições:** servidor ativo; ao menos 3 alimentos selecionados.
- **Passo a passo:**
  1. Abrir a tela 2; escolher "Conjunto base", "Lista ampla" ou buscar e marcar alimentos.
  2. Ajustar preço, mínimo e máximo de cada alimento; definir preço do leite, período e redução máxima.
  3. Acionar **Simular com o RuFaS**. A interface cria a tarefa, mostra a barra de progresso ("Na fila…" ou "Simulando no RuFaS…") e consulta o estado a cada 1,5 s.
  4. Ao terminar: aviso "Simulação concluída." e resultados (seção 10.4).
  5. Alterar só o preço do leite e simular de novo: resultado em segundos (cache).
- **Resultado esperado:** seis indicadores, ração, composição, exigências e leite diário.
- **Erros possíveis:** menos de 3 alimentos (aviso "Selecione pelo menos 3 alimentos (um volumoso, um concentrado e um mineral)."); falha do RuFaS (F8); leite perdido (F8).
- **Logs:** `runs/web_<id>/console.log`.

### F6. Rodar a sensibilidade

- **Pré-condições:** os mesmos de F5.
- **Passo a passo:**
  1. Abrir a tela 4; marcar fatores e ajustar faixas; escolher método e níveis; conferir a estimativa.
  2. Acionar **Rodar sensibilidade**; acompanhar "x de y simulações do RuFaS concluídas".
  3. Ao terminar: aviso "Análise concluída." e resultados (seção 10.6).
- **Resultado esperado:** tabela `S1…SN` com `Res`, efeito de Spearman e margem por cenário.
- **Erros possíveis:** cenário que falha aparece como "falhou" sem derrubar a análise; falha geral da tarefa (aviso "Falha na análise" ou a primeira linha do erro).
- **Logs:** `runs/web_<id>_sNNN/console.log` por simulação.

### F7. Ver a curva de lactação

- **Passo a passo:** abrir a tela 3; ajustar PEV, gestação e secagem. Para usar os parâmetros calibrados, simular antes (F5).
- **Resultado esperado:** curvas por paridade com marcos; selo da origem dos parâmetros.

### F8. Falha de simulação e leite perdido

- **Falha total:** o RuFaS termina sem sucesso (seção 12.1). Na simulação única, a tarefa fica em `error` e a interface mostra um aviso com a primeira linha da mensagem ("RuntimeError: Simulação do RuFaS falhou: <detalhe>"); o resultado anterior, se houver, permanece na tela (D1). Na sensibilidade, o cenário vira linha com `Res = null` ("falhou"), sem zeros.
- **Leite perdido:** o RuFaS reduziu o leite para fechar a ração; aparecem o indicador âmbar e o alerta (seção 10.4).
- **Ação do usuário:** revisar alimentos, preços, limites ou aumentar a redução máxima; detalhes em `runs/<nome>/console.log`.

### F9. Servidor indisponível

- **Passo a passo:** se o servidor cair durante o uso, chamadas falham e o aviso mostra a mensagem do erro de rede; o selo continua "conectado" até recarregar (a conexão só é verificada ao carregar). Reiniciar com `iniciar.bat` e recarregar.
- **Efeito:** tarefas em andamento são perdidas; simulações concluídas continuam no cache.

### F10. Atualizar a interface (mantenedor)

- **Pré-condições:** Node 20.9+.
- **Passo a passo:** editar `web/src/`; executar `scripts\build-web.ps1`: copia `web/` para `%LOCALAPPDATA%\dietopt-web-build`, instala dependências, compila e publica em `frontend/` (na primeira vez move o `frontend` existente para `frontend_legacy`, depois apenas o substitui); atualiza o `package-lock.json` em `web/`.
- **Resultado esperado:** `frontend/` atualizado, servido pelo servidor Python (recarregar a página).

---

## 14. Validações e Regras de Negócio

### 14.1 Exercício do quadro

- Minimiza `Σ custo_i · x_i` sujeito a `mínimo_j ≤ Σ q_ij · x_i ≤ máximo_j` para cada nutriente `j`, com `0 ≤ x_i ≤ máximo_i`. Resolvido por HiGHS.
- Restrição de máximo só entra se o máximo for finito; restrição de mínimo só entra se o mínimo for maior que zero. Máximo de nutriente vazio na tela vira 1e9.
- Sem solução: `feasible = false` e a mensagem do solucionador; sem resultado parcial.
- **Preço-sombra** (chaves `<nutriente>_min` e `<nutriente>_max`): variação do custo ótimo por unidade adicional do limite, com o sinal ajustado para o mínimo. `reduced_costs`: custo reduzido por alimento.
- **Cenários do quadro:** dois fatores obrigatoriamente diferentes; cada fator tem `n` níveis igualmente espaçados de `low` a `high` (`n` efetivo ≥ 2 na tela; o servidor usa `max(n − 1, 1)` no passo); as linhas são o produto cartesiano; `Res` = custo ótimo (4 casas) ou `null` se inviável.
- O exercício exige no mínimo 2 alimentos; os nomes dos alimentos devem ser únicos (não validado, D3).

### 14.2 Biblioteca e tetos de inclusão padrão

| Condição (nesta ordem) | Teto (kg MS/vaca/dia) |
|---|---|
| `kind = Mineral` ou categoria `Vitamin/Mineral` | 0,6 |
| `ee ≥ 80` (gorduras) | 0,9 |
| `cp ≥ 60` (farinhas proteicas) | 1,0 |
| demais | 100 (sem teto prático) |

O teto vale quando o usuário não informa limite (`feed_limits_from`); na interface, é o valor inicial do campo **máx. kg/dia**. O mínimo inicial é 0.

### 14.3 Preços

- Preço inicial de um alimento selecionado na interface: preço de `/api/defaults` → `default_price` da biblioteca → `FALLBACK_PRICE` do tipo (Forage 0,12; Conc 0,35; Mineral 0,15) → 0,30.
- A interface sempre envia o preço de todos os alimentos selecionados; campo vazio vira 0,30.
- No servidor, os preços do usuário sobrepõem `DEFAULT_PRICES`. Um alimento **sem preço em nenhuma fonte** entra no custo a US$ 0.
- Campos vazios de mínimo viram 0; de máximo, 100; preço do leite, 0,45; redução máxima, 5.

### 14.4 Montagem do cenário

- Período: `years` limitado a 1–3; simulação de `2013:1` a `<2012 + anos>:365`. A interface oferece 1 ou 2 anos.
- Padrão nutricional sempre `NRC`; ids 301 e 302 do exemplo trocados por 230 e 167.
- Ração: o sistema não impõe percentuais; informa apenas a lista de alimentos permitidos (`lac_cow_feeds`).
- Limites: do usuário ou `[0, teto]`; gravados em `lower_limit` e `limit` de `NRC_comp.csv`, em kg/animal/dia.
- Redução máxima de leite: valor do usuário, padrão 5,0.
- Semente 42; rebanho do exemplo `freestall`, salvo `cow_num`.
- Todo caminho passado ao RuFaS é relativo a `vendor/RuFaS`.
- A pasta `runs/<nome>/` é apagada e recriada se já existir.

### 14.5 Execução e falha

Seção 12.1. Resumo: sucesso = código 0 + linha de resumo; falha nunca vira resultado zerado; o motivo é exibido e o detalhe fica em `console.log`.

### 14.6 Cache

- Chave: SHA-1 (16 primeiros caracteres) do conteúdo do cenário **sem** `name` e `filters`, serializado com chaves ordenadas.
- Se `runs/_cache/<chave>.json` existe, devolve-se o resultado sem executar o RuFaS (`seconds = 0`, `detail = "cache"`). Só execuções bem-sucedidas são gravadas.
- Mudar preço ou limite de alimento, lista de alimentos, período, semente ou redução máxima gera nova chave. Mudar só o preço do leite não altera o cenário.
- A chave não considera a versão do RuFaS nem o conteúdo das tabelas de entrada (D6).

### 14.7 Tarefas e concorrência

- Cada requisição de simulação ou sensibilidade cria uma tarefa e a executa em uma thread.
- Um bloqueio global permite **uma tarefa por vez**; as demais ficam `queued`.
- Qualquer exceção na tarefa vira `status = error` com tipo, mensagem e parte do *traceback*; `finished` é sempre preenchido.
- Na sensibilidade, as simulações rodam em lotes de até `workers` (padrão 2) em paralelo.
- As tarefas não são removidas da memória.

### 14.8 Entradas da interface

- Simular exige pelo menos 3 alimentos selecionados.
- Sensibilidade: botão desabilitado sem fatores marcados, sem conexão ou com menos de 3 alimentos.
- Níveis/amostras da sensibilidade limitados a 2–12.
- Campos numéricos aceitam vazio durante a edição; antes de enviar, valores inválidos são trocados pelo padrão (`finite()`).
- Nenhuma validação bloqueia a digitação; a validação final está no servidor, que é mínima (D4).

### 14.9 Conexão

- Ao carregar, a interface busca `/api/feeds` e `/api/defaults`. Sucesso: "conectado". Falha: "sem conexão com o servidor". Não há nova tentativa nem verificação periódica.
- Sem conexão, os botões de execução ficam desabilitados.

### 14.10 Persistência no navegador

- `dietopt.v1` é gravado a cada alteração de `selected` ou `params`, quando conectado.
- Ao abrir: restaura `selected` se houver ao menos um alimento; restaura `params` se existirem; caso contrário, aplica o "Conjunto base" e os padrões.
- Falha de leitura ou escrita do `localStorage` é ignorada.

---

## 15. Cálculos e Modelos

### 15.1 Economia da simulação (`evaluate`)

Para cada simulação bem-sucedida:

| Grandeza | Cálculo |
|---|---|
| `receita` | `leite_total_kg × preço_do_leite` |
| `custo_de_alimentação` | `Σ_alimentos ( Σ quantidade comprada no período × preço do alimento )`, para todo o rebanho |
| **`margem`** | `receita − custo_de_alimentação` |
| `custo da ração por vaca por dia` | para cada intervalo, `Σ kg × preço` da ração por vaca (sem `dry_matter_intake_total`); média dos intervalos |
| `ração média` | média, entre intervalos, dos kg MS/vaca/dia de cada alimento |
| `reduction` (leite perdido) | média, entre intervalos, de `avg_milk_production_reduction_pen` |

Preços: `DEFAULT_PRICES` com os do usuário sobrepostos; ausência = 0. Se a simulação falha, a avaliação sai com `ok = false`, sem valores numéricos e com o motivo em `detail`.

Arredondamentos da linha resumida: `leite_kg` inteiro; `receita` e `custo_alimentacao` 2 casas; `custo_vaca_dia` 3; `margem` 2; `segundos` 1.

### 15.2 Sensibilidade (`run_sensitivity`)

- **Fatores:** `Factor { key, label, low, high }`; `key` é o id do alimento (preço, exige simulação) ou `milk_price` (só altera a receita).
- **Pontos:** `grid` gera `max(n, 2)` níveis igualmente espaçados por fator e o produto cartesiano (`n^k` pontos); `latin` gera `n` amostras, uma por estrato de cada fator (semente 42).
- **Simulações únicas:** pontos com os mesmos preços de alimento (arredondados a 4 casas) compartilham uma única simulação; fatores de leite não geram simulação. Cenários nomeados `<nome>_s001`, `_s002`…
- **Execução:** em lotes de `workers` simulações; o progresso é "feitas de total". Cada simulação passa pelo cache.
- **Linha `Sn`:**

| Campo | Conteúdo |
|---|---|
| `cenario` | `S1`…`SN` |
| um por fator | Valor do ponto (4 casas), na chave igual ao `label` do fator |
| `leite_kg`, `receita` (= leite × preço do leite do ponto), `custo_alimentacao`, `custo_vaca_dia`, `reducao_leite` | Da avaliação da simulação correspondente |
| `Res` | `receita − custo_alimentacao` (2 casas) |
| `ration` | Alimentos com mais de 0,001 kg MS/vaca/dia (3 casas) |
| (falha) | `Res = null` e `erro` com o motivo |

- **Efeito de cada fator:** correlação de postos de Spearman entre o fator e `Res`, só com as linhas válidas (3 casas). Fica `null` com menos de 3 linhas válidas ou se o fator ou `Res` não variam.
- **Interpretação:** +1 = margem cresce com o fator; −1 = cai.
- **Estimativa na tela:** seção 10.6.

### 15.3 Curva de lactação (`lactation.py`)

- `y(t) = l · t^m · e^(−n·t)`, kg de leite por vaca por dia, para `t = 1…330` no servidor (e até o maior entre 330 e parto + 15 na tela).
- Parâmetros `l`, `m`, `n` por paridade (1, 2 e 3 ou mais) vêm do RuFaS (`LactationCurve`); sem simulação, valem os de `DEFAULT_WOOD` (média base do RuFaS `l = 19,9`, `m = 0,247`, `n = 0,003376` mais o ajuste de paridade, sem os ajustes de ano, região e ordenha).
- **Marcos:** `proximo_parto = PEV + gestação`; `secagem = proximo_parto − dias de secagem`. Padrão do quadro: PEV 60, gestação 270, secagem 60 dias antes do parto (parto no dia 330, secagem no dia 270).
- **Pico:** dia e valor do máximo nos 305 primeiros dias (na tela). **Produção em 305 dias:** soma dos 305 primeiros valores diários, mostrada em toneladas.

### 15.4 Cenários de referência

Resultados obtidos nesta implementação, com semente 42, rebanho `freestall` (100 vacas nas medições), 1 ano e os preços ilustrativos vigentes. Servem de casos de aceite do comportamento, **não** como recomendação de dieta.

| Caso | Entrada | Resultado esperado |
|---|---|---|
| Exercício do quadro | Valores iniciais (seção 9.8) | Custo US$ 15,3453; arroz 4,473 kg; milho 3,873 kg; mínimos de carboidrato e proteína ativos; preços-sombra aproximados US$ 0,57/kg (carboidrato) e US$ 13,22/kg (proteína) |
| Simulação padrão | "Conjunto base"; preço do leite 0,45 | Margem ≈ US$ 385 mil; custo da ração ≈ US$ 4,02 por vaca por dia; leite ≈ 40,3 kg por vaca por dia; 30 a 37 s |
| Preço do farelo de arroz | Farelo de arroz de US$ 0,375 para US$ 0,125 por kg MS; milho a US$ 0,14; leite a US$ 0,54 | Uso do farelo de arroz de 0,4 para 11,2 kg por vaca por dia; margem de US$ 513.574 para US$ 519.929 |
| Sensibilidade | Arroz × milho × preço do leite, grade de 2 níveis (8 cenários, 4 simulações) | ρ de Spearman com a margem: leite ≈ +0,87; arroz ≈ −0,44; milho ≈ −0,22; ≈ 66 s |
| Cenário que antes abortava | Milho a US$ 0,42 e farelo de arroz a US$ 0,375 | Conclui, com leite perdido ≈ 0,17 kg/vaca/dia |

---

## 16. Tratamento de Erros e Mensagens

### 16.1 Mensagens da interface

| Situação | Onde | Mensagem |
|---|---|---|
| Menos de 3 alimentos ao simular | Aviso (*toast*) de erro | Selecione pelo menos 3 alimentos (um volumoso, um concentrado e um mineral). |
| Simulação concluída | Aviso de sucesso | Simulação concluída. |
| Falha na simulação | Aviso de erro | Primeira linha do erro da tarefa (por exemplo, `RuntimeError: Simulação do RuFaS falhou: <detalhe>`); sem mensagem, "Falha na simulação" |
| Análise concluída | Aviso de sucesso | Análise concluída. |
| Falha na análise | Aviso de erro | Primeira linha do erro; sem mensagem, "Falha na análise" |
| Fatores iguais no exercício | Aviso de erro | Escolha dois fatores diferentes. |
| Falha ao resolver / gerar cenários | Aviso de erro | Mensagem do erro, ou "Falha ao resolver" / "Falha ao gerar cenários" |
| Problema inviável | Bloco na solução | Sem solução viável. Os limites mínimo e máximo são incompatíveis com os alimentos disponíveis. |
| Cenário inviável na tabela do quadro | Célula `Res` | inviável |
| Cenário falho na sensibilidade | Célula `Res` | falhou (causa na dica e na coluna da ração) |
| Ração insuficiente | Indicador e alerta | Seção 10.4 |
| Servidor inacessível ao carregar | Selo no cabeçalho | sem conexão com o servidor |
| Sem seleção de fatores | Estimativa | Marque ao menos um fator. |
| Busca sem resultado | Seletor de alimentos | Nenhum alimento encontrado. |

### 16.2 Erros do servidor

Formato `{"error": "<Tipo>: <mensagem>"}`: o tipo é o nome da exceção Python (`KeyError`, `JSONDecodeError`, `StopIteration`…). Tarefas guardam em `error` o tipo, a mensagem e até 4 níveis de *traceback*; a interface mostra só a primeira linha.

### 16.3 Mensagens de console e de scripts

| Origem | Mensagem |
|---|---|
| Servidor | `Servidor em http://<host>:<porta>  (Ctrl+C para parar)` |
| `setup.ps1` | "Python 3.12 nao encontrado. Instale com: winget install Python.Python.3.12"; "pip falhou; baixando os pacotes com curl..."; "Pronto. Inicie com iniciar.bat" |

### 16.4 Princípio

Erros explicam o que houve; o detalhe fica em `runs/<nome>/console.log`. Nenhum erro derruba o servidor. A recuperação de um servidor parado é reiniciar com `iniciar.bat` e recarregar a página.

---

## 17. Logs e Auditoria

**Logs do servidor:** o log de cada requisição é silenciado. Só a linha de início é escrita no console (seção 16.3). Nada é persistido pelo servidor.

**Logs das simulações:** persistidos em disco.

| Arquivo | Conteúdo |
|---|---|
| `runs/<nome>/console.log` | Saída padrão e de erro do RuFaS |
| `runs/<nome>/logs/`, `runs/<nome>/tm_logs/` | Logs do RuFaS e do gerenciador de tarefas (verbosidade `errors`) |
| `runs/<nome>/out`, `json`, `csv`, `reports`, `graphics` | Saídas do RuFaS |

Não há log estruturado, retenção definida nem serviço centralizado.

**Auditoria:** não existe. Nenhum registro de quem simulou o quê. A pasta `runs/` permite reconstruir *o que foi simulado*, não *por quem*. Não é requisito da versão 1 (seção 27).

---

## 18. Uploads, Anexos, Relatórios e Exportações

O sistema tem **exportação** (CSV e relatório HTML, seção A.10) e **importação de preços** por CSV (seção A.9), mas não tem anexos nem armazenamento de arquivos no servidor: o arquivo importado é lido no navegador e os exportados são baixados na hora.

---

## 19. Configurações Globais

Não há arquivo `.env` nem painel de configuração. A configuração está no código e em argumentos de linha de comando.

| Parâmetro | Valor | Onde fica | Efeito |
|---|---|---|---|
| Porta do servidor | 8000 | `server.py` (`--port`), `iniciar.bat`, `next.config.ts` (desenvolvimento) | Mudar exige alterar todos os pontos |
| Endereço do servidor | `127.0.0.1` | `server.py` (`--host`) | Só local por padrão (D5) |
| Período simulado | 1 a 3 anos (interface: 1 ou 2) | `server.py` | `end_date` |
| Data inicial | `2013:1` | `Scenario` | Início da simulação |
| Semente | 42 | `Scenario`, `server.py`, `sensitivity.py` | Reprodutibilidade |
| Exemplo base do RuFaS | `freestall` | `rufas_adapter.py` (`EXAMPLE`) | Rebanho e configuração |
| Padrão nutricional | `NRC` | `server.py` | Exigências |
| Redução máxima de leite | 5,0 kg/vaca/dia | `server.py`, interface | Limite antes de abortar |
| Preço do leite | 0,45 US$/kg | `scenarios.py`, interface | Receita |
| Tempo limite do RuFaS | 3600 s | `rufas_adapter.py` | Interrompe simulação presa |
| Simulações em paralelo | 2 | `sensitivity.py`, `scenarios.py` | Uso de memória |
| Tarefas simultâneas | 1 | `jobs.py` | Uso de memória |
| Consulta do estado da tarefa | 1,5 s | `lib/api.ts` | Atualização do progresso |
| Tempo estimado por simulação | 17 s | `SensitivityView.tsx` | Estimativa na tela |
| Níveis/amostras | 2 a 12 | `SensitivityView.tsx` | Tamanho da análise |
| Resultados da busca de alimentos | 60 | `FeedPicker.tsx` | Lista exibida |
| Tetos de inclusão padrão | 0,6 / 0,9 / 1,0 / 100 | `feeds.py` | Seção 14.2 |
| Dias da curva | 330 | `lactation.py` | Eixo da curva |
| PEV, gestação, secagem | 60, 270, 60 dias | `lactation.py`, `CurveView.tsx` | Marcos |
| Chave de armazenamento | `dietopt.v1` | `AppProvider.tsx` | Persistência no navegador |
| Pasta de cenários e cache | `runs/`, `runs/_cache/` | `rufas_adapter.py`, `scenarios.py` | Armazenamento |
| Filtros de saída do RuFaS | `RESULT_FILTERS` | `rufas_results.py` | Quais variáveis são lidas |

---

## 20. Evolução dos Dados de Referência e da Distribuição

Substitui, neste sistema, o papel das migrations: como evoluir os dados de referência com segurança.

### 20.1 Alterar preços padrão, tetos ou parâmetros de referência

1. Editar `DEFAULT_PRICES` e `DEFAULT_MILK_PRICE` (`scenarios.py`), os tetos (`feeds.py`) ou `DEFAULT_WOOD` (`lactation.py`). Preços são em US$/kg MS e devem permanecer rotulados como ilustrativos enquanto não forem cotações.
2. Se o cenário padrão muda, as simulações em cache continuam válidas apenas para parâmetros idênticos: preços alterados geram nova chave.
3. Executar os testes (`pytest`) e conferir os casos de referência (seção 15.4).

### 20.2 Atualizar a versão do RuFaS ou suas tabelas

1. Trocar a tag em `vendor/RuFaS` e atualizar `requirements-rufas.txt`.
2. **Apagar `runs/_cache/`**: a chave do cache não considera a versão do RuFaS nem as tabelas de entrada (D6).
3. Revisar o adaptador (nomes de campos, filtros de saída, ids de alimentos) e repetir a validação completa (seção 23).

### 20.3 Alterar a interface

Editar `web/src/` e executar `scripts\build-web.ps1`. Para mudar uma cor, editar o token em `web/src/app/globals.css` (claro e escuro) e refazer a conferência de contraste.

### 20.4 Adicionar um endpoint

Implementar em `server.py` (`do_GET` ou `do_POST`), tipar a resposta em `lib/types.ts`, expor em `lib/api.ts` e usar na tela. Responder erros no formato da seção 11.3.

### 20.5 Execução segura

- Nunca apagar `vendor/RuFaS` com uma tarefa em andamento.
- Reiniciar o servidor descarta as tarefas; resultados concluídos permanecem no cache.
- `runs/` cresce sem limite: apagar pastas antigas manualmente quando necessário (preservar `runs/_cache/` se quiser manter resultados).

---

## 21. Segurança Funcional

### 21.1 Princípios

- O sistema não coleta dados pessoais nem credenciais.
- Nada sai da máquina em tempo de uso.
- O sistema nunca mascara falhas.

### 21.2 O que existe

- Escuta em `127.0.0.1` por padrão.
- Servir arquivos estáticos somente de `frontend/` (proteção contra saída da pasta).
- Execução do RuFaS com argumentos fixos e caminhos construídos pelo adaptador (o usuário não escolhe caminhos nem comandos).
- Falhas viram resposta JSON sem derrubar o servidor.
- Versão do RuFaS e dependências fixadas.

### 21.3 O que não existe (alertas)

1. **Sem autenticação, validação de `Host`, de `Origin`/`Referer` ou limite de requisições.** Uma página aberta no navegador do mesmo computador pode enviar requisições ao servidor local (por exemplo, disparar simulações de ≈ 1,2 GB de RAM cada) e, em cenários de religação de DNS, tentar ler respostas. Os dados são de baixa sensibilidade; o consumo de recursos não.
2. **`--host` permite expor o servidor à rede sem proteção alguma** (D5).
3. **Sem limite de tamanho do corpo** das requisições nem validação de esquema.
4. **Sem teto de cenários** na sensibilidade: uma grade com vários fatores de alimento e 12 níveis dispara `12^k` simulações, de 30 s cada em 2 paralelas.
5. **`localStorage`** guarda seleção, preços e parâmetros em texto simples.

Qualquer rota nova herda essas ausências. Se o servidor for exposto à rede, é preciso antes acrescentar autenticação e limite de requisições, o que não existe hoje (seção 27).

### 21.4 Superfície de confiança da instalação

- O script de instalação executa `pip`, `git clone` e `curl` com a identidade do usuário; a integridade depende dos repositórios e índices de pacotes.
- O RuFaS roda com os privilégios do usuário e lê e grava em `vendor/RuFaS` e `runs/`.

### 21.5 Licenciamento

O RuFaS é GPLv3 e não é modificado; a distribuição conjunta deve respeitar a licença. O template da interface é MIT (aviso em `web/LICENSE-TEMPLATE.md`).

---

## 22. Critérios de Implementação

O sistema é considerado implementado quando:

1. `scripts\setup.ps1` cria o ambiente e `iniciar.bat` inicia o servidor conforme F1 e F2.
2. O servidor expõe as rotas da seção 11.2 com os formatos e códigos da seção 11, escutando em loopback por padrão e servindo apenas `frontend/`.
3. O PL do exercício reproduz os casos da seção 15.4 (custo 15,3453; 4,473 kg; 3,873 kg), com preços-sombra, restrições ativas e inviabilidade sinalizada.
4. O adaptador monta as entradas do RuFaS conforme a seção 12.1, usa caminhos relativos, trata ids NASEM → NRC e detecta falha pela linha de resumo.
5. A economia segue a seção 15.1 e o cache segue a seção 14.6.
6. A sensibilidade segue a seção 15.2, incluindo simulações únicas, falha por cenário e efeitos de Spearman.
7. A curva de lactação segue a seção 15.3.
8. As telas apresentam os componentes, textos e estados da seção 10, com tema claro e escuro e contraste mínimo de 4,5:1 nos textos.
9. Falhas nunca aparecem como resultado válido; o leite perdido é sempre exibido.
10. Os testes automatizados passam e os desvios D1 a D7 estão resolvidos ou formalmente aceitos.

---

## 23. Critérios de Validação

### 23.1 Funcionais

| Cenário | Resultado esperado |
|---|---|
| Abrir o sistema com o servidor ativo | Selo "conectado · N alimentos NRC"; exercício resolvido sozinho |
| Resolver o exercício com os valores iniciais | US$ 15,35/dia; arroz 4,473 kg; milho 3,873 kg |
| Tornar o problema inviável (máximo menor que o mínimo) | "Sem solução viável." |
| Gerar cenários com fatores iguais | "Escolha dois fatores diferentes." |
| Gerar cenários com 3 × 3 níveis | 9 linhas `S1…S9` com `Res` e dieta de cada uma |
| Buscar "soja" na lista de alimentos | Apenas alimentos cujo título ou tipo contém o texto |
| Aplicar "Lista ampla" | Até 18 alimentos selecionados (ids que não existam na biblioteca são ignorados), com preços e tetos padrão |
| Simular com menos de 3 alimentos | Aviso; nenhuma tarefa criada |
| Simular com o "Conjunto base" | Em até 60 s, seis indicadores, ração, composição, exigências e leite |
| Repetir a mesma simulação | Resultado em segundos (cache) |
| Alterar só o preço do leite e simular | Resultado em segundos; receita e margem mudam |
| Rodar sensibilidade com leite e dois alimentos | Tabela `S1…SN` com `Res`, efeitos e margem por cenário |
| Cenário que falha na sensibilidade | Linha "falhou"; demais linhas válidas |
| Abrir a curva sem simular | Selo "parâmetros de referência" |
| Abrir a curva após simular | Selo "calibrados pela simulação RuFaS" |
| Alterar o PEV da curva | Os marcos e a faixa de gestação se movem |
| Recarregar a página | Seleção de alimentos e parâmetros restaurados; resultados não |

### 23.2 Cálculos e integração

| Cenário | Resultado esperado |
|---|---|
| Casos da seção 15.4 | Valores aproximados dos indicados |
| Simulação com ração insuficiente | Indicador "Leite perdido" e alerta; margem calculada com o leite reduzido |
| Simulação em que o RuFaS aborta | Tarefa em erro; nenhum resultado zerado |
| Alimento de teto padrão (mineral) | Ração média do mineral não ultrapassa 0,6 kg MS/vaca/dia |
| Troca de ids 301/302 | Entradas do RuFaS sem ids NASEM quando o padrão é `NRC` |
| Pontos de grade | `n^k` pontos incluindo os extremos de cada faixa |
| Hipercubo latino | `n` amostras, uma por estrato de cada fator, dentro das faixas |
| Spearman | Sinal coerente com a relação entre fator e margem |

### 23.3 Servidor

| Cenário | Resultado esperado |
|---|---|
| `GET /api/jobs/<id inexistente>` | 404 `job não encontrado` |
| `POST` em rota inexistente | 404 `rota não encontrada` |
| `GET` de caminho fora de `frontend/` (por exemplo `/../README.md`) | 404 |
| `POST /api/jobs/simulate` sem `feeds` | 500 com `KeyError` |
| Duas tarefas disparadas em seguida | A segunda fica `queued` até a primeira terminar |
| Requisição `HEAD` a uma rota da interface | 200 sem corpo |

### 23.4 Resiliência e instalação

| Cenário | Resultado esperado |
|---|---|
| Servidor fechado ao abrir a página | "sem conexão com o servidor"; botões desabilitados |
| Reiniciar o servidor durante uma sensibilidade | Tarefa perdida; simulações concluídas voltam do cache na nova execução |
| `pip` falha por TLS | `setup.ps1` baixa os pacotes com `curl` e instala sem rede |
| Executar `scripts\build-web.ps1` | `frontend/` regenerado e servido |

### 23.5 Testes automatizados

| Arquivo | Cobertura |
|---|---|
| `test_diet_lp.py` | Ótimo do quadro, preço-sombra positivo, inviabilidade |
| `test_sensitivity.py` | Produto cartesiano da grade com extremos, hipercubo latino, sinal dos efeitos de Spearman |
| `test_adapter.py` | Troca de ids NASEM → NRC, tetos padrão, resumo de falha do RuFaS, chave de cache |
| `test_standards.py` | Padrão nutricional (NRC e NASEM): bibliotecas, preços restritos à biblioteca, montagem do cenário NASEM com limites |
| `test_module_requirements.py` | Exigências da vaca pelas calculadoras do RuFaS, validação dos campos, sobrescritas, restrições por categoria, rotas do módulo |

| `test_module_evaluate.py` | Avaliação de dietas: oferta linear = oferta do RuFaS no ponto, erro fora do ponto, razões exatas, `min` da proteína, categorias, ordenação, replicações do RuFaS, entradas inválidas |

Total: 71 testes passando. Integração real com o RuFaS e interface foram verificadas manualmente, **sem teste automatizado**.

---

## 24. Preparação da Entrega

### 24.1 Conteúdo da entrega

Pasta do projeto completa (seção 5.1) com `frontend/` compilado, `docs/` atualizada e `README.md`. `.venv`, `wheelhouse/` e `runs/` são gerados na máquina e não precisam ser entregues.

### 24.2 Pré-requisitos por máquina

Windows 10/11; Python 3.12 (`py -3.12`); Git; internet na instalação; cerca de 1 GB de disco e, para simular, ≥ 2,5 GB de RAM livre; navegador moderno. Node 20.9+ só para alterar a interface.

### 24.3 Instalação (usuário novo)

1. Copiar a pasta do projeto para um local de trabalho (de preferência fora do OneDrive e sem acentos no caminho para o build da interface).
2. Executar `scripts\setup.ps1` (F1).
3. Executar `iniciar.bat` (F2).
4. Rodar o exercício do quadro e uma simulação para conferir.

### 24.4 Atualizações

Não há atualização automática. A interface é recompilada com `scripts\build-web.ps1` (F10); mudanças no back-end exigem reiniciar o servidor.

### 24.5 Controle de versão do código

O projeto é um repositório Git (ramo `main`, remoto `origin` em `https://github.com/gebasss/PO_Rufas.git`, um commit `first commit` em 01/11/2026). O `.gitignore` exclui `.venv/`, `wheelhouse/`, `runs/` e caches. Não há fluxo de pull request, ramos protegidos nem CI/CD definidos. `vendor/RuFaS` é um clone Git do RuFaS na tag v1.0.6. Ver seção 27.

### 24.6 Ambientes

Um único ambiente: a máquina do usuário. Não há homologação nem produção separadas.

---

## 25. Organização Sugerida da Implementação

Ordem recomendada para (re)construir o sistema, cada etapa validável sozinha:

1. **Ambiente:** `setup.ps1`, `requirements-rufas.txt`, clone do RuFaS v1.0.6; verificar que o RuFaS roda um exemplo.
2. **PL do exercício** (`diet_lp.py`): validar com o caso do quadro e a inviabilidade (`test_diet_lp.py`).
3. **Biblioteca de alimentos e constantes** (`feeds.py`, `DEFAULT_PRICES`): conferir os 130 alimentos e os tetos.
4. **Adaptador do RuFaS** (`rufas_adapter.py`): montar um cenário, executá-lo e detectar falha; validar a troca de ids e o resumo de falha.
5. **Leitor de saídas** (`rufas_results.py`): filtros e `SimulationResult`.
6. **Economia e cache** (`scenarios.py`): margem, custo por vaca por dia, leite perdido; cache por conteúdo.
7. **Sensibilidade** (`sensitivity.py`): pontos, cenários únicos, Spearman.
8. **Curva de lactação** (`lactation.py`).
9. **Tarefas e servidor** (`jobs.py`, `server.py`): rotas, erros, arquivos estáticos; validar com a seção 23.3.
10. **Interface:** estado compartilhado e cliente da API; exercício do quadro; seletor de alimentos e tela da vaca; sensibilidade; curva; premissas.
11. **Build e distribuição da interface** (`build-web.ps1`, `iniciar.bat`).
12. **Validação ponta a ponta:** seção 23 completa em uma máquina limpa.

Dependências principais: as etapas 4 a 6 dependem da 3; 7 depende de 6; 9 depende de 2 a 8; 10 depende do contrato da 9.

---

## 26. Desvios Conhecidos entre a Implementação Atual e esta Especificação

| ID | Especificado | Implementado hoje | Impacto |
|---|---|---|---|
| D1 | Resultados exibidos devem indicar a que parâmetros correspondem, ou deixar de ser exibidos como atuais quando a entrada muda ou a nova simulação falha (princípio de não esconder o que o modelo fez) | Os resultados da simulação e da sensibilidade permanecem na tela sem marca. Depois de editar preços ou alimentos, ou de uma nova simulação que falhou, o resultado anterior continua visível como se fosse atual | O usuário pode ler um resultado desatualizado como o do cenário em edição |
| D2 | A estimativa de simulações da sensibilidade reflete o que será executado | No modo hipercubo latino com apenas o preço do leite marcado, a tela estima `n` simulações, mas só 1 é executada (o leite não gera simulação) | Estimativa de tempo maior que a real; sem impacto nos dados |
| D3 | Nomes de alimento do exercício do quadro únicos | Dois alimentos com o mesmo nome colidem: as quantidades são indexadas pelo nome, uma sobrescreve a outra e as linhas da tabela se repetem | Solução do exercício incorreta ou tela inconsistente com nomes repetidos |
| D4 | Fator de cenário do quadro que aponta para alimento renomeado ou removido deve gerar mensagem clara | O fator mantém o alvo antigo; o servidor falha com `StopIteration` e a tela mostra uma mensagem genérica. Mais amplamente, o servidor quase não valida entradas (chaves ausentes geram `KeyError` 500) | Mensagem pouco útil; sem corrupção de dados |
| D5 | O servidor só atende a própria máquina (PRD, RNF-07) | O argumento `--host` permite escutar em outros endereços, e não há autenticação, validação de `Host`/`Origin` nem limite de requisições | Servidor exposto à rede sem proteção, se alguém usar `--host` |
| D6 | Mesma entrada, mesmo resultado, inclusive após trocar a versão do RuFaS ou suas tabelas (RNF-06) | A chave do cache considera apenas os parâmetros do cenário; trocar a versão do RuFaS ou editar as tabelas de entrada sem apagar `runs/_cache/` devolve resultados antigos | Resultados desatualizados e silenciosamente reaproveitados |
| D7 | A NEL estimada exibida na lista de alimentos só vale para alimentos com TDN informado (NRC, Eq. 2-3) | O código calcula `0,0245 × TDN − 0,12` para todos. Para minerais, com TDN igual a 0 (por exemplo, carbonato de cálcio), o valor sai −0,12 Mcal/kg, e a tela formata o valor sem tratamento especial (conferido no código; **não conferido na tela**) | Valor sem sentido físico exibido para minerais; sem efeito no cálculo, que é do RuFaS |

---

## 27. Pontos Pendentes e Decisões Futuras

Nenhum dos itens abaixo impede a manutenção da versão atual com base neste FSD. Os dois primeiros bloqueiam a especificação de partes novas.

**Decisões em aberto que bloqueiam especificação (PRD, seção 15)**

- **Q2** — O professor espera uma dieta por fase da lactação (recém-parida, pico, fim)? Hoje a ração é formulada por grupo. Proposta registrada: manter a ração por grupo e documentar a limitação.
- **Q3** — Como tratar a resposta fraca do leite à dieta no RuFaS v1.0.6? Proposta registrada: manter o leite do RuFaS.

**Outras decisões em aberto**

- **Q1** — PEV como *período de espera voluntário* e 270 dias como gestação a partir do PEV (interpretação do autor; parâmetros editáveis).
- **Q4** — Referência profissional para validar a ração (métrica M6). Proposta: tabelas da NRC 2001.
- **Q5** — Preços do CEPEA: fornecimento, moeda e unidade (RF-22, M7).
- **Q6** — O NASEM 2021 é requisito de entrega (RF-24)?
- **Q7** — Prazo de entrega e formato de apresentação.
- **Q8** — Limiares das verificações de consistência (Anexo A.4.2) e **Q9** — tratamento do arroz em grão no padrão NRC (Anexo A.5.3).
- Como o sistema será entregue ao professor (sem instalador nem processo de entrega formal).
- Autor, professor, instituição e prazo estão em branco nos documentos.

**Requisitos do PRD ainda não especificados (dependem das decisões acima)**

- RF-19 (balanço nutricional), RF-20 (exportação), RF-21 (salvar e carregar cenários), RF-22 (importar preços), RF-23 (mais nutrientes no exercício) e RF-13 (tamanho do rebanho na interface). Quando decididos, devem receber especificação própria neste documento.
- RF-24 (NASEM), RF-26 (alimentos personalizados, arroz em grão) e RF-27 (verificações de consistência) já estão especificados no Anexo A; faltam as decisões Q6 (revisada), Q8 e Q9 e a implementação.
- RF-28 e RF-29 (módulo ampliado, modelo linear) estão especificados no Anexo B e em `LINEARIZACAO.md`; RF-30 (dieta ótima sugerida) é a fase 2. Faltam a decisão Q11 e a implementação.

**Melhorias e limitações conhecidas**

- Cada simulação leva de 30 a 37 s e usa ≈ 1,2 GB de RAM; uma tarefa por vez.
- A sensibilidade não tem teto de cenários (seção 21.3).
- As tarefas ficam na memória do servidor e nunca são removidas; `runs/` cresce sem limite.
- A conexão só é verificada ao carregar a página; o selo pode ficar "conectado" depois da queda do servidor.
- A biblioteca NRC 2001 só tem farelo de arroz; o "arroz" do exercício é representado por ele.
- O leite quase não responde à dieta no RuFaS v1.0.6; a margem varia sobretudo pelo custo da dieta.
- Preços iniciais ilustrativos; resultados não validados contra uma referência profissional.
- Testado apenas no Windows e em um computador; interface vista em 1.440 px e cerca de 540 px.
- Acessibilidade sem auditoria automatizada nem leitor de tela; contraste das cores de gráfico não medido.
- Gráficos sem descrição alternativa em texto.

**Operação e infraestrutura**

- O repositório Git existe, mas o fluxo de trabalho (ramos, pull requests, revisão) não foi definido.
- Não há CI/CD, ambiente de homologação nem testes automatizados de integração com o RuFaS ou de interface.
- Não há limpeza de `runs/` nem invalidação do cache por versão do simulador.
- Versão em linha de comando com relatório combinada como fase seguinte, sem decisão técnica registrada.
- Resolução dos desvios D1 a D7 (seção 26).

---

## 28. Conclusão

O Dieta Ótima com RuFaS é uma ponte local entre um problema de Pesquisa Operacional (a dieta de custo mínimo) e um simulador científico (o RuFaS): uma interface web se comunica por HTTP com um servidor Python em loopback, que monta os arquivos de entrada do RuFaS, o executa em um processo separado, lê os resultados e calcula custo, receita e margem sobre o custo de alimentação. A mesma base alimenta a análise de sensibilidade (tabela de cenários `S1…SN` com `Res` e efeito de Spearman) e a curva de lactação de Wood. Não há banco de dados, login, upload, relatório ou auditoria. O princípio que guia as regras é que o sistema nunca esconde o que o modelo fez: falhas aparecem como falhas, leite reduzido aparece como "leite perdido" e preços ilustrativos são rotulados como tais.

Este documento consolida o comportamento esperado, os contratos, os cálculos, a identidade visual, a instalação e os critérios de validação. Os sete desvios catalogados na seção 26 são os únicos pontos em que a implementação difere desta especificação. Os requisitos RF-24, RF-26 e RF-27 estão especificados, sem implementação, no Anexo A; RF-13 e RF-19 a RF-23 e as questões Q1 a Q9 permanecem pendentes de decisão.

Não foram identificadas pendências que impeçam a manutenção da versão atual com base neste FSD.

---

## Anexo A. Especificação dos Requisitos Planejados RF-24, RF-26 e RF-27 (RF-27 implementado; RF-24 e RF-26 não)

> **Status (03/11/2026):** o **RF-27** (A.4) está implementado, junto com o balanço nutricional (RF-19, A.4b); veja as notas "Implementado" nas seções A.4 e A.4b. Os demais itens deste anexo **ainda não existem** na interface e o texto abaixo, fora dessas notas, não descreve a interface atual. **Já implementados no back-end em 02/11/2026** (etapas E1 a E3 de `PLANO_IMPLEMENTACAO.md`): o padrão NASEM nos cenários e na biblioteca (A.3.2 e A.3.3), e as rotas `/api/module/defaults`, `/api/module/requirements` e `/api/module/evaluate` (B.3, B.6 e B.7). Foi escrito a partir de uma leitura do NASEM 2021 (notas em `docs/nasem2021_notas/`), do código do RuFaS v1.0.6 e dos resultados de simulação já guardados em `runs/_cache/`. Onde um fato do RuFaS ainda não foi verificado, o texto diz **"a verificar"**. Os limiares e as decisões marcados **(a confirmar)** dependem do professor ou da equipe (seção A.6).

### A.1 Visão geral

| ID | Requisito | Origem | Dependência |
|---|---|---|---|
| RF-24 | Padrão nutricional **NASEM 2021** selecionável, e comparação NRC × NASEM do mesmo cenário | Quadro do professor (cita NRC e NASEM); PRD, RF-24 | Nenhuma |
| RF-26 | **Alimentos personalizados**, começando pelo **arroz em grão** | Quadro do professor (arroz); NASEM, Tabela 19-1 | RF-24 (o arroz em grão só tem dados completos no padrão NASEM) |
| RF-27 | **Painel de verificações de consistência** da ração obtida | Achados da análise NRC × NASEM × RuFaS | Nenhuma (consumo, FDN e gordura); expor o amido da biblioteca (A.4.3) |

Ordem de implementação sugerida: RF-27, RF-24, RF-26. O RF-27 usa só dados que a API já devolve e vale para os dois padrões.

### A.2 Fatos verificados que sustentam a especificação

| Fato | Evidência |
|---|---|
| O RuFaS já aceita `nutrient_standard = "NASEM"`; o exemplo-base (`example_freestall_config.json`) já vem em NASEM | `config.json` do exemplo |
| O metadata do RuFaS tem duas bibliotecas: `NRC_Comp` (`NRC_comp.csv`, 134 alimentos, ids até 251) e `NASEM_Comp` (`NASEM_Comp_with_TDN_urea.csv`, 176 linhas, ids até 307; a variante sem ureia tem 175 linhas) | `vendor/RuFaS/input/` |
| As duas bibliotecas têm as colunas `limit` e `lower_limit`, usadas pelo adaptador para os limites de inclusão | cabeçalhos dos CSVs |
| Os 18 ids dos presets ("Conjunto base" e "Lista ampla") existem na biblioteca NASEM | comparação de ids |
| Só 113 ids são comuns às duas bibliotecas (21 só NRC, 63 só NASEM) | comparação de ids |
| O RuFaS, no modo NASEM, implementa a Eq. 2-1 de consumo, a mantença de 0,10 Mcal/kg de peso metabólico (Eq. 3-13), o útero gravídico (Eq. 3-15 e 3-16a) e o cálcio e fósforo de lactação (Eq. 7-4 e 7-8b), conforme as notas do NASEM | leitura de `nasem_requirements_calculator.py` |
| O otimizador do RuFaS usa o conjunto de restrições NASEM (`NASEM_constraint_functions`, com `NASEM_net_energy_constraint`) quando o padrão é NASEM | `ration_optimizer.py` |
| Das 88 linhas da Tabela 19-1 já transcritas nas notas, 53 têm correspondente na biblioteca NASEM do RuFaS (MS, PB e FDN iguais); só 3 diferem em amido, por arredondamento | comparação programática |
| O livro tem arroz em grão ("Grãos de Arroz", código NRC16F123, p. 427); nenhuma biblioteca do RuFaS tem | notas do cap. 19; bibliotecas |

### A.3 RF-24: padrão nutricional NASEM 2021

**Objetivo.** Permitir simular o mesmo cenário (alimentos, preços, limites, preço do leite) no padrão NRC 2001 ou NASEM 2021, e comparar os dois lado a lado.

**A.3.1 Seletor de padrão (tela Vaca leiteira)**
- Novo campo **Padrão nutricional** no painel "Cenário", com as opções "NRC 2001" (padrão) e "NASEM 2021". Valor guardado em `params.standard` e em `dietopt.v1`. Ao restaurar um estado salvo sem esse campo, usar "NRC".
- A escolha vale também para a tela Sensibilidade (usa o mesmo `params`).
- Ao trocar o padrão, a interface recarrega a biblioteca (`GET /api/feeds?standard=<NRC|NASEM>`) e mantém os alimentos selecionados que existem nos dois padrões. Alimentos ausentes na nova biblioteca são **removidos da seleção** e listados em um aviso: "Removidos por não existirem no padrão <X>: <lista>." Se restarem menos de 3 alimentos, o botão Simular fica desabilitado com a mensagem já existente de mínimo de 3.
- O selo do cabeçalho mostra "· N alimentos <padrão>" no lugar de "NRC".

**A.3.2 Biblioteca de alimentos por padrão**
- `GET /api/feeds` aceita o parâmetro `standard` (padrão `NRC`). Valor diferente de `NRC` e `NASEM`: erro no formato da seção 11.3.
- Na biblioteca NASEM, cada alimento traz `id`, `name`, `kind`, `category`, `dm`, `cp`, `ndf`, `ee`, `starch`, `de_base` (coluna `DE_Base`, Mcal/kg MS), `calcium`, `phosphorus`, `default_price`, `default_max`. O campo `nel` (Eq. 2-3 do NRC) **não** é enviado nem exibido no NASEM, porque o NASEM define que o valor de energia depende da dieta e da ingestão, não do ingrediente.
- Na lista da tela, a linha de apoio do alimento passa a ser "tipo · PB x% · FDN x% · amido x% · ED base x,xx Mcal/kg" no NASEM.
- Os tetos de inclusão padrão (seção 14.2) valem nos dois padrões. As categorias da biblioteca NASEM (`Fd_Category`) diferem das do NRC; o critério de "mineral" precisa ser conferido (A.7).

**A.3.3 Montagem do cenário no padrão NASEM**
- `Scenario.nutrient_standard = "NASEM"` (já existe).
- Não aplicar a troca de ids 301 → 230 e 302 → 167 (só vale para NRC).
- Gravar `lower_limit` e `limit` na cópia do CSV NASEM, e apontar o `metadata.json` para ela na chave `NASEM_Comp` (hoje o adaptador só edita `NRC_Comp`).
- Os preços continuam por id (`DEFAULT_PRICES` e preços do usuário), mas **devem ser restritos aos ids da biblioteca do padrão
  escolhido**: o farelo de soja 44% (id 166) não existe na biblioteca NASEM e o `with_defaults` do adaptador mescla todos os
  `DEFAULT_PRICES`, o que gera `KeyError` no RuFaS (verificado em 01/11/2026). Os 7 ids do "Conjunto base" (50, 110, 44, 167,
  138, 230 e 23) existem nas duas bibliotecas.
- A chave do cache já inclui o padrão (campo do `Scenario`), então resultados NRC e NASEM não se misturam.
- O corpo de `POST /api/jobs/simulate` e `/api/jobs/sensitivity` ganha `standard` (`"NRC"` por padrão).

**A.3.4 Resultados**
- Mesmas telas e indicadores. Mostrar um selo "Padrão: NRC 2001" ou "Padrão: NASEM 2021" no topo dos resultados.
- O gráfico "Exigências" lê hoje `NEl_requirement`, `DMIest_requirement` e `MP_requirement` da saída do RuFaS. **Verificado em 01/11/2026:** o modo NASEM grava as mesmas 13 variáveis no filtro `lac_ration` (inclusive os aminoácidos essenciais, que no NASEM vêm não nulos). Os nomes são idênticos, então o leitor de saídas não precisa de mapeamento; o gráfico só deve rotular a energia conforme o padrão (NASEM usa 0,66 de ME para NEL, o NRC usa 0,64).

**A.3.5 Comparar padrões**
- Botão **Comparar NRC × NASEM** na tela Vaca leiteira, habilitado com as mesmas condições de Simular.
- Cria uma tarefa `compare` que roda o cenário nos dois padrões (2 simulações, podendo usar o paralelismo de 2) e devolve duas avaliações.
- Resultado: tabela com uma coluna por padrão e uma de diferença (%): margem, receita, custo de alimentação, custo da ração por vaca por dia, leite por vaca, leite perdido, consumo da ração, consumo estimado e ração média por alimento. Gráfico de barras agrupadas do mesmo conjunto, em série única por padrão.
- A comparação não altera o resultado exibido nas demais seções; fica em um cartão próprio.
- Falha em um dos padrões: mostrar o outro e marcar o que falhou como "falhou", sem zeros (princípio P2).

**A.3.6 Critérios de aceite**
1. Simular o "Conjunto base" em NASEM termina sem erro e exibe os seis indicadores (**verificado** em 01/11/2026 pelo
   adaptador, com os preços restritos à biblioteca, em 22,7 s; ver A.7.1).
2. Com o padrão em NRC, os resultados continuam iguais aos da seção 15.4.
3. Trocar de padrão remove da seleção, com aviso, os alimentos ausentes na outra biblioteca.
4. Os limites mínimo e máximo informados valem nos dois padrões (ração média dentro dos limites).
5. "Comparar" mostra os dois padrões, ou o que falhou, e as diferenças em %.
6. Testes automatizados: troca de ids só em NRC; escrita de limites no CSV NASEM; chave de cache distinta por padrão.

**A.3.7 Validação científica (substitui parcialmente a métrica M6)**
- Comparar as exigências calculadas pelo RuFaS no modo NASEM com as equações do capítulo 20 do NASEM para vacas de referência (consumo, mantença, lactação, cálcio e fósforo).
- A Tabela 21-1 do NASEM **não** serve como teste exato de consumo: com a Eq. 2-1, as multíparas só reproduzem o consumo da tabela com escore de condição corporal ≈ 2,7 e as primíparas só com ≈ 1,0, o que é implausível. As premissas da tabela não estão no texto. Usar a tabela só para ordem de grandeza e as equações para o teste.

### A.4 RF-27: painel de verificações de consistência

> **Implementado em 03/11/2026 (etapa E8a):** `backend/dietopt/ration_checks.py` e `web/src/views/cow/ChecksCard.tsx`. Como ficou:
> - V1 a V5 como na tabela A.4.2, calculadas em `simulation_payload` e devolvidas em `checks` (`id`, `label`, `status`, `value`,
>   `limit`, `detail` e `metrics`) e `checks_summary`. A **média** dos intervalos decide o estado de V1 a V4; o **pior intervalo**
>   só pode elevá-lo a "atenção" (V1 mostra os dois).
> - Tolerância de 1e-3 ponto percentual nos limites: o otimizador do RuFaS deixa a FDN em 45,0000006%, que vale como 45% (atenção).
> - O amido vem da coluna `starch` das duas bibliotecas (`FeedInfo.starch` passou a existir também no NRC; a interface do NRC
>   continua sem ele).
> - Na tela: cartão **Verificações** entre os indicadores e o gráfico da ração (resumo no título, estado em texto e ícone, nota da
>   Tabela 5-1) e aviso no topo (destrutivo com alerta, padrão com só atenção). A coluna "Verif." da sensibilidade (A.4.1) **não** foi feita.
> - Aceite: os seis critérios de A.4.5 estão em `tests/test_ration_checks.py`.
> - Conferência em simulação real (NRC, "Conjunto base", 03/11/2026): V1 alerta (+29,5% em média), V2 atenção (45,0%), V3, V4 e V5 ok.

**Objetivo.** Mostrar, junto dos resultados, se a ração obtida é coerente com o que o NRC e o NASEM consideram plausível. As verificações **só informam**: não alteram margem, custo nem ração, e não filtram cenários.

**A.4.1 Onde aparece**
- Na tela Vaca leiteira: cartão **Verificações**, entre os indicadores e o gráfico "Ração das vacas em lactação". Mostra um resumo no título ("3 verificações: 1 em alerta, 1 em atenção, 1 ok") e uma linha por verificação.
- Cada linha tem: estado (ícone e texto "ok", "atenção" ou "alerta"), nome, valor obtido, limite e uma dica de uma frase. A cor nunca é o único canal.
- Se houver ao menos um alerta, o topo dos resultados mostra um `Alert` destrutivo: "A ração tem N verificação(ões) em alerta. Veja o cartão Verificações." Com apenas atenções, um aviso em âmbar.
- Na sensibilidade (fase 2, opcional): coluna "Verif." com o pior estado de cada cenário.

**A.4.2 Verificações e regras**

| ID | Verificação | Valor | ok | atenção | alerta | Base |
|---|---|---|---|---|---|---|
| V1 | Consumo de matéria seca da ração × consumo estimado | `consumo da ração ÷ estimado − 1`, por intervalo de 30 dias; mostrar a média e o pior intervalo | ≤ +12% | de +12% a +24% | > +24% **(a confirmar)** | O erro típico (RMSE) da equação de consumo do NASEM é 12,1% (avaliação do modelo, cap. 20, pp. 522–523; o texto impresso diz 12,4%). O RuFaS permite a ração até 30% acima do estimado (`DMI_CONSTRAINT_FRACTION = 0,30`) |
| V2 | FDN total da ração | % da MS (média) | de 25% a 45%, a mais de 0,5 ponto dos limites | a menos de 0,5 ponto de 25% ou de 45% | fora de 25% a 45% | Limites do RuFaS (`MINIMUM_RATION_NDF` 25, `MAXIMUM_RATION_NDF` 45). O NASEM só traz o mínimo de 25% (p. 70) |
| V3 | FDN de forragem, FDN total e amido × Tabela 5-1 do NASEM | ver A.4.3 | cumpre a Tabela 5-1 | FDN de forragem entre 15% e 19% e cumpre a tabela; ou amido a menos de 2 pontos do máximo | não cumpre a tabela, ou FDN de forragem abaixo de 15% | NASEM, Tabela 5-1 (p. 70) |
| V4 | Gordura (extrato etéreo) da ração | % da MS (média) | ≤ 5% | de 5% a 7% | > 7% | RuFaS (`MAXIMUM_RATION_FAT` 7) e NASEM (gordura total ≤ 7%; < 5% no início da lactação, pp. 46 e 59) |
| V5 | Leite perdido por ração insuficiente | kg/vaca/dia (já calculado) | 0 | > 0,005 | ≥ 50% da redução máxima configurada **(a confirmar)** | Seção 14.4, 15.1 |

**A.4.3 Regra da Tabela 5-1 (V3)**
- Premissas da tabela (devem aparecer como nota no cartão): dieta em TMR, forragem com tamanho de partícula adequado e milho moído seco como fonte predominante de amido.
- Tabela do NASEM:

| FDN de forragem mín. (% MS) | FDN total mín. (% MS) | Amido máx. (% MS) |
|---|---|---|
| 19 | 25 | 30 |
| 18 | 27 | 28 |
| 17 | 29 | 26 |
| 16 | 31 | 24 |
| 15 | 33 | 22 |

- Para `FDNf` (FDN de forragem, % MS) entre 15 e 19: `FDN total mínimo = 25 + 2 × (19 − FDNf)` e `amido máximo = 30 − 2 × (19 − FDNf)`. Para `FDNf ≥ 19`: mínimo 25 e máximo 30. Para `FDNf < 15`: a tabela não informa; classificar como alerta.
- Cálculo, com a ração média: `FDNf = Σ(kg × NDF%) dos alimentos de tipo Forage ÷ Σ kg`; `FDN total` e `amido` análogos sobre todos os alimentos. Para o estado "atenção", usar também o pior intervalo de 30 dias.
- **Requer expor `starch`** (amido, % MS) no `FeedInfo` e em `GET /api/feeds` (hoje só `cp`, `ndf`, `ee`, `tdn`, `calcium`, `phosphorus`). A coluna `starch` existe nas duas bibliotecas do RuFaS.
- O livro registra uma divergência que as notas não apontam: a Tabela 21-1 imprime "FDN de forragem mín. 19–25", enquanto a Tabela 5-1 traz 15 a 19. Esta especificação segue a Tabela 5-1.

**A.4.4 Dados e API**
- As verificações são calculadas no **servidor**, em `simulation_payload`, e devolvidas em `result.checks`: lista de `{ id, label, status, value, limit, detail }` (`status` ∈ `ok`, `warn`, `alert`). Assim são testáveis com `pytest` sobre resultados do cache.
- Entradas já disponíveis no resultado: `intervals.ration` (inclui `dry_matter_intake_total`), `intervals.requirements` (inclui `DMIest_requirement`), `average_ration` e `summary.reducao_leite`.
- Entradas a acrescentar: `starch` por alimento (A.4.3).

**A.4.5 Critérios de aceite**
1. Para um resultado com consumo da ração de 33,5 kg e estimado de 25,8 kg (+30%), V1 = alerta; para 29,6 kg (+15%), V1 = atenção; para 28,0 kg (+8%), V1 = ok.
2. Uma ração com FDN de forragem 17%, FDN total 28% e amido 25% falha V3 (FDN total mínimo 29%); com FDN total 30% cumpre.
3. Uma ração com FDN total de 45,0% marca V2 como atenção (no limite do RuFaS).
4. Uma ração com gordura de 7,0% marca V4 como atenção; acima de 7,0%, alerta.
5. As verificações aparecem para NRC e NASEM e não mudam margem nem custo.
6. A cor não é o único canal (texto e valor sempre presentes), e o contraste dos estados segue os tokens da seção 10.8.

**A.4.6 Observação sobre os resultados já guardados**
Das 57 simulações em `runs/_cache/` (preços ilustrativos), o estimado ficou em ≈ 25,8 kg e a ração entre 28 e 34 kg, várias no teto de ≈ 33,5 kg (+30%). A FDN total ficou em 45% (o teto do RuFaS) na maioria; a FDN de forragem ficou entre 30% e 45% e o amido entre 2% e 28%, o que cumpre a Tabela 5-1. Uma ração com 11 kg/dia de farelo de arroz chegou exatamente a 7,0% de gordura. Esses números são o motivo de V1, V2 e V4.

### A.4b RF-19: balanço nutricional

> **Implementado em 03/11/2026 (etapa E8b)**, sem especificação prévia neste anexo. `backend/dietopt/ration_balance.py` e
> `web/src/views/cow/BalanceCard.tsx`. O RuFaS já avalia a ração a cada intervalo (`NutritionEvaluator`) e o filtro de saída
> `lac_ration` passou a guardar `avg_eval_results_for_LAC_COW` (`SimulationResult.evaluations`); resultados guardados em
> `runs/_cache/` antes disso não têm a avaliação e a simulação roda de novo.
> - Linhas: energia total, de mantença e atividade, de lactação e gestação e de crescimento (Mcal/dia); proteína metabolizável
>   (g/dia); cálcio e fósforo (g/dia); consumo de MS (kg/dia); FDN total, FDN de forragem e gordura (% da MS).
> - Convenções do RuFaS: energia, cálcio e fósforo = oferta − exigência (a oferta mostrada é exigência + diferença); proteína
>   metabolizável e consumo = 0 dentro da faixa aceita (1 a 1,5 vezes a exigência; 0,7 a 1,3 vezes o estimado), senão a distância
>   até o limite (a oferta exata não aparece); FDN total = 0 entre 25% e 45%; FDN de forragem = % − 15; gordura = 7 − %. A exigência de
>   fósforo é a maior entre a da vaca e a do processo; a de energia soma mantença, atividade, crescimento, gestação e lactação.
> - Cada linha mostra a diferença média dos intervalos, a do pior intervalo (mais desfavorável) e o estado: **Atende**, **Déficit**
>   ou **Fora da faixa**, a partir do pior intervalo. A oferta de FDN, FDN de forragem, gordura e consumo é a da ração média.
> - Cartão **Balanço nutricional** logo depois das verificações. Os números vêm do RuFaS, não do modelo linear do módulo ampliado.
> - Observação: o RuFaS marca a ração como inválida se a diferença de gordura não for 0, embora ela seja 7 − % (positiva em
>   qualquer ração abaixo do teto); a tela trata gordura ≥ 0 como atendida.

### A.5 RF-26: alimentos personalizados (arroz em grão)

**Objetivo.** Permitir que o usuário use um alimento que não está nas bibliotecas do RuFaS. O primeiro caso é o **arroz em grão** do quadro do professor: as bibliotecas do RuFaS só têm farelo de arroz (id 138), e o NASEM traz a composição do arroz em grão na Tabela 19-1 (p. 427).

**A.5.1 Comportamento**
- Botão **+ Alimento personalizado** no seletor de alimentos (tela Vaca leiteira), com um formulário: nome, tipo (`Forage`, `Conc` ou `Mineral`), padrão em que o alimento vale (NASEM ou NRC) e os campos de composição.
- Um alimento personalizado é guardado no arquivo `custom_feeds.json` na raiz do projeto, **fora** de `vendor/RuFaS` (o RuFaS continua sem modificação), com id a partir de **1001** (as bibliotecas usam ids até 307).
- O adaptador acrescenta uma linha por alimento personalizado às cópias dos CSVs da biblioteca em `runs/<nome>/`, nas colunas do padrão escolhido. As colunas que o usuário não preenche herdam os valores de um **alimento de referência** escolhido no formulário.
- O alimento aparece na lista com um selo **"personalizado"** e, quando houver colunas herdadas, **"composição parcial"**, com dica listando as colunas herdadas e o alimento de referência. Os resultados dessa simulação repetem o selo.
- Preço, mínimo e máximo funcionam como nos demais alimentos. Sem preço padrão, vale o preço de partida do tipo (Conc 0,35), rotulado como ilustrativo.
- Excluir um alimento personalizado o remove do arquivo e da seleção.

**A.5.2 Pré-cadastro: arroz em grão (NASEM, Tabela 19-1, p. 427, código NRC16F123)**

| Campo do livro | Coluna no CSV do RuFaS (NASEM) | Valor (média) |
|---|---|---|
| MS (%) | `DM` | 87,9 |
| Cinzas (% MS) | `ash` | 1,8 |
| PB (% MS) | `CP` | 8,1 |
| Frações A, B, C da PB (%) | `N_A`, `N_B`, `N_C` | 31; 54; 15 |
| Kd (%/h) | `Kd` | 19,1 |
| PNDR; digestibilidade da PNDR (%) | `RUP`, `dRUP` | 29; 88 |
| PB solúvel (% PB) | `sol_prot` | 17,9 |
| PIDA; PIDN (% MS) | `ADICP`, `NDICP` | 0,41; 1,12 |
| FDA; FDN (% MS) | `ADF`, `NDF` | 4,6; 6,4 |
| Lignina (% MS) | `lignin` | 1,55 |
| Amido (% MS) | `starch` | 75,8 |
| CSA (% MS) | `WSC` | 1,4 |
| Ácidos graxos totais; extrato etéreo (% MS) | `FA`, `EE` | 1,24; 2,0 |
| ED base (Mcal/kg MS) | `DE_Base` | 3,48 |
| Ca; P; Mg; K; Na; Cl; S (% MS) | `calcium`, `phosphorus`, `magnesium`, `potassium`, `sodium`, `chlorine`, `sulfur` | 0,02; 0,26; 0,1; 0,25; 0,01; 0,07; 0,1 |
| Cu; Fe; Mn; Zn; Mo (mg/kg MS) | `copper`, `iron`, `manganese`, `zinc`, `molibdenum` | 3,96; 83; 37; 21; 1,0 |

Fonte dos valores: `docs/nasem2021_notas/ch19_dados/tab19-1_parcial_88alimentos.csv` (local, não versionado; linha NRC16F123), conferida pela auditoria independente das notas. O pré-cadastro cita a fonte na dica do alimento.

**A.5.3 O que o livro dá e o que falta**
- **Falta**: os perfis de aminoácidos e de ácidos graxos do arroz em grão estão na Tabela 19-2 (p. 453), que as notas **não** transcrevem (60 de 184 alimentos). Essas colunas devem ser transcritas com conferência visual da p. 453 ou herdadas (selo "composição parcial").
- **Falta**: as colunas `TDN` e `DE` do arquivo `NASEM_Comp_with_TDN*.csv` não existem no livro; foram acrescentadas pelo RuFaS e **a origem do cálculo é desconhecida (a verificar)**. Sem elas, o comportamento do otimizador para o alimento personalizado é incerto.
- **No padrão NRC** o arroz em grão **não** tem `TDN` nem composição na Tabela 15-1 do NRC. O alimento fica **indisponível** no padrão NRC (cinza, com dica) até decisão **(a confirmar, Q9)**.
- A coluna `is_wetforage` aparece como verdadeira em 33 alimentos da biblioteca NASEM do RuFaS, incluindo vários com MS acima de 80% (farelo de arroz, grão de aveia, farinha de carne e ossos). O efeito no modo NASEM não foi verificado; o alimento personalizado deve usar `is_wetforage = FALSE` (arroz em grão tem MS de 87,9%).

**A.5.4 Critérios de aceite**
1. O arroz em grão pode ser selecionado no padrão NASEM e fica indisponível no NRC, com a dica explicando.
2. Uma simulação NASEM com o arroz em grão e limite máximo definido termina e a ração média respeita o limite (**a verificar**).
3. O RuFaS (`vendor/`) continua sem alterações; o alimento só existe em `custom_feeds.json` e nas cópias de `runs/`.
4. O selo "personalizado" e, quando houver, "composição parcial" aparecem na lista e nos resultados.
5. Testes automatizados: leitura e escrita de `custom_feeds.json`; linha acrescentada ao CSV com as colunas herdadas; id ≥ 1001.

### A.6 Decisões que dependem do professor ou da equipe

| # | Questão | Proposta (a confirmar) |
|---|---|---|
| Q6 (revisada) | O NASEM 2021 é requisito de entrega? Hoje é **viável** (A.2) e há especificação (A.3) | Implementar o seletor e a comparação |
| Q8 | Limiares de V1 (+12% e +24%) e de V5 (50% da redução máxima) | Usar múltiplos do erro de 12,1% do NASEM (1× e 2×) |
| Q9 | Como tratar o arroz em grão no padrão NRC (sem `TDN`)? | Disponível só no NASEM |
| Q3 (ligada) | O NASEM calcula proteína e gordura do leite a partir de aminoácidos e energia absorvidos (Eq. 6-6 e 20-185) com erro de 14,4% e 17,1% (RMSE), mas o próprio livro desaconselha usar o leite "permitido" por energia ou proteína como meta (erro de 22 a 24%). Vale um modelo de resposta do leite à dieta? | Manter o leite do RuFaS por ora; levar a opção ao professor |
| — | O RuFaS aceita ração até 30% acima do consumo estimado (`DMI_CONSTRAINT_FRACTION`). É intencional? | Perguntar ao professor, que participou do RuFaS; o sistema não modifica o RuFaS |

### A.7 Riscos e itens a verificar antes de implementar

| Item | Risco | Como verificar |
|---|---|---|
| O modo NASEM com as nossas listas de alimentos e preços converge? | O otimizador e as restrições são diferentes (`NASEM_net_energy_constraint`) | **Verificado** (A.7.1): converge, desde que os preços sejam restritos à biblioteca |
| Variáveis de saída do RuFaS no modo NASEM | O leitor de saídas e o gráfico de exigências podem não achar as variáveis | **Verificado**: as mesmas 13 variáveis no filtro `lac_ration` |
| Categorias da biblioteca NASEM | O teto padrão de minerais (seção 14.2) depende de `Fd_Category`/`feed_type` | Listar as categorias do CSV NASEM |
| Ids do RuFaS fora das bibliotecas | O RuFaS pode exigir o alimento também em `user_feeds.csv` e em outras listas de `feed.json` | Testar com um alimento personalizado |
| Memória | A comparação roda 2 simulações de ≈ 1,2 GB cada | Manter o limite de 2 simultâneas |
| Preços ilustrativos | Comparar padrões com preços ilustrativos pode ser lido como recomendação | Manter o rótulo "ilustrativo" |
| Divergências do próprio NASEM | Erros de impressão e ambiguidades (por exemplo, parênteses da Eq. 2-1; Tabela 21-1 × 5-1) | Consultar `00_INDICE.md`, seção 4, das notas; o código R oficial prevalece |

#### A.7.1 Resultado da verificação do modo NASEM (01/11/2026)

Execução do "Conjunto base" (ids 50, 110, 44, 167, 138, 230 e 23) pelo adaptador, uma vez em cada padrão, sem alterar o
RuFaS. O NASEM terminou em 22,7 s.

| Indicador | NRC 2001 | NASEM 2021 |
|---|---|---|
| Margem sobre custo de alimentação (US$, rebanho) | 384.622 | 440.925 |
| Custo da ração, vaca em lactação (US$/dia) | 4,019 | 3,425 |
| Consumo estimado (kg MS/dia) | 25,77 | 24,62 |
| Consumo da ração (kg MS/dia) | 33,5 | 32,0 |
| Energia de mantença (Mcal/dia) | 10,04 | 12,55 |
| Energia de gestação (Mcal/dia) | 0,31 | 2,72 |
| Proteína metabolizável (g/dia) | 2.822 | 2.695 |
| Cálcio (g/dia) | 72,2 | 66,6 |
| Leite total do rebanho (kg) | 1.278.982 | 1.278.982 |

A ração do NASEM ficou em 14,81 kg (id 50), 16,8 kg (id 110), 0,17 kg (id 138) e 0,03 kg (id 23) por dia. O leite não
mudou (nenhuma redução por ração insuficiente). Os números são ilustrativos (preços ilustrativos) e **não** indicam qual
padrão é "melhor": as exigências diferem por construção (mantença de 0,08 para 0,10 Mcal/kg^0,75, gestação, DMI).

### A.9 RF-22: importar preços por CSV (implementado em 03/11/2026, etapa E8d)

**Objetivo.** Usar cotações reais (por exemplo, do CEPEA) sem digitá-las à mão. O sistema não busca o indicador sozinho: o
usuário traz um arquivo e diz a que alimento do RuFaS cada preço se refere.

**Arquivo.** Texto com cabeçalho; separador vírgula, ponto e vírgula ou tabulação; vírgula decimal aceita; linhas em branco e
linhas que começam com `#` são ignoradas. Colunas (sem acento e em qualquer ordem; apelidos entre parênteses):

| Coluna | Obrigatória | Significado |
|---|---|---|
| `id` (`rufas_id`) ou `alimento` (`nome`) | uma das duas | Id do alimento na biblioteca do padrão, ou o nome exato (sem diferença de caixa ou acento; "nome" ou "nome — descrição"). O nome que serve a mais de um alimento é recusado com a lista de ids |
| `preco` (`valor`) | sim | Preço, na moeda, unidade e base abaixo |
| `moeda` | não (USD) | `USD` ou `BRL` |
| `cambio` | só em BRL | R$ por US$; se faltar, vale o campo "Câmbio" da tela |
| `unidade_kg` | não (1) | kg por unidade comercial (saca de 60 kg: 60; tonelada: 1000) |
| `base` | não (MS) | `MS` (matéria seca) ou `MN` (matéria natural, dividida pela MS do alimento) |
| `fonte` | não | Indicador e data, só para registro |

**Conversão** (`LINEARIZACAO.md`, 7.2): `US$/kg MS = preço ÷ unidade_kg ÷ (MS/100, se MN) ÷ câmbio (se BRL)`.

**API.** `POST /api/prices/import` com `{ standard, csv, fx? }`. Resposta: `prices` (id → US$/kg MS), `items` (linha, id, nome,
preço, valor original e fonte), `problems` (linha, texto e motivo) e `warnings` (id repetido: vale o último). Falta de cabeçalho
ou de colunas, ou câmbio inválido, voltam como erro 500 no formato da seção 11.3. Linhas inválidas **não** derrubam as outras.

**Tela.** Botão **Importar preços (CSV)**, campo de câmbio e botão **Modelo** (baixa um CSV de exemplo), nos cartões de
alimentos da tela Vaca leiteira e de **Preços e limites** do módulo Avaliar dietas. Só os alimentos já selecionados têm o preço
trocado; os demais do arquivo aparecem como "fora da seleção" (não são adicionados). Depois da importação a tela mostra quantos
preços foram aplicados, a conversão linha a linha e as linhas sem correspondência ou inválidas, cada uma com o motivo.

**Não feito.** Leitura automática de indicadores do CEPEA, histórico de preços e mapeamento automático indicador × alimento.

**Aceite.** `tests/test_prices.py`: dólar por kg de MS sem conversão; reais por saca na matéria natural (70 R$ por saca de
60 kg a R$ 5,00 por US$ viram `70 ÷ 60 ÷ MS ÷ 5`); câmbio da tela e da linha; id fora da biblioteca do padrão; nome ambíguo;
separador e vírgula decimal; cabeçalho incompleto.

### A.10 RF-20: exportar tabelas e relatório (implementado em 03/11/2026, etapa E8e)

**Objetivo.** Registrar um resultado sem captura de tela: a tabela em CSV, para abrir no Excel, e um relatório que se lê e se imprime.

**Onde.** Botões **Baixar CSV** e **Baixar relatório**, com um campo "Observação para o relatório", no topo dos resultados das telas
Vaca leiteira, Sensibilidade e Avaliar dietas; o Exercício simples só tem o CSV da tabela de cenários.

| Tela | CSV | Relatório (HTML) |
|---|---|---|
| Vaca leiteira | `racao-media.csv`: por alimento, kg de MS por vaca e dia, % da dieta, preço e custo (mais a linha TOTAL) | Indicadores, ração média com preços e limites, verificações (A.4) e balanço nutricional (A.4b) |
| Sensibilidade | `cenarios-sensibilidade.csv`: uma linha por cenário com os fatores, `Res`, indicadores, a ração (uma coluna por alimento) e o erro, se falhou | Resumo (melhor e pior margem, ração do melhor cenário), tabela de cenários e correlação de Spearman |
| Exercício simples | `cenarios-exercicio.csv`: fatores, `Res` e a quantidade de cada alimento | (só CSV) |
| Avaliar dietas | `avaliacao-de-dietas.csv`: uma linha por dieta e restrição, com a posição no ranking | Ranking (com o desvio do ótimo, se a dieta ótima estiver atualizada), dieta ótima e comparação com o RuFaS |

**Formato.** CSV com vírgula como separador, ponto decimal e BOM (o Excel reconhece os acentos); células sem valor ficam vazias, e o
cenário que falhou não ganha números. O relatório é um HTML único, sem arquivos externos, com números no formato brasileiro, estilo de
impressão (salvar em PDF pelo navegador) e a data da geração. Todo texto vindo do usuário (observação, nomes) é **escapado**.

**API.** `POST /api/export/<csv|report>/<simulation|sensitivity|toy|module>` com `{ data, meta }` (o resultado que está na tela e
dados extras: `note`, `standard`, `feed_names`, `optimal`). Resposta: `{ filename, mime, content }`. Nada é gravado no servidor.
A simulação passou a devolver `limits` (mínimo e máximo de cada alimento) para o relatório mostrar os que valeram.

**Não feito.** PDF gerado no servidor, exportação da curva de lactação e dos gráficos, e exportação do histórico (não existe).

**Aceite.** `tests/test_exports.py`: conteúdo de cada CSV, formato brasileiro e seções dos relatórios, escape de HTML, ordem do
ranking, coluna de desvio só com a dieta ótima, despacho e pedidos inválidos.

### A.11 RF-21: salvar e abrir cenários (implementado em 03/11/2026, etapa E8f)

**Objetivo.** Reusar uma configuração entre sessões e enviá-la a outra pessoa, sem depender do navegador. O cenário é um arquivo
JSON local; o servidor não guarda nada.

**Onde.** Botões **Salvar cenário** e **Abrir cenário** no cartão Cenário da tela Vaca leiteira e no topo da tela Avaliar dietas.
Abrir um arquivo de outro tipo mostra uma mensagem pedindo a tela correspondente.

**Formato (versão 1).**

```json
{ "format": "dietopt-scenario", "version": 1, "kind": "cow" | "module", "saved_at": "2026-11-03T16:00:00", "data": { ... } }
```

| `kind` | Conteúdo de `data` |
|---|---|
| `cow` (Vaca leiteira) | `standard`, `params` (`milkPrice`, `years`, `maxReduction`), `feeds` (`id`, `price`, `min`, `max`) e, se houver, `sensitivity` (`method`, `levels`, `factors` com `on`, `low` e `high` por alimento ou `milk_price`) |
| `module` (Avaliar dietas) | `standard`, `category`, `animalType`, `cow` (campos da vaca), `override` (exigências sobrescritas), `feeds`, `diets` (`name` e `amounts` por id), `tolerance`, `resolution` e `seeds` |

O arquivo guarda **só entradas**, nunca resultados: ao abrir, a tela recalcula (os resultados da tela são descartados). Campos da vaca
ainda vazios ficam vazios.

**Validação** (`backend/dietopt/scenario_files.py`, na ida e na volta): formato e versão; faixas dos parâmetros; preço obrigatório e
mínimo não maior que o máximo (máximo vazio vale o teto padrão do alimento); categoria e tipo de animal; campos da vaca e exigências
conhecidos; até 10 dietas; resolução e sementes. Alimentos que não existem na biblioteca do padrão, fatores de alimentos fora do
cenário e quantidades de alimentos fora da tabela são **removidos com aviso**. Qualquer outro problema recusa o arquivo com o motivo.

**Versionamento.** Um arquivo de versão **mais nova** que a do programa é recusado ("atualize o programa"). Para versões mais antigas
existe a tabela `MIGRATIONS` (versão n para n + 1), vazia enquanto só existe a versão 1; uma mudança incompatível do formato soma a
versão e acrescenta a migração.

**API.** `POST /api/scenario/save` com `{ kind, data }` devolve `{ filename, mime, content }`; `POST /api/scenario/load` com
`{ text }` devolve `{ kind, version, saved_at, data, warnings }`. Erros no formato da seção 11.3.

**Efeito colateral.** Os fatores, o método e os níveis da sensibilidade passaram a ficar na memória da página (antes eram locais da
tela e se perdiam ao trocar de página); continuam sem ir para o navegador (`dietopt.v1` só guarda a seleção e os parâmetros).

**Não feito.** Histórico de cenários, salvamento automático e cenário do Exercício simples.

**Aceite.** `tests/test_scenario_files.py`: ida e volta (idempotente), avisos de alimento removido, os dados inválidos de cada campo,
arquivo inválido ou de versão mais nova, BOM e migração.

### A.12 Histórico de execuções (implementado em 03/11/2026, etapa D3 da repaginação)

**Objetivo.** Guardar cada execução com seus parâmetros e resultado, para consultar, comparar com um cenário-base, reabrir os
parâmetros e exportar, sem depender de captura de tela.

**O que é uma execução.** Qualquer uma destas, num histórico único (a tabela traz o tipo numa coluna): **simulação** do RuFaS,
**sensibilidade**, **avaliação de dietas** e **dieta ótima**. As tarefas que falham também entram (estado "Falhou", com o
motivo); cancelar não é execução. Uma simulação que vem do cache do RuFaS também é gravada.

**Armazenamento** (`backend/dietopt/history.py`). Arquivos em `runs/_history` (pasta local, fora do git): `<id>.json` (parâmetros
e resultado completos) e `<id>.meta.json` (título, tipo, estado e um resumo pequeno), para listar sem abrir os resultados grandes.
O identificador é `AAAAMMDD-HHMMSS-nnnn` e cresce com a ordem de gravação; a escrita é atômica (arquivo temporário e troca).
O histórico guarda no máximo 200 execuções e apaga as mais antigas que não sejam o cenário-base.

**Cenário-base.** Uma execução **concluída** por tipo pode ser marcada com a estrela; marcar outra do mesmo tipo troca a base.
Na tela Vaca leiteira, cada indicador mostra a variação em % em relação à simulação-base (receita e margem: subir é bom; custos:
descer é bom); sem base, a tela explica como defini-la, e na própria base não há variação.

**API.**

| Rota | Corpo | Resposta |
|---|---|---|
| `GET /api/history?kind=&status=&q=&page=&per_page=` | | `{ items, total, page, per_page, pages }`; `items` são metadados (sem o resultado), da mais recente para a mais antiga; a busca `q` olha título, tipo, nome das dietas e código |
| `GET /api/history/<id>` | | execução completa: metadados, `params` e `result` |
| `GET /api/history/base?kind=` | | metadados da base do tipo, ou `null` |
| `POST /api/history/<id>/base` | `{ value }` | metadados atualizados |
| `POST /api/history/<id>/delete` | `{}` | `{ ok: true }` |

`kind`: `simulation`, `sensitivity`, `evaluation` ou `optimization`; `status`: `done` ou `error`; `per_page` de 1 a 100. O resultado
das tarefas e da avaliação de dietas passa a trazer `run_id`. Identificador inválido ou execução inexistente voltam como erro no
formato da seção 11.3.

**Tela Execuções** (`/execucoes`, item no grupo Análise). Tabela com busca, filtro por tipo e por estado, linhas por página (10, 25
ou 50), estrela do cenário-base, tipo e estado em pills (ícone e texto), resultado principal em uma linha, data e as ações: **ver**,
**duplicar** (abre os parâmetros na tela de origem, para editar e executar de novo), **exportar** (JSON com parâmetros e resultado)
e **excluir** (com confirmação), mais a paginação. Sem execuções, mostra o estado vazio com os passos.

**Detalhe** (`/execucoes/?id=<id>`). Parâmetros usados à esquerda (valores gerais, fatores, exigências, vaca, alimentos com preço e
limites, dietas) e os resultados à direita: a simulação reaproveita os resultados da tela Vaca leiteira (abas, gráficos e
exportação), a sensibilidade reaproveita a tabela e os gráficos de cenários, e a avaliação de dietas e a dieta ótima mostram o
ranking ou a ração. Uma execução que falhou mostra o motivo.

**Não feito.** Renomear ou comentar execuções, comparar duas execuções lado a lado, limpar o histórico de uma vez e o delta dos
indicadores das demais telas (Sensibilidade, Avaliar dietas), que seguem nas etapas D4 e D5.

**Aceite.** `tests/test_history.py`: gravação e resumo de cada tipo, listagem com filtros, busca e paginação, base única por tipo e só
para execução concluída, exclusão, identificador inválido, retenção que preserva a base, falha gravada com o motivo, cancelamento
ignorado e arquivo corrompido fora da lista.

### A.13 RF-13: tamanho do rebanho (implementado em 10/11/2026, etapa E8g)

**O que o usuário faz.** Na tela Vaca leiteira, o campo **Vacas no rebanho** (padrão 100, de 60 a 500) vale para a simulação e para a sensibilidade. Fora da faixa, ou não inteiro, o campo mostra o motivo e os botões Executar ficam desabilitados; o servidor repete a validação (erro 500 no formato da seção 11.3). Acima de 250 vacas a tela avisa o tempo e a memória de cada simulação. O número entra no arquivo de cenário (`params.cowNum`; arquivos antigos abrem com 100), no resumo e no título da execução no histórico (só quando difere de 100), na tela de detalhe e no relatório HTML. Os totais do rebanho (margem, receita, custo de alimentação, leite total) só são comparados com o cenário-base se os dois têm o mesmo número de vacas; os valores por vaca sempre são.

**Por que não basta `cow_num`.** O exemplo `freestall` tem 100 vacas e, junto, bezerras, novilhas, uma reserva de reposição e um tamanho-alvo (`herd_num`): o RuFaS vende novilhas prenhes quando vacas e novilhas prenhes passam de 103% do alvo e compra reposição abaixo de 101%. Mudar só `cow_num` deixava o alvo em 100 e o RuFaS recompunha o rebanho. Além disso, cada lote tem um número fixo de baias (`number_of_stalls`) e o RuFaS recusa a simulação se o lote passa da lotação máxima (500 vacas falhou com "Number of stalls in calf pen"). O adaptador (`backend/dietopt/herd.py`, `scale_herd`) escala por `cow_num / 100`: o próprio `cow_num` e o `herd_num`, bezerras, novilhas I, II e III, a reposição (`replace_num`) e as baias de todos os lotes (arredondando para cima), com mínimo de 1. Informar 100 equivale a não informar (mesma chave de cache).

**Limites verificados** (simulações reais, 1 ano, NRC, 7 alimentos, mesma máquina, medidas em 10/11/2026):

| Vacas | Resultado | Tempo | Pico de memória |
|---|---|---|---|
| 10 | falha (`IndexError` no otimizador de ração de um lote) | | |
| 50 | falha (`ZeroDivisionError`, ver abaixo) | | |
| 60 | ok (também com 3 anos: 45 s, 1,0 GB) | 25 s | 0,65 GB |
| 75 | ok (também com 3 anos) | 50 s | 0,66 GB |
| 90 | ok | 34 s | 0,67 GB |
| 100 | ok (padrão) | 27 s | 0,68 GB |
| 200 | ok (leite total 2,0× o de 100 vacas) | 37 s | 0,75 GB |
| 500 | ok | 57 s | 0,96 GB |

O tempo cresce cerca de 20 s mais 0,075 s por vaca e a memória, cerca de 0,6 GB mais 0,7 MB por vaca; a interface usa essa reta, relativa à estimativa de 17 s para 100 vacas, no aviso e na previsão de tempo da sensibilidade. O teto de 500 é o maior tamanho medido (a máquina de teste tinha pouca memória livre; 1000 vacas não foi tentado).

**Limitação do RuFaS (PRD, L9).** Abaixo de 60 vacas a simulação quebra por um defeito do próprio RuFaS 1.0.6: em `herd_manager.py`, ao inserir um animal num lote vazio sem ração definida pelo usuário, a lista de alimentos do lote é filtrada com o dicionário inteiro de rações em vez da lista do lote; o lote das bezerras fica sem alimentos e a divisão por zero aborta a simulação. Em rebanhos pequenos o lote das bezerras esvazia entre um nascimento e outro. O código do RuFaS não é alterado, então o mínimo fica em 60 vacas. O resultado de um tamanho só vale se a simulação concluir; o limite foi verificado com a semente 42, e outra semente pode falhar perto do mínimo (a mensagem do RuFaS aparece no erro da execução).

### A.8 Alterações previstas em outras partes deste documento (quando implementado)

| Seção | Alteração |
|---|---|
| 3 e 12 | Registrar a biblioteca NASEM e o arquivo `custom_feeds.json` |
| 9.3, 11.2 | Campo `standard` nos parâmetros e nos corpos; parâmetro `standard` em `/api/feeds`; campo `checks` no resultado; tarefa `compare` |
| 10.4, 10.6 | Seletor de padrão, botão de comparação, cartão Verificações, seletor com alimentos personalizados |
| 14 e 15 | Regras do padrão, das verificações e dos alimentos personalizados |
| 16 | Mensagens novas (alimentos removidos, padrão inválido, verificações) |
| 23 | Casos de validação de A.3.6, A.4.5 e A.5.4 |
| 26 | Remover D7 quando a exibição de NEL for corrigida |


---

## Anexo B. Especificação do Módulo Ampliado do Exercício do Quadro (RF-28 a RF-30; fases 1 e 2 implementadas)

> **Status (03/11/2026):** a **fase 1** (RF-28, RF-29: avaliação e ordenação de dietas, com a interface da seção B.2) está
> implementada, com a comparação com o RuFaS da B.8 (fase 1, etapa E6, 03/11/2026); a **fase 2** (RF-30: dieta ótima e
> comparação com o `RationOptimizer`, etapa E7, 03/11/2026) também está implementada, como descrito na seção B.11.
> A base técnica (equações do RuFaS,
> linearização, verificação do erro) está em [LINEARIZACAO.md](LINEARIZACAO.md); este anexo especifica o
> **comportamento funcional**, a interface e a API. Onde um fato não foi verificado, o texto diz **"a verificar"**; onde a
> decisão é da equipe ou do professor, diz **"(a confirmar)"**.

### B.1 Visão geral

**Origem.** Pedido do professor de Pesquisa Operacional: maximizar a sessão "Exercício do quadro", com entradas mais
ricas (características da vaca, exigências e restrições nutricionais pelo NASEM, dieta escolhida e preços em dólares) e com
**equações lineares**, para que o otimizador próprio seja **comparável** ao do RuFaS.

| ID | Requisito | Fase |
|---|---|---|
| RF-28 | Avaliar e comparar dietas já montadas para uma vaca (categoria e fase) | 1 |
| RF-29 | Modelo linear das restrições, verificação do erro de linearização e comparação com o RuFaS | 1 |
| RF-30 | Sugerir e prever a dieta ótima para a vaca e a fase | 2 (posterior) |

**Decisões vigentes (de `LINEARIZACAO.md`, seção 1):** documento principal NASEM 2021, apoio NRC 2001; preços do CEPEA em
dólares (conversões depois); categorias só as que o RuFaS otimiza; o RuFaS é replicado onde diverge do livro; a entrada é
uma dieta já montada.

**Dependências.** RF-24 (padrão NASEM) para o modo NASEM; RF-27 (verificações) reaproveita parte das regras; RF-26 para o
arroz em grão. Sem RF-24, o módulo funciona só no padrão NRC.

### B.2 Interface

O módulo amplia a **tela 1 (Exercício do quadro)**, sem remover o exercício atual.

- Um seletor no topo da tela alterna entre **"Exercício simples"** (o atual, padrão da tela) e **"Avaliar dietas (vaca
  real)"**.
- No modo ampliado, a tela tem quatro cartões, em ordem:

| Cartão | Conteúdo |
|---|---|
| **Vaca** | Padrão nutricional (NASEM ou NRC); categoria (B.3); campos da vaca (B.3); exigências calculadas, com a opção de **sobrescrever** cada uma |
| **Dietas** | Tabela de dietas montadas: nome e quantidades (kg MS/dia) por alimento (B.4); botões **+ Dieta** e **Remover** |
| **Preços** | US$/kg MS por alimento, com valor original, unidade, moeda, câmbio e base (B.5) |
| **Resultado** | Botão **Avaliar dietas**; **ranking** das dietas; detalhe por restrição de uma dieta escolhida; erro de linearização |

- Estados: antes de avaliar, texto "Informe a vaca, monte as dietas e clique em Avaliar dietas."; durante o cálculo, botão
  desabilitado ("Avaliando…"); erro, aviso com a primeira linha da mensagem (padrão da seção 16).
- O cálculo não executa o RuFaS completo (seção B.6): é **síncrono** e rápido, sem tarefa em segundo plano.

**Implementada em 03/11/2026 (etapa E5)**, em `web/src/views/ExerciseView.tsx`, `ModuleView.tsx` e `web/src/views/module/`.
Onde a tela difere ou completa o texto acima:

- O seletor "Exercício simples" × "Avaliar dietas (vaca real)" fica no cabeçalho da tela 1; o exercício simples continua o
  padrão. A escolha e todos os dados do modo ampliado ficam na memória da página (some ao recarregar).
- **Vaca:** o padrão (NASEM, principal, ou NRC), a categoria e o tipo de animal (vaca seca ou novilha pré-parto; novilha I ou
  II) ficam neste cartão. Os campos vêm de `GET /api/module/defaults` (obrigatórios com `*`, faixas validadas) e abrem com uma
  vaca de **exemplo** da categoria; trocar de categoria ou de tipo volta ao exemplo do novo tipo. Os campos do lote (metano e N
  urinário, só NASEM) e da ração anterior (opcionais; vazio = vem da dieta) têm blocos próprios. As exigências vêm de
  `POST /api/module/requirements` (com atraso de 0,4 s após a digitação), com a coluna **Sobrescrever** por exigência.
- **Dietas:** tabela com uma linha por alimento e uma coluna por dieta (nome editável, até 10), total por dieta e o consumo
  estimado; busca para adicionar alimentos da biblioteca do padrão; botão **Dietas de exemplo** (três dietas cujo total é o
  consumo estimado). Ao trocar o padrão, os alimentos que não existem na nova biblioteca saem da tabela, com o aviso
  "Removidos por não existirem no padrão <X>: <lista>." (o mesmo texto de A.3.1).
- **Preços e limites** (no lugar de "Preços"): US$/kg MS e limites mínimo e máximo por alimento (kg MS/dia), com os padrões da
  seção 14.3. A conversão de reais, de matéria natural e do CEPEA continua para depois (B.5).
- **Resultado:** o botão fica desabilitado com a lista do que falta (campos obrigatórios ou fora da faixa, dieta sem
  quantidades, nome repetido, preço ausente, mínimo maior que o máximo). O ranking mostra a **posição 1 como a mais
  recomendada** (a API devolve a lista da menos para a mais recomendada); a dieta viável de menor custo leva o selo "Melhor
  entre as informadas". Estados em texto e ícone: **Viável**, **Inviável** e **Viável, incompleta** (alguma restrição sem
  dados, como a energia do NASEM sem metano e N urinário); por restrição: **Atende**, **No limite**, **Violada** e
  **Indisponível** (com a nota do que falta). O detalhe de uma dieta (clique no nome) traz consumo, TDN%, % de concentrado,
  desconto de ingestão e a tabela de restrições com exigência, oferta linear, oferta do RuFaS, erro de linearização
  (destacado acima de 1%), folga e estado. Se as entradas mudarem depois de avaliar, o resultado fica esmaecido com o aviso
  "As entradas mudaram desde a última avaliação".
- **Não feito nesta etapa:** persistência em `localStorage`, seletor de padrão da simulação (A.3.1, tela Vaca leiteira) e
  o selo do cabeçalho com o padrão.
- A cor nunca é o único canal: estados "viável", "inviável" e "no limite" também aparecem em texto.
- Os dados do modo ampliado ficam na **memória da página** (como o exercício simples); persistência em `localStorage` fica
  como melhoria **(a confirmar)**.

### B.3 Entradas: padrão, categoria e vaca

**Padrão:** `NASEM` (principal) ou `NRC`. **Categoria**, só as que o RuFaS otimiza (`LINEARIZACAO.md`, seção 2):
`LAC_COW` (vaca em lactação), `CLOSE_UP` (vaca seca e novilha pré-parto), `GROWING` (novilhas I e II).

Campos (assinatura de `calculate_requirements` do RuFaS; o uso por categoria foi verificado em 01/11/2026 perturbando cada
campo nas calculadoras NRC e NASEM; "NASEM" e "NRC" indicam que só aquele padrão usa o campo):

| Campo | Unidade | Lactação | Seca e pré-parto | Crescimento |
|---|---|---|---|---|
| Peso corporal (`body_weight`) | kg | sim | sim | sim |
| Peso à maturidade (`mature_body_weight`) | kg | sim | sim | sim |
| Paridade (`parity`) | número | sim | sim | opcional |
| Dias em lactação (`days_in_milk`) | dias | sim | NASEM: opcional | NASEM: opcional |
| Dia de gestação (`day_of_pregnancy`) | dias | NASEM: opcional | sim | opcional (novilha prenhe) |
| Escore de condição corporal (`body_condition_score_5`) | 1 a 5 | NASEM | não | NRC |
| Produção de leite (`milk_production`) | kg/dia | sim | não | não |
| Gordura, proteína verdadeira e lactose do leite | % | sim | não | não |
| Ganho médio diário da novilha (`average_daily_gain_heifer`) | **kg/dia** (o texto do RuFaS diz g, mas o código usa kg; 0,8 e não 800) | não | não | sim |
| Intervalo entre partos (`calving_interval`) | dias | opcional (vazio vale 0 e desliga o ganho de peso da vaca de 1ª ou 2ª paridade; há aviso) | opcional (idem) | não |
| Idade (`days_born`; só o NRC, e só para novilhas) | dias de vida | não | não | NRC: sim |
| Alojamento (`housing`: `Barn` ou `Grazing`) e distância percorrida | m | sim | sim | sim |
| FDN da ração anterior (`ndf_percentage`) | % da MS | opcional | opcional | opcional |
| Fósforo do processo (`process_based_phosphorus_requirement`) | g/dia | opcional | opcional | opcional |
| TDN% da dieta, temperatura anterior e concentração de energia líquida da dieta (só NRC) | fração, °C, Mcal/kg | TDN% | TDN% | os três |
| Metano entérico e nitrogênio urinário do lote | g/dia e kg | NASEM | NASEM | NASEM |

As calculadoras rodam **sem iniciar uma simulação** (verificado). O TDN% e os demais campos exclusivos do NRC dependem da
dieta e, no módulo, vêm da própria dieta avaliada. O metano entérico e o nitrogênio urinário do lote (última linha da tabela) são
**saídas do RuFaS**: médias do lote dos valores do dia anterior de cada animal, usadas só no NASEM; para uma vaca isolada o
módulo os recebe ou os estima pelas equações do NASEM (`LINEARIZACAO.md`, 7.3, decisão pendente L-Q2). Validações: valores numéricos positivos onde aplicável; campos
vazios usam o padrão do RuFaS apenas onde o RuFaS define um **(a verificar)**; nenhum valor inventado.

### B.4 Entradas: dietas montadas

- Até **10 dietas** por avaliação **(a confirmar)**; cada dieta tem **nome** e uma lista de alimentos da **biblioteca do
  padrão escolhido**, com a quantidade em **kg de MS por dia**.
- Validações: ao menos um alimento; quantidades maiores ou iguais a zero; consumo total maior que zero. Alimentos ausentes na
  biblioteca do padrão (RF-24, A.3.1) são removidos da dieta, com aviso.
- Os alimentos personalizados (RF-26) valem aqui, no padrão em que existirem.
- Os limites por alimento (mínimo e máximo, kg MS/dia) valem como restrições (`LINEARIZACAO.md`, 4.1) e entram na
  verificação de cada dieta.

### B.5 Entradas: preços

- US$ por kg de MS, por alimento. Valores iniciais ilustrativos (seção 14.3), rotulados como tais.
- Campos de origem (regra de conversão em `LINEARIZACAO.md`, 7.2): valor original, unidade comercial, moeda, câmbio (R$ por
  US$), base (matéria natural ou MS) e fonte (indicador do CEPEA e data). A conversão automática e o mapeamento CEPEA ×
  biblioteca **ficam para depois**; nesta fase o usuário informa o valor em US$/kg MS, ou o valor original com o câmbio.
  **Implementado em 03/11/2026 (etapa E8d):** a importação de preços por CSV (seção A.9) aplica essa conversão; o mapeamento
  indicador × alimento é feito pelo usuário no arquivo (por id do RuFaS ou nome), e a leitura automática do CEPEA segue pendente.

### B.6 Cálculo

Para cada dieta `d`, com os coeficientes avaliados **na própria dieta** (ponto de referência `x_d`):

1. **Exigências** da vaca, pelo RuFaS (calculadoras NASEM ou NRC), com as sobrescritas do usuário. As
   calculadoras podem ser chamadas diretamente, sem iniciar uma simulação do RuFaS (**verificado** em 01/11/2026, para NRC e NASEM,
   nas seis categorias).
2. **Restrições aplicáveis** (`LINEARIZACAO.md`, seções 2 e 3): custo, limites por alimento, consumo, cálcio, fósforo,
   FDN total, FDN de forragem, gordura, energia (NRC: mantença, lactação, crescimento e total; NASEM: energia líquida), e
   proteína metabolizável.
3. **Oferta linearizada** de cada restrição (técnicas A, B e D), com os coeficientes calculados em `x_d`.
4. **Oferta não linear** (funções originais do RuFaS) e **erro de linearização** (`LINEARIZACAO.md`, seção 6).
5. **Folga** `= oferta − exigência` (ou o inverso nas restrições de teto), **estado** (viável ou inviável) e **violação
   normalizada** `V = Σ max(0, (exigência − oferta)/exigência)` (`LINEARIZACAO.md`, 7.4).
6. **Custo** `= Σ p_i·x_i`, em US$/dia.

Na fase 1 **não há otimização** (implementada em 02/11/2026, etapa E3); logo, **não há preços-sombra** (eles existem só quando um LP com `x` livre é resolvido,
RF-30; na fase 2 saem do LP da dieta ótima, seção B.11). Na disjunção de energia do NRC, a oferta usada é a do ramo que cobre a exigência total, ou a maior, se nenhum cobre.
O RuFaS é replicado onde diverge do livro (amido em kg; oferta de proteína do NRC no modo NASEM), com aviso no resultado.

**Ordenação (RF-28), da menos para a mais recomendada (a confirmar):**
1. Dietas **inviáveis**, em ordem decrescente de `V`.
2. Dietas **viáveis**, em ordem decrescente de custo.
A dieta viável de menor custo é marcada **"melhor entre as informadas"** (não "ótima": a ótima é do RF-30).

### B.7 API (implementada em 02/11/2026, etapas E2 e E3)

| Método e rota | Corpo | Resposta |
|---|---|---|
| `GET /api/module/defaults?standard=<NASEM\|NRC>&category=<LAC_COW\|CLOSE_UP\|GROWING>` | — | Campos da vaca da categoria, com unidade e se são obrigatórios; restrições aplicáveis |
| `POST /api/module/evaluate` | `{ standard, category, cow: {…}, requirements_override?: {…}, diets: [{ name, amounts: { <id>: <kg MS/dia> } }], prices: { <id>: <US$/kg MS> } }` | Para cada dieta: `cost`, `feasible`, `violation`, `constraints: [{ id, label, requirement, supply_linear, supply_nonlinear, error_pct, slack, status }]`, `warnings`; mais `requirements` calculadas e `ranking` (lista de nomes, da menos para a mais recomendada) |

Rota adicional (E2): `POST /api/module/requirements` com `{ standard, category, animal_type?, cow, requirements_override? }` devolve as
exigências calculadas, as sobrescritas aplicadas, os valores efetivamente enviados à calculadora e os avisos.

Detalhes da implementação de `POST /api/module/evaluate`:

- Corpo, além do acima: `limits?` (`{ <id>: [mín, máx] }` em kg MS/dia; padrão: 0 e o teto padrão do alimento, seção 14.2),
  `animal_type?` (`DRY_COW` ou `HEIFER_III` em `CLOSE_UP`; `HEIFER_I` ou `HEIFER_II` em `GROWING`) e, em `cow`, os campos do
  lote `enteric_methane` (g/dia) e `urinary_nitrogen` (kg/dia), usados só na energia do NASEM (`LINEARIZACAO.md`, 7.3).
  Sem eles, a restrição `ne_nasem` fica com estado `indisponivel` e a dieta, `incomplete: true` (decisão L-Q2 pendente).
- Resposta: `requirements` (calculadas com os padrões do RuFaS), `diets[]` (`cost`, `cost_per_kg`, `feasible`, `violation`,
  `violated[]`, `incomplete`, `intake`, `requirements` da própria dieta, `constraints[]`, `warnings[]`), `ranking[]` (da menos para a
  mais recomendada), `best` (viável de menor custo ou `null`) e `warnings[]`.
- Cada `constraints[]` traz `id`, `label`, `unit`, `kind` (L, E ou A), `sense` (`ge` ou `le`), `requirement`, `supply_linear`,
  `supply_nonlinear` (do `RationOptimizer` do RuFaS), `error_pct`, `slack` e `status` (`ok`, `no_limite`, `violada` ou
  `indisponivel`). Os limites por alimento entram como `limit_ge_<id>` e `limit_le_<id>`.
- As exigências são calculadas **para cada dieta**, com a própria dieta como "ração anterior" (TDN%, energia e FDN), como o RuFaS
  faz com a ração do dia anterior; valores informados pelo usuário nesses campos prevalecem.
- `error_pct` é o maior desvio, entre −5% e +5% das quantidades, da oferta linear (coeficientes congelados na dieta) em relação
  à oferta original, **em % da oferta original** (não da exigência: a exigência de crescimento do NRC é pequena e inflaria o
  número). É 0 nas classes L e E, que são exatas.
- "No limite": folga de até 0,5% da exigência. Até 10 dietas por avaliação.

Erros no formato da seção 11.3. A rota é síncrona. O `id` dos alimentos é o `rufas_id` da biblioteca do padrão.

Rota da comparação (E6): `POST /api/module/compare`, com o mesmo corpo de `evaluate` e `tolerance_pct?` (padrão 1; a tolerância
ainda é uma decisão em aberto, L-Q1). Cada restrição de `evaluate` traz também `probes`: as ofertas linear e original com as
quantidades escaladas por 0,95 e 1,05 (só a classe A; vazio nas classes L e E).

### B.8 Comparação com o RuFaS (RF-29)

- **Fase 1 (implementada em 03/11/2026, etapa E6; `module/compare.py`):** para a mesma vaca, o mesmo lote e a mesma dieta, comparar a oferta e a folga de cada restrição **linearizada**
  com a **original do RuFaS** (as funções `NutritionSupplyCalculator.*`, chamadas diretamente; **verificado** em 01/11/2026: o estudo numérico de `LINEARIZACAO.md`, seção 10, já as chamou assim).
  Relatório: erro por restrição e por dieta, com as tolerâncias de `LINEARIZACAO.md`, seção 6.
  Como ficou: para cada dieta e restrição, a oferta e a folga lineares e originais, o erro **com sinal** (em % da oferta original)
  no ponto e a −5% e +5%, o maior erro em módulo, se está dentro da tolerância, a igualdade no ponto (1e-6), o estado (viável ou
  violada) nos dois modelos e se ele coincide nas sondagens; por dieta, o maior erro, a restrição de maior erro e quantas passam
  da tolerância; e um resumo geral. Os limites por alimento não entram (não têm função equivalente no RuFaS). Restrições sem
  dados (energia do NASEM sem metano e N urinário) ficam de fora das contagens, com a nota. O relatório sai na tela (cartão
  "Comparação com o RuFaS", depois do resultado) e em CSV (uma linha por dieta e restrição; botão "Baixar CSV"). A disjunção
  de `LINEARIZACAO.md`, seção 6 ("o ramo escolhido continua o de maior oferta?"), não tem coluna própria: o `min` e o `max` ficam
  dentro da forma linear e uma troca de ramo aparece no erro de oferta.
- **Fase 2 (implementada em 03/11/2026, etapa E7; `module/optimize.py`):** comparar o LP (ótimo global do problema linearizado) com
  o otimizador do RuFaS (`RationOptimizer`, ótimo local, ponto inicial aleatório quando não há ração anterior): custo, ração e
  folgas (`LINEARIZACAO.md`, 5.4). O RuFaS roda com as sementes 0 a N−1; entram na estatística as execuções que convergem e
  ficam viáveis nas restrições originais, com a tolerância relativa de 1e-5 do SLSQP. Resultado e detalhes na seção B.11.

### B.9 Critérios de aceite

1. **Identidade no ponto:** para cada dieta, a oferta linearizada avaliada em `x_d` é igual à não linear, dentro de 1e-6.
2. **Erro fora do ponto:** com os coeficientes de `x_d` e as quantidades da dieta variadas de −5% a +5%, o erro de oferta
   fica em até 1% da oferta original (`LINEARIZACAO.md`, seções 6 e 10: a ±10% o erro de energia chegou a 1,5%) **(a confirmar)**.
   Medido em 02/11/2026 (NRC, vaca em lactação, quantidades de −5% a +5%): no regime sem desconto (TDN% ≤ 60, `D` = 1) o erro
   de energia é 0 e o de proteína fica em até 0,4%; no regime com desconto, o erro cresce com o TDN%: 0,5% a 0,7% (TDN 61%),
   1,2% a 2,4% (TDN 70%) e 2% a 4% (TDN 77%); a proteína fica em até 0,2%. O critério de 1% **não vale** para dietas com
   `D` < 1 e TDN% acima de ≈ 65; o erro é mostrado em cada restrição (`error_pct`), e a decisão L-Q1 (tolerância) fica para o
   professor. Na fase 2 o problema não aparece, porque a parametrização congela os escalares globais de forma exata.
3. **Razões exatas:** em dietas aleatórias, a forma linear de FDN, FDN de forragem e gordura (4.3) dá o **mesmo** estado
   viável/inviável que a razão original.
4. **`min` de proteína:** as duas restrições lineares equivalem ao `min` (4.6) em dietas aleatórias.
5. **Categorias:** novilhas e vacas secas, no modo NRC, **não** têm as restrições `NE_total` e `NE_lactation`.
6. **Ordenação:** inviáveis antes de viáveis; entre inviáveis, `V` decrescente; entre viáveis, custo decrescente.
7. **Vetores de teste:** as três rações guardadas de `LINEARIZACAO.md`, 5.3, não estão no repositório (`runs/` é local). O teste usa
   a ração do "Conjunto base" (TDN% = 59,97, `D` = 1) e uma com mais concentrado (TDN% = 69,9, `D` < 1), com ofertas de
   referência gravadas a partir do próprio RuFaS.
8. **Replicação do RuFaS:** o amido total em kg é usado na digestibilidade da FDN do NASEM, e o resultado traz o aviso.
9. **Testes automatizados** (`pytest`) para os itens 1 a 8, em `backend/tests/test_module_evaluate.py`; o RuFaS **não** é modificado.

### B.11 Dieta ótima (RF-30, fase 2; implementada em 03/11/2026, etapa E7)

Sugere a dieta de **menor custo** entre os alimentos da tabela de dietas, para a mesma vaca, com as mesmas restrições, e a compara
com o otimizador do RuFaS. O método está em `LINEARIZACAO.md`, 5.1b e 7.6 (LP por ponto de uma grade de escalares globais).

- **Tela:** cartão "Dieta ótima" depois do Resultado: resolução da busca (rápida ≈ 5 s, normal ≈ 15 s, fina ≈ 1 min), número de
  execuções do RuFaS (0 a 30; padrão 5), botão **Calcular dieta ótima** e **Cancelar**, com barra de progresso. Mostra o custo, o
  consumo, o TDN% e o % de concentrado, o regime (TDN% abaixo ou a partir de 60), a ração (kg MS/dia e % da dieta), a conferência com
  as restrições originais do RuFaS, a comparação com o RuFaS (custo do LP em relação ao melhor do RuFaS, melhor, mediana e
  quantas execuções ficaram viáveis; tabela por semente; ração do melhor do RuFaS), a tabela de restrições da dieta ótima e os
  **preços-sombra**. No cartão Resultado, a dieta ótima vira a **referência final** do ranking, com a coluna "Desvio do ótimo"
  `(custo_d − custo_ótimo)/custo_ótimo`; um desvio negativo é de dieta inviável mais barata que a ótima.
- **Entradas:** a vaca e as sobrescritas como na avaliação; os alimentos são **todos** os da tabela de dietas (não só os usados nas
  dietas), com preço e limites. No NASEM, metano e N urinário do lote são obrigatórios (sem eles a energia não existe).
- **API:** tarefa em segundo plano `POST /api/jobs/optimize`, com o corpo de `evaluate` sem `diets` e com `feed_ids`, `resolution`
  (`rapida`, `normal` ou `fina`) e `seeds` (0 a 30); progresso em `done` e `total`; `POST /api/jobs/<id>/cancel` pede o cancelamento
  (estado `cancelled`; um job ainda na fila nem começa). O resultado traz `status` (`ok` ou `infeasible`, com `message`), `diet`
  (`amounts`, `cost`, `scalars`, `regime`, `energy_branch`, `verified`, `evaluation` no formato de uma dieta de `evaluate`),
  `shadow_prices`, `rufas` (`runs`, `cost_min`, `cost_median`, `cost_max`, `n_success`, `lp_gap_pct`), `search` e `warnings`.
- **Exigências:** as da vaca sem ração anterior (padrões do RuFaS), como na primeira formulação do RuFaS; por isso elas diferem um
  pouco das exigências de cada dieta na avaliação, que usa a própria dieta como ração anterior. A tela avisa.
- **Preços-sombra:** variação do custo por unidade da exigência (ou do limite do alimento), com o consumo, o TDN% e o % de
  concentrado fixos no ponto ótimo; valem perto da dieta ótima.
- **Sem dieta viável:** o resultado é `infeasible` com a mensagem "Nenhuma dieta com os alimentos escolhidos atende às restrições…".
- **Não feito:** o laço de redução de leite do RuFaS (`LINEARIZACAO.md`, 7.6), a otimização por fase da lactação e a persistência
  do resultado entre recargas da página.
- **Critérios de aceite (E7):** a dieta ótima atende às restrições originais do RuFaS nas seis combinações de padrão e categoria;
  no caso-base do NRC o custo do LP fica a menos de 0,1% do melhor do RuFaS; nos escalares do melhor SLSQP o LP reproduz o custo do
  SLSQP (erro relativo abaixo de 1e-6); cancelamento, progresso e entradas inválidas têm testes (`test_module_optimize.py`, `test_jobs.py`).

### B.10 Riscos e itens a verificar antes de implementar

| Item | Risco | Como verificar |
|---|---|---|
| Chamar as calculadoras de exigência do RuFaS sem simulação | Dependências do pacote `RUFAS` (gerenciador de saídas, constantes) | **Verificado**: `calculate_requirements` roda isolado, em NRC e NASEM, para as seis categorias |
| Modo NASEM para novilhas e vacas secas | As calculadoras devolvem valores plausíveis, mas o otimizador do RuFaS não foi exercitado nessas categorias; a unidade do ganho diário (kg/dia) é fácil de errar | Avaliar casos de referência do NASEM (Tabela 21-1, com cautela) e validar a faixa de entrada do ganho diário |
| Metano e nitrogênio urinário de uma vaca isolada | Valores do lote não existem fora do RuFaS | Decisão L-Q2 |
| Otimização linearizada (fase 2) | O ponto fixo simples parou 4,8% acima do RuFaS; o desconto de ingestão é descontínuo em TDN% = 60 | Parametrização dos escalares globais, com dois regimes (`LINEARIZACAO.md`, 5.1b e seção 10) |
| Biblioteca de alimentos | Alimentos NRC-only ou NASEM-only (RF-24) | Aviso e remoção (A.3.1) |

### B.11 Alterações previstas em outras partes deste documento (quando implementado)

| Seção | Alteração |
|---|---|
| 3, 4 e 5.1 | Novos módulos do back-end e testes do modelo linear |
| 6, 10 e 13 | Escopo, tela 1 ampliada (cartões Vaca, Dietas, Preços e Resultado) e novo fluxo "Avaliar dietas montadas" |
| 11 | Rotas `GET /api/module/defaults` e `POST /api/module/evaluate` |
| 14, 15 e 16 | Regras de ordenação, cálculo linearizado e mensagens |
| 23 | Casos de validação de B.9 |

# DECISÕES TÉCNICAS DO PROJETO

> Adaptado de um modelo pensado para um sistema a ser criado do zero. Aqui a
> diferença é importante: o **Dieta Ótima com RuFaS já está implementado e
> verificado** (protótipo acadêmico, ainda sem uso em produção) — este documento
> não propõe decisões, ele **registra** as que já foram tomadas (extraídas do
> PRD, do DESIGN, do DOMINIO e do código-fonte real), sinaliza o que ainda está
> em aberto, e alerta o que o FSD não deve inventar.
>
> Data de referência: 12/10/2026.

## 1. Documentos recebidos

- `PRD.md` (v0.3): recebido — fonte funcional, descreve o que o sistema deve
  fazer, os requisitos com situação (atendido, parcial, pendente), as regras de
  validação e as questões em aberto.
- `DESIGN.md` (v0.2): recebido — documenta o padrão visual implementado na
  interface web (tokens de cor, tipografia, componentes, telas, acessibilidade),
  a origem no template AdminCN e as decisões de interface D1 a D12.
- `DOMINIO.md`: recebido — registra o domínio, as entidades, as regras de
  negócio implementadas e o mapeamento técnico regra → arquivo → função →
  teste. Usado aqui como fonte técnica primária, complementar ao PRD — este
  documento não repete o que já está lá.
- `README.md` (raiz do projeto): instruções de instalação e uso.
- `FSD.md`: **ainda não existe** (é o próximo documento).
- Materiais de origem, fora do repositório: o quadro do professor de Pesquisa
  Operacional (problema da dieta, diagrama simulador/otimizador/sensibilidade,
  gráfico da lactação) e o PDF *Nutrient Requirements of Dairy Cattle* (NRC,
  2001). O sistema não lê o PDF: a composição dos alimentos vem das tabelas do
  próprio RuFaS (`NRC_comp.csv`).
- Observação: como o sistema já está implementado, "decisão técnica" aqui
  significa "o que já está implementado e funcionando", não "o que se
  pretende construir".

## 2. Identificação do sistema

- **Nome:** Dieta Ótima com RuFaS
- **Objetivo principal:** formular a dieta de vacas leiteiras de custo mínimo e
  medir seu efeito econômico (margem sobre o custo de alimentação) ao longo da
  lactação, usando o RuFaS como simulador e permitindo testar muitos cenários
  de preço.
- **Público usuário:** nutricionista de rebanho leiteiro e produtor de leite
  (personas do PRD, seção 4); o professor de Pesquisa Operacional como
  avaliador.
- **Contexto de uso:** local e individual, na própria máquina do usuário
  (Windows), sem uso remoto. Cada simulação leva de 30 a 37 s.
- **Resumo funcional:** resolve o exercício de dieta do quadro por programação
  linear; simula uma vaca leiteira no RuFaS com alimentos, preços e limites
  escolhidos e calcula receita, custo e margem; roda análise de sensibilidade
  (cenários S1..SN com coluna `Res` e efeito de Spearman); desenha a curva de
  lactação de Wood com PEV e gestação; explica premissas e limites do modelo.

## 3. Decisões técnicas confirmadas

### Stack
**Python 3.12.10** (ambiente virtual do projeto) para o servidor local, o
adaptador do RuFaS, o PL, a sensibilidade e a curva de lactação, com a
biblioteca padrão (`http.server`) no servidor e **NumPy/SciPy** nos cálculos.
**TypeScript** (modo estrito) com **Next.js 16**, **React 19**, **Tailwind CSS
4**, **shadcn/ui** (sobre Base UI) e **Recharts** na interface, exportada como
**site estático**. O simulador é o **RuFaS v1.0.6** (Python), usado sem
modificação. Não há framework web de backend (Flask, Django, FastAPI), ORM nem
servidor Node em tempo de uso.

### Arquitetura
A interface (HTML, JS e CSS estáticos) fala, via HTTP/JSON, exclusivamente com
`127.0.0.1:8000` — um servidor Python local que expõe 9 rotas de API e serve os
arquivos de `frontend/`. Simulações e sensibilidades são tarefas em segundo
plano (uma por vez); cada uma monta uma pasta de cenário em `runs/<nome>/`, chama
o RuFaS (`main.py`) em um **subprocesso** e lê os JSONs de saída filtrados.
Não há backend remoto nem servidor compartilhado: cada instalação é individual.

### Integração com o RuFaS
Decisões já tomadas:
- **Chamar o RuFaS completo** como simulador (subprocesso), em vez de reaproveitar
  só suas fórmulas — decisão do usuário.
- **Não modificar o RuFaS** (GPLv3, versão fixada v1.0.6); toda adaptação fica em
  `backend/dietopt/rufas_adapter.py`, que escreve cópias editadas dos arquivos
  de entrada.
- **Caminhos relativos** a `vendor/RuFaS`, porque o validador do RuFaS rejeita
  caracteres acentuados e o caminho do projeto contém "Á".
- **Sucesso** definido pelo código de saída 0 e pela linha `Finished task: 1/1
  with 0 error(s)` no console, porque o gerenciador de tarefas do RuFaS sai com
  código 0 mesmo em falha.
- **Ração formulada pelo próprio RuFaS** (otimizador SLSQP); o sistema informa
  só a lista de alimentos permitidos, preços e limites.
- **Leite = o simulado pelo RuFaS** (curva de Wood, reduzida só quando a ração
  não atende às exigências); o sistema não prevê leite próprio.
- **Padrão nutricional NRC 2001**; alimentos que só existem no NASEM no exemplo
  base são trocados (301 → 230, 302 → 167).
- **Redução máxima de leite** de 5,0 kg/vaca/dia por padrão, para a simulação
  degradar em vez de abortar.
- **Semente fixa (42)** e versões fixadas, para mesma entrada dar mesmo
  resultado.

### Banco de dados
Não existe banco de dados relacional nem NoSQL. Os dados vêm de arquivos do
RuFaS (biblioteca de alimentos e exemplo `freestall`), de constantes do código
(preços ilustrativos, parâmetros de Wood de referência) e do que o usuário
digita. A persistência é por arquivos: a pasta `runs/` (cenários, logs e cache
`runs/_cache/*.json`) e o `localStorage` do navegador.

### Ambientes
- **Local:** a máquina de quem usa e mantém o código — única existente. O
  projeto fica em uma pasta sincronizada pelo OneDrive; o build da interface
  roda fora dela (`%LOCALAPPDATA%\dietopt-web-build`).
- **Distribuição ("produção"):** não existe um processo formal. O sistema roda a
  partir da própria pasta do projeto (`iniciar.bat`) depois de `scripts\setup.ps1`.
- **Homologação:** não existe ambiente formal separado. Ver pendência na seção 10.

### Controle de versão
**O projeto não está sob controle de versão**: a pasta não é um repositório Git
(há um `.gitignore` já preparado, mas nenhum `git init`) e não há remoto. Apenas
`vendor/RuFaS` é um clone Git do RuFaS na tag v1.0.6 (histórico raso, de terceiros).
A sincronização do OneDrive não substitui versionamento. Ver pendência na seção 10.

### Autenticação
Não existe login, senha ou token. O sistema não pede, não armazena e não
transmite nenhuma credencial. Ele não acessa serviços externos em tempo de uso.

### Autorização
Não existe. Toda requisição recebida pelo servidor local é atendida; a única
barreira é o servidor escutar em `127.0.0.1` por padrão (`--host` configurável).
Não há token, validação de `Host`, de `Origin`/`Referer` nem limite de
requisições. Ver alertas na seção 8.

### Usuários e permissões
Perfil único e implícito: quem abre a aplicação. Sem hierarquia e sem
diferenciação de acesso (PRD §4.4). Marina, Carlos e o professor são personas
de produto, não perfis do sistema.

### Auditoria
Não existe. Nenhum registro de quem simulou o quê. Cada cenário deixa a pasta
`runs/<nome>/` com os arquivos de entrada e o `console.log`, o que permite
reconstruir *o que foi simulado*, mas não *por quem* nem *quando* (além das
datas dos arquivos). Ver pendência na seção 10.

### Soft delete
Não aplicável. O sistema não tem modelo de dados próprio sujeito a exclusão —
não existe operação de exclusão em lugar nenhum. A pasta de um cenário é
recriada se o mesmo nome for reutilizado, e nenhuma pasta antiga é apagada
automaticamente.

### Logs
- **Servidor HTTP:** o log de cada requisição é silenciado (`log_message`); só
  uma linha de início ("Servidor em http://…") é escrita no console, visível
  enquanto a janela estiver aberta.
- **Simulações:** persistidas em disco. Cada execução grava `runs/<nome>/console.log`
  (saída do RuFaS) e as pastas `logs/` e `tm_logs/` do RuFaS (verbosidade
  `errors`). O motivo resumido de uma falha é exibido na tela; o detalhe fica no
  arquivo.
- Não há log estruturado, retenção definida nem serviço centralizado.

### Configurações / dados de referência
Não há arquivo único de configuração. Os dados de referência estão em:
- `vendor/RuFaS/input/` — exemplo `freestall` (config, animal, feed, metadata) e
  as tabelas `NRC_comp.csv` e `user_feeds.csv`, que o adaptador copia e edita por
  cenário;
- `scenarios.py` — `DEFAULT_PRICES` (19 alimentos, US$/kg MS, **ilustrativos**) e
  `DEFAULT_MILK_PRICE` (0,45 US$/kg);
- `feeds.py` — tetos de inclusão padrão por tipo de alimento;
- `lactation.py` — `DEFAULT_WOOD` (curva de referência usada sem simulação);
- `web/src/providers/AppProvider.tsx` — conjuntos de alimentos "base" e "ampla" e
  valores iniciais do exercício do quadro.

### Uploads
Não existe.

### Exportações
Não existe (PRD, RF-20 pendente). A forma atual de registrar um resultado é a
captura de tela.

### APIs e integrações externas
Nenhuma integração com serviço externo em tempo de execução. Duas dependências
técnicas locais, nenhuma via API HTTP de terceiros:
- **RuFaS v1.0.6** — chamado por linha de comando em subprocesso; entrada e saída
  por arquivos.
- **HiGHS (via SciPy)** — solucionador do PL do exercício do quadro.

Preços de mercado (CEPEA) e o padrão NASEM 2021 **não** são integrados (PRD,
RF-22 e RF-24 pendentes). A instalação, uma vez feita, funciona sem internet.

### Segurança
Servidor restrito a `127.0.0.1` por padrão; sem dados pessoais; proteção do
caminho nos arquivos estáticos (nada fora de `frontend/` é servido); erros
internos viram resposta JSON 500 sem derrubar o servidor. Não há as demais
camadas típicas (Host, Origin, token, limite de requisições, sanitização), nem
limite de tamanho do corpo das requisições. Detalhe do que existe em
`DOMINIO.md` §5.10; riscos na seção 8.

### Desempenho
Há requisitos de desempenho no PRD (RNF-01), todos atendidos nas medições:
uma simulação de 1 ano com 100 vacas em até 60 s (medido: 30 a 37 s) e uma
sensibilidade de 4 simulações em até 3 min (medido: cerca de 66 s, com 2 em
paralelo). Cada simulação usa cerca de 1,2 GB de RAM; por isso há **no máximo 2
simulações simultâneas e uma tarefa por vez**. Simulações repetidas voltam do
cache em segundos.

### Reprodutibilidade
Versão do RuFaS fixada (v1.0.6), dependências fixadas em `requirements-rufas.txt`,
semente aleatória fixa (42) e interface travada por `package-lock.json`. A
instalação é reproduzível por script (`scripts/setup.ps1`), inclusive onde o
`pip` falha por TLS (baixa os pacotes com `curl` para `wheelhouse/`).

### Testes
10 testes automatizados em `backend/tests/` (PL, amostragem e efeitos de
Spearman, adaptador e cache), todos passando. Integração real com o RuFaS e
interface foram verificadas manualmente, **sem teste automatizado**.

### Licenciamento
O RuFaS é GPLv3 e não é modificado. O template da interface é MIT (aviso em
`web/LICENSE-TEMPLATE.md`). A distribuição conjunta com o RuFaS deve respeitar a
GPLv3. Lista completa em `DESIGN.md`, seção Licenças.

### Fora de escopo técnico
Multiusuário ou multiestação numa mesma instalação; hospedagem em nuvem;
autenticação; banco de dados; modificação do código do RuFaS; qualquer
persistência de dados além do que está descrito na seção "Banco de dados".

## 4. Stack e ambientes

| Item | Valor |
|---|---|
| Linguagem (servidor, adaptador, cálculo) | Python 3.12.10 em `.venv` (o RuFaS exige 3.12 ou 3.13; o Python 3.14 do sistema não é usado) |
| Linguagem (interface) | TypeScript 5.9.3 (modo estrito), HTML e CSS gerados pelo Next.js |
| Banco de dados | Nenhum — arquivos do RuFaS, pasta `runs/` e `localStorage` |
| Servidor HTTP | `http.server` (`ThreadingHTTPServer`) da biblioteca padrão |
| Tecnologias de interface | Next.js 16.2.6 (exportação estática), React 19.2.4, Tailwind CSS 4.3.3, shadcn/ui sobre Base UI 1.6.0, Recharts 3.8.0, Lucide, next-themes, Sonner, fonte Geist |
| Bibliotecas Python | NumPy 2.2.0, SciPy 1.16.2 (PL com HiGHS e Spearman), pandas 2.3.2 (exigido pelo RuFaS); o código próprio só importa NumPy e SciPy além da biblioteca padrão |
| Simulador | RuFaS v1.0.6 em `vendor/RuFaS` (GPLv3), sem modificação |
| Ferramentas de build | Node 24.18 e npm 11.16 (Node 20.9 ou superior); só para quem altera a interface |
| Sistema operacional | Windows 10/11 (único testado) |
| Ambiente local | A máquina do usuário; `iniciar.bat` sobe o servidor na porta 8000 |
| Ambiente de homologação | Não existe formalmente (pendência, seção 10) |
| Ambiente de produção | Não existe separado do local |
| Deploy | Sem CI/CD e sem pacote de instalação. Uso = `scripts\setup.ps1` (uma vez) + `iniciar.bat`; alterar a interface = `scripts\build-web.ps1` (cerca de 15 s) |
| Tamanho em disco | `.venv` ≈ 615 MB, `wheelhouse` ≈ 140 MB, `runs` ≈ 48 MB, `frontend` 2,9 MB (valores observados) |
| Memória | ≈ 1,2 GB por simulação do RuFaS |

## 5. Arquitetura obrigatória

Este documento não detalha estrutura de pastas nem organização interna
função a função — isso já está registrado, com granularidade de
arquivo/função, no `DOMINIO.md` (seções 3 e 7); a organização da interface está
no `DESIGN.md` (Arquitetura e Origem, Apêndice B). O FSD usa esses dois
documentos como referência técnica de baixo nível, sem reconstruir o
levantamento do zero.

Restrições arquiteturais que valem para qualquer mudança:

| Restrição | Motivo |
|---|---|
| `vendor/RuFaS` não é modificado; toda adaptação fica no adaptador | GPLv3, versão fixada, isolar mudanças de versões futuras |
| Todo caminho passado ao RuFaS é relativo a `vendor/RuFaS` | O validador do RuFaS rejeita caracteres acentuados |
| A interface é um site estático servido pelo servidor Python | Execução local simples, sem Node em tempo de uso |
| Uma tarefa por vez, no máximo 2 simulações em paralelo | ≈ 1,2 GB de RAM por simulação |
| Falha do RuFaS nunca vira resultado zero | Sucesso exige código 0 **e** a linha de resumo da tarefa |
| Toda rota nova da API passa pelo mesmo tratamento de erro e de `NaN` | `clean()` e o `try/except` de `do_GET` e `do_POST` |
| Build da interface fora do OneDrive | Caminho com "Á" e 551 MB de `node_modules` |

## 6. Perfis e permissões em nível alto

| Perfil | Permissões |
|---|---|
| Usuário da aplicação (único perfil existente, implícito) | Resolver o exercício do quadro; escolher alimentos, preços e limites; disparar simulações e sensibilidades; ver resultados e a curva de lactação; ler premissas e limites. Não há operações de edição de dados de terceiros nem de administração |

Não existe perfil administrativo nem qualquer hierarquia de acesso.

## 7. Módulos, telas e fluxos esperados em nível alto

- **Exercício do quadro** (`/`): PL de dieta com arroz e milho, preços-sombra e
  tabela de cenários S1..SN.
- **Vaca leiteira (RuFaS)** (`/vaca/`): seleção de alimentos, preços e limites;
  simulação; indicadores, ração por intervalo, composição, exigências e leite
  diário.
- **Curva de lactação** (`/curva/`): curva de Wood por paridade com PEV, gestação
  e secagem.
- **Sensibilidade (RuFaS)** (`/sensibilidade/`): fatores, método (grade ou
  hipercubo latino), tabela de cenários, efeito de Spearman e margem por cenário.
- **Premissas e limites** (`/sobre/`): o que o modelo assume e não faz.
- **Módulo de adaptação do RuFaS** (servidor, sem interface): montagem do
  cenário, execução e leitura das saídas.
- **Módulo de economia e sensibilidade** (servidor): custo, receita, margem,
  cache, geração de cenários e efeitos.
- **Módulo de tarefas** (servidor): fila, progresso e erros das tarefas longas.

O FSD detalha o comportamento de cada tela, o dicionário de campos e as
mensagens — o layout visual já está coberto pelo `DESIGN.md`. Não é papel deste
documento.

## 8. Alertas para logs, auditoria e segurança

- **Sem auditoria hoje.** Se surgir a necessidade (ex.: rastrear quem simulou o
  quê), precisa ser desenhada do zero — a pasta `runs/` guarda os cenários, mas
  não a autoria.
- **Logs do servidor sem persistência.** A saída do servidor só é visível em
  tempo real. Já o `console.log` de cada simulação é persistido em
  `runs/<nome>/`, e é a fonte para diagnosticar falhas do RuFaS.
- **Servidor sem autenticação, validação de `Host` nem de `Origin`.** A
  proteção é só escutar em `127.0.0.1`. Uma página aberta no navegador do mesmo
  computador pode enviar requisições simples ao servidor (por exemplo, disparar
  simulações, que consomem ≈ 1,2 GB de RAM cada) e, em cenários de *DNS
  rebinding*, tentar ler respostas. Os dados são de baixa sensibilidade, mas o
  consumo de recursos não. Qualquer rota nova herda essa ausência de defesa. Se o
  servidor for exposto à rede (`--host`), é preciso antes acrescentar autenticação
  e limite de requisições, o que **não** existe hoje.
- **Sem limite de tamanho do corpo nem validação de esquema** nas requisições: o
  servidor converte tipos e deixa exceções virarem erro 500 com a mensagem.
- **Cache sem versão do simulador.** A chave do cache (`runs/_cache/`) considera os
  parâmetros do cenário, mas **não** a versão do RuFaS nem o conteúdo das tabelas
  de entrada. Trocar a versão do RuFaS ou editar `NRC_comp.csv`/`example_*` sem
  apagar `runs/_cache/` devolveria resultados antigos.
- **Crescimento da pasta `runs/`.** Nenhum cenário nem cache é apagado
  automaticamente.
- **Perda de estado ao reiniciar.** As tarefas ficam na memória do servidor; os
  resultados da tela ficam na memória da página. Reiniciar o servidor ou
  recarregar a página descarta o que não estiver no cache.
- **Resultados dependem de preços ilustrativos.** Qualquer uso fora da
  demonstração exige preços reais e validação contra uma referência
  profissional (PRD, M6, M7 e RNF-10).
- **Dados do usuário no navegador.** `localStorage` guarda a seleção de alimentos,
  preços e parâmetros em texto simples; não há dado pessoal, mas ele persiste até
  o usuário limpar os dados do site.

## 9. Itens que não devem ser inventados

- Login/senha, perfis ou hierarquia de permissões — não existem e não são
  requisitos.
- Banco de dados relacional, ORM ou qualquer modelo de dados persistente além
  de arquivos e `localStorage`.
- Modificações no código do RuFaS (`vendor/RuFaS`).
- Um modelo próprio de resposta do leite à dieta, ou otimização por fase da
  lactação — dependem de decisão do professor (PRD §15, Q2 e Q3); hoje o leite e
  a ração vêm do RuFaS.
- Suporte ao padrão NASEM 2021 e obtenção automática de preços do CEPEA —
  pendentes de decisão (Q5 e Q6), não existem.
- Suporte a vários usuários ou várias fazendas numa mesma instalação.
- Hospedagem em nuvem, serviço remoto ou exposição do servidor à rede.
- Exportação, relatórios em PDF, salvar/carregar cenários — pendentes (RF-20,
  RF-21), não existem.
- Balanço de nutrientes (oferta × exigência) da ração — pendente (RF-19); hoje
  só as exigências são exibidas.
- Repositório Git, remoto, CI/CD ou ambiente de homologação — **não existem**;
  não presumir que existem.
- Testes automatizados de integração e de interface — não existem; só os 10
  testes do back-end.
- Preços como cotações reais: os valores iniciais são ilustrativos.

## 10. Pendências não bloqueantes

- **Controle de versão:** o projeto não é um repositório Git. Não foi decidido
  se será versionado nem onde ficaria hospedado.
- **Ambiente de homologação e publicação:** não existe separação nem processo de
  entrega; não foi decidido como o sistema será entregue ao professor
  (relacionado à questão Q7 do PRD, prazo e formato de apresentação).
- **Validação científica:** não foi definida a referência profissional para
  comparar a ração (PRD, Q4, M6).
- **Preços reais:** não foi confirmado se haverá cotações do CEPEA e em que
  moeda e unidade (PRD, Q5, M7, RF-22).
- **Padrão NASEM 2021:** não foi decidido se é requisito de entrega (PRD, Q6).
- **Interpretação do gráfico do quadro:** PEV como *período de espera voluntário* e
  270 dias como gestação a partir do PEV seguem como interpretação do autor,
  com parâmetros editáveis (PRD, Q1).
- **Testes automatizados** de integração com o RuFaS e de interface: não foi
  decidido se entram antes da entrega.
- **Limpeza de `runs/` e invalidação do cache** por versão do simulador: não foi
  discutido.
- **Auditoria e autenticação:** não foram discutidas; relevantes só se o
  servidor sair da máquina local.
- **Outros sistemas operacionais e telas pequenas:** não verificados (só Windows;
  interface vista em 1.440 px e cerca de 540 px).
- **Versão em linha de comando com relatório:** combinada como fase seguinte à
  web, sem decisão técnica registrada ainda.
- **Autor, professor, instituição e prazo** em branco nos documentos.

Pendências que **bloqueiam partes do FSD** (PRD §15.1): Q2 (dieta por fase da
lactação) e Q3 (tratamento da resposta fraca do leite à dieta). Sem resposta,
vale a proposta registrada no PRD: manter a ração por grupo e o leite do RuFaS.

Nenhuma das demais pendências impede o funcionamento correto da versão atual.

## 11. Pronto para o FSD

**Sim, para documentar o que já existe; não, para especificar o que ainda
depende de decisão.** As decisões técnicas essenciais para descrever o
funcionamento atual e as fronteiras técnicas do sistema estão registradas. Para
a parte já construída, o FSD (`FSD.md`) tem o papel de documentar formalmente o
comportamento de cada tela e rota, usando este documento e o `DOMINIO.md` como
fontes primárias.

Os requisitos pendentes (RF-13, RF-19 a RF-24) e a dieta por fase da lactação
só podem ser especificados no FSD depois de resolvidas as questões Q2 e Q3 (e
Q5 e Q6 para preços e NASEM). Até lá, o FSD deve descrevê-los como pendentes,
sem inventar o comportamento.

# Dieta Ótima com RuFaS

Sistema web local que integra o simulador **RuFaS** (modelo de fazenda leiteira) a um otimizador de dieta de custo
mínimo, com análise de sensibilidade e a curva de lactação. Nasceu de um exercício de Pesquisa Operacional:
dieta de arroz e milho (carboidratos e proteína) que se generaliza para uma vaca leiteira real, com as exigências
da **NRC (2001)**.

```
 Cenários (S1..SN)  ──►  RuFaS (simulador)  ──►  otimizador de ração  ──►  margem sobre o custo de alimentação
 preços, limites           leite, exigências        custo mínimo (NRC)       Res = receita do leite − custo da dieta
```

## Como usar

1. Primeira vez: `powershell -ExecutionPolicy Bypass -File scripts\setup.ps1` (cria o venv, instala as dependências
   e clona o RuFaS v1.0.6 em `vendor/RuFaS`).
2. Dia a dia: dê dois cliques em `iniciar.bat`. O navegador abre em `http://127.0.0.1:8000`.

| Tela | O que faz |
|---|---|
| 1 · Exercício do quadro | PL da dieta (arroz × milho). Editável, com preços-sombra e tabela de cenários `S1..SN` (colunas dos fatores + `Res`). Resposta instantânea. |
| 2 · Vaca leiteira (RuFaS) | Escolha de alimentos NRC (130), preços e limites. Roda o RuFaS (~30 s por ano simulado) e mostra margem, ração, exigências e leite. |
| 3 · Curva de lactação | Curva de Wood por paridade (parâmetros calibrados pelo RuFaS), com PEV, gestação e secagem ajustáveis. |
| 4 · Sensibilidade (RuFaS) | Varia preços de alimentos e do leite (grade ou hipercubo latino), roda o RuFaS e monta a tabela de cenários e o efeito (Spearman) de cada fator. |
| 5 · Premissas e limites | O que o modelo assume, o que ele não faz e como ler os resultados. |

## Como funciona por dentro

- `backend/dietopt/diet_lp.py`: PL da dieta com HiGHS (SciPy), reproduz o quadro: **US$ 15,35/dia** (4,473 kg de arroz e
  3,873 kg de milho).
- `backend/dietopt/rufas_adapter.py`: monta cada cenário em `runs/<id>/` (cópias editadas das entradas do RuFaS),
  roda `vendor/RuFaS/main.py` em subprocesso e lê as saídas filtradas.
- `backend/dietopt/scenarios.py`: economia (preço do leite, custo da dieta, margem) e cache de simulações em
  `runs/_cache`. Mudar só o preço do leite não roda o RuFaS de novo.
- `backend/dietopt/sensitivity.py`: amostragem dos cenários e correlação de Spearman.
- `backend/dietopt/server.py`: API JSON com a biblioteca padrão do Python; também serve a interface.
- `web/`: fontes da interface (Next.js, React, Tailwind e shadcn/ui, adaptados do template AdminCN, MIT). Para
  alterar a interface: `powershell -ExecutionPolicy Bypass -File scriptsuild-web.ps1` (exige Node 20.9+; compila
  fora do OneDrive e publica em `frontend/`). Quem só usa o sistema não precisa de Node.
- `frontend/`: interface já compilada (site estático, funciona sem internet). `frontend_legacy/`: primeira versão,
  em HTML puro.

O RuFaS formula a ração das vacas em lactação com o próprio otimizador (SLSQP) usando o preço e os limites de cada
alimento que o sistema define. Quando a ração não atende às exigências, o RuFaS **reduz o leite** (0,25 kg por
tentativa, até o limite configurado); é assim que a dieta afeta o leite no modelo.

## Premissas e limitações (leia antes de apresentar)

- **Preços são ilustrativos** (US$/kg de matéria seca), não cotações. Substitua pelos seus, por exemplo do CEPEA.
- **No RuFaS v1.0.6 o leite não responde à qualidade da dieta**, só cai quando a ração não consegue atender às
  exigências. Por isso a margem varia sobretudo com o custo da dieta. O trade-off leite × custo aparece quando o
  conjunto de alimentos ou os limites ficam restritivos (veja "Leite perdido" na interface).
- **Limites de inclusão** são em kg de matéria seca por vaca por dia (unidade do `limit` do RuFaS). Minerais,
  gorduras e farinhas proteicas animais têm teto padrão; sem ele, o otimizador usa calcário como "enchimento".
- **NRC 2001 só traz farelo de arroz** (não arroz em grão). O "arroz" do exercício vira farelo de arroz (id 138).
- **PEV = período de espera voluntário** e a faixa de 270 d como gestação são a *leitura* do quadro do professor.
  Confirme com ele.
- O RuFaS pode abortar com certos preços (o otimizador não converge). A simulação então aparece como "falhou" na
  tabela, ou degrada com perda de leite se o limite de redução permitir.
- Simulação de 1 ano, rebanho de 100 vacas (exemplo `freestall`), sementes fixas. Cada simulação usa ~1,2 GB de RAM,
  por isso o sistema roda no máximo 2 em paralelo.
- O RuFaS é GPLv3: a distribuição deste sistema junto com ele deve respeitar a licença. Não modificamos o RuFaS.

## Documentação

- [`docs/PRD.md`](docs/PRD.md): Documento de Requisitos do Produto (escopo da versão web, requisitos com situação,
  riscos, plano de validação e rastreabilidade com o pedido do professor).
- [`docs/DOMINIO.md`](docs/DOMINIO.md): Domínio e Regras de Negócio (componentes, entidades, regras implementadas e
  onde cada uma vive no código).
- [`docs/FSD.md`](docs/FSD.md): Especificação funcional (telas, API, fluxos, cálculos, mensagens, critérios de
  validação e desvios conhecidos).
- [`docs/DECISOES_TECNICAS.md`](docs/DECISOES_TECNICAS.md): Decisões técnicas já tomadas (stack, ambientes,
  integração com o RuFaS, segurança), alertas e pendências antes do FSD.
- [`docs/DESIGN.md`](docs/DESIGN.md): Documento de Design (origem e adaptação do template, arquitetura da interface,
  tokens de design, especificação das telas, acessibilidade e decisões).

## Testes

```
cd backend
..\.venv\Scripts\python -m pytest tests
```

## Próximos passos

Versão em linha de comando com relatório (planejada depois da versão web).

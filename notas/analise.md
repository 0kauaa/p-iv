# Análise Metodológica e de Resultados

> Documento de consolidação: reúne os resultados numéricos e gráficos dos dois cenários,
> compara com a proposta do projeto e registra a conclusão geral.
> Base: backtest walk-forward 2021-04-16 a 2026-04-03 (260 semanas OOS, warm-up 2020–2021),
> `ρ` dinâmico sem piso (1.13), cenário duplo de variância (1.14), métricas por regime (1.15),
> higiene Sortino + fallback variância-ciente (1.16).

---

## 1. Tese do projeto

O artigo Dedu & Șerban (2026) é a **base fundacional** (arcabouço MaxEnt unificado). A réplica
limita-se aos fundamentos; o projeto é uma **extensão dinâmica com backtest**: janela móvel de
52 semanas, rebalanceamento semanal com custos de 10 bps e avaliação fora da amostra.

- **Núcleo réplica** (coberto pela prova MaxEnt do artigo): Shannon, Tsallis ($q=2$), WSE ($u=(0.35,0.30,0.20,0.15)$).
- **Extensão** (inovação, fora da prova unificada): Rényi ($\alpha=3.0$), KL (prior $p=(0.50,0.25,0.15,0.10)$).
- **Benchmark**: $1/N$.
- A entropia é tratada como o artigo a define — **regularizador estrutural da diversificação,
  não proxy de risco** — e a Frente B é motivação empírica (testar se se sustenta na prática, por regime).

---

## 2. Metodologia — análise completa

### 2.1. Dados

BTC, ETH, SOL, BNB via yfinance, resample semanal `W-FRI` (último preço válido), forward fill +
dropna sincronizado, retornos **simples** em toda a cadeia (estimação de $\mu$/$\Sigma$, execução e
acumulação). Série alinhada desde 04/2020 (SOL sem dados antes); 312 semanas, 260 de teste.

### 2.2. Problema de otimização (operado dinamicamente por janela)

$$
\sum_i w_i = 1, \quad w_i \geq 0, \quad w^T\mu \geq \rho, \quad w^T\Sigma w \leq \sigma^2_{max}
$$

- **$\rho$ dinâmico** ($f_{meta}=0.5$): $\rho = \mu^T w_{1/N} + 0.5\,(\max\mu - \mu^T w_{1/N})$.
  Combinação convexa entre o retorno do benchmark e o melhor ativo da janela: sempre factível
  quanto a retorno ($\leq \max\mu$), vinculante com dispersão, acompanha o regime — **inclusive
  negativo em bears** (média 2,64%/sem; min −1,70%; max 9,79%; 40 janelas com $\rho<0$; **0
  infactíveis por retorno**). O piso $rf=0$ anterior gerava 30 janelas infactíveis e foi removido (1.13).
- **Teto duplo de variância** ($\sigma^2_{max} = f_{var} \cdot var_{1/N}$): **agressivo** $f_{var}=2.0$
  (Frente A) e **conservador** $f_{var}=1.0$ (Frente B), mesmo $\rho$ — a diferença vem só do teto.
  Calibração: $0.5\to100\%$ fallback; $0.8\to64\%$; **$1.0\to55\%$** (var ativa em 18%);
  $1.5\to37\%$; **$2.0\to8\%$** (var ativa em 7%); $3.0\to0\%$ (teto inútil).
- **Solver**: SLSQP unificado (`restricoes_padrao`), warm-start concentrado quando $\rho$ ativo,
  fallback em dois níveis: (1) base MaxEnt variância-ciente, (2) uniforme se o conjunto é vazio
  (nível-2 = 0 nos dois cenários — o fallback nunca viola o teto sem registro).

### 2.3. Métricas

Retorno acumulado/anualizado, vol anual, Sharpe, **Sortino por downside deviation vs 0**
($\sqrt{mean(\min(0,r)^2)}\cdot\sqrt{52}$; corrigido em 1.16), Max Drawdown global + **intra-bloco
por regime** (expansão 38 sem / stress 52 / recuperação 117 / cauda 53).

---

## 3. Resultados numéricos

### 3.1. Global — agressivo ($f_{var}=2.0$), riqueza final (base 1)

| Modelo | Riqueza | Acum. | Anual. | Vol | Sharpe | Sortino | MDD |
|---|---|---|---|---|---|---|---|
| 1/N | 2,454 | +145% | 19,7% | 63,6% | 0,31 | 0,47 | −79% |
| shannon | 2,633 | +163% | 21,4% | 69,2% | 0,31 | 0,47 | −83% |
| tsallis | 2,802 | +180% | 22,9% | 68,3% | 0,34 | 0,51 | −82% |
| renyi | 2,904 | +190% | 23,8% | 67,8% | 0,35 | 0,53 | −81% |
| wse | 2,752 | +175% | 22,4% | 70,1% | 0,32 | 0,50 | −84% |
| kl | 2,974 | +197% | 24,4% | 70,1% | 0,35 | 0,54 | −84% |

Leitura: todos os entrópicos batem o 1/N no acumulado — **todos com maior vol e pior MDD**.

### 3.2. Global — conservador ($f_{var}=1.0$), riqueza final

| Modelo | Riqueza | Acum. | Sharpe | Sortino | MDD |
|---|---|---|---|---|---|
| 1/N | 2,454 | +145% | 0,31 | 0,47 | −79% |
| shannon | 1,936 | +94% | 0,23 | 0,34 | −76% |
| tsallis | 2,020 | +102% | 0,25 | 0,37 | −75% |
| renyi | 2,058 | +106% | 0,25 | 0,38 | −75% |
| wse | 1,938 | +94% | 0,23 | 0,34 | −76% |
| kl | 1,529 | +53% | 0,15 | 0,22 | −75% |

Leitura: inversão completa do ranking — **todos perdem do 1/N no acumulado**, com vol menor e
MDD 4–5 pp melhor. KL vai de primeiro a último (prior BTC-heavy cobra o preço sob teto rígido).

### 3.3. Por regime — agressivo (acumulado / Sharpe / MDD intra-bloco)

| Regime | 1/N | shannon | tsallis | renyi | wse | kl |
|---|---|---|---|---|---|---|
| Expansão (38s) | +95% / 1,78 / −48% | +168% / 2,91 / −45% | +160% / 2,77 / −47% | +161% / 2,79 / −48% | +185% / 3,18 / −44% | **+218% / 3,74 / −43%** |
| Stress (52s) | −72,6% / −1,06 / −69,9% | −77,1% / −1,08 / −73,7% | −75,7% / −1,08 / −72,1% | −75,1% / −1,08 / −71,5% | −77,9% / −1,07 / −74,4% | −77,8% / −1,07 / −74,2% |
| Recuperação (117s) | +398% / 1,88 / −34% | +490% / 1,97 / −39% | +488% / 2,00 / −36% | +484% / 2,00 / −36% | +488% / 1,95 / −40% | +468% / 1,97 / −39% |
| Cauda (53s) | −7,8% / −0,14 / −56% | −27,3% / −0,52 / −56,6% | −24,6% / −0,47 / −56,2% | −23,2% / −0,44 / −56,2% | −25,7% / −0,49 / −56,2% | −26,1% / −0,49 / −57,5% |

### 3.4. Por regime — conservador

| Regime | 1/N | shannon | tsallis | renyi | wse | kl |
|---|---|---|---|---|---|---|
| Expansão | +95% | +95% (= base) | +95% (= base) | +95% (= base) | +91% | +46% |
| Stress | −72,6% / −69,9% | −68,1% / −65,0% | −67,2% / −64,0% | −66,7% / −63,4% | −68,0% / −65,0% | **−65,6% / −63,6%** |
| Recuperação | +398% | +299% | +297% | +295% | +300% | +283% |
| Cauda | −7,8% | −22,0% | −20,5% | −19,9% | −20,6% | −20,3% |

### 3.5. O mecanismo (buy-hold por ativo × pesos médios agressivos)

| Regime | BTC | ETH | **SOL** | BNB | Peso SOL (agr.) |
|---|---|---|---|---|---|
| Expansão | −28% | +65% | **+532%** | −8% | 46–60% |
| Stress | −64% | −68% | **−94%** | −52% | 37–42% |
| Recuperação | +411% | +57% | **+1149%** | +148% | 29–34% |
| Cauda | −20% | +11% | **−35%** | +1% | 16–17% |

SOL é o ativo de maior beta nos quatro regimes. O $\rho$ meio-caminho aponta para o trailing
max-μ (quase sempre SOL) → overweight sistemático de SOL → **amplificação simétrica**:
ganha mais nos bulls, apanha mais nos bears. O teto modula a amplitude (conservador corta SOL
para 17–19% no stress e amortece). Na cauda, mesmo com pesos médios quase neutros
(27/27/17/29), perde-se por *timing* — o $\rho$ por média trailing induz comportamento
momentum-like com whipsaw em reversões (custos descartados como causa: 0,004–0,017%/sem).

### 3.6. Estatísticas de honestidade

Fallbacks: agressivo 239 ok + 21 nível-1 + 0 nível-2 (8%); conservador ~116 ok + ~144 nível-1 +
0 nível-2 (55%); 0 infactíveis por retorno. Turnover médio ~0,13/semana. Correlação mínima entre
entrópicos **0,986**. Diffs vs 1/N com **p 0,55–0,66** (t pareado) — **ranking global sem
significância estatística**. Sharpe/Sortino com $rf=0$.

---

## 4. Comparação com a proposta

- **§2 (extensão dinâmica)**: ✅ cumprido — tese sem inversão conceitual.
- **§3 (núcleo + extensão)**: ✅ nos notas; ⚠️ Rényi/KL sem marcação de papel no código.
- **§4 (dados)**: ✅ sincronizado (warm-up + 260 sem OOS).
- **§5 Frente A**: ✅ cumprida com resultado positivo — sob teto permissivo, captura superior em expansão e recuperação.
- **§5 Frente B**: ⚠️ cumprida pela metade — só se sustenta sob teto restritivo e ao custo da recuperação; no agressivo, MDD pior em todos os modelos; a "proteção" do conservador é modesta (−65% vs −73% ainda é devastação).
- **§6 (resultados)**: ✅ curvas por cenário + tabelas por regime existem; falta a discussão escrita.

---

## 5. Pontos fortes, fracos e limitações

**Fortes**: diário auditor-corretivo (1.11–1.16) raro em PIV; pipeline modular com SLSQP unificado,
warm-start e fallback documentado; correção log→simples; duplo cenário + regimes dão material
empírico real para "risco≠ganho"; números determinísticos e reproduzíveis no `.venv`.

**Fracos / limitações a declarar no artigo**: ranking global sem significância (p>0,5; corr 0,986);
conservador = 55% carteira-base (o teto × meta são incompatíveis em mais da metade das janelas);
cauda 2025–26 desfavorável nos dois cenários; Rényi $\alpha=3.0$ e prior do KL arbitrários e sem
âncora teórica; viés de sobrevivência (4 sobreviventes); $\mu$ por média de 52 semanas ruidosa com
momentum implícito; $J=52$, $f_{meta}=0.5$, custos 10 bps sem análise de sensibilidade;
Sharpe/Sortino com $rf=0$; sem versionamento de dados/dependências (pós-redação).

---

## 6. Conclusão geral

O incômodo da Frente B é **natureza do problema, não artefato**: acoplada a uma meta de retorno,
a regularização entrópica concentra no ativo de maior beta e amplifica os dois lados; só o teto
restritivo quebra a simetria, cobrando o preço na recuperação. O projeto está **apto à redação
com a tese que os números sustentam** — "o teto permissivo amplifica bull e bear; o restritivo
amortece o stress e sacrifica a recuperação" — e **não** com qualquer variante de "entropia X é a
melhor / protege capital" (p-valores e cauda 2025–26 vetam). Redação deve conter: parágrafo de
mecanismo (tilt SOL via $\rho$, §3.5), momentum implícito como limitação declarada, Rényi/KL como
extensão exploratória, e as taxas de fallback/correlação/significância como honestidade
metodológica — é isso que blinda contra revisor.

# Modelos de Otimização a serem Trabalhados no Projeto

> Tese: o artigo Dedu & Șerban é a base fundacional (MaxEnt unificado). A réplica limita-se aos
> fundamentos; o projeto é uma **extensão dinâmica com backtest walk-forward**. Por isso os modelos
> abaixo se dividem em **núcleo réplica** (cobertos pela prova do artigo) e **extensão**
> (inovação do projeto, fora da prova unificada).

Todas as restrições comuns traduzem o problema fundamental de alocação de portfólio sob as premissas do projeto.
No artigo elas são estáticas por regime; aqui são **operadas dinamicamente** a cada janela do walk-forward
($\rho$ dinâmico, $\sigma^2_{max}$ relativo ao $1/N$ da janela):

* **Orçamento:** A soma dos pesos investidos não pode exceder 1 (100% do capital).
  $$
  \sum_i^N w_i = 1
  $$
* **Positividade:** Não são permitidas posições vendidas ( *short selling* ); os pesos devem ser não-negativos.
  $$
  w_i \geq 0
  $$
* **Retorno Mínimo:** A alocação deve atingir ou superar um patamar de retorno esperado pré-estabelecido.
  $$
  w^T\mu \geq R_{min}
  $$
* **Teto de Variância (do artigo, operado em dois cenários separados):** a variância da carteira não pode
  exceder um múltiplo da variância do $1/N$ na janela — permissivo na Frente A, restritivo na Frente B.
  Risco e ganho são eixos separados: minimizar um não é maximizar o outro.
  $$
  w^T\Sigma w \leq \sigma^2_{max}
  $$

### 1. 1/N — Benchmark Base

* **Descrição:** Alocação ingênua com pesos iguais em todos os ativos. Serve como o piso informacional e de custo-benefício do mercado.

  $$
  w_i = \frac{1}{N}
  $$

  *(Obs.: Não envolve otimização matemática direta).*

### 2. Shannon Entropy (Núcleo réplica)

* **Descrição:** Maximiza a incerteza informacional clássica, forçando uma distribuição de pesos mais homogênea e livre de pressupostos paramétricos rígidos.

  $$
  \max_w \left( -\sum_i w_i \ln(w_i) \right)
  $$

  **Sujeito a:**

  $$
  w^T\mu \geq R_{min}, \quad w^T\Sigma w \leq \sigma^2_{max}, \quad \sum_i w_i = 1, \quad w_i \geq 0
  $$

### 3. Tsallis Entropy (Núcleo réplica)

* **Descrição:** Generalização não-extensiva controlada pelo parâmetro **$q$**, altamente sensível e adaptada para lidar com distribuições de caudas pesadas ( *fat-tails* ), típicas de criptoativos.

  $$
  \max_w \left( \frac{-\sum_i w_i^q}{q - 1} \right)
  $$

  **Sujeito a:**

  $$
  w^T\mu \geq R_{min}, \quad w^T\Sigma w \leq \sigma^2_{max}, \quad \sum_i w_i = 1, \quad w_i \geq 0
  $$

### 4. Weighted Shannon Entropy / WSE (Núcleo réplica)

* **Descrição:** Generaliza Shannon com pesos informacionais **$u_i > 0$** por ativo (liquidez/market cap).
  Default do projeto $u = (0.35, 0.30, 0.20, 0.15)$ (BTC, ETH, SOL, BNB), conforme o artigo.

  $$
  \max_w \left( -\sum_i u_i w_i \ln(w_i) \right)
  $$

  **Sujeito a:**

  $$
  w^T\mu \geq R_{min}, \quad w^T\Sigma w \leq \sigma^2_{max}, \quad \sum_i w_i = 1, \quad w_i \geq 0
  $$

### 5. Rényi Entropy (Extensão — fora do MaxEnt unificado)

* **Descrição:** Generalização informacional parametrizada por **$\alpha$** (default $\alpha=3.0$ para
  não colapsar no Tsallis $q=2$). Incluída como extensão do projeto para testar sensibilidade alternativa
  à concentração; não possui a prova de existência/unicidade do arcabouço unificado.

  $$
  \max_w \left( \frac{1}{1 - \alpha} \ln \left( \sum_i w_i^\alpha \right) \right)
  $$

  **Sujeito a:**

  $$
  w^T\mu \geq R_{min}, \quad w^T\Sigma w \leq \sigma^2_{max}, \quad \sum_i w_i = 1, \quad w_i \geq 0
  $$

### 6. Kullback-Leibler Divergence / Entropia Relativa (Extensão — controle estrutural)

* **Descrição:** Minimiza a distância informacional entre os pesos resultantes da otimização e uma distribuição de referência prévia (**$p_i$**, default $p = (0.50, 0.25, 0.15, 0.10)$ com dominância BTC),
  impedindo alocações extremas ou "alucinações" do otimizador. Não é maximização de entropia:
  entra como extensão para testar âncora estrutural no walk-forward.

  $$
  \min_w \left( \sum_i w_i \ln\left(\frac{w_i}{p_i}\right) \right)
  $$

  **Sujeito a:**

  $$
  w^T\mu \geq R_{min}, \quad w^T\Sigma w \leq \sigma^2_{max}, \quad \sum_i w_i = 1, \quad w_i \geq 0
  $$

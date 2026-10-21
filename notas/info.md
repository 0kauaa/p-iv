# Otimização de Carteiras: Entropia vs. 1/N em Criptomoedas

## 1. Teoria da Informação e Entropia em Finanças

* **Conceito Chave:** A Teoria da Informação, desenvolvida por Claude Shannon, quantifica a incerteza e a surpresa associada aos eventos. Em finanças, a medida central é a entropia, que reflete o grau de desordem ou aleatoriedade de uma distribuição de probabilidades dos retornos dos ativos.
* **Valor da Informação:** A informação está ligada à surpresa; dados que quebram expectativas carregam alto valor informativo.
* **Aplicação em Portfólios:** A entropia busca maximizar a diversificação, evitando que a carteira fique excessivamente concentrada em poucos ativos ou cenários incertos.

## 2. O Framework de Dedu e Șerban (2026) e a Geometria

* **Crítica aos Modelos Tradicionais:** Abordagens clássicas como o modelo de Markowitz falham em capturar a essência de mercados de alta volatilidade e dados ruidosos, como o de criptomoedas.
* **Princípio da Máxima Entropia:** Dedu e Șerban propõem um framework baseado em entropia para otimizar carteiras de cripto, onde a entropia atua como um regularizador estrutural que governa a geometria da diversificação.
* **Objetivo Geométrico:** O framework usa essa geometria para manter a carteira distante de distribuições arriscadas e concentradas, direcionando-a para regiões de maior equilíbrio.

## 3. A Superioridade do Modelo 1/N e a Limitação dos Modelos Baseados em Dados

* **Modelos de Aprendizado de Padrões:** Modelos entrópicos e outros baseados em aprendizado tentam capturar como os dados funcionam para alocar recursos. No entanto, pressupõem que as relações passadas continuarão válidas no futuro.
* **Instabilidade do Mercado de Cripto:** Em mercados de criptomoedas altamente voláteis e instáveis, essas premissas frequentemente falham, gerando reações inesperadas e alocações inadequadas.
* **A Resiliência do 1/N:** Em cenários de aversão a risco onde o objetivo é minimizar perdas, a metodologia 1/N (distribuir o capital igualmente entre os ativos) frequentemente supera abordagens complexas. O 1/N não depende de previsões de parâmetros ou suposições sobre dados passados, tornando-se mais resiliente a choques e quedas abruptas.

## 4. Modelos de Entropia Utilizados

* **Entropia de Shannon:** Mede a incerteza básica do sistema de forma uniforme.
* **Entropia Ponderada de Shannon:** Atribui pesos específicos a eventos e cenários para refinar a alocação.
* **Entropia de Tsallis:** Adaptada para lidar com sistemas complexos, caóticos e de alta volatilidade extrema.
* **Divergência KL (Kullback-Leibler):** Atua como um regularizador que mede a diferença entre distribuições de probabilidade, evitando desvios perigosos da carteira.

## 5. Referências Bibliográficas

1. **Dedu, S., & Șerban, F. (2026).** *Entropy-Based Portfolio Optimization in Cryptocurrency Markets: A Unified Maximum Entropy Framework*. (Framework de otimização de portfólio baseado em entropia unificada).
1. **DeMiguel, V., Garlappi, L., & Uppal, R. (2009).** *Optimal Versus Naive Diversification: How Inefficient is the 1/N Portfolio Strategy?* Review of Financial Studies, 22(5), 1915-1953. (Trabalho seminal que discute a ineficiência de estratégias de otimização complexas frente à diversificação ingênua 1/N).

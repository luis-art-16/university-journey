# 📡 Teoria dos Sistemas para as Telecomunicações

**Ano:** 2º Ano | **Semestre:** 2º Semestre  
**Área:** Análise de Sistemas Dinâmicos Lineares (LTI), Resposta no Tempo e na Frequência

## 📌 Sobre a Cadeira
Unidade curricular focada no estudo, modelação e análise de sistemas dinâmicos contínuos. Abrange a caraterização no domínio do tempo (equações diferenciais e resposta ao degrau) e no domínio da frequência (Transformada de Laplace, Funções de Transferência $G(s)$ e Diagramas de Bode).

## 🎯 Principais Tópicos Abordados
* **Sistemas Dinâmicos de 1ª Ordem:**
  * Equação diferencial $T y'(t) + y(t) = K x(t)$ e Função de Transferência $G(s) = \frac{K}{Ts+1}$.
  * Parâmetros fundamentais: Constante de tempo ($T$) e Ganho em regime permanente ($K$).
  * Resposta livre (condições iniciais) e resposta forçada ao degrau unitário.
* **Sistemas Dinâmicos de 2ª Ordem:**
  * Modelo padrão: $G(s) = \frac{K \omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$.
  * Parâmetros caraterísticos: Frequência natural de oscilação ($\omega_n$) e Coeficiente de amortecimento ($\zeta$).
  * Classificação dos regimes consoante os pólos no plano $s$:
    * **Subamortecido ($0 < \zeta < 1$):** Pólos complexos conjugados, comportamento oscilatório.
    * **Criticamente Amortecido ($\zeta = 1$):** Pólos reais iguais, resposta rápida sem oscilação.
    * **Sobre-amortecido ($\zeta > 1$):** Pólos reais distintos, resposta lenta sem oscilação.
    * **Não-amortecido ($\zeta = 0$):** Oscilações sustentadas à frequência $\omega_n$.
  * Especificações no tempo para sistemas subamortecidos: Tempo de pico ($T_p$), Sobre-elongação percentual ($PO\%$), Tempo de subida ($T_r$) e Tempo de assentamento ($T_s$).
* **Casos de Estudo Físicos & Circuitos:**
  * Circuitos RC com amplificação operacional e Circuitos RLC Série/Paralelo.
* **Resposta em Frequência e Diagramas de Bode:**
  * Análise em regime sinusoidal permanente $s = j\omega$.
  * Traçagem de Diagramas de Bode de Amplitude ($20\log_{10}|G(j\omega)|$ em dB) e Fase ($\angle G(j\omega)$ em graus).
  * Frequência de corte e filtragem (Passa-Baixo / Passa-Alto).

## 📂 Organização da Pasta
* 📖 **`Teoricas/`:** Apresentações e diapositivos cobrindo o estudo formal de sistemas de 1ª e 2ª ordem, circuitos RLC e análise temporal/frequencial.
* 📝 **`Fichas_e_Exercicios/`:** Fichas de trabalho laboratoriais e de exercícios resolvidos (fichas de resposta em frequência, diagramas de Bode e simulação de circuitos RC com ganho).
* 📑 **`Avaliacoes/`:** Enunciados e resoluções de testes de avaliação teórica e prática.

## 🛠️ Ferramentas Utilizadas
* **Simulação Computacional:** MATLAB / Simulink / Scilab (ScicosLab).
* **Análise Matemática:** Transformadas de Laplace e cálculo no plano $s$.

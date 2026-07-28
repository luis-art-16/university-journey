# 📡 Comunicações Digitais

**Grau:** Mestrado | **Ano:** 1º Ano | **Semestre:** 1º Semestre  
**Bibliografia de Referência:** *Communication Systems* – Simon Haykin

## 📌 Sobre a Cadeira
Unidade curricular avançada de mestrado dedicada à análise, projeto e otimização de sistemas de comunicação digital modernos. Aprofunda os blocos fundamentais de um sistema de transmissão digital, focando-se na representação de sinais no espaço vetorial, técnicas avançadas de codificação de canal, modulações multiportadora e espalhamento espetral.

## 🎯 Principais Tópicos Abordados
* **Modulação de Pulso e Processamento em Banda Base:**
  * Modulação por Amplitude de Pulso (PAM), Duração (PDM) e Posição (PPM).
  * Modulação por Código de Pulsos (PCM) e processos de quantização (uniforme e não-uniforme).
  * Critério de Nyquist para ausência de Interferência Inter-Símbolos (ISI) e modelação de filtros adaptados (*Matched Filters*).
* **Teoria da Codificação de Canal (Correção de Erros - FEC):**
  * **Códigos de Bloco Linear:** Matriz geradora ($G$), matriz de controlo de paridade ($H$) e deteção/correção de erros por sindroma.
  * **Códigos Convolucionais:** Representação por estados, diagramas em árvore/treliça e codificação sistemática/não-sistemática.
  * **Algoritmo de Viterbi:** Descodificação de máxima vergonhabilidade para códigos convolucionais e cálculo da distância livre ($d_f$).
* **Modulações Digitais Avançadas & Portadoras:**
  * Modulação de Frequência Mínima Deslocada (**MSK** - *Minimum Shift Keying*).
  * Desempenho de probabilidade de erro de bit ($BER$) em canais com Ruído Aditivo Branco Gaussiano (AWGN): $BER = Q\left(\sqrt{\frac{2E_b}{N_0}}\right)$.
* **Modulação Multiportadora e Espalhamento Espetral:**
  * **OFDM** (*Orthogonal Frequency Division Multiplexing*): Implementação eficiente baseada em IDFT / IFFT e inserção de prefixo cíclico.
  * **Espalhamento Espetral (*Spread Spectrum*):** Sequências Pseudo-Ruído (PN / *Pseudo-Noise*), FHSS e DSSS.

## 📂 Organização da Pasta
* 📖 **`Apontamentos_e_Aulas/`:** Notas manuscritas detalhadas e resumos estruturados de preparação para os três momentos de avaliação (Testes 1, 2 e 3).
* 📚 **`Bibliografia_e_Manuais/`:** O livro de referência (*Communication Systems* - Simon Haykin) e respetivo manual de soluções completo.
* 💻 **`Codigo_e_Simulacoes/`:** Scripts de laboratório e simulações numéricas (MATLAB/Python) de modulações e desmodulações digitais.

## 🛠️ Ferramentas e Conceitos
* **Análise Teórica:** Espaços de sinais, ortogonalidade e otimização de recetores ótimos.
* **Simulação Computacional:** MATLAB (Signal Processing e Communications Toolboxes).

# 📡 Processamento Digital de Sinal

**Ano:** 3º Ano | **Semestre:** 1º Semestre  
**Área:** Aquisição, Análise e Filtragem de Sinais Digitais em Sistemas Embebidos

## 📌 Sobre a Cadeira
Unidade curricular orientada à aquisição, análise, processamento e filtragem de sinais. Foca-se na transição do domínio analógico para o digital e na implementação de algoritmos para mitigação de ruído e estimação de parâmetros, essenciais para sistemas de comunicação e automação robótica.

## 🎯 Principais Tópicos Abordados
* **Fundamentos de Sinais e Ruído:**
  * Caracterização de sinais em tempo discreto e contínuo.
  * Relação Sinal-Ruído (SNR) e tipos de ruído associados a componentes eletrónicos (Ruído Térmico/Johnson, Ruído *Shot* e ruído ambiente).
* **Filtros e Processamento Digital:**
  * Diferenças arquiteturais e matemáticas entre filtros convencionais (Passa-Baixo, FIR, IIR) e abordagens preditivas.
* **Filtro de Kalman:**
  * Algoritmo de filtragem preditiva para mitigação de ruído e incerteza na aquisição de dados.
  * Ciclo de funcionamento iterativo: Previsão (modelo preditivo) e Atualização (incorporação da nova leitura e adaptação contínua ao ruído).

## 📂 Organização da Pasta
* 📖 **`Teoricas/`:** Apresentações e resumos teóricos (Aulas 1 a 10).
* 📝 **`Fichas/`:** Guiões e resoluções práticos (6 Fichas de exercícios).
* 📑 **`Avaliacoes/`:** Enunciados e resoluções teóricas dos 2 Testes de avaliação.
* 🤖 **`Trabalho_AutoRobot/`:** Relatório final, apresentação e vídeos de demonstração de um robô de navegação autónoma baseado no Filtro de Kalman.

## 🏆 Projeto em Destaque: AutoRobot
* **Descrição:** Robô autónomo capaz de identificar e desviar-se de obstáculos em tempo real, movimentando-se com extrema precisão sem recorrer a paragens bruscas.
* **Desafio:** As leituras do sensor ultrassónico apresentavam perturbações significativas causadas por reflexões irregulares e ruído do ambiente, o que afetava a tomada de decisão do robô.
* **Solução e Processamento de Sinal:** Implementação de um **Filtro de Kalman** para estabilizar o sinal. A predição e atualização dos dados mitigou eficientemente as flutuações e garantiu estimativas de distância confiáveis, superando largamente a eficiência de um simples filtro passa-baixo.

## 🛠️ Tecnologias e Ferramentas
* **Hardware / Eletrónica:** Arduino Mega R3, Motores DC, Motor Driver L298N, Sensor Ultrassónico HC-SR04.
* **Algoritmia:** C/C++ (Implementação de filtros estocásticos / Filtro de Kalman).

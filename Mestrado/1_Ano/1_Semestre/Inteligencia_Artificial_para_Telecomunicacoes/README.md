# 🤖 Inteligência Artificial para as Telecomunicações

**Grau:** Mestrado | **Ano:** 1º Ano | **Semestre:** 1º Semestre  
**Linguagens e Ferramentas:** Python (VS Code), KNIME Analytics Platform, AutoML  
**Áreas:** Machine Learning, Data Mining, Otimização, Algoritmos de Procura e Engenharia de Features

## 📌 Sobre a Cadeira
Unidade curricular de mestrado focada na aplicação de técnicas de Inteligência Artificial e Aprendizagem Automática (Machine Learning) a problemas complexos do mundo real, com especial foco em telemetria, análise de dados de sensores (IoT) e otimização logística. 

## 🎯 Principais Tópicos Abordados
* **Machine Learning Clássico:**
  * Aprendizagem Supervisionada (Classificação e Regressão) e Não-Supervisionada (Clustering: K-Means, Hierárquico).
* **Data Science e Pré-processamento:**
  * Limpeza de dados, tratamento de *missing values*, normalização e **Feature Engineering**.
* **Modelos Avançados e Ensembles:**
  * Naïve Bayes, Random Forest, **XGBoost**.
  * Aplicação de **AutoML** para otimização de hiperparâmetros e *Cross-Validation*.
* **Algoritmos de Procura e Otimização:**
  * Resolução de problemas de roteamento e alocação de recursos em ambientes dinâmicos.

---

## 🏆 Projetos em Destaque

### 1. 🩺 Nurse Stress Prediction using Wearable Sensors (Trabalho Individual)
* **O Desafio:** Analisar um dataset massivo (~11.5 milhões de registos) contendo dados fisiológicos contínuos (Frequência Cardíaca - HR, Atividade Eletrodérmica - EDA, Temperatura e Movimento) recolhidos por sensores *wearables* em enfermeiros durante a pandemia COVID-19.
* **A Solução:** Desenvolvimento de um *workflow* completo de Machine Learning no **KNIME**. Implementação de engenharia de *features* (ex: compressão da magnitude de movimento) e treino de modelos supervisionados (XGBoost, Random Forest) para prever com alta precisão os níveis de stress. O uso de AutoML confirmou padrões determinísticos nos dados fisiológicos, atingindo valores de $R^2 > 0.98$ na previsão de sinais contínuos.

### 2. 🚛 Otimização de Veículos Autónomos em Centros de Distribuição (Trabalho de Grupo)
* **O Desafio:** Desenvolver um sistema baseado em algoritmos de procura (Inteligência Artificial Simbólica) para gerir uma frota de *LogiBots* (veículos autónomos).
* **A Solução:** Modelação e implementação em **Python** de algoritmos de otimização para minimizar tempos de entrega e evitar colisões, garantindo a gestão eficiente da bateria, capacidade de carga e restrições de tráfego nos corredores do armazém.

---

## 📂 Organização da Pasta
* 📖 **`Aulas_e_Praticas/`:** Slides teóricos de introdução ao ML, guiões de aprendizagem de Python e *workflows* práticos desenvolvidos em KNIME (ex: previsão de sobrevivência do Titanic com *Ensemble Models*).
* 👤 **`Trabalho_Individual_ML/`:** Relatório detalhado (`Relatório_PG61434.pdf`), apresentação em PowerPoint e documentação do projeto de previsão de stress hospitalar.
* 👥 **`Trabalho_Grupo_Otimizacao/`:** Enunciado, especificações e código-fonte (`.py`) do algoritmo de roteamento de veículos autónomos.

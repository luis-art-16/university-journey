# 📱 Redes Móveis

**Ano:** 3º Ano | **Semestre:** 2º Semestre  
**Área:** Comunicações Sem Fios, Redes Celulares, Técnicas de Espalhamento Espetral e CDMA

## 📌 Sobre a Cadeira
Unidade curricular dedicada ao estudo dos princípios teóricos, arquiteturas e protocolos de funcionamento dos sistemas de comunicação móvel e celular. Abrange a gestão do espectro radioelétrico, mobilidade, handovers, controlo de potência, técnicas de acesso múltiplo (FDMA, TDMA, CDMA, OFDMA) e evolução de arquiteturas desde as redes 2G (GSM) até aos sistemas modernos de banda larga.

## 🎯 Principais Tópicos Abordados
* **Fundamentos de Propagação e Canal Rádio:**
  * Espectro radioelétrico e características de propagação em ambiente móvel (atenuação, multipercurso e desvanecimento).
  * Conceito de rede celular, reutilização de frequência e cálculo de capacidade.
* **Sistemas Celulares 2G e 3G (GSM e UMTS):**
  * **GSM:** Arquitetura de rede (HLR, VLR, MSC, BSC, BTS), interfaces de rádio, modulação GMSK, salto de frequências (FHSS) e gestão de serviços (SMS, handovers).
  * **UMTS:** Introdução ao WCDMA, duplexação FDD/TDD e controlo de potência.
* **Técnicas de Acesso Múltiplo e Espalhamento Espetral (CDMA):**
  * Princípios do *Code Division Multiple Access* (CDMA).
  * Códigos ortogonais (Walsh-Hadamard) e sequências de pseudo-ruído (PN).
  * Sincronização temporal, mitigação de interferência multiutilizador e gestão de atrasos/offsets.
* **Evolução para Redes de Banda Larga (HSDPA / LTE):**
  * Otimizações de desempenho ao nível do Node-B (*Scheduling at the Node-B*).

## 📂 Organização da Pasta
* 📖 **`TPCs/`:** Conjunto de 11 trabalhos para casa e exercícios práticos de consolidação teórica.
* 📑 **`Avaliacoes/`:** Enunciados e resoluções de testes e exames de avaliação (ex: Teste de Redes Móveis).
* 🛠️ **`Trabalho_CDMA/`:** Relatório final e código-fonte da **Simulação CDMA** desenvolvida em grupo, cobrindo a modelação de blocos (transmissor, canal, recetor, medidor de BER e sincronização multi-utilizador).

## 🏆 Projeto em Destaque: Simulação CDMA
* **Descrição:** Implementação e simulação computacional de um sistema de comunicações móveis baseado em CDMA, permitindo avaliar o desempenho da transmissão digital face a ruído aditivo e desfasamentos temporais.
* **Módulos Desenvolvidos:**
  * **Transmissor e Canal:** Codificação, espalhamento por códigos ortogonais e injeção de ruído no canal de rádio.
  * **Recetor e Sincronização:** Algoritmos de sincronização temporal e recuperação de sinal para múltiplos utilizadores com *offsets* aleatórios.
  * **Análise de Desempenho:** Avaliação empírica da Taxa de Erro de Bits (BER) em função da Relação Sinal-Ruído (SNR) e da contenção de canal.
* **Autores:** Luís Baptista, Bernardo Salgado e Luís Marques.

## 🛠️ Tecnologias e Ferramentas
* **Simulação e Análise Numérica:** MATLAB / Python / Scripts de modelação matemática de sinais.
* **Bibliografia de Apoio:** * *Mobile Communications* – Jochen Schiller
  * *Wireless Communications: Principles and Practice* – Theodore S. Rappaport

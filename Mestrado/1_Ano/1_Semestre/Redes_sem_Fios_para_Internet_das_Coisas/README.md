# 📡 Redes sem Fios para Internet das Coisas (RSIoT)

**Grau:** Mestrado | **Ano:** 1º Ano | **Semestre:** 1º Semestre  
**Docente:** Prof. José Augusto Afonso  
**Áreas:** Comunicações Sem Fios, Camada Física RF, Qualidade de Serviço (QoS), Controlo de Acesso ao Meio (MAC) e Standards IEEE (802.11, 802.15)

## 📌 Sobre a Cadeira
Unidade curricular de mestrado focada no estudo aprofundado dos princípios, técnicas e protocolos de comunicação sem fios aplicados à Internet das Coisas (IoT). Abrange desde os fenómenos físicos de propagação no meio radioelétrico até ao projeto de camadas MAC e arquiteturas de rede sem fios de área pessoal e local (WPAN/WLAN).

## 🎯 Principais Tópicos Abordados

* **1. Arquitetura de Redes Sem Fios & Standards:**
  * Tipologias de redes: WLAN, WPAN, WMAN e Redes Celulares.
  * Modelos de comunicação: Direta (*Peer-to-Peer*) vs. Centralizada (*Access Point* / *Base Station*), Ad-hoc vs. Infraestruturada.
  * Estrutura do Comité IEEE 802 (802.3, 802.11, 802.15 e respetivos *Task Groups*).
  * Encapsulamento de dados: Unidades de dados PDU, SDU, PPDU e MPDU.

* **2. Camada Física Sem Fios (Wireless Physical Layer):**
  * **Fundamentos RF:** Espectro eletromagnético, notação em Decibéis ($dB$, $dBm$, $dBW$), antenas isotrópicas e ganho.
  * **Deterioração do Sinal:** Perdas em espaço livre (*Path Loss*), atenuação, reflexão, refração, difração, espalhamento e propagação multipercurso (*Fading* e Interferência Inter-Símbolos - ISI).
  * **Rácio Sinal-Ruído:** Relação $E_b/N_0$ (energia por bit sobre densidade de potência de ruído), ruído térmico e cálculo de BER (*Bit Error Rate*).
  * **Técnicas de Modulação & Espalhamento Espetral:**
    * Modulações analógicas e digitais (ASK, FSK, PSK, QAM).
    * Correção de erros à cabeça (FEC) e *Interleaving*.
    * Espalhamento Espetral: DSSS (*Direct Sequence Spread Spectrum*) e FHSS (*Frequency Hopping Spread Spectrum*).

* **3. Qualidade de Serviço (QoS) & Desempenho:**
  * Parâmetros objetivos: Atraso (*Delay*), *Jitter*, *Throughput* / *Goodput*, PER (*Packet Error Rate*) e *Delivery Ratio*.
  * Análise de componentes de atraso: Transmissão, propagação, processamento e acesso ao meio.
  * Suporte de tráfego de tempo real e classes de serviço.

* **4. Controlo de Acesso ao Meio (MAC Layer) & IEEE 802.11:**
  * Técnicas de acesso múltiplo: SDMA, FDMA, TDMA e CDMA.
  * Mecanismos de contenção e reserva dinâmica (CSMA/CD, CSMA/CA, PRMA, MASCARA).
  * **Arquitetura IEEE 802.11 (Wi-Fi):** BSS, ESS, IBSS, mecanismos CSMA/CA com RTS/CTS para mitigação do problema do nó escondido, e evolução dos padrões (802.11a/b/g/n/ac/ax/p/af/ah).

## 📂 Organização da Pasta
* 📖 **`Teoricas/`:** Diapositivos oficiais cobrindo introdução a redes sem fios, camada física, qualidade de serviço, controlo de acesso ao meio e a norma IEEE 802.11.
* 📝 **`Exercicios/`:** Listas de exercícios práticos resolvidos sobre cálculo de atenuação, perdas em espaço livre, ruído térmico, $E_b/N_0$, atrasos de propagação e análise de tráfego.
* 📑 **`Avaliacoes/`:** Enunciados e resoluções dos 2 Testes de avaliação da unidade curricular.

## 🛠️ Conceitos e Ferramentas
* **Cálculos RF:** Perda em espaço livre ($FSPL$), densidade de ruído ($N_0 = k T$), cálculo de nível de sinal em $dBm$/$dBW$.
* **Análise Protocolar:** Padrões IEEE 802.11 e IEEE 802.15.4 (ZigBee/PAN).

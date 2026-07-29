# ✈️💡 Sistema Li-Fi para Ambiente Aeroportuário

**Grau:** Mestrado | **Ano:** 1º Ano | **Semestre:** 2º Semestre (Projeto Integrador)  
**Autores:** Luís Baptista, Bernardo Salgado, Nuno Mirra, Pedro Daniel  
**Áreas:** Comunicações Óticas (Li-Fi), Eletrónica Analógica, Sistemas Embebidos (ESP32), Redes (Modelo OSI) e Web Development

## 📌 Sobre a Cadeira
O Projeto Integrador em Telecomunicações e Informática (PITI) é uma unidade curricular desenhada para integrar competências transversais de eletrónica, redes e software. O objetivo consiste em construir um sistema de comunicação completo do zero, desde a modulação do sinal elétrico na camada física até à interface do utilizador na camada de aplicação.

---

## 🏆 Projeto Desenvolvido: Sistema de Comunicação Ótica Sem Fios (Li-Fi)
**O Desafio:** Em ambientes de elevada densidade como aeroportos, as redes sem fios por radiofrequência (Wi-Fi) sofrem de saturação espetral e interferência (EMI). O projeto visou criar uma alternativa de comunicação baseada em luz infravermelha (Li-Fi) para a transmissão segura e confinada de dados a passageiros.

Para garantir o sucesso deste sistema, a arquitetura foi dividida em três fases de desenvolvimento, acompanhando estritamente as camadas do modelo OSI:

### 📡 Fase A - Camada Física (Transdutor Ótico)
* **Desenho do Hardware Analógico:**
  * **Emissor:** Geração de portadora a 100 kHz (modulação OOK - *On-Off Keying*) utilizando um temporizador **NE555** e transístores para acionamento do LED infravermelho.
  * **Recetor (Frontend Ótico):** Utilização de um fototransístor acoplado a múltiplos andares de amplificação operacional (**TL084**). Implementação de um Amplificador de Transimpedância (TIA) para conversão corrente-tensão, filtragem de ruído de luz solar/lâmpadas (Filtro Passa-Alto a 50Hz) e um detetor de envelope para recuperação do sinal banda-base.
  * **Desafio Superado:** Para atingir o alcance pretendido de 1 metro, foi necessário escalar o ganho adicionando um segundo amplificador operacional em cascata.

### 🔗 Fase B - Camada de Ligação de Dados (Controlo de Erros e Fluxo)
* **Processamento Embebido (ESP32):**
  * Desenho de uma trama de comunicação com delimitação (*Start of Frame*), endereçamento MAC e controlo de sequência.
  * **Controlo de Erros:** Implementação de um código de bloco **Hamming (7,4)** combinado com CRC para deteção e correção automática de erros no canal ruidoso.
  * **Controlo de Fluxo:** Implementação do protocolo ARQ *Stop-and-Wait*.
  * **Desafio Superado:** O processamento na ESP32 e a latência de transferência exigiram a recalibração de temporizadores (Timeouts para 2.0s) e retransmissões (limite de 7 tentativas) para manter o feixe ótico estável.

### 💻 Fase C - Camada de Aplicação e Integração Full-Duplex
* **Multiplexagem e Interface do Utilizador:**
  * Criação de um protocolo assimétrico: *Downlink* via feixe IV e *Uplink* de controlo (ACKs) por cabo/série, com ligação a um servidor de backend.
  * **Interface Web (React/WebSockets):** O passageiro pode consultar horários de voos em tempo real e descarregar ficheiros binários utilitários.
  * **Desafio Superado:** Como a baixa taxa de transmissão física (9600 baud rate) poderia congelar a aplicação durante a transferência de ficheiros (estrangulamento do canal), foi desenhado um mecanismo de **multiplexagem assíncrona** permitindo a navegação simultânea e retomas de transferências (Resume) sem bloqueios na interface.

---

## 📂 Organização da Pasta
* 📄 **`Enunciado/`:** Especificações do Projeto Laboratorial de PITI.
* 🔌 **`Fase_A_Camada_Fisica/`:** Relatório de planeamento e dimensionamento do hardware ótico e circuitos analógicos, acompanhado da apresentação técnica.
* ⚙️ **`Fase_B_Camada_Ligacao/`:** Racional do algoritmo de correção de erros e especificação do controlo de fluxo Stop-and-Wait no ESP32.
* 🚀 **`Fase_C_Camada_Aplicacao/`:** Relatórios finais, diagrama de integração do sistema, avaliação do *link budget*, documento de síntese (apresentação interativa) e demonstração de eficiência global.

## 🛠️ Stack Tecnológica
* **Hardware & IoT:** Osciloscópios, Geradores de Funções, CI NE555, AmpOp TL084, ESP32, LEDs IV e Fototransístores.
* **Redes:** Modulação OOK, Hamming (7,4), Stop-and-Wait, TCP/IP, WebSockets.
* **Software:** C/C++ (ESP32), React (Frontend Web), Node.js (Servidor Local).

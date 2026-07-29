# 📡 Protocolo de Comunicação de Dados - PITI (Fase B)

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![OS](https://img.shields.io/badge/OS-Linux%20%7C%20Arch-lightgrey)
![Status](https://img.shields.io/badge/Status-Concluído-success)

Este repositório contém a implementação completa de uma **Stack Protocolar Customizada** desenvolvida para a disciplina de Projeto Integrado de Tecnologias de Informação (PITI) - Grupo 3. 

O sistema implementa as Camadas Física, de Ligação de Dados e de Aplicação (baseadas no Modelo OSI/TCP-IP), permitindo a transferência de ficheiros (Texto, Imagens e Documentos binários) através de um canal de comunicação série (UART/ESP32) de forma 100% fiável.

---

## 🚀 Principais Funcionalidades e Mecanismos

A nossa arquitetura foi desenhada para resistir a canais ruidosos e quebras de ligação, implementando técnicas avançadas de Redes de Computadores:

* **Enquadramento (Framing):** Baseado no protocolo HDLC com flags `SOF` e algoritmo de *Byte Stuffing/Destuffing* para garantir a transparência dos dados.
* **Deteção de Erros (FCS):** Verificação de integridade ponta-a-ponta através de matemática polinomial **CRC-8**.
* **Correção Forward Error Correction (FEC):** Implementação nativa de codificação de canal usando o **Código de Hamming (7,4)**, permitindo a deteção e correção instantânea de erros de bit único por *nibble*, sem necessidade de retransmissão.
* **Controlo de Fluxo e Erros (ARQ):** Máquina de estados baseada no protocolo **Stop-and-Wait** com alternância de bits (0 e 1) para prevenir pacotes duplicados.
* **Recuperação de Falhas:** Temporizadores (*Timeouts*) para pedidos de retransmissão e um Monitor de Inatividade de Sessão que atua em caso de falha grave do link.

---

## 📂 Estrutura do Repositório

O projeto segue uma arquitetura modular, onde cada ficheiro representa um bloco funcional independente:

```text
📁 PITI-FaseB/
│
├── 📝 app_cliente.py               # Camada de Aplicação: Emissor
├── 📝 app_servidor.py              # Camada de Aplicação: Recetor
│
├── 📝 camada_ligacao_dados.py      # Core da Camada 2 (Integra os módulos abaixo)
├── 📝 camada_fisica.py             # Interface de Hardware (Porta Série/UART)
├── 📝 framing_hdlc.py              # Byte Stuffing e Delimitação
├── 📝 encapsulamento.py            # Formatação do Cabeçalho (PDU)
├── 📝 crc8.py                      # Algoritmo Cyclic Redundancy Check
├── 📝 fec_hamming.py               # Matemática do Código de Hamming (7,4)
├── 📝 maquina_estados_arq.py       # Lógica do protocolo Stop-and-Wait
├── 📝 temporizador_arq.py          # Gestão temporal de ACKs e retransmissões
├── 📝 constantes_protocolo.py      # Tipos de trama e parâmetros físicos
├── 📝 logger.py                    # Sistema de formatação de logs e terminal
│
├── 📁 Testes/                      # Scripts de auditoria e stress ao protocolo
│   ├── teste_falhas.py             # Simula injeção de ruído no canal (Bit flips e Drops)
│   └── teste_desempenho.py         # Avaliação de Débito (Throughput) e Fiabilidade
│
├── 📁 ficheiros_enviados/          # (Opcional) Ficheiros de teste do utilizador
└── 📁 ficheiros_recebidos/         # Diretório criado dinamicamente pelo Recetor
⚙️ Instalação e Requisitos
Certifica-te que tens o Python 3.8+ instalado no teu sistema.

Instala a dependência de comunicação de hardware (PySerial):

pip install pyserial

Verifica as tuas portas de comunicação. Por defeito, os scripts estão configurados para os ambientes Linux (Ex: /dev/ttyUSB0 e /dev/ttyUSB1). Altera as constantes PORTA_COM no app_cliente.py e app_servidor.py caso utilizes Windows (COM3, COM4, etc.).

💻 Como Utilizar
Para testar o protocolo em pleno funcionamento, necessitas de dois terminais abertos em simultâneo (simulando dois computadores).

1. Iniciar o Servidor (Recetor)
No primeiro terminal, inicia a escuta contínua:

python app_servidor.py

2. Iniciar o Cliente (Emissor)
No segundo terminal, invoca o emissor passando como argumento o caminho relativo do ficheiro a enviar:

python app_cliente.py ficheiros_enviados/documento.pdf

O sistema irá automaticamente inferir o tipo de ficheiro, aplicar todo o processamento de rede e guardar o ficheiro reconstruído e validado na diretoria ficheiros_recebidos/.

🛠️ Auditoria e Demonstração
O projeto inclui módulos de teste criados especificamente para a defesa técnica:

Injeção de Ruído: python Testes/teste_falhas.py
(Demonstra o protocolo a recuperar autonomamente de erros de CRC adulterados e interrupções de cabo).

Teste de Throughput: python Testes/teste_desempenho.py
(Envia tráfego pesado para medir a velocidade de transmissão efetiva da rede em bps).

Desenvolvido por Grupo 3 - PITI.


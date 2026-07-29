# 🌐 Redes de Acesso e Núcleo (RAN)

**Grau:** Mestrado | **Ano:** 1º Ano | **Semestre:** 2º Semestre  
**Docentes:** Prof. Flávio de Oliveira Silva  
**Áreas:** Redes de Núcleo (Core), Redes de Acesso, MPLS-TE, DiffServ-TE, DWDM, Redes Óticas Passivas (PON) e Emulação com EVE-NG

## 📌 Sobre a Cadeira
Unidade curricular de mestrado focada no projeto, dimensionamento e gestão de arquiteturas de redes de telecomunicações de grande escala. Abrange a evolução e integração dos segmentos de acesso (cobre, fibra PON e constelações de satélite) com o núcleo de rede de alta velocidade (backbone IP/MPLS e infraestrutura ótica DWDM).

## 🎯 Principais Tópicos Abordados

* **1. Tecnologias e Arquiteturas de Redes de Acesso:**
  * Evolução do acesso fixo e móvel: Par de cobre, xDSL, FTTx e Redes Óticas Passivas (**PON** / GPON / EPON).
  * Comunicações por Satélite: Comparação entre órbitas **GEO**, **MEO** e **LEO** (latência, *throughput*, atenuação e rastreio).
* **2. Núcleo de Rede & Multiprotocol Label Switching (MPLS):**
  * Limitações do roteamento IP tradicional (*best-effort*, *hop-by-hop*) face aos requisitos de débitos na ordem dos centenas de Gbps.
  * Encaminhamento baseado em etiquetas: Routers LER (*Label Edge Router*) e LSR (*Label Switching Router*).
  * Distribuição de etiquetas com **LDP** e engenharia de tráfego com **RSVP-TE**.
  * **Engenharia de Tráfego (MPLS-TE) & DiffServ-TE:**
    * Criação de túneis de tráfego com rotas explícitas disjuntas e suporte de largura de banda reservada.
    * Integração com modelos de Qualidade de Serviço (DiffServ): Classificação de tráfego, marcação de pacotes e **Policy-Based Routing (PBR)** para isolamento de fluxos (ex.: HTTP vs. UDP/Multimédia).
* **3. Redes Óticas de Transporte (OTN / DWDM):**
  * Evolução das redes de multiplexagem: SDH (*Synchronous Digital Hierarchy*) até às redes DWDM (*Dense Wavelength Division Multiplexing*).
  * Integração de Inteligência Artificial / *Knowledge-Defined Networking* (**KDN**) no plano de controlo SDN para otimização autónoma da camada física ótica (ROADMs, amplificadores e transceivers).

---

## 🏆 Trabalhos Práticos em Destaque

### 🧪 TP1: Modelação e Análise de Desempenho no EVE-NG
* **Descrição:** Instalação e orquestração do emulador **EVE-NG**, simulação de ligações de acesso com injeção de parâmetros reais (latência, *jitter*, *packet loss*) via **NETem** e medição de largura de banda e throughput máximo em TCP e UDP recorrendo ao **iPerf3**.

### 🛠️ TP2: Engenharia de Tráfego com MPLS-TE & DiffServ-TE (Topologia Duplo Peixe)
* **Descrição:** Implementação e validação de uma infraestrutura de rede de núcleo MPLS completa em ambiente EVE-NG numa topologia complexa em *Duplo Peixe*.
* **Funcionalidades:**
  * Configuração de *underlay* IGP com OSPF e túneis de tráfego explícitos com RSVP-TE.
  * Balanceamento de carga assimétrico e garantia de resiliência sob falha de ligações críticas (*fast-reroute*).
  * Separação de tráfego aplicacional usando **Policy-Based Routing (PBR)** para direcionar tráfego HTTP e streaming UDP para túneis distintos com garantias de QoS.
* **Autores:** Luís Baptista e Bernardo Salgado.

### 🧠 TP3: Arquitetura Conceitual de Redes DWDM Baseadas em IA (KDN)
* **Descrição:** Proposta e modelação teórica de uma arquitetura de rede ótica DWDM/OTN de próxima geração operada por controladores SDN com integração de algoritmos de Aprendizagem por Reforço (RL) e Máquinas de Vetores de Suporte (SVM) no plano de conhecimento (KDN) para gestão autónoma de recetores e ROADMs.

---

## 📂 Organização da Pasta
* 📖 **`Teoricas/`:** Apresentações teóricas oficiais sobre Redes de Acesso (PON/Satélites), Arquitetura MPLS/MPLS-TE e Redes Óticas (SDH/WDM).
* 🧪 **`Trabalho_Pratico_1_EVE_iPerf/`:** Roteiro, relatórios e testes de medição de desempenho com iPerf3 e NETem no EVE-NG.
* 🛠️ **`Trabalho_Pratico_2_MPLS_TE/`:** Relatório técnico completo (`Relatório Overleaf.pdf`), enunciados e ficheiros de configuração (*startup-configs*) da topologia *Duplo Peixe* em MPLS-TE.
* 🧠 **`Trabalho_Pratico_3_Redes_Oticas_AI/`:** Especificação da arquitetura conceitual para redes óticas DWDM inteligentes baseadas em IA/KDN.

## 🛠️ Tecnologias e Ferramentas
* **Emulação de Redes:** EVE-NG (Community Edition) / Cisco IOS XE (OSPF, MPLS, RSVP-TE, PBR)
* **Análise de Desempenho:** iPerf3, Linux NETem, Wireshark
* **Conceitos de Núcleo:** MPLS, MPLS-TE, DiffServ-TE, PBR, DWDM, PON, KDN

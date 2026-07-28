# 🌍 Redes de Computadores II

**Ano:** 3º Ano | **Semestre:** 2º Semestre  
**Área:** Roteamento Avançado, Sistemas Autónomos, IPv6, QoS e Emulação de Redes  
**Ferramentas:** Emulador CORE, Quagga (`vtysh`), Ubuntu, Wireshark

## 📌 Sobre a Cadeira
Unidade curricular avançada de engenharia de redes, focada nos mecanismos de encaminhamento de grande escala na Internet, transição para o protocolo IPv6, gestão de tráfego, qualidade de serviço (QoS) e controlo de congestionamento em redes de computadores de alta velocidade.

## 🎯 Principais Tópicos Abordados
* **Encaminhamento Intra-Domínio e Inter-Domínio:**
  * Sistemas Autónomos (AS) e agregação de rotas.
  * Protocolos de Encaminhamento Interno (IGP): OSPF (Estado de Ligação) e RIP (Vetor de Distância, divisão de horizontes e envenenamento do percurso inverso).
  * Protocolos de Encaminhamento Externo (EGP): **BGP** (*Border Gateway Protocol*), políticas de encaminhamento e interconexão de ISPs.
* **O Protocolo IPv6:**
  * Motivação e esgotamento do espaço IPv4.
  * Formato otimizado do cabeçalho IPv6 e extensões.
  * Esquemas de endereçamento e tipos de endereços (Unicast, Multicast, Anycast).
  * Mecanismos de transição: Stack Dupla (*Dual Stack*) e Túneis IP-sobre-IP.
* **Qualidade de Serviço (QoS):**
  * Modelo DiffServ (*Differentiated Services*): Classificação, marcação e funções de encaminhamento em routers de fronteira vs. interiores.
* **Controlo de Fluxo e Congestionamento (TCP):**
  * Comportamento do TCP-Reno, fases de *Slow Start* e *Congestion Avoidance*, limiar (*threshold*) e mecanismos de controlo de fluxo ponta a ponta.
  * Conexões HTTP persistentes com pipelining e gestão de sockets.

## 📂 Organização da Pasta
* 📖 **`Teoricas/`:** Apresentações teóricas oficiais sobre IPv6, algoritmos de encaminhamento (Partes 1, 2 e 3) e roteamento inter-domínio.
* 💻 **`Praticas/`:** Guiões de exercícios teórico-práticos de subnetting, algoritmos de estado de ligação/vetores de distância e o **Guia Prático do CORE** para ambiente Ubuntu.
* 📑 **`Avaliacoes/`:** Enunciados e resoluções de testes e exames de avaliação.
* 🛠️ **`Trabalho_CORE/`:** Ficheiros de topologia de simulação (`.xml`), configuração de routers e relatórios práticos do projeto de emulação de redes.

## 🛠️ Tecnologias e Ferramentas
* **Emulação de Redes:** CORE (*Common Open Research Emulator*)
* **Gestão de Roteamento:** Quagga (`vtysh` para comandos Cisco-like como `show ip route` e `show ip bgp`)
* **Sistema Operativo:** Ubuntu Linux

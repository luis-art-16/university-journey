# 🛠️ Gestão e Virtualização de Redes (GVR)

**Grau:** Mestrado | **Ano:** 1º Ano | **Semestre:** 1º Semestre  
**Áreas:** Gestão de Infraestruturas (SNMP/NETCONF) & Software-Defined Networking (SDN/OpenFlow)  
**Ferramentas:** MIB Designer, Net-SNMP, Open vSwitch / Mininet, Controladores SDN, OpenFlow

## 📌 Sobre a Cadeira
Unidade curricular de mestrado que combina os dois pilares da administração de redes avançadas: a monitorização/gestão clássica e moderna de dispositivos heterogéneos (Gestão de Redes) e a programação dinâmica da camada de encaminhamento através de redes definidas por software e virtualização (Virtualização de Redes).

---

## 🎯 Principais Tópicos Abordados

### 📡 1. Gestão de Redes (GR)
* **Arquiteturas e Modelos de Gestão:**
  * Modelo TMN (ITU-T M.3010) e modelo de gestão da Internet (SNMP Framework).
* **Protocolo SNMP (Simple Network Management Protocol):**
  * Evolução: SNMPv1, SNMPv2c e **SNMPv3** (segurança com USM - *User-based Security Model* e VACM).
  * Comandos de consulta e alteração: `snmpget`, `snmpgetnext`, `snmpwalk`, `snmpset`, `snmptable` e *Traps/Notifications*.
* **Modelação de Informação de Gestão (SMI & MIBs):**
  * Linguagem ASN.1, SMIv1 e SMIv2.
  * Estrutura da árvore MIB (`iso.org.dod.internet.mgmt.mib-2`).
  * Modelação de tabelas concetualmente complexas (`SEQUENCE`, `INDEX`, campos `RowStatus` para gestão dinâmica de entradas).
  * Edição visual de MIBs com **MIB Designer** e instrumentação de agentes SNMP em Python/Java com Net-SNMP.
* **Gestão Moderna de Redes:**
  * Protocolo **NETCONF** (RFC 6241) baseado em XML/SSH e operações sobre *datastores* (`<get-config>`, `<edit-config>`, `<commit>`).
  * Linguagem de modelação de dados **YANG** (RFC 7950).

---

### 🔀 2. Virtualização de Redes & SDN (VR)
* **Software-Defined Networking (SDN):**
  * Separação clara entre o **Plano de Controlo** (centralizado na figura do Controlador SDN) e o **Plano de Dados** (executado pelos *switches*).
* **O Protocolo OpenFlow:**
  * Arquitetura de um *OpenFlow Switch* e o canal seguro com o Controlador.
  * **Pipelines de Processamento:** Processamento sequencial por tabelas de fluxo (começando obrigatoriamente na Tabela 0).
  * Estrutura de uma entrada de fluxo:
    * **Header Match Fields:** Filtragem por portas de entrada, endereços MAC/IP, tipo de tráfego (TCP/UDP/ICMP) e portas L4.
    * **Priority & Counters:** Resolução de conflitos por prioridade e métricas de tráfego.
    * **Instructions & Actions:** Ações como `goto_table` (para tabelas seguintes), `set_field` (reescrita de IPs/portas), `output` (envio para porta ou controlador) e `drop` (descarte).
* **Aplicações Práticas de OpenFlow:**
  * Implementação de regras proativas e reativas.
  * Construção de Pipelines com funções encadeadas: **Firewall/Filtragem L3/L4** na Tabela 0, **NAT (Network Address Translation)** na Tabela 1 e **Encaminhamento de Saída** na Tabela 2.

---

## 📂 Organização da Pasta
* 📖 **`Teoricas_e_Guias/`:** Slides teóricos oficiais de GR e VR, guias de SNMP, NETCONF e documentação do MIB Designer.
* 📊 **`Componente_GR/`:** Testes teóricos/práticos modelo, ficheiros `.txt` das MIBs personalizadas desenvolvidas em ASN.1, guias de instrumentação do agente SNMP e o **Trabalho Prático de Gestão de Redes**.
* 🔀 **`Componente_VR/`:** Notas das aulas práticas de OpenFlow, definições de pipelines, regras de fluxo OpenFlow, o teste de VR e o **Trabalho Prático de Virtualização de Redes / SDN**.

## 🛠️ Tecnologias e Ferramentas
* **Gestão:** Net-SNMP (`snmpwalk`, `snmpget`, `snmpsim`), MIB Designer 3.2, NETCONF, PySNMP / Python.
* **Virtualização / SDN:** OpenFlow (v1.3/v1.5), Open vSwitch (OVS), Mininet, Controladores SDN (Ryu / Floodlight).

# 🛡️ Cibersegurança

**Grau:** Mestrado | **Ano:** 1º Ano | **Semestre:** 2º Semestre  
**Áreas:** Segurança de Redes, Criptografia Aplicada, Controlo de Acesso, Análise de Risco e Deteção de Intrusões (IDS)  
**Ferramentas:** OpenSSL, GnuPG (Kleopatra), Wireshark, Suricata NIDS, Linux Firewalls

## 📌 Sobre a Cadeira
Unidade curricular orientada aos aspetos ofensivos e defensivos da segurança da informação. Combina o estudo teórico de políticas de segurança, modelos formais e gestão de risco com a implementação "hands-on" de infraestruturas de chaves públicas, análise forense de pacotes e configuração de sistemas de deteção de intrusão em tempo real.

---

## 🏆 Portefólio de Trabalhos Práticos (TPs)

Esta cadeira foi integralmente avaliada com base na execução e documentação de 5 laboratórios/trabalhos práticos intensivos (desenvolvidos em colaboração com Bernardo Salgado):

### 🏭 TP1: Análise de Risco Simplificada (SCADA / ICS)
* **Contexto:** Avaliação de ameaças em Redes de Controlo Industrial (OT vs. IT).
* **Trabalho Desenvolvido:** Identificação de vulnerabilidades que permitem movimentos laterais e acesso remoto indevido. Proposta de arquiteturas de defesa em profundidade baseadas nas normas da ENISA, implementando **Data Diodes**, **Firewalls Industriais** com inspeção profunda (Modbus/DNP3) e **Bastion Hosts / Jump Servers** na DMZ para mitigar riscos de interrupção operacional (Disponibilidade e Integridade).

### 🔐 TP2: Modelos Formais de Controlo de Acesso (Bell-LaPadula)
* **Contexto:** Aplicação de modelos matemáticos de segurança (Lattice e BLP).
* **Trabalho Desenvolvido:** Construção de um reticulado (*Lattice*) combinando níveis de segurança (Public, Confidential, Strictly Confidential) com categorias (Serviços Académicos e Científicos). Mapeamento das propriedades "Simple Security" (No Read Up) e "*-Property" (No Write Down) para ecossistemas modernos através de *Mandatory Access Control* (MAC) com **SELinux** e **Microsoft AD RMS**.

### 🔑 TP3: Infraestrutura de Chaves Públicas (PKI) e PGP
* **Contexto:** Gestão de certificados, assinaturas digitais e revogação.
* **Trabalho Desenvolvido:** Laboratório prático dividido em duas partes:
  1. **Modelo Descentralizado (Web of Trust):** Criação e partilha de chaves assimétricas usando PGP (GnuPG/Kleopatra).
  2. **Modelo Hierárquico (X.509):** Simulação de uma Autoridade Certificadora (CA) local com **OpenSSL**. Geração de chaves RSA (`genrsa`), pedidos de assinatura de certificado (`req`), emissão de certificados autoassinados (`x509`) e exportação no formato PKCS#12 (`pkcs12`).

### 🕵️‍♂️ TP4: Análise Forense de Tráfego de Rede
* **Contexto:** Inspeção de pacotes e reconstrução de sessões.
* **Trabalho Desenvolvido:** Utilização de ferramentas de *packet sniffing* (ex: Wireshark / `pcap`) para identificar anomalias, isolar tráfego suspeito, extrair metadados estatísticos e rastrear sessões TCP/HTTP complexas, incluindo processos de autenticação em texto limpo ou tráfego malicioso.

### 🚨 TP5: Ferramentas de Segurança (Firewalls e Suricata NIDS)
* **Contexto:** Proteção de perímetro e Deteção de Intrusões baseada em assinaturas.
* **Trabalho Desenvolvido:** * Configuração avançada de regras de firewall (bloqueio por portas, limites de taxa de conexão, agendamentos e políticas de negação de serviço a sites específicos).
  * Implementação e afinação do **Suricata NIDS**, separando o papel do Engenheiro de Segurança (afinação de regras para mitigar falsos positivos/negativos) do papel do Analista de Dados na inspeção de milhares de alertas de segurança.

---

## 📂 Organização da Pasta
* 📄 **`TP1_Analise_de_Risco/`:** Relatório sobre ameaças a sistemas SCADA e arquitetura de mitigação.
* 📄 **`TP2_Controlo_de_Acesso/`:** Relatório detalhado sobre o modelo Bell-LaPadula e reticulados de segurança.
* 🛠️ **`TP3_PKI_e_Criptografia/`:** Guiões de laboratório, comandos OpenSSL e o *LogBook* (Relatório) com a demonstração prática da PKI.
* 📊 **`TP4_Analise_de_Trafego/`:** Template/Roteiro de dissecação e síntese de ficheiros de captura de tráfego (`.pcap`).
* 🧱 **`TP5_Firewalls_e_NIDS/`:** Documentação do laboratório de configuração de firewalls Linux e Suricata IDS.

# 🌐 Emulação e Simulação de Redes de Telecomunicações

**Grau:** Mestrado | **Ano:** 1º Ano | **Semestre:** 1º Semestre  
**Ferramentas Principais:** GNS3, CupCarbon, Docker, NGINX, MQTT

## 📌 Sobre a Cadeira
Unidade curricular orientada à simulação e emulação de arquiteturas de redes complexas. O foco é a integração de ferramentas de simulação de Redes de Sensores Sem Fios (WSN) com plataformas de emulação de redes IP de topo, culminando na orquestração de serviços Cloud através de contentores.

---

## 🏆 Projeto: Infraestrutura IoT para o Campus de Azurém
**Autores:** Luís Baptista, Bernardo Salgado, Nuno Mirra  
**Tema:** Parque Inteligente e Controlo Ambiental (Smart Parking + Monitorização de CO2)

O projeto consistiu no desenho de uma arquitetura "fim-a-fim" para a gestão de estacionamento e monitorização da qualidade do ar nos parques subterrâneos da Universidade do Minho. Em vez de tratar a rede e os sensores como componentes isolados, o projeto simulou todo o ecossistema: desde a recolha física dos dados, passando pelo encaminhamento na rede core, até à apresentação em dashboards na Cloud.

### 🔄 Fases de Desenvolvimento
* **Fase A (Especificação e Arquitetura):**
  * Definição dos requisitos funcionais, topologia de rede, planeamento e esquema de endereçamento (IPv4/NAT) para a integração dos dispositivos IoT.
* **Fase B (Simulação e Prototipagem):**
  * Modelação dos sensores ambientais e de estacionamento utilizando o simulador de IoT **CupCarbon**.
  * Integração da rede simulada com o emulador **GNS3** para simular o tráfego a atravessar o *backbone* da rede académica.
* **Fase C (Integração Cloud e Sistema Completo):**
  * Implementação dos serviços de backend orquestrados em **Docker**.
  * Configuração de um broker MQTT (Eclipse Mosquitto) para a receção dos dados.
  * *Troubleshooting* e otimização da arquitetura face a estrangulamentos de tráfego.

### 🚀 Desafios Técnicos e Soluções (Destaque)
Durante as simulações intensivas da Fase C, o elevado volume de leituras dos múltiplos dispositivos concorrentes causou latência nas bases de dados e sobrecarga do backend. 
**A nossa solução:** Implementámos uma estratégia de **Replicação de Serviços (API/MQTT)** acoplada a um **Load Balancer (NGINX)**, reorganizando a estrutura das queries SQL. Isto garantiu alta disponibilidade e eliminou os gargalos da rede.

## 📂 Organização da Pasta
* 📄 **`Fase_A_Especificacao/`:** Relatório de Especificação Inicial (`REA-G3`).
* 📄 **`Fase_B_Prototipagem/`:** Relatório da arquitetura GNS3 e scripts de sensores do CupCarbon (`REB-G3`).
* 🚀 **`Fase_C_Sistema_Completo/`:** Relatório Final (`REC-G3`), Artigo Científico e Apresentação em modelo *pitch* abordando os desafios de latência e balanceamento de carga.

## 🛠️ Stack Tecnológica
* **Simulação IoT:** CupCarbon
* **Emulação de Rede Core:** GNS3 (Encaminhamento, NAT, Topologias)
* **Orquestração e Infraestrutura:** Docker, NGINX (Load Balancing)
* **Comunicação:** Protocolo MQTT (Mosquitto), APIs REST

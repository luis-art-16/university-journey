# 🩺 HealthSync: IoT System for Real-Time Vital Signs Monitoring

**Ano:** 3º Ano | **Semestre:** 2º Semestre (Projeto Integrado de Telecomunicações)  
**Autores:** Luís Baptista, Bernardo Salgado, Luís Marques  
**Área:** Internet das Coisas (IoT), Sistemas Embebidos, Aplicações Cloud e Tele Saúde  

## 📌 Sobre a Cadeira
Unidade curricular de projeto integrador do 3º ano, desenhada para aplicar os conhecimentos acumulados de redes, sistemas distribuídos, eletrónica e programação na conceção, desenvolvimento e validação de um sistema tecnológico completo, dividido em três fases evolutivas (**Fase A, Fase B e Fase C**).

---

## 🏆 Projeto Desenvolvido: HealthSync
O **HealthSync** é uma plataforma IoT abrangente desenvolvida para a monitorização contínua e em tempo real de sinais vitais (temperatura, frequência cardíaca, nível de oxigénio no sangue - $SpO_2$ e movimento), integrando recolha por hardware (*wearables*), transmissão sem fios de baixa latência, processamento analítico em backend e dashboards interativos para doentes, cuidadores e profissionais de saúde.

### 🔄 Fases de Desenvolvimento do Projeto
* **Fase A (Especificação e Arquitetura):**
  * Definição dos requisitos do sistema, arquitetura geral por diagrama de blocos, planeamento temporal e estudo de viabilidade tecnológica.
* **Fase B (Prototipagem e Comunicação):**
  * Implementação da infraestrutura de comunicação baseada no protocolo **MQTT** (com broker Eclipse Mosquitto), simulação de geradores de dados e validação inicial da transmissão de mensagens de sensores.
* **Fase C (Sistema Completo, Segurança e Validação):**
  * Integração do hardware (microcontrolador ESP32 e sensores), backend em Node.js / Flask, base de dados relacional MySQL, interface web de administração e aplicação móvel nativa/híbrida (React Native).
  * Implementação de camadas de segurança robustas (Autenticação baseada em tokens JWT via OAuth2, encriptação AES-256 e TLS 1.3) e testes de robustez/desempenho.

---

## 📂 Organização da Pasta
* 📄 **`Fase_A_Especificacao/`:** Relatório de Especificação da Fase A (`REA-G2-JAA.pdf`).
* 📄 **`Fase_B_Prototipagem/`:** Relatório da Fase B focado na configuração do MQTT e testes de subscrição/publicação (`REB-G2_HCR.pdf`).
* 📄 **`Fase_C_Sistema_Completo/`:** Relatório Final Completo da Fase C (`REC-G2.pdf`), Artigo Científico (`artigo final template.pdf`) e Poster Científico (`Poter_Final.pdf`).
* 🎬 **`Recursos_Multimédia/`:** Vídeo de demonstração funcional do sistema HealthSync (`Vídeo.mp4`).

---

## 🛠️ Stack Tecnológica
* **Hardware & IoT:** Dispositivos ESP32, sensores biométricos de sinais vitais, protocolo de mensagens leve **MQTT**.
* **Backend & Base de Dados:** Node.js / Python Flask, API REST, Base de Dados MySQL.
* **Frontend & Mobile:** Dashboard Web administrativo (HTML/CSS/JavaScript), Aplicação Móvel (*React Native*).
* **Segurança & Infraestrutura:** TLS 1.3, AES-256, OAuth2 com JSON Web Tokens (JWT), ferramentas de auditoria e logging.

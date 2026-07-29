# 🚗📡 Redes Veiculares (VANETs & V2X)

**Grau:** Mestrado | **Ano:** 1º Ano | **Semestre:** 2º Semestre (UC Opcional)  
**Docentes:** Prof. António Luís Costa
**Áreas:** Redes Ad-hoc Móveis (MANETs), Redes Veiculares (VANETs), Redes Tolerantes a Atrasos (DTN), Padrões C-ITS / ETSI ITS-G5 e Simulação V2X  
**Ferramentas de Simulação:** Eclipse MOSAIC 25.2, SUMO (*Simulation of Urban Mobility*)

## 📌 Sobre a Cadeira
Unidade curricular dedicada ao estudo dos novos paradigmas de redes móveis sem infraestrutura física fixa ou com conetividade intermitente. Aborda a transição das redes ad-hoc genéricas para ambientes veiculares altamente dinâmicos, focando-se na segurança rodoviária ativa, eficiência de tráfego colaborativa, arquiteturas V2X (*Vehicle-to-Everything*) e redes tolerantes a disrupções.

## 🎯 Principais Tópicos Abordados

* **1. Redes Móveis Ad-Hoc (MANETs) & Encaminhamento Geográfico:**
  * Desafios de mobilidade na Internet e desadequação do IP tradicional.
  * Algoritmos de encaminhamento baseados em localização geográfica, como o **LAR** (*Location-Aided Routing*), utilizando *route search zones* para limitar a inundação de pedidos (*flooding*).
* **2. Redes Tolerantes a Atrasos e Disrupções (DTN):**
  * Ausência de conetividade ponta-a-ponta permanente e o paradigma **Store-Carry-and-Forward**.
  * Camada *Bundle* (RFC 9171 / RFC 4838) e transferência de custódia entre nós.
  * Encaminhamento epidémico, riscos de colapso de *buffers* e mecanismos de limpeza proativa via **Dead Certificates / Anti-Packets**.
* **3. Redes Veiculares (VANETs) & Pilha ETSI ITS-G5:**
  * **Domínios de Comunicação:** In-Vehicle, Ad-Hoc (V2V - *Vehicle-to-Vehicle*) e Infraestrutura (V2I com RSUs - *Road Side Units* e OBUs - *On-Board Units*).
  * **Camada Física e MAC:** Operação na banda dos 5.9 GHz (IEEE 802.11p / OCB), modulação OFDM e Controlo de Acesso ao Meio com **EDCA** (*Enhanced Distributed Channel Access*) para priorização de tráfego crítico de segurança.
  * **Mensagens C-ITS:** Mensagens periódicas de estado **CAM** (*Cooperative Awareness Message*) e mensagens de evento **DENM** (*Decentralized Environmental Notification Message*).
  * **Gestão de Congestionamento:** Controlo descentralizado **DCC** (*Decentralized Congestion Control*) para regulação dinâmica do tempo de transmissão do canal radioelétrico.

---

## 🏆 Projeto em Destaque: Gestão Cooperativa de Tráfego em Zona de Obras com V2X
**Autores:** Luís Baptista, Bernardo Salgado, Luís Oliveira  
**Título do Artigo:** *Gestão Cooperativa de Tráfego em Zona de Obras com V2X: Harmonização de Fluxo e Prevenção de Deadlocks de Controlo* (Formato LNCS)

* **O Desafio:** Em vias de alta velocidade, zonas de obras funcionam como estrangulamentos críticos que geram ondas de choque (*shock waves*), paragens bruscas (*stop-and-go*) e acidentes devido à reação tardia à sinalização estática.
* **A Arquitetura de Simulação:**
  * **SUMO:** Modelação física do movimento microscópico dos veículos e colisões.
  * **Eclipse MOSAIC:** Emulação da camada de rede ad-hoc V2X (ETSI ITS-G5), incluindo perdas de propagação rádio (*fading*) e latências de canal.
* **A Solução & Resolução de Deadlock:**
  * Implementação de uma RSU (*Road Side Unit*) inteligente a 1000m da zona de obras.
  * A RSU analisa dinamicamente o estado da via e emite recomendações de velocidade com mecanismos de **histerese** e **anti-flooding** (`sequenceNumber`).
  * **Descoberta Científica:** A investigação identificou e corrigiu uma falha crítica de controlo onde a amostragem pela velocidade média da via retinha o tráfego permanentemente (*deadlock*). A solução passou a usar limiares espácio-temporais focados no número de veículos efetivamente parados, eliminando os fenómenos de *stop-and-go* e suavizando a transição de vias.

---

## 📂 Organização da Pasta
* 📖 **`Teoricas_e_Resumos/`:** Apresentações oficiais sobre MANETs, DTNs e Redes Veiculares, acompanhadas por uma compilação de resumos técnicos (`RV_Resumos.docx`) orientada à preparação de exames.
* 🛠️ **`Trabalho_Pratico_V2X/`:** Enunciado do projeto (`Veiculares-2526-Enunciado-TrabalhoPratico.pdf`), o Artigo Final completo em formato científico LNCS (`RV_COPYY (1).pdf`), a apresentação de defesa em PowerPoint (`Apresentação RV.pptx`) e os scripts de simulação MOSAIC/SUMO.

## 🛠️ Tecnologias e Ferramentas
* **Simulação de Tráfego e Redes:** Eclipse MOSAIC 25.2, SUMO (*Simulation of Urban Mobility*)
* **Protocolos e Padrões:** ETSI ITS-G5, IEEE 802.11p, CAM, DENM, EDCA, DTN Bundle Protocol, Java/C++

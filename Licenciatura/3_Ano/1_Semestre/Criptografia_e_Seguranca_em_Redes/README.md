# 🔐 Criptografia e Segurança em Redes

**Ano:** 3º Ano | **Semestre:** 1º Semestre  
**Linguagens / Ferramentas:** Python (`cryptography`), OpenSSL, Certificados X.509, RSA, AES, SHA-256

## 📌 Sobre a Cadeira
Unidade curricular dedicada aos princípios de segurança da informação, mecanismos criptográficos e protocolos de proteção de redes. Combina o estudo teórico de algoritmos de cifragem com o desenvolvimento prático de sistemas distribuídos seguros protegidos contra ataques e escutas indevidas.

## 🎯 Principais Tópicos Abordados
* **Princípios de Segurança & Modelação de Ameaças:**
  * **Tríade CIA:** Confidencialidade, Integridade e Disponibilidade (acrescida de Autenticidade e Não-repúdio).
  * **Modelo STRIDE:** *Spoofing*, *Tampering*, *Repudiation*, *Information Disclosure*, *Denial of Service* (DoS), e *Elevation of Privilege*.
  * Classificação de ataques: Ativos vs. Passivos.
* **Criptografia Simétrica:**
  * Cifras de Fluxo (*Stream Ciphers*) e Cifras Clássicas (OTP - *One-Time Pad*).
  * Cifras de Bloco (*Block Ciphers*): Princípios de Confusão e Difusão (Redes S-P) e algoritmo **AES** (128/192/256 bits).
  * Modos de Operação: ECB, CBC, CTR e gestão de vetores de inicialização (IV / *Nonce*).
* **Funções de Síntese / Hash Criptográficas:**
  * Propriedades: Resistência a pré-imagem, segunda pré-imagem e colisões.
  * Algoritmos: Famílias SHA-2 (SHA-256) e SHA-3. Aplicações na verificação de integridade e armazenamento seguro de credenciais.
* **Criptografia Assimétrica & Gestão de Chaves:**
  * Troca de chaves de Diffie-Hellman.
  * Algoritmos **RSA** e Criptografia de Curvas Elípticas (**ECC**).
  * Assinaturas Digitais e Infraestrutura de Chaves Públicas (**PKI** / Certificados X.509 e Autoridades Certificadoras - CA).
* **Segurança em Redes e Perímetro:**
  * *Firewalls* (Filtro de pacotes, *Stateful Inspection*, *Application Gateway*).
  * Sistemas de Detecção/Prevenção de Intrusões (IDS / IPS) e *Honeypots*.
  * Protocolos seguros (TLS/SSL, HTTPS, IPSec, S/MIME).

## 📂 Organização da Pasta
* 📖 **`Teoricas/`:** Diapositivos teóricos cobrindo introdução à segurança, criptografia simétrica (clássica e por blocos) e funções de síntese (*hash*).
* 📝 **`Notas_e_Resumos/`:** Guiões de estudo, resumos de preparação para exames e resoluções de questões/testes teóricos.
* 💻 **`Trabalho_Pratico/`:** Projeto prático de desenvolvimento de um **sistema assíncrono e seguro de troca de mensagens cliente-servidor** utilizando Python, chaves RSA para troca de chaves de sessão AES-CBC, e verificação de autenticidade via certificados X.509.

## 🛠️ Tecnologias e Criptossistemas
* **Linguagem:** Python 3
* **Bibliotecas:** `cryptography` (hazmat / primitives)
* **Padrões:** X.509, PKCS#7 / PKCS#12, JSON, AES-CBC, RSA-2048, SHA-256

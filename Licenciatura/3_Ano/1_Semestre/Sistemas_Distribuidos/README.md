# 🌐 Sistemas Distribuídos

**Ano:** 3º Ano | **Semestre:** 1º Semestre  
**Tecnologias:** Java (OpenJDK), Sockets TCP, Threads, Concorrência e Protocolos Binários

## 📌 Sobre a Cadeira
Unidade curricular dedicada ao estudo de sistemas cujos componentes se encontram distribuídos por computadores em rede, comunicando e coordenando as suas ações através de mensagens. Abrange desde a concorrência ao nível de memória partilhada (threads e exclusão mútua) até à arquitetura de serviços em rede tolerantes a falhas e de alta concorrência.

## 🎯 Principais Tópicos Abordados
* **Concorrência e Sincronização (Memória Partilhada):**
  * Fios de execução (*Threads*) em Java (`Runnable`, `Thread`, `start`, `join`).
  * Condições de Corrida (*Race Conditions*) e secções críticas.
  * Mecanismos de exclusão mútua: *Reentrant Locks* (`lock()`, `unlock()`).
* **Comunicação em Redes (Sistemas Distribuídos):**
  * Arquitetura Cliente-Servidor baseada em **Sockets TCP**.
  * Concorrência no servidor: Atendimento multi-cliente síncrono vs. assíncrono.
  * Desenho e implementação de protocolos de comunicação em formato binário (`DataInputStream` / `DataOutputStream`).
* **Armazenamento Distribuído / Chave-Valor:**
  * Gestão de dados em memória de forma volátil/persistente com acesso remoto.
  * Garantia de atomicidade nas operações de leitura e escrita concorrente.

## 📂 Organização da Pasta
* 📖 **`Teoricas/`:** Apresentações e diapositivos teóricos (12 aulas) cobrindo modelos de concorrência, arquiteturas distribuídas e algoritmos de sincronização.
* 💻 **`Praticas_e_Guioes/`:** Guiões laboratoriais (8 guiões em Java) focados na criação de threads, partilha de estado, resolução de corridas e uso de locks.
* 📑 **`Avaliacoes/`:** Enunciados e resoluções dos 2 testes de avaliação teórica e prática.
* 🛠️ **`Trabalho_Pratico/`:** Projeto desenvolvido em grupo (*Armazenamento de dados em memória com acesso remoto*), contendo o relatório final em PDF, especificações e código-fonte.

## 🏆 Projeto em Destaque: Armazenamento de Chave-Valor em Memória com Acesso Remoto
* **Descrição:** Desenvolvimento de um serviço de armazenamento de dados partilhado em Java, onde múltiplos clientes interagem concorrentemente com um servidor central através de Sockets TCP.
* **Arquitetura & Protocolo:**
  * Servidor multi-threaded capaz de gerir conexões simultâneas de forma eficiente, isolando a escrita em sockets por threads dedicadas para evitar bloqueios (*slow clients*).
  * Protocolo de comunicação baseado em formato binário utilizando streams de dados (`DataInput`/`DataOutput`).
  * Organização estruturada em camadas: Biblioteca cliente independente, lógica de negócio no servidor e interface de testes.
* **Autores do Projeto:** Bernardo Salgado, Luís Baptista e Luís Marques.

## 🛠️ Tecnologias e Ferramentas
* **Linguagem:** Java
* **Redes:** Sockets TCP / IP (`java.net`, `java.io`)
* **Concorrência:** `java.util.concurrent.locks.ReentrantLock`, `java.lang.Thread`
* **IDE:** IntelliJ IDEA / Eclipse

# ⚙️ Sistemas Operativos

**Ano:** 2º Ano | **Semestre:** 2º Semestre  
**Linguagem / Ambiente:** C / POSIX (Linux/Unix)

## 📌 Sobre a Cadeira
Unidade curricular focada na arquitetura, princípios de funcionamento e abstrações fornecidas pelos sistemas operativos modernos. Aborda a gestão eficiente de recursos de hardware (CPU, Memória, I/O e Armazenamento) e a programação concorrente/paralela.

## 🎯 Principais Tópicos Abordados
* **Conceitos Fundamentais:** Chamadas ao sistema (*System Calls*), modo utilizador vs. modo núcleo (*Kernel/User Mode*), interrupções e excepções.
* **Gestão de Processos e Threads:**
  * Estados de um processo, Bloco de Controlo de Processo (PCB) e criação/gestão de processos (`fork`, `exec`, `wait`).
  * Threads vs. Processos e utilização da biblioteca POSIX Threads (`pthreads`).
  * Escalonamento de CPU (*Scheduling*): FCFS, SJF, Round-Robin, Prioridades e Filas Multinível.
* **Sincronização e Concorrência:**
  * Condições de corrida (*Race Conditions*) e secções críticas.
  * Mecanismos de sincronização: Mutexes, Semáforos e Variáveis de Condição.
  * Problemas clássicos (Produtor-Consumidor, Jantar dos Filósofos, Leitores-Escritores) e prevenção de impasses (*Deadlocks*).
* **Gestão de Memória:**
  * Memória virtual, paginação (*Paging*), segmentação e algoritmos de substituição de páginas (FIFO, LRU).
* **Sistemas de Ficheiros e I/O:**
  * Estrutura de diretórios, *Inodes*, descritores de ficheiro e Comunicação Inter-Processos (Pipes, Named Pipes/FIFOs, Shared Memory).

## 📂 Organização da Pasta
* 📖 **`Teoricas/`:** Diapositivos e apontamentos sobre os conceitos teóricos do sistema operativo.
* 💻 **`Praticas/`:** Guiões de exercícios e pequenas implementações em C desenvolvidas durante as aulas.
* 📁 **`Trabalhos/`:** Projetos e trabalhos práticos desenvolvidos no âmbito da unidade curricular.

## 🛠️ Tecnologias e Ferramentas
* **Linguagem:** C (POSIX / C99)
* **Ambiente de Desenvolvimento:** Linux / Bash
* **Ferramentas:** GCC, Make, GDB, Valgrind

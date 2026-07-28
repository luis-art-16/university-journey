#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>


#define FIFO_NAME "myfifo"
#define BUFFER_SIZE 128

int main(argc, char* argv[]) {
    int fd;
    char buffer[BUFFER_SIZE];
    int number, occurrences;
   
    int array[] = {1, 2, 3, 2, 4, 2, 5}; // Exemplo de vetor
    
    int size = sizeof(array) / sizeof(array[0]);

   
    mkfifo(FIFO_NAME, 0666); //Cria o pipe

    while (1) {
       
        // Abre o pipe para leitura
        fd = open(FIFO_NAME, O_RDONLY);
        read(fd, buffer, sizeof(buffer));
        number = atoi(buffer);
        close(fd);

        // Contar ocorrências
        occurrences = 0;
        for (int i = 0; i < size; i++) {
            if (array[i] == number) {
                occurrences++;
            }
        }

        // Envia a contagem de volta ao cliente
        char response[BUFFER_SIZE];
        sprintf(response, "%d", occurrences);
        fd = open(FIFO_NAME, O_WRONLY);
        write(fd, response, strlen(response) + 1);
        close(fd);
    }

    return 0;
}
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>

#define FIFO_NAME "myfifo"
#define BUFFER_SIZE 128

int main() {
    char buffer[BUFFER_SIZE];
    int fd;
    int number;

    // Lê o número a ser pesquisado
    printf("Digite o número a procurar: ");
    scanf("%d", &number);

    // Envia o número para o servidor
    fd = open(FIFO_NAME, O_WRONLY);
    printf(buffer, "%d", number);
    
    write(fd, buffer, strlen(buffer) + 1);
    close(fd);

    // Aguarda a resposta do servidor
    fd = open(FIFO_NAME, O_RDONLY);
    read(fd, buffer, sizeof(buffer));
    
    printf("Número de ocorrências: %s\n", buffer);
    close(fd);

    return 0;
}
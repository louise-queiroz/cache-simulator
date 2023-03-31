#include <stdio.h>

int main() {
    FILE *fp;
    long int buffer;
    int count = 0;

    fp = fopen("bin_100.bin", "rb"); // abre o arquivo binário para leitura

    if (fp == NULL) {
        printf("Erro ao abrir o arquivo.");
        return 1;
    }

    // lê um long int por vez até o fim do arquivo
    while (fread(&buffer, sizeof(long int), 1, fp) == 1) {
        printf("%lu\n", buffer); // exibe o valor lido
        count++;
    }

    fclose(fp); // fecha o arquivo

    printf("Total de elementos lidos: %d\n", count);

    return 0;
}

#include<stdio.h>
#include<stdlib.h>
#include<string.h>

typedef struct carro{
	char matricula[25];
	int ano;
}Carro;

typedef struct no
{
	Carro carro;
	struct no* proximo;
}No;

typedef struct fila
{
	No* cabeca;
	No* cauda;
} Fila;

void printDados(Carro* no)
{
	printf("\nMATRICULA: %s, ANO: %d", no->matricula, no->ano);
}

Fila* create()
{
	Fila *f = (Fila*) malloc(sizeof(Fila));
	f->cabeca = NULL;
	f->cauda = NULL;
	return f;
}

//inserção pela cauda
void enqueue(Fila *fila, Carro carro)
{
	No* novo = (No*)malloc(sizeof(No));
	novo->carro = carro;
	novo->proximo = NULL;
	if (fila->cabeca==NULL)
	{
		fila->cabeca=novo;
		fila->cauda=novo;
	}
	else
	{
		//O "proximo" do úlimo elemento aponta para o "novo"
		fila->cauda->proximo = novo;
		//A nova cauda é o "novo" nó
		fila->cauda = novo;
	}
}

//Remoção pela cabeça (os mais antigos saem primeiro)
Carro* dequeue(Fila *fila)
{
	if(fila->cabeca!=NULL)
	{
		No* aux = fila->cabeca;
		fila->cabeca = aux->proximo;
		Carro *c = (Carro*)malloc(sizeof(Carro));
		*c = aux->carro;
		free(aux);
		aux=NULL;
		return c;		
	}
	return NULL;
}

Carro* peek(Fila *fila)
{
	if (fila->cabeca!=NULL)
	{
		Carro *c = (Carro*)malloc(sizeof(Carro));
		*c = fila->cabeca->carro;
		return c;	
	}
	return NULL;
}

int empty(Fila *fila)
{
	if(fila->cabeca!=NULL)
		return 0;
	return 1;
}

void destroy(Fila **fila)
{
	while(!empty(*fila))
		dequeue(*fila); 
	free(*fila);
	*fila = NULL;
}

Carro novoCarro(char *matricula, int ano)
{
	Carro c = {.ano = ano};
	strcpy(c.matricula, matricula);
	return c;
}

main()
{
	Fila *fila = create();
	enqueue(fila, novoCarro("11-22-33", 1990));
	enqueue(fila, novoCarro("22-33-44", 1950));
	enqueue(fila, novoCarro("22-33-44", 1930));
	printDados(dequeue(fila));
	printDados(dequeue(fila));
	destroy(&fila);
	printDados(peek(fila));
	printDados(peek(fila));
	printDados(peek(fila));
	printDados(peek(fila));
}

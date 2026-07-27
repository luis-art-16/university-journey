#include<stdio.h>
#include<stdlib.h>
#include<string.h>

//Criar uma estrutura Aluno, com número mecanográfico e nome. 
//A estrutura deve ter um apontador “next” para suportar operações 
//com listas ligadas. 

typedef struct aluno{
	int numMec;
	char nome[200];
	struct aluno *next;
}Aluno;

/*
typedef struct No{	
	Aluno aluno;
	struct No* next;
}No;
*/

Aluno* novoAluno(int nummec, char *nome)
{
	Aluno *novo = (Aluno*) malloc(sizeof(Aluno));
	strcpy(novo->nome, nome);
	novo->numMec = nummec;
	novo->next = NULL;
	return novo;
}

void imprimeAluno(Aluno aluno)
{
	printf("-------------------------------------------\n");
	printf("NumMec: %d | Nome: %s\n", aluno.numMec, aluno.nome);
	printf("-------------------------------------------\n");
	
}

void imprimeLista(Aluno **lista){
	if(*lista==NULL)
		return;
	
	Aluno *a =*lista;
	do
	{
		imprimeAluno(*a);
		a=a->next;		
	}while(a!=NULL);
}

void insereNaLista(Aluno **lista, Aluno *novo)
{
	if(*lista==NULL)
	{
		*lista = novo;
	}
	else
	{
		novo->next = *lista;
		*lista = novo;
	}
}

void insereNaLista_FIM(Aluno **lista, Aluno *novo)
{
	if(*lista==NULL)
	{
		*lista = novo;
	}
	else
	{
		Aluno *aux = *lista;
		while(aux->next!=NULL)
		{
			aux = aux->next;
		}
		aux->next = novo;
	}
}

void removePorNumero(Aluno **lista, int num)
{
	if (*lista==NULL)
		return;
	else //AQUI A LISTA NÃO ESTÁ VAZIA....
	{
		Aluno *aux = *lista;
		Aluno *ant = NULL;
		while(aux!=NULL && aux->numMec!=num)
		{
			ant = aux;
			aux = aux->next;
		}
		if(aux == NULL)
		{
			return;
		}
		else if (ant==NULL)
		{
			*lista = aux->next;
		}
		else
		{
			ant->next = aux->next;
		}
		free(aux);
	}
}

main()
{
	Aluno *listaDeAlunos = NULL;
	
	insereNaLista_FIM(&listaDeAlunos, novoAluno(1000, "Frederico Varandas"));
	insereNaLista_FIM(&listaDeAlunos, novoAluno(2000, "Zeca Afonso"));
	insereNaLista_FIM(&listaDeAlunos, novoAluno(3000, "Armando Lopes"));
	
	removePorNumero(&listaDeAlunos, 2000);
	
	imprimeLista(&listaDeAlunos);
}

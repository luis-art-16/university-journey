#include<stdio.h>
#include<string.h>
#include<stdlib.h>

///////////////////////////////////////////////////////////////Estruturas
///////////////////////////////////////////////////////////////Estruturas
///////////////////////////////////////////////////////////////Estruturas
typedef struct dados{
    char nome[100];
    int edicao;
} Livro;

/* definição da lista ligada */
typedef struct node {
    Livro livro;
    struct node* next;
} No;

/* definição da stack */
typedef struct stack {
    No *topo;
} Pilha;
///////////////////////////////////////////////////////////////Estruturas
///////////////////////////////////////////////////////////////Estruturas
///////////////////////////////////////////////////////////////Estruturas

///////////////////////////////////////////////////////////////Funções auxiliares para criar no e imprimir
///////////////////////////////////////////////////////////////Funções auxiliares para criar no e imprimir
///////////////////////////////////////////////////////////////Funções auxiliares para criar no e imprimir
No* criarNo(char *nome_livro, int n_edicao)
{
    Livro l;
    strcpy(l.nome, nome_livro);
    l.edicao = n_edicao;
    No *novo = (No*) malloc(sizeof(No));
    novo->next = NULL;
    novo->livro = l;
    return novo;
}

void imprimeLivro(Livro *livro)
{
    printf("\n------------------------------------\n");
    if (livro != NULL)
        printf("Nome do livro: %s | N Edicao: %d\n", livro->nome, livro->edicao);
    else
        printf("NO NULL\n");
    printf("------------------------------------\n");
}
///////////////////////////////////////////////////////////////Funções auxiliares para criar no e imprimir
///////////////////////////////////////////////////////////////Funções auxiliares para criar no e imprimir
///////////////////////////////////////////////////////////////Funções auxiliares para criar no e imprimir

///////////////////////////////////////////////////////////////Funções da stack (pilha)
///////////////////////////////////////////////////////////////Funções da stack (pilha)
///////////////////////////////////////////////////////////////Funções da stack (pilha)
Pilha* create()
{
    Pilha* nova = (Pilha*) malloc(sizeof(Pilha));
    nova->topo = NULL;
    return nova;
}

int is_empty(Pilha *pilha)
{
    if (pilha->topo==NULL)
        return 1;
        
    return 0;
}

Livro* peek(Pilha* pilha)
{
    Livro *p = NULL;
    if(!is_empty(pilha)) //Se não está vazio???
    {
        p = (Livro*) malloc(sizeof(Livro));
        *p = pilha->topo->livro;
    }
    return p;
}

void push(Pilha *p, No* novo){
    
    if(is_empty(p)) //Se está vazio???
    {
        p->topo = novo;
    }
    else
    {
        novo->next = p->topo;
        p->topo = novo;
    }
    
}

Livro* pop(Pilha *pilha)
{
    Livro *p = NULL;
    if(!is_empty(pilha)) //Se não está vazio???
    {
        p = peek(pilha);
        No* aux_cima = pilha->topo;
        pilha->topo = aux_cima->next;
        free(aux_cima);
        aux_cima = NULL;
    }    
    return p;
}

void destroy(Pilha **pilha)
{
    while(pop(*pilha)!=NULL)
    {
        //Não precisa de estar nada aqui dentro;
    }
    
    free(*pilha);
    *pilha=NULL;
}
///////////////////////////////////////////////////////////////Funções da stack (pilha)
///////////////////////////////////////////////////////////////Funções da stack (pilha)
///////////////////////////////////////////////////////////////Funções da stack (pilha)

int main()
{
    //printf("Welcome to Online IDE!! Happy Coding :)");
    
    Pilha *minhaPilha = create();
    push(minhaPilha, criarNo("Livro ABC", 100));
    push(minhaPilha, criarNo("Livro DEF", 200));
    
    imprimeLivro(pop(minhaPilha));
    imprimeLivro(pop(minhaPilha));
    imprimeLivro(pop(minhaPilha));

    push(minhaPilha, criarNo("Livro ABC", 100));
    push(minhaPilha, criarNo("Livro ABC", 200));
    push(minhaPilha, criarNo("Livro ABC", 300));
    push(minhaPilha, criarNo("Livro ABC", 400));
    push(minhaPilha, criarNo("Livro ABC", 500));
    destroy(&minhaPilha);
    imprimeLivro(peek(minhaPilha));
    
    return 0;
}

#include<stdio.h>
#include"complexidade.h"


void InsertionSort(int vec[], int n)
{
   conta_reset();
   int i, j, x;
   for (i = 1; i < n; i++) {
      x = vec[i];
      conta_maismais();
      for (j = i; j > 0 && x < vec[j-1]; j--)
      {
         vec[j] = vec[j-1];
         conta_maismais();
	  }
      vec[j] = x; 
   }
}

void BubbleSort(int vec[], int n)
{
	conta_reset();
	int troca, i, j, aux;
	for (i = n-1; i > 0; i--) { 
			/* o maior valor entre vec[0] e vec[i] vai para a posição vec[i]*/
	  troca = 0;     
	  conta_maismais();
	  for (j =0 ; j < i; j++)  {
	  	conta_maismais();
	    if (vec[j] > vec[j+1]) {
	      aux = vec[j]; vec[j] = vec[j+1]; vec[j+1] = aux;
	      troca = 1;
	    }
	  }
	  if (!troca) return;
	}
}
  
void QuickSort(int vec[], int a, int b)
{  
  conta_maismais();
  if (a >= b) return;  /* caso básico (tamanho <= 1) */
      int x = vec[(a+b)/2], tmp; 
   int i = a, j = b;
   // passo de partição
      do {
      	conta_maismais();
      	while (vec[i] < x) i++;
      	while (vec[j] > x) j--;
      	if (i > j) break;
      	tmp=vec[i]; vec[i]=vec[j]; vec[j]=tmp;
	i++; j--; /*troca*/
   } while (i <= j);  
   /* passo recursivo */
   QuickSort(vec, a, j);
   QuickSort(vec, i, b);
}


main()
{
	int N = 100; 
	int v[N];
	
	preenche_vetor_random(v, N);
	print_vetor(v, N);
	InsertionSort(v, N);
	print_vetor(v, N);
	conta_print("Contagem Insertion Sort");
	
	preenche_vetor_random(v, N);
	print_vetor(v, N);
	BubbleSort(v, N);
	print_vetor(v, N);
	conta_print("Contagem Bubble Sort");
	
	preenche_vetor_random(v, N);
	print_vetor(v, N);
	conta_reset();
	QuickSort(v, 0, N);
	print_vetor(v, N);
	conta_print("Contagem Bubble Sort");
	
}

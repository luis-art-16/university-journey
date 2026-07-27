#include<stdio.h>

#define N 3
#define M 2

int fatorial(int n)
{
	if (n==0)
		return 1;
	
	return n*fatorial(n-1);
}

main()
{
	
	int m[N][M] = {
		{ 2 ,  3 }, //Linha 0
		{ 34, 2 },//Linha 1 
		{ 2 ,  3 }, //Linha 2
	};
	
	printf("%d", m[0][1]);
	
	int numeroqq = 6;
	printf("---> %d", fatorial(numeroqq));
}

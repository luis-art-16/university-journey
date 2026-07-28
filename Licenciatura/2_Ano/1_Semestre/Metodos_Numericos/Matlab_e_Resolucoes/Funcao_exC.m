A=[15 10 10; 3 4 1; 3 3 8];
b=[20 10 20]';

x=A\b  %Método direto e estável

%Caso seja definida positiva
d1=det(A(1,1))
d2=det(A(1:2, 1:2))
d3=det(A)

C=[0 -0.6667 -0.6667; 0 0.5 0.25; 0 0.0625 0.1562];
norm_C_inf=norm(C, Inf)%norma infinita
norm_C_1=norm(C,1)%norma 1

%Caso não deem a matriz CGS
%D=diag(diag(A));
%L=trill(-A, -1);
%U=tru(-A,1);
%C=inv(D-L)*U
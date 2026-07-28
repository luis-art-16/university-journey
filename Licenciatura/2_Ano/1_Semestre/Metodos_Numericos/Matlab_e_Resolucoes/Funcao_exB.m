op=optimset('TolFun', 1e-2);
x0=[1,1]';
[x,f,exitflag]=fsolve(@fun, x0, op)

function f=fun(x)
f(1)= x(1)^2+x(2)^2-3;
f(2)= sin(x(1))-2*x(2);
end
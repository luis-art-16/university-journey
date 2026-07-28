op=optimset('TolX', 1e-1);
x0=[-1, -0.5]';
[x,f,exitflag]=fzero(@fun, x0, op);
function f=fun(x)
f=exp(2*x)-(1-x^2);
end
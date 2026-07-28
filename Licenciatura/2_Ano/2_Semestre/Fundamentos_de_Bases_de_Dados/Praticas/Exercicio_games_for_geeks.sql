--Exercicio do GamesForGeeks;

-- Q1 -- Quais os jogos para a consola XBOX(cod_jogo e nºexemplar) que, neste momento, se encontram disponíveis para alugar?

SELECT cod_jogo, nexemplar
FROM exemplares e
WHERE consola = "XBX" AND (cod_jogo, nexemplar) NOT IN (SELECT cod_jogo, nexemplar
                                                        FROM alugueres
                                                        WHERE data_entrega IS NULL);

-- (OU)                                                        
                                                                                                                                                                        
SELECT cod_jogo, nexemplar
FROM exemplares e
WHERE consola = "XBX"
EXCEPT
(SELECT cod_jogo, nexemplar
FROM alugueres
WHERE data_entrega IS NULL);

-- Q2 -- Quais os clientes(nºcliente e nome) que nunca alugaram jogos para a PS3?

SELECT ncliente, nome
FROM clientes
WHERE ncliente NOT IN (SELECT a.ncliente
                       FROM alugueres a, exemplares e
                       WHERE consola = "PS3" AND a.cod_jogo = e.cod_jogo AND a.nexemplar = e.nexemplar);
                     
-- Q3 -- Quais os jogos(cod_jogo e títul0) existentes na empresa para as consolas PS3 e PS4?                     

SELECT cod_jogo, titulo
FROM jogos
WHERE cod_jogo in (SELECT cod_jogo FROM exemplares WHERE consola = "PS3")
      AND
      cod_jogo in (SELECT cod_jogo FROM exemplares WHERE consola = "PS4");
      
-- Q4 -- Relativamente a cada aluguer que terminou em multa, identificar qual o cliente envolvivod(nºcliente e nome), 
      -- qual o valor da multa paga, e de que jogo(título) se tratava

SELECT c.ncliente, c.nome, a.multa, j.titulo
FROM alugueres a, jogos j, clientes c  
WHERE a.multa > 0 AND a.ncliente = c.ncliente AND a.cod_jogo = j.cod_jogo;

-- Q5 -- Listar os jogos com exemplares para a PS4(cod_jogo, título, número de exemplares)

SELECT e.cod_jogo, j.titulo, COUNT(*) AS Exemplares
FROM exemplares e, jogos j
WHERE e.consola = "PS4" AND e.cod_jogo = j.cod_jogo
GROUP BY e.cod_jogo;

-- Q6 -- Relativamente a cada jogo(cod_jogo e título), listar o número de exemplares existentes para as diversas consolas

SELECT cod_jogo, titulo, (SELECT COUNT(*) FROM exemplares e WHERE e.consola = "PS3" AND e.cod_jogo = j.cod_jogo) as PS3,
                         (SELECT COUNT(*) FROM exemplares e WHERE e.consola = "PS4" AND e.cod_jogo = j.cod_jogo) as PS4,
                         (SELECT COUNT(*) FROM exemplares e WHERE e.consola = "XBX" AND e.cod_jogo = j.cod_jogo) as XBOX,
                         (SELECT COUNT(*) FROM exemplares e WHERE e.consola = "NDS" AND e.cod_jogo = j.cod_jogo) as NINTENDO
FROM jogos j

-- Q7 -- Qual o maior valor de multa alguma vez ocorrido? Qual o cliente(nºcliente e nome) e jogo(cod_jogo e título) envolvidos?

SELECT c.ncliente, c.nome, a.multa, j.titulo
FROM alugueres a, jogos j, clientes c  
WHERE a.multa = (SELECT MAX(multa) FROM alugueres) AND a.ncliente = c.ncliente AND a.cod_jogo = j.cod_jogo;

-- Q8 -- Listar, por ordem ascendente de nome de cliente, os títulos dos jogos que ainda não alugou

SELECT nome, titulo
FROM clientes, jogos
WHERE (ncliente, cod_jogo) NOT IN (SELECT ncliente, cod_jogo
                                   FROM alugueres)
ORDER BY nome ASC, titulo DESC;

-- Q9 -- Quais os clientes(nºcliente e nome) que já alugaram todos os jogos existentes para a consola Nintendo?

SELECT *
FROM clientes c1
WHERE NOT EXISTS (SELECT *
                  FROM jogos j
                  WHERE cod_jogo IN (SELECT cod_jogo FROM exemplares WHERE consola = "NDS") AND
                        NOT EXISTS (SELECT *
                                    FROM alugueres a
                                    WHERE a.ncliente = c1.ncliente AND a.cod_jogo = j.cod_jogo));

                  
SELECT * FROM alugueres;


--Recorrendo a mecanismos do tipo view, resolva as seguintes questões:
-- Q10 -- Qual o cliente(nºcliente e nome) com maior número de alugueres terminados em multa até ao momento?

CREATE multas_por_cliente_A100457 (cliente, num_multas)
AS SELECT ncliente, count (*)
    FROM alugueres
    WHERE multa > 0
    GROUP BY ncliente;
    
DROP multas_por_cliente

SELECT m.cliente, c.nome
FROM multas_por_cliente m, clientes c
WHERE num_multas = (SELECT MAX(num_multas) FROM multas_por cliente)
    AND c.ncliente = m.cliente;

-- Q11 -- Listar os jogos por ordem decrescente de rentabilidade(título e lucro até ao momento)

create view investimento_por_jogo (jogo, investimento)
as select num_jogo, sum(preco_compra)
from exemplares
group by num_jogo;


create view rendimento_por_jogo (jogo, investimento)
as select num_jogo, sum(preco + ifnull(multa_preco,0))
from alugueres
group by num_jogo;



create view lucro_por_jogo (jogo, lucro)
as select ipj.jogo,(ifnull(rpj.investimento,0) - ipj.investimento)
from investimento_por_jogo ipj left join rendimento_por_jogo rpj
on ipj.jogo = rpj.jogo;

--outra maneira para o view anterior

create view lucro_por_jogo_portavel(jogo,lucro)
as select ipj.jogo, (se_for_nulo(rpj.rendimento,o) - ipj.investimento)
from investimento_por_jogo ipj left join rendimento_por_jogo
on ipj.jogo = rpj.jogo;

create function se_for_nulo ( valor real, result real)
returns real
begin

if (valor is null) then
    return (result);
else
    return(valor);
 end if;
 
 end;
 
 
 select se_for_nulo(123, 0)
 
 --------------------------------------------------------------


select lpj.jogo, j.titulo, lpj.lucro
from lucro_por_jogo lpj, jogos j
where lpj.jogo = j.cod_jogo

select * from rendimento_por_jogo
select * from investimento_por_jogo
select * from lucro_por_jogo

-- Armazenamento de código na base de dados

-- Q1.AC -- Desenvolver uma função "multa_a_pagar" que, dado um jogo que foi alugado, juntamente com o número de dias de atraso,
         -- retorna o correspondente valor da multa a pagar.

CREATE FUNCTION multa_a_pagar_A100457(jogo CHAR(4), dias INT)
RETURNS DECIMAL(5,2)
BEGIN

SELECT * FROM clientes;

-- Q2.AC -- Desenvolver uma função "disponiveis" que, dada a identificação de um jogo e o tipo de consola, retorne o número
         -- de exemplares que neste momento não se encontram alugados

CREATE FUNCTION consola_A100457(jogo CHAR(4), exemplar INT)
RETURNS CHAR(3)
BEGIN
    DECLARE tipo CHAR(3);
    
    SELECT consola
    INTO tipo
    FROM exemplares
    WHERE cod_jogo = jogo AND nexemplar = exemplar;
    
    RETURN(tipo);

END;

CREATE FUNCTION disponiveis_A100457(jogo CHAR(4), tipo CHAR(3))
RETURNS INT
BEGIN
    DECLARE adquiridos, alugados INT;
    
    SELECT COUNT(*)
    INTO adquiridos
    FROM exemplares
    WHERE cod_jogo = jogo AND consola = tipo;
    
    SELECT COUNT(*)
    INTO alugados
    FROM alugueres
    WHERE data_entrega IS NULL AND cod_jogo = jogo AND consola_A100457(cod_jogo, nexemplar) = tipo;
    
    RETURN(adquiridos - alugados);
    
END;

SELECT consola_A100457("1",1)
SELECT disponiveis_A100457("1","PS4")
SELECT titulo, disponiveis_A100457(cod_jogo,"PS3") AS PS3,
               disponiveis_A100457(cod_jogo,"PS4") AS PS4,
               disponiveis_A100457(cod_jogo,"XBX") AS XBOX,
               disponiveis_A100457(cod_jogo,"NDS") AS Nintendo
FROM jogos
               



create function cliente_existe_A100457(cliente int)
returns bool
begin
    declare name char(50);
    
    select nome
    into name
    from clientes
    where ncliente = cliente;
    
    if (name is null) then
        return(false);
    else
        return(true);
    end if;
    
end;

create function exemplar_esta_disponivel_A100457 (jogo char(4), exemplar int)
returns bool
begin
    declare cons char(3);
    declare aluguer int;
    
    select consola
    into cons
    from exemplares
    where cod_jogo = jogo and nexemplar = exemplar;
    
    select naluguer
    into aluguer
    from alugueres
    where cod_jogo = jogo and nexemplar = exemplar and data_entrega is null;
    
    if (cons is not null) and (aluguer is not null)
        return(true);
    else
        return(false);
    end if;

end;

 -- Q3. AC -- Desenvolver um procedimento "abrir_aluguer" com um número mínimo de parâmetros de entrada.
           -- Este procedimento deverá ser invocado sempre que se quiser iniciar um novo aluguer.
 
create procedure abrir_aluguer_A100457(in cliente int, jogo char(4), exemplar int)
begin
    declare price dec(2,1);
    
    if (cliente_existe_A100457(cliente) and exemplar_esta_disponivel_A100457(jogo, exemplar) then
    
        select preco_aluguer
        into price
        from jogos
        where cod_jogo = jogo;
    
        insert into alugueres (ncliente, cod_jogo, nexemplar, data_aluguer, preco)
            values(cliente, jogo, exemplar, curdate(), price);
        commit;
    end if;
    
end;

desc clientes
desc exemplares
call GamesForGeeks.abrir_aluguer_A100457(10, "1", 2)

 -- Q4. AC -- Desenvolver um procedimento "fechar_aluguer" com um número mínimo de parâmetros de entrada.
           -- Este procedimento deverá ser invocado sempre que se quiser terminar um novo aluguer.
           
create procedure fechar_aluguer_A100457(in aluguer int)
begin
    declare jogo char(4);
    declare dias int;
    declare data date;
    
    if (aluguer_aberto_A100457(aluguer)) then 
    
        select cod_jogo, data_aluguer
        into jogo, data
        from alugueres
        where naluguer = aluguer;
        
        set dias = to_days(curdate()) - to_days(data) -1;
        
        if (dias < 0) then
            set dias = 0;
            end if;
        
        update alugueres
            set data_entrega = curdate(),
                multa = multa_a_pagar_A100457(jogo, dias)
        where naluguer = aluguer
        commit;
    end if;
end;

drop aluguer_aberto_A100457 if exists

create function aluguer_aberto_A100457 (aluguer int)
returns bool
begin
    declare data date;
    declare cliente int;
    
    select data_entrega, ncliente
    into data, cliente
    from alugueres
    where naluguer = aluguer;
    
    if (data is null and cliente is not null) then
        return(true);
    else  
        return(false);
    end if
end;

create function cliente_existe_A100457(cliente int)
returns bool
begin
    declare name char(50)
    select nome
    into name
    from clientes
    where nclientes = cliente
    
    if (name is null) then
        return (false);
    else
        return (true);
    end if;
    
end;


-- Q5. AC -- Desenvolver um trigger que implemente a seguinte regra de negócio " para todos os clientes com mais de 3 alugueres
          -- terminados em multa, quaisquer novos alugueres verão o seu preço agravado num valor correspondente ao jogo mais caro

create trigger GamesForGeeks.castigo_A100457
before insert on alugueres
for each row
begin
    declare multas int;
    
    select count(*)
    into multas
    from alugueres
    where ncliente = new.nciente;
    
    if (multas > 1) then
        set new.preco = new.preco + (select max(preco_aluguer) from jogos);
    end if;
end;



desc alugueres
select to_days(curdate())
call GamesForGeeks.fechar_aluguer_A100457(3)
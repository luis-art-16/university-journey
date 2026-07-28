

drop table departamentos;

CREATE TABLE departamentos (
	cod_dep	int primary key,
	designacao char(10) not null,
	endereco varchar(100)
	);
    
INSERT INTO departamentos
	values (1, "Producao", "Guimaraes"),
		   (2, "Recursos ", "Guimaraes");


drop table if exists funcionarios;

CREATE TABLE funcionarios (
    func            int primary key auto_increment,
    nome            varchar(100) not null,
    data_nasc       date default "2020-01-01",
    salario         decimal (6,1),
    dep             int,
    
    constraint salario_minimo check (salario > 750),
    
    foreign key (dep) 
    references departamentos(cod_dep)
    on update cascade
    on delete restrict
);


-- Inserts
INSERT INTO departamentos (designacao, endereco)
	values ("Informática", "Porto");
           
INSERT INTO funcionarios (nome, salario, dep)
	values ("Alberto", 1500, 1);

COMMIT;
           
SELECT * FROM departamentos;
SELECT * FROM funcionarios;



-- Desenvolver:



-- C1 -- Uma stored function "total_dispendido" que, dado um funcionário(nºfunc), 
      -- forneça o valor total já dispendsido pela empresa em compras, para esse funcionário.

CREATE FUNCTION total_dispendido(f_n_func INT)
RETURNS FLOAT
BEGIN

	DECLARE total FLOAT;
		SELECT SUM(Precofinal(preco, quantidade))
    FROM encomenda
    WHERE n_encomenda
			SELECT n_encomenda
			FROM aprovacao
			WHERE n_pedido IN (SELECT n_pedido
							  FROM pedido
							  WHERE n_funcionario = f_n_func);

	RETURN total
   
	
END

CREATE FUNCTION PrecoFinal (f_preco FLOAT, f_quantidade INT)
RETURNS precoFinal FLOAT
BEGIN

	SET precoFinal = f_preco * f_quantidade
    
    RETURN precoFinal
    
END


-- C2 -- Um stored procedure "adicionar_pedido", com um número mínimo de parâmetros, 
      -- que permita adicionar um pedido aprovado a uma encomenda ainda aberta( ou seja, ainda não concluida)
       

CREATE PROCEDURE adicionar_pedido (p_n_pedido INT, p_n_ecomenda INT)

BEGIN

    DECLARE p_n_pedido INT(3); 
    DECLARE p_n_ecomenda INT(3);
     
    DECLARE p_quant INT (3);
    DECLARE p_conclusao VARCHAR (10); 
    DECLARE p_equant INT(3);
    DECLARE p_nomef VARCHAR(50); 
    DECLARE p_preco FLOAT(2,2); 
    DECLARE p_tipo_produto VARCHAR(15); 
    DECLARE p_mensagem VARCHAR(50); 
        
    SELECT quant INTO p_quant
    FROM pedido
    WHERE n_pedido = p_n_pedido;
    
    SELECT nomef INTO p_nomef
    AND SELECT preco INTO p_preco
    AND SELECT conclusao INTO p_conclusao
    AND SELECT quantidade INTO p_equant
    AND SELECT tipo_produto INTO p_tipo_produto
    AND SELECT mensagem INTO p_mensagem
    FROM ecomenda
    WHERE n_ecomenda = p_n_ecomenda;
 
    SET p_quant = SUM (p_quant+p_equant)
    
    IF conclusao = "aberto" THEN
    
        INSERT INTO ecomenda (n_ecomenda,nomef,preco,conclusao,quantidade,tipo_produto,mensagem)
        VALUES (p_n_ecomenda,p_nomef,p_preco,p_conclusao,p_quant,p_tipo_produto,p_mensagem);
        
    ELSE
    
        SET MESSAGE_TEXT = 'NÃ£o Ã© possÃ­vel adicionar pedidos a uma encomenda fechada.';
        
    END IF;
    
 END


-- D1 -- Listar os funcionários (nºfunc e nome) por ordem decrescente de valor despendido em compras até ao momento


SELECT n_func, nome
FROM funcionarios
JOIN encomendas ON funcionarios.n_func = encomendas.n_func
GROUP BY funcionarios.n_func, funcionarios.nome
ORDER BY SUM(encomendas.preco) DESC;

-- D2 -- Quais os artigos(descrição e quantidade) requesitados pelo funcionário Nº1234 durante o mês de 
      -- Dezembro de 2022, já aprovados mas ainda não entregues?

SELECT tipo_produto, quantidade FROM encomendas
JOIN aprovacao ON encomendas.n_encomenda = aprovacao.n_encomenda
WHERE funcionarios.n_func = 1234 AND decisao IS NULL AND MONTH = 12 AND YEAR = 2022;

-- D3 -- Quais os fornecedores(designação) que já fizeram entregas mais de 30 dias após a realização
      -- das respetivas encomendas? Quais os artigos encomendados(descrição) e respetivas quantidades?

SELECT nomef, tipo_material
FROM encomendas, pedidos
WHERE DATEDIFF(encomendas.data_e - encomendas.data_p > 30);




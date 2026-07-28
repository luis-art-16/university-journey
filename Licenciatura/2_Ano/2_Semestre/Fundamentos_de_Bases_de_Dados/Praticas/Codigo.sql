-- A1015419 - Luis Baptista

 -- C

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


-- D 
       

CREATE PROCEDURE adicionar_pedido (p_n_pedido INT, p_n_ecomenda INT)

BEGIN

    DECLARE p_n_pedido INT(3); 
    DECLARE p_n_encomenda INT(3);
     
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
    
        SET MESSAGE_TEXT = 'Nao e possivel adicionar pedidos a uma encomenda fechada.';
        
    END IF;
    
 END




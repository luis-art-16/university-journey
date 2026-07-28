Considerando o seguinte esquema de uma base de dados relacional: 

   Sócios (nºsócio, nome, morada, telefone, BI, Data_Nasc, Data_Insc)
   Filmes (cod_filme, título, duração) 
   Modalidades (modalid, preço, multa_diária) 
   Cópias (cod_filme, nºcópia, formato, data_aquisição, preço) 
   Alugueres (nºaluguer, nºsócio, cod_filme, nºcópia, modalid, data_aluguer, data_entrega, 
   preço, multa) 
  
  Sendo que: 
              Se (multa = 0) então (o aluguer terminou sem multa) 
              Se (multa > 0) então (o aluguer terminou com multa)
              Se (multa é null) então (o aluguer ainda não terminou) 

                               
                                Responder às seguintes questões utilizando a linguagem SQL: 

-- 1 –- Quais as cassetes (cod_filme e nºcópia) que, neste momento, não se encontram alugadas?

SELECT c.cod_filme, c.nºcópia
FROM Cópias c
WHERE NOT EXISTS (
    SELECT 1
    FROM Alugueres a
    WHERE c.cod_filme = a.cod_filme AND c.nºcópia = a.nºcópia AND a.data_entrega IS NULL
);

-- 2 –- Quais os sócios (nºsócio e nome) que nunca alugaram DVDs?

SELECT s.nºsócio, s.nome
FROM Sócios s
WHERE NOT EXISTS (
    SELECT 1
    FROM Alugueres a
    WHERE s.nºsócio = a.nºsócio
);

3 – Quais os filmes (cod_filme e título) que existem no clube em formato cassete e DVD? 

SELECT c1.cod_filme, c1.título
FROM Cópias c1
JOIN Cópias c2 ON c1.cod_filme = c2.cod_filme AND c1.formato = 'Cassete' AND c2.formato = 'DVD'
WHERE NOT EXISTS (
    SELECT 1
    FROM Cópias c3
    WHERE c1.cod_filme = c3.cod_filme AND (c3.formato = 'Cassete' OR c3.formato = 'DVD')
    HAVING COUNT(DISTINCT c3.formato) = 1
);


4 – Relativamente a cada aluguer que terminou em multa, identificar qual o sócio envolvido 
(nºsócio e nome), qual o valor da multa paga, e de que filme (título) se tratava. 

SELECT s.nºsócio, s.nome, a.multa, f.título
FROM Sócios s
JOIN Alugueres a ON s.nºsócio = a.nºsócio
JOIN Cópias c ON a.cod_filme = c.cod_filme AND a.nºcópia = c.nºcópia
JOIN Filmes f ON c.cod_filme = f.cod_filme
WHERE a.multa > 0;


5 – Quais os sócios (nºsócio e nome) que já efectuaram alugueres em todas as modalidades 
existentes?

SELECT s.nºsócio, s.nome
FROM Sócios s
WHERE NOT EXISTS (
    SELECT 1
    FROM Modalidades m
    WHERE NOT EXISTS (
        SELECT 1
        FROM Alugueres a
        WHERE s.nºsócio = a.nºsócio AND a.modalid = m.modalid
    )
);


6 – Listar, para cada filme (cod_filme, título) o número de cassetes existentes no clube. 

SELECT c.cod_filme, c.título, COUNT(*) AS num_cassetes
FROM Filmes f
JOIN Cópias c ON f.cod_filme = c.cod_filme
WHERE c.formato = 'Cassete'
GROUP BY c.cod_filme, c.título;


7 – Qual o maior valor de multa alguma vez ocorrido? Qual o sócio (nºsócio e nome) e filme 
(cod_filme e título) envolvidos? 

SELECT MAX(a.multa) AS maior_multa,
       s.nºsócio, s.nome,
       c.cod_filme, f.título
FROM Sócios s
JOIN Alugueres a ON s.nºsócio = a.nºsócio
JOIN Cópias c ON a.cod_filme = c.cod_filme AND a.nºcópia = c.nºcópia
JOIN Filmes f ON c.cod_filme = f.cod_filme
GROUP BY s.nºsócio, s.nome, c.cod_filme, f.título
HAVING MAX(a.multa) = (
    SELECT MAX(a.multa)
    FROM Sócios s
    JOIN Alugueres a ON s.nºsócio = a.nºsócio
    JOIN Cópias c ON a.cod_filme = c.cod_filme AND a.nºcópia = c.nºcópia
    JOIN Filmes f ON c.cod_filme = f.cod_filme
);


Recorrendo a mecanismos do tipo view, resolva as seguintes questões: 
1) Qual o sócio (nºsócio e nome) com maior número de alugueres terminados em multa até ao 
momento?

CREATE VIEW socio_mais_multas AS
SELECT s.nºsócio, s.nome, COUNT(a.nºsócio) AS num_multas
FROM Sócios s
JOIN Alugueres a ON s.nºsócio = a.nºsócio
WHERE a.multa > 0
GROUP BY s.nºsócio, s.nome
ORDER BY num_multas DESC
LIMIT 1;

2) Qual o filme (título) mais rentável do vídeo-clube?

CREATE VIEW filme_mais_rentavel AS
SELECT f.título, SUM(a.valor_pago) AS receita_total
FROM Filmes f
JOIN Cópias c ON f.cod_filme = c.cod_filme
JOIN Alugueres a ON c.cod_filme = a.cod_filme AND c.nºcópia = a.nºcópia
GROUP BY f.título
ORDER BY receita_total DESC
LIMIT 1;


1) Desenvolver uma função “exemplares_dentro” que, dada a identificação de um filme 
(cod_filme), retorne o número de exemplares (de todos os tipos) que neste momento não se 
encontram alugados.


CREATE FUNCTION exemplares_dentro(cod_filme INT)
RETURNS INT
BEGIN
  DECLARE num_exemplares_totais INT;
  DECLARE num_exemplares_alugados INT;

  -- Obter o número total de exemplares do filme (todos os tipos)
  SELECT COUNT(*) INTO num_exemplares_totais
  FROM Cópias c
  WHERE c.cod_filme = cod_filme;

  -- Obter o número de exemplares alugados do filme (todos os tipos)
  SELECT COUNT(*) INTO num_exemplares_alugados
  FROM Cópias c
  JOIN Alugueres a ON c.cod_filme = a.cod_filme AND c.nºcópia = a.nºcópia
  WHERE a.data_devolução IS NULL;

  -- Calcular e retornar o número de exemplares disponíveis
  RETURN num_exemplares_totais - num_exemplares_alugados;
END;


2) Desenvolver uma função “multa_a_pagar” que dada a modalidade em que um aluguer foi 
realizado, juntamente com o número de dias em atraso, retorna o correspondente valor da 
multa a pagar. 

CREATE FUNCTION multa_a_pagar(modalidade VARCHAR(20), dias_atraso INT)
RETURNS DECIMAL(5,2)
BEGIN
  DECLARE multa_base DECIMAL(5,2);
  DECLARE fator_multiplicador DECIMAL(2,1);

  -- Obter multa base e fator multiplicador para a modalidade
  IF modalidade = 'Normal' THEN
    SET multa_base = 1.50, fator_multiplicador = 1.0;
  ELSEIF modalidade = 'Infantil' THEN
    SET multa_base = 1.00, fator_multiplicador = 0.5;
  ELSEIF modalidade = 'Clássico' THEN
    SET multa_base = 2.00, fator_multiplicador = 1.2;
  ELSE
    -- Se a modalidade não for válida, retorna um valor negativo indicando erro
    RETURN -1;
  END IF;

  -- Calcular a multa total
  RETURN multa_base + (dias_atraso * fator_multiplicador);
END;


3) Desenvolver um procedimento “abrir_aluguer” com um número mínimo de parâmetros de 
entrada. Este procedimento deverá ser invocado sempre que se quiser iniciar um novo 
aluguer. 

CREATE PROCEDURE abrir_aluguer(
  cod_socio INT,
  cod_filme INT,
  cod_copia INT,
  data_aluguer DATE
)
BEGIN
  DECLARE aluguer_id INT;

  -- Inserir novo registo na tabela Alugueres
  INSERT INTO Alugueres (cod_socio, cod_filme, cod_copia, data_aluguer)
  VALUES (cod_socio, cod_filme, cod_copia, data_aluguer);

  -- Obter o ID do novo aluguer
  SELECT LAST_INSERT_ID() INTO aluguer_id;

  -- Mensagem de sucesso
  IF aluguer_id IS NOT NULL THEN
    SELECT CONCAT('Aluguer #', aluguer_id, ' aberto com sucesso!');
  ELSE
    SELECT 'Erro ao abrir aluguer.';
  END IF;
END;

4) Desenvolver um procedimento “fechar_aluguer” com um número mínimo de parâmetros de 
entrada. Este procedimento deverá ser invocado sempre que se quiser terminar um novo 
aluguer.

CREATE PROCEDURE fechar_aluguer(
  cod_aluguer INT,
  data_devolucao DATE,
  multa DECIMAL(5,2) DEFAULT 0.00
)
BEGIN
  DECLARE data_aluguer DATE;
  DECLARE valor_pago DECIMAL(5,2) DEFAULT 0.00;

  -- Obter data de aluguer e valor pago do aluguer
  SELECT data_aluguer, valor_pago
  FROM Alugueres a
  WHERE a.cod_aluguer = cod_aluguer;

  -- Se o aluguer já estiver fechado, retornar mensagem de erro
  IF data_devolucao IS NOT NULL THEN
    SELECT 'Aluguer já fechado.';
    RETURN;
  END IF;

  -- Atualizar a data de devolução e multa
  UPDATE Alugueres a
  SET data_devolucao = data_devolucao, multa = multa
  WHERE a.cod_aluguer = cod_aluguer;

  -- Calcular valor a pagar (se não estiver definido)
  IF valor_pago = 0.00 THEN
    SELECT SUM(preco_dia * DATEDIFF(data_devolucao, data_aluguer))
    INTO valor_pago
    FROM Precos p
    JOIN Cópias c ON p.cod_filme = c.cod_filme AND p.tipo_copia = c.tipo_copia
    JOIN Alugueres a ON c.cod_copia = a.cod_copia AND a.cod_aluguer = cod_aluguer;
  END IF;

  -- Atualizar valor pago
  UPDATE Alugueres a
  SET valor_pago = valor_pago + multa
  WHERE a.cod_aluguer = cod_aluguer;

  -- Mensagem de sucesso
  SELECT CONCAT('Aluguer #', cod_aluguer, ' fechado com sucesso!');
END;


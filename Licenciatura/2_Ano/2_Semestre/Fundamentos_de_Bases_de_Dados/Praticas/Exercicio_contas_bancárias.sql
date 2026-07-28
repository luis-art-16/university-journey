-- Contas Bancárias

-- 1 -- listar as várias contas bancárias por ordem decrescente do respetivo saldo disponível

SELECT *
FROM CCredito.contas_bancarias
ORDER BY saldo_dispon DESC;

-- 2 -- Quantos cartões de crédito existem sobre a conta nºconta=12345?

SELECT COUNT(*)
FROM CCredito.cartoes_credito
WHERE CCredito.cartoes_credito.n_conta = "12345";

-- 3 -- Quais os clientes para os quais não foi registado o respetivo NºContribuinte?

SELECT *
FROM CCredito.clientes
WHERE CCredito.clientes.n_contribuinte IS NULL;

-- 4 -- Para cada conta bancária, calcular o valor em crédito de todos os cartões que lhes estão associados.

SELECT SUM(CCredito.cartoes_credito.valor_em_credito), CCredito.cartoes_credito.n_conta
FROM CCredito.cartoes_credito
GROUP BY CCredito.cartoes_credito.n_conta;

-- 5 -- Quais as contas bancárias(nºconta) a que não estão associados quaisquer cartões de crédito?

SELECT CCredito.contas_bancarias.n_conta 
FROM CCredito.contas_bancarias
EXCEPT;
SELECT CCredito.cartoes_credito.n_conta 
FROM CCredito.cartoes_credito;

-- 6 -- Quais os cartões de crédito cujo valor em crédito ultrapassou o saldo disponivel das contas que lhe estão associadas?

SELECT CCredito.cartoes_credito.n_cartao
FROM CCredito.cartoes_credito, CCredito.contas_bancarias
WHERE CCredito.cartoes_credito.n_conta = CCredito.contas_bancarias.n_conta AND CCredito.cartoes_credito.valor_em_credito > CCredito.contas_bancarias.saldo_dispon;

-- 7 -- Para cada conta com saldo contabilistico inferior a 1000, listar os vários cartões de crédito que lhe estão associados.

SELECT cartoes_credito.*
FROM cartoes_credito, contas_bancarias
WHERE cartoes_credito.n_conta = contas_bancarias.n_conta AND contas_bancarias.saldo_contab < 1000;

-- 8 -- Quais as contas cujo saldo disponivel é inferior ao total de valor em crédito de todos os cartões emitidos sobre cada uma dessas contas?

SELECT cb.n_conta
FROM contas_bancarias cb
WHERE (SELECT SUM(valor_em_credito)
FROM cartoes_credito cc
WHERE cc.n_conta = cb.n_conta)> ALL
(SELECT saldo_dispon
FROM contas_bancarias)

-- 9 -- Quais os clientes(nºcliente e nome) que, apesar de possuírem contas no banco, não detêm qualquer cartão de crédito?

SELECT n_cliente, nome
FROM clientes
WHERE n_cliente IN (SELECT n_cliente
					FROM titularidades
                    EXCEPT
                    SELECT n_cliente
                    FROM cartoes_credito)
                    
-- 10 -- Quais os clientes(nºcliente e nome) que, apesar de não possuirem qualquer conta no banco, são detentores de, pelo menos, um cartão de crédito?

SELECT n_cliente, nome
FROM clientes
EXCEPT
SELECT n_cliente
FROM titularidades
WHERE EXISTS (SELECT n_cliente
			  FROM cartoes_credito)
   

-- 11 -- Quais os lientes(nºcliente e nome) que possuem cartão de crédito para cada conta de que são titulares?







-- 12 -- Quais os clientes(nºcliente e nome) titulares de pelo menos uma conta bancária, que são detentores de pelo menos um cartão de crédito

SELECT n_cliente, nome
FROM clientes
WHERE n_cliente IN (SELECT *
					FROM titularidades
                    WHERE n_conta IN (SELECT *
									  FROM cartoes_credito));

-- 13 -- Quais os clientes nºcliente e nome) titulares de contas para as quais foram emitidos cartões de crédito de todos os tipos existentes?

SELECT *
FROM clientes c
WHERE NOT EXISTS (SELECT *
                  FROM tipos_cartao t
                  WHERE tipo NOT EXISTS (SELECT *
										 FROM cartoes_credito cc
										 WHERE cc.n_cliente = c.n_cliente AND cc.tipo = t.cod_jogo));
                                         
SELECT n_cliente, nome
FROM clientes CL
WHERE n_cliente IN (SELECT tt.n_cliente
					FROM titularidades tt
                    WHERE NOT EXISTS (SELECT *
									  FROM tipos_cartao TC
                                      WHERE NOT EXISTS (SELECT *
														FROM cartoes_credito CC
                                                        WHERE CC.tipo = TC.tipo
                                                        AND
                                                        CC.n_conta = tt.n_conta)));
                                                        

create table Cartoes_Credito (
	ncartao char(30),
	tipo char(5),
	ncliente char(30),
	nconta char(30),
	data_emissao date,
	prazo_validade date,
	valor_em_credito decimal,
	
	Primary key (ncartao)
	
	
);

create table Tipos_cartao (
	tipo char(5),
	condicoes_pagamento char(20),
	limite_credito decimal,

	Primary key (tipo)
	
);

create table Contas_bancarias (
	nconta char(30),
	ncliente char(30),
	saldo_contab decimal,
	saldo_dispon decimal,

	Primary key (nconta)
	
	
);

create table Clientes (
	ncliente char(30),
	nome char(100),
	morada char(100),
	telefone char(9),
	BIdentidade char(11),
	NContribuinte char(11),

	Primary key (ncliente),
	
	unique (BIdentidade),
	unique (NContribuinte)
	
);

insert into Clientes
	values 	(01, 'Rui Cadete', 'Urgeses', 913815870, 11680873, 1256789),
			(02, 'Anselmo Abilio', 'Carvalhos', 966779423, 11680950, 1256783),
			(03, 'Filipe Fernandes', 'Creixomil', 966495629, 11680873, 1256784),
			(04, 'Rui das Aves', 'Aves', 916782095, 11450546, 125623),
			(05, 'bate codigo', 'Famalicao', 913813670, 11680563, 1245789),		
			(06, 'fifas', 'Lousada', 984576235, 12345678, 124346754);


------------------------------------------------------------------------------------------------------------

Instruções apresentadas recorrendo ao exemplo:
	
	Clientes (cod_cliente, cliente, profissão, localidade) 
	Agências (cod_agência, agência, localidade) 
	Contas (num_conta, tipo_conta, cod_agência, cod_cliente, saldo)
	Empréstimos (num_empréstimo, cod_agência, cod_cliente, valor) 

Quais os clientes (cod_cliente e cliente) deste banco?
	SELECT cod_cliente, cliente
	FROM Clientes

Quais os clientes que residem em Braga?
	SELECT *
	FROM Clientes
	WHERE localidade = 'Braga'

Quais os clientes (cod_cliente) com contas na agência cod_agencia=’123’? 

	SELECT DISTINCT cod_cliente
	FROM Contas
	WHERE cod_agencia = '123'

Quais os clientes que residem na mesma localidade das agências onde possuem contas? 
	SELECT Clientes.*
	FROM Clientes, Contas, Agencias
	WHERE Clientes.localidade = Agencias.localidade
     		AND Clientes.cod_cliente = Contas.cod_cliente
     		AND Contas.cod_agencia = Agencias.cod_agencia

É necessário o nome das tabelas para evitar ambiguidades.

Quais os clientes com empréstimos de valor superior a 500.000? 

	SELECT Clientes.*
	FROM Clientes, Emprestimos
	WHERE Clientes.cod_cliente = Emprestimos.cod_cliente
		AND Emprestimos.valor > 500000

	Utilizando sinónimos (aliases): 

	SELECT C.*
	FROM Clientes C, Emprestimos E
	WHERE C.cod_cliente = E.cod_cliente
		AND E.valor > 500000

Quais os nomes dos clientes com a mesma profissão que o cliente com cod_cliente = ‘1234’? 
	SELECT C1.cliente
	FROM Clientes C1, Clientes C2
	WHERE C1.profissao = C2.profissao
		AND C2.cod_cliente = '1234' 

Listar as contas (num_conta, saldo) da agência cujo cod_agencia = ‘123’, por ordem decrescente do seu valor de saldo. 
	SELECT num_conta, saldo
	FROM Contas
	WHERE cod_agencia = '123'
	ORDER BY saldo DESC 

Quantas contas existem em todas as agências do banco?
	SELECT COUNT(*)
	FROM Contas 

	Existem outras funções de agregação para o cálculo do máximo, do mínimo, da média e do somatório (respectivamente, MAX, MIN, AVG e SUM). 

Quantos clientes possuem contas na agência cujo cod_agencia = ‘123’? 
	SELECT COUNT (DISTINCT cod_cliente)
	FROM Contas
	WHERE cod_agencia = '123' 

Listar o número de contas existentes em cada agência.
	SELECT cod_agencia, COUNT(*)
	FROM Contas
	GROUP BY cod_agencia 

Para cada agência (cod_agencia) com menos de 1000 contas, listar os valores máximo e mínimo dos saldos dessas contas, assim como o saldo médio.
	SELECT cod_agencia, MAX(saldo), MIN(saldo), AVG(saldo)
	FROM Contas
	GROUP BY cod_agencia
	HAVING COUNT(*) < 1000

Quais os clientes cuja profissão é desconhecida?
	SELECT *
	FROM Clientes
	WHERE profissao IS NULL 

Quais os clientes (cod_cliente e cliente) da agência cod_agencia=‘123’?

	SELECT Cl.cod_cliente, Cl.cliente
	FROM Contas Co, Clientes Cl, Emprestimos E
	WHERE (Co.cod_agencia = '123' 
          AND	Co.cod_cliente = Cl.cod_cliente) OR
	      (E.cod_agencia = '123' AND
      		E.cod_cliente = Cl.cod_cliente)

Ou (um UNION que substitui o OR de duas condições):


	SELECT Cl.cod_cliente, Cl.cliente
	FROM Contas Co, Clientes Cl
	WHERE Co.cod_agencia = '123' 
      		AND Co.cod_cliente = Cl.cod_cliente
	UNION
	SELECT Cl.cod_cliente, Cl.cliente
	FROM Emprestimos E, Clientes Cl
	WHERE E.cod_agencia = '123' 
      		AND E.cod_cliente = Cl.cod_cliente

Quais os clientes (cod_cliente e cliente) que são, simultaneamente, depositantes e devedores (de empréstimos) na agência cujo cod_agencia = ‘123’?

	SELECT Cl.cod_cliente, Cl.cliente
	FROM Contas Co, Clientes Cl
	WHERE Co.cod_agencia = '123' 
       		AND 	Co.cod_cliente = Cl.cod_cliente
	INTERSECT 
	SELECT Cl.cod_cliente, Cl.cliente
	FROM Emprestimos E, Clientes Cl
	WHERE E.cod_agencia = '123‘
       		AND E.cod_cliente = Cl.cod_cliente 

Ou:

  SELECT Cl.cod_cliente, Cl.cliente
	FROM Contas Co, Clientes Cl
	WHERE (Co.cod_agencia = '123' 
       		AND Co.cod_cliente = Cl.cod_cliente) 
		AND (E.cod_agencia = '123‘
       		AND E.cod_cliente = Cl.cod_cliente) 

Quais os clientes (cod_cliente e cliente) da agência com cod_agencia = ‘123’ que apenas são depositantes? 

	SELECT Cl.cod_cliente, Cl.cliente
	FROM Contas Co, Clientes Cl
	WHERE Co.cod_agencia = '123' 
      		AND Co.cod_cliente = Cl.cod_cliente
	EXCEPT 
	SELECT Cl.cod_cliente, Cl.cliente
	FROM Emprestimos E, Clientes Cl
	WHERE E.cod_agencia = '123' 
      		AND E.cod_cliente = Cl.cod_cliente 

Quais os clientes (cod_cliente e cliente) com, pelo menos, um empréstimo no banco? 
	SELECT C.cod_cliente, C.cliente
	FROM Clientes C
	WHERE EXISTS (SELECT *
              FROM Emprestimos E
              WHERE C.cod_cliente = E.cod_cliente)

Ou,

	SELECT cod_cliente, cliente
	FROM Clientes
	WHERE cod_cliente IN (SELECT cod_cliente
              FROM Emprestimos)

Quais as agências (cod_agencia, agencia) com depositantes residentes em Lisboa? 

	SELECT A.cod_agencia, A.agencia
	FROM Agencias A, Contas C
	WHERE C.cod_cliente IN 
      	   (SELECT cod_cliente
       	   FROM Clientes
       	   WHERE localidade = 'Lisboa') 
    		AND  	C.cod_agencia = A.cod_agencia 

Quais os clientes cujo saldo total das suas contas é superior ao valor de qualquer empréstimo contraído neste banco?  

	SELECT Cl.*
	FROM Clientes Cl
	WHERE (SELECT SUM(Co.saldo)
       	FROM Contas Co
       	WHERE Co.cod_cliente = Cl.cod_cliente)
       	> 
      	(SELECT MAX (valor)
       	 FROM Emprestimos) 

Inserção de dados
	INSERT INTO <tabela> [(<colunas>)]
	  VALUES (<valores>)

Alguns exemplos
  INSERT INTO Clientes
     VALUES('1234','J.Silva','Estudante','Braga')

	INSERT INTO Clientes
     (cod_cliente, cliente, localidade)
     VALUES ('1235','A.Costa','Guimarães')

  
Alteração de dados
	UPDATE <tabela>
	SET <coluna> = <expressão>,
        ...    =    ...
	[WHERE <condição>]

Alguns exemplos
	UPDATE Contas
	SET saldo = saldo + 1000
	WHERE num_conta = '1234567890‘


	UPDATE Contas
	SET saldo = (SELECT MAX (saldo)
               FROM Contas
               WHERE cod_cliente = '1234')
	WHERE cod_cliente = '1234' 

Remoção de dados
	DELETE FROM <tabela>
	[WHERE <condição>]

Alguns exemplos
	DELETE FROM Contas
	WHERE num_conta = '1234567890' 


	DELETE FROM Clientes
	WHERE cod_cliente IN (SELECT cod_cliente
                        FROM Contas
                        WHERE cod_agencia ='123')

 
-----------------------------------------------------------

Criação de tabelas:
	CREATE TABLE <nome_tabela> (
		< definição de colunas e
		restrições de integridade >
		) 

Quais os atributos/campos da tabela?
Quais os seus domínios (INTEGER, DECIMAL, CHAR, …) ? 
Quais as restrições de integridade? 

Exemplos:
	NOT NULL 
	 custo	DECIMAL(5,2) NOT NULL 

A SQL como linguagem de definição de dados (cont.)
- PRIMARY  KEY
	cod_produto	CHAR(6) PRIMARY KEY

    Ou,
	num_factura	CHAR(5),
	cod_produto	CHAR(6),
	PRIMARY KEY (num_factura, cod_produto)

- UNIQUE
	cod_fornecedor	CHAR(4) PRIMARY KEY,
	nome_fornecedor	CHAR(20) NOT NULL,
	UNIQUE (nome_fornecedor)

- CHECK
	peso			INTEGER,
	classificacao		SMALLINT,
	genero			CHAR(1),
	CHECK (peso > 50),
	CHECK (classificacao BETWEEN 0 AND 20),
	CHECK (genero IN ('F','M')) 

Restrições de integridade referencial

Modificação de cod_dep na tabela Departamentos ????
Remoção do dep. Informática na tabela Departamentos ????

CREATE TABLE Funcionarios (
	...
	cod_dep	CHAR(3),
	FOREIGN KEY (cod_dep)
	REFERENCES Departamentos (cod_dep)
	ON UPDATE CASCADE
	ON DELETE SET NULL ),
	...

Exemplo de esquema relacional considerando:

	Clientes (cod_cliente, cliente, profissao, localidade)
	Agencias (cod_agencia, agencia, localidade)
	Contas (num_conta, tipo_conta, cod_cliente, cod_agencia, saldo)
	Emprestimos (num_emprestimo, cod_cliente, cod_agencia, valor)

Restrições
    . Só existem contas Ordem e Prazo
    . O saldo de qualquer conta tem de ser sempre igual ou superior a 10.000
    . Os empréstimos têm de ser >=100.000 e <=10.000.000

O esquema poderia ser definido em SQL:

CREATE TABLE Contas (
	num_conta		CHAR(10),
	tipo_conta		CHAR(5),
	cod_agencia		CHAR(3),
	cod_cliente		CHAR(4) NOT NULL,
	saldo			DECIMAL(10,2) NOT NULL,
	CONSTRAINT tipos_de_contas
	   CHECK (tipo_conta IN ('ordem','prazo')),
	CONSTRAINT valor_saldo CHECK (saldo >= 10000),
	CONSTRAINT ch_prim_Contas
	   PRIMARY KEY (num_conta),
	CONSTRAINT ch_estr_Agencias_Contas
	   FOREIGN KEY (cod_agencia)
	   REFERENCES Agencias (cod_agencia)
	   ON UPDATE CASCADE
	   ON DELETE SET NULL,		<============
	CONSTRAINT ch_estr_Clientes_Contas
	   FOREIGN KEY (cod_cliente)
	   REFERENCES Clientes (cod_cliente)
	   ON UPDATE CASCADE
	   ON DELETE CASCADE		<============
	) 

CREATE TABLE Emprestimos (
	num_emprestimo		CHAR(5),
	cod_agencia		CHAR(3),
	cod_cliente		CHAR(4) NOT NULL,
	valor			INTEGER NOT NULL,
	CONSTRAINT valor_emprestimo
	   CHECK (valor BETWEEN 100000 AND 100000000),
	CONSTRAINT ch_prim_Emprestimos
	   PRIMARY KEY (num_emprestimo),
	CONSTRAINT ch_estr_Agencias_Emprestimos
	   FOREIGN KEY (cod_agencia)
	   REFERENCES Agencias (cod_agencia)
	   ON UPDATE CASCADE
	   ON DELETE SET NULL,		<==============
	CONSTRAINT ch_estr_Clientes_Emprestimos
	   FOREIGN KEY (cod_cliente)
	   REFERENCES Clientes (cod_cliente)
	   ON UPDATE CASCADE
	   ON DELETE CASCADE		<==============
	) 

CREATE TABLE Agencias (
	cod_agencia	CHAR(3),
	agencia		VARCHAR(20) NOT NULL,
	localidade	VARCHAR(10) NOT NULL,
	CONSTRAINT ch_candidata_Agencias
	   UNIQUE (agencia),
	CONSTRAINT ch_prim_Agencias
	   PRIMARY KEY (cod_agencia)
	)

CREATE TABLE Clientes (
	cod_cliente	CHAR(4),
	cliente		VARCHAR(30) NOT NULL,
	profissao	VARCHAR(10),
	localidade	VARCHAR(10) NOT NULL,
	CONSTRAINT ch_prim_Clientes
	   PRIMARY KEY (cod_cliente)
	)

Alteração da estrutura das tabelas:
	ALTER TABLE Clientes
	   ADD COLUMN nacionalidade VARCHAR(15)
              	DEFAULT 'portuguesa'

	ALTER TABLE Clientes
	   MODIFY COLUMN nacionalidade VARCHAR(25)

	ALTER TABLE Clientes
	   DROP COLUMN nacionalidade

Remoção de tabelas:

	DROP TABLE Clientes 


Tabelas virtuais (views)
	CREATE VIEW <view> [(<colunas>)]
	   AS <questão>
	   [WITH CHECK OPTION]

Exemplo
	CREATE VIEW Grandes_Contas 
	   AS (SELECT *
		FROM Contas
		WHERE saldo > 100000000)

(View que pode ser utilizada como se de uma tabela se tratasse.)

Clientes cujas contas têm saldos superiores ao saldo médio das contas do banco:

	
   CREATE VIEW Super_Clientes (cod_cliente, cliente)
     AS (SELECT Cl.cod_cliente, Cl.cliente
         FROM Clientes Cl
         WHERE (SELECT AVG (saldo)
                FROM Contas)
              < ALL
               (SELECT Saldo
                FROM Contas Co
                WHERE Co.cod_cliente = Cl.cod_cliente)) 

As views são muito utilizadas na simplificação de questões
Exemplo
	“quais os clientes, com empréstimos contraídos neste banco, cujas contas têm saldos superiores à media (super clientes) ?” 

	SELECT *
	FROM Super_Clientes
	WHERE cod_cliente IN (SELECT cod_cliente
                      	  FROM Emprestimos)  

	Remoção da view
	DROP VIEW Super_Clientes

Actualização de views
    . Nem todas as views são actualizáveis...
    . As que forem, podem evitar actualizações fora do seu âmbito
	Exemplo
	CREATE VIEW Grandes_Contas
     	    AS (SELECT *
         	    FROM Contas
         	    WHERE saldo > 100000000)
     	    WITH CHECK OPTION 

Restrições do tipo assertion
    . Não ficam “presas” a qualquer tabela
    . Úteis para especificar restrições sobre várias tabelas
    . Exemplo: “O saldo total das contas de cada cliente (caso possua alguma!) não pode ser superior ao valor de qualquer empréstimo contraído por esse cliente”

ALTER TABLE Emprestimos
		ADD CONSTRAINT Emprestimos_Contas
		CHECK ((SELECT SUM(C.saldo)
	            FROM Contas C
	            WHERE C.cod_cliente = cod_cliente)
	           <
	           (SELECT MIN(E.valor)
	            FROM Emprestimos E
	            WHERE E.cod_cliente = cod_cliente))


-- Resumos de SQL -- Luís Baptista

SELECT- extrai dados de um banco de dados

--Exemplos

--1 
SELECT column1, column2, ...    -- selecionar colunas especificas
FROM table_name;

--2
SELECT * FROM table_name; -- selecionar todas as colunas da tabela

--3
SELECT DISTINCT column1, column2, ... --selecionar valores distintos das colunas, ou seja, valores que não se repetem
FROM table_name;

--4
SELECT COUNT(DISTINCT column1) FROM table_name; -- isto permite contar quantos valores diferentes temos na tabela

-------------------------------------------------------------------------------------------------------------------------

                                                    -//// Where - Condicao \\\\-

--Exmplos e especificações

SELECT column1, column2, ...
FROM table_name
WHERE condition;

-- 1
SELECT * FROM Customers
WHERE Country = 'Mexico'; -- Seleciona todos os clientes do "México" , é necessário áspas simples em texto

--2 
SELECT * FROM Customers
WHERE CustomerID = 1;   -- seleciona todos os clientes com ID = 1, os números não necessitam de áspas


Operadores para usar no Where :

     =    ->   Igual a
     >    ->   Maior que
     <    ->   Menor que
     >=   ->   Maior ou igual
     <=   ->   Menor ou igual
     !=   ->   Diferente de
     BETWEEN   Entre A And B ou 10 And 50
     IN        Especificar vários valores de uma coluna -O IN é uma abreviação para múltiplas condições OR
     Like      Procurar por um simbolo ou letra
     
     Existem dois simbolos frequentemente usados num conjunto com o LIKE:

O sinal de percentagem (%) representa zero, um ou vários caracteres
O sinal de sublinhado (_) representa um único caractere

Tabela com aplicações do Like

LIKE Operator	                Description

WHERE CustomerName LIKE 'a%'	Finds any values that start with "a"
WHERE CustomerName LIKE '%a'	Finds any values that end with "a"
WHERE CustomerName LIKE '%or%'	Finds any values that have "or" in any position
WHERE CustomerName LIKE '_r%'	Finds any values that have "r" in the second position
WHERE CustomerName LIKE 'a_%'	Finds any values that start with "a" and are at least 2 characters in length
WHERE CustomerName LIKE 'a__%'	Finds any values that start with "a" and are at least 3 characters in length
WHERE ContactName LIKE 'a%o'	Finds any values that start with "a" and ends with "o"

--Exclusivo
A seguinte instrução SQL seleciona todos os clientes com um CustomerName que NÃO começa com "a":

SELECT * FROM Customers
WHERE CustomerName NOT LIKE 'a%';
     
     
--NOTA 
A WHERE pode ser combinada com os operadores AND, OR e NOT.

Os operadores AND e OR são usados para filtrar registos com base em mais de uma condição:

O AND exibe um registo se todas as condições separadas por AND forem TRUE.

--Ex
SELECT column1, column2, ...
FROM table_name
WHERE condition1 AND condition2 AND condition3 ...;

O OR exibe um registo se alguma das condições separadas por OR for TRUE.

--EX
SELECT column1, column2, ...
FROM table_name
WHERE condition1 OR condition2 OR condition3 ...;

O NOT exibe um registo se a(s) condição(ões) NÃO for(em) VERDADEIRA(S).

--Ex
SELECT column1, column2, ...
FROM table_name
WHERE NOT condition;

-------------------------------------------------------------------------------------------------------------------------

                                              -//// ORDER BY \\\\-

A ORDER BY classifica os registos em ordem crescente por padrão. 
Para classificar os registros em ordem decrescente, usa-se a palavra DESC, ORDER BY column1 DESC;


-----------------------------------------------------------------------------------------------------------------------------

                                        -/// INSERT INTO- insere novos \\\-


É possível escrever a INSERT INTO de duas maneiras:

-- 1. Especificar os nomes das colunas e os valores a serem inseridos:

INSERT INTO table_name (column1, column2, column3, ...)
VALUES (value1, value2, value3, ...);

-- 2. Adicionar valores para todas as colunas da tabela

INSERT INTO table_name
VALUES (value1, value2, value3, ...);

----------------------------------------------------------------------------------------------------------------------------

                                                             -///// Valores NULL \\\\\-


Não é possível testar valores NULL com operadores de comparação, como =, < ou <>.
Teremos que usar os operadores IS NULL and IS NOT NULL em vez disso. 

--Exemplos

-- É NULL
SELECT column_names
FROM table_name
WHERE column_name IS NULL;

--Não é NULL
SELECT column_names
FROM table_name
WHERE column_name IS NOT NULL;


---------------------------------------------------------------------------------------------------------------------------


                                                    -/// Instrução UPDATE \\\\-

A instrução UPDATE é usada para modificar os registos existentes numa tabela.

--Exemplo
UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE condition;

NOTA - Ter cuidado ao atualizar registos numa tabela! 
A WHERE especifica quais são os registos que devem ser atualizados. 
Se omitirmos a WHERE, todos os registos da tabela serão atualizados!


-----------------------------------------------------------------------------------------------------------------------------


                                        -/////// DELETE- exclui dados da base de dados \\\\\\\-
 
 -- Exemplo
 
DELETE FROM table_name WHERE condition;

NOTA - A WHERE especifica quais são os registos que devem devem ser excluídos. 
Se omitirmos a WHERE, todos os registos da tabela serão apagados!

--------------------------------------------------------------------------------------------------------------------------------

                                       -////// Instrução LIMIT \\\\\\-          Isto não sai

A LIMIT é usada para especificar o número de registos a serem retornados.
A LIMIT é útil em tabelas grandes com milhares de registros. 
O retorno de um grande número de registos pode afetar o desempenho.

-- Sintax
SELECT column_name(s)
FROM table_name
WHERE condition
LIMIT number;

--Exemplo
SELECT * FROM Customers
LIMIT 3;

E se quisermos selecionar os registos 4 a 6 (inclusive)?
Usamos o comando OFFSET.

A consulta SQL abaixo diz "retornar apenas 3 registos, iniciar no registo 4 (OFFSET 3)":

-- Exemplo
SELECT * FROM Customers
LIMIT 3 OFFSET 3;

-----------------------------------------------------------------------------------------------------------------------------------------


                                                             -///// Funções MIN() e MAX() \\\\\-
 
A MIN() retorna o menor valor da coluna selecionada.

A MAX() retorna o maior valor da coluna selecionada.

-- Sintax MÍN()
SELECT MIN(column_name)
FROM table_name
WHERE condition;

-- Sintax MAX()
SELECT MAX(column_name)
FROM table_name
WHERE condition;

--------------------------------------------------------------------------------------------------------------------------------------


                                          -///// Funções COUNT(), AVG() e SUM() \\\\\-

A COUNT()retorna o número de linhas que corresponde a um critério especificado.

--Ex
SELECT COUNT(column_name)
FROM table_name
WHERE condition;

A AVG()função retorna o valor médio de uma coluna numérica. 

--Ex
SELECT AVG(column_name)
FROM table_name
WHERE condition;

A SUM()função retorna a soma total de uma coluna numérica. 

--Ex
SELECT SUM(column_name)
FROM table_name
WHERE condition;


---------------------------------------------------------------------------------------------------------------------------------


                                                        -///// Instrução AS \\\\\\-



A instrução SQL a seguir cria dois aliases, um para a coluna CustomerName e outro para a coluna ContactName. 
Nota: Aspas simples ou duplas serão obrigatórias se o nome alternativo contiver espaços:

SELECT CustomerName AS Customer, ContactName AS "Contact Person"
FROM Customers;

A instrução SQL a seguir cria um alias chamado "Endereço" que combina quatro colunas (Endereço, Código Postal, Cidade e País):

SELECT CustomerName, CONCAT_WS(', ', Address, PostalCode, City, Country) AS Address
FROM Customers;

Usamos o AS para puder simplificar os nomes das tabelas, por exemplo:

SELECT o.OrderID, o.OrderDate, c.CustomerName
FROM Customers AS c, Orders AS o
WHERE c.CustomerName='Around the Horn' AND c.CustomerID=o.CustomerID;

                                                         
----------------------------------------------------------------------------------------------------------------------                                                         
                                                         
                                                         -///// Instruções JOIN \\\\\\-


-- Tipos de junções suportadas no MySQL
INNER JOIN: Retorna registos que possuem valores correspondentes em ambas as tabelas
LEFT JOIN:  Retorna todos os registos da tabela esquerda e os registros correspondentes da tabela direita
RIGHT JOIN: Retorna todos os registos da tabela direita e os registros

--Exemplo de INNER JOIN
SELECT Orders.OrderID, Customers.CustomerName, Orders.OrderDate
FROM Orders
INNER JOIN Customers 
ON Orders.CustomerID=Customers.CustomerID;

--Exemplo de LEFT JOIN
SELECT column_name(s)
FROM table1
LEFT JOIN table2
ON table1.column_name = table2.column_name;



--Exemplo de RIGHT JOIN
A instrução SQL a seguir retornará todos os funcionários e quaisquer pedidos que eles possam ter feito:
SELECT Orders.OrderID, Employees.LastName, Employees.FirstName
FROM Orders
RIGHT JOIN Employees ON Orders.EmployeeID = Employees.EmployeeID
ORDER BY Orders.OrderID;

-----------------------------------------------------------------------------------------------------------------------
                                          
                                          -//// Auto - Junção \\\\\-



Uma junção automática é uma junção regular, mas a tabela é unida a si mesma.

--Exemplo
SELECT A.CustomerName AS CustomerName1, B.CustomerName AS CustomerName2, A.City
FROM Customers A, Customers B
WHERE A.CustomerID != B.CustomerID
AND A.City = B.City
ORDER BY A.City;

-----------------------------------------------------------------------------------------------------------------------


                                               -////Operador Union \\\\\\-

O UNION é usado para combinar o conjunto de resultados de duas ou mais SELECT.

Cada SELECT dentro UNION deve ter o mesmo número de colunas
As colunas também devem ter tipos de dados semelhantes
As colunas em cada SELECT também devem estar na mesma ordem

--Exemplo:
SELECT column_name(s) FROM table1
UNION
SELECT column_name(s) FROM table2;


O UNION seleciona apenas valores distintos por padrão. Para permitir valores duplicados, usa-se o UNION ALL:

SELECT column_name(s) FROM table1
UNION ALL
SELECT column_name(s) FROM table2;

----------------------------------------------------------------------------------------------------------------------------

                                              -//////// Instrução GROUP BY \\\\\\\\-

A GROUP BYagrupa linhas que possuem os mesmos valores em linhas de resumo, como "encontre o número de clientes em cada país".

A GROUP BY é frequentemente usada com funções agregadas ( COUNT(), MAX(), MIN(), SUM(), AVG())
para agrupar o conjunto de resultados de uma ou mais colunas.

--SINTAX
SELECT column_name(s)
FROM table_name
WHERE condition
GROUP BY column_name(s)
ORDER BY column_name(s);

-----------------------------------------------------------------------------------------------------------
                                               
                                                 -/////////// Instrução HAVING \\\\\\\\\\-

A HAVING foi adicionada ao SQL porque a WHERE não pode ser usada com funções agregadas.

--EX
SELECT column_name(s)
FROM table_name
WHERE condition
GROUP BY column_name(s)
HAVING condition
ORDER BY column_name(s);

A instrução SQL a seguir lista o número de clientes em cada país. Inclui apenas países com mais de 5 clientes:
SELECT COUNT(CustomerID), Country
FROM Customers
GROUP BY Country
HAVING COUNT(CustomerID) > 5;


-------------------------------------------------------------------------------------------------------------------

                                                          -///// Operador EXISTS \\\\\-

O EXISTS é usado para testar a existência de qualquer registo em uma subconsulta.
O EXISTS retorna TRUE se a subconsulta retornar um ou mais registos.

--Exemplo
A instrução SQL a seguir retorna TRUE e lista os fornecedores com preço de produto igual a 22:
SELECT SupplierName
FROM Suppliers
WHERE EXISTS (SELECT ProductName FROM Products WHERE Products.SupplierID = Suppliers.supplierID AND Price = 22);




-----------------------------------------------------------------------------------------------------------------------

                                                  -////Instrução INSERT INTO SELECT \\\\\-

A INSERT INTO SELECT copia dados de uma tabela e insere-os noutra tabela.
A INSERT INTO SELECT exige que os tipos de dados nas tabelas de origem e de destino correspondam.

A seguinte instrução SQL copia "Fornecedores" em "Clientes" (as colunas que não são preenchidas com dados conterão NULL):

INSERT INTO Customers (CustomerName, City, Country)
SELECT SupplierName, City, Country FROM Suppliers;


----------------------------------------------------------------------------------------------------------


                                                   -///// Instução CASE \\\\\\\-



A CASEinstrução passa por condições e retorna um valor quando a primeira condição é atendida
(como uma instrução if-then-else). 
Assim, uma vez que uma condição seja verdadeira, ela irá parar de ler e retornar o resultado. 
Se nenhuma condição for verdadeira, ele retorna o valor da ELSE.
Se não houver nenhuma ELSE e nenhuma condição for verdadeira, retorna NULL.


--SINTAX
CASE
    WHEN condition1 THEN result1
    WHEN condition2 THEN result2
    WHEN conditionN THEN resultN
    ELSE result
END;

--Exemplos

O SQL a seguir passa pelas condições e retorna um valor quando a primeira condição é atendida:
SELECT OrderID, Quantity,
CASE
    WHEN Quantity > 30 THEN 'The quantity is greater than 30'
    WHEN Quantity = 30 THEN 'The quantity is 30'
    ELSE 'The quantity is under 30'
END AS QuantityText
FROM OrderDetails;

O SQL a seguir ordenará os clientes por cidade. No entanto, se City for NULL, ordena por país:
SELECT CustomerName, City, Country
FROM Customers
ORDER BY
(CASE
    WHEN City IS NULL THEN Country
    ELSE City
END);

-----------------------------------------------------------------------------------------------------------------------


                                               -///// Função IFNULL() \\\\\\\\\-


A função MySQL IFNULL()permite retornar um valor alternativo se uma expressão for NULL.

O exemplo abaixo retorna 0 se o valor for NULL:

SELECT ProductName, UnitPrice * (UnitsInStock + IFNULL(UnitsOnOrder, 0))
FROM Products;


CREATE TABLE- cria uma nova tabela

--SINTAX
CREATE TABLE table_name (
    column1 datatype,
    column2 datatype,
    column3 datatype,
   ....
);

--Ex

O exemplo a seguir cria uma tabela chamada "Pessoas" que contém cinco colunas: PersonID, LastName, FirstName, Address e City:
CREATE TABLE Persons (
    PersonID int,
    LastName varchar(255),
    FirstName varchar(255),
    Address varchar(255),
    City varchar(255)
);

-- Criar tabela usando outra tabela
Uma cópia de uma tabela existente também pode ser criada usando CREATE TABLE.
A nova tabela obtém as mesmas definições de coluna. Todas as colunas ou colunas específicas podem ser selecionadas.
Se criarmos uma nova tabela usando uma tabela existente, 
a nova tabela será preenchida com os valores existentes da tabela antiga.

--Sintax
CREATE TABLE new_table_name AS
    SELECT column1, column2,...
    FROM existing_table_name
    WHERE ....;


--Ex
CREATE TABLE TestTable AS
SELECT customername, contactname
FROM customers;


A instução TRUNCATE TABLE é usada para excluir os dados dentro de uma tabela, mas não a própria tabela.

--Sintax
TRUNCATE TABLE table_name;


A instrução ALTER TABLE  é usada para adicionar uma Coluna

--Sintaz
ALTER TABLE table_name
ADD column_name datatype;

-- Exluir a coluna de uma tabela:
ALTER TABLE table_name
DROP COLUMN column_name;

-- Para alterar o tipo de dados de uma coluna em uma tabela, usamos a seguinte sintax:

ALTER TABLE table_name
MODIFY COLUMN column_name datatype;


---------------------------------------------------------------------------------------------------------------------------

                                                            -/////////// Restrições\\\\\\\\\\\-

NOT NULL- Garante que uma coluna não pode ter um valor NULL

--EX
CREATE TABLE Persons
   ID int NOT NULL
   LastName varchar(255) NOT NULL,
   FirstName varchar(255) NOT NULL
   Age int );
   
   


UNIQUE- Garante que todos os valores em uma coluna sejam diferentes

--EX
CREATE TABLE Persons (
    ID int NOT NULL,
    LastName varchar(255) NOT NULL,
    FirstName varchar(255),
    Age int,
    UNIQUE (ID)
);



PRIMARY KEY- Uma combinação de a NOT NULLe UNIQUE. Identifica exclusivamente cada linha em uma tabela

--Ex
CREATE TABLE Persons (
    ID int NOT NULL,
    LastName varchar(255) NOT NULL,
    FirstName varchar(255),
    Age int,
    PRIMARY KEY (ID)
);



FOREIGN KEY - Impede ações que destruiriam links entre tabelas

-- A FOREIGN KEY é um campo (ou coleção de campos) em uma tabela, que se refere a PRIMARY KEYoutra tabela.
-- A tabela com a chave estrangeira é chamada de tabela filha,
-- e a tabela com a chave primária é chamada de tabela referenciada ou tabela pai.

CREATE TABLE Orders (
    OrderID int NOT NULL,
    OrderNumber int NOT NULL,
    PersonID int,
    PRIMARY KEY (OrderID),
    FOREIGN KEY (PersonID) REFERENCES Persons(PersonID)
);



CHECK- Garante que os valores em uma coluna satisfaçam uma condição específica


O SQL a seguir cria uma CHECK na coluna "Idade" quando a tabela "Pessoas" é criada. 
A CHECK garante que a idade de uma pessoa deve ser 18 anos ou mais:

CREATE TABLE Persons (
    ID int NOT NULL,
    LastName varchar(255) NOT NULL,
    FirstName varchar(255),
    Age int,
    CHECK (Age>=18)
);



DEFAULT- Define um valor padrão para uma coluna se nenhum valor for especificado

A DEFAULT é usada para definir um valor padrão para uma coluna.

O valor padrão será adicionado a todos os novos registros, se nenhum outro valor for especificado.

--Ex
CREATE TABLE Persons (
    ID int NOT NULL,
    LastName varchar(255) NOT NULL,
    FirstName varchar(255),
    Age int,
    City varchar(255) DEFAULT 'Sandnes'
);


CREATE INDEX- Usado para criar e recuperar dados do banco de dados muito rapidamente

A CREATE INDEXinstrução é usada para criar índices em tabelas.

Os índices são usados para recuperar dados do banco de dados mais rapidamente do que de outra forma. 
Os usuários não podem ver os índices, eles apenas servem para agilizar pesquisas/consultas.

Nota: Atualizar uma tabela com índices leva mais tempo do que atualizar uma tabela sem 
(porque os índices também precisam de atualização). 
Portanto, crie índices apenas em colunas que serão pesquisadas com frequência.


--Ex
CREATE INDEX index_name
ON table_name (column1, column2, ...);


CREATE DATABASE testDB;
ALTER DATABASE - Altera a base de dados
DROP DATABASE - Apaga a base de dados


---------------------------------------------------------------------------------------------------------------------

                               -////////////// Tipos de dados de data \\\\\\\\\\\\\\\\-


DATE- formato AAAA-MM-DD
DATETIME- formato: AAAA-MM-DD HH:MI:SS
TIMESTAMP- formato: AAAA-MM-DD HH:MI:SS
YEAR- formato AAAA ou AA


Agora queremos selecionar os registros com OrderDate de "2008-11-11" na tabela acima.

SELECT * FROM Orders WHERE OrderDate='2008-11-11'


-----------------------------------------------------------------------------------------------------------------------

                                               -////////Instrução CREATE VIEW \\\\\\\\-

-- Nota 
Uma visualização contém linhas e colunas, assim como uma tabela real. 
Os campos em uma visualização são campos de uma ou mais tabelas reais do banco de dados.
Você pode adicionar instruções e funções SQL a uma visualização e apresentar os dados como se viessem de uma única tabela.


--SINTAX
CREATE VIEW view_name AS
SELECT column1, column2, ...
FROM table_name
WHERE condition;


--O SQL a seguir cria uma view que mostra todos os clientes do Brasil:
CREATE VIEW [Brazil Customers] AS
SELECT CustomerName, ContactName
FROM Customers
WHERE Country = 'Brazil';


SELECT * FROM [Brazil Customers]; -- Para concultar a view



-----------------------------------

Uma visualização pode ser atualizada com a CREATE OR REPLACE VIEWinstrução.

--SINTAX
CREATE OR REPLACE VIEW view_name AS
SELECT column1, column2, ...
FROM table_name
WHERE condition;

O SQL a seguir adiciona a coluna "Cidade" à visualização "Clientes do Brasil":

--Exemplo
CREATE OR REPLACE VIEW [Brazil Customers] AS
SELECT CustomerName, ContactName, City
FROM Customers
WHERE Country = 'Brazil';


A view is deleted with the DROP VIEW statement.

DROP VIEW Syntax
DROP VIEW view_name;


-------------------------------------------------------------------------------------------------------------------------


                   -///////////////// Tipos de Dados\\\\\\\\\\\\\\\\\- 


 CHAR(size)
 BOOLEAN
 INT(size)
























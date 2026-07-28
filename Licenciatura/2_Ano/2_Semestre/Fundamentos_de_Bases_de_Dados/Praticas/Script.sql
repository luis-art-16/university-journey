-- A105419 - Luis Baptista

-- B.

drop table if exists funcionarios;

CREATE TABLE funcionarios (
    n_funcionario   int primary key auto_increment,
    nome            varchar(100) not null,
    designação      varchar(30) not null
    
   );


CREATE TABLE Artigo (
    n_artigo    int not null,
    designacao_artigo  varchar(150),
    
    Primary Key (n_artigo)
     Foreign Key (n_funcionario),
    REFERENCES Artigo(n_artigo)
   
);
    
drop table encomenda;
CREATE TABLE Encomenda(
  n_encomenda int not null,
  quantidade int not null,
  preco Decimal(50),
   
  Primary Key (n_encomenda)
   
  );

CREATE TABLE Fornecedor (
      n_fornecedor  int not null,
      designacao_forncedor  varchar(150),
      
      Primary key (n_fornecedor)
      
      );    
    
-- Inserts
INSERT INTO funcionarios (n_funcionario, nome ,designação)
	values (1,"Luis", "nao_responsavel"),
           (2, "Joao", "responsavel"),
           (3, "Pedro", "nao_responsavel"),
           (4, "Tiago", "nao_responsavel"),
           (5, "Lucas", "nao_responsavel"),
           (6, "Armindo", "nao_responsavel"),
           (7, "Diogo", "nao_responsavel"),
           (8, "Vasco", "nao_responsavel"),
           (9, "Jose", "nao_responsavel"),
           (10, "Leandro", "nao_responsavel");
       
           
           
INSERT INTO Artigo (n_artigo, designacao_artigo)
    values(1, "material_escrita"),
          (2, "software"),
          (3, "livros"),
          (4, "material_apoio");
          

      
INSERT INTO Encomenda( n_encomenda, quantidade, preco)
   values (1,2,10.3),
          (2,10,10.3),
          (3,2,5.1),
          (4,3,6.7),
          (5,2,10.3),
          (6,4,10.3),
          (7,5,8.2),
          (8,1,10.3);
          
 
INSERT INTO Fornecedor ( n_fornecedor, designacao_forncedor)
   values (1, "Porto"),
          (2, "Braga"),
          (3, "Lisboa"),
          (4, "Guimarães"),
          (5, "Algarve"),
          (6, "Bragança");     
         

COMMIT;
           
SELECT * FROM Artigo;
SELECT * FROM funcionarios;
-- Exercicio do Lince

drop table if exists linces;

create table linces(
	cod_lince		int unsigned not null auto_increment,
    nome			varchar(20) not null,
    genero			varchar(15) not null,
    dataNasc		date default current_timestamp,
    dataObito		date default current_timestamp,
    cod_pai			int,
    cod_mae			int,
    
    primary key (cod_lince)
) 


drop table if exists tecnicos;

create table tecnicos(
	cod_tecnico		int unsigned not null auto_increment,
    nome			varchar(20) not null default '',
    primary key (cod_tecnico)
)


drop table if exists localizacoes;

create table localizacoes(
	cod_lince		int unsigned not null,
    horas			int unsigned not null,
    dataLclz		date default current_timestamp,
    longitude		float(6,4) not null,
    latitude		float(6,4) not null,
    
    primary key (cod_lince),
    foreign key (cod_lince)
 )



drop table if exists controlos;

create table controlos(
	cod_lince		int unsigned not null auto_increment,
    cod_Tecnico		int unsigned not null,
    dataCntrl		date default current_timestamp,
    peso			decimal(50,2),
    estadoSaude		varchar(50),
    
    primary key (cod_lince, cod_Tecnico),
    foreign key (cod_Lince),
    foreign key (cod_Tecnico)
    
)

-- insert na table linces
insert into linces(cod_lince, nome, genero, dataNasc, dataObito, cod_pai, cod_mae)
values
    (1,'Luck','Masculino', '2008-10-01', '2020-12-01', NULL, NULL),
	(2,'Mini','Feminino', '2008-10-01', '2020-09-01', NULL, NULL),
    (3,'Red','Masculino', '2010-11-02', '2021-02-01', NULL, NULL),
    (4,'Blue','Feminino', '2009-10-13', '2020-03-01', NULL, NULL),
    (5,'Lincy','Feminino', '2014-12-21', '2022-12-01', 1, 2),
    (6,'Bonny','Feminino', '2014-12-21', '2022-12-01', 1, 2),
    (7,'Cooper','Masculino', '2015-11-21', NULL, 1, 2),
    (8,'Charlie','Masculino', '2015-11-21', NULL, 1, 2),
    (9,'Maxy','Masculino', '2014-03-11', '2021-01-01', 3, 4),
    (10,'Moly','Feminino', '2016-05-01', '2022-12-01', 3, 4),
    (11,'Buddy','Masculino', '2014-03-11', NULL, 3, 4),
    (12,'Luna','Feminino', '2016-05-01', NULL, 3, 4),
    (13,'Siri','Feminino', '2018-08-18', NULL, 7, 5),
    (14,'Bella','Feminino', '2019-09-07', NULL, 7, 5),
    (15,'Doly','Feminino', '2019-09-07', NULL, 8, 6),
    (16,'Rocky','Masculino', '2019-09-07', '2022-01-01', 8, 6),
    (17,'Oliver','Masculino', '2021-09-07', NULL, 11, 14),
    (18,'Nova','Feminino', '2019-09-07', '2022-12-01', 16, 12);

select * from linces

-- insert na table tecnicos
insert into tecnicos(cod_tecnico, nome)
values
    (1,'Luis'),
	(2,'Catarina'),
	(3,'Pedro'),
	(4,'Maria'),
	(5,'Miguel'),
	(6,'Lara'),
	(7,'Antonio'),
	(8,'Renato'),
	(9,'Nuno'),
	(10,'Joana'),
	(11,'Filipe'),
	(12,'Beatriz'),
	(13,'Maria Alice'),
	(14,'Fernando'),
	(15,'Rui'),
	(16,'Francisca'),
	(17,'Mariana'),
    (18,'Santiago'),
    (19,'Manuel'),
    (20,'Rafael');
    
select * from tecnicos

-- insert na table localizacoes
insert into localizacoes(cod_lince, dataLclz, horas, longitude, latitude)
values
    (1, '2009-10-01', 6, 55.2341, 11.4444),
    (2, '2010-08-02', 12, 59.2341, 15.4444),
    (3, '2010-10-01', 18, 22.2341, 35.4444),
    (4, '2009-10-01', 24, 45.2341, 36.4444),
    (5, '2015-10-01', 6, 77.2341, 77.4444),
    (6, '2016-10-01', 12, 66.2341, 26.4444),
    (7, '2016-10-01', 18, 88.2341, 22.4444),
    (8, '2018-10-01', 24, 33.2341, 21.4444),
    (9, '2019-10-01', 6, 21.2341, 63.4444),
    (10, '2020-10-01', 12, 13.2341, 76.4444),
    (11, '2015-10-01', 18, 59.2341, 15.4444),
    (12, '2016-10-01', 24, 34.2233, 55.4223),
    (13, '2019-10-02', 6, 44.2233, 33.4223),
    (14, '2020-10-01', 12, 66.2233, 36.4223),
    (15, '2020-10-01', 18, 76.2233, 63.4223),
    (16, '2022-01-05', 24, 78.2233, 23.4223),
    (17, '2022-04-05', 6, 24.2233, 52.4223),
    (18, '2022-01-09', 12, 21.2341, 63.4444);

select * from localizacoes

-- insert na table controlos
insert into controlos(cod_lince, cod_Tecnico, dataCntrl, peso, estadoSaude)
values
    (1, 1, '2015-02-10', 20, 'Saudavel'),
    (1, 2, '2015-03-10', 22, 'Saudavel'),
    (2, 1, '2015-04-15', 23, 'Saudavel'),
    (2, 4, '2015-05-15', 14, 'Doente'),
    (3, 3, '2015-06-19', 19, 'Saudavel'),
    (3, 5, '2015-07-18', 19, 'Saudavel'),
    (4, 5, '2015-08-17', 18, 'Saudavel'),
    (4, 6, '2016-07-16', 25, 'Saudavel'),
    (5, 6, '2016-01-15', 25, 'Saudavel'),
    (5, 8, '2016-02-14', 25, 'Saudavel'),
    (6, 9, '2016-03-13', 27, 'Doente'),
    (6, 10, '2016-04-10', 20, 'Saudavel'),
    (7, 7, '2016-01-13', 19, 'Saudavel'),
    (7, 8, '2016-01-11', 19, 'Doente'),
    (8, 7, '2016-01-11', 18, 'Saudavel'),
    (8, 1, '2016-01-16', 18, 'Saudavel'),
    (9, 2, '2016-01-18', 23, 'Saudavel'),
    (9, 11, '2016-01-10', 23, 'Doente'),
    (10, 11, '2017-01-20', 20, 'Saudavel'),
    (10, 10, '2017-01-22', 19, 'Doente'),
    (11, 13, '2017-01-22', 19, 'Doente'),
    (11, 12, '2017-01-26', 18, 'Saudavel'),
    (12, 12, '2017-01-27', 18, 'Saudavel'),
    (12, 15, '2017-01-20', 21, 'Saudavel'),
    (13, 15, '2018-01-10', 21, 'Doente'),
    (13, 16, '2018-01-10', 21, 'Saudavel'),
    (14, 16, '2019-01-19', 20, 'Saudavel'),
    (14, 14, '2019-01-19', 19, 'Doente'),
    (15, 14, '2020-11-11', 19, 'Saudavel'),
    (15, 15, '2020-11-11', 18, 'Saudavel'),
    (16, 17, '2021-11-11', 18, 'Saudavel'),
    (16, 18, '2021-11-11', 20, 'Doente'),
    (17, 18, '2022-01-09', 20, 'Saudavel'),
    (17, 19, '2022-01-09', 20, 'Saudavel'),
    (18, 19, '2022-01-09', 19, 'Doente'),
    (18, 20, '2022-01-09', 19, 'Doente');

select * from controlos

commit;


-- PROCEDIMENTOS

/* Registar_Lince – a ser invocado sempre que nascer um novo lince */
create function Registar_Lince(name varchar(20), gender varchar(10), birthday date, death date, father int, mother int)
returns void
begin
    insert into linces
    values
        (name, gender, birthday, death, father, mother);
end;

/*Agendar_Controlo – a ser invocado para agendar um controlo para um dado lince, numa dada data.*/
create function Agendar_Controlo(id_lince int, id_tecnico int, data date)
returns void
begin
    insert into controlos
    values
        (id_lince, id_tecnico, data, null, null);
end;

/*Registar_Controlo – a ser invocado para registar os dados de um controlo previamente agendado.*/
create function Registar_controlo(id_lince int, id_tecnico int, weight decimal(4,2), healthCondition varchar(7))
returns void
begin
    update linces
    set peso = weight, estadoSaude = healthCondition;
    where cod_lince = id_linc and cod_Tecnico = id_tecnico;
end;
    

-- Respostas questões em SQL
-- Q1 Nome e género dos linces em que ambos os progenitores ainda estão vivos?

select l.nome, l.genero
from linces l
where l.cod_pai in (select cod_lince
                    from linces
                    where genero = 'Masculino' and dataObito is null)
    and l.cod_mae in (select cod_lince
                    from linces
                    where genero = 'Feminino' and dataObito is null);

-- Q2 Nome e género dos linces em que apenas um dos progenitores ainda está vivo?

select l.nome, l.genero
from linces l
where l.cod_pai in (select cod_lince
                    from linces
                    where genero = 'Masculino' and dataObito is not null)
    and l.cod_mae in (select cod_lince
                     from linces
                     where genero = 'Feminino' and dataObito is null)
union

select l.nome, l.genero
from linces l
where l.cod_mae in (select cod_lince
                    from linces
                    where genero = 'Feminino' and dataObito is not null)
    and l.cod_pai in (select cod_lince
                     from linces
                     where genero = 'Masculino' and dataObito is null);


-- Q3  Para cada lince do tipo macho (id_lince, lince) apresentar o número de filhotes de que é pai (Nº de filhotes).

select l.cod_lince, l.nome, count(*) as "Nº de filhotes"
from linces l
where l.genero = "Masculino"
    and l.cod_lince in (select cod_pai
                        from linces)
group by l.cod_lince
                        

-- (1,'Luck', 4)
-- (3,'Red', 4)
-- (7,'Cooper', 2)
-- (8,'Charlie', 2)
-- (11,'Buddy', 1)
-- (16,'Rocky', 1)


-- Q4 Quais os linces do tipo fêmea (id_lince, lince) que no último controlo realizado tinham peso superior à média dos controlos anteriores?

select distinct l.cod_lince, l.nome
from linces l
inner join controlos on l.cod_lince = controlos.cod_lince
where l.genero = "Feminino" 
    and controlos.peso < controlos.peso in (select c.peso
                                            from controlos c
                                            where c.dataCntrl = controlos.dataCntrl)
                                            
                                            
                                            
                                            
                                            
DELIMITER $$

CREATE PROCEDURE Registar_Lince_Mingos(IN p_nome VARCHAR(20), IN p_genero VARCHAR(15), IN p_dataNasc DATE, IN p_cod_pai INT, IN p_cod_mae INT)
BEGIN
	INSERT INTO linces(nome, genero, dataNasc, cod_pai, cod_mae) VALUES (p_nome, p_genero ,p_dataNasc, p_cod_pai ,p_cod_mae);
END $$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE Agendar_Controlo_Mingos(IN p_cod_lince INT, IN p_dataControl DATE)
BEGIN

	IF (Lince_Vivo_Mingos(p_cod_lince)) IS TRUE THEN

	INSERT INTO controlos(cod_lince, dataControl) VALUES (p_cod_lince, p_dataControl);
    
    END IF;

END $$

DELIMITER ;

DELIMITER $$

CREATE FUNCTION Lince_Vivo_Mingos(f_cod_lince int)
RETURNS BOOL
BEGIN
    DECLARE f_dataObito DATE;
    
    SELECT dataObito
    INTO f_dataObito
    FROM linces
    WHERE cod_lince = f_cod_lince;
    
    IF (f_dataObito IS NULL) THEN
        RETURN(TRUE);
    ELSE
        RETURN(FALSE);
    END IF;
    
END $$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE Registrar_Controlo(IN cod_lince INT, IN p_data
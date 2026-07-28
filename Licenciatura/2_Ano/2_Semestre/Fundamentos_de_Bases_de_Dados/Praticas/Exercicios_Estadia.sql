-- Exercicio de Estadia


 -- a) 

drop database if exists fugaspt;
create database fugaspt;
use fugaspt;

 -- b) 

drop database if exists fugaspt;
create database fugaspt;
use fugaspt;

create table tipos_de_alojamento(
num_tipo int,
tipo varchar(20),
primary key(num_tipo)
);
create table regioes(
num_regiao int,
nome varchar(50) unique,
primary key (num_regiao)
);
create table proprietarios(
num_proprietario int,
nome varchar(50),
email varchar(50),
telfone int,
primary key(num_proprietario)
);
create table clientes(
num_cliente int,
nome varchar(50),
morada varchar(50),
email varchar(50),
nif '999999999',
telefone int,
primary key(num_cliente)
);

create table alojamentos(
num_alojamento int,
nome varchar(50),
morada varchar(50),
num_regiao int,
num_tipo int,
num_proprietario int,
estrelas int null,
capacidade int,
descricao varchar(100),
preco1 float(5,2),
preco2 float(5,2),
preco3 float(5,2),
primary key(num_alojamento),
foreign key(num_regiao) references regioes(num_regiao),
foreign key(num_tipo) references tipos_de_alojamento(num_tipo),
foreign key(num_proprietario) references proprietarios(num_proprietario)
);
create table estadias(
num_reserva int,
num_cliente int,
num_alojamento int,
data_reserva date,
data_entrada date,
data_saida date,
valor_pago float(5,2),
primary key (num_reserva),
foreign key(num_cliente) references clientes(num_cliente),
foreign key(num_alojamento) references alojamentos(num_alojamento)
);
create table apreciacoes(
num_reserva int,
email_ocupante varchar(50),
nome_ocupante varchar(50),
apreciacao varchar(200),
primary key(num_reserva,email_ocupante),
foreign key(num_reserva) references estadias(num_reserva)
);
insert into regioes values('1','douro');
insert into regioes values('2','minho');
insert into tipos_de_alojamento values('1','classico');
insert into tipos_de_alojamento values('2','rustico');
insert into proprietarios values('1','joao sousa','joao@gmail.com','919919299');
insert into proprietarios values('2','ricardo sousa','ricardo@gmail.com','915519299');
insert into proprietarios values('3','helder sousa','helder@gmail.com','919779299');
insert into clientes values('300','rui silva','2569685','rui@gmail.com','123456789');
insert into clientes values('301','helder silva','2569686','helder@gmail.com','123356789');
insert into estadias values('01','300','0000','2017-01-01','2017-01-15','2017-01-26','45');
insert into estadias values('02','300','0000','2017-01-02','2017-02-16','2017-02-27','60');
insert into estadias values('03','301','0000','2017-01-03','2017-01-17','2017-01-28','100');
insert into alojamentos values('0000','vistaboa','rua da azenha','1','1','1','4','100','boa vista para o rio','45','60','100');
insert into alojamentos values('0000','vistaboa','rua da liberdade','2','1','1','4','100','boa vista para o rio','45','60','100');
insert into alojamentos values('0000','vistaboa','rua 25 abril','1','2','1','4','100','boa vista para o rio','45','60','100');
insert into alojamentos values('0000','vistaboa','rua dos combatentes','1','1','1','4','100','boa vista a montanha','45','60','100');
insert into apreciacoes values('01','rui@gmail','rui','gostei');
insert into apreciacoes values('01','rui@gmail','rui','gostei');
insert into apreciacoes values('02','rui@gmail','rui','nao gostei');
insert into apreciacoes values('03','helder@gmail','helder','gostei muito');

  -- c) 

select count(*)
from estadias
where num_alojamento='1234';

  -- d) 

select num_alojameto,data_entrada,data_saida sum(valor_pago)
from estadias
where (num_alojameto='5678' and data_entrada>'01-01-2916' and data_saida<'31-03-2016');

  -- e) 

select num_cliente
from clientes
alter num_cliente where num_cliente='300';

select email_ocupante
from apreciacoes
alter email_ocupante where email_ocupante='helder@gmail.com';

select num_regiao
from regioes
alter num_regiao where num_regiao='1';

  -- f) 

delete from clientes 
where num_cliente='300';

delete from alojamentos 
where num_alojamento='0000';

delete from estadias
where num_reserva='01';

  -- g) 

drop table tipos_de_alojamento;
drop table regioes;
drop table proprietarios;
drop table clientes;

-- Parte 2

-- 1 -- 

drop view if exists filial_mais_saidas;
delimiter @
create view filial_mais_saidas(filial_saida)
AS SELECT Count(filial_saida)
from alugueres
group by filial_saida;
@
delimiter ;
Select max(filial_saida)
	from filial_mais_saidas;

-- 2 -- 

DROP FUNCTION IF EXISTS valor_por_km;
DELIMITER @
Create function valor_por_km(km int)
returns int 
begin 
declare pr_km decimal(4,2);
declare fkms int;
declare ikms int;
declare total;
select kms_i into ikms from alugueres;
select kms_devolucao into fkms from alugueres;
select preco_km into pr_km from precos;
total=(fkms-ikms);
if (total>minkms and total<maxkms) then
return pr_km WHERE alugueres.cod_preco=preco.cod_preco;
end if;
end;
@
DELIMITER ;

Drop function if exists valor_kilometragem
DELIMITER @
create function valor_kilometragem(nalug)
returns decimal(5,2)
begin

declare pr decimal(4,2);
declare band decimal(4,2);
declare consumo int;
declare idade int;
select euros_consumo into consumo from alugueres;
select pr_km into pr from valor_por_km;
select ano into idade from viaturas;
if((curdate() -ano)>3) then
select euros_bandeirada into band from alugueres where num_aluguer=nalug
 return (band+pr+consumo);
 else return (pr+consumo);
 end if;
 end;
 @
 DELIMITER ;

-- 3 -- 

drop procedure if exists abrir_aluguer;
DELIMITER @
CREATE PROCEDURE abrir_aluguer(in mat char(8),cod_cl char(10),filial_exit char(1),ban decimal(5,2),ikms int)
begin
declare mat char(8);
declare cod_cl char(10);
declare filial_exit(1);
declare ikms int;
declare ban decimal(5,2);
select matricula
into mat from viaturas where viaturas.matricula=mat;
select cod_cli into cod_cl from clientes where clientes.cod_cli=cod_cl;
select cod_filial into filial_exit from filiais where cod_filial.filiais=filial_exit;
select bandeirada into ban from viaturas where viaturas.matricula=mat;
select kms_acumulados into ikms from viaturas where viaturas.matricula=mat;
insert into alugueres values(max(num_aluguer+1),'mat',cod_cl,null,'filial_exit',null,band,null,now(),'ikms',null);
end;
@ delimiter ;


-- 4 -- 

drop procedure if exists fechar_aluguer;
DELIMITER @
CREATE PROCEDURE fechar_aluguer(num_aluguer)
begin
declare cod_pre int;
declare fil_entr int;
select cod_filial
into fil_entr
from filiais;
select cod_preco
into cod_pre
from precos;

Update alugueres values(null,null,null,cod_pre,null,fil_entr,euros_consumo,euros_bandeirada,null,now(),null,kms_devolucao);
end@
DELIMITER;

-- 5 -- 

drop trigger if exists clientes_vip;
DELIMITER @
CREATE TRIGGER clientes_vip
before insert on alugueres
for each row
begin
declare num_alug_fin int;
declare band decimal(5,2);

select cod_cli,count(*)
into num_alug_fin
from alugueres
where data_devolucao is not null
group by cod_cli;

IF(num_alug_fin >3) then
select bandeirada 
into band 
from viaturas 
where viaturas.matricula=alugueres.matricula;
set new.bandeirada=null;
end if;
end@ 
DELIMITER ;
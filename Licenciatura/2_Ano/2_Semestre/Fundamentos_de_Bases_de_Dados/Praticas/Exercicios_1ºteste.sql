Modelo Relacional

Docente(n_mec, nome, telemovel, cod_dep)
Departamento(cod_dep, Designacao)
Vigilancia(n_mec, n_prova, cod_vigilancia)
UC(cod_uc, designacao,alunos)
Prova( tipo, cod_prova, cod_sala_cod_uc)
Sala( cod_sala, capacaidade, n_edificio)

Perguntas em sql:

 1 - Quais as unidades curriculares(cod_uc e designacao) em que participaram docentes do departamento de Matemática como vigilantes?
 
WITH docente_matematica AS (
    SELECT n_mec
    FROM Docente
    JOIN Departamento ON Docente.cod_dep = Departamento.cod_dep
    WHERE Departamento.Designacao = 'Matemática'
),
vigilancia_docente_matematica AS (
    SELECT n_mec, cod_prova
    FROM Vigilancia
    WHERE n_mec IN (SELECT n_mec FROM docente_matematica)
)
SELECT cod_uc, designacao
FROM UC
WHERE cod_uc IN (
    SELECT cod_sala_cod_uc
    FROM Prova
    WHERE cod_prova IN (SELECT cod_prova FROM vigilancia_docente_matematica)
);


 
 
 
 2 - Quais os docentes do departamento de Matemática(num_mecanog e nome) que já fizeram vigilâncias em todas as salas que existem na EEUM?
 
 WITH docente_matematica AS (
    SELECT n_mec
    FROM Docente
    JOIN Departamento ON Docente.cod_dep = Departamento.cod_dep
    WHERE Departamento.Designacao = 'Matemática'
),
salas_eeum AS (
    SELECT cod_sala
    FROM Sala
),
vigilancia_docente_matematica_sala AS (
    SELECT n_mec, cod_sala
    FROM Vigilancia
    JOIN Prova ON Vigilancia.cod_prova = Prova.cod_prova
    JOIN Sala ON Prova.cod_sala_cod_uc = Sala.cod_sala
    WHERE n_mec IN (SELECT n_mec FROM docente_matematica)
)
SELECT n_mec, nome
FROM Docente
WHERE n_mec IN (SELECT n_mec FROM docente_matematica)
AND NOT EXISTS (
    SELECT *
    FROM salas_eeum
    WHERE cod_sala NOT IN (SELECT cod_sala FROM vigilancia_docente_matematica_sala)
);

 
 3 - Quais os docentes do departamento de Física(num_mecanog e nome) que não fizeram quaisquer vigilâncias em todas as salas que existem na EEUM?
  
  
  WITH docente_fisica AS (
    SELECT n_mec
    FROM Docente
    JOIN Departamento ON Docente.cod_dep = Departamento.cod_dep
    WHERE Departamento.Designacao = 'Física'
),
salas_eeum AS (
    SELECT cod_sala
    FROM Sala
)
SELECT n_mec, nome
FROM docente_fisica
WHERE NOT EXISTS (
    SELECT *
    FROM salas_eeum
    WHERE cod_sala IN (
        SELECT cod_sala
        FROM Vigilancia
        JOIN Prova ON Vigilancia.cod_prova = Prova.cod_prova
        JOIN Sala ON Prova.cod_sala_cod_uc = Sala.cod_sala
        WHERE n_mec IN (SELECT n_mec FROM docente_fisica)
    )
);

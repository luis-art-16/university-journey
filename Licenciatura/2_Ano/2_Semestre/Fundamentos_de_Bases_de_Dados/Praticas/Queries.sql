--E a) -- Listar os funcionários (nºfunc e nome) por ordem decrescente de valor despendido em compras até ao momento

SELECT n_funcionario, nome
FROM funcionarios
JOIN Encomenda ON funcionarios.n_funcionario = Encomenda.n_funcionario
GROUP BY funcionarios.n_funcionario, funcionarios.nome
ORDER BY SUM(Encomenda.preco) DESC;



--E b) -- Quais os fornecedores(designação) que já fizeram entregas mais de 30 dias após a realização
       -- das respetivas encomendas? Quais os artigos encomendados(descrição) e respetivas quantidades?

SELECT
  Fornecedor.designacao_forncedor,
  Artigo.designacao_artigo,
  Encomenda.quantidade
FROM Encomenda
JOIN Fornecedor ON Encomenda.n_fornecedor = Fornecedor.n_fornecedor
JOIN Artigo ON Encomenda.n_artigo = Artigo.n_artigo
JOIN Envio ON Encomenda.n_encomenda = Envio.n_encomenda
WHERE Envio.data_entrega_real - Encomenda.data_encomenda > 30; 
-- o parâmaetro data_entrega_real / data_encomenda não foram descritos no modelo relacional



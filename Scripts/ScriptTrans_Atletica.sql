--Transação 1: Registro de Novo Evento com Participação de Equipe e Compra de Produtos

--Nesta transação, estaremos registrando um novo evento, atribuindo uma equipe a ele e registrando a compra de produtos para o evento.

BEGIN;

-- Operação 1: Registrar um novo evento
INSERT INTO Evento (tipo, departamento_marketing_id) VALUES ('Festa 60 é 100', 2);

-- Operação 2: Atribuir uma equipe ao evento
INSERT INTO ParticipacaoEvento (equipe_id, evento_id) VALUES (3, (SELECT id FROM Evento WHERE tipo = 'Festa 60 é 100'));

-- Operação 3: Registrar a compra de produtos para o evento
INSERT INTO CompraFornecedor (fornecedor_id, produto_id, quantidade, valor_total, data_compra) VALUES (2, 3, 100, 3000.00, CURRENT_DATE);

COMMIT;

--Transação 2: Venda de Produtos

--Nesta transação, estaremos registrando uma venda de produtos para um usuário específico.

BEGIN;

-- Operação 1: Registrar uma venda de produtos
INSERT INTO VendaProduto (produto_id, usuario_id, quantidade, valor_total, data_venda) VALUES (1, 2, 2, 50.00, CURRENT_DATE);

-- Operação 2: Atualizar a quantidade de produtos após a venda
UPDATE Produto SET quantidade = quantidade - 2 WHERE id = 1;

-- Operação 3: Anexar o comprovante da venda
UPDATE VendaProduto SET comprovante_venda = 'DADOS DO COMPROVANTE' WHERE id = (SELECT MAX(id) FROM VendaProduto);

COMMIT;

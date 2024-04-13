BEGIN;

-- Inserts para a tabela Usuario
INSERT INTO Usuario (nome, dt_nascimento, sexo, foto_perfil) VALUES ('João Silva', '1990-05-15', 'M', NULL);
COMMIT;

BEGIN;
INSERT INTO Usuario (nome, dt_nascimento, sexo, foto_perfil) VALUES ('Maria Oliveira', '1992-08-20', 'F', NULL);
COMMIT;

BEGIN;
INSERT INTO Usuario (nome, dt_nascimento, sexo, foto_perfil) VALUES ('Pedro Santos', '1995-03-10', 'M', NULL);
COMMIT;

BEGIN;
-- Inserts para a tabela Visitante
INSERT INTO Visitante (usuario_id, eh_estudante, cidade_origem) VALUES (1, TRUE, 'São Paulo');
COMMIT;

BEGIN;
INSERT INTO Visitante (usuario_id, eh_estudante, cidade_origem) VALUES (2, FALSE, 'Rio de Janeiro');
COMMIT;

BEGIN;
INSERT INTO Visitante (usuario_id, eh_estudante, cidade_origem) VALUES (3, TRUE, 'Belo Horizonte');
COMMIT;

BEGIN;
-- Inserts para a tabela Aluno
INSERT INTO Aluno (usuario_id, curso, matricula, comprovante_vinculo, data_ingresso) VALUES (1, 'Engenharia Civil', 'EC123', NULL, '2019-02-10');
COMMIT;

BEGIN;
INSERT INTO Aluno (usuario_id, curso, matricula, comprovante_vinculo, data_ingresso) VALUES (3, 'Administração', 'ADM456', NULL, '2020-01-15');
COMMIT;

BEGIN;
-- Inserts para a tabela Equipe
INSERT INTO Equipe (nome, modalidade, cor_uniforme) VALUES ('Time A', 'Futebol', 'Azul');
COMMIT;

BEGIN;
INSERT INTO Equipe (nome, modalidade, cor_uniforme) VALUES ('Time B', 'Vôlei', 'Vermelho');
COMMIT;

BEGIN;
-- Inserts para a tabela Atleta
INSERT INTO Atleta (aluno_id, equipe_id, peso, altura) VALUES (1, 1, 75.5, 1.85);
COMMIT;

BEGIN;
INSERT INTO Atleta (aluno_id, equipe_id, peso, altura) VALUES (3, 2, 68.2, 1.75);
COMMIT;

BEGIN;
-- Inserts para a tabela Funcionario
INSERT INTO Funcionario (aluno_id, cargo, departamento) VALUES (1, 'Técnico', 101);
COMMIT;

BEGIN;
INSERT INTO Funcionario (aluno_id, cargo, departamento) VALUES (3, 'Secretário', 102);
COMMIT;

BEGIN;
-- Inserts para a tabela DepartamentoMarketing
INSERT INTO DepartamentoMarketing (orcamento) VALUES (50000.00);
COMMIT;

BEGIN;
INSERT INTO DepartamentoMarketing (orcamento) VALUES (75000.00);
COMMIT;

BEGIN;
-- Inserts para a tabela Evento
INSERT INTO Evento (tipo, departamento_marketing_id) VALUES ('Feira Cultural', 1);
COMMIT;

BEGIN;
INSERT INTO Evento (tipo, departamento_marketing_id) VALUES ('Campeonato Esportivo', 2);
COMMIT;

BEGIN;
-- Inserts para a tabela ParticipacaoEvento
INSERT INTO ParticipacaoEvento (equipe_id, evento_id) VALUES (1, 1);
COMMIT;

BEGIN;
INSERT INTO ParticipacaoEvento (equipe_id, evento_id) VALUES (2, 2);
COMMIT;

BEGIN;
-- Inserts para a tabela Local
INSERT INTO Local (endereco, data_entrada, data_saida) VALUES ('Rua Principal, 123, São Paulo', '2024-05-10', '2024-05-15');
COMMIT;

BEGIN;
INSERT INTO Local (endereco, data_entrada, data_saida) VALUES ('Avenida Central, 456, Rio de Janeiro', '2024-06-20', '2024-06-25');
COMMIT;

BEGIN;
-- Inserts para a tabela Patrimonio
INSERT INTO Patrimonio (valor_unitario, descricao, quantidade) VALUES (100.00, 'Computador', 20);
COMMIT;

BEGIN;
INSERT INTO Patrimonio (valor_unitario, descricao, quantidade) VALUES (50.00, 'Cadeira', 50);
COMMIT;

BEGIN;
-- Inserts para a tabela UsoPatrimonio
INSERT INTO UsoPatrimonio (evento_id, patrimonio_id, atleta_id, quantidade) VALUES (1, 1, 1, 10);
COMMIT;

BEGIN;
INSERT INTO UsoPatrimonio (evento_id, patrimonio_id, atleta_id, quantidade) VALUES (2, 2, 3, 20);
COMMIT;

BEGIN;
-- Inserts para a tabela Produto
INSERT INTO Produto (nome, valor_unitario, descricao, quantidade, tamanho) VALUES ('Camiseta Esportiva', 25.00, 'Camiseta para prática esportiva', 100, 'M');
COMMIT;

BEGIN;
INSERT INTO Produto (nome, valor_unitario, descricao, quantidade, tamanho) VALUES ('Tênis de Corrida', 150.00, 'Tênis especializado para corrida', 50, '42');
COMMIT;

BEGIN;
-- Inserts para a tabela Fornecedor
INSERT INTO Fornecedor (nome_fantasia, cnpj, cidade, estado, telefone) VALUES ('Fornecimento Ltda.', '12345678901234', 'São Paulo', 'SP', '(11) 1234-5678');
COMMIT;

BEGIN;
INSERT INTO Fornecedor (nome_fantasia, cnpj, cidade, estado, telefone) VALUES ('Equipamentos Esportivos SA', '98765432109876', 'Rio de Janeiro', 'RJ', '(21) 8765-4321');
COMMIT;

BEGIN;
-- Inserts para a tabela VendaProduto
INSERT INTO VendaProduto (produto_id, usuario_id, quantidade, valor_total, data_venda, comprovante_venda) VALUES (1, 1, 2, 50.00, '2024-04-10', NULL);
COMMIT;

BEGIN;
INSERT INTO VendaProduto (produto_id, usuario_id, quantidade, valor_total, data_venda, comprovante_venda) VALUES (2, 2, 1, 150.00, '2024-04-12', NULL);
COMMIT;

BEGIN;
-- Inserts para a tabela CompraFornecedor
INSERT INTO CompraFornecedor (fornecedor_id, produto_id, quantidade, valor_total, data_compra) VALUES (1, 1, 50, 1250.00, '2024-03-20');
COMMIT;

BEGIN;
INSERT INTO CompraFornecedor (fornecedor_id, produto_id, quantidade, valor_total, data_compra) VALUES (2, 2, 20, 3000.00, '2024-03-25');
COMMIT;

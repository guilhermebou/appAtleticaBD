--Procedure 1:
--Registra a participação de uma equipe em um evento.

CREATE OR REPLACE PROCEDURE RegistrarParticipacaoEvento (
    IN p_equipe_id INTEGER,
    IN p_evento_id INTEGER,
    IN p_patrimonio_id INTEGER,
    IN p_atleta_id INTEGER,
    IN p_quantidade_patrimonios INTEGER
)
AS
BEGIN
    INSERT INTO ParticipacaoEvento (equipe_id, evento_id)
    VALUES (p_equipe_id, p_evento_id);

    INSERT INTO UsoPatrimonio (evento_id, patrimonio_id, atleta_id, quantidade)
    VALUES (p_evento_id, p_patrimonio_id, p_atleta_id, p_quantidade_patrimonios);
END;


--Procedure 2:
--Registra uma compra de produtos de um fornecedor.

CREATE OR REPLACE PROCEDURE registrar_compra_fornecedor(
    IN fornecedor_id INTEGER,
    IN produto_id INTEGER,
    IN quantidade INTEGER,
    IN valor_total DECIMAL,
    IN data_compra DATE
)
AS $$
BEGIN
    INSERT INTO CompraFornecedor (fornecedor_id, produto_id, quantidade, valor_total, data_compra)
    VALUES (fornecedor_id, produto_id, quantidade, valor_total, data_compra);
END;
$$
LANGUAGE plpgsql;

--Procedure 3:
--Permite registrar a entrada e saída de patrimônio em um local específico.


CREATE OR REPLACE PROCEDURE RegistrarMovimentacaoPatrimonio (
    IN p_patrimonio_id INTEGER,
    IN p_local_id INTEGER,
    IN p_data_entrada DATE,
    IN p_data_saida DATE
)
AS
BEGIN
    INSERT INTO MovimentacaoPatrimonio (patrimonio_id, local_id, data_entrada, data_saida)
    VALUES (p_patrimonio_id, p_local_id, p_data_entrada, p_data_saida);
END;

--Procedure 4:
--Retorna os dados de um aluno e sua equipe associada.

CREATE OR REPLACE PROCEDURE atualizar_info_atleta(
    IN p_aluno_id INTEGER,
    IN p_peso DECIMAL(5, 2),
    IN p_altura DECIMAL(5, 2)
)
AS $$
BEGIN
    UPDATE Atleta
    SET peso = p_peso, altura = p_altura
    WHERE aluno_id = p_aluno_id;
END;
$$ LANGUAGE plpgsql;



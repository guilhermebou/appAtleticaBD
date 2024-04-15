--Trigger 1:
--É acionado antes de excluir um aluno e verifica se ele está participando de algum evento.

CREATE OR REPLACE FUNCTION verificar_participacao_evento()
RETURNS TRIGGER AS $$
DECLARE
    participacao_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO participacao_count
    FROM ParticipacaoEvento
    WHERE equipe_id = (
        SELECT equipe_id FROM Atleta
        WHERE aluno_id = OLD.usuario_id
    );
    
    IF participacao_count > 0 THEN
        RAISE EXCEPTION 'Não é possível excluir o aluno, pois ele está participando de eventos.';
    END IF;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER excluir_aluno_trigger
BEFORE DELETE ON Aluno
FOR EACH ROW
EXECUTE FUNCTION verificar_participacao_evento();

--Trigger 2:
--Calcula  o valor total de uma venda assim que ela é realizada

CREATE OR REPLACE FUNCTION calcular_valor_total()
RETURNS TRIGGER AS $$
BEGIN
    
    SELECT valor_unitario INTO NEW.valor_total
    FROM Produto
    WHERE id = NEW.produto_id;

    NEW.valor_total = NEW.quantidade * NEW.valor_total;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_calcular_valor_total
BEFORE INSERT ON VendaProduto
FOR EACH ROW
EXECUTE FUNCTION calcular_valor_total();

--Trigger 3:
--É acionada sempre que um novo atleta é adicionado à tabela Atleta. Ela registra automaticamente a participação desse atleta em um evento na tabela ParticipacaoEvento, com base na equipe à qual o atleta pertence e no evento em que ele está participando.

CREATE OR REPLACE FUNCTION registrar_participacao_evento()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO ParticipacaoEvento (equipe_id, evento_id)
    VALUES (NEW.equipe_id, NEW.evento_id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER registrar_entrada_atleta_evento
AFTER INSERT ON Atleta
FOR EACH ROW
EXECUTE FUNCTION registrar_participacao_evento();

--Trigger 4:
--Verifica se a quantidade de um patrimonio é suficiente antes de usa-lo em um evento

CREATE OR REPLACE FUNCTION verificar_quantidade_patrimonio()
RETURNS TRIGGER AS $$
DECLARE
    quantidade_patrimonio INTEGER;
BEGIN
    SELECT quantidade INTO quantidade_patrimonio
    FROM Patrimonio
    WHERE id = NEW.patrimonio_id;

    IF quantidade_patrimonio < NEW.quantidade THEN
        RAISE EXCEPTION 'Quantidade de patrimônio insuficiente!';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER verificar_quantidade_patrimonio_trigger
BEFORE INSERT ON UsoPatrimonio
FOR EACH ROW
EXECUTE FUNCTION verificar_quantidade_patrimonio();





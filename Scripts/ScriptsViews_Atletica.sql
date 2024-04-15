--Visão 1:
--Retorna informações sobre o uso de patrimônios durante eventos, incluindo o tipo de patrimônio, a quantidade utilizada e o evento associado.

CREATE VIEW UsoPatrimonioPorEvento AS
SELECT
    e.id AS evento_id,
    e.tipo AS tipo_evento,
    p.id AS patrimonio_id,
    p.descricao AS descricao_patrimonio,
    up.quantidade AS quantidade_utilizada
FROM
    Evento e
INNER JOIN
    UsoPatrimonio up ON e.id = up.evento_id
INNER JOIN
    Patrimonio p ON up.patrimonio_id = p.id;

--Visão 2:
--Retorna uma lista de atletas e suas respectivas equipes que participaram de eventos.

CREATE VIEW AtletasEquipesParticipantes AS
SELECT
    a.aluno_id AS atleta_id,
    u.nome AS nome_atleta,
    eq.id AS equipe_id,
    eq.nome AS nome_equipe,
    e.id AS evento_id,
    e.tipo AS tipo_evento
FROM
    Atleta a
INNER JOIN
    Aluno al ON a.aluno_id = al.usuario_id
INNER JOIN
    Usuario u ON al.usuario_id = u.id
INNER JOIN
    Equipe eq ON a.equipe_id = eq.id
INNER JOIN
    ParticipacaoEvento pe ON eq.id = pe.equipe_id
INNER JOIN
    Evento e ON pe.evento_id = e.id;
	
--Visão 3:
--Fornece um relatório das vendas realizadas

CREATE VIEW RelatorioVendas AS
SELECT U.nome AS NomeCliente,P.nome AS Produto
	, VP.quantidade AS Quantidade
	, VP.valor_total AS ValorTotal
	, VP.data_venda AS DataVenda
FROM VENDAPRODUTO VP
INNER JOIN USUARIO U ON VP.usuario_id = U.id
INNER JOIN PRODUTO P ON P.id = VP.produto_id

--Visão 4:
--Fornece um relatório sobre os atletas cadastrados, incluindo detalhes sobre sua equipe e informações pessoais.

CREATE VIEW RelatorioAtletas AS
SELECT 
    A.aluno_id AS id_atleta,
    U.nome AS nome_atleta,
    U.dt_nascimento AS data_nascimento,
    U.sexo AS sexo,
    E.nome AS equipe,
    A.peso AS peso,
    A.altura AS altura
FROM Atleta A
INNER JOIN Aluno AL ON A.aluno_id = AL.usuario_id
INNER JOIN Usuario U ON AL.usuario_id = U.id
INNER JOIN Equipe E ON A.equipe_id = E.id;



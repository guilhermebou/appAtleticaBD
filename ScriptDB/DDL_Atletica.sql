-- Tabela: Usuario
CREATE TABLE Usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    dt_nascimento DATE NOT NULL,
    sexo CHAR(1) NOT NULL CHECK (sexo IN ('M', 'F')),
    foto_perfil BYTEA
);

-- Tabela: Visitante
CREATE TABLE Visitante (
    usuario_id INTEGER PRIMARY KEY,
	eh_estudante BOOLEAN,
	cidade_origem VARCHAR(100),
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id) ON DELETE CASCADE
);

-- Tabela: Aluno
CREATE TABLE Aluno (
    usuario_id INTEGER PRIMARY KEY,
    curso VARCHAR(100) NOT NULL,
    matricula VARCHAR(20) NOT NULL,
    comprovante_vinculo BYTEA,
	data_ingresso DATE,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id) ON DELETE CASCADE
);

-- Tabela: Equipe
CREATE TABLE Equipe (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    modalidade VARCHAR(100) NOT NULL,
    cor_uniforme VARCHAR(50) NOT NULL
);

-- Tabela: Atleta
CREATE TABLE Atleta (
    aluno_id INTEGER PRIMARY KEY,
    equipe_id INTEGER NOT NULL,
	peso DECIMAL(5,2),
    altura DECIMAL(5,2),
    FOREIGN KEY (aluno_id) REFERENCES Aluno(usuario_id) ON DELETE CASCADE,
	FOREIGN KEY (equipe_id) REFERENCES Equipe(id) ON DELETE CASCADE
);

-- Tabela: Funcionario
CREATE TABLE Funcionario (
    aluno_id INTEGER PRIMARY KEY,
    cargo VARCHAR(100) NOT NULL,
    departamento INTEGER NOT NULL,
    FOREIGN KEY (aluno_id) REFERENCES Aluno(usuario_id) ON DELETE CASCADE
);

-- Tabela: DepartamentoMarketing
CREATE TABLE DepartamentoMarketing (
    id SERIAL PRIMARY KEY,
    orcamento DECIMAL(10, 2) NOT NULL
);

-- Tabela: Evento
CREATE TABLE Evento (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(100) NOT NULL,
    departamento_marketing_id INTEGER NOT NULL,
    FOREIGN KEY (departamento_marketing_id) REFERENCES DepartamentoMarketing(id) ON DELETE CASCADE
);

-- Tabela: ParticipacaoEvento
CREATE TABLE ParticipacaoEvento (
    equipe_id INTEGER NOT NULL,
    evento_id INTEGER NOT NULL,
    PRIMARY KEY (equipe_id, evento_id),
    FOREIGN KEY (equipe_id) REFERENCES Equipe(id) ON DELETE CASCADE,
    FOREIGN KEY (evento_id) REFERENCES Evento(id) ON DELETE CASCADE
);

-- Tabela: Local
CREATE TABLE Local (
    id SERIAL PRIMARY KEY,
    endereco VARCHAR(255) NOT NULL,
    data_entrada DATE NOT NULL,
    data_saida DATE NOT NULL
);

-- Tabela: Patrimonio
CREATE TABLE Patrimonio (
    id SERIAL PRIMARY KEY,
    valor_unitario DECIMAL(10, 2) NOT NULL,
    descricao TEXT NOT NULL,
    quantidade INTEGER NOT NULL
);

-- Tabela: UsoPatrimonio
CREATE TABLE UsoPatrimonio (
    evento_id INTEGER,
    patrimonio_id INTEGER,
    atleta_id INTEGER,
    quantidade INTEGER NOT NULL,
    PRIMARY KEY (evento_id, patrimonio_id, atleta_id),
    FOREIGN KEY (evento_id) REFERENCES Evento(id) ON DELETE CASCADE,
    FOREIGN KEY (patrimonio_id) REFERENCES Patrimonio(id) ON DELETE CASCADE,
    FOREIGN KEY (atleta_id) REFERENCES Atleta(aluno_id) ON DELETE CASCADE
);

-- Tabela: Produto
CREATE TABLE Produto (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    valor_unitario DECIMAL(10, 2) NOT NULL,
    descricao TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    tamanho VARCHAR(50)
);

-- Tabela: Fornecedor
CREATE TABLE Fornecedor (
    id SERIAL PRIMARY KEY,
    nome_fantasia VARCHAR(100) NOT NULL,
    cnpj VARCHAR(14) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado CHAR(2) NOT NULL,
    telefone VARCHAR(20) NOT NULL
);

-- Tabela: VendaProduto
CREATE TABLE VendaProduto (
    produto_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    valor_total DECIMAL(10, 2) NOT NULL,
    data_venda DATE NOT NULL,
	comprovante_venda BYTEA,
    PRIMARY KEY (produto_id, usuario_id, data_venda),
    FOREIGN KEY (produto_id) REFERENCES Produto(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id) ON DELETE CASCADE
);

-- Tabela: CompraFornecedor
CREATE TABLE CompraFornecedor (
    fornecedor_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    valor_total DECIMAL(10, 2) NOT NULL,
    data_compra DATE NOT NULL,
    PRIMARY KEY (fornecedor_id, produto_id, data_compra),
    FOREIGN KEY (fornecedor_id) REFERENCES Fornecedor(id) ON DELETE CASCADE,
    FOREIGN KEY (produto_id) REFERENCES Produto(id) ON DELETE CASCADE
);
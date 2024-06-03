-- Criação do Banco de Dados
CREATE DATABASE relatorio_avaliativo;

-- Seleção do Banco de Dados
\c relatorio_avaliativo;

-- Criação das Tabelas

-- Tabela Ano_Letivo
CREATE TABLE Ano_Letivo (
    id SERIAL PRIMARY KEY,
    ano_letivo VARCHAR(10) NOT NULL
);

-- Tabela Regional_Ensino
CREATE TABLE Regional_Ensino (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- Tabela Unidade_Escolar
CREATE TABLE Unidade_Escolar (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- Tabela Bloco
CREATE TABLE Bloco (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(100) NOT NULL
);

-- Tabela Serie_Ano
CREATE TABLE Serie_Ano (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(50) NOT NULL
);

-- Tabela Turma
CREATE TABLE Turma (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(50) NOT NULL
);

-- Tabela Turno
CREATE TABLE Turno (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(50) NOT NULL
);

-- Tabela Professor
CREATE TABLE Professor (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- Tabela Deficiencia_Transtorno
CREATE TABLE Deficiencia_Transtorno (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(100),
    sim_nao BOOLEAN NOT NULL
);

-- Tabela Adequacao_Curricular
CREATE TABLE Adequacao_Curricular (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(100),
    sim_nao BOOLEAN NOT NULL
);

-- Tabela Temporalidade
CREATE TABLE Temporalidade (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(100),
    sim_nao BOOLEAN NOT NULL
);

-- Tabela Sala_Recurso
CREATE TABLE Sala_Recurso (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(100),
    sim_nao BOOLEAN NOT NULL
);

-- Tabela SuperAcao
CREATE TABLE SuperAcao (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(100),
    checkbox BOOLEAN NOT NULL
);

-- Tabela OC_SuperAcao
CREATE TABLE OC_SuperAcao (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(100),
    checkbox BOOLEAN NOT NULL
);

-- Tabela Bimestre
CREATE TABLE Bimestre (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(50),
    checkbox BOOLEAN NOT NULL
);

-- Tabela Dias_Letivos
CREATE TABLE Dias_Letivos (
    id SERIAL PRIMARY KEY,
    dias VARCHAR(10) NOT NULL
);

-- Tabela Total_Faltas
CREATE TABLE Total_Faltas (
    id SERIAL PRIMARY KEY,
    faltas VARCHAR(10) NOT NULL
);

-- Tabela Conteudos
CREATE TABLE Conteudos (
    id SERIAL PRIMARY KEY,
    descricao TEXT NOT NULL
);

-- Tabela Objetivos_Aprendizagem
CREATE TABLE Objetivos_Aprendizagem (
    id SERIAL PRIMARY KEY,
    descricao TEXT NOT NULL
);

-- Tabela Nivel_Apreensao
CREATE TABLE Nivel_Apreensao (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(50) NOT NULL
);

-- Tabela Alunos
CREATE TABLE Alunos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    matricula VARCHAR(50) UNIQUE NOT NULL,
    serie_ano_id INT REFERENCES Serie_Ano(id),
    turma_id INT REFERENCES Turma(id)
);

-- Tabela Avaliacoes
CREATE TABLE Avaliacoes (
    id SERIAL PRIMARY KEY,
    aluno_id INT REFERENCES Alunos(id),
    disciplina_id INT REFERENCES Disciplinas(id),
    conteudo_id INT REFERENCES Conteudos(id),
    objetivo_aprendizagem_id INT REFERENCES Objetivos_Aprendizagem(id),
    nivel_apreensao_id INT REFERENCES Nivel_Apreensao(id),
    deficiencia_transtorno BOOLEAN NOT NULL,
    adequacao_curricular BOOLEAN NOT NULL,
    temporalidade BOOLEAN NOT NULL,
    sala_recurso BOOLEAN NOT NULL,
    superacao BOOLEAN NOT NULL,
    oc_superacao BOOLEAN NOT NULL,
    bimestre BOOLEAN NOT NULL,
    dias_letivos VARCHAR(10) NOT NULL,
    total_faltas VARCHAR(10) NOT NULL,
    data_avaliacao DATE NOT NULL DEFAULT CURRENT_DATE
);

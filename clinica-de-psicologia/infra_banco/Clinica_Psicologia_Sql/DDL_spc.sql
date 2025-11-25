-- ==================================================
-- TABELAS DE INSCRIÇÃO (FICHAS)
-- ==================================================
CREATE TABLE inscritoconvenio (
    idfichaconvenio SERIAL PRIMARY KEY,
    nomeinscrito VARCHAR(100) NOT NULL,
    dtnascimento DATE NOT NULL,
    testavpsico BOOLEAN NOT NULL DEFAULT FALSE,
    tipoencaminhamento VARCHAR(50) NOT NULL CHECK (tipoencaminhamento IN ('CAPS','CRAS','CREAS','DEAM','DPDF','MPDFT','SES','SEJUS','UBS','Clinica Ana Lucia Chaves Fecury Unieuro Asa Sul')),
    nomeresp VARCHAR(50),
    grauresp VARCHAR(25),
    cpfresp CHAR(11) UNIQUE,
    estadocivilresp VARCHAR(25) CHECK (estadocivilresp IN ('Solteiro', 'Casado', 'Divorciado', 'Viúvo', 'União Estável', 'Nenhum', 'Outros')),
    tellcellresp VARCHAR(20),
    emailresp VARCHAR(45),
    estadocivilinscrito VARCHAR(25) CHECK (estadocivilinscrito IN ('Solteiro', 'Casado', 'Divorciado', 'Viúvo', 'União Estável', 'Nenhum', 'Outros')),
    cpfinscrito CHAR(11) NOT NULL UNIQUE,
    tellcellinscrito VARCHAR(20) NOT NULL,
    contatourgencia VARCHAR(15) NOT NULL,
    dthinsert TIMESTAMP NOT NULL DEFAULT NOW(),
    nomecontatourgencia VARCHAR(50)NOT NULL,
    emailinscrito VARCHAR(50) NOT NULL,
    identidadegenero VARCHAR(25) NOT NULL CHECK (identidadegenero IN('Masculino', 'Feminino', 'Não Binário', 'Transgênero','Outros')),
    etnia VARCHAR(15) NOT NULL CHECK (etnia IN('Branca', 'Preta', 'Parda', 'Amarela', 'Indígena', 'Outras')),
    religiao VARCHAR(30) NOT NULL CHECK (religiao IN('Católico','Evangélico','Budismo','Espirita', 'Hinduísmo', 'Islamismo', 'Judaismo', 'Religião de Matriz Africana', 'Sem religião', 'Outros')),
    confirmlgpd BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE inscritocomunidade (
    idfichacomunidade SERIAL PRIMARY KEY,
    nomeinscrito VARCHAR(100) NOT NULL,
    dtnascimento DATE NOT NULL,
    nomeresp VARCHAR(50),
    grauresp VARCHAR(25),
    cpfresp CHAR(11) UNIQUE,
    estadocivilresp VARCHAR(25) CHECK (estadocivilresp IN ('Solteiro', 'Casado', 'Divorciado', 'Viúvo', 'União Estável', 'Nenhum', 'Outros')),
    tellcellresp VARCHAR(20),
    emailresp VARCHAR(45),
    estadocivilinscrito VARCHAR(25) CHECK (estadocivilinscrito IN ('Solteiro', 'Casado', 'Divorciado', 'Viúvo', 'União Estável', 'Nenhum', 'Outros')),
    cpfinscrito CHAR(11) NOT NULL UNIQUE,
    tellcellinscrito VARCHAR(20) NOT NULL,
    contatourgencia VARCHAR(15) NOT NULL,
    nomecontatourgencia VARCHAR(50)NOT NULL,
    dthinsert TIMESTAMP NOT NULL DEFAULT NOW(),
    emailinscrito VARCHAR(45) NOT NULL,
    identidadegenero VARCHAR(25) NOT NULL CHECK(identidadegenero IN('Masculino', 'Feminino', 'Não Binário', 'Transgênero', 'Outros')),
    etnia VARCHAR(15) NOT NULL CHECK (etnia IN('Branca', 'Preta', 'Parda', 'Amarela', 'Indígena','Outras')),
    religiao VARCHAR(30) NOT NULL CHECK (religiao IN('Católico','Evangélico','Budismo','Espirita', 'Hinduísmo', 'Islamismo', 'Judaismo', 'Religião de Matriz Africana', 'Sem religião', 'Outros')),
    confirmlgpd BOOLEAN NOT NULL DEFAULT FALSE
);

-- ==================================================
-- TABELAS AUXILIARES DAS FICHAS
-- ==================================================
CREATE TABLE endereco (
    idendereco SERIAL PRIMARY KEY,
    idfichaconvenio INT,
    idfichacomunidade INT,
    cidade VARCHAR(40) NOT NULL,
    bairro VARCHAR(50),
    dthinsert TIMESTAMP NOT NULL DEFAULT NOW(),
    rua VARCHAR(100) NOT NULL,
    uf CHAR(2) DEFAULT 'DF' CHECK(uf in('DF')) NOT NULL,
    cep CHAR(10) UNIQUE NOT NULL,
    FOREIGN KEY (idfichaconvenio) REFERENCES inscritoconvenio(idfichaconvenio),
    FOREIGN KEY (idfichacomunidade) REFERENCES inscritocomunidade(idfichacomunidade) 
);

CREATE TABLE tipoterapia(
    idtipoterapia SERIAL PRIMARY KEY,
    idfichaconvenio INT,
    idfichacomunidade INT,  
    individualift BOOLEAN DEFAULT FALSE,
    individualadt BOOLEAN DEFAULT FALSE,
    individualadto BOOLEAN DEFAULT FALSE,
    individualids BOOLEAN DEFAULT FALSE,
    familia BOOLEAN DEFAULT FALSE,
    grupo BOOLEAN DEFAULT FALSE,
    casal BOOLEAN DEFAULT FALSE,
    dthtipot TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (idfichaconvenio) REFERENCES inscritoconvenio(idfichaconvenio),
    FOREIGN KEY (idfichacomunidade) REFERENCES inscritocomunidade(idfichacomunidade)
);

CREATE TABLE pcdsnd(
    idpcdnd SERIAL PRIMARY KEY,
    idfichaconvenio INT,
    idfichacomunidade INT,
    tea BOOLEAN DEFAULT FALSE,
    tdah BOOLEAN DEFAULT FALSE,
    dffs BOOLEAN DEFAULT FALSE,
    dfv BOOLEAN DEFAULT FALSE,
    dfa BOOLEAN DEFAULT FALSE,
    ttap BOOLEAN DEFAULT FALSE,
    ahst BOOLEAN DEFAULT FALSE,
    outro BOOLEAN DEFAULT FALSE,
    dthinsert TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (idfichaconvenio) REFERENCES inscritoconvenio(idfichaconvenio),
    FOREIGN KEY (idfichacomunidade) REFERENCES inscritocomunidade(idfichacomunidade)
);

CREATE TABLE motivoacompanhamento(
    idmotivoacamp SERIAL PRIMARY KEY,
    idfichaconvenio INT,
    idfichacomunidade INT,
    ansiedade BOOLEAN DEFAULT FALSE,
    assediomoral BOOLEAN DEFAULT FALSE,
    depressao BOOLEAN DEFAULT FALSE,
    dfaprendizagem BOOLEAN DEFAULT FALSE,
    humorinstavel BOOLEAN DEFAULT FALSE,
    insonia BOOLEAN DEFAULT FALSE,
    isolasocial BOOLEAN DEFAULT FALSE,
    luto BOOLEAN DEFAULT FALSE,
    tristeza BOOLEAN DEFAULT FALSE,
    apatia BOOLEAN DEFAULT FALSE,
    chorofc BOOLEAN DEFAULT FALSE,
    exaustao BOOLEAN DEFAULT FALSE,
    fadiga BOOLEAN DEFAULT FALSE,
    faltanimo BOOLEAN DEFAULT FALSE,
    vldt BOOLEAN DEFAULT FALSE,
    assediosexual BOOLEAN DEFAULT FALSE,
    outro BOOLEAN DEFAULT FALSE,
    dthinsert TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (idfichaconvenio) REFERENCES inscritoconvenio(idfichaconvenio),
    FOREIGN KEY (idfichacomunidade) REFERENCES inscritocomunidade(idfichacomunidade)
);

CREATE TABLE medicamento(
    idmedicamento SERIAL PRIMARY KEY,
    idfichaconvenio INT,
    idfichacomunidade INT,
    ansiolitico BOOLEAN DEFAULT FALSE,
    antidepressivo BOOLEAN DEFAULT FALSE,
    antipsicotico BOOLEAN DEFAULT FALSE,
    estabhumor BOOLEAN DEFAULT FALSE,
    memoriatct BOOLEAN DEFAULT FALSE,
    outro BOOLEAN DEFAULT FALSE,
    dthmedic TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (idfichaconvenio) REFERENCES inscritoconvenio(idfichaconvenio),
    FOREIGN KEY (idfichacomunidade) REFERENCES inscritocomunidade(idfichacomunidade)
);

CREATE TABLE doencafisica(
    iddoencafisica SERIAL PRIMARY KEY,
    idfichaconvenio INT,
    idfichacomunidade INT,
    doencaresp BOOLEAN DEFAULT FALSE,
    cancer BOOLEAN DEFAULT FALSE,
    diabete BOOLEAN DEFAULT FALSE,
    disfusexual BOOLEAN DEFAULT FALSE,
    doencadgt BOOLEAN DEFAULT FALSE,
    escleorosemlt BOOLEAN DEFAULT FALSE,
    hcpt BOOLEAN DEFAULT FALSE,
    luposatm BOOLEAN DEFAULT FALSE,
    obesidade BOOLEAN DEFAULT FALSE, 
    pblmarenal BOOLEAN DEFAULT FALSE,
    outro BOOLEAN DEFAULT FALSE,
    dthinsert TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (idfichaconvenio) REFERENCES inscritoconvenio(idfichaconvenio),
    FOREIGN KEY (idfichacomunidade) REFERENCES inscritocomunidade(idfichacomunidade)
);

CREATE TABLE disponibilidade(
    iddisponibilidade SERIAL PRIMARY KEY,
    idfichaconvenio INT,
    idfichacomunidade INT,
    manha BOOLEAN DEFAULT FALSE,
    tarde BOOLEAN DEFAULT FALSE,
    noite BOOLEAN DEFAULT FALSE,
    dthdispo TIMESTAMP NOT NULL DEFAULT NOW(),
    sabado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (idfichaconvenio) REFERENCES inscritoconvenio(idfichaconvenio),
    FOREIGN KEY (idfichacomunidade) REFERENCES inscritocomunidade(idfichacomunidade)
);

-- ==================================================
-- CONTROLE DE ACESSO E USUÁRIOS (Refatorado)
-- ==================================================

-- Tabela BASE de Usuários
CREATE TABLE usuario (
    iduser SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    emailinst VARCHAR(150) UNIQUE NOT NULL,
    cpf VARCHAR(30) UNIQUE NOT NULL,
    matricula VARCHAR(15) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    dthinsert TIMESTAMP NOT NULL DEFAULT NOW(),
    cargo VARCHAR(25) NOT NULL CHECK (cargo IN ('Coordenador', 'Supervisor', 'Secretaria', 'Estagiario', 'ResponsavelTec')),
    is_active BOOLEAN DEFAULT TRUE
);

-- Tabelas de CARGOS (Vinculadas 1:1 com usuario via iduser)

CREATE TABLE coordenador (
    crp INT NOT NULL PRIMARY KEY,
    iduser INT NOT NULL UNIQUE, -- Link 1:1 com a tabela usuario
    crpcoord INT, -- Auto-relacionamento
    dthcoord TIMESTAMP NOT NULL DEFAULT NOW(),
    foto_cooder bytea, 
    status BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (iduser) REFERENCES usuario(iduser),
    FOREIGN KEY (crpcoord) REFERENCES coordenador(crp)
);

CREATE TABLE supervisor (
    crp INT NOT NULL PRIMARY KEY,
    iduser INT NOT NULL UNIQUE, -- Link 1:1
    crpcoord INT NOT NULL,
    foto_coord bytea, 
    dthsup TIMESTAMP NOT NULL DEFAULT NOW(), 
    status BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (iduser) REFERENCES usuario(iduser),
    FOREIGN KEY (crpcoord) REFERENCES coordenador(crp)  
);

CREATE TABLE secretaria (
    matricula_sec INT NOT NULL PRIMARY KEY, -- Definido como PK para ser referenciado
    iduser INT NOT NULL UNIQUE, -- Link 1:1
    crpcoord INT NOT NULL,
    dthsec TIMESTAMP NOT NULL DEFAULT NOW(),
    foto_sec bytea,
    status BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (iduser) REFERENCES usuario(iduser),
    FOREIGN KEY (crpcoord) REFERENCES coordenador(crp)
);

CREATE TABLE resptec(
    crpresp INT NOT NULL PRIMARY KEY,
    iduser INT NOT NULL UNIQUE, -- Link 1:1
    crpcoord INT NOT NULL,
    dthresp TIMESTAMP NOT NULL DEFAULT NOW(),
    foto_resptec bytea, 
    status BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (iduser) REFERENCES usuario(iduser),
    FOREIGN KEY (crpcoord) REFERENCES coordenador(crp)
);

CREATE TABLE estagiario (
    ra INT NOT NULL PRIMARY KEY,
    iduser INT NOT NULL UNIQUE, -- Link 1:1
    crpsup INT NOT NULL,
    crpcoord INT NOT NULL,
    nivelestagio VARCHAR(10) NOT NULL,
    semestre VARCHAR(10) NOT NULL, 
    foto_estg BYTEA, 
    dthestg TIMESTAMP DEFAULT NOW(),
    status BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (iduser) REFERENCES usuario(iduser),
    FOREIGN KEY (crpsup) REFERENCES supervisor (crp),
    FOREIGN KEY (crpcoord) REFERENCES coordenador (crp)
);

-- ==================================================
-- OPERACIONAL DA CLÍNICA
-- ==================================================

CREATE TABLE escolheins(
    idescolheins SERIAL PRIMARY KEY,
    ra INT NOT NULL, -- Corrigido de 'idestagiario' para 'ra'
    idfichaconvenio INT,
    idfichacomunidade INT,
    status BOOLEAN DEFAULT FALSE,
    dthescolha TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (ra) REFERENCES estagiario (ra),
    FOREIGN KEY (idfichaconvenio) REFERENCES inscritoconvenio (idfichaconvenio),
    FOREIGN KEY (idfichacomunidade) REFERENCES inscritocomunidade (idfichacomunidade)
);

CREATE TABLE sala(
    idsala SERIAL PRIMARY KEY,
    matricula_sec INT, -- Corrigido para coincidir com a PK da secretaria
    crpresp INT,
    crpcoord INT,
    numsala INT NOT NULL,
    tiposala VARCHAR(10) NOT NULL,
    capacidade INT NOT NULL,
    dthsala TIMESTAMP NOT NULL DEFAULT NOW(),
    status BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (crpcoord) REFERENCES coordenador (crp),
    FOREIGN KEY (matricula_sec) REFERENCES secretaria (matricula_sec),
    FOREIGN KEY (crpresp) REFERENCES resptec (crpresp)
);

CREATE TABLE agendamento(
    idagendamento SERIAL PRIMARY KEY,
    idsala INT NOT NULL,
    matricula_sec INT, -- Corrigido nome da coluna
    crpresp INT,
    crpcoord INT,
    confirmsec BOOLEAN DEFAULT FALSE,
    dthconfirmsec TIMESTAMP,
    confirmresp BOOLEAN DEFAULT FALSE,
    dthconfirmresp TIMESTAMP,
    confirmcoord BOOLEAN DEFAULT FALSE,
    dthconfirmcoord TIMESTAMP,
    FOREIGN KEY (idsala) REFERENCES sala(idsala),
    FOREIGN KEY (matricula_sec) REFERENCES secretaria (matricula_sec),
    FOREIGN KEY (crpresp) REFERENCES resptec (crpresp),
    FOREIGN KEY (crpcoord) REFERENCES coordenador (crp)
);

CREATE TABLE salaagendamento(
    idsolicitacoes SERIAL PRIMARY KEY,
    idagendamento INT NOT NULL,
    crpsup INT,
    ra INT,
    dthsolisup TIMESTAMP,
    dthsoliest TIMESTAMP,
    FOREIGN KEY (idagendamento) REFERENCES agendamento(idagendamento),
    FOREIGN KEY (crpsup) REFERENCES supervisor (crp),
    FOREIGN KEY (ra) REFERENCES estagiario (ra)
);

CREATE TABLE prontuario (
    idprontuario SERIAL PRIMARY KEY,
    crpcoord INT, 
    crpsup INT ,
    ra INT ,
    idfichaconvenio INT,
    idfichacomunidade INT, 
    tcle BYTEA NOT NULL,
    dthprontuario TIMESTAMP NOT NULL DEFAULT NOW(),
    status BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (crpcoord) REFERENCES coordenador (crp),
    FOREIGN KEY (crpsup) REFERENCES supervisor (crp),
    FOREIGN KEY (ra) REFERENCES estagiario (ra),
    FOREIGN KEY (idfichaconvenio) REFERENCES inscritoconvenio (idfichaconvenio),
    FOREIGN KEY (idfichacomunidade) REFERENCES inscritocomunidade (idfichacomunidade)
);

CREATE TABLE folhaevo (
    idfolhaevolução SERIAL PRIMARY KEY,
    idprontuario INT NOT NULL,
    folhaevolucao BYTEA NOT NULL,
    dthanexo TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (idprontuario) REFERENCES prontuario(idprontuario)
);

CREATE TABLE fichafreqest(
    idfichafreq SERIAL PRIMARY KEY,
    ra INT NOT NULL,
    crpsup INT,
    crpcoord INT,
    fichafreq BYTEA, 
    FOREIGN KEY (ra) REFERENCES estagiario (ra),
    FOREIGN KEY (crpsup) REFERENCES supervisor (crp),
    FOREIGN KEY (crpcoord) REFERENCES coordenador (crp)
);

CREATE TABLE anamnese(
    idanamnese SERIAL PRIMARY KEY,
    idprontuario INT,
    anamnesedoc BYTEA,
    dthanexo TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (idprontuario) REFERENCES prontuario(idprontuario)
);

CREATE TABLE laudomed(
    idlaudo SERIAL PRIMARY KEY,
    idprontuario INT,
    laudodoc BYTEA,
    dthanexo TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (idprontuario) REFERENCES prontuario(idprontuario)
);

CREATE TABLE arqinscrito(
    idarqinscrito SERIAL PRIMARY KEY,
    idfichaconvenio INT,
    idfichacomunidade INT,
    status BOOLEAN DEFAULT TRUE,
    dtharquinscrito TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (idfichaconvenio) REFERENCES inscritoconvenio (idfichaconvenio),
    FOREIGN KEY (idfichacomunidade) REFERENCES inscritocomunidade (idfichacomunidade)   
);

CREATE TABLE arquivamento(
    idarquivamento SERIAL PRIMARY KEY,
    idsolicitacao INT NOT NULL,
    crpcoord INT,
    crpresp INT,
    idprontuario INT,
    idarqinscrito INT,
    dtharq TIMESTAMP DEFAULT NOW(),
    retencao TIMESTAMP GENERATED ALWAYS AS (dtharq + INTERVAL '5 years') STORED,
    justificativa VARCHAR(255),
    FOREIGN KEY (crpcoord) REFERENCES coordenador (crp),
    FOREIGN KEY (crpresp) REFERENCES resptec (crpresp),
    FOREIGN KEY (idprontuario) REFERENCES prontuario (idprontuario),
    FOREIGN KEY (idarqinscrito) REFERENCES arqinscrito (idarqinscrito)
);

CREATE TABLE soliarquivamento(
    idsloicitacao SERIAL PRIMARY KEY,
    idprontuario INT,
    idarqinscrito INT,
    idarquivamento INT NOT NULL,
    ra INT,
    dthsoliestagiario TIMESTAMP,
    crpsup INT,
    confirmsup BOOLEAN DEFAULT FALSE,
    dthsolisup TIMESTAMP,
    crpresp INT,
    confirmresp BOOLEAN DEFAULT FALSE,
    crpcoord INT,
    confirmcoord BOOLEAN DEFAULT FALSE,
    descricao VARCHAR(255),
    FOREIGN KEY (idprontuario) REFERENCES prontuario (idprontuario),
    FOREIGN KEY (idarqinscrito) REFERENCES arqinscrito (idarqinscrito),
    FOREIGN KEY (idarquivamento) REFERENCES arquivamento (idarquivamento),
    FOREIGN KEY (ra) REFERENCES estagiario (ra),
    FOREIGN KEY (crpsup) REFERENCES supervisor (crp),
    FOREIGN KEY (crpresp) REFERENCES resptec (crpresp),
    FOREIGN KEY (crpcoord) REFERENCES coordenador (crp)
);

CREATE TABLE htocorrencia(
    idhtc SERIAL PRIMARY KEY,
    idprontuario INT,
    idarqinscrito INT,
    ra INT,
    crpsup INT,
    crpcoord INT,
    nomepessoa VARCHAR(50) NOT NULL,
    dthora TIMESTAMP NOT NULL DEFAULT NOW(),
    comparecimento BOOLEAN DEFAULT FALSE,
    faltas INT NOT NULL,
    justificativa VARCHAR(255) NOT NULL,
    FOREIGN KEY (idprontuario) REFERENCES prontuario (idprontuario),
    FOREIGN KEY (idarqinscrito) REFERENCES arqinscrito (idarqinscrito),
    FOREIGN KEY (ra) REFERENCES estagiario (ra),
    FOREIGN KEY (crpsup) REFERENCES supervisor (crp),
    FOREIGN KEY (crpcoord) REFERENCES coordenador (crp) 
);
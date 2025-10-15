# INTRODUÇÃO

Esse documento tem como objetivo registrar a construção, criação do ambiente codespace do desenvolvedor fullstack!
Recomendo que lenham antes a documentação: 1.1 - Codespace_Conteiner.md e 1 - Ambiente_Virtual_Python.md

## Ferramentas, FremeWorks, Artefatos, Tecnologias:

Fullstack:

    Banco de dados:

    - Postgres version 14 

    Back-End:

    - Python version 3 ou + 
    - Django
    - Psycopg2
    - Jinja2

    Front-end:

    - Html version 5 
    - JavaScript version mais recente 
    - CSS


## Fluxo de como funciona a nossa aplicação:

[ navegador ] ⇄ [ Django (views) ] ⇄ [ Modelos ORM ] ⇄ [ PostgreSQL ]
        ↑                ↓                  ↑               ↓
     HTML/CSS        Templates         Classes Python     Dados reais
        ↑
 [ JS opcional ]

- Cenário prático:

  Usuário acessa http://localhost:8000/

  Django executa uma view

  A view consulta um modelo que acessa o banco PostgreSQL via ORM (abstraído por Psycopg2)

  Os dados retornam para a view

  A view renderiza um template HTML (com Django Template ou Jinja2)

  A resposta HTML é enviada ao navegador


## Estrutura do Projeto da Fabrica de software e alguns exemplos! 


fabrica_de_software/
│
├── .devcontainer/                # ✅ Configura o ambiente Codespace (container + VSCode)
│   ├── devcontainer.json         # Define a imagem, PostgreSQL, extensões, portas, comandos
│   └── Dockerfile                # Define o ambiente base (Python + dependências)
│
├── .venv/                        # ⚠️ Ambiente virtual local (não versionar — ignore no Git)
│
├── back/                         # ✅ Backend em Django (views, models, templates)
│   ├── manage.py
│   ├── config/                   # Configurações globais do Django
│   ├── apps/                     # Apps Django (ex: auth, cliente, laudos, etc.)
│   └── requirements.txt          # Dependências do projeto (psycopg2, django, jinja2 etc.)
│
├── doc/                          # ✅ Documentação técnica (markdown ou PDFs)
│   ├── setup.md                  # Explica o uso do devcontainer, migrações etc.
│   ├── arquitetura.md
│   └── endpoints.md
│
├── front/                        # ✅ Frontend estático (HTML, CSS, JS)
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── UIUX/                         # ✅ Protótipos, mockups, fluxos visuais (Figma, PNG etc.)
│   ├── tela_login.png
│   └── fluxo_sistema.fig
│
├── infra_banco/                  # ✅ Infraestrutura de banco de dados (scripts SQL e docs)
│   ├── ddl/                      # CREATE TABLE, ALTER TABLE
│   ├── dml/                      # INSERTs de dados iniciais
│   ├── dump/                     # Backups do banco
│   └── README.md                 # Instruções para restaurar ou popular o banco
│
├── .gitignore                    # ✅ Ignora `.venv`, `__pycache__`, `.env`, `.sqlite3`
└── README.md                     # ✅ Visão geral do projeto (stack, como rodar, autores)



## Instalando postgres no nosso codespace

2. Pré-requisitos

    Conta no GitHub com acesso a Codespaces.

      Utilizar 2 Núcles/Cores no codespace que é gratuito: limite de 60h por mês

      observação: Você pode criar um com 4 cores, mas aí é contigo kkkkk

    Docker instalado e configurado no Codespace (o Codespaces já vem com Docker instalado, mas é importante verificar).

    Permissões para executar comandos Docker dentro do Codespace.

    VS Code instalado localmente ou acesso ao editor via browser com Codespaces.

3. Verificar se o Docker está instalado no Codespace

    Abra o terminal do Codespace (integrado no VS Code ou via interface web) e execute
    o comando para verificar a instalação do Docker:

        docker --version

    Resultado esperado:

        Exemplo: Docker version 20.10.17, build 100c701

    Se esse comando retornar a versão do Docker, significa que o Docker está instalado e funcionando no Codespace.

    Se não estiver instalado:

        No Codespace padrão, Docker já está disponível. Caso não esteja, verifique as configurações do ambiente 
        ou informe o administrador do repositório.

4. Criar e rodar o container PostgreSQL

    Para iniciar o PostgreSQL em um container Docker dentro do Codespace, execute o comando abaixo:


      docker run --name postgres-codespace -e POSTGRES_PASSWORD=sua_senha -e POSTGRES_DB=nome_seu_banco -p 5432:5432 -d postgres

    Explicação dos parâmetros:
        
        --name postgres-codespace: nome do container para facilitar o gerenciamento.

        -e POSTGRES_PASSWORD = suasenha: variável de ambiente que define a senha do usuário padrão postgres.
        Substitua suasenha por uma senha forte e segura.

        -e POSTGRES_DB = scp : variável que cria automaticamente um banco de dados chamado laudinho ao iniciar o container.

        -p 5432:5432: mapeia a porta 5432 do container para a porta 5432 do Codespace, permitindo conexão externa.

        -d postgres: especifica a imagem oficial do PostgreSQL e roda o container em modo "detach" (em segundo plano).

5. Confirmar se o container está rodando

    Verifique se o container foi iniciado corretamente com:

        docker ps

    Esse comando lista todos os containers ativos. Você deve ver uma linha parecida com:


      CONTAINER ID   IMAGE      COMMAND                  CREATED        STATUS       PORTS                    NAMES
      abcd1234efgh   postgres   "docker-entrypoint.s…"   2 minutes ago  Up 2 minutes 0.0.0.0:5432->5432/tcp   postgres-codespace

    Se o container aparecer listado e com status Up, seu PostgreSQL está rodando.

6. Conectar ao PostgreSQL via terminal dentro do Codespace (OBRIGATÓRIO FAZER ISSO PARA DAR CERTO)

    Para interagir com o banco via terminal, você pode usar o cliente psql. Caso não tenha o cliente instalado, execute:


      sudo apt update
      sudo apt install -y postgresql-client

    Depois, conecte-se ao banco com o comando:

        psql -h localhost -U postgres -d scp

      -h localhost: host onde o banco está rodando (localhost, pois está dentro do Codespace).

      -U postgres: usuário padrão do PostgreSQL.

      -d laudinho: banco de dados que foi criado no container.

    Ao executar, será solicitada a senha (aquela que você definiu em POSTGRES_PASSWORD). Digite a senha e pressione Enter.

    Se conectar com sucesso, verá o prompt do PostgreSQL, por exemplo:

        psql (14.2 (Ubuntu 14.2-1.pgdg22.04+1))
    
        nome_seu_banco=#    

    Digite "help" para ajuda.

7. Instalar a extensão PostgreSQL no VS Code

    Para facilitar a gestão do banco, use a extensão oficial do PostgreSQL para VS Code.

    Passos:
        
        No VS Code (seja local ou no Codespace), clique no ícone de Extensões (lado esquerdo, ícone de quadrados empilhados).

        Na barra de busca, digite PostgreSQL.

        Encontre a extensão oficial, normalmente identificada pelo ícone do elefante azul e desenvolvida pela Microsoft ou ms-ossdata.

        Clique em Instalar.

        Após instalação, a extensão estará disponível no painel lateral esquerdo.

8. Conectar ao banco PostgreSQL via extensão no VS Code
    
    Após instalar a extensão:

        Clique no ícone do banco de dados (🗄️) que aparece na barra lateral esquerda.

        Clique em Adicionar nova conexão (geralmente um botão “+” ou “Nova Conexão”).

    Preencha os dados da conexão:

        +---------+------------+----------------------------------------------+
        | Campo   | Valor      | Observações                                  |
        +---------+------------+----------------------------------------------+
        | Host    | localhost  | Como o container mapeia localhost no Codespace |
        | Porta   | 5432       | Porta padrão do PostgreSQL                   |
        | Usuário | postgres   | Usuário padrão                               |
        | Senha   | sua senha  | A mesma definida no POSTGRES_PASSWORD        |
        | Banco   | seu banco  | Banco criado no container                    |
        +---------+------------+----------------------------------------------+

    SALVER A CONEXÃO E CLIQUE EM CONNECT.

    Teste a conexão e, se tudo estiver correto, você poderá navegar pelas tabelas, 
    executar queries e gerenciar o banco direto pelo VS Code.

9. Comandos úteis para gerenciamento do container

    Parar o container:

        docker stop postgres-codespace

    Iniciar o container parado:

        docker start postgres-codespace

    Acessar o terminal dentro do container (shell):

        docker exec -it postgres-codespace bash

    Remover o container (apaga dados se não estiver em volume persistente):


        docker rm -f postgres-codespace

10. Observações finais

    Persistência de dados: Por padrão, o banco dentro do container perde os dados quando o container é removido. 
    Para evitar isso, configure um volume Docker para persistência, exemplo:


        docker run --name postgres-codespace \
        -e POSTGRES_PASSWORD=suasenha \
        -e POSTGRES_DB=laudinho \
        -p 5432:5432 \
        -v pgdata:/var/lib/postgresql/data \
        -d postgres

    Segurança: Evite usar senhas fracas ou padrão em ambientes de produção.

    Performance: Codespaces é um ambiente em nuvem e pode ter limitações de performance comparado a uma instalação local.



## Configuração do Codespace no devcontainer.json (.devcontainer/)

{
  "name": "fabrica_de_software",
  "build": {
    "dockerfile": "Dockerfile"
  },
  "features": {
    "ghcr.io/devcontainers/features/postgres:1": {
      "version": "14",                // ← Versão do PostgreSQL
      "database": "dbprojeto",
      "user": "usuario",
      "password": "senha"
    }
  },
  "postCreateCommand": "pip install -r back/requirements.txt",
  "forwardPorts": [8000, 5432],
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",           // Python e linting
        "batisteo.vscode-django",     // Suporte ao Django
        "ms-azuretools.vscode-docker" // Visualização de containers
      ]
    }
  }
}

## Configurando o nosso Dockerfile

FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    netcat \
    && apt-get clean

WORKDIR /workspace

COPY . .
RUN pip install --upgrade pip
RUN pip install -r back/requirements.txt

## requirements.txt

Django>=4.2
psycopg2-binary
jinja2

## Configurando Banco de dados Postgres no nosso BACK-END:

Você está usando a feature oficial do DevContainer:

- Porta: 5432 # porta lógica do postgres, padrão

- Host: localhost (dentro do container)

- Database: nome_banco # nome do banco de dados do seu projeto

- User: postgres # nome do usuario, por padrão é o postgres

- Password: senha # senha do seu banco de dados

**No settings.py do Django:**

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dbprojeto',
        'USER': 'usuario',
        'PASSWORD': 'senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

##  Frontend Estático
Seus arquivos HTML, JS e CSS estão em front/. Você pode servir isso:
  Diretamente com Django (STATICFILES_DIRS)
  Ou mantê-los separados no GitHub Pages / deploy externo

Exemplo no settings.py do Django:

STATICFILES_DIRS = [
    BASE_DIR / "front"
]

## Instalar as extensões no VScode:
Python, Python Debugger, Pylance, autopep8, PostgreSQL, Docker, Container Tools, Rest Client

## Inicialização do nosso projeto:

cd back
django-admin startproject backend
python manage.py migrate
python manage.py runserver 0.0.0.0:8000


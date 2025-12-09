# Guia de Instalação e Execução - Clínica de Psicologia

Este guia contém o passo a passo para configurar o ambiente de desenvolvimento, iniciar o banco de dados e executar o sistema localmente para testes.

## 1. Clonar o Repositório

Baixe o código fonte do projeto para sua máquina local ou Codespace.

```bash
git clone https://github.com/devops-softhub/clinica-de-psicologia.git
cd clinica-de-psicologia
# Navegue até a pasta raiz do projeto Django (onde está o manage.py)
cd clinica-de-psicologia-vitor-total/clinica-de-psicologia
```

## 2. Configurar o Ambiente Virtual

Recomenda-se criar um ambiente virtual para isolar as dependências do projeto.

### Criar o ambiente:

```bash
# Linux/Mac/Codespaces
python3 -m venv venv

# Windows
python -m venv venv
```

### Ativar o ambiente:

```bash
# Linux/Mac/Codespaces
source venv/bin/activate

# Windows
venv\Scripts\activate
```

## 3. Instalar Dependências

Com o ambiente virtual ativo, instale as bibliotecas listadas no `requirements.txt`.

```bash
pip install -r requirements.txt
```

## 4. Configurar Variáveis de Ambiente (.env)

O sistema utiliza variáveis de ambiente para conectar ao banco de dados. Crie um arquivo `.env` na raiz do projeto (mesmo local do `manage.py`) baseando-se no exemplo fornecido.

1. Crie o arquivo `.env`
2. Cole o seguinte conteúdo (configurado para o Docker sugerido abaixo):

```env
DB_NAME=clinica
DB_USER=postgres
DB_PASSWORD=123456
DB_HOST=localhost
DB_PORT=5432
```

## 5. Subir o Banco de Dados (Docker)

Utilize o Docker para rodar um container PostgreSQL configurado conforme as variáveis do seu `.env`.

Execute o comando abaixo no terminal para baixar e iniciar o banco de dados:

```bash
docker run --name postgres-clinica \
-e POSTGRES_PASSWORD=123456 \
-e POSTGRES_USER=postgres \
-e POSTGRES_DB=clinica \
-p 5432:5432 \
-d postgres
```

**Observação:** Se estiver usando Codespaces, o Docker já vem instalado. Apenas execute o comando.

## 6. Inicializar o Banco de Dados

Com o container rodando, aplique as migrações do Django para criar as tabelas no banco de dados.

```bash
python manage.py makemigrations
python manage.py migrate
```

**Opcional:** Criar um superusuário para acessar a área administrativa:

```bash
python manage.py createsuperuser
```

## 7. Executar o Servidor

Inicie o servidor de desenvolvimento do Django.

```bash
python manage.py runserver
```

O sistema estará acessível em `http://127.0.0.1:8000/`.

## 8. Mapa de Funcionalidades e URLs

Abaixo estão as URLs para acessar as principais funcionalidades do sistema, baseadas na configuração de rotas.

| Funcionalidade | URL Completa (Local) | Descrição |
|----------------|----------------------|-----------|
| Login | `http://127.0.0.1:8000/login/login/` | Tela de acesso ao sistema |
| Cadastro Usuário | `http://127.0.0.1:8000/login/cadastro/` | Registro de novos usuários |
| Cadastro Comunidade | `http://127.0.0.1:8000/formulario/cadastro/comunidade/` | Formulário de inscrição (Público Geral) |
| Cadastro Convênio | `http://127.0.0.1:8000/formulario/cadastro/convenio/` | Formulário de inscrição (Convênios) |
| Dashboard Coord. | `http://127.0.0.1:8000/login/dashboard/coord/` | Painel do Coordenador |
| Recuperar Senha | `http://127.0.0.1:8000/login/nova-senha/` | Redefinição de senha |
| Admin Django | `http://127.0.0.1:8000/admin/` | Painel administrativo do Django |
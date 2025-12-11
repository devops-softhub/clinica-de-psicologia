# Instruções de QA - Validação de Fluxo de Inscritos

## 1. Objetivo do Teste
O objetivo deste teste é validar a integridade dos dados desde o preenchimento do formulário de inscrição até a sua visualização nas telas de consulta e detalhes do sistema. A equipe de QA deve identificar discrepâncias, campos não preenchidos ou erros de renderização.

## 2. Configuração do Ambiente
Para iniciar os testes, siga os passos abaixo (baseado no `guia_inicializacao.md`):

1.  **Ambiente Virtual:**
    *   Crie: `python3 -m venv venv`
    *   Ative: `source venv/bin/activate` (Linux/Mac) ou `venv\Scripts\activate` (Windows)
    *   Instale dependências: `pip install -r requirements.txt`

2.  **Banco de Dados:**
    *   Certifique-se de ter o Docker instalado.
    *   Crie o arquivo `.env` na raiz com as configurações do banco (ver `guia_inicializacao.md`).
    *   Suba o container: `docker run --name postgres-clinica -e POSTGRES_PASSWORD=123456 -e POSTGRES_USER=postgres -e POSTGRES_DB=clinica -p 5432:5432 -d postgres`
    *   Aplique as migrações: `python manage.py migrate`

3.  **Execução:**
    *   Inicie o servidor: `python manage.py runserver`
    *   Acesse: `http://127.0.0.1:8000/`

## 3. Cenários de Teste

### Caso A: Preenchimento e Submissão
1.  Acesse o formulário de comunidade: `http://127.0.0.1:8000/formulario/cadastro/comunidade/`
2.  Preencha **todos** os campos. Tire um **Print Screen** do formulário preenchido antes de enviar.
3.  Envie o formulário.

### Caso B: Validação na Lista (`consulta_inscrito.html`)
1.  Logue com um usuário Estagiário ou Supervisor.
2.  Navegue até a lista de inscritos disponíveis.
3.  **Verificar:**
    *   O inscrito recém-criado aparece na lista?
    *   Os botões de ação ("Selecionar") aparecem corretamente para o seu perfil?
    *   A paginação funciona se houver muitos registros?

### Caso C: Validação de Detalhes (`dados_inscrito.html`)
1.  Clique para ver os detalhes do inscrito.
2.  **Verificar:**
    *   Compare os dados desta tela com o **Print Screen** do passo A.
    *   Todos os campos preenchidos estão visíveis?
    *   **Atenção Especial:** Verifique a seção de **Disponibilidade de Horário**. Existe uma suspeita de que esses dados não estão sendo exibidos corretamente. Confirme se aparecem ou se a seção está em branco.

## 4. Entregáveis e Relatório
Para cada erro ou inconsistência encontrada, gere um relatório contendo:

1.  **Descrição do Problema:** O que deveria aparecer vs. o que apareceu.
2.  **Evidências:**
    *   Print do Formulário Original (o que foi digitado).
    *   Print da Tela de Consulta/Detalhes (como o sistema mostrou).
3.  **Casos de "Não Aparece":** Liste especificamente quais campos sumiram (ex: "O campo 'Bairro' foi preenchido mas está vazio na visualização").

---
**Nota:** Utilize este guia para garantir que nenhum dado está se perdendo no fluxo entre o banco de dados e o front-end.

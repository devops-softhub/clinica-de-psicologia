# Clínica de Psicologia - Sistema de Gestão

Sistema de gestão para a clínica de psicologia, desenvolvido em Django.

## 🚀 Melhorias de Performance (Refatoração - Consulta de Inscritos)

Foi realizada uma refatoração completa no módulo de consulta de inscritos (`estagiario`) para resolver problemas de performance (N+1 queries) e implementar paginação real no banco de dados.

### 1. Otimização de Consultas (Query Optimization)
- **Problema Anterior:** A listagem de inscritos fazia uma consulta adicional para cada linha para buscar o "Tipo de Terapia" (N+1), resultando em centenas de queries por página.
- **Solução:** Implementado `prefetch_related` para carregar os tipos de terapia em lote (2 queries adicionais constantes, independente do número de registros).
- **Resultado:** Redução de ~60 queries para ~12 queries por carregamento de página.

### 2. Paginação no Banco de Dados (Server-Side Pagination)
- **Problema Anterior:** O sistema carregava **todos** os inscritos do banco para a memória Python e fazia a paginação via lista (`list[start:end]`). Isso causaria estouro de memória com o crescimento da base.
- **Solução:** Implementado `Paginator` do Django, que utiliza `LIMIT` e `OFFSET` no SQL.
- **Configuração:** 50 itens por página.

### 3. Índices de Banco de Dados
- Adicionados índices compostos e simples nas tabelas `Inscritocomunidade` e `Inscritoconvenio` para acelerar a ordenação por data de inscrição (`dthinscricao`).

### 4. Testes de Performance
- Criado teste automatizado `ConsultaInscritosPerfTest` em `clinicaps/estagiario/tests.py`.
- O teste valida:
    - Número de queries executadas (garante que não há N+1).
    - Paginação correta (50 itens).
    - Separação de contextos (Comunidade vs Convênio).

## 🛠 Como rodar os testes

```bash
python manage.py test estagiario
```

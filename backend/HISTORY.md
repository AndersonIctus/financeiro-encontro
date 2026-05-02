# Histórico de Versões

## [0.4.0] — 2026-05-01

### Adicionado
- Autenticação via JWT com endpoint `POST /auth/login`
- Migration da tabela de usuários (gerenciados via seeds, sem cadastro público)
- Endpoint `PATCH /lancamentos/conciliar-lancamento/{id}` para conciliação manual
- Endpoints de dashboard: totais, por dia e por mês com filtros
- CORS configurável via variável de ambiente `CORS_ORIGINS`
- Filtro por `finalidade_id` no endpoint de lançamentos
- Endpoint `GET /extratos-bancarios/{id}/download` para baixar o CSV importado
- Suporte a variáveis de ambiente para JWT, porta e CORS (centralizadas em `config.py`)
- Dockerfiles e configuração para deploy com Docker Compose completo

### Corrigido
- Exceção correta (`401 Não Autorizado`) em chamadas sem token ou com token inválido
- Variáveis de ambiente de deploy ajustadas para funcionar tanto localmente quanto via Docker

---

## [0.3.0] — 2026-04-14

### Adicionado
- CRUD de extratos bancários (`/extratos-bancarios`)
- Parser de CSV para conciliação (suporte ao formato Banco Inter)
- Engine de conciliação (`Conciliador`) com deduplicação por hash MD5
- Rota de upload de CSV (`POST /conciliacao/upload`)
- Sugestão automática de finalidade por palavras-chave no lançamento
- Estado de processamento no extrato bancário
- Endpoint de finalidades (`/finalidades`) com seeds de dados
- Seeds reorganizados em pasta dedicada

### Corrigido
- Integração do conciliador desacoplada do domínio principal
- Modelos ajustados para funcionar dentro de seus próprios domínios
- Upgrade de dependências do banco de dados

---

## [0.2.0] — 2026-03-29

### Adicionado
- Modelo ORM de lançamentos com enums (`TipoLancamento`, `StatusLancamento`, `FormaPagamento`)
- CRUD completo de lançamentos (`/lancamentos`)
- Paginação e ordenação genérica via `QueryParams` e `sort_utils`
- DTO base para filtros de listagem
- Integração com Alembic e primeira migration do banco de dados

### Corrigido
- Exceções `NotFoundException` tratadas sem derrubar o servidor

---

## [0.1.0] — 2026-03-14

### Adicionado
- Estrutura inicial do projeto FastAPI com arquitetura em camadas (`routers`, `services`, `repositories`, `schemas`, `models`)
- Configuração do ambiente virtual e script `start-backend.sh`
- Integração com PostgreSQL via SQLAlchemy
- Docker Compose para banco de dados e pgAdmin

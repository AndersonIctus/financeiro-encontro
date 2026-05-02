# Financeiro Encontro — Backend

Backend do sistema **Financeiro Encontro**, responsável por gerenciar toda a lógica financeira do evento.

Este serviço fornece uma API REST para controle de:

- Entradas e saídas financeiras
- Formas de pagamento (PIX, dinheiro, cartão)
- Finalidades (oferta, campanha, inscrição)
- Importação e conciliação de extratos bancários via CSV

---

## Tecnologias Utilizadas

- Python 3.11
- FastAPI
- SQLAlchemy 2.0
- Pydantic v2
- PostgreSQL 15
- Pandas (processamento de CSV)
- Docker

---

## Arquitetura

O backend segue uma **arquitetura em camadas**, separando responsabilidades:

```
app/
│
├── core/          # Configurações e exceções customizadas
├── database/      # Sessão do banco e seeds de dados
├── models/        # Entidades ORM (SQLAlchemy)
├── schemas/       # Validação de dados (Pydantic) e DTOs de filtro
├── repositories/  # Acesso ao banco de dados
├── services/      # Regras de negócio
├── routers/       # Endpoints HTTP
├── integracao/    # Parser de CSV e engine de conciliação
├── utils/         # Funções auxiliares (hash, sorting)
│
└── main.py        # Inicialização da aplicação
```

Fluxo de uma requisição:

```
Request → Router → Service → Repository → Banco
```

---

## Banco de Dados

- PostgreSQL 15
- Schema gerenciado via **Alembic** (migrations versionadas)
- Seeds de dados executados no startup (finalidades padrão)

⚠️ O backend **depende do banco rodando via Docker** antes de ser iniciado.

---

## Como rodar

### 1. Subir o banco

Na raiz do projeto:

```bash
docker compose -f docker-compose-db.yml up -d
```

### 2. Rodar o backend

```bash
cd backend
./start-backend.sh
```

O script faz automaticamente:

- Cria o venv (se não existir)
- Ativa o ambiente virtual
- Instala dependências
- Carrega o `.env` se existir na pasta `backend/`
- Inicia o servidor FastAPI na porta definida por `APP_PORT` (padrão: 8000)

---

## Variáveis de Ambiente

O projeto usa dois arquivos `.env.example` conforme o contexto:

| Arquivo | Quando usar |
|---|---|
| `backend/.env.example` | Desenvolvimento local (`./start-backend.sh`) |
| `.env.example` (raiz) | Stack completa com Docker Compose |

### Configurando para desenvolvimento local

```bash
cd backend
cp .env.example .env
# edite .env com os valores reais
```

### Variáveis disponíveis

| Variável | Descrição | Padrão | Obrigatória |
|---|---|---|---|
| `DATABASE_URL` | URL de conexão com o banco | `postgresql://...@localhost:5432/financeiro_encontro` | Sim |
| `UPLOAD_FOLDER` | Pasta onde os CSVs são salvos | `./uploads` | Não |
| `APP_PORT` | Porta em que o servidor sobe | `8000` | Não |
| `JWT_SECRET` | Chave secreta para assinar os tokens | `changeme-insecure-secret` | **Sim em produção** |
| `JWT_ALGORITHM` | Algoritmo de assinatura JWT | `HS256` | Não |
| `JWT_EXPIRE_MINUTES` | Expiração do token em minutos | `480` (8 horas) | Não |
| `SQL_ECHO` | Exibe queries SQL no console | `false` | Não |

> ⚠️ O arquivo `.env` está no `.gitignore` e **nunca deve ser commitado**. Apenas `.env.example` é versionado.

> ⚠️ Em produção, sempre defina um `JWT_SECRET` forte. Para gerar:
> ```bash
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

---

## Acessos

| Serviço | URL |
|---|---|
| API | `http://localhost:{APP_PORT}` |
| Swagger | `http://localhost:{APP_PORT}/docs` |
| Health Check | `http://localhost:{APP_PORT}/health` |

---

## Autenticação

Todas as rotas — exceto `/auth/login` e `/health` — exigem um token JWT no header:

```
Authorization: Bearer <token>
```

O token é obtido via `POST /auth/login`. Por padrão expira em **8 horas** (configurável via `JWT_EXPIRE_MINUTES`).

### Autenticação `/auth`

| Método | Rota | Descrição | Pública |
|---|---|---|---|
| POST | `/auth/login` | Gera token JWT | Sim |
| GET | `/auth/me` | Retorna usuário autenticado | Não |

---

## Endpoints

### Lançamentos `/lancamentos`

| Método | Rota | Descrição |
|---|---|---|
| GET | `/lancamentos/` | Listar com paginação e filtros |
| GET | `/lancamentos/all` | Listar todos sem paginação |
| GET | `/lancamentos/{id}` | Buscar por ID |
| POST | `/lancamentos/` | Criar lançamento |
| PUT | `/lancamentos/{id}` | Atualizar lançamento |
| DELETE | `/lancamentos/{id}` | Excluir lançamento |
| PATCH | `/lancamentos/conciliar-lancamento/{id}?idFinalidade={id}` | Conciliar manualmente um lançamento |

**Filtros disponíveis no GET `/lancamentos/`:**
- `data_inicio` / `data_fim` — intervalo de data de pagamento
- `status` — `CONCILIADO` ou `NAO_CONCILIADO`
- `tipo` — `RECEITA` ou `DESPESA`
- `skip` / `limit` — paginação
- `sort` — ordenação (ex: `data_pagamento:desc`)

---

### Finalidades `/finalidades`

| Método | Rota | Descrição |
|---|---|---|
| GET | `/finalidades/` | Listar com paginação |
| GET | `/finalidades/all` | Listar todas sem paginação |
| GET | `/finalidades/{id}` | Buscar por ID |

> Finalidades são gerenciadas via seeds. Não há endpoints de criação ou edição.

---

### Extratos Bancários `/extratos-bancarios`

| Método | Rota | Descrição |
|---|---|---|
| GET | `/extratos-bancarios/` | Listar com paginação e filtros |
| GET | `/extratos-bancarios/all` | Listar todos sem paginação |
| GET | `/extratos-bancarios/{id}` | Buscar por ID |
| DELETE | `/extratos-bancarios/{id}` | Excluir extrato |

**Filtros disponíveis:**
- `nome_arquivo` — filtro por nome do arquivo
- `processado_em_inicio` / `processado_em_fim` — intervalo de data de processamento

---

### Conciliação `/conciliacao`

| Método | Rota | Descrição |
|---|---|---|
| POST | `/conciliacao/upload` | Upload e processamento de CSV bancário |

---

## Fluxo de Conciliação via CSV

1. Upload de CSV (formato Banco Inter) via `POST /conciliacao/upload`
2. Backend valida e processa o arquivo
3. Cria lançamentos automaticamente como `NAO_CONCILIADO`
4. Aplica sugestão automática de finalidade por palavras-chave
5. Retorna relatório com totais de inseridos, duplicados e erros
6. Usuário concilia manualmente via `PATCH /lancamentos/conciliar-lancamento/{id}`

### Deduplicação

Cada lançamento gera um hash MD5 a partir de `data_pagamento + valor + descricao`. Reenviar o mesmo CSV não duplica registros.

---

## Migrations (Alembic)

Os comandos abaixo devem ser executados dentro da pasta `backend/` com o venv ativo.

### Aplicar todas as migrations pendentes

```bash
alembic upgrade head
```

### Gerar nova migration a partir das mudanças nos models

```bash
alembic revision --autogenerate -m "descricao da mudanca"
```

> Sempre revise o arquivo gerado em `alembic/versions/` antes de aplicar — o autogenerate não detecta tudo (ex: renomeações de coluna).

### Reverter a última migration

```bash
alembic downgrade -1
```

### Ver histórico de migrations

```bash
alembic history
```

### Ver qual migration está aplicada no banco

```bash
alembic current
```

---

## Problemas comuns

**Erro de conexão com o banco:**

```
could not connect to server
```

Solução: subir o banco antes do backend.

```bash
docker compose -f docker-compose-db.yml up -d
```

---

## Próximos passos

- Suporte a outros bancos no parser de CSV (Itaú, Bradesco, Santander)
- Deploy em nuvem (banco de dados + backend + frontend)

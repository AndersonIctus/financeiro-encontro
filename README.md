# Financeiro Encontro

Sistema web para gerenciamento financeiro de encontros da igreja, permitindo controle de entradas e saídas, conciliação de extratos bancários via CSV e geração de relatórios financeiros.

---

## Funcionalidades

- Registro de receitas e despesas (PIX, dinheiro, cartão)
- Organização por finalidades (ofertas, campanhas, inscrições)
- Importação e conciliação de extratos bancários (Banco Inter — limite 3 MB)
- Dashboard financeiro com totais, por dia e por mês
- Relatórios PDF: Livro Caixa e Resumo Geral (pivot por forma de pagamento e finalidade)
- CRUD de usuários com controle de acesso por perfil (RBAC)
- Autenticação via JWT

---

## Perfis de Acesso (RBAC)

| Perfil | Acesso |
|---|---|
| `ADMINISTRADOR` | Acesso total ao sistema (lançamentos, conciliação, arquivos, finalidades, usuários, relatórios) |
| `CONCILIADOR` | Acesso financeiro — lançamentos, conciliação e arquivos. Sem acesso às telas de administração |
| `REPORTER` | Somente Dashboard (sem navegar para lançamentos) e Relatórios |

Usuários são gerenciados pela tela **Administração → Usuários** (somente ADMINISTRADOR). O usuário de ID 1 (administrador principal) não pode ser excluído, e nenhum usuário pode excluir a si mesmo.

---

## Stack

| Camada | Tecnologia |
|---|---|
| Frontend | Angular 21 + TypeScript 5.9 (strict) + SCSS |
| Backend | Python 3.11 + FastAPI + SQLAlchemy 2.0 |
| Banco | PostgreSQL 15 |
| Infra | Docker + Docker Compose + Nginx |

---

## Como subir o projeto

### Opção 1 — Stack completa com Docker

**Pré-requisitos:** Docker e Docker Compose instalados.

**1. Copiar e preencher o `.env`:**

```bash
cp .env.example .env
```

Edite o `.env` e defina ao menos:

| Variável | O que preencher |
|---|---|
| `POSTGRES_PASSWORD` | Senha do banco (qualquer valor) |
| `JWT_SECRET` | Chave aleatória segura — gere com `python -c "import secrets; print(secrets.token_hex(32))"` |

As demais variáveis já têm valores funcionais no `.env.example`.

**2. Build e start:**

```bash
docker compose up --build
```

Na primeira execução o build demora alguns minutos (download de imagens + compilação do Angular). Nas próximas execuções use `docker compose up` (sem `--build`) para subir sem recompilar.

**3. Aguardar os containers ficarem saudáveis:**

O backend aguarda o PostgreSQL passar no healthcheck antes de iniciar. Acompanhe com:

```bash
docker compose logs -f
```

Quando aparecer `Application startup complete.` o sistema está pronto.

#### Acessos (Docker)

| Serviço | URL |
|---|---|
| Frontend | `http://localhost` |
| API | `http://localhost:8000` |
| Swagger | `http://localhost:8000/docs` |
| Health Check | `http://localhost:8000/health` |

#### Comandos úteis

```bash
docker compose down           # para e remove os containers (dados persistem nos volumes)
docker compose down -v        # para e remove containers E volumes (apaga o banco)
docker compose logs -f backend   # logs em tempo real do backend
docker compose logs -f frontend  # logs em tempo real do frontend
docker compose up --build --no-cache  # força rebuild completo sem cache
```

---

### Opção 2 — Desenvolvimento local

**Pré-requisitos:** Docker (para o banco), Python 3.11, Node.js 20+.

**1. Subir o banco:**

```bash
docker compose -f docker-compose-db.yml up -d
```

**2. Subir o backend:**

```bash
cd backend
cp .env.example .env   # preencha os valores (primeira vez)
./start-backend.sh
```

O script cria o venv, instala dependências, aplica as migrations e sobe o servidor na porta definida em `APP_PORT` (padrão: `8000`).

**3. Subir o frontend:**

```bash
cd frontend/financeiro-encontro
npm install
npm start            # ng serve em http://localhost:4200
```

#### Acessos (desenvolvimento local)

| Serviço | URL |
|---|---|
| Frontend | `http://localhost:4200` |
| API | `http://localhost:8000` |
| Swagger | `http://localhost:8000/docs` |
| Health Check | `http://localhost:8000/health` |
| pgAdmin | `http://localhost:9090` |

---

## Documentação detalhada

- [backend/README.md](backend/README.md) — endpoints, autenticação, variáveis de ambiente, migrations e fluxo de conciliação
- [frontend/financeiro-encontro/README.md](frontend/financeiro-encontro/README.md) — estrutura de componentes, variáveis de ambiente e build

---

## Licença

Projeto interno utilizado para gerenciamento financeiro do encontro da igreja.

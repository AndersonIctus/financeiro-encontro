# Financeiro Encontro

Sistema web para gerenciamento financeiro de encontros da igreja, permitindo controle de entradas e saídas, conciliação de extratos bancários via CSV e geração de relatórios financeiros.

---

## Funcionalidades

- Registro de receitas e despesas (PIX, dinheiro, cartão)
- Organização por finalidades (ofertas, campanhas, inscrições)
- Importação e conciliação de extratos bancários (Banco Inter)
- Dashboard financeiro com totais, por dia e por mês
- Autenticação via JWT

---

## Stack

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.11 + FastAPI + SQLAlchemy 2.0 |
| Banco | PostgreSQL 15 |
| Infra | Docker + Docker Compose + Nginx |

---

## Como subir o projeto

### Opção 1 — Stack completa com Docker

```bash
cp .env.example .env   # preencha os valores
docker compose up --build
```

Acesse em `http://localhost`.

### Opção 2 — Desenvolvimento local

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

---

## Acessos (desenvolvimento local)

| Serviço | URL |
|---|---|
| API | `http://localhost:8000` |
| Swagger | `http://localhost:8000/docs` |
| Health Check | `http://localhost:8000/health` |
| pgAdmin | `http://localhost:9090` |

---

## Documentação detalhada

- [backend/README.md](backend/README.md) — endpoints, autenticação, variáveis de ambiente, migrations e fluxo de conciliação

---

## Licença

Projeto interno utilizado para gerenciamento financeiro do encontro da igreja.

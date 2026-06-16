# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Financeiro Encontro** is a financial management system for church events. It handles income/expense tracking, payment reconciliation via CSV import (Banco Inter), dashboard reporting, and JWT-based authentication.

## Development Commands

### Database (start first)
```bash
docker compose -f docker-compose-db.yml up -d
# PostgreSQL on :5432, pgAdmin on :9090
# Requires .env at project root with POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
```

### Backend (FastAPI/Python)
```bash
cd backend
cp .env.example .env   # first time only — fill in values
./start-backend.sh     # creates venv, installs deps, loads .env, runs uvicorn on $APP_PORT
```

### Frontend (Angular)
```bash
cd frontend/financeiro-encontro
npm install
npm start            # ng serve on :4200
npm run build        # production build
npm test             # vitest
npm run test:watch   # vitest watch mode
```

### Full Stack (Docker)
```bash
cp .env.example .env   # first time only — fill in values
docker compose up --build   # Nginx :80, backend :$APP_PORT, DB :5432
```

## Architecture

### Stack
- **Backend**: Python 3.11 + FastAPI + SQLAlchemy 2.0 + PostgreSQL 15
- **Frontend**: Angular 21 (standalone components) + TypeScript strict + SCSS
- **Infra**: Docker Compose + Nginx reverse proxy

### Backend Layer Structure (`backend/app/`)
```
core/         # config.py (all env vars), security.py (JWT + bcrypt), exceptions, deps.py (get_current_user)
database/     # DB session factory, seed data loader (runs on startup via lifespan)
models/       # SQLAlchemy ORM models + enums
schemas/      # Pydantic request/response schemas + filter DTOs
repositories/ # Data access layer — all DB queries live here
services/     # Business logic — orchestrates repositories
routers/      # FastAPI route handlers — thin, delegate to services
integracao/   # CSV parsing (ParserFactory pattern) + Conciliador engine
utils/        # Shared helpers (hash_utils, sort_utils)
```

**Key domain models:**
- `Lancamento`: Financial transaction (RECEITA/DESPESA), with payment form (PIX/DINHEIRO/CARTAO_*), status (CONCILIADO/NAO_CONCILIADO), and a deduplication `hash_transacao`
- `Finalidade`: Category/purpose for a transaction — full CRUD via API; seeds provide initial data at startup
- `ExtratoBancario`: Imported bank statement file record
- `Usuario`: Authenticated user — read-only via API, managed via seeds

### Authentication
All routes except `POST /auth/login` and `GET /health` require a JWT bearer token.
Token obtained via `POST /auth/login`. Dependency `get_current_user` in `core/deps.py` validates it on every protected request.
Users are seeded at startup — no registration endpoint.

### Deduplication Logic
Hashes are generated from `descricao_normalizada + valor + data_pagamento` (SHA-256). A unique constraint on `hash_transacao` in the DB prevents duplicates. The service layer checks before insert and the reconciliation engine (`Conciliador`) uses the same logic when processing CSV imports.

### CSV Reconciliation Flow
`POST /conciliacao/upload` → `ConciliacaoService` → `ParserFactory` (selects bank parser) → `Conciliador.processar()` → returns report with inserted/duplicated/errored counts. Currently only Banco Inter CSV format is supported.
After import, records are `NAO_CONCILIADO`. Manual reconciliation via `PATCH /lancamentos/conciliar-lancamento/{id}?idFinalidade={id}`.

### Dashboard Endpoints
`GET /dashboard/totais` — aggregated totals (receitas, despesas, saldo, quantidade).
`GET /dashboard/por-dia` — day-by-day breakdown for a period.
`GET /dashboard/por-mes` — month-by-month breakdown for a period.
`GET /dashboard/por-finalidade` — totals grouped by finalidade (id, nome, total_valor, quantidade).
All share the same filter DTO: `data_inicio`, `data_fim` (defaults: today → today+30d), `forma_pagamento[]`, `finalidade_id[]`, `tipo`, `status`.

### Frontend Structure (`frontend/financeiro-encontro/src/app/`)
Angular standalone component architecture — no `NgModule`. Routes defined in `app.routes.ts`, app bootstrapped in `app.config.ts`. All components use `bootstrapApplication` pattern.

### API Base URL
Frontend communicates with backend at `http://localhost:{APP_PORT}` in development (default 8000). In Docker, Nginx proxies frontend and backend together on port 80.

## Key Config Locations
- **All env vars**: `backend/app/core/config.py` — single source of truth, reads from environment
- **Local dev env**: `backend/.env` (gitignored) — copy from `backend/.env.example`
- **Docker env**: `.env` at project root (gitignored) — copy from `.env.example`
- **Backend Python deps**: `backend/requirements.txt`
- **Frontend deps**: `frontend/financeiro-encontro/package.json`
- **DB schema**: managed via Alembic migrations (`backend/alembic/versions/`)
- **Seed data**: `backend/app/database/seeds/` — runs on startup, idempotent

## Environment Variables Reference

| Variable | Default | Purpose |
|---|---|---|
| `DATABASE_URL` | `postgresql://...@localhost:5432/financeiro_encontro` | DB connection string |
| `UPLOAD_FOLDER` | `uploads` | Folder for uploaded CSV files |
| `APP_PORT` | `8000` | Port uvicorn listens on |
| `JWT_SECRET` | `changeme-insecure-secret` | JWT signing key — always override in production |
| `JWT_ALGORITHM` | `HS256` | JWT algorithm |
| `JWT_EXPIRE_MINUTES` | `480` | Token expiry (8 hours) |
| `SQL_ECHO` | `false` | Log all SQL queries to console — enable in development only |
| `CORS_ORIGINS` | `http://localhost:4200` | Allowed CORS origins (comma-separated) |

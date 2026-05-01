# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Financeiro Encontro** is a financial management system for church events. It handles income/expense tracking, payment reconciliation via CSV import (Banco Inter), and financial reporting.

## Development Commands

### Database (start first)
```bash
docker compose -f docker-compose-db.yml up -d
# PostgreSQL on :5432, pgAdmin on :9090
```

### Backend (FastAPI/Python)
```bash
cd backend
./start-backend.sh   # creates venv, installs deps, runs uvicorn on :8000
# or manually:
python -m uvicorn app.main:app --reload --port 8000
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
docker compose up --build   # Nginx :80, backend :8000, DB :5432
```

## Architecture

### Stack
- **Backend**: Python 3.11 + FastAPI + SQLAlchemy 2.0 + PostgreSQL 15
- **Frontend**: Angular 21 (standalone components) + TypeScript strict + SCSS
- **Infra**: Docker Compose + Nginx reverse proxy

### Backend Layer Structure (`backend/app/`)
```
core/         # Config (settings.py), security, custom exceptions
database/     # DB session factory, seed data loader (runs on startup)
models/       # SQLAlchemy ORM models
schemas/      # Pydantic request/response schemas
repositories/ # Data access layer — all DB queries live here
services/     # Business logic — orchestrates repositories
routers/      # FastAPI route handlers — thin, delegate to services
integracao/   # CSV parsing (ParserFactory pattern) + Conciliador engine
utils/        # Shared helpers
```

**Key domain models:**
- `Lancamento`: Financial transaction (RECEITA/DESPESA), with payment form (PIX/DINHEIRO/CARTAO_*), status (CONCILIADO/NAO_CONCILIADO), and a deduplication `hash_transacao`
- `Finalidade`: Category/purpose for a transaction
- `ExtratoBancario`: Imported bank statement row

### Deduplication Logic
Hashes are generated from `data_pagamento + valor + descricao + observacao` (MD5). A unique constraint on `hash_transacao` in the DB prevents duplicates. The service layer checks before insert and the reconciliation engine (`Conciliador`) uses the same logic when processing CSV imports.

### CSV Reconciliation Flow
`POST /conciliacao` → `ConciliadorService` → `ParserFactory` (selects bank parser) → returns `ConciliacaoDTO` with lists of inserted, duplicated, and errored rows. Currently only Banco Inter CSV format is supported.

### Frontend Structure (`frontend/financeiro-encontro/src/app/`)
Angular standalone component architecture — no `NgModule`. Routes defined in `app.routes.ts`, app bootstrapped in `app.config.ts`. All components use `bootstrapApplication` pattern.

### API Base URL
Frontend communicates with backend at `http://localhost:8000` in development. In Docker, Nginx proxies frontend and backend together on port 80.

## Key Config Locations
- Backend env/DB credentials: `docker-compose.yml` environment section (not `.env`)
- Backend Python deps: `backend/requirements.txt`
- Frontend deps: `frontend/financeiro-encontro/package.json`
- DB schema: defined via SQLAlchemy models (no Alembic migrations yet — schema is created via `Base.metadata.create_all`)

# Financeiro Encontro — Backend

Backend do sistema **Financeiro Encontro**, responsável por gerenciar toda a lógica financeira do evento.

Este serviço fornece uma API REST para controle de:

- Entradas e saídas financeiras
- Formas de pagamento (PIX, dinheiro, cartão)
- Finalidades (oferta, campanha, inscrição)
- Importação e conciliação de extratos bancários
- Relatórios financeiros

---

# 📌 Objetivo

Este backend foi desenvolvido para garantir:

- organização financeira do evento
- rastreabilidade das movimentações
- facilidade na prestação de contas
- base para relatórios contábeis

---

# 🧱 Tecnologias Utilizadas

- Python 3.11
- FastAPI
- SQLAlchemy 2.0
- Pydantic
- PostgreSQL
- Pandas (processamento de CSV)
- Docker

---

# 🏗️ Arquitetura

O backend segue uma **arquitetura em camadas**, separando responsabilidades:

```
app/
│
├── core/          # Configurações e segurança
├── database/      # Conexão com banco
├── models/        # Entidades do banco
├── schemas/       # Validação de dados (Pydantic)
├── repositories/  # Acesso ao banco (futuro)
├── services/      # Regras de negócio
├── routers/       # Endpoints HTTP
├── utils/         # Funções auxiliares
│
└── main.py        # Inicialização da aplicação
```

---

# 🔄 Fluxo da Aplicação

```
Request → Router → Service → Model → Banco
```

---

# 🗄️ Banco de Dados

Banco utilizado:

- PostgreSQL

⚠️ IMPORTANTE:

O backend **depende do banco rodando via Docker**.

---

# 🚀 Como rodar o backend

## 1. Subir o banco

Na raiz do projeto:

```bash
docker compose -f docker-compose-db.yml up -d
```

---

## 2. Rodar backend

```bash
cd backend
./start-backend.sh
```

Esse script faz automaticamente:

- cria o venv (se não existir)
- ativa o ambiente virtual
- instala dependências
- inicia o servidor FastAPI

---

# 🌐 Acessos

API:

http://localhost:8000

Swagger:

http://localhost:8000/docs

Health Check:

http://localhost:8000/health

---

# 📡 Endpoints principais

## Lançamentos

- GET /lancamentos → listar lançamentos
- POST /lancamentos → criar lançamento
- PUT /lancamentos → atualizar lançamento
- DELETE /lancamentos → excluir lançamento

---

## Extrato bancário

- POST /extrato-bancario → importar CSV
- GET /extrato-bancario → listar extratos

---

## Sistema

- GET /health → verificar status da API

---

# 📥 Conciliação de Extratos

Fluxo:

1. Upload de CSV (Banco Inter)
2. Backend processa arquivo
3. Cria lançamentos automaticamente
4. Marca como NÃO CONCILIADO
5. Usuário ajusta finalidade depois

---

# ⚠️ Problemas comuns

## Erro: conexão com banco

```
could not connect to server
```

✔ Solução:

```bash
docker compose -f docker-compose-db.yml up -d
```

---

## Erro: tabela não existe

```
relation "lancamentos" does not exist
```

✔ Isso será resolvido na próxima etapa com migrations (Alembic)

---

# 🔐 Segurança (próximos passos)

Planejado:

- autenticação JWT
- controle de acesso
- proteção de endpoints

---

# 📈 Evoluções futuras

- Alembic (migrations)
- autenticação JWT
- paginação
- filtros avançados
- dashboard financeiro
- geração de relatórios
- logs estruturados
- tratamento global de erros

---

# 📌 Observações

Este backend foi projetado para ser:

- simples de usar durante o evento
- robusto para evitar erros financeiros
- escalável para futuras melhorias

---

# 📄 Licença

Projeto interno para uso no gerenciamento financeiro do encontro da igreja.

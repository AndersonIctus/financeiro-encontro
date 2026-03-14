# Financeiro Encontro --- Backend

Backend do sistema **Financeiro Encontro**, uma aplicação desenvolvida
para auxiliar na gestão financeira de eventos da igreja.

O sistema permite registrar **entradas e saídas financeiras**,
acompanhar pagamentos realizados via **PIX, dinheiro e cartão**, além de
permitir a **conciliação de extratos bancários** e geração de relatórios
financeiros.

Este backend fornece uma **API REST** construída com FastAPI que será
consumida por um frontend Angular.

------------------------------------------------------------------------

# Objetivo do Sistema

Durante a organização de um encontro da igreja existem várias
movimentações financeiras:

-   Ofertas
-   Campanhas
-   Inscrições
-   Pagamentos diversos
-   Despesas operacionais

O objetivo deste sistema é **centralizar e registrar todas essas
movimentações**, permitindo:

-   controle financeiro do evento
-   rastreamento de pagamentos
-   conciliação com extratos bancários
-   geração de relatórios financeiros

------------------------------------------------------------------------

# Tecnologias Utilizadas

Backend

-   Python 3.11
-   FastAPI
-   SQLAlchemy
-   Pydantic
-   PostgreSQL
-   Pandas

Infraestrutura

-   Docker
-   Docker Compose

------------------------------------------------------------------------

# Arquitetura do Backend

O backend segue uma arquitetura organizada em camadas para facilitar
manutenção e evolução do sistema.

Estrutura principal:

backend/

app/ core/ database/ models/ schemas/ routers/ services/ utils/

main.py

Descrição das camadas:

core\
Configurações globais da aplicação.

database\
Configuração de conexão com o banco de dados.

models\
Entidades do banco de dados (SQLAlchemy).

schemas\
Validação de dados usando Pydantic.

routers\
Endpoints HTTP da API.

services\
Regras de negócio da aplicação.

utils\
Funções utilitárias.

main.py\
Ponto de entrada da aplicação FastAPI.

------------------------------------------------------------------------

# Dependência do Banco de Dados

O backend depende de um banco **PostgreSQL rodando em Docker**.

Sem o banco ativo o backend **não conseguirá iniciar corretamente**.

Para subir o banco execute na raiz do projeto:

docker compose -f docker-compose-db.yml up -d

Verifique se o container está rodando:

docker ps

------------------------------------------------------------------------

# Rodando o Backend Localmente

Entre na pasta do backend:

```cd backend```

Crie um ambiente virtual:

```python -m venv venv```

Ative o ambiente virtual.

Linux ou Mac:

```source venv/bin/activate```

Windows:

```venv`\Scripts`{=tex}`\activate`{=tex}```

Instale as dependências:

```pip install -r requirements.txt```

Inicie o servidor:

```uvicorn app.main:app --reload```

------------------------------------------------------------------------

# Acessando a API

Documentação Swagger:

```http://localhost:8000/docs```

Health check:

```http://localhost:8000/health```

------------------------------------------------------------------------

# Estrutura de Diretórios
```
backend/
    app/ 
        core/ 
            config.py
        database/ 
            base.py 
            session.py
        models/ 
            lancamento.py 
            finalidade.py 
            extrato.py
        schemas/
        routers/
        services/
        utils/
    main.py
    requirements.txt 
    Dockerfile
```
------------------------------------------------------------------------

# Próximas Evoluções do Backend

As próximas melhorias planejadas para o sistema incluem:

-   migrations com Alembic
-   autenticação JWT
-   paginação de endpoints
-   filtros avançados de lançamentos
-   upload de extratos bancários
-   conciliação automática de pagamentos
-   geração de relatórios financeiros
-   logging estruturado
-   tratamento global de exceções

------------------------------------------------------------------------

# Licença

Projeto interno desenvolvido para gerenciamento financeiro do encontro
da igreja.

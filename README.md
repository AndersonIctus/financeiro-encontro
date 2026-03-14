Financeiro Encontro

Sistema web para gerenciamento financeiro de um encontro da igreja,
permitindo o controle de entradas e saídas financeiras durante reuniões
de preparação e durante o evento final.

O objetivo do sistema é ajudar a equipe financeira a registrar
pagamentos, acompanhar receitas e despesas, conciliar pagamentos via PIX
e gerar relatórios financeiros.

------------------------------------------------------------------------

FUNCIONALIDADES DO SISTEMA

O sistema permitirá gerenciar:

-   Ofertas
-   Campanhas
-   Inscrições de participantes
-   Inscrições de trabalhadores
-   Receitas
-   Despesas
-   Pagamentos via PIX
-   Pagamentos em dinheiro
-   Pagamentos em cartão

Também será possível realizar:

-   Conciliação de extratos bancários
-   Relatórios financeiros
-   Dashboard de acompanhamento financeiro

------------------------------------------------------------------------

TECNOLOGIAS UTILIZADAS

Backend - Python 3.11 - FastAPI - SQLAlchemy - PostgreSQL - Pandas

Infraestrutura - Docker - Docker Compose

------------------------------------------------------------------------

ARQUITETURA DO BACKEND

O backend segue uma arquitetura em camadas para manter o código
organizado e escalável.

Estrutura principal:

backend/ app/ core/ -> configurações do sistema database/ -> conexão com
banco de dados models/ -> entidades do banco schemas/ -> validação de
dados routers/ -> endpoints HTTP services/ -> regras de negócio utils/
-> utilidades

main.py -> inicialização da aplicação FastAPI

------------------------------------------------------------------------

BANCO DE DADOS

O sistema depende de um banco PostgreSQL rodando em um container Docker.

Antes de iniciar o backend localmente é necessário subir o banco.

Comando:

docker compose -f docker-compose-db.yml up -d

Para verificar se o container está rodando:

docker ps

------------------------------------------------------------------------

RODANDO O BACKEND LOCALMENTE

Entrar na pasta do backend:

cd backend

Criar ambiente virtual:

python -m venv venv

Ativar ambiente virtual

Linux ou Mac:

source venv/bin/activate

Windows:

venv

Instalar dependências:

pip install -r requirements.txt

Executar o servidor:

uvicorn app.main:app –reload

------------------------------------------------------------------------

ACESSANDO A API

Swagger (documentação automática):

http://localhost:8000/docs

Health check:

http://localhost:8000/health

------------------------------------------------------------------------

IMPORTANTE

O backend depende do PostgreSQL rodando em Docker.

Caso o banco não esteja ativo ocorrerá erro de conexão.

Para subir o banco:

docker compose -f docker-compose-db.yml up -d

------------------------------------------------------------------------

PRÓXIMOS PASSOS DO PROJETO

Evoluções planejadas:

-   Migrations com Alembic
-   Autenticação JWT
-   Paginação de endpoints
-   Filtros de lançamentos
-   Upload de extratos bancários
-   Conciliação automática de pagamentos
-   Geração de relatórios financeiros
-   Logs estruturados
-   Tratamento global de exceções

------------------------------------------------------------------------

LICENÇA

Projeto interno utilizado para gerenciamento financeiro do encontro da
igreja.

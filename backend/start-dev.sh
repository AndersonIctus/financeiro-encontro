#!/bin/bash

echo "======================================"
echo "Iniciando Backend - Financeiro Encontro"
echo "======================================"

# cria venv se não existir
if [ ! -d "venv" ]; then
  echo "Criando ambiente virtual..."
  python -m venv venv
fi

echo "Ativando ambiente virtual..."
source venv/Scripts/activate

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Subindo servidor FastAPI..."

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
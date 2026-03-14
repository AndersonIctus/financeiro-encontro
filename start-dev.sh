#!/bin/bash

echo "======================================"
echo "Financeiro Encontro - Ambiente DEV"
echo "======================================"

echo ""
echo "Subindo banco PostgreSQL..."
docker compose -f docker-compose-db.yml up -d

echo ""
echo "Aguardando banco inicializar..."
sleep 5

echo ""
echo "Iniciando backend..."

cd backend

bash start-backend.sh
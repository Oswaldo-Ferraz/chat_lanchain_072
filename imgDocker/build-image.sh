#!/bin/bash

# Script para fazer build e salvar a imagem Docker
# Uso: ./build-image.sh

set -e

echo "🐳 Iniciando build da imagem LangChain API..."

# Navegar para a pasta do projeto
cd "$(dirname "$0")/.."

# Build da imagem
echo "📦 Fazendo build da imagem..."
docker build -f imgDocker/Dockerfile -t langchain-api:latest .

echo "✅ Build concluído!"

# Verificar se a imagem foi criada
echo "📋 Verificando imagem criada..."
docker images | grep langchain-api

# Salvar imagem como arquivo .tar
echo "💾 Salvando imagem como arquivo .tar..."
docker save -o imgDocker/langchain-api.tar langchain-api:latest

echo "🎉 Imagem salva em: imgDocker/langchain-api.tar"
echo "📏 Tamanho do arquivo:"
ls -lh imgDocker/langchain-api.tar

echo ""
echo "🚀 Para fazer upload no Portainer:"
echo "1. Vá em Images → Import"
echo "2. Selecione o arquivo: imgDocker/langchain-api.tar"
echo "3. Tag: langchain-api:latest"
echo "4. Clique em Upload"
echo ""
echo "🔧 Para rodar localmente:"
echo "docker run -d --name langchain-api -p 8000:8000 -e OPENAI_API_KEY=sua_chave langchain-api:latest"

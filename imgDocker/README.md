# 🐳 Docker Image para LangChain API

Esta pasta contém todos os arquivos necessários para criar e fazer deploy da imagem Docker da sua API LangChain.

## 📁 Arquivos incluídos:

- **`Dockerfile`** - Configuração da imagem Docker
- **`requirements.txt`** - Dependências Python
- **`.dockerignore`** - Arquivos a serem ignorados no build
- **`docker-compose.yml`** - Para rodar com Docker Compose
- **`build-image.sh`** - Script automatizado de build
- **`README.md`** - Esta documentação

## 🚀 Como usar:

### Opção 1: Script Automatizado (Recomendado)
```bash
cd imgDocker
./build-image.sh
```

Este script vai:
1. ✅ Fazer build da imagem
2. ✅ Salvar como `langchain-api.tar`
3. ✅ Mostrar instruções de upload

### Opção 2: Comandos manuais
```bash
# Build da imagem
docker build -f imgDocker/Dockerfile -t langchain-api:latest .

# Salvar como arquivo
docker save -o imgDocker/langchain-api.tar langchain-api:latest
```

## 📤 Upload no Portainer:

1. **Portainer** → **Images** → **Import**
2. **Select file**: `langchain-api.tar`
3. **Tag**: `langchain-api:latest`
4. **Upload** ✅

## 🔧 Deploy no Portainer:

### Via Container:
- **Image**: `langchain-api:latest`
- **Port**: `8000:8000`
- **Environment Variables**:
  - `OPENAI_API_KEY=sua_chave_openai`
- **Deploy** ✅

### Via Stack (docker-compose):
Use o arquivo `docker-compose.yml` incluído.

## 🌐 Endpoints da API:

- **POST** `/chat` - Endpoint principal
- **GET** `/health` - Health check
- **GET** `/docs` - Documentação Swagger
- **GET** `/` - Info da API

## 📋 Exemplo de uso:

```bash
curl -X POST "http://seu-ip:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "context": "Python é uma linguagem de programação",
       "question": "Quais são suas vantagens?"
     }'
```

## 🔒 Segurança:

- ✅ Credenciais via environment variables
- ✅ Usuário não-root no container
- ✅ Health checks configurados
- ✅ Nenhuma credencial na imagem

## 📏 Especificações:

- **Base**: Python 3.11-slim
- **Tamanho estimado**: ~800MB
- **Porta**: 8000
- **Health check**: `/health` endpoint

# 🚀 Prompt para Criar Docker-Compose no Portainer Web Editor

## 📋 PROMPT PARA PORTAINER WEB EDITOR:

```
Crie um docker-compose.yml para o Portainer Web Editor com as seguintes especificações:

CONFIGURAÇÃO OBRIGATÓRIA:
- Service name: langchain-api
- Image: python:3.11-slim
- Port: 8000:8000
- Network: fernet (IMPORTANTE: usar "fernet", NÃO "network_public")
- Restart: unless-stopped

COMANDO DE INSTALAÇÃO:
1. Atualizar apt-get e instalar curl + git
2. Clonar repositório: https://github.com/Oswaldo-Ferraz/chat_lanchain_072.git para /app
3. Instalar requirements.txt
4. Instalar uvicorn[standard] separadamente
5. Iniciar: uvicorn src.langchain_fastapi:app --host 0.0.0.0 --port 8000 --reload

ENVIRONMENT VARIABLES:
- OPENAI_API_KEY=[INSERIR_CHAVE_AQUI]
- PINECONE_API_KEY=sua_chave_pinecone_aqui
- ENVIRONMENT=production

TRAEFIK LABELS:
- Host: langchain.agenciafer.com.br
- Entrypoint: websecure
- TLS certresolver: letsencrypt
- Service port: 8000

HEALTH CHECK:
- Test: curl -f http://localhost:8000/health
- Interval: 30s, timeout: 10s, retries: 3, start_period: 60s

NETWORK EXTERNA:
- Nome: fernet (external: true)

ERROS COMUNS A EVITAR:
❌ NÃO usar "network_public" - usar "fernet"
❌ NÃO esquecer de instalar uvicorn[standard]
❌ NÃO esquecer de instalar curl para health check
❌ NÃO usar ports internos diferentes de 8000

Gere o docker-compose.yml completo e funcional.
```

## 🎯 VERSÃO RESUMIDA DO PROMPT:

```
Crie docker-compose para Portainer:
- Image: python:3.11-slim
- Clone: https://github.com/Oswaldo-Ferraz/chat_lanchain_072.git
- Instale: requirements.txt + uvicorn[standard] + curl
- Network: fernet (não network_public!)
- Traefik: langchain.agenciafer.com.br
- Health: curl localhost:8000/health
- Port: 8000
```

## 📊 RESULTADO ESPERADO:

O prompt acima garante que qualquer IA ou pessoa criará o docker-compose correto, evitando os 3 principais erros que enfrentamos:

1. ✅ **Network correto**: `fernet` em vez de `network_public`
2. ✅ **Dependências completas**: FastAPI + Uvicorn instalados
3. ✅ **Health check funcional**: Curl instalado no container

## 🔧 HISTÓRICO DE CORREÇÕES:

### Problemas Resolvidos:
- **Network Issue**: Mudança de `network_public` para `fernet`
- **Missing Dependencies**: Adição de `fastapi==0.104.1` e `uvicorn[standard]==0.24.0` ao requirements.txt
- **Health Check**: Instalação do `curl` no container para monitoramento

### Stack Final Funcionando:
- **API URL**: http://147.79.83.6:8000
- **Health Check**: ✅ {"status":"healthy","chain_loaded":true}
- **Chat Endpoint**: ✅ Responde perguntas via OpenAI GPT-4o
- **Traefik Integration**: ✅ Configurado para langchain.agenciafer.com.br

---

*Criado em: 26 de agosto de 2025*  
*Status: Testado e funcionando em produção*

# 🤖 LangChain Chat API

API REST construída com FastAPI e LangChain para integração com OpenAI GPT-4o.

## 🚀 Funcionalidades

- ✅ **FastAPI** - API REST moderna e rápida
- ✅ **LangChain** - Framework para aplicações com LLM
- ✅ **OpenAI GPT-4o** - Modelo de linguagem avançado
- ✅ **Docker** - Containerização para deploy fácil
- ✅ **Portainer** - Deploy em VPS simplificado
- ✅ **Documentação automática** - Swagger UI em `/docs`

## 📋 Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/` | Informações da API |
| `POST` | `/chat` | Endpoint principal de chat |
| `GET` | `/health` | Health check |
| `GET` | `/docs` | Documentação Swagger |

## 💬 Exemplo de uso

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "context": "Python é uma linguagem de programação",
       "question": "Quais são suas principais vantagens?"
     }'
```

**Resposta:**
```json
{
  "response": "Python possui várias vantagens: sintaxe simples, grande comunidade...",
  "status": "success"
}
```

## 🐳 Deploy com Docker

### Método 1: Build local + Upload Portainer

```bash
cd imgDocker
./build-image.sh
```

Isso gera o arquivo `langchain-api.tar` para upload no Portainer.

### Método 2: Docker Compose

```bash
docker-compose -f imgDocker/docker-compose.yml up -d
```

### Método 3: Container simples

```bash
docker run -d \
  --name langchain-api \
  -p 8000:8000 \
  -e OPENAI_API_KEY=sua_chave_aqui \
  langchain-api:latest
```

## ⚙️ Configuração

### Variáveis de ambiente obrigatórias:

- `OPENAI_API_KEY` - Sua chave da API OpenAI

### Variáveis opcionais:

- `PINECONE_API_KEY` - Para integração com Pinecone
- `ENVIRONMENT` - production/development

## 📁 Estrutura do projeto

```
├── src/
│   ├── 001.py              # Script original de teste
│   └── api_fastapi.py      # API FastAPI principal
├── config/
│   └── config.yaml         # Configurações (sem credenciais)
├── imgDocker/
│   ├── Dockerfile          # Imagem Docker
│   ├── docker-compose.yml  # Compose para deploy
│   ├── build-image.sh      # Script de build
│   └── requirements.txt    # Dependências
├── .env                    # Credenciais locais (não versionado)
└── README.md
```

## 🔧 Desenvolvimento local

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar credenciais

Criar arquivo `.env`:
```
OPENAI_API_KEY=sua_chave_openai
```

### 3. Executar API

```bash
uvicorn src.api_fastapi:app --reload --host 127.0.0.1 --port 8000
```

### 4. Testar script original

```bash
python src/001.py
```

## 🌐 Deploy em produção

### VPS com Portainer:

1. **Upload da imagem:**
   - Portainer → Images → Import
   - Selecionar `imgDocker/langchain-api.tar`
   - Tag: `langchain-api:latest`

2. **Deploy do container:**
   - Containers → Add container
   - Image: `langchain-api:latest`
   - Port: `8000:8000`
   - Environment: `OPENAI_API_KEY=sua_chave`

3. **Acessar:**
   - API: `http://seu-ip:8000/chat`
   - Docs: `http://seu-ip:8000/docs`

## 📚 Integração com n8n

Configure no n8n:

- **URL:** `http://seu-ip:8000/chat`
- **Method:** `POST`
- **Headers:** `Content-Type: application/json`
- **Body:**
```json
{
  "context": "{{ $json.context }}",
  "question": "{{ $json.question }}"
}
```

## 🔒 Segurança

- ✅ Credenciais via environment variables
- ✅ Container com usuário não-root
- ✅ Health checks configurados
- ✅ Arquivos sensíveis no .gitignore
- ✅ Nenhuma credencial hardcoded no código

## 📊 Especificações técnicas

- **Python:** 3.11
- **FastAPI:** 0.104+
- **LangChain:** 0.3.27+
- **Tamanho da imagem:** ~989MB
- **Porta padrão:** 8000

## 🆘 Troubleshooting

### API não inicia:
- Verificar se `OPENAI_API_KEY` está definida
- Conferir logs: `docker logs nome-do-container`

### Erro 500 no /chat:
- Validar chave OpenAI
- Verificar formato do JSON de entrada

### Upload falha no Portainer:
- Arquivo muito grande (usar Docker Registry)
- Conexão lenta (aumentar timeout)

## 📝 Licença

Este projeto é de uso educacional e demonstrativo.

---

**Desenvolvido por:** Oswaldo Ferraz  
**Stack:** FastAPI + LangChain + OpenAI + Docker

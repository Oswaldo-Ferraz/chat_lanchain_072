from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from pathlib import Path
import yaml
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# Carrega .env ao iniciar
load_dotenv()

# Modelos de request/response
class ChatRequest(BaseModel):
    context: str
    question: str

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

# Inicializa FastAPI
app = FastAPI(title="LangChain Chat API", version="1.0.0")

# Carrega chain uma vez na inicialização
def load_config_file() -> dict:
    config_path = Path(__file__).resolve().parent.parent / "config" / "config.yaml"
    if not config_path.exists():
        return {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}

def ensure_api_keys(config: dict):
    if not os.environ.get("OPENAI_API_KEY"):
        yaml_key = config.get("OPENAI_API_KEY") or ""
        if yaml_key:
            os.environ["OPENAI_API_KEY"] = yaml_key
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY não definida")

# Inicializa chain globalmente
try:
    config = load_config_file()
    ensure_api_keys(config)
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="Context: {context}\n\nQuestion: {question}\n\nAnswer:"
    )
    chain = prompt | llm
    print("✅ Chain carregada com sucesso!")
except Exception as e:
    print(f"❌ Erro ao carregar chain: {e}")
    chain = None

@app.get("/")
async def root():
    return {"message": "LangChain Chat API está rodando!", "docs": "/docs"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if chain is None:
        raise HTTPException(status_code=500, detail="Chain não inicializada")
    
    try:
        response = chain.invoke({
            "context": request.context,
            "question": request.question
        })
        
        return ChatResponse(
            response=response.content,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na inferência: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "chain_loaded": chain is not None}
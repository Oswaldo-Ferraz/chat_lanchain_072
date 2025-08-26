import os
from pathlib import Path
import yaml
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv


def load_config_file() -> dict:
    """Carrega config.yaml (placeholders) se existir, sem exigir chaves reais.
    Retorna dict vazio se não existir ou estiver inválido.
    """
    config_path = Path(__file__).resolve().parent.parent / "config" / "config.yaml"
    if not config_path.exists():
        return {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data
    except Exception:
        return {}


def ensure_api_keys(config: dict):
    """Garante que OPENAI_API_KEY esteja disponível via ambiente.
    Ordem: variáveis de ambiente já exportadas > valores do YAML (se não vazios).
    Lança erro se nenhum valor for encontrado.
    """
    if not os.environ.get("OPENAI_API_KEY"):
        yaml_key = config.get("OPENAI_API_KEY") or ""
        if yaml_key:
            os.environ["OPENAI_API_KEY"] = yaml_key
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY não definida. Exporte no ambiente.")


def build_chain():
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="Context: {context}\n\nQuestion: {question}\n\nAnswer:"
    )
    return prompt | llm


def run_example(chain):
    exemplo = {
        "context": "A França é um país na Europa Ocidental, conhecido por sua culinária, arte e monumentos como a Torre Eiffel.",
        "question": "Qual é a capital da França e qual é seu principal monumento?"
    }
    resp = chain.invoke(exemplo)
    print("---Resposta do Modelo---")
    print(resp.content)


def main():
    # Carrega variáveis de um .env local se existir
    load_dotenv()
    config = load_config_file()
    ensure_api_keys(config)
    chain = build_chain()
    run_example(chain)


if __name__ == "__main__":
    main()
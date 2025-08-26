"""
Chatbot RAG Otimizado - Sistema de Suporte Técnico para Britadeiras
Versão: 2.0 - Otimizada com Cache, Async, Modelos Híbridos e Streaming
"""

# Imports
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain.globals import set_llm_cache
from langchain_community.cache import InMemoryCache
import yaml
import os
import asyncio
import time

def setup_sistema():
    """Configurar sistema com cache e modelos otimizados"""
    print("🚀 Iniciando setup do Chatbot RAG Otimizado...")
    
    # Carregar configurações
    with open("../config/config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
    os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]
    
    # Configurar cache para respostas mais rápidas
    set_llm_cache(InMemoryCache())
    
    # Modelos otimizados
    openai_rapido = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)    # Para análises rápidas
    openai_premium = ChatOpenAI(model='gpt-4', temperature=0)          # Para resposta final
    
    print("✅ Setup concluído com sucesso!")
    print("🔥 Cache ativado para respostas mais rápidas!")
    print(f"⚡ Modelo rápido: {openai_rapido.model_name}")
    print(f"🔧 Modelo premium: {openai_premium.model_name}")
    print(f"🌡️ Temperatura: {openai_premium.temperature}")
    print("🚀 Sistema otimizado pronto para uso!")
    
    return openai_rapido, openai_premium

def carregar_documentos():
    """Carregar base de conhecimento"""
    print("\n📚 Carregando base de conhecimento...")
    
    loader = TextLoader('../data/base_conhecimento_britadeira.txt')
    documents = loader.load()
    
    print("✅ Documentos carregados:")
    for doc in documents:
        first_line = doc.page_content.split('\n')[0]
        print(f"- {first_line}")
    
    return documents

def preparar_inputs(documents, pergunta, historico_conversas=""):
    """Preparar e otimizar inputs do sistema"""
    print("\n⚙️ Preparando inputs otimizados...")
    
    # Verificar se todas as variáveis estão presentes
    variaveis_necessarias = {
        'documents': documents is not None and len(documents) > 0,
        'pergunta': pergunta is not None and pergunta.strip() != "",
        'historico_conversas': True  # Opcional
    }
    
    # Verificar quais estão faltando
    faltando = [var for var, presente in variaveis_necessarias.items() if not presente]
    
    if not faltando:
        # Otimizar contexto para melhor performance
        context_completo = "\n".join(doc.page_content for doc in documents)
        context_otimizado = context_completo[:8000] if len(context_completo) > 8000 else context_completo
        
        inputs = {
            "context": context_otimizado,
            "question": pergunta,
            "historico": historico_conversas
        }
        
        print("✅ Inputs preparados com sucesso!")
        if len(context_completo) > 8000:
            print("⚡ Contexto otimizado para melhor performance!")
        
        return inputs
    else:
        print("⚠️ ERRO - Variáveis faltando:")
        for var in faltando:
            print(f"❌ {var} não está presente ou está vazia")
        return None

def criar_prompts():
    """Criar templates de prompts especializados"""
    print("\n🎯 Criando prompts especializados...")
    
    prompt_base_conhecimento = PromptTemplate(
        input_variables=["context", "question"],
        template="""Use o seguinte contexto para responder à pergunta. 
        Responda apenas com base nas informações fornecidas.
        Não forneceça instruções de procedimento já realizados.
        Não utilize informações externas ao contexto:
        Contexto: {context}
        Pergunta: {question}"""
    )
    
    prompt_historico_conversas = PromptTemplate(
        input_variables=["historico", "question"],
        template="""Use o histórico de conversas para responder à pergunta. 
        Responda apenas com base nas informações fornecidas. 
        Não forneceça instruções de procedimento já realizados.
        Não utilize informações externas ao contexto:
        Histórico: {historico}
        Pergunta: {question}"""
    )
    
    prompt_final = PromptTemplate(
        input_variables=["resposta_base_conhecimento", "resposta_historico_conversas"],
        template="""Combine as seguintes respostas para gerar uma resposta final,
        mas não forneça instruções de procedimentos já realizados:
        Resposta da base de conhecimento: {resposta_base_conhecimento}
        Resposta do histórico de conversas: {resposta_historico_conversas}"""
    )
    
    print("✅ Prompts templates criados com sucesso!")
    return prompt_base_conhecimento, prompt_historico_conversas, prompt_final

def criar_chains(prompts, openai_rapido, openai_premium):
    """Criar cadeias otimizadas com modelos híbridos"""
    print("\n🔗 Criando cadeias otimizadas...")
    
    prompt_base_conhecimento, prompt_historico_conversas, prompt_final = prompts
    
    # Cadeias otimizadas com modelos híbridos
    chain_base_conhecimento = prompt_base_conhecimento | openai_rapido      # GPT-3.5 para análise rápida
    chain_historico_conversas = prompt_historico_conversas | openai_rapido  # GPT-3.5 para análise rápida  
    chain_final = prompt_final | openai_premium                             # GPT-4 para resposta final
    
    print("✅ Cadeias otimizadas definidas com sucesso!")
    print("⚡ Análises iniciais: GPT-3.5 Turbo (rápido)")
    print("🎯 Resposta final: GPT-4 (premium)")
    
    return chain_base_conhecimento, chain_historico_conversas, chain_final

async def executar_chains_otimizada(chains, inputs):
    """Executar chains de forma assíncrona com medição de tempo"""
    chain_base_conhecimento, chain_historico_conversas, chain_final = chains
    
    inicio = time.time()
    print("\n⏱️ Iniciando execução das chains otimizadas...")
    
    # Executar as duas primeiras chains em paralelo (GPT-3.5)
    inicio_paralelo = time.time()
    resultado_base, resultado_historico = await asyncio.gather(
        chain_base_conhecimento.ainvoke({"context": inputs["context"], "question": inputs["question"]}),
        chain_historico_conversas.ainvoke({"historico": inputs["historico"], "question": inputs["question"]})
    )
    fim_paralelo = time.time()
    print(f"⚡ Análises paralelas (GPT-3.5) executadas em: {fim_paralelo - inicio_paralelo:.2f}s")
    
    # Executar chain final com GPT-4
    inicio_final = time.time()
    resultado_final = await chain_final.ainvoke({
        "resposta_base_conhecimento": resultado_base, 
        "resposta_historico_conversas": resultado_historico
    })
    fim_final = time.time()
    print(f"🎯 Resposta final (GPT-4) executada em: {fim_final - inicio_final:.2f}s")
    
    fim = time.time()
    print(f"🏁 TEMPO TOTAL OTIMIZADO: {fim - inicio:.2f}s")
    
    return resultado_base, resultado_historico, resultado_final

async def resposta_streaming(chain_final, resultado_base, resultado_historico, pergunta):
    """Gerar resposta com streaming em tempo real"""
    print("\n" + "="*50)
    print("🤖 CHATBOT RAG OTIMIZADO - RESPOSTA EM TEMPO REAL")
    print("=" * 50)
    print(f"❓ Pergunta:\n{pergunta}")
    print("\n" + "=" * 50)
    print("💬 Resposta:")
    
    # Streaming da resposta final em tempo real
    resposta_completa = ""
    inicio_stream = time.time()
    
    async for chunk in chain_final.astream({
        "resposta_base_conhecimento": resultado_base,
        "resposta_historico_conversas": resultado_historico
    }):
        print(chunk.content, end="", flush=True)
        resposta_completa += chunk.content
    
    fim_stream = time.time()
    
    print(f"\n\n" + "=" * 50)
    print(f"⚡ Streaming executado em: {fim_stream - inicio_stream:.2f}s")
    print("✅ Resposta otimizada gerada com base na documentação\ntécnica e histórico de conversas")
    print("🔥 Sistema utilizando: Cache + Async + Modelos Híbridos + Streaming")
    
    return resposta_completa

async def processar_pergunta(pergunta, historico_conversas=""):
    """Função principal para processar uma pergunta"""
    print("="*70)
    print("🤖 CHATBOT RAG OTIMIZADO - INICIANDO PROCESSAMENTO")
    print("="*70)
    
    # 1. Setup do sistema
    openai_rapido, openai_premium = setup_sistema()
    
    # 2. Carregar documentos
    documents = carregar_documentos()
    
    # 3. Preparar inputs
    inputs = preparar_inputs(documents, pergunta, historico_conversas)
    if not inputs:
        return None
    
    # 4. Criar prompts
    prompts = criar_prompts()
    
    # 5. Criar chains
    chains = criar_chains(prompts, openai_rapido, openai_premium)
    
    # 6. Executar processamento
    resultado_base, resultado_historico, resultado_final = await executar_chains_otimizada(chains, inputs)
    
    # 7. Mostrar resultados detalhados (opcional)
    print("\n" + "="*60)
    print("📊 RESULTADOS DAS ANÁLISES:")
    print("="*60)
    print("🔍 Resultado Base de Conhecimento:\n", resultado_base.content)
    print("\n" + "-"*40)
    print("📝 Resultado Histórico de Conversas:\n", resultado_historico.content)
    print("\n" + "-"*40)
    print("🎯 Resultado Final Combinado:\n", resultado_final.content)
    
    # 8. Resposta final com streaming
    resposta_final = await resposta_streaming(chains[2], resultado_base, resultado_historico, pergunta)
    
    return resposta_final

# Função para uso direto
async def main():
    """Executar exemplo de uso"""
    # Dados de exemplo
    historico_conversas = """Cliente: Minha britadeira não liga. Chatbot: Você já verificou 
                             se a bateria está carregada e conectada corretamente?"""
    
    pergunta = "Minha britadeira não liga. Eu já verifiquei e a bateria está carregada e conectada corretamente"
    
    # Processar pergunta
    resposta = await processar_pergunta(pergunta, historico_conversas)
    
    return resposta

# Executar se for chamado diretamente
if __name__ == "__main__":
    # Para executar em ambiente assíncrono
    resposta = asyncio.run(main())

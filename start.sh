#!/bin/bash
# Quick Start - Chatbot RAG - Projeto1

echo "🚀 Iniciando Chatbot RAG - Projeto1..."
echo ""

# Verificar se está na pasta correta
if [ ! -f "requirements.txt" ]; then
    echo "❌ Execute este script da pasta raiz do projeto!"
    exit 1
fi

# Instalar dependências
echo "📦 Instalando dependências..."
pip3 install -r requirements.txt

echo ""
echo "✅ Setup concluído!"
echo ""
echo "📋 Para executar:"
echo "   cd src"
echo "   python3 chatbot_rag.py"
echo ""
echo "📓 Para Jupyter Notebook:"
echo "   cd notebooks" 
echo "   jupyter notebook 01.ipynb"
echo ""

# Verificar se config existe
if [ ! -f "config/config.yaml" ]; then
    echo "⚠️  IMPORTANTE: Configure sua API key em config/config.yaml"
    echo "   Copie o arquivo config.yaml.example e adicione sua chave OpenAI"
fi

echo "🎯 Projeto pronto para uso!"

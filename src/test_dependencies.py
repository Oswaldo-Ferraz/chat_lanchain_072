#!/usr/bin/env python3
"""
Teste de Dependências - Projeto1
Verifica se todas as dependências necessárias estão instaladas
"""

import sys

def test_dependencies():
    """Testar todas as importações necessárias"""
    print("🔍 Testando dependências do Projeto1...")
    print("-" * 50)
    
    # Lista de dependências a testar
    dependencies = [
        ("langchain_openai", "ChatOpenAI"),
        ("langchain.prompts", "PromptTemplate"), 
        ("langchain_community.document_loaders", "TextLoader"),
        ("langchain.globals", "set_llm_cache"),
        ("langchain_community.cache", "InMemoryCache"),
        ("yaml", None),
        ("os", None),
        ("asyncio", None),
        ("time", None)
    ]
    
    failed = []
    success = []
    
    for module, component in dependencies:
        try:
            if component:
                exec(f"from {module} import {component}")
                print(f"✅ {module}.{component}")
                success.append(f"{module}.{component}")
            else:
                exec(f"import {module}")
                print(f"✅ {module}")
                success.append(module)
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed.append(f"{module}: {e}")
        except Exception as e:
            print(f"⚠️  {module}: Erro inesperado - {e}")
            failed.append(f"{module}: {e}")
    
    print("-" * 50)
    print(f"📊 Resultado: {len(success)}/{len(dependencies)} dependências OK")
    
    if failed:
        print("❌ Dependências com problemas:")
        for fail in failed:
            print(f"  - {fail}")
        return False
    else:
        print("🎯 Todas as dependências estão funcionando!")
        return True

def test_config_file():
    """Testar se o arquivo de configuração existe"""
    print("\n🔧 Testando arquivo de configuração...")
    
    import os
    config_path = "../config/config.yaml"
    
    if os.path.exists(config_path):
        print("✅ config.yaml encontrado")
        try:
            import yaml
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
            
            if "OPENAI_API_KEY" in config and config["OPENAI_API_KEY"]:
                print("✅ OPENAI_API_KEY configurada")
                return True
            else:
                print("⚠️  OPENAI_API_KEY não encontrada ou vazia")
                return False
        except Exception as e:
            print(f"❌ Erro ao ler config.yaml: {e}")
            return False
    else:
        print("❌ config.yaml não encontrado")
        return False

def test_data_file():
    """Testar se o arquivo de dados existe"""
    print("\n📄 Testando arquivo de base de conhecimento...")
    
    import os
    data_path = "../data/base_conhecimento_britadeira.txt"
    
    if os.path.exists(data_path):
        print("✅ base_conhecimento_britadeira.txt encontrado")
        try:
            with open(data_path, "r", encoding="utf-8") as f:
                content = f.read()
            if len(content) > 100:
                print(f"✅ Arquivo contém {len(content)} caracteres")
                return True
            else:
                print("⚠️  Arquivo muito pequeno")
                return False
        except Exception as e:
            print(f"❌ Erro ao ler arquivo: {e}")
            return False
    else:
        print("❌ base_conhecimento_britadeira.txt não encontrado")
        return False

if __name__ == "__main__":
    print("🚀 TESTE DE DEPENDÊNCIAS - PROJETO1")
    print("=" * 50)
    
    # Testar dependências
    deps_ok = test_dependencies()
    
    # Testar arquivos
    config_ok = test_config_file()
    data_ok = test_data_file()
    
    print("\n" + "=" * 50)
    print("📋 RESUMO FINAL:")
    print(f"🔗 Dependências: {'✅ OK' if deps_ok else '❌ PROBLEMA'}")
    print(f"⚙️  Configuração: {'✅ OK' if config_ok else '❌ PROBLEMA'}")
    print(f"📄 Base dados: {'✅ OK' if data_ok else '❌ PROBLEMA'}")
    
    if deps_ok and config_ok and data_ok:
        print("\n🎯 PROJETO PRONTO PARA USO!")
        sys.exit(0)
    else:
        print("\n⚠️  HÁ PROBLEMAS A RESOLVER")
        sys.exit(1)

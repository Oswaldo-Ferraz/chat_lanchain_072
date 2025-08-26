import streamlit as st
import os
import yaml
from pypdf import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

# --- CONFIGURAÇÃO DA PÁGINA E CREDENCIAIS ---

st.set_page_config(page_title="Chat com PDF", page_icon="📄")
st.header("Converse com seus documentos PDF 💬")

def setup_openai_api_key():
    """Carrega a chave da API OpenAI do arquivo de configuração."""
    try:
        with open("../config/config.yaml", "r") as config_file:
            config = yaml.safe_load(config_file)
        os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]
        return True
    except FileNotFoundError:
        st.error("Arquivo 'config.yaml' não encontrado. Por favor, configure sua chave da OpenAI.")
        return False
    except KeyError:
        st.error("A chave 'OPENAI_API_KEY' não foi encontrada no 'config.yaml'.")
        return False

# --- FUNÇÕES DE PROCESSAMENTO DE PDF E RAG ---

def get_pdf_text(pdf_docs):
    """Extrai o texto de uma lista de documentos PDF."""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    """Divide o texto em chunks menores."""
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

@st.cache_resource
def get_vectorstore(text_chunks):
    """Cria um vector store a partir dos chunks de texto."""
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    """Cria a cadeia de conversação RAG."""
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

# --- LÓGICA PRINCIPAL DO STREAMLIT ---

def main():
    if not setup_openai_api_key():
        return

    # Inicializar o estado da sessão
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Barra lateral para upload de arquivos
    with st.sidebar:
        st.subheader("Seus documentos")
        pdf_docs = st.file_uploader(
            "Faça o upload dos seus PDFs aqui e clique em 'Processar'", 
            accept_multiple_files=True, 
            type="pdf"
        )
        if st.button("Processar"):
            if pdf_docs:
                with st.spinner("Processando documentos..."):
                    # 1. Extrair texto dos PDFs
                    raw_text = get_pdf_text(pdf_docs)
                    
                    # 2. Dividir texto em chunks
                    text_chunks = get_text_chunks(raw_text)
                    
                    # 3. Criar vector store (base de conhecimento)
                    vectorstore = get_vectorstore(text_chunks)
                    
                    # 4. Criar a cadeia de conversação
                    st.session_state.conversation = get_conversation_chain(vectorstore)
                    st.success("Documentos processados! Pronto para conversar.")
            else:
                st.warning("Por favor, faça o upload de pelo menos um arquivo PDF.")

    # Área de chat principal
    if st.session_state.conversation:
        # Exibir histórico do chat
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                with st.chat_message("user"):
                    st.write(message.content)
            else:
                with st.chat_message("assistant"):
                    st.write(message.content)

        # Input do usuário
        user_question = st.chat_input("Faça uma pergunta sobre seus documentos...")
        if user_question:
            response = st.session_state.conversation({'question': user_question})
            st.session_state.chat_history = response['chat_history']
            # Redesenha a tela para mostrar a nova mensagem instantaneamente
            st.rerun()
    else:
        st.info("Por favor, faça o upload de um PDF e clique em 'Processar' para começar.")

if __name__ == '__main__':
    main()

import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.vectorstores import FAISS
from langchain.document_loaders import WebBaseLoader
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from uuid import uuid4
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv
import os
import numpy as np
import tiktoken
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings



# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Streamlit App Title
st.title("🧠 NomosAI Search Engine + Website RAG + Doc Query")

# Tabs: Search Agent and Website RAG
tab1, tab2, tab3 = st.tabs(["🌍 Search Agent", "📄 Website RAG", "Doc Query"])

# Initialize LLM
llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)

#embedding
embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')



## Sidebar for settings
st.sidebar.title("Settings")

# ---- Tab 1: Search Agent ----
with tab1:
    """
    This tab uses DuckDuckGo, Wikipedia, and Arxiv tools to answer your queries.
    """

   
    ## Arxiv and wikipedia Tools
    arxiv_wrapper=ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)
    arxiv=ArxivQueryRun(api_wrapper=arxiv_wrapper)

    api_wrapper=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=200)
    wiki=WikipediaQueryRun(api_wrapper=api_wrapper)

    search=DuckDuckGoSearchRun(name="Search")

    load_dotenv()
    api_key=os.getenv("GROQ_API_KEY")
    if "messages" not in st.session_state:
        st.session_state["messages"]=[
            {"role":"assisstant","content":"Hi,I'm a chatbot who can search the web. How can I help you?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg['content'])

    if prompt:=st.chat_input(placeholder="What is machine learning?"):
        st.session_state.messages.append({"role":"user","content":prompt})
        st.chat_message("user").write(prompt)

        tools=[search,arxiv,wiki]

        search_agent=initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,handling_parsing_errors=True)

        with st.chat_message("assistant"):
            st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
            response=search_agent.run(st.session_state.messages,callbacks=[st_cb])
            st.session_state.messages.append({'role':'assistant',"content":response})
            st.write(response)



# ---- Tab 2: Website RAG ----
with tab2:
    """
    This tab allows you to ask questions based on the content of a website (RAG).
    """

    url_input = st.text_input("🔗 Enter a website URL", placeholder="https://example.com")

    if "rag_messages" not in st.session_state:
        st.session_state.rag_messages = [
            {"role": "assistant", "content": "Hello! Ask me anything based on the website you provide above."}
        ]

    # Function to load and embed website content
    @st.cache_resource
    def get_website_qa_chain(url):
        loader = WebBaseLoader(url)
        docs = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_documents(docs)

        embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(texts, embeddings)

        retriever = vectorstore.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

        return qa_chain

    if rag_prompt := st.chat_input("Ask based on the website..."):
        st.session_state.rag_messages.append({"role": "user", "content": rag_prompt})
        st.chat_message("user").write(rag_prompt)

        with st.chat_message("assistant"):
            if url_input:
                try:
                    qa_chain = get_website_qa_chain(url_input)
                    response = qa_chain.run(rag_prompt)
                except Exception as e:
                    response = f"⚠️ Error processing website: {e}"
            else:
                response = "⚠️ Please enter a valid website URL."

            st.session_state.rag_messages.append({"role": "assistant", "content": response})
            st.write(response)

# ---- Tab 3: Doc Query ----
with tab3:
    """
    This tab allows you to ask questions based on the content of a PDF.
    """

    # PDF Upload
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file is not None:
        with st.spinner("Reading PDF..."):
            # Save PDF temporarily
            temp_path = os.path.join("temp_files", uploaded_file.name)
            os.makedirs("temp_files", exist_ok=True)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.read())

            # Load and split PDF
            loader = PyPDFLoader(temp_path)
            pages = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            splits = text_splitter.split_documents(pages)

            # Embedding model
            embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"device": "cpu"})

            # Vector store
            vectorstore = Chroma.from_documents(documents=splits, embedding=embedding, persist_directory="./chroma_db")
            retriever = vectorstore.as_retriever()

            # Prompt template
            prompt = hub.pull("rlm/rag-prompt")

            # LLM setup
            llm = ChatGroq(
                api_key=os.getenv("GROQ_API_KEY"),
                model="Llama3-8b-8192",  # or "llama-3-8b-8192" if you need faster inference
                temperature=0.7,
                max_tokens=5000,
            )

            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)

            chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )

            # Question input
            question = st.text_input("Ask a question about the PDF:")
            if question:
                with st.spinner("Getting answer..."):
                    answer = chain.invoke(question)
                    st.markdown(f"**Answer:** {answer}")

                    # Similarity calculation
                    question_vec = embedding.embed_query(question)
                    answer_vec = embedding.embed_query(answer)

                    def cosine_similarity(vec1, vec2):
                        dot_product = np.dot(vec1, vec2)
                        norm_vec1 = np.linalg.norm(vec1)
                        norm_vec2 = np.linalg.norm(vec2)
                        return dot_product / (norm_vec1 * norm_vec2)

                    similarity = cosine_similarity(question_vec, answer_vec)
                    st.markdown(f"**Cosine Similarity between Question and Answer:** `{similarity:.4f}`")


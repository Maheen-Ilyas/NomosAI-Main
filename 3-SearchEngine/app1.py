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


# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Streamlit App Title
st.title("🧠 Search Engine + Website RAG")

# Tabs: Search Agent and Website RAG
tab1, tab2 = st.tabs(["🌍 Search Agent", "📄 Website RAG"])

# Initialize LLM
llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)

# ---- Tab 1: Search Agent ----
with tab1:
    """
    This tab uses DuckDuckGo, Wikipedia, and Arxiv tools to answer your queries.
    """

    # Arxiv and Wikipedia Tools
    arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)
    arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)

    wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
    wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)

    search = DuckDuckGoSearchRun(name="Search")
    tools = [search, arxiv, wiki]

    # Initialize search agent
    search_agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True
    )

    if "search_messages" not in st.session_state:
        st.session_state.search_messages = [
            {"role": "assistant", "content": "Hi! I'm your search assistant. Ask me anything about the web."}
        ]

    for msg in st.session_state.search_messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask the Search Agent..."):
        st.session_state.search_messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            try:
                response = search_agent.run(st.session_state.search_messages, callbacks=[st_cb])
            except Exception as e:
                response = f"⚠️ Agent error: {e}"
            st.session_state.search_messages.append({"role": "assistant", "content": response})
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

    for msg in st.session_state.rag_messages:
        st.chat_message(msg["role"]).write(msg["content"])

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

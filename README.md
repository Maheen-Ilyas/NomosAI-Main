# NomosAI: Legal AI Assistant

NomosAI is an advanced legal AI assistant that leverages Retrieval-Augmented Generation (RAG) technologies to simplify legal research, document analysis, and case file study. It offers a user-friendly platform that integrates AI models specifically fine-tuned for legal tasks.

## 🔍 Overview

NomosAI addresses the complexity of the legal field by providing an intuitive interface for legal professionals, researchers, and students. The system can summarize case files, answer legal queries, and help navigate constitutional provisions through an interactive platform.

## ✨ Key Features

- **Case File Summarization**: Upload legal documents and receive AI-generated summaries
- **Interactive Query System**: Ask specific questions about uploaded documents
- **Constitutional Knowledge Base**: Query provisions, IPC criminal codes, and regulations
- **Website Content Analysis**: Extract and query legal information from websites
- **Legal Q&A**: Get answers to general legal questions related to Indian law

## 🛠️ Technology Stack

### Frontend
- **Next.js**: React framework for building the user interface
- **Tailwind CSS**: Utility-first CSS framework for styling

### Backend
- **FastAPI**: Modern, high-performance web framework for building APIs
- **Python 3.x**: Core programming language

### AI & NLP Components
- **LangChain**: Framework for developing applications powered by language models
- **Hugging Face Transformers**: Library for state-of-the-art NLP models
  - **Sentence Transformer (all-MiniLM-L6-v2)**: For embedding generation
- **Llama 3.3**: Large language model for generating responses
- **Groq**: LLM integration for efficient inference
- **PEFT (Parameter-Efficient Fine-Tuning)**: For efficient model adaptation using LoRA
- **TRL (Transformer Reinforcement Learning)**: Tools for supervised fine-tuning
- **Unsloth**: Optimized versions of Hugging Face models

### Data Processing
- **PyPDFLoader**: For extracting text from PDF documents
- **RecursiveCharacterTextSplitter**: For dividing documents into manageable chunks
- **ChromaDB**: Vector database for storing and retrieving embeddings

### Tools & External Services
- **DuckDuckGo Search**: For web queries
- **Wikipedia API**: For encyclopedic information
- **Arxiv API**: For academic research

### Deployment & Development
- **Docker**: For containerization and deployment
- **Git & GitHub**: For version control
- **Amazon DynamoDB**: For secure data storage (case files and chat history)

## 📝 Modules

- **Q&A Agent**: Conversational interface for legal questions
- **Document Query**: Process and query uploaded documents
- **Search Agent**: Web search capabilities using multiple tools
- **Website RAG**: Query content from specific websites
- **AI Summarizer**: Summarize large legal documents
- **Fine-Tuning**: Adapt models for legal domain tasks

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/nomosai.git
   cd nomosai
   ```

2. Install backend dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Install frontend dependencies
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. Set up environment variables
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. Run the application
   ```bash
   # Start backend
   uvicorn app.main:app --reload
   
   # Start frontend (in a new terminal)
   cd frontend
   npm run dev
   ```

## 📊 Project Status

NomosAI is currently under active development.

## 👥 Contributors

- Rania Mehreen Farooq
- Maheen Ilyas

# Dynamic RAG Chatbot with Knowledge Expansion

## About
The Dynamic RAG Chatbot is a versatile AI assistant capable of automatically expanding its knowledge base. It monitors a local directory for new or updated documents and indexes them in real-time to provide context-aware responses. This ensures the chatbot remains up-to-date with the latest information without manual re-indexing.

## Features
- Real-time knowledge base synchronization for .txt and .pdf files.
- Automated file update detection using MD5 hashing.
- Fully local operation ensuring data privacy.
- Semantic document retrieval for context-aware answers.
- Source tracking to identify which document provided the information.

## Tech Stack
- Frontend: Streamlit
- LLM Orchestration: LangChain
- Vector Database: ChromaDB
- Document Processing: PyPDF, LangChain Text Splitters

## Model Used
- Large Language Model: Llama 3 (via Ollama)
- Embeddings: nomic-embed-text (via Ollama)

## How it Works
The chatbot employs a background engine that tracks files in the `knowledge_base` directory. When a file is added or modified, its content is extracted, split into chunks using a recursive character splitter, and converted into vector embeddings. These embeddings are stored in ChromaDB. During a chat session, the system performs a similarity search against the vector database to retrieve relevant context, which is then used by the Llama 3 model to generate an informed response.

## Project Structure
```text
Dynamic_Chatbot_Knowledge_Expansion/
├── app.py              # Main application logic and UI
├── chroma_db/          # Persistent vector database directory
├── knowledge_base/     # Directory for source documents (.txt, .pdf)
├── file_tracker.json   # Tracking file for MD5 hashes and sync state
└── README.md           # Project documentation
```

## How to Run

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Dynamic_Chatbot_Knowledge_Expansion
```

### 2. Install Dependencies
```bash
pip install streamlit langchain langchain-ollama langchain-chroma langchain-community langchain-core langchain-text-splitters chromadb pypdf
```
Ensure Ollama is installed and models are pulled:
```bash
ollama pull llama3
ollama pull nomic-embed-text
```

### 3. Run the Application
1. Place your documents in the `knowledge_base/` folder.
2. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Examples
- Summarize the contents of the latest uploaded PDF.
- What are the company policies regarding remote work?
- Find information about the pricing details in the text files.

## Author
Jinesh Khalas

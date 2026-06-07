# ArXiv Computer Science Expert Chatbot

## About
The ArXiv Computer Science Expert Chatbot is an AI-powered research assistant designed to help researchers and students navigate complex Computer Science concepts. By utilizing the ArXiv dataset, it provides users with accurate, research-backed answers through a Retrieval-Augmented Generation (RAG) framework.

## Features
- RAG-powered conversational interface for discussing CS theories.
- Advanced paper search engine to locate research by title or abstract.
- Data visualization tools to analyze the distribution of Computer Science sub-domains.
- Automated source attribution providing direct links and IDs for cited research papers.

## Tech Stack
- Frontend: Streamlit
- LLM Orchestration: LangChain
- Vector Database: ChromaDB
- Data Processing: Pandas, JSON

## Model Used
- Large Language Model: Llama 3 (via Ollama)
- Embeddings: HuggingFace sentence-transformers/all-MiniLM-L6-v2

## Dataset
- ArXiv Metadata: A curated subset focusing on Computer Science research papers.

## How it Works
The application first extracts and cleans Computer Science paper metadata from the raw ArXiv JSON dataset. It then generates semantic embeddings for these papers and stores them in a ChromaDB vector database. When a user asks a question, the system retrieves the most relevant paper abstracts and provides them as context to the Llama 3 model, which synthesizes a comprehensive and accurate response.

## Project Structure
```text
Arxiv_Chatbot/
├── app.py                      # Main Streamlit application
├── build_vector_db.py          # Script to generate embeddings and build ChromaDB
├── clean_data.py               # Script to filter for strict CS categories
├── data_prep.py                # Extracts CS papers from raw ArXiv JSON
├── discover_domains.py         # Utility to analyze ArXiv domain distributions
├── all_cs_papers_strict.csv    # Processed dataset used by the application
├── chroma_db/                  # Persistent vector store
└── arxiv-metadata-oai-snapshot.json # Raw ArXiv metadata source
```

## How to Run

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Arxiv_Chatbot
```

### 2. Install Dependencies
```bash
pip install streamlit pandas langchain langchain-community chromadb sentence-transformers
```
Ensure Ollama is installed and the Llama 3 model is available:
```bash
ollama pull llama3
```

### 3. Run the Application
1. Prepare the data and build the vector database:
   ```bash
   python data_prep.py
   python clean_data.py
   python build_vector_db.py
   ```
2. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Examples
- What are the latest trends in Transformer architectures?
- Explain the concept of Zero-Shot learning in Computer Vision.
- How does reinforcement learning apply to autonomous systems?

## Author
Jinesh Khalas

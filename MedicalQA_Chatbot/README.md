# Agentic Medical Assistant Chatbot

## About
The Agentic Medical Assistant is an intelligent healthcare chatbot designed to provide accurate medical information. It combines semantic search over a curated local dataset with specialized Medical Named Entity Recognition (NER) and a live web search fallback. This ensures that users receive verified information from local data or the most recent updates from the web.

## Features
- Semantic Search using Sentence-Transformers for high-relevance retrieval.
- Specialized Medical NER to identify and extract clinical entities.
- Domain Guardrails to ensure queries remain focused on medical topics.
- Live Web Synthesis via DuckDuckGo for real-time information fallback.
- Dual interface support for both Streamlit Web UI and Terminal mode.

## Tech Stack
- Frontend: Streamlit
- LLM Engine: Ollama
- NLP & NER: SciSpaCy, spaCy, Sentence-Transformers
- Search API: DuckDuckGo Search
- Data Processing: Pandas

## Model Used
- Large Language Model: Llama 3 (via Ollama)
- Medical NER Model: SciSpaCy (en_core_sci_sm)
- Embeddings: sentence-transformers/all-MiniLM-L6-v2

## Dataset
- MedQA Dataset: A curated collection of medical questions and answers, processed into `MedQA_Clean_Dataset.csv`.

## How it Works
When a user submits a query, the assistant first performs domain classification to ensure the request is medical. It then uses SciSpaCy to extract medical entities and performs a semantic search against the local medical dataset. If a high-confidence match is found (similarity score > 0.65), it synthesizes an answer using the retrieved context. If no high-confidence local match is found, the system triggers a web search to provide a live synthesis of the information.

## Project Structure
```text
MedicalQA_Chatbot/
├── app.py                  # Streamlit Web Application
├── main.py                 # Core AI logic and Terminal Interface
├── data_prep.py            # Data cleaning and preprocessing script
├── MedQA_Dataset.csv       # Raw medical dataset
├── MedQA_Clean_Dataset.csv # Processed and cleaned medical dataset
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## How to Run

### 1. Clone the Repository
```bash
git clone <repository-url>
cd MedicalQA_Chatbot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
Download the specialized SciSpaCy model:
```bash
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_core_sci_sm-0.5.4.tar.gz
```
Ensure Ollama is running and Llama 3 is pulled:
```bash
ollama pull llama3
```

### 3. Run the Application
1. (Optional) Clean the raw dataset:
   ```bash
   python data_prep.py
   ```
2. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. Or run in Terminal mode:
   ```bash
   python main.py
   ```

## Examples
- What are the symptoms of Type 2 Diabetes?
- Explain the side effects of Lisinopril.
- What is the recommended treatment for a common cold?

## Author
Jinesh Khalas

---
*Disclaimer: This is an AI assistant for informational purposes only and does not replace professional medical advice.*

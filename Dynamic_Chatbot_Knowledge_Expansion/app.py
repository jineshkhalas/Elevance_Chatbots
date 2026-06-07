import os
import streamlit as st
import json
import hashlib
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

MODEL_NAME = "llama3"
EMBED_MODEL_NAME = "nomic-embed-text" 
DB_DIR = "chroma_db"
DATA_DIR = "knowledge_base"
TRACKING_FILE = "file_tracker.json"

st.title("LLAMA3 Dynamic RAG ChatBot")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant", 
            "content": "Hello! Drop any .txt or .pdf files into the knowledge base and I will dynamically sync and answer from them instantly!"
        }
    ]

@st.cache_resource
def get_models():
    ollama = OllamaLLM(model=MODEL_NAME)
    embeddings = OllamaEmbeddings(model=EMBED_MODEL_NAME) 
    return ollama, embeddings

ollama, embeddings = get_models()

def load_tracker():
    if os.path.exists(TRACKING_FILE):
        with open(TRACKING_FILE, "r") as f:
            return json.load(f)
    return {}

def save_tracker(tracker):
    with open(TRACKING_FILE, "w") as f:
        json.dump(tracker, f, indent=4)

def auto_sync_knowledge_base():
    if not os.path.exists(DATA_DIR):
        return

    current_files = [f for f in os.listdir(DATA_DIR) if f.endswith(('.txt', '.pdf'))]
    if not current_files:
        return
        
    vector_store = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    tracker = load_tracker()
    processed_paths = []
    has_changes = False

    for file_name in current_files:
        file_path = os.path.join(DATA_DIR, file_name)
        processed_paths.append(file_path)
        
        try:
            with open(file_path, "rb") as f:
                file_bytes = f.read()
            current_file_hash = hashlib.md5(file_bytes).hexdigest()
            last_known_hash = tracker.get(file_path)

            if last_known_hash is None or current_file_hash != last_known_hash:
                docs = []
                
                if file_name.endswith('.txt'):
                    loader = TextLoader(file_path, encoding='utf-8')
                    loaded_docs = loader.load()
                    for d in loaded_docs:
                        d.metadata["source"] = file_name
                    docs.extend(loaded_docs)
                elif file_name.endswith('.pdf'):
                    loader = PyPDFLoader(file_path)
                    loaded_docs = loader.load()
                    for d in loaded_docs:
                        d.metadata["source"] = file_name
                    docs.extend(loaded_docs)
                
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
                chunks = text_splitter.split_documents(docs)
                
                chunk_ids = []
                for chunk in chunks:
                    chunk_content = f"{file_name}_{chunk.page_content}"
                    chunk_id = hashlib.md5(chunk_content.encode('utf-8')).hexdigest()
                    chunk_ids.append(chunk_id)
                
                vector_store.add_documents(chunks, ids=chunk_ids)
                tracker[file_path] = current_file_hash
                has_changes = True
                print(f"🔄 Hard Drive Sync: Successfully indexed/updated {file_name}")
                
        except Exception as e:
            st.error(f"Error indexing file {file_name}: {e}")

    for tracked_path in list(tracker.keys()):
        if tracked_path not in processed_paths:
            try:
                vector_store.delete_collection()
                tracker = {}
                has_changes = True
                print("🗑️ Source file missing. Cleared collection for full reset.")
                break
            except Exception:
                pass

    if has_changes:
        save_tracker(tracker)

for msg in st.session_state.messages:
    st.chat_message(
        msg["role"], avatar="🧑‍💻" if msg["role"] == "user" else "🤖"
    ).write(msg["content"])

def generate_response():
    messages = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in st.session_state.messages    
    ]
    prompt = messages[-1]["content"]
    context = ""
    
    auto_sync_knowledge_base()
    
    try:
        live_vector_store = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
        results = live_vector_store.similarity_search_with_score(prompt, k=5)
        
        if results:
            best_score = results[0][1]
            print(f"🔍 Top Match Distance Score for '{prompt}': {best_score}")
            
            if best_score < 1.45:
                context_parts = []
                for doc, score in results:
                    source_file = os.path.basename(doc.metadata.get("source", "Unknown Document"))
                    context_parts.append(f"--- START OF BLOCK FROM FILE: {source_file} ---\n{doc.page_content}\n--- END OF BLOCK FROM FILE: {source_file} ---")
                
                context = "\n\n".join(context_parts)
    except Exception as e:
        pass

    if context:
        augmented_prompt = f"""You are an advanced data extraction assistant with access to local reference files and general knowledge.

        THE FOLLOWING CONTEXT BLOCKS ARE EXTRACTED FROM UNIQUE FILES IN THE KNOWLEDGE BASE:
        {context}

        INSTRUCTIONS:
        1. Review the user's question and determine who or what entity they are asking about.
        2. Read the text blocks above carefully. Match the entity in the question to the text contents and the specific 'START OF BLOCK FROM FILE' labels.
        3. Keep information from different files completely distinct. Do not blend or cross-mix details between separate source files.
        4. Always explicitly state which [Source File] your facts came from in your final answer.
        5. If the question is a general conversation, greeting, math, or coding task, ignore the local files entirely and answer using your own knowledge.

        Question: {prompt}
        Answer:"""
    else:
        augmented_prompt = f"""You are a helpful AI assistant. Respond politely to the user's input.
        
        User: {prompt}
        Assistant:"""

    response = ollama.stream(augmented_prompt)
    full_response = ""
    for token in response:
        full_response += token
        yield token
    
    st.session_state["full_message"] = full_response

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="🧑‍💻").write(prompt)
    
    with st.chat_message("assistant", avatar="🤖"):
        response = st.write_stream(generate_response())

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": st.session_state["full_message"]
        }
    )
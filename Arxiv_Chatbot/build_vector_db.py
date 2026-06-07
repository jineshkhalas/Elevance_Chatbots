import pandas as pd
import os
from langchain_community.vectorstores  import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def build_chroma_db(input_csv, db_directory, sample_size = 10000):
    print(f"--- Starting Vector Database Build ---")

    if not os.path.exists(input_csv):
        print(f"Error: {input_csv} not found! Check your filename.")
        return
    
    print(f"Loading data from {input_csv}...")
    df = pd.read_csv(input_csv, low_memory=False)

    print(f"Total available CS papers: {len(df):,}")
    if len(df) > sample_size:
        print(f"Sampling the first {sample_size:,} papers for the vector database...")
        df = df.head(sample_size)

    print("Converting data into document formats...")
    documents = []

    for _, row in df.iterrows():
        abstract = str(row['abstract']) if pd.notna(row['abstract']) else ""
        title = str(row['title']) if pd.notna(row['title']) else "Untitled"
        paper_id = str(row['id']) if pd.notna(row['id']) else "Unknown ID"

        full_text = f"Title: {title}\nAbstract: {abstract}"

        doc = Document(
            page_content = full_text,
            metadata = {"id": paper_id, "title": title}
        )
        documents.append(doc)

    print("Splitting documents into smaller text chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 600,
        chunk_overlap = 100
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks):,} text chunks from {len(df):,} papers.")

    print("Loading HuggingFace Embedding Model ('all-MiniLM-L6-v2')...")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print(f"Generating embeddings and saving to '{db_directory}'...")
    print("Note: This might take 5-10 minutes depending on your CPU. Please wait...")

    vector_db = Chroma.from_documents(
        documents = chunks,
        embedding = embeddings,
        persist_directory = db_directory
    )

    vector_db.persist()
    print(f"\n--- SUCCESS ---")
    print(f"Vector Database successfully created and saved in: {db_directory}")

if __name__ == "__main__":
    # Ensure these names match your workspace files exactly
    INPUT_FILE = 'all_cs_papers_strict.csv'
    OUTPUT_DB_DIR = './chroma_db'
    
    # Feel free to adjust this. 5,000 to 10,000 is great for testing your UI/LLM setup!
    SAMPLE_SIZE = 10000 
    
    build_chroma_db(INPUT_FILE, OUTPUT_DB_DIR, sample_size=SAMPLE_SIZE)
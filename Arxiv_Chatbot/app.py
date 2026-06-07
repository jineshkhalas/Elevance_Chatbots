import streamlit as st
import os
import pandas as pd
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import Ollama

st.set_page_config(page_title = "ArXiv CS Expert Bot", page_icon = "🤖", layout = "wide")
st.title("🤖 ArXiv Computer Science Expert Chatbot")
st.markdown("---")

@st.cache_resource
def load_rag_system():
   db_directory = "./chroma_db"

   embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")
   vector_db = Chroma(persist_directory = db_directory, embedding_function = embeddings)

   llm = Ollama(model = "llama3")

   memory = ConversationBufferMemory(memory_key = "chat_history", return_messages = True, output_key = 'answer')

   qa_chain = ConversationalRetrievalChain.from_llm(
      llm = llm,
      retriever = vector_db.as_retriever(search_kwargs = {"k": 3}),
      memory = memory,
      return_source_documents = True
   )

   return qa_chain


try:
   qa_chain = load_rag_system()
   system_ready = True
except Exception as e:
   st.warning("⚠️ Chat feature failed to initialize. Please ensure Ollama is running in the background.")
   system_ready = False

@st.cache_data
def load_raw_metadata():
   if os.path.exists('all_cs_papers_strict.csv'):
      return pd.read_csv('all_cs_papers_strict.csv', nrows = 10000, low_memory = False)
   return None

df_meta = load_raw_metadata()


st.sidebar.header("🛠️ Features & Controls")
app_mode = st.sidebar.radio("Navigate to: ", ["Chatbot", "Paper Search Engine", "Concept Visualization"])

if app_mode == "Chatbot":
    st.header("Discuss Advance Computer Science Concepts")
    st.caption("Ask comple questions, get text summaries, or request breakdowns of research theories.")

    if not system_ready:
        fallback_msg = "The system is running in standalone local metadata mode. Please start your Ollama app to enable chat."
        st.info(fallback_msg)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
       with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What would you like to investigate today?"):
       with st.chat_message("user"):
            st.markdown(prompt)
       st.session_state.messages.append({"role": "user", "content": prompt})

       with st.chat_message("assistant"):
          if system_ready:
             with st.spinner("Analyzing papers and synthesizing response"):
                try:
                    response = qa_chain({"question": prompt})
                    answer = response["answer"]
                    sources = response.get("source_documents", [])
                    
                    st.markdown(answer)

                    if sources:
                        with st.expander("📚 View Cited Research Sources"):
                            for idx, doc in enumerate(sources):
                                title = doc.metadata.get('title', 'Unknown Title')
                                paper_id = doc.metadata.get('id', 'N/A')
                                st.write(f"**{idx+1}. {title}** (ArXiv ID: {paper_id})")
                                st.caption(doc.page_content)
                                
                    st.session_state.messages.append({"role": "assistant", "content": answer})

                except Exception as e:
                    answer = f"Error communicating with local LLM. Make sure the Ollama app is open and running! Details: {str(e)}"
                    st.error(answer)
          else:
             error_msg = "Cannot process question. Please start your local Ollama engine to enable chat."
             st.error(error_msg)

elif app_mode == "Paper Search Engine":
    st.subheader("Local Metadata Paper Search")

    if df_meta is not None:
        search_query = st.text_input("Type keyword to search titles or abstracts (e.g., 'Neural', 'Quantum', 'Optimization'):") 

        if search_query:
            results = df_meta[
                df_meta['title'].str.contains(search_query, case = False, na = False) |
                df_meta['abstract'].str.contains(search_query, case = False, na = False)
            ]

            st.write(f"Found {len(results)} matching entries in local metadata slice.")

            for idx, row in results.head(10).iterrows():
                with st.container():
                    st.markdown(f"### 📄 {row['title']}")
                    st.caption(f"**Categories:** {row['categories']} | **ArXiv ID:** {row['id']}")
                    st.write(row['abstract'])
                    st.markdown('---')

    else:
        st.error("Could not locate 'all_cs_papers_strict.csv'. Please ensure your dataset matches the setup.")

elif app_mode == "Concept Visualization":
    st.subheader("Domain Concept Visualizations")
    st.write("Distribution of specific computer science tags across your extracted records.")

    if df_meta is not None:
        all_tags = []
        for tags_str in df_meta['categories'].dropna():
            all_tags.extend([t for t in tags_str.split() if 'cs.' in t])
        
        tag_counts = pd.Series(all_tags).value_counts().head(15)

        chart_data = pd.DataFrame({
            'Sub-Domain Tag': tag_counts.index,
            'Paper Count': tag_counts.values
        }).set_index('Sub-Domain Tag')

        st.bar_chart(chart_data)

        st.write("### Sub-Domain Breakdown Guide:")
        st.markdown("""
        * **cs.CV:** Computer Vision & Pattern Recognition
        * **cs.LG / stat.ML:** Machine Learning
        * **cs.AI:** Artificial Intelligence
        * **cs.CL:** Computation and Language (NLP)
        """)
    else:
         st.error("Metadata is unavailable for charting visualization profiles.")
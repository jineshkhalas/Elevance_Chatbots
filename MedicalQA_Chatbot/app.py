import streamlit as st
from main import setup_chatbot_brain, ask_question

st.set_page_config(page_title="Medical AI Assistant", page_icon="⚕️", layout="centered")
st.title("⚕️ Agentic Medical Assistant")
st.caption("A smart healthcare assistant powered by Semantic Search and live web synthesis.")

@st.cache_resource
def load_engine():
    return setup_chatbot_brain('MedQA_Clean_Dataset.csv')

df, model, database_embeddings, ner_model = load_engine()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a medical question (e.g., What are the symptoms of asthma?)"):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Analyzing medical data..."):
            ans, source, score, terms = ask_question(prompt, df, model, database_embeddings, ner_model)
            st.markdown(ans)

            with st.expander("🔍 Behind the scenes (AI Logic)"):
                st.write(f"**Confidence Score:** {score:.4f}")
                st.write(f"**Source Used:** {source}")
                if terms:
                    st.write(f"**Extracted Entities:** {', '.join(terms)}")
                else:
                    st.write("**Extracted Entities:** None")
    
    st.session_state.messages.append({"role": "assistant", "content": ans})
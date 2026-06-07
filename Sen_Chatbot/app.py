import streamlit as st
from main import analyze_sentiment, get_system_prompt, generate_llm_response

st.set_page_config(page_title = "Sentiment AI Assistant", page_icon = "🤖", layout = "wide")

st.title("🤖 Sentiment-Aware Customer Support Chatbot")
st.write("This chatbot detects user emotion dynamically and adjusts its response strategy.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "latest_sentiment" not in st.session_state:
    st.session_state.latest_sentiment = {"label": "None", "icon": "⚪", "score": 0.0}


with st.sidebar:
    st.header("📊 Real-time Sentiment Analytics")
    st.write("Use this panel to evaluate your task criteria.")
    st.markdown("---")
    st.metric(label="Detected Sentiment", value=st.session_state.latest_sentiment["label"])
    st.metric(label="Polarity Score", value=f"{st.session_state.latest_sentiment['score']:.2f}")
    st.write(f"Current Tone Modifier Hook: `{st.session_state.latest_sentiment['icon']}`")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_input := st.chat_input("How can I help you today?"):
    with st.chat_message("user"):
        st.write(user_input)

    label, icon, score = analyze_sentiment(user_input)
    st.session_state.latest_sentiment = {"label": label, "icon": icon, "score": score}

    system_instruction = get_system_prompt(label)
    ollama_messages = [{"role": "system", "content": system_instruction}]

    for msg in st.session_state.messages:
        ollama_messages.append({"role": msg["role"], "content": msg["content"]})

    ollama_messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Analyzing context and generating response..."):
            try:
                reply_text = generate_llm_response(ollama_messages, model_name = "llama3")
                st.write(reply_text)
                st.session_state.messages.append({"role": "assistant", "content": reply_text})
            except Exception as e:
                st.error(f"Ollama Connection Error: {e}. Make sure Ollama desktop app is running!")

    st.rerun()
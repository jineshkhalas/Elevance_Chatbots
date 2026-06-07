import streamlit as st
from main import analyze_sentiment, detect_language, get_multilingual_prompt, generate_llm_response

st.set_page_config(page_title="Multilingual Sentiment Assistant", page_icon="🤖", layout="wide")

st.title("🤖 Multilingual Sentiment-Aware Chatbot")
st.write("This chatbot detects user language and emotional states automatically to provide culturally appropriate responses.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "metrics" not in st.session_state:
    st.session_state.metrics = {
        "sentiment": "None",
        "score": 0.0,
        "lang_code": "en"
    }

flag_mapping = {
    'en': 'English 🇺🇸',
    'gu': 'Gujarati 🇮🇳',
    'hi': 'Hindi 🇮🇳',
    'es': 'Spanish 🇪🇸'
}

with st.sidebar:
    st.header("📊 Multi-Turn NLP Analytics")
    st.write("Evaluates active language routing and sentiment states dynamically.")
    st.markdown("---")
    st.metric(label="Detected Language", value=flag_mapping.get(st.session_state.metrics["lang_code"], "English 🇺🇸"))
    st.metric(label="Sentiment Class", value=st.session_state.metrics["sentiment"])
    st.metric(label="Polarity Index", value=f"{st.session_state.metrics['score']:.2f}")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_input := st.chat_input("Type in English, ગુજરાતી, हिंदी, or Español..."):
    
    with st.chat_message("user"):
        st.write(user_input)
        
    sentiment_label, icon, score = analyze_sentiment(user_input)
    detected_lang = detect_language(user_input)
    
    st.session_state.metrics = {
        "sentiment": f"{icon} {sentiment_label}",
        "score": score,
        "lang_code": detected_lang
    }
    
    system_instruction = get_multilingual_prompt(sentiment_label, detected_lang)
    ollama_messages = [{"role": "system", "content": system_instruction}]
    
    for msg in st.session_state.messages:
        ollama_messages.append({"role": msg["role"], "content": msg["content"]})
        
    ollama_messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
        with st.spinner("Processing multilingual prompt logic..."):
            try:
                reply_text = generate_llm_response(ollama_messages, model_name='gemma2') 
                st.write(reply_text)
                st.session_state.messages.append({"role": "assistant", "content": reply_text})
                
            except Exception as e:
                st.error(f"Ollama Connection Error: {e}. Check if your background app is active and the model name is correct.")
    
    st.rerun()
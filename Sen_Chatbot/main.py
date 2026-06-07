import ollama
from textblob import TextBlob

def analyze_sentiment(text):
    analysis = TextBlob(text)
    score = analysis.sentiment.polarity

    if score > 0.15:
        return "Positive / Satisfied", "🟢", score
    elif score < -0.15:
        return "Negative / Frustrated", "🔴", score
    else:
        return "Neutral / Informational", "🟡", score
    

def get_system_prompt(sentiment_label):
    base = (
        "You are a professional customer support AI assistant. "
        "You can solve math problems, write summaries, write code, and provide factual answers.\n\n"
    )

    if sentiment_label == "Negative / Frustrated":
        base += (
            "CRITICAL DIRECTION:\n"
            "- The customer is unhappy, angry, sad, or frustrated.\n"
            "- You MUST be deeply empathetic, polite, patient, and apologetic.\n"
            "- Validate their feelings immediately (e.g., 'I completely understand your frustration').\n"
            "- Prioritize finding a clear, direct solution to their problem."
        )

    elif sentiment_label == "Positive / Satisfied":
        base += (
            "CRITICAL DIRECTION:\n"
            "- The customer is happy or giving praise.\n"
            "- Match their positive energy! Be enthusiastic, warm, and expressive.\n"
            "- Thank them sincerely for their positive feedback."
        )

    else:
        base += (
            "CRITICAL DIRECTION:\n"
            "- The user is neutral or asking an analytical question.\n"
            "- Provide clear, concise, objective, and highly accurate information.\n"
            "- Keep the tone helpful, professional, and efficient."
        )

    return base

def generate_llm_response(ollama_messages, model_name='llama3'):
    response = ollama.chat(model = model_name, messages = ollama_messages)
    return response['message']['content']

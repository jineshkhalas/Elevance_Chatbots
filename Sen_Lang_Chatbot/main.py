import ollama
from textblob import TextBlob
from langdetect import detect

def analyze_sentiment(text):
    analysis = TextBlob(text)
    score = analysis.sentiment.polarity

    if score > 0.15:
        return "Positive / Satisfied", "🟢", score
    elif score < -0.15:
        return "Negative / Frustrated", "🔴", score
    else:
        return "Neutral / Informational", "🟡", score
    
def detect_language(text):
    try:
        lang_code = detect(text)
        supported_langs = ['en', 'gu', 'hi', 'es']
        if lang_code in supported_langs:
            if lang_code in ['mr', 'ne']:
                return 'hi'
            return lang_code
        return 'en'
    except:
        return 'en'

def get_multilingual_prompt(sentiment_label, lang_code):
    lang_map = {
        'en' : ('English', 'Professional and clear customer support tone.'),
        'gu' : ('Gujarati', 'Respectful Gujarati etiquette. Use greetings like "જય શ્રી કૃષ્ણ" and ensure the response is in Gujarati script.'),
        'hi' : ('Hindi', 'Polite Hindi vocabulary. Use "नमस्कार" and respectful "आप" grammar. Ensure the response is in Devanagari script.'),
        'es' : ('Spanish', 'Warm, polite Spanish using formal "usted".')
    }

    lang_name, cultural_rule = lang_map.get(lang_code, lang_map['en'])

    base_prompt = (
        f"You are a highly capable multilingual assistant. The current conversation is in {lang_name}.\n"
        f"CORE INSTRUCTION: Respond to the user's request accurately and helpfully in {lang_name}.\n"
        f"LANGUAGE CONSTRAINT: Your response must be entirely in {lang_name}. Do not use English, Hindi (unless it is the target language), or other languages, except for technical terms, programming code, or proper nouns where no good {lang_name} equivalent exists.\n"
        f"TECHNICAL CONTENT: If the user asks for programming code, provide it in its standard format (e.g., C++ code in English), but provide all surrounding explanations in {lang_name}.\n"
        f"CULTURAL GUIDELINE: {cultural_rule}\n\n"
    )

    if sentiment_label == "Negative / Frustrated":
        base_prompt += (
            "EMOTION HANDLING:\n"
            "- The user seems frustrated. Be empathetic and apologetic.\n"
            "- Focus on providing a direct solution to their problem."
        )
    elif sentiment_label == "Positive / Satisfied":
        base_prompt += (
            "EMOTION HANDLING:\n"
            "- The user is happy. Match their energy and express gratitude."
        )
    else:
        base_prompt += (
            "EMOTION HANDLING:\n"
            "- Maintain a professional and objective tone."
        )
    
    return base_prompt

def generate_llm_response(ollama_messages, model_name='gemma2'):
    response = ollama.chat(model=model_name, messages=ollama_messages)
    return response['message']['content']

# Sentiment-Aware Customer Support Chatbot

## About
The Sentiment-Aware Customer Support Chatbot is an intelligent assistant designed to enhance user experience by detecting emotional states in real-time. By analyzing the sentiment of user messages, the chatbot dynamically adjusts its persona and communication style to provide more empathetic and contextually appropriate support.

## Features
- Real-time Sentiment Detection: Analyzes user input to determine polarity (Positive, Negative, or Neutral).
- Dynamic Persona Adjustment: Modifies the system prompt on-the-fly to match the user's emotional tone.
- Empathetic Responses: Automatically switches to a patient and apologetic tone for frustrated users.
- Live Analytics Sidebar: Displays real-time sentiment labels and polarity scores for every interaction.
- Local LLM Integration: Uses Ollama for secure and private local inference.

## Tech Stack
- Frontend: Streamlit
- Sentiment Analysis: TextBlob
- LLM Engine: Ollama
- Language: Python

## Model Used
- Large Language Model: Llama 3 (via Ollama)
- Sentiment Model: TextBlob (PatternAnalyzer)

## How it Works
As a user types a message, the application uses TextBlob to calculate a sentiment polarity score. This score is categorized into Frustrated, Neutral, or Satisfied. Based on this category, the system selects a specialized "System Persona" (e.g., an empathetic support agent for negative sentiment) and injects it into the prompt sent to the Llama 3 model. This ensures the model's response is perfectly aligned with the user's current mood.

## Project Structure
```text
Sen_Chatbot/
├── app.py              # Streamlit frontend and UI logic
├── main.py             # Core logic for sentiment analysis and LLM integration
└── README.md           # Project documentation
```

## How to Run

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Sen_Chatbot
```

### 2. Install Dependencies
```bash
pip install streamlit ollama textblob
```
Download the necessary TextBlob corpora:
```bash
python -m textblob.download_corpora
```
Ensure Ollama is running and Llama 3 is pulled:
```bash
ollama pull llama3
```

### 3. Run the Application
Start the Streamlit server:
```bash
streamlit run app.py
```

## Examples
- I am very unhappy with the recent service delay. (Triggers empathetic persona)
- Can you tell me the store hours for the weekend? (Triggers professional neutral persona)
- I love the new features you just added! (Triggers enthusiastic persona)

## Author
Jinesh Khalas

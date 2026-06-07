# Advanced Multimodal Gemini Chatbot

## About
The Advanced Multimodal Gemini Chatbot is a sophisticated AI application that combines state-of-the-art vision and language models with creative image generation. It allows users to engage in natural language conversations, analyze visual content from uploaded images, and generate high-quality AI images through simple text prompts.

## Features
- Multimodal Chat: Seamless natural language interaction using Google Gemini.
- Image Analysis: Upload photos to ask questions about their visual context and details.
- AI Image Generation: Create custom images on-the-fly using Pollinations AI integration.
- Dynamic Prompt Optimization: Automatically refines user prompts for superior image generation results.
- Persistent Session History: Keeps track of the conversation flow within the current user session.

## Tech Stack
- Frontend: Streamlit
- API Integration: Google Gemini API, Pollinations AI API
- Image Processing: Pillow (PIL)
- Networking: Requests

## Model Used
- Multimodal Model: Google Gemini 2.5 Flash
- Image Generation: Pollinations AI

## How it Works
The chatbot uses the Google Gemini API to process both text and image inputs. When a user uploads an image, the model analyzes the pixels alongside the text prompt to provide context-aware answers. For image generation, the system detects "generate" or "draw" keywords, optimizes the user's description into a high-quality condensed prompt using Gemini, and fetches the resulting image from the Pollinations AI API.

## Project Structure
```text
Multimodel_Chatbot/
├── app.py              # Main application logic and Streamlit UI
├── .env                # Environment variables (API Keys)
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## How to Run

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Multimodel_Chatbot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
Create a `.env` file in the root directory and add your Google Gemini API Key:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

### 4. Run the Application
Start the Streamlit server:
```bash
streamlit run app.py
```

## Examples
- What is happening in this uploaded image?
- Generate a futuristic city with neon lights and flying cars.
- Explain the concept of quantum entanglement in simple terms.

## Author
Jinesh Khalas

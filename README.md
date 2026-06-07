# ElevanceSkills Data Science Internship Projects

Data Science portfolio. This repository contains a collection of advanced AI applications, ranging from RAG-based research assistants and medical agents to multimodal chatbots and sentiment-aware customer support systems.

## Projects Overview

| Project | Key Technologies | Core Functionality |
| :--- | :--- | :--- |
| **[ArXiv Chatbot](./Arxiv_Chatbot)** | Llama 3, ChromaDB, RAG | CS Research assistant with paper search and visualization. |
| **[Dynamic Knowledge RAG](./Dynamic_Chatbot_Knowledge_Expansion)** | Llama 3, ChromaDB, Live Sync | Chatbot that auto-indexes new local documents (.pdf, .txt). |
| **[Agentic Medical Assistant](./MedicalQA_Chatbot)** | Llama 3, SciSpaCy, Web Search | Medical QA with domain guardrails and live web fallback. |
| **[Multimodal Gemini Bot](./Multimodel_Chatbot)** | Gemini 1.5 Flash, Pollinations AI | Text/Image analysis and AI image generation. |
| **[Sentiment Support Bot](./Sen_Chatbot)** | Llama 3, TextBlob | Sentiment-aware assistant that adjusts its persona based on user mood. |
| **[Multilingual Sentiment Bot](./Sen_Lang_Chatbot)** | Gemma 2, langdetect, TextBlob | Culturally-aware bot supporting multiple languages and greetings. |

---

## Detailed Project Breakdown

### 1. [ArXiv Computer Science Expert Chatbot](./Arxiv_Chatbot)
An AI-powered research assistant designed to help navigate complex Computer Science concepts using the ArXiv dataset.
- **Features:** RAG-powered conversation, paper search by title/abstract, and data visualization of CS sub-domains.
- **Stack:** Streamlit, LangChain, ChromaDB, Llama 3.

### 2. [Dynamic RAG with Knowledge Expansion](./Dynamic_Chatbot_Knowledge_Expansion)
A versatile AI assistant that automatically expands its knowledge base by monitoring a local directory.
- **Features:** Real-time synchronization of .txt and .pdf files, MD5 hashing for change detection, and source tracking.
- **Stack:** Streamlit, LangChain, ChromaDB, Llama 3.

### 3. [Agentic Medical Assistant Chatbot](./MedicalQA_Chatbot)
An intelligent healthcare chatbot providing verified medical information from local datasets and web fallback.
- **Features:** Medical Named Entity Recognition (NER), domain guardrails, and live web synthesis via DuckDuckGo.
- **Stack:** SciSpaCy, Sentence-Transformers, Ollama (Llama 3), Streamlit.

### 4. [Advanced Multimodal Gemini Chatbot](./Multimodel_Chatbot)
A sophisticated application combining vision, language, and creative image generation.
- **Features:** Image analysis, AI image generation, and dynamic prompt optimization.
- **Stack:** Google Gemini 1.5 Flash, Pollinations AI, Streamlit.

### 5. [Sentiment-Aware Customer Support Chatbot](./Sen_Chatbot)
An empathetic assistant that detects emotional states to enhance user experience.
- **Features:** Real-time sentiment detection (Positive/Negative/Neutral) and dynamic persona adjustment.
- **Stack:** TextBlob, Ollama (Llama 3), Streamlit.

### 6. [Multilingual Sentiment-Aware Chatbot](./Sen_Lang_Chatbot)
A culturally-conscious assistant capable of interacting in multiple languages with emotional intelligence.
- **Features:** Automatic language detection (English, Hindi, Gujarati, Spanish), and culturally-tailored greetings.
- **Stack:** langdetect, TextBlob, Ollama (Gemma 2), Streamlit.

---

## Global Requirements
Most projects in this repository require **Ollama** for local LLM inference.
- **Models used:** `llama3`, `gemma2`, `nomic-embed-text`.
- **UI:** All projects utilize **Streamlit** for their web interfaces.

## Author
**Jinesh Khalas**
Data Science & AI Engineer

---

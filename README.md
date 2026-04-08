# Multilingual Social Media Insights Dashboard

**PhD Research Prototype**  
**Sentiment Analysis and Audience Insights for Indian Multilingual Social Media**

---

## 📌 Project Overview

This repository contains a **research-oriented Streamlit dashboard** developed as part of ongoing PhD research in Natural Language Processing (NLP) and Social Media Analytics.

The system enables **cross-platform analysis** of social media content from **Twitter (X), LinkedIn, and YouTube**, with a strong emphasis on **Indian multilingual and code-mixed content** (English + Tamil, Hinglish, etc.).

It serves as both an **interactive analysis tool** and a **research prototype** for experimenting with different sentiment models — from traditional lexicon-based approaches to state-of-the-art multilingual transformers.

---

## 🎯 Research Objectives

- Develop a hybrid framework for robust sentiment and category analysis on Indian social media data.
- Compare performance of lexicon-based (TextBlob) vs. transformer-based models (IndicBERT, MuRIL) on code-mixed text.
- Provide structured AI-generated insights using Large Language Models (Gemini).
- Create a reproducible, extensible prototype for multilingual social media analytics research.

---

## ✨ Key Features

- **Multi-Platform Support**: Twitter, LinkedIn (static datasets) and YouTube (live comments via API)
- **Multiple Sentiment Models**:
  - Baseline: TextBlob (Lexicon-based)
  - Advanced: IndicBERT (`ai4bharat/indic-bert`), MuRIL (`google/muril-base-cased`)
- **Category Classification**: Enhanced rule-based + zero-shot detection
- **AI Insights**: Structured, research-focused insights powered by Google Gemini
- **Evaluation Framework**: Accuracy, Macro F1-score, Weighted F1, Confusion Matrix
- **Interactive Visualizations**: Metrics cards, pie charts, bar plots, and model comparison
- **Modern UI**: Clean, responsive Streamlit interface with sidebar controls

---

## 📁 Project Structure

```bash
ai-social-media-insights/
├── app.py                  # Main Streamlit dashboard
├── config.py               # Configuration and model settings
├── data_loader.py          # Dataset loading and filtering
├── sentiment_models.py     # Sentiment analysis models (baseline + transformers)
├── category_models.py      # Category detection logic
├── insights_llm.py         # Gemini-powered structured insights
├── evaluation.py           # Model evaluation and metrics
├── visualization.py        # Charts and plots
├── youtube_fetcher.py      # YouTube Data API integration
├── utils.py                # Utilities and ethics disclaimer
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

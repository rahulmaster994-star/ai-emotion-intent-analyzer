# AI Emotion + Intent Analyzer – Chat Intelligence System

A premium, futuristic, 3D animated AI web application built with Python and Streamlit. This application analyzes user-entered text to detect emotion, intent, tone, urgency level, confidence score, and suggests smart replies using offline AI/NLP models (Hugging Face Transformers).

## Features
- **Emotion Detection:** Uses `j-hartmann/emotion-english-distilroberta-base`.
- **Intent & Urgency Classification:** Uses zero-shot classification via `facebook/bart-large-mnli`.
- **Tone Analysis:** Analyzes sentiment polarity.
- **Smart Reply Suggestion:** Generates contextual responses based on detected traits.
- **Batch Processing:** Upload a CSV for bulk analysis.
- **Voice Analyzer:** Records audio and transcribes it using `openai-whisper`.
- **Advanced Dashboard & Analytics:** Track usage and analysis history with Plotly charts.
- **Premium 3D UI:** Custom CSS with neon glows, glassmorphism, and hover animations.
- **Secure Authentication:** User login/signup with bcrypt hashing and SQLite storage.

## Tech Stack
- **Backend/Frontend:** Python, Streamlit
- **AI/NLP:** Hugging Face Transformers, PyTorch, openai-whisper
- **Database:** SQLite
- **Styling:** Custom CSS, HTML inside Streamlit
- **Data Visualization:** Pandas, Plotly

## Installation Steps

1. **Clone the repository** (or navigate to the directory).
2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   > **Note on Voice Analyzer:** The `openai-whisper` package requires `ffmpeg` to be installed on your system. 
   > - On Windows: Use `winget install ffmpeg` or download from the official site and add to PATH.
   > - On Mac: `brew install ffmpeg`
   > - On Linux: `sudo apt update && sudo apt install ffmpeg`

4. **Set up Environment Variables (Optional):**
   - Copy `.env.example` to `.env` if you need to add custom API tokens (like a HuggingFace token to bypass rate limits during model downloads).

## Run Command

Run the application using:
```bash
python -m streamlit run app.py
```

*Note: The first time you run the analyzer, it will download the necessary AI models (~1.5GB total). This may take a few minutes depending on your internet connection.*

## Folder Structure
```text
ai_emotion_intent_analyzer/
│
├── app.py                 # Main entry point and global navigation
├── ai_engine.py           # NLP model loading and inference logic
├── auth.py                # Authentication and session management
├── database.py            # SQLite database initialization and CRUD
├── utils.py               # Helper functions and CSS loader
├── requirements.txt
├── README.md
├── .env.example
├── .env                   # (Not in source control)
│
├── pages/                 # UI Modules for each page
│   ├── __init__.py
│   ├── landing.py
│   ├── login.py
│   ├── dashboard.py
│   ├── analyzer.py
│   ├── history.py
│   ├── analytics.py
│   ├── batch_analyzer.py
│   ├── voice_analyzer.py
│   ├── admin.py
│   ├── settings.py
│   ├── contributors.py
│   └── help.py
│
├── assets/
│   ├── images/
│   └── icons/
│
└── styles/
    └── custom.css         # 3D, neon, and glassmorphism styling
```

## Future Scope
- Integration with LLMs (e.g., LLaMA, GPT-4) for dynamic response generation.
- Real-time chat interface analysis.
- Multi-language support for emotion and intent detection.
- Export analytics reports to PDF.

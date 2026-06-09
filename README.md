<div align="center">

# 🧠 AI Emotion & Intent Analyzer
### A Next-Gen Chat Intelligence System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Models-orange.svg?style=for-the-badge)](https://huggingface.co/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)](https://pytorch.org/)

*A premium, futuristic, 3D-animated web application that analyzes text, voice, and facial expressions to detect emotion, intent, tone, urgency, and confidence—all powered by advanced offline NLP models.*

---

</div>

## ✨ Key Features

- **🎭 Emotion Detection:** Precise multi-emotion detection using `j-hartmann/emotion-english-distilroberta-base`.
- **🎯 Intent & Urgency Classification:** Zero-shot classification via `facebook/bart-large-mnli` to determine the underlying goal and time-sensitivity of a message.
- **🗣️ Voice Analyzer:** Record and transcribe audio in real-time using `openai-whisper`.
- **📸 Camera Analyzer:** Real-time visual emotion detection using computer vision.
- **📂 Batch Processing:** Upload CSV files for lightning-fast bulk analysis.
- **💡 Smart Reply Suggestion:** Generates contextual, empathetic responses based on detected traits.
- **📊 Advanced Analytics Dashboard:** Track usage, analyze historical data, and visualize trends with interactive Plotly charts.
- **🎨 Premium UI/UX:** Stunning aesthetics featuring 3D perspective transforms, glowing orbs, glassmorphism, pulse animations, and a vibrant Pink/Dark/Light theme switcher.
- **🔐 Secure Authentication:** Full user login/signup flow with bcrypt password hashing and SQLite storage.

---

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| **Frontend Framework** | Streamlit, HTML5, Custom CSS3 |
| **Backend Logic** | Python |
| **AI & NLP Core** | Hugging Face Transformers, PyTorch, OpenAI Whisper |
| **Database Management** | SQLite3 |
| **Data Visualization** | Pandas, Plotly Express |

---

## 🚀 Getting Started

Follow these steps to run the application on your local machine.

### 1. Clone the Repository
```bash
git clone https://github.com/rahulmaster994-star/ai-emotion-intent-analyzer.git
cd ai-emotion-intent-analyzer
```

### 2. Set Up Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
> **⚠️ Important note for Voice Analyzer:** The `openai-whisper` package requires `ffmpeg` to be installed on your system.
> - **Windows:** `winget install ffmpeg`
> - **Mac:** `brew install ffmpeg`
> - **Linux:** `sudo apt update && sudo apt install ffmpeg`

### 4. Environment Variables
Copy `.env.example` to `.env`. This step is optional but recommended if you want to bypass rate limits during model downloads or secure your local sessions:
```bash
HF_API_KEY=your_optional_huggingface_key
APP_SECRET_KEY=your_random_secret_string
```

### 5. Launch the App
```bash
python -m streamlit run app.py
```
*(Note: The first time you run the analyzer, it will securely download the required AI models (~1.5GB). This may take a few minutes.)*

---

## 📂 Project Architecture

```text
ai_emotion_intent_analyzer/
├── 📄 app.py                 # Main entry point & routing
├── 🧠 ai_engine.py           # NLP model loading & inference logic
├── 🔐 auth.py                # Authentication & session management
├── 🗄️ database.py            # SQLite database initialization & CRUD
├── ⚙️ utils.py               # Helper functions & dynamic CSS loader
├── 🎨 styles/                # UI Themes (Dark, Light, Premium Pink)
├── 📦 pages/                 # Modular UI pages (Dashboard, Analyzer, etc.)
├── 🖼️ static/                # Background images and banners
└── 👥 assets/images/         # Contributor avatars
```

---

## 🌍 Deployment (Streamlit Community Cloud)

This app is deployment-ready for Streamlit Cloud!
1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Connect your GitHub and select this repository.
3. Set the main file path to `app.py`.
4. The `packages.txt` file is already configured to install `ffmpeg` automatically on the Linux server.
5. Paste your `.env` variables into the **Secrets** section in the Streamlit dashboard.
6. Click **Deploy!**

---

## 🔮 Future Roadmap

- [ ] **LLM Integration:** Connect with LLaMA or GPT-4 APIs for dynamic, generative responses.
- [ ] **Live Chat Plugin:** Embed the analyzer into live customer support chat windows.
- [ ] **Multi-language Support:** Expand emotion and intent detection to global languages.
- [ ] **Export to PDF:** Download beautiful analytics reports.

---

<div align="center">
  <i>Built with ❤️ by the AI Core Team.</i>
</div>

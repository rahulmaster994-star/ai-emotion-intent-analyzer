import streamlit as st
import time
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    has_gemini = bool(os.getenv("GEMINI_API_KEY"))
except Exception:
    has_gemini = False

try:
    from transformers import pipeline
except ImportError:
    pipeline = None

# Using Streamlit's cache_resource to load models once and keep them in memory
@st.cache_resource(show_spinner="Loading Emotion Model...")
def load_emotion_model():
    if pipeline is None: return None
    try:
        return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)
    except Exception as e:
        print(f"Emotion model load error: {e}")
        return None

@st.cache_resource(show_spinner="Loading Intent & Urgency Model...")
def load_intent_model():
    if pipeline is None: return None
    try:
        # zero-shot classification for intents and urgency
        return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    except Exception as e:
        print(f"Intent model load error: {e}")
        return None

@st.cache_resource(show_spinner="Loading Sentiment Model...")
def load_tone_model():
    if pipeline is None: return None
    try:
        return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    except Exception as e:
        print(f"Tone model load error: {e}")
        return None

@st.cache_resource(show_spinner="Loading Face Emotion Model...")
def load_face_emotion_model():
    if pipeline is None: return None
    try:
        # Image classification for facial emotions
        return pipeline("image-classification", model="dima806/facial_emotions_image_detection")
    except Exception as e:
        print(f"Face emotion model load error: {e}")
        return None

def detect_emotion(text, model):
    if not model: return "Neutral", 0.0
    try:
        results = model(text)
        # Results format: [[{'label': 'joy', 'score': 0.9}, ...]]
        top_result = max(results[0], key=lambda x: x['score'])
        return top_result['label'].capitalize(), float(top_result['score'])
    except:
        return "Unknown", 0.0

def detect_intent(text, model):
    if not model: return "Unknown", 0.0
    candidate_labels = [
        "greeting", "complaint", "question", "request", "appreciation", 
        "feedback", "urgent help", "support query", "cancellation", 
        "refund request", "technical issue", "account issue", "general conversation"
    ]
    try:
        result = model(text, candidate_labels)
        return result['labels'][0].capitalize(), float(result['scores'][0])
    except:
        return "Unknown", 0.0
        
def detect_tone(text, model):
    if not model: return "Neutral", 0.0
    try:
        result = model(text)
        return result[0]['label'].capitalize(), float(result[0]['score'])
    except:
        return "Unknown", 0.0

def detect_urgency(text, model):
    if not model: return "Low", 0.0
    candidate_labels = ["low urgency", "medium urgency", "high urgency", "critical urgency"]
    try:
        result = model(text, candidate_labels)
        urgency = result['labels'][0].replace(" urgency", "").capitalize()
        return urgency, float(result['scores'][0])
    except:
        return "Low", 0.0

def generate_smart_reply(emotion, intent, tone, urgency, input_message=""):
    if has_gemini:
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"""
            You are a professional, empathetic, and highly capable customer support assistant.
            A user just sent the following message: "{input_message}"
            
            Our AI analysis system detected the following about the message:
            - Emotion: {emotion}
            - Intent: {intent}
            - Tone: {tone}
            - Urgency: {urgency}
            
            Based on this context, write a concise, professional, and empathetic response (2-3 sentences max) to directly address the user's issue or statement. 
            Do not include placeholders like "[Your Name]". Sound like a confident, helpful AI.
            """
            response = model.generate_content(prompt)
            if response.text:
                return response.text.strip()
        except Exception as e:
            print(f"Gemini API error: {e}")
            # Fall back to rule-based engine below if API fails
            
    # Rule-based contextual smart reply generation based on AI outputs (Fallback)
    reply = ""
    if urgency in ["Critical", "High"] or intent in ["Urgent help", "Technical issue"]:
        reply = "I understand this is critical. I'm escalating this immediately to our priority support team. "
    elif emotion == "Anger" or intent == "Complaint":
        reply = "I sincerely apologize for the inconvenience you've experienced. "
    elif intent == "Greeting":
        reply = "Hello! How can I assist you today? "
    elif emotion == "Joy" or intent == "Appreciation":
        reply = "Thank you so much! We're glad you're happy with our service. "
    else:
        reply = "Thank you for reaching out. Let me check that for you. "
        
    if intent == "Refund request":
        reply += "I will initiate the refund process right away. It typically takes 3-5 business days."
    elif intent == "Cancellation":
        reply += "I can help you cancel your subscription. Could you confirm your account details?"
    
    return reply

def generate_explanation(emotion, intent, urgency):
    return f"The system detected a primary emotion of '{emotion}' and identified the core intent as '{intent}'. Given the context, the urgency was evaluated as '{urgency}'."

def analyze_text(text):
    if not text or len(text.strip()) == 0:
        raise ValueError("Input text cannot be empty.")
        
    if pipeline is None:
        raise RuntimeError("Transformers library is not installed or models failed to load. Please check requirements.")
        
    emotion_model = load_emotion_model()
    intent_model = load_intent_model()
    tone_model = load_tone_model()
    
    emotion, emo_conf = detect_emotion(text, emotion_model)
    intent, int_conf = detect_intent(text, intent_model)
    tone, tone_conf = detect_tone(text, tone_model)
    urgency, urg_conf = detect_urgency(text, intent_model)
    
    # Simulate processing delay for effect
    time.sleep(1)
    
    overall_conf = (emo_conf + int_conf + tone_conf + urg_conf) / 4.0
    
    suggestion = generate_smart_reply(emotion, intent, tone, urgency, text)
    explanation = generate_explanation(emotion, intent, urgency)
    
    return {
        "input_message": text,
        "emotion": emotion,
        "emotion_confidence": emo_conf,
        "intent": intent,
        "intent_confidence": int_conf,
        "tone": tone,
        "urgency": urgency,
        "overall_confidence": overall_conf,
        "suggestion": suggestion,
        "explanation": explanation
    }

def analyze_face(image):
    model = load_face_emotion_model()
    if not model:
        raise RuntimeError("Face emotion model failed to load.")
    
    results = model(image)
    # Results format: [{'label': 'happy', 'score': 0.99}, ...]
    top_result = results[0]
    emotion = top_result['label'].capitalize()
    
    # Map common model labels to our standard emotions if necessary
    mapping = {
        'Happy': 'Joy',
        'Angry': 'Anger',
        'Sad': 'Sadness'
    }
    standardized_emotion = mapping.get(emotion, emotion)
    
    return standardized_emotion, float(top_result['score'])

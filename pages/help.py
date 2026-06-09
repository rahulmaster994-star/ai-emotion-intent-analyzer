import streamlit as st
from utils import back_to_home_button

def show_help():
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)
    st.markdown('<h2>❓ Help & FAQ</h2>', unsafe_allow_html=True)
    
    st.markdown("""<div class="glass-panel">
<h3 style="margin-top: 0;">How to use the app?</h3>
<p style="color:#aaa;">Navigate to the <b>Text Analyzer</b> from the menu. Enter any message in the text box and click "Analyze Now". The AI models will process the text and return insights. You can view past analyses in the <b>History</b> and <b>Analytics</b> tabs.</p>
<hr style="border-color: rgba(100, 150, 255, 0.1);">

<h3>What does Emotion Detection mean?</h3>
<p style="color:#aaa;">It classifies the text into 7 basic emotions: Joy, Anger, Sadness, Fear, Surprise, Disgust, and Neutral. It uses a DistilRoBERTa model fine-tuned on emotion datasets.</p>
<hr style="border-color: rgba(100, 150, 255, 0.1);">

<h3>What does Intent Detection mean?</h3>
<p style="color:#aaa;">It determines the primary goal of the user's message (e.g., Complaint, Refund request, Greeting). This uses a Zero-Shot classification model (BART Large).</p>
<hr style="border-color: rgba(100, 150, 255, 0.1);">

<h3>How does the Confidence Score work?</h3>
<p style="color:#aaa;">The models provide a probability score (0 to 1) for their predictions. We convert this to a percentage. The Overall Confidence is an average of the Emotion, Intent, Tone, and Urgency confidence scores.</p>
<hr style="border-color: rgba(100, 150, 255, 0.1);">

<h3>Troubleshooting</h3>
<ul style="color:#aaa;">
<li><b style="color:white;">Analysis takes too long:</b> The first time you run an analysis, the AI models are downloaded to your system (~1.5GB). Subsequent analyses will be much faster.</li>
<li><b style="color:white;">Voice analyzer fails:</b> Ensure you have <code>ffmpeg</code> installed on your system path, as Whisper requires it for audio processing.</li>
</ul>
</div>""", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    back_to_home_button()

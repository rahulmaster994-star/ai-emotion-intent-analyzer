"""
Privacy Policy Page
"""
import streamlit as st

def render():
    # ── Global Background Fix ──
    st.markdown("""
    <style>
    .stApp { background-color: transparent !important; }
    .stApp::before {
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-image: url("/app/static/bg_privacy.png") !important;
        background-size: cover !important; background-position: center !important;
        background-attachment: fixed !important; z-index: -2;
    }
    .stApp::after {
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(255, 255, 255, 0.88) !important;
        backdrop-filter: blur(15px) !important; z-index: -1; pointer-events: none;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
<div style="display: flex; justify-content: center; padding: 60px 20px;">
<div class="glass-card reveal" style="max-width: 900px; padding: 60px; background: #ffffff;">
<h1 style="color: #0f172a; font-weight: 800; margin-bottom: 30px;">Privacy Policy</h1>
<p style="color: #64748b; margin-bottom: 40px;">Last updated: May 2026</p>
<div style="color: #475569; line-height: 1.8;">
<h3 style="color: #0ea5e9; margin-top: 30px;">1. Information We Collect</h3>
<p>We collect information you provide directly to us when you use the AI Emotion + Intent Analyzer, including text inputs for analysis, account information, and usage metadata.</p>
<h3 style="color: #0ea5e9; margin-top: 30px;">2. How We Use Your Information</h3>
<p>We use the information we collect to provide, maintain, and improve our services, including training our local AI models (if enabled) and providing you with personalized analytics.</p>
<h3 style="color: #0ea5e9; margin-top: 30px;">3. Data Security</h3>
<p>We use enterprise-grade encryption and secure SQLite storage to protect your data. Your analysis history is stored locally or in your designated secure database instance.</p>
<h3 style="color: #0ea5e9; margin-top: 30px;">4. AI Processing</h3>
<p>Our AI processing is performed using state-of-the-art transformer models. We do not sell your personal data to third parties for advertising purposes.</p>
</div>
<div style="margin-top: 60px;">
""", unsafe_allow_html=True)
    
    if st.button("← Back to Home", key="back_from_privacy"):
        st.session_state.current_page = "landing"
        st.rerun()
        
    st.markdown("""
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


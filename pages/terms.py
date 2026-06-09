"""
Terms of Service Page
"""
import streamlit as st

def render():
    # ── Global Background Fix ──
    st.markdown("""
    <style>
    .stApp { background-color: transparent !important; }
    .stApp::before {
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-image: url("/app/static/bg_terms.png") !important;
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
<h1 style="color: #0f172a; font-weight: 800; margin-bottom: 30px;">Terms of Service</h1>
<p style="color: #64748b; margin-bottom: 40px;">Effective Date: May 2026</p>
<div style="color: #475569; line-height: 1.8;">
<h3 style="color: #0ea5e9; margin-top: 30px;">1. Acceptance of Terms</h3>
<p>By accessing or using the AI Emotion + Intent Analyzer, you agree to be bound by these Terms of Service.</p>
<h3 style="color: #0ea5e9; margin-top: 30px;">2. Use of Service</h3>
<p>You agree to use the service only for lawful purposes and in accordance with these terms. You are responsible for all text and media uploaded for analysis.</p>
<h3 style="color: #0ea5e9; margin-top: 30px;">3. Intellectual Property</h3>
<p>The AI models, underlying code, and branding of the NEURAL CORE system are the intellectual property of the project contributors.</p>
<h3 style="color: #0ea5e9; margin-top: 30px;">4. Limitation of Liability</h3>
<p>We provide the service "as is" and do not guarantee the absolute accuracy of AI-generated insights. We are not liable for any decisions made based on AI analysis results.</p>
</div>
<div style="margin-top: 60px;">
""", unsafe_allow_html=True)
    
    if st.button("← Back to Home", key="back_from_terms"):
        st.session_state.current_page = "landing"
        st.rerun()
        
    st.markdown("""
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


"""
Support Page
"""
import streamlit as st

def render():
    # ── Global Background Fix ──
    st.markdown("""
    <style>
    .stApp { background-color: transparent !important; }
    .stApp::before {
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-image: url("/app/static/bg_support.png") !important;
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
<div style="display: flex; justify-content: center; padding: 60px 20px 20px;">
<div class="glass-card reveal" style="max-width: 900px; width: 100%; padding: 60px; background: #ffffff;">
<h1 style="color: #0f172a; font-weight: 800; margin-bottom: 10px;">Support Center</h1>
<p style="color: #64748b; margin-bottom: 40px;">How can we help you today?</p>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 50px;">
<div style="padding: 25px; border-radius: 15px; border: 1px solid #e2e8f0;">
<h4 style="color: #0ea5e9; margin-bottom: 10px;">📧 Email Support</h4>
<p style="font-size: 0.9rem; color: #475569;">Reach out to our experts for technical help.</p>
<p style="color: #0ea5e9; font-weight: 600;">support@neuralcore.ai</p>
</div>
<div style="padding: 25px; border-radius: 15px; border: 1px solid #e2e8f0;">
<h4 style="color: #8b5cf6; margin-bottom: 10px;">📚 Documentation</h4>
<p style="font-size: 0.9rem; color: #475569;">Explore our comprehensive guides and API docs.</p>
<p style="color: #8b5cf6; font-weight: 600;">docs.neuralcore.ai</p>
</div>
</div>
</div>
</div>

<div style="display: flex; justify-content: center;">
<div style="max-width: 900px; width: 100%; padding: 0 20px;">
<h3 style="color: #0f172a; margin-top: 10px; margin-bottom: 20px;">Send us a message</h3>
""", unsafe_allow_html=True)
    
    # Use native Streamlit columns to constrain the form width
    _, col, _ = st.columns([1, 8, 1])
    with col:
        with st.form("support_form"):
            st.text_input("Subject")
            st.text_area("How can we help?", height=150)
            submit = st.form_submit_button("Submit Request", use_container_width=True)
            if submit:
                st.success("Support ticket created! We will get back to you soon.")
                
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to Home", key="back_from_support"):
            st.session_state.current_page = "landing"
            st.rerun()


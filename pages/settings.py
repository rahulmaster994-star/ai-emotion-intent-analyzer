import streamlit as st
import database as db
import auth
from utils import back_to_home_button

def show_settings():
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)
    st.markdown('<h2>⚙️ Settings</h2>', unsafe_allow_html=True)
    
    username = st.session_state.get('username')
    user_info = db.get_user(username)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3>Profile Details</h3>', unsafe_allow_html=True)
    st.write(f"**Username:** {user_info['username']}")
    st.write(f"**Email:** {user_info['email']}")
    
    st.markdown('<br><h3>Actions</h3>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🗑️ Clear My History", use_container_width=True):
            db.clear_history(username)
            st.success("History cleared.")
    with c2:
        if st.button("🚪 Logout", type="primary", use_container_width=True):
            auth.logout_user()
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<br><div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3>App Information</h3>', unsafe_allow_html=True)
    st.write("**Version:** 1.0.0")
    st.write("**Core AI Models:** distilroberta-base, bart-large-mnli, whisper-base")
    st.write("**Frameworks:** Python, Streamlit, Plotly, PyTorch")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    back_to_home_button()

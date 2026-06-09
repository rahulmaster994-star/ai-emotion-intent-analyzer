import streamlit as st
import database as db
import pandas as pd
from utils import back_to_home_button

def show_history():
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)
    st.markdown('<h2>📖 Analysis History</h2>', unsafe_allow_html=True)
    
    username = st.session_state.get('username')
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        search_kw = st.text_input("🔍 Search Message")
    with col2:
        emo_filter = st.selectbox("Filter Emotion", ["All", "Joy", "Anger", "Sadness", "Fear", "Surprise", "Disgust", "Neutral"])
    with col3:
        int_filter = st.selectbox("Filter Intent", ["All", "Greeting", "Complaint", "Question", "Request", "Appreciation", "Urgent help", "Technical issue", "Account issue"])
    with col4:
        urg_filter = st.selectbox("Filter Urgency", ["All", "Low", "Medium", "High", "Critical"])
        
    if search_kw:
        df = db.search_history(username, search_kw)
    else:
        df = db.filter_history(username, emo_filter, int_filter, urg_filter)
        
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if df.empty:
        st.info("No analysis history found.")
    else:
        st.dataframe(
            df[['timestamp', 'input_message', 'emotion', 'intent', 'urgency', 'overall_confidence']],
            use_container_width=True,
            hide_index=True
        )
        
        csv = df.to_csv(index=False).encode('utf-8')
        c1, c2 = st.columns([1, 4])
        with c1:
            st.download_button("📥 Export to CSV", csv, "analysis_history.csv", "text/csv", use_container_width=True)
        with c2:
            if st.button("🗑️ Clear All History", type="secondary"):
                db.clear_history(username)
                st.rerun()
                
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    back_to_home_button()

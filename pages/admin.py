import streamlit as st
import database as db
import pandas as pd
from utils import back_to_home_button

def show_admin():
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)
    st.markdown('<h2>🛡️ Admin Command Center</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#aaa;">System overview and user management.</p>', unsafe_allow_html=True)
    
    if not st.session_state.get('is_admin', False):
        st.error("You do not have permission to view this page.")
        back_to_home_button()
        return
        
    users_df = db.get_all_users_stats()
    analysis_df = db.get_all_analysis_stats()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'''
            <div class="glass-card metric-card">
                <h4 style="color: #00ffcc;">Total Users</h4>
                <h1>{len(users_df)}</h1>
            </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
            <div class="glass-card metric-card">
                <h4 style="color: #ff0055;">Total System Analyses</h4>
                <h1>{len(analysis_df)}</h1>
            </div>
        ''', unsafe_allow_html=True)
    with col3:
        top_system_emotion = "N/A"
        if not analysis_df.empty:
            top_system_emotion = analysis_df['emotion'].value_counts().idxmax()
            
        st.markdown(f'''
            <div class="glass-card metric-card">
                <h4 style="color: #4d4dff;">Most Common Emotion</h4>
                <h2>{top_system_emotion}</h2>
            </div>
        ''', unsafe_allow_html=True)
        
    st.markdown('<br>', unsafe_allow_html=True)
    
    st.markdown('<h3>👥 User Management</h3>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.dataframe(users_df[['id', 'username', 'email', 'full_name', 'is_admin', 'created_at', 'last_login']], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h3>📊 System Activity log</h3>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if not analysis_df.empty:
        st.dataframe(analysis_df[['timestamp', 'username', 'emotion', 'intent', 'urgency', 'overall_confidence']].sort_values(by='timestamp', ascending=False).head(50), use_container_width=True)
    else:
        st.info("No system activity yet.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    back_to_home_button()

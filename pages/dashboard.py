import streamlit as st
import database as db
from utils import back_to_home_button

def show_dashboard():
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)
    
    username = st.session_state.get('username', 'User')
    user_info = db.get_user(username)
    full_name = user_info['full_name'] if user_info and user_info.get('full_name') else username
    
    st.markdown(f'<h2>Welcome back, {full_name}! 👋</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#aaa;">Here is your intelligence overview.</p>', unsafe_allow_html=True)
    
    stats = db.get_user_stats(username)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'''
            <div class="glass-card metric-card">
                <h4 style="color: #00ffcc;">Total Analyses</h4>
                <h1>{stats['total_analyses']}</h1>
            </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
            <div class="glass-card metric-card">
                <h4 style="color: #ff0055;">Top Emotion</h4>
                <h2>{stats['top_emotion']}</h2>
            </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
            <div class="glass-card metric-card">
                <h4 style="color: #4d4dff;">Top Intent</h4>
                <h2>{stats['top_intent']}</h2>
            </div>
        ''', unsafe_allow_html=True)
    with col4:
        st.markdown(f'''
            <div class="glass-card metric-card">
                <h4 style="color: #ffcc00;">Avg Confidence</h4>
                <h2>{stats['avg_confidence']}%</h2>
            </div>
        ''', unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown('<h3>⚡ Quick Actions</h3>', unsafe_allow_html=True)
    
    qa1, qa2, qa3, qa4, qa5 = st.columns(5)
    with qa1:
        if st.button("💬 Text Analysis", use_container_width=True):
            st.session_state['current_page'] = 'analyzer'
            st.rerun()
    with qa2:
        if st.button("🎙️ Voice Analysis", use_container_width=True):
            st.session_state['current_page'] = 'voice_analyzer'
            st.rerun()
    with qa3:
        if st.button("📷 Camera Analysis", use_container_width=True):
            st.session_state['current_page'] = 'camera_analyzer'
            st.rerun()
    with qa4:
        if st.button("📂 Batch Upload", use_container_width=True):
            st.session_state['current_page'] = 'batch_analyzer'
            st.rerun()
    with qa5:
        if st.button("📊 View Full Analytics", use_container_width=True):
            st.session_state['current_page'] = 'analytics'
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)
    back_to_home_button()

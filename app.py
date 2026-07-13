import streamlit as st
import database as db
from utils import load_css

# Page Imports
from pages.landing import show_landing
from pages.login import show_login
from pages.dashboard import show_dashboard
from pages.analyzer import show_analyzer
from pages.history import show_history
from pages.analytics import show_analytics
from pages.batch_analyzer import show_batch_analyzer
from pages.voice_analyzer import show_voice_analyzer
from pages.camera_analyzer import show_camera_analyzer
from pages.admin import show_admin
from pages.settings import show_settings
from pages.contributors import show_contributors
from pages.help import show_help
import auth

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI Emotion + Intent Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INIT ---
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'dark'

load_css(st.session_state['theme'])
db.init_database()

# --- SESSION STATE ---
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'landing'
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'is_admin' not in st.session_state:
    st.session_state['is_admin'] = False

# Check URL query params to restore session on page refresh
params = st.query_params if hasattr(st, "query_params") else st.experimental_get_query_params()
session_id = params.get("session_id", None)
if isinstance(session_id, list):
    session_id = session_id[0] if session_id else None

if session_id and not st.session_state['authenticated']:
    username = db.get_session(session_id)
    if username:
        user_info = db.get_user(username)
        if user_info and user_info['is_active']:
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
            st.session_state['is_admin'] = bool(user_info['is_admin'])
            st.session_state['session_id'] = session_id
            st.session_state['current_page'] = 'dashboard'

def nav_to(page):
    st.session_state['current_page'] = page

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown('<h2>🤖 AI Core</h2>', unsafe_allow_html=True)
    st.markdown('<hr style="border-color: rgba(0, 255, 204, 0.2);">', unsafe_allow_html=True)
    
    if st.button("🏠 Home", use_container_width=True): nav_to('landing')
    
    if not st.session_state['authenticated']:
        if st.button("🔑 Login / Signup", use_container_width=True): nav_to('login')
    else:
        st.markdown('<p style="color:#aaa; font-size:12px; margin-bottom:5px;">Dashboard</p>', unsafe_allow_html=True)
        if st.button("📈 Overview", use_container_width=True): nav_to('dashboard')
        
        st.markdown('<p style="color:#aaa; font-size:12px; margin-bottom:5px; margin-top:15px;">Intelligence Tools</p>', unsafe_allow_html=True)
        if st.button("💬 Text Analyzer", use_container_width=True): nav_to('analyzer')
        if st.button("🎙️ Voice Analyzer", use_container_width=True): nav_to('voice_analyzer')
        if st.button("📷 Camera Analyzer", use_container_width=True): nav_to('camera_analyzer')
        if st.button("📂 Batch Analyzer", use_container_width=True): nav_to('batch_analyzer')
        
        st.markdown('<p style="color:#aaa; font-size:12px; margin-bottom:5px; margin-top:15px;">Data & Records</p>', unsafe_allow_html=True)
        if st.button("📖 History", use_container_width=True): nav_to('history')
        if st.button("📊 Analytics", use_container_width=True): nav_to('analytics')
        
        if st.session_state['is_admin']:
            st.markdown('<p style="color:#ff0055; font-size:12px; margin-bottom:5px; margin-top:15px;">Admin Controls</p>', unsafe_allow_html=True)
            if st.button("🛡️ Admin Panel", use_container_width=True): nav_to('admin')
            
        st.markdown('<p style="color:#aaa; font-size:12px; margin-bottom:5px; margin-top:15px;">Account</p>', unsafe_allow_html=True)
        if st.button("⚙️ Settings", use_container_width=True): nav_to('settings')
        if st.button("🚪 Logout", use_container_width=True): 
            auth.logout_user()
            st.rerun()

    st.markdown('<hr style="border-color: rgba(0, 255, 204, 0.2);">', unsafe_allow_html=True)
    if st.button("👥 Contributors", use_container_width=True): nav_to('contributors')
    if st.button("❓ Help", use_container_width=True): nav_to('help')
    
    st.markdown('<hr style="border-color: rgba(0, 255, 204, 0.2);">', unsafe_allow_html=True)
    st.markdown('<p style="color:#aaa; font-size:12px; margin-bottom:5px; margin-top:15px;">Theme</p>', unsafe_allow_html=True)
    
    theme_options = ['dark', 'light', 'pink']
    theme_display = ['🌙 Dark Mode', '☀️ Light Mode', '🌸 Premium Pink Mode']
    
    current_theme = st.session_state.get('theme', 'dark')
    if current_theme not in theme_options:
        current_theme = 'dark'
        
    current_index = theme_options.index(current_theme)
    
    selected_theme_display = st.selectbox(
        "Select Theme", 
        theme_display, 
        index=current_index,
        label_visibility="collapsed"
    )
    
    new_theme = theme_options[theme_display.index(selected_theme_display)]
    
    if new_theme != current_theme:
        st.session_state['theme'] = new_theme
        st.rerun()

# --- TOP BAR ---
if st.session_state['authenticated']:
    st.markdown("""
    <div class="top-bar-container">
        <div class="top-bar">
            <div class="top-bar-left">
                <span>Welcome back, <strong>AI Core Admin</strong> 👋</span>
            </div>
            <div class="top-bar-right">
                <button class="upgrade-btn">⚡ Upgrade Plan</button>
                <div style="background: rgba(255,255,255,0.1); width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer;">🔔</div>
                <div style="background: linear-gradient(135deg, #4d4dff, #ff0055); width: 30px; height: 30px; border-radius: 50%; cursor: pointer;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- ROUTER ---
page = st.session_state['current_page']

# Protected routes checking
protected_pages = ['dashboard', 'analyzer', 'history', 'analytics', 'batch_analyzer', 'voice_analyzer', 'camera_analyzer', 'admin', 'settings']

if page in protected_pages and not st.session_state['authenticated']:
    st.warning("You must be logged in to access this page.")
    show_login()
else:
    if page == 'landing': show_landing()
    elif page == 'login': show_login()
    elif page == 'dashboard': show_dashboard()
    elif page == 'analyzer': show_analyzer()
    elif page == 'history': show_history()
    elif page == 'analytics': show_analytics()
    elif page == 'batch_analyzer': show_batch_analyzer()
    elif page == 'voice_analyzer': show_voice_analyzer()
    elif page == 'camera_analyzer': show_camera_analyzer()
    elif page == 'admin': show_admin()
    elif page == 'settings': show_settings()
    elif page == 'contributors': show_contributors()
    elif page == 'help': show_help()
    else: show_landing()

import streamlit as st

def show_landing():
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)
    
    st.markdown('''
        <div style="text-align: center; padding: 50px 0;">
            <h1 class="hero-title">AI Emotion + Intent Analyzer</h1>
            <h3 style="color: #a0a0b0; margin-bottom: 30px;">A Smart Chat Intelligence System powered by AI and NLP</h3>
        </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 Get Started (Login)", use_container_width=True):
            st.session_state['current_page'] = 'login'
            st.rerun()
            
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown('<h3>✨ Core Features</h3>', unsafe_allow_html=True)
    
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        st.markdown('''
            <div class="glass-card metric-card">
                <h2>🧠</h2>
                <h4>Emotion Detection</h4>
                <p style="font-size: 12px; color: #aaa;">Deep NLP analysis to understand user sentiment</p>
            </div>
        ''', unsafe_allow_html=True)
    with col_b:
        st.markdown('''
            <div class="glass-card metric-card">
                <h2>🎯</h2>
                <h4>Intent Classification</h4>
                <p style="font-size: 12px; color: #aaa;">Zero-shot classification for actionable insights</p>
            </div>
        ''', unsafe_allow_html=True)
    with col_c:
        st.markdown('''
            <div class="glass-card metric-card">
                <h2>⚡</h2>
                <h4>Urgency Detection</h4>
                <p style="font-size: 12px; color: #aaa;">Identify critical messages instantly</p>
            </div>
        ''', unsafe_allow_html=True)
    with col_d:
        st.markdown('''
            <div class="glass-card metric-card">
                <h2>💬</h2>
                <h4>Smart Reply</h4>
                <p style="font-size: 12px; color: #aaa;">Context-aware automated response suggestions</p>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col_e, col_f, col_g, col_h = st.columns(4)
    with col_e:
        st.markdown('''
            <div class="glass-card metric-card">
                <h2>📊</h2>
                <h4>Analytics</h4>
            </div>
        ''', unsafe_allow_html=True)
    with col_f:
        st.markdown('''
            <div class="glass-card metric-card">
                <h2>🎙️</h2>
                <h4>Voice Analyzer</h4>
            </div>
        ''', unsafe_allow_html=True)
    with col_g:
        st.markdown('''
            <div class="glass-card metric-card">
                <h2>📂</h2>
                <h4>Batch Processing</h4>
            </div>
        ''', unsafe_allow_html=True)
    with col_h:
        st.markdown('''
            <div class="glass-card metric-card">
                <h2>🔒</h2>
                <h4>Secure Data</h4>
            </div>
        ''', unsafe_allow_html=True)
        
    st.markdown('''
        <hr style="border-color: rgba(255,255,255,0.1);">
        <div style="text-align: center; color: #888; font-size: 12px; padding: 20px;">
            Designed for advanced chat intelligence. &copy; 2026 AI Analyzer Team.
        </div>
        </div>
    ''', unsafe_allow_html=True)

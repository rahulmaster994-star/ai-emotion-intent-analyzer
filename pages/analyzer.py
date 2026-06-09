import streamlit as st
from ai_engine import analyze_text
import database as db
from utils import get_color_for_emotion, get_color_for_urgency

def show_analyzer():
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 5px;">
        <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #6a11cb, #2575fc); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 0 20px rgba(37,117,252,0.4);">💬</div>
        <h1 class="main-title" style="margin: 0; background: linear-gradient(90deg, #ffffff, #a0a0b0); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Text Intelligence Analyzer</h1>
    </div>
    <p style="color:#a0a0b0; font-size: 15px; margin-left: 65px; margin-bottom: 30px;">Enter text to detect emotion, intent, tone, urgency, and generate a smart reply.</p>
    """, unsafe_allow_html=True)
    
    # Top Grid
    col1, col2 = st.columns([2.5, 1])
    
    with col1:
        text_input = st.text_area("Message to analyze", height=150, placeholder="Type a message here or load an example...")
        st.markdown(f'<div style="text-align: right; font-size: 11px; color: #a0a0b0; margin-top: -15px; margin-bottom: 10px; position: relative; z-index: 10;">{len(text_input)} / 5000</div>', unsafe_allow_html=True)
        
        # Action Buttons Row
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("📄 Load Example 1", use_container_width=True):
                st.session_state['temp_text'] = "I am extremely angry! My account was charged twice and I want a refund right now!"
                st.rerun()
        with c2:
            if st.button("📄 Load Example 2", use_container_width=True):
                st.session_state['temp_text'] = "Thank you so much for your help yesterday. The service was excellent."
                st.rerun()
        with c3:
            if st.button("🧹 Clear", use_container_width=True):
                if 'temp_text' in st.session_state:
                    del st.session_state['temp_text']
                st.rerun()
        with c4:
            if st.button("← Back to Home", use_container_width=True):
                st.session_state['current_page'] = 'landing'
                st.rerun()
                
        if 'temp_text' in st.session_state and not text_input:
            text_input = st.session_state['temp_text']
    
    with col2:
        st.markdown('<div class="analysis-controls-hook"></div>', unsafe_allow_html=True)
        st.markdown('<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;"><span style="font-size: 18px;">⚙️</span><h4 style="margin:0; font-size: 16px; color:white;">Analysis Controls</h4></div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 12px; color: #a0a0b0; margin-bottom: 5px;">Characters</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size: 14px; color: #00ffcc; font-weight: bold; margin-bottom: 30px;">{len(text_input)} <span style="color: #a0a0b0; font-weight: normal; font-size: 12px;">/ 5000</span></p>', unsafe_allow_html=True)
        
        analyze_btn = st.button("🚀 Analyze Now", use_container_width=True, type="primary")
        st.markdown('<p style="font-size: 11px; color: #a0a0b0; text-align: center; margin-top: 15px;">Get AI-powered insights instantly</p>', unsafe_allow_html=True)
        
    # Divider
    st.markdown('<div style="margin: 25px 0;"></div>', unsafe_allow_html=True)
        
    if analyze_btn:
        if not text_input.strip():
            st.warning("Please enter some text to analyze.")
        else:
            with st.spinner("🧠 AI Models Processing..."):
                try:
                    result = analyze_text(text_input)
                    if 'username' in st.session_state:
                        db.save_analysis(st.session_state['username'], result)
                    
                    # Bottom Grid
                    bot_col1, bot_col2 = st.columns([1.5, 1])
                    
                    with bot_col1:
                        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
                        st.markdown("""
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <span style="color: #00ffcc;">📊</span>
                                <h4 style="margin:0; font-size: 15px;">Live Insight Preview</h4>
                            </div>
                            <div style="background: rgba(0, 255, 204, 0.1); border: 1px solid #00ffcc; border-radius: 12px; padding: 2px 8px; font-size: 10px; color: #00ffcc;">● Live</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        emo_col = get_color_for_emotion(result['emotion'])
                        urg_col = get_color_for_urgency(result['urgency'])
                        
                        st.markdown(f"""
                        <div style="display: flex; gap: 15px; flex-wrap: wrap;">
                            <div class="insight-pill">
                                <div class="pill-icon" style="background: rgba(0, 255, 204, 0.1); color: {emo_col};">😊</div>
                                <div>
                                    <div style="font-size: 10px; color: #a0a0b0;">Emotion</div>
                                    <div style="font-size: 13px; font-weight: 600; color: #fff;">{result['emotion']}</div>
                                </div>
                            </div>
                            <div class="insight-pill">
                                <div class="pill-icon" style="background: rgba(77, 77, 255, 0.1); color: #4d4dff;">🎯</div>
                                <div>
                                    <div style="font-size: 10px; color: #a0a0b0;">Intent</div>
                                    <div style="font-size: 13px; font-weight: 600; color: #fff;">{result['intent']}</div>
                                </div>
                            </div>
                            <div class="insight-pill">
                                <div class="pill-icon" style="background: rgba(0, 255, 150, 0.1); color: #00ff96;">〰️</div>
                                <div>
                                    <div style="font-size: 10px; color: #a0a0b0;">Tone</div>
                                    <div style="font-size: 13px; font-weight: 600; color: #fff;">{result['tone']}</div>
                                </div>
                            </div>
                            <div class="insight-pill">
                                <div class="pill-icon" style="background: rgba(255, 0, 85, 0.1); color: {urg_col};">⏱️</div>
                                <div>
                                    <div style="font-size: 10px; color: #a0a0b0;">Urgency</div>
                                    <div style="font-size: 13px; font-weight: 600; color: #fff;">{result['urgency']}</div>
                                </div>
                            </div>
                        </div>
                        <p style="font-size: 11px; color: #a0a0b0; text-align: center; margin-top: 20px;">Insights update in real-time as you type or analyze.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    with bot_col2:
                        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
                        st.markdown("""
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
                            <span style="color: #4d4dff;">🛡️</span>
                            <h4 style="margin:0; font-size: 15px;">Confidence Score</h4>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        overall = int(result["overall_confidence"] * 100)
                        emo_conf = int(result["emotion_confidence"] * 100)
                        int_conf = int(result["intent_confidence"] * 100)
                        tone_conf = int(min(1.0, result["overall_confidence"] * 1.05) * 100)
                        urg_conf = int(min(1.0, result["overall_confidence"] * 0.95) * 100)
                        
                        st.markdown(f"""
                        <div style="display: flex; align-items: center; gap: 20px;">
                            <div class="circular-progress" style="--progress: {overall}%;">
                                <div class="circular-progress-value">
                                    <div style="text-align: center;">
                                        {overall}%
                                        <div style="font-size: 8px; font-weight: normal; color: #a0a0b0; margin-top: -5px;">High Confidence</div>
                                    </div>
                                </div>
                            </div>
                            <div style="flex-grow: 1;">
                                <div class="confidence-row">
                                    <div class="confidence-label">Emotion</div>
                                    <div class="confidence-track"><div class="confidence-fill" style="width: {emo_conf}%; background: #00ffcc;"></div></div>
                                    <div class="confidence-value">{emo_conf}%</div>
                                </div>
                                <div class="confidence-row">
                                    <div class="confidence-label">Intent</div>
                                    <div class="confidence-track"><div class="confidence-fill" style="width: {int_conf}%; background: #4d4dff;"></div></div>
                                    <div class="confidence-value">{int_conf}%</div>
                                </div>
                                <div class="confidence-row">
                                    <div class="confidence-label">Tone</div>
                                    <div class="confidence-track"><div class="confidence-fill" style="width: {tone_conf}%; background: #00ff96;"></div></div>
                                    <div class="confidence-value">{tone_conf}%</div>
                                </div>
                                <div class="confidence-row">
                                    <div class="confidence-label">Urgency</div>
                                    <div class="confidence-track"><div class="confidence-fill" style="width: {urg_conf}%; background: #bf00ff;"></div></div>
                                    <div class="confidence-value">{urg_conf}%</div>
                                </div>
                            </div>
                        </div>
                        <p style="font-size: 10px; color: #a0a0b0; text-align: center; margin-top: 15px;">Model confidence based on input quality and context.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    st.markdown("""
                    <div class="glass-panel">
                        <h4 style="color: #00ffcc; font-size: 15px; margin-bottom: 10px;">💡 Smart Reply Suggestion</h4>
                        <p style="color: #e6f0ff; font-size: 14px;">{}</p>
                    </div>
                    """.format(result["suggestion"]), unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Analysis failed: {e}")
                    
    st.markdown('</div>', unsafe_allow_html=True)

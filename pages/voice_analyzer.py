import streamlit as st
import tempfile
import os
from ai_engine import analyze_text
import database as db
from utils import back_to_home_button, get_color_for_emotion, get_color_for_urgency

try:
    from streamlit_mic_recorder import mic_recorder
except ImportError:
    mic_recorder = None

try:
    import whisper
except ImportError:
    whisper = None

@st.cache_resource(show_spinner="Loading Whisper Model...")
def load_whisper_model():
    if whisper is None: return None
    try:
        # 'base' model is faster and smaller
        return whisper.load_model("base")
    except Exception as e:
        print(f"Whisper load error: {e}")
        return None

def show_voice_analyzer():
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)
    st.markdown('<h2>🎙️ Voice Intelligence Analyzer</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#aaa;">Record your voice to transcribe and analyze emotion and intent.</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="neon-card" style="text-align: center;">', unsafe_allow_html=True)
    
    if mic_recorder is None:
        st.error("Audio recording module not available. Please install streamlit-mic-recorder.")
        st.markdown('</div>', unsafe_allow_html=True)
        back_to_home_button()
        return
        
    if whisper is None:
        st.error("Whisper module not available. Please install openai-whisper.")
        st.markdown('</div>', unsafe_allow_html=True)
        back_to_home_button()
        return
    
    st.write("Click to start recording:")
    audio = mic_recorder(
        start_prompt="🔴 Start Recording",
        stop_prompt="⏹️ Stop Recording",
        just_once=True,
        use_container_width=False,
        format="webm",
        key='mic_record'
    )
    
    st.markdown('</div><br>', unsafe_allow_html=True)
    
    if audio:
        st.audio(audio['bytes'])
        
        with st.spinner("Transcribing audio..."):
            # Save audio bytes to a temp file for whisper
            try:
                # webm might need ffmpeg to convert to wav, whisper handles it if ffmpeg is installed
                fd, temp_path = tempfile.mkstemp(suffix=".webm")
                with os.fdopen(fd, 'wb') as f:
                    f.write(audio['bytes'])
                    
                model = load_whisper_model()
                if model:
                    result = model.transcribe(temp_path)
                    transcribed_text = result["text"].strip()
                    
                    st.markdown('<h4>Transcribed Text:</h4>', unsafe_allow_html=True)
                    st.info(transcribed_text)
                    
                    if transcribed_text:
                        with st.spinner("Analyzing text..."):
                            analysis = analyze_text(transcribed_text)
                            
                            # Save to db
                            if 'username' in st.session_state:
                                db.save_analysis(st.session_state['username'], analysis)
                            
                            st.success("Analysis Complete!")
                            
                            r1, r2, r3, r4 = st.columns(4)
                            with r1:
                                emo_col = get_color_for_emotion(analysis['emotion'])
                                st.markdown(f'''
                                    <div class="glass-card result-card" style="border-top: 3px solid {emo_col}">
                                        <p style="color:#aaa; font-size:12px; margin:0;">Emotion</p>
                                        <h3 style="color:{emo_col}; margin:0;">{analysis['emotion']}</h3>
                                    </div>
                                ''', unsafe_allow_html=True)
                            with r2:
                                st.markdown(f'''
                                    <div class="glass-card result-card" style="border-top: 3px solid #4d4dff">
                                        <p style="color:#aaa; font-size:12px; margin:0;">Intent</p>
                                        <h3 style="color:#4d4dff; margin:0;">{analysis['intent']}</h3>
                                    </div>
                                ''', unsafe_allow_html=True)
                            with r3:
                                urg_col = get_color_for_urgency(analysis['urgency'])
                                st.markdown(f'''
                                    <div class="glass-card result-card" style="border-top: 3px solid {urg_col}">
                                        <p style="color:#aaa; font-size:12px; margin:0;">Urgency</p>
                                        <h3 style="color:{urg_col}; margin:0;">{analysis['urgency']}</h3>
                                    </div>
                                ''', unsafe_allow_html=True)
                            with r4:
                                st.markdown(f'''
                                    <div class="glass-card result-card" style="border-top: 3px solid #ffcc00">
                                        <p style="color:#aaa; font-size:12px; margin:0;">Tone</p>
                                        <h3 style="color:#ffcc00; margin:0;">{analysis['tone']}</h3>
                                    </div>
                                ''', unsafe_allow_html=True)
                                
                            st.markdown(f'''
                                <div class="neon-card result-card" style="margin-top: 15px;">
                                    <h5 style="color: #00ffcc;">💡 Smart Reply Suggestion</h5>
                                    <p>{analysis['suggestion']}</p>
                                </div>
                            ''', unsafe_allow_html=True)
                else:
                    st.error("Failed to load Whisper model.")
            except Exception as e:
                st.error(f"Transcription error: {e}. Note: Whisper requires ffmpeg to be installed on your system.")
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

    st.markdown('</div>', unsafe_allow_html=True)
    back_to_home_button()

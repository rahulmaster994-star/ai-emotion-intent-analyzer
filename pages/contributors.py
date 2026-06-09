import streamlit as st
from utils import back_to_home_button

def show_contributors():
    from utils import get_image_base64
    
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-shadow: 0 0 10px rgba(255,255,255,0.3);">👥 Project Contributors</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#aaa;">The brilliant minds behind the <span style="color:#00ffcc; font-weight:bold;">AI Emotion + Intent Analyzer</span>.</p>', unsafe_allow_html=True)
    
    st.markdown('<br>', unsafe_allow_html=True)
    
    img_rahul = get_image_base64('rahul.jpeg')
    img_karan = get_image_base64('karan.jpeg')
    img_deepa = get_image_base64('deepa.jpeg')
    img_swayam = get_image_base64('swayam.jpeg')
    img_keerthana = get_image_base64('keerthana.jpeg')
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f"""<div class="glass-panel" style="text-align: center; padding: 20px; border-radius: 15px; height: 100%;">
<img src="{img_rahul}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 50%; border: 3px solid #00ffcc; margin-bottom: 15px; box-shadow: 0 0 15px rgba(0, 255, 204, 0.5);">
<h3 style="margin-bottom: 5px; margin-top: 0;">Rahul S</h3>
<p style="color: #00ffcc; font-size: 14px; font-weight: bold; margin-bottom: 10px;">Main Contributor</p>
<p style="color: #aaa; font-size: 12px; line-height: 1.4; margin-bottom: 0;">Contributed to the planning and overall development of the project.</p>
</div>""", unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""<div class="glass-panel" style="text-align: center; padding: 20px; border-radius: 15px; height: 100%;">
<img src="{img_karan}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 50%; border: 3px solid #00ffcc; margin-bottom: 15px; box-shadow: 0 0 15px rgba(0, 255, 204, 0.5);">
<h3 style="margin-bottom: 5px; margin-top: 0;">Karan M Rajur</h3>
<p style="color: #00ffcc; font-size: 14px; font-weight: bold; margin-bottom: 10px;">Helped with Development</p>
<p style="color: #aaa; font-size: 12px; line-height: 1.4; margin-bottom: 0;">Helped in building and improving the application features.</p>
</div>""", unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""<div class="glass-panel" style="text-align: center; padding: 20px; border-radius: 15px; height: 100%;">
<img src="{img_deepa}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 50%; border: 3px solid #00ffcc; margin-bottom: 15px; box-shadow: 0 0 15px rgba(0, 255, 204, 0.5);">
<h3 style="margin-bottom: 5px; margin-top: 0;">Deepa sri</h3>
<p style="color: #00ffcc; font-size: 14px; font-weight: bold; margin-bottom: 10px;">Helped with Design</p>
<p style="color: #aaa; font-size: 12px; line-height: 1.4; margin-bottom: 0;">Helped in designing the interface and improving user experience.</p>
</div>""", unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    
    blank1, c4, c5, blank2 = st.columns([1, 2, 2, 1])
    
    with c4:
        st.markdown(f"""<div class="glass-panel" style="text-align: center; padding: 20px; border-radius: 15px; height: 100%;">
<img src="{img_swayam}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 50%; border: 3px solid #4d4dff; margin-bottom: 15px; box-shadow: 0 0 15px rgba(77, 77, 255, 0.5);">
<h3 style="margin-bottom: 5px; margin-top: 0;">Swayam</h3>
<p style="color: #00ffcc; font-size: 14px; font-weight: bold; margin-bottom: 10px;">Helped with AI & NLP</p>
<p style="color: #aaa; font-size: 12px; line-height: 1.4; margin-bottom: 0;">Helped in emotion and intent analysis using AI and NLP.</p>
</div>""", unsafe_allow_html=True)
        
    with c5:
        st.markdown(f"""<div class="glass-panel" style="text-align: center; padding: 20px; border-radius: 15px; height: 100%;">
<img src="{img_keerthana}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 50%; border: 3px solid #ff0055; margin-bottom: 15px; box-shadow: 0 0 15px rgba(255, 0, 85, 0.5);">
<h3 style="margin-bottom: 5px; margin-top: 0;">Keerthana G</h3>
<p style="color: #00ffcc; font-size: 14px; font-weight: bold; margin-bottom: 10px;">Helped with Testing & Documentation</p>
<p style="color: #aaa; font-size: 12px; line-height: 1.4; margin-bottom: 0;">Helped in testing the application and maintaining documentation.</p>
</div>""", unsafe_allow_html=True)
        
    st.markdown('<br><br>', unsafe_allow_html=True)
    
    st.markdown("""<div class="glass-panel" style="display: flex; align-items: center; padding: 20px; border-radius: 15px;">
<div style="font-size: 40px; margin-right: 20px; text-shadow: 0 0 10px rgba(0,255,204,0.5);">🧠</div>
<div>
<h4 style="margin-bottom: 5px; margin-top: 0;">About the Project</h4>
<p style="color: #aaa; font-size: 12px; margin-bottom: 0; line-height: 1.5;">The AI Emotion + Intent Analyzer is an interdisciplinary project that combines Artificial Intelligence, Natural Language Processing, and an interactive interface to analyze emotions, detect intent, understand tone, and generate smart reply suggestions.</p>
</div>
</div>""", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    back_to_home_button()

import streamlit as st
import os
import base64

def get_image_base64(image_filename):
    image_path = os.path.join(os.path.dirname(__file__), 'assets', 'images', image_filename)
    if not os.path.exists(image_path):
        name = image_filename.split('.')[0]
        return f"https://ui-avatars.com/api/?name={name}&background=0d1117&color=00ffcc&size=100&rounded=true"
    
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    
    ext = image_filename.split('.')[-1].lower()
    mime = 'image/jpeg' if ext in ['jpg', 'jpeg'] else 'image/png'
    return f"data:{mime};base64,{encoded_string}"

def inject_floating_bubbles():
    bubbles_html = """
    <div class="bubble-container">
        <div class="bubble"></div>
        <div class="bubble"></div>
        <div class="bubble"></div>
        <div class="bubble"></div>
        <div class="bubble"></div>
        <div class="bubble"></div>
    </div>
    """
    st.markdown(bubbles_html, unsafe_allow_html=True)

def load_css(theme='dark'):
    css_path = os.path.join(os.path.dirname(__file__), 'styles', 'custom.css')
    try:
        with open(css_path, "r") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Custom CSS file not found.")
        
    if theme == 'light':
        light_css_path = os.path.join(os.path.dirname(__file__), 'styles', 'light.css')
        try:
            with open(light_css_path, "r") as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        except FileNotFoundError:
            pass
    elif theme == 'pink':
        pink_css_path = os.path.join(os.path.dirname(__file__), 'styles', 'pink.css')
        try:
            with open(pink_css_path, "r") as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        except FileNotFoundError:
            pass

    inject_floating_bubbles()

def back_to_home_button():
    st.markdown('<div style="margin-bottom: 20px;"></div>', unsafe_allow_html=True)
    if st.button("← Back to Home", key=f"back_home_{st.session_state.get('current_page', 'none')}"):
        st.session_state['current_page'] = 'landing'
        st.rerun()

def get_color_for_emotion(emotion):
    emotion = emotion.lower()
    colors = {
        'joy': '#00ffcc',
        'anger': '#ff0055',
        'sadness': '#4d4dff',
        'fear': '#bf00ff',
        'surprise': '#ffcc00',
        'disgust': '#a6ff4d',
        'neutral': '#cccccc'
    }
    return colors.get(emotion, '#ffffff')

def get_color_for_urgency(urgency):
    urgency = urgency.lower()
    colors = {
        'low': '#00ffcc',
        'medium': '#ffcc00',
        'high': '#ff6600',
        'critical': '#ff0055'
    }
    return colors.get(urgency, '#ffffff')

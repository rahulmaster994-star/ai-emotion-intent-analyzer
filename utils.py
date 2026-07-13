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

import streamlit.components.v1 as components

def inject_3d_solar_system():
    # Generates a randomized starfield in HTML
    import random
    stars_html = ""
    for _ in range(250):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        size = random.uniform(0.5, 2.5)
        opacity = random.uniform(0.3, 1.0)
        stars_html += f'<div class="star" style="left: {x}vw; top: {y}vh; width: {size}px; height: {size}px; opacity: {opacity};"></div>'

    solar_html = f"""
    <div class="starfield">
        {stars_html}
    </div>
    <div class="solar-system">
        <div class="sun"></div>
        
        <div class="orbit mercury-orbit">
            <div class="planet mercury"></div>
        </div>
        
        <div class="orbit venus-orbit">
            <div class="planet venus"></div>
        </div>
        
        <div class="orbit earth-orbit">
            <div class="planet earth"></div>
        </div>
        
        <div class="orbit mars-orbit">
            <div class="planet mars"></div>
        </div>
        
        <div class="orbit jupiter-orbit">
            <div class="planet jupiter"></div>
        </div>
        
        <div class="orbit saturn-orbit">
            <div class="planet saturn">
                <div class="saturn-ring"></div>
            </div>
        </div>
        
        <div class="orbit uranus-orbit">
            <div class="planet uranus"></div>
        </div>
        
        <div class="orbit neptune-orbit">
            <div class="planet neptune"></div>
        </div>
    </div>
    """
    st.markdown(solar_html, unsafe_allow_html=True)

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

    inject_3d_solar_system()

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

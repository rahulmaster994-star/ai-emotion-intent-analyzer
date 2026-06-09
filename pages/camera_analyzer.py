import streamlit as st
from PIL import Image
from ai_engine import analyze_face
from utils import back_to_home_button, get_color_for_emotion

def show_camera_analyzer():
    st.markdown("""
    <div class="page-container">
        <h1 class="main-title">📷 Camera Analyzer</h1>
        <p class="subtitle">Capture or upload an image and analyze it using AI.</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_image = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png"]
    )

    camera_image = st.camera_input("Or capture image using camera")

    image_file = uploaded_image if uploaded_image is not None else camera_image

    if image_file is not None:
        try:
            st.image(image_file, caption="Selected Image", use_container_width=True)

            with st.spinner("🧠 Analyzing facial emotion..."):
                img = Image.open(image_file)
                emotion, confidence = analyze_face(img)
                
            emo_col = get_color_for_emotion(emotion)

            st.markdown(f"""
            <div class="neon-card result-card" style="border-top: 3px solid {emo_col}">
                <h4 style="color: #00ffcc;">📊 Camera Analysis Result</h4>
                <p style="color:#aaa; font-size:12px; margin:0;">Detected Emotion</p>
                <h3 style="color:{emo_col}; margin:0;">{emotion}</h3>
                <p style="font-size:10px; margin:0;">{confidence*100:.1f}% confidence</p>
            </div>
            """, unsafe_allow_html=True)

            st.success("Image received and analyzed successfully.")

        except Exception as e:
            st.error(f"Failed to analyze image: {e}")

    else:
        st.info("Awaiting camera input... Please upload an image or grant camera permission.")

    back_to_home_button()
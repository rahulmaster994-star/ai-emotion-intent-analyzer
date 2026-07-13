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
    solar_js = """
    <script>
    const doc = window.parent.document;
    if (!doc.getElementById('solar-system-canvas')) {
        const canvas = doc.createElement('canvas');
        canvas.id = 'solar-system-canvas';
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        canvas.style.zIndex = '-999';
        canvas.style.pointerEvents = 'none';
        canvas.style.background = '#050914';
        doc.body.insertBefore(canvas, doc.body.firstChild);

        const ctx = canvas.getContext('2d');
        let width, height;

        function resize() {
            width = window.parent.innerWidth;
            height = window.parent.innerHeight;
            canvas.width = width;
            canvas.height = height;
        }
        window.parent.addEventListener('resize', resize);
        resize();

        const stars = [];
        for(let i = 0; i < 800; i++) {
            stars.push({
                x: Math.random() * 2000 - 1000,
                y: Math.random() * 2000 - 1000,
                z: Math.random() * 2000 - 1000,
                r: Math.random() * 1.2
            });
        }

        const planets = [
            {name: 'Mercury', r: 3, d: 60, s: 0.015, angle: Math.random()*Math.PI*2, color: '#a8a8a8'},
            {name: 'Venus', r: 5, d: 100, s: 0.011, angle: Math.random()*Math.PI*2, color: '#e3bb76'},
            {name: 'Earth', r: 5.5, d: 150, s: 0.009, angle: Math.random()*Math.PI*2, color: '#4b95f9'},
            {name: 'Mars', r: 4, d: 200, s: 0.007, angle: Math.random()*Math.PI*2, color: '#e27b58'},
            {name: 'Jupiter', r: 16, d: 320, s: 0.003, angle: Math.random()*Math.PI*2, color: '#c3a171'},
            {name: 'Saturn', r: 13, d: 430, s: 0.002, angle: Math.random()*Math.PI*2, color: '#ead6b8', ring: true},
            {name: 'Uranus', r: 9, d: 530, s: 0.001, angle: Math.random()*Math.PI*2, color: '#4fd0e7'},
            {name: 'Neptune', r: 8.5, d: 620, s: 0.0008, angle: Math.random()*Math.PI*2, color: '#4b70dd'}
        ];

        let time = 0;
        
        function drawSphere(x, y, r, color, glow) {
            ctx.beginPath();
            ctx.arc(x, y, r, 0, Math.PI * 2);
            let grad = ctx.createRadialGradient(x - r*0.3, y - r*0.3, r*0.1, x, y, r);
            grad.addColorStop(0, '#ffffff');
            grad.addColorStop(0.2, color);
            grad.addColorStop(1, '#000000');
            ctx.fillStyle = grad;
            ctx.fill();
        }

        function drawRing(x, y, r, scale) {
            ctx.beginPath();
            ctx.ellipse(x, y, r * 2.4, r * 0.8, 0, 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(234, 214, 184, 0.5)';
            ctx.lineWidth = r * 0.4;
            ctx.stroke();
        }

        function animate() {
            ctx.clearRect(0, 0, width, height);
            time += 1;
            
            const cx = width / 2;
            const cy = height / 2;
            
            ctx.fillStyle = '#ffffff';
            for(let i=0; i<stars.length; i++) {
                let s = stars[i];
                let sx = s.x * Math.cos(time*0.0002) - s.z * Math.sin(time*0.0002);
                let sz = s.z * Math.cos(time*0.0002) + s.x * Math.sin(time*0.0002);
                let scale = 800 / (800 + sz);
                if(scale < 0) continue;
                let px = cx + sx * scale;
                let py = cy + s.y * scale;
                ctx.globalAlpha = Math.min(1, scale * 0.8);
                ctx.beginPath();
                ctx.arc(px, py, s.r * scale, 0, Math.PI*2);
                ctx.fill();
            }
            ctx.globalAlpha = 1;

            ctx.beginPath();
            ctx.arc(cx, cy, 35, 0, Math.PI * 2);
            let sunGrad = ctx.createRadialGradient(cx, cy, 5, cx, cy, 35);
            sunGrad.addColorStop(0, '#ffffff');
            sunGrad.addColorStop(0.2, '#fff4cc');
            sunGrad.addColorStop(0.8, '#ff9900');
            sunGrad.addColorStop(1, '#ff3300');
            ctx.fillStyle = sunGrad;
            ctx.shadowBlur = 60;
            ctx.shadowColor = '#ff6600';
            ctx.fill();
            ctx.shadowBlur = 0;
            
            const perspectiveTilt = 0.35;
            
            ctx.lineWidth = 1;
            for (let p of planets) {
                ctx.beginPath();
                ctx.ellipse(cx, cy, p.d, p.d * perspectiveTilt, 0, 0, Math.PI * 2);
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.04)';
                ctx.stroke();
            }

            let renderPlanets = [];
            for(let p of planets) {
                p.angle -= p.s; 
                let px = Math.cos(p.angle) * p.d;
                let pz = Math.sin(p.angle) * p.d;
                renderPlanets.push({...p, px: px, pz: pz});
            }
            renderPlanets.sort((a,b) => a.pz - b.pz);

            for (let p of renderPlanets) {
                let scale = 800 / (800 + p.pz);
                let x = cx + p.px * scale;
                let y = cy + (p.pz * perspectiveTilt) * scale;
                let r = Math.max(0.1, p.r * scale);
                
                if (p.ring && p.pz > 0) drawRing(x, y, r, scale);
                drawSphere(x, y, r, p.color, false);
                if (p.ring && p.pz <= 0) drawRing(x, y, r, scale);
            }
            window.parent.requestAnimationFrame(animate);
        }
        animate();
    }
    </script>
    """
    components.html(solar_js, height=0, width=0)

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

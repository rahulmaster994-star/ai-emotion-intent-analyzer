import streamlit as st
import auth
from utils import back_to_home_button

def show_login():
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<h2 style="text-align: center;">Welcome Back</h2>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            with st.form("login_form"):
                login_user = st.text_input("Username")
                login_pass = st.text_input("Password", type="password")
                submit_login = st.form_submit_button("Login", use_container_width=True)
                
                if submit_login:
                    if login_user and login_pass:
                        success, msg = auth.login_user(login_user, login_pass)
                        if success:
                            st.success(msg)
                            st.session_state['current_page'] = 'dashboard'
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.warning("Please fill all fields")
            
        with tab2:
            with st.form("signup_form"):
                reg_full = st.text_input("Full Name")
                reg_user = st.text_input("Username")
                reg_email = st.text_input("Email")
                reg_pass = st.text_input("Password", type="password")
                reg_pass2 = st.text_input("Confirm Password", type="password")
                submit_signup = st.form_submit_button("Sign Up", use_container_width=True)
                
                if submit_signup:
                    if reg_pass != reg_pass2:
                        st.error("Passwords do not match!")
                    elif reg_user and reg_email and reg_pass and reg_full:
                        success, msg = auth.register_user(reg_user, reg_email, reg_pass, reg_full)
                        if success:
                            st.success(msg)
                        else:
                            st.error(msg)
                    else:
                        st.warning("Please fill all fields")
            
    st.markdown('</div>', unsafe_allow_html=True)
    back_to_home_button()

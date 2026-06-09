import streamlit as st
import bcrypt
import database as db

def verify_password(plain_password, hashed_password):
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def login_user(username, password):
    user = db.get_user(username)
    if user:
        if verify_password(password, user['password_hash']):
            if user['is_active']:
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                st.session_state['is_admin'] = bool(user['is_admin'])
                
                # Save session to DB and query params
                session_id = db.create_session(username)
                st.session_state['session_id'] = session_id
                
                if hasattr(st, "query_params"):
                    st.query_params["session_id"] = session_id
                else:
                    st.experimental_set_query_params(session_id=session_id)
                
                db.update_last_login(username)
                return True, "Login successful"
            else:
                return False, "Account is disabled"
    return False, "Invalid username or password"

def register_user(username, email, password, full_name):
    if db.get_user(username):
        return False, "Username already exists"
    if db.get_user_by_email(email):
        return False, "Email already exists"
        
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    success = db.create_user(username, email, hashed, full_name)
    
    if success:
        return True, "Registration successful! Please login."
    return False, "An error occurred during registration"

def logout_user():
    # Remove session from DB and query params
    if 'session_id' in st.session_state:
        db.delete_session(st.session_state['session_id'])
        
    if hasattr(st, "query_params"):
        if "session_id" in st.query_params:
            del st.query_params["session_id"]
    else:
        st.experimental_set_query_params()
        
    for key in ['authenticated', 'username', 'is_admin', 'current_page', 'session_id']:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state['current_page'] = 'landing'

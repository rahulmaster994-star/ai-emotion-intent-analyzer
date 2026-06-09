import sqlite3
import datetime
import bcrypt
import pandas as pd
import os

DB_NAME = 'ai_analyzer.db'

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            is_admin BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Create analysis_history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            input_message TEXT NOT NULL,
            emotion TEXT,
            emotion_confidence REAL,
            intent TEXT,
            intent_confidence REAL,
            tone TEXT,
            urgency TEXT,
            overall_confidence REAL,
            suggestion TEXT,
            explanation TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    ''')
    
    # Create sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    ''')
    
    # Insert default admin if not exists
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        hashed = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, full_name, is_admin)
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin', 'admin@example.com', hashed, 'System Administrator', True))
        
    conn.commit()
    conn.close()

def create_user(username, email, password_hash, full_name):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, full_name)
            VALUES (?, ?, ?, ?)
        ''', (username, email, password_hash, full_name))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user(username):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE LOWER(username) = LOWER(?)", (username,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def get_user_by_email(email):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def update_last_login(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE username = ?", (username,))
    conn.commit()
    conn.close()

def save_analysis(username, data_dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO analysis_history (
            username, input_message, emotion, emotion_confidence,
            intent, intent_confidence, tone, urgency, overall_confidence,
            suggestion, explanation
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        username,
        data_dict.get('input_message', ''),
        data_dict.get('emotion', ''),
        data_dict.get('emotion_confidence', 0.0),
        data_dict.get('intent', ''),
        data_dict.get('intent_confidence', 0.0),
        data_dict.get('tone', ''),
        data_dict.get('urgency', ''),
        data_dict.get('overall_confidence', 0.0),
        data_dict.get('suggestion', ''),
        data_dict.get('explanation', '')
    ))
    conn.commit()
    conn.close()

def get_analysis_history(username):
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM analysis_history WHERE username = ? ORDER BY timestamp DESC", conn, params=(username,))
    conn.close()
    return df

def delete_analysis(record_id, username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analysis_history WHERE id = ? AND username = ?", (record_id, username))
    conn.commit()
    conn.close()

def clear_history(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analysis_history WHERE username = ?", (username,))
    conn.commit()
    conn.close()

def get_user_stats(username):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM analysis_history WHERE username = ?", (username,))
    total = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT emotion, COUNT(emotion) as c FROM analysis_history 
        WHERE username = ? GROUP BY emotion ORDER BY c DESC LIMIT 1
    ''', (username,))
    row = cursor.fetchone()
    top_emotion = row[0] if row else "N/A"
    
    cursor.execute('''
        SELECT intent, COUNT(intent) as c FROM analysis_history 
        WHERE username = ? GROUP BY intent ORDER BY c DESC LIMIT 1
    ''', (username,))
    row = cursor.fetchone()
    top_intent = row[0] if row else "N/A"
    
    cursor.execute("SELECT AVG(overall_confidence) FROM analysis_history WHERE username = ?", (username,))
    row = cursor.fetchone()
    avg_conf = round(row[0] * 100, 2) if row and row[0] else 0.0
    
    conn.close()
    return {
        "total_analyses": total,
        "top_emotion": top_emotion,
        "top_intent": top_intent,
        "avg_confidence": avg_conf
    }

def get_all_users_stats():
    conn = get_connection()
    df = pd.read_sql_query("SELECT id, username, email, full_name, is_admin, created_at, last_login FROM users", conn)
    conn.close()
    return df

def get_all_analysis_stats():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM analysis_history", conn)
    conn.close()
    return df

def search_history(username, keyword):
    conn = get_connection()
    query = "SELECT * FROM analysis_history WHERE username = ? AND input_message LIKE ? ORDER BY timestamp DESC"
    df = pd.read_sql_query(query, conn, params=(username, f'%{keyword}%'))
    conn.close()
    return df

def filter_history(username, emotion=None, intent=None, urgency=None):
    conn = get_connection()
    query = "SELECT * FROM analysis_history WHERE username = ?"
    params = [username]
    
    if emotion and emotion != "All":
        query += " AND emotion = ?"
        params.append(emotion)
    if intent and intent != "All":
        query += " AND intent = ?"
        params.append(intent)
    if urgency and urgency != "All":
        query += " AND urgency = ?"
        params.append(urgency)
        
    query += " ORDER BY timestamp DESC"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

import uuid

def create_session(username):
    conn = get_connection()
    cursor = conn.cursor()
    session_id = str(uuid.uuid4())
    cursor.execute("INSERT INTO sessions (session_id, username) VALUES (?, ?)", (session_id, username))
    conn.commit()
    conn.close()
    return session_id

def get_session(session_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM sessions WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def delete_session(session_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()

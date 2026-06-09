import streamlit as st
import pandas as pd
import database as db
import plotly.express as px
from utils import back_to_home_button

def show_analytics():
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)
    st.markdown('<h2>📊 Analytics Dashboard</h2>', unsafe_allow_html=True)
    
    username = st.session_state.get('username')
    df = db.get_analysis_history(username)
    
    if df.empty:
        st.warning("Not enough data to generate analytics. Please run some text analysis first.")
    else:
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        
        with c1:
            emo_counts = df['emotion'].value_counts().reset_index()
            emo_counts.columns = ['Emotion', 'Count']
            fig_emo = px.pie(emo_counts, values='Count', names='Emotion', title='Emotion Distribution', hole=0.4,
                             color_discrete_sequence=px.colors.sequential.Teal)
            fig_emo.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_emo, use_container_width=True)
            
        with c2:
            int_counts = df['intent'].value_counts().reset_index()
            int_counts.columns = ['Intent', 'Count']
            fig_int = px.bar(int_counts, x='Intent', y='Count', title='Intent Distribution',
                             color='Count', color_continuous_scale='Purp')
            fig_int.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_int, use_container_width=True)
            
        st.markdown('</div><br>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        
        with c3:
            urg_counts = df['urgency'].value_counts().reset_index()
            urg_counts.columns = ['Urgency', 'Count']
            fig_urg = px.pie(urg_counts, values='Count', names='Urgency', title='Urgency Levels', hole=0.4,
                             color_discrete_sequence=['#00ffcc', '#ffcc00', '#ff6600', '#ff0055'])
            fig_urg.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_urg, use_container_width=True)
            
        with c4:
            date_counts = df.groupby('date').size().reset_index(name='Count')
            fig_time = px.line(date_counts, x='date', y='Count', title='Analyses Over Time', markers=True)
            fig_time.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            fig_time.update_traces(line_color='#ff0055')
            st.plotly_chart(fig_time, use_container_width=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
    back_to_home_button()

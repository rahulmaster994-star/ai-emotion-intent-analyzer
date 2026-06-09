import streamlit as st
import pandas as pd
from ai_engine import analyze_text
import database as db
from utils import back_to_home_button
import time

def show_batch_analyzer():
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)
    st.markdown('<h2>📂 Batch Intelligence Analyzer</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#aaa;">Upload a CSV or TXT file containing messages to analyze them in bulk using AI.</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload File", type=["csv", "txt", "tsv"])
    
    if uploaded_file is not None:
        try:
            file_name = uploaded_file.name.lower()
            
            # Read file based on type
            if file_name.endswith('.txt'):
                content = uploaded_file.read().decode('utf-8', errors='ignore')
                lines = [line.strip() for line in content.splitlines() if line.strip() and not line.strip().startswith('#')]
                df = pd.DataFrame({'Text': lines})
                text_col = 'Text'
            elif file_name.endswith('.tsv'):
                df = pd.read_csv(uploaded_file, sep='\t', comment='#', on_bad_lines='skip')
                text_col = None
            else:
                df = pd.read_csv(uploaded_file, comment='#', on_bad_lines='skip')
                text_col = None
            
            if df.empty:
                st.warning("The uploaded file is empty or could not be parsed.")
                return
            
            # Reset index to ensure clean integer indexing
            df = df.reset_index(drop=True)
            
            st.markdown("**Preview:**")
            st.dataframe(df.head(5), use_container_width=True)
            st.caption(f"📊 Total rows: **{len(df)}** | Columns: **{', '.join(df.columns)}**")
            
            # Auto-detect text column
            if text_col is None:
                detected = None
                for col in df.columns:
                    col_lower = col.lower()
                    if any(kw in col_lower for kw in ['text', 'message', 'content', 'comment', 'review', 'feedback', 'description', 'body', 'note', 'sentence', 'query', 'input']):
                        detected = col
                        break
                
                # Fallback: pick the column with the longest average string length
                if detected is None:
                    str_cols = df.select_dtypes(include=['object']).columns.tolist()
                    if str_cols:
                        avg_lens = {col: df[col].astype(str).str.len().mean() for col in str_cols}
                        detected = max(avg_lens, key=avg_lens.get)
                
                if detected:
                    text_col = st.selectbox(
                        "Select the column containing text to analyze:",
                        df.columns.tolist(),
                        index=df.columns.tolist().index(detected)
                    )
                else:
                    text_col = st.selectbox(
                        "Select the column containing text to analyze:",
                        df.columns.tolist()
                    )
            else:
                st.info(f"Auto-detected text column: **{text_col}**")
            
            # Convert selected column to string
            df[text_col] = df[text_col].astype(str)
            
            # Filter out empty/NaN-like rows
            valid_mask = df[text_col].apply(lambda x: x.strip() not in ['', 'nan', 'None', 'NaN', 'null'])
            valid_df = df[valid_mask].reset_index(drop=True)
            
            st.caption(f"✅ **{len(valid_df)}** valid text rows found for analysis.")
            
            if len(valid_df) == 0:
                st.warning("No valid text rows found in the selected column. Please choose a different column.")
                return
            
            if st.button("🚀 START BATCH ANALYSIS", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                results_list = []
                total = len(valid_df)
                
                for idx in range(total):
                    text = valid_df.iloc[idx][text_col].strip()
                    status_text.text(f"🔍 Analyzing {idx + 1}/{total}: \"{text[:50]}...\"" if len(text) > 50 else f"🔍 Analyzing {idx + 1}/{total}: \"{text}\"")
                    
                    try:
                        res = analyze_text(text)
                        
                        if 'username' in st.session_state:
                            db.save_analysis(st.session_state['username'], res)
                        
                        results_list.append({
                            'Original_Text': text,
                            'Emotion': res.get('emotion', 'N/A'),
                            'Emotion_Confidence': f"{res.get('emotion_confidence', 0) * 100:.1f}%",
                            'Intent': res.get('intent', 'N/A'),
                            'Tone': res.get('tone', 'N/A'),
                            'Urgency': res.get('urgency', 'N/A'),
                            'Smart_Reply': res.get('suggestion', 'N/A')
                        })
                    except Exception as ex:
                        results_list.append({
                            'Original_Text': text,
                            'Emotion': 'Error',
                            'Emotion_Confidence': '0%',
                            'Intent': 'Error',
                            'Tone': 'Error',
                            'Urgency': 'Error',
                            'Smart_Reply': str(ex)
                        })
                    
                    progress_bar.progress((idx + 1) / total)
                
                status_text.empty()
                st.success(f"✅ Successfully analyzed **{len(results_list)}** records!")
                
                res_df = pd.DataFrame(results_list)
                
                # Show results in a styled dataframe
                st.markdown("### 📊 Analysis Results")
                st.dataframe(res_df, use_container_width=True)
                
                # Summary stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    if 'Emotion' in res_df.columns:
                        top_emotion = res_df['Emotion'].mode()
                        st.metric("Top Emotion", top_emotion.iloc[0] if len(top_emotion) > 0 else "N/A")
                with col2:
                    if 'Intent' in res_df.columns:
                        top_intent = res_df['Intent'].mode()
                        st.metric("Top Intent", top_intent.iloc[0] if len(top_intent) > 0 else "N/A")
                with col3:
                    if 'Urgency' in res_df.columns:
                        top_urgency = res_df['Urgency'].mode()
                        st.metric("Top Urgency", top_urgency.iloc[0] if len(top_urgency) > 0 else "N/A")
                
                # Download button
                csv = res_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Download Analyzed Results (CSV)",
                    csv,
                    "batch_analysis_results.csv",
                    "text/csv",
                    use_container_width=True
                )
                
        except pd.errors.EmptyDataError:
            st.error("The file is empty. Please upload a valid file.")
        except pd.errors.ParserError as e:
            st.error(f"Could not parse the file. Please ensure it's a valid CSV/TSV. Error: {e}")
        except Exception as e:
            st.error(f"Error processing file: {e}")
            
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    back_to_home_button()

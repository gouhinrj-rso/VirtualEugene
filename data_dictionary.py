#1547

import streamlit as st
import pandas as pd
import sqlite3

def init_data_dictionary():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS data_dictionary 
                 (id INTEGER PRIMARY KEY, database_name TEXT, table_name TEXT, 
                  column_name TEXT, data_type TEXT, description TEXT, relationships TEXT)''')
    conn.commit()
    conn.close()

def upload_data_dictionary():
    uploaded_file = st.file_uploader("Upload Data Dictionary CSV", type="csv")
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            required_columns = ['database_name', 'table_name', 'column_name', 'data_type', 'description', 'relationships']
            if not all(col in df.columns for col in required_columns):
                st.error("CSV must contain columns: " + ", ".join(required_columns))
                return
            conn = sqlite3.connect('app.db')
            df.to_sql('data_dictionary', conn, if_exists='replace', index=False)
            conn.close()
            st.success("Data dictionary uploaded successfully!")
        except Exception as e:
            st.error(f"Error uploading CSV: {str(e)}")

def search_data_dictionary(search_term):
    try:
        conn = sqlite3.connect('app.db')
        c = conn.cursor()
        c.execute("SELECT * FROM data_dictionary WHERE column_name LIKE ? OR table_name LIKE ?", 
                  (f'%{search_term}%', f'%{search_term}%'))
        results = [{'database_name': row[1], 'table_name': row[2], 'column_name': row[3], 
                    'data_type': row[4], 'description': row[5], 'relationships': row[6]} 
                   for row in c.fetchall()]
        conn.close()
        return results
    except Exception as e:
        st.error(f"Error searching data dictionary: {str(e)}")
        return []

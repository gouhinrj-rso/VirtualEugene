# Databricks notebook source
import sqlite3
import streamlit as st

def init_knowledge_base():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS knowledge_base 
                 (id INTEGER PRIMARY KEY, title TEXT, content TEXT, code TEXT, tags TEXT)''')
    # Sample data (in practice, populate with real guides)
    sample_data = [
        ('Pandas GroupBy', 'Group data by columns', 'df.groupby("column").sum()', 'pandas,groupby'),
        ('Matplotlib Bar Plot', 'Create a bar plot', 'plt.bar(df["x"], df["y"])', 'matplotlib,plot'),
        ('PySpark Join', 'Join two DataFrames', 'df1.join(df2, "id", "inner")', 'pyspark,join')
    ]
    c.executemany('INSERT OR IGNORE INTO knowledge_base (title, content, code, tags) VALUES (?, ?, ?, ?)', sample_data)
    conn.commit()
    conn.close()

def search_knowledge_base(query):
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("SELECT title, content, code FROM knowledge_base WHERE tags LIKE ? OR title LIKE ? OR content LIKE ?", 
              (f'%{query}%', f'%{query}%', f'%{query}%'))
    results = [{'title': row[0], 'content': row[1], 'code': row[2]} for row in c.fetchall()]
    conn.close()
    return results
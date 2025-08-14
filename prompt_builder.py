# Databricks notebook source
import streamlit as st

def build_prompt():
    st.write("Let's build a custom prompt!")
    goal = st.text_input("What's your goal? (e.g., 'Analyze sales data')")
    tool = st.selectbox("Preferred tool", ["pandas", "PySpark", "Matplotlib", "Excel"])
    details = st.text_area("Any specific details or constraints?")
    
    if st.button("Generate Prompt"):
        prompt = f"Create a {tool} solution to {goal}. Details: {details}"
        st.write("Generated Prompt:", prompt)
        # Sample example based on tool
        if tool == "pandas":
            st.code("df = pd.read_csv('data.csv')\ndf.groupby('category').sum()", language='python')
        elif tool == "PySpark":
            st.code("df = spark.read.csv('data.csv')\ndf.groupBy('category').sum()", language='python')
        st.write("You can refine this prompt or copy it to the Notebook module!")
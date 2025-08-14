# Databricks notebook source
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

def clean_data():
    uploaded_file = st.file_uploader("Upload CSV for Cleaning", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Original Data Preview:", df.head())
        
        # Guided cleaning steps
        st.subheader("Cleaning Steps")
        
        # Handle missing values
        if df.isnull().sum().sum() > 0:
            st.write("Missing Values Detected:", df.isnull().sum())
            missing_action = st.selectbox("Handle missing values", ["Drop", "Fill with Mean", "Fill with Median", "Fill with Mode"])
            if missing_action == "Drop":
                df = df.dropna()
            elif missing_action == "Fill with Mean":
                df = df.fillna(df.mean(numeric_only=True))
            elif missing_action == "Fill with Median":
                df = df.fillna(df.median(numeric_only=True))
            elif missing_action == "Fill with Mode":
                df = df.fillna(df.mode().iloc[0])
        
        # Handle duplicates
        if df.duplicated().sum() > 0:
            st.write(f"Duplicates Detected: {df.duplicated().sum()}")
            if st.button("Remove Duplicates"):
                df = df.drop_duplicates()
        
        # Handle data types
        st.write("Current Data Types:", df.dtypes)
        for col in df.columns:
            if st.checkbox(f"Convert {col} to datetime"):
                try:
                    df[col] = pd.to_datetime(df[col])
                except:
                    st.warning(f"Cannot convert {col} to datetime")
        
        # Save cleaned DataFrame
        st.session_state.cleaned_df = df
        st.write("Cleaned Data Preview:", df.head())
        
        # Export options
        st.download_button(
            label="Download Cleaned Data as CSV",
            data=df.to_csv(index=False),
            file_name="cleaned_data.csv",
            mime="text/csv"
        )
        st.download_button(
            label="Download Cleaned Data as Excel",
            data=df.to_excel(index=False, engine='openpyxl'),
            file_name="cleaned_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
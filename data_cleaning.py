#1349

import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

def clean_data():
    uploaded_file = st.file_uploader("Upload CSV for Cleaning", type="csv")
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            col1, col2 = st.columns(2)
            with col1:
                st.write("Original Data Preview:", df.head(10))
            with col2:
                st.subheader("Cleaning Steps")
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
                if df.duplicated().sum() > 0:
                    st.write(f"Duplicates Detected: {df.duplicated().sum()}")
                    if st.button("Remove Duplicates"):
                        df = df.drop_duplicates()
                st.write("Current Data Types:", df.dtypes)
                for col in df.columns:
                    if st.checkbox(f"Convert {col} to datetime"):
                        try:
                            df[col] = pd.to_datetime(df[col])
                        except:
                            st.warning(f"Cannot convert {col} to datetime")
                st.session_state.cleaned_df = df
                st.write("Cleaned Data Preview:", df.head(10))
                st.download_button(
                    label="Download Cleaned Data as CSV",
                    data=df.to_csv(index=False),
                    file_name="cleaned_data.csv",
                    mime="text/csv"
                )
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                st.download_button(
                    label="Download Cleaned Data as Excel",
                    data=output.getvalue(),
                    file_name="cleaned_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        except Exception as e:
            st.error(f"Error processing CSV: {str(e)}")

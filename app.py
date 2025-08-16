# Databricks notebook source
import streamlit as st
import pandas as pd
from knowledge_base import search_knowledge_base, init_knowledge_base
from prompt_builder import build_prompt
from notebook import run_notebook
from data_dictionary import upload_data_dictionary, search_data_dictionary, init_data_dictionary
from data_cleaning import clean_data
from eda import perform_eda
from etl_agent import run_etl_agent
from io import BytesIO

st.set_page_config(page_title="Data Analytics Hub", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for better style and ergonomics
st.markdown("""
    <style>
    .section-divider { border-top: 1px solid #ddd; margin: 20px 0; }
    .stButton > button { width: 100%; }
    .stExpander { border: 1px solid #ddd; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# Initialize databases
with st.spinner("Initializing resources and prompts from APIs..."):
    init_knowledge_base()
    init_data_dictionary()

# Session state for cleaned data
if 'cleaned_df' not in st.session_state:
    st.session_state.cleaned_df = None


tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Overview",
    "Data Cleaning",
    "EDA",
    "Notebook",
    "ETL Assistant",
    "Resource Hub",
    "Prompt Builder",
    "ETL Agent",
])


with tab1:
    st.header("App Overview")
    st.write("Welcome to your Data Analytics Hub! Start with Data Cleaning, explore in EDA, analyze in Notebook, or access resources.")
    st.divider()  # Section divider
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Quick Status")
        if st.session_state.cleaned_df is not None:
            st.success("Data loaded! Rows: " + str(st.session_state.cleaned_df.shape[0]))
        else:
            st.info("No data loaded yet. Go to Data Cleaning tab.")
    with col2:
        st.subheader("Quick Links")
        st.markdown("- [Data Dictionary Upload](#data-dictionary)")
        st.markdown("- [Search Resources](#resource-hub)")
    st.expander("App Tips", expanded=True).write("Use tabs for navigation. Sidebar in modules for filters. Export data anytime.")

with tab2:
    st.header("Data Cleaning")
    clean_data()

with tab3:
    st.header("Exploratory Data Analysis (EDA)")
    perform_eda()

with tab4:
    st.header("Notebook")
    run_notebook()

with tab5:
    st.header("ETL Assistant")
    run_etl_agent()

with tab6:
    st.header("Resource Hub")
    query = st.text_input(
        "Search for guides (e.g., 'pandas groupby')",
        help="Search API-fetched docs and snippets.",
    )
    if query:
        results = search_knowledge_base(query)
        for result in results:
            with st.expander(result['title']):
                st.write(result['content'])
                st.code(result['code'], language='python')

with tab7:
    st.header("Prompt Builder")
    build_prompt()


with tab8:
    st.header("ETL Agent")
    run_etl_agent()


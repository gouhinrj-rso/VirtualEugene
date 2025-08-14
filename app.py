import streamlit as st
import pandas as pd
from knowledge_base import search_knowledge_base, init_knowledge_base
from prompt_builder import build_prompt
from notebook import run_notebook
from data_dictionary import upload_data_dictionary, search_data_dictionary, init_data_dictionary
from data_cleaning import clean_data
from eda import perform_eda
from io import BytesIO

st.set_page_config(page_title="Data Analytics Hub", layout="wide")

# Initialize session state for storing cleaned data
if 'cleaned_df' not in st.session_state:
    st.session_state.cleaned_df = None

# Initialize databases
init_knowledge_base()
init_data_dictionary()

# Sidebar navigation
st.sidebar.title("Data Analytics Hub")
module = st.sidebar.selectbox("Select Module", [
    "Resource Hub", "Prompt Builder", "Notebook", 
    "Data Dictionary", "Data Cleaning", "EDA"
])

# Main content
st.title("Data Analytics Hub")

if module == "Resource Hub":
    st.header("Resource Hub")
    query = st.text_input("Search for guides (e.g., 'pandas groupby')")
    if query:
        results = search_knowledge_base(query)
        for result in results:
            st.subheader(result['title'])
            st.write(result['content'])
            st.code(result['code'], language='python')

elif module == "Prompt Builder":
    st.header("Prompt Builder")
    build_prompt()

elif module == "Notebook":
    st.header("Notebook")
    run_notebook()

elif module == "Data Dictionary":
    st.header("Data Dictionary")
    upload_data_dictionary()
    search_term = st.text_input("Search for a field or chart")
    if search_term:
        results = search_data_dictionary(search_term)
        for result in results:
            st.write(f"Table: {result['table_name']}, Database: {result['database_name']}")
            st.write(f"Field: {result['column_name']}, Type: {result['data_type']}")
            st.write(f"Description: {result['description']}")
            st.write(f"Relationships: {result['relationships']}")
            if st.button(f"Download Table {result['table_name']}"):
                df = pd.DataFrame([result])
                # CSV export
                st.download_button(
                    label="Download as CSV",
                    data=df.to_csv(index=False),
                    file_name=f"{result['table_name']}.csv",
                    mime="text/csv"
                )
                # Excel export
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                st.download_button(
                    label="Download as Excel",
                    data=output.getvalue(),
                    file_name=f"{result['table_name']}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

elif module == "Data Cleaning":
    st.header("Data Cleaning")
    clean_data()

elif module == "EDA":
    st.header("Exploratory Data Analysis")
    perform_eda()
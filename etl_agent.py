
import streamlit as st
import sqlite3
from notebook import SparkSession
from pyspark.sql import functions as F
from knowledge_base import search_knowledge_base

def run_etl_agent():
    """Simple Streamlit-based ETL assistant using Spark."""
    st.info(
        "Upload a CSV or use cleaned data from session state to perform ETL steps with Spark."
    )

    if st.button("Get ETL Help"):
        resources = search_knowledge_base("ETL")
        for res in resources:
            with st.expander(res["title"], expanded=False):
                st.write(res["content"])
                if res["code"]:
                    st.code(res["code"], language="python")

    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    spark = SparkSession.builder.appName("ETLAgent").getOrCreate()
    sdf = None
    if uploaded_file is not None:
        sdf = spark.read.csv(uploaded_file, header=True, inferSchema=True)
        st.success("Loaded file into Spark DataFrame.")
    elif st.session_state.get("cleaned_df") is not None:
        sdf = spark.createDataFrame(st.session_state.cleaned_df)
        st.success("Using cleaned DataFrame from session state.")

    if sdf is None:
        st.warning("Please upload a CSV or clean data first.")
        return

    st.subheader("Column Selection")
    cols = sdf.columns
    selected_cols = st.multiselect("Select columns", cols, default=cols)
    sdf = sdf.select(*selected_cols)
    st.write(sdf.limit(10).toPandas())

    st.subheader("Transformations")
    transform = st.selectbox(
        "Choose a transformation",
        ["None", "Uppercase a column", "Filter rows"],
    )
    if transform == "Uppercase a column":
        string_cols = [c for c, t in sdf.dtypes if t == "string"]
        if string_cols:
            col_name = st.selectbox("Column", string_cols)
            sdf = sdf.withColumn(f"{col_name}_upper", F.upper(F.col(col_name)))
    elif transform == "Filter rows":
        col_name = st.selectbox("Column", selected_cols)
        value = st.text_input("Value equals")
        if value:
            sdf = sdf.filter(F.col(col_name) == value)

    st.write("Transformed Preview:")
    st.write(sdf.limit(10).toPandas())

    st.subheader("Write Output")
    write_option = st.selectbox(
        "Write option", ["None", "Download CSV", "Save to SQLite table"]
    )
    if write_option == "Download CSV":
        pdf = sdf.toPandas()
        st.download_button(
            "Download CSV",
            data=pdf.to_csv(index=False),
            file_name="etl_output.csv",
            mime="text/csv",
        )
    elif write_option == "Save to SQLite table":
        table_name = st.text_input("Table name", "etl_table")
        if st.button("Save to table"):
            pdf = sdf.toPandas()
            conn = sqlite3.connect("app.db")
            pdf.to_sql(table_name, conn, if_exists="replace", index=False)
            conn.close()
            st.success(f"Saved to table '{table_name}'.")

    st.markdown("### Sample ETL pipeline")
    sample_code = '''\
from pyspark.sql import SparkSession
from pyspark.sql.functions import upper

spark = SparkSession.builder.getOrCreate()
# Read
sdf = spark.read.csv("input.csv", header=True, inferSchema=True)
# Transform
sdf = sdf.select("col1", "col2")
sdf = sdf.withColumn("col1_upper", upper("col1"))
# Write
def_df = sdf.toPandas()
def_df.to_sql("my_table", sqlite3.connect("app.db"), if_exists="replace", index=False)
'''
    st.code(sample_code, language="python")

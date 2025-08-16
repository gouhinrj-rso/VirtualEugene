import streamlit as st
import pandas as pd


def guide_etl(df: pd.DataFrame, table_name: str, spark):
    try:
        if df is None:
            uploaded_file = st.file_uploader("Upload CSV for ETL", type="csv")
            if uploaded_file is None:
                return "Awaiting data for ETL.", "Upload a CSV file or use cleaned data."
            df = pd.read_csv(uploaded_file)
        if not table_name:
            return "Please specify a table name.", "Provide a name for the Delta table."
        sdf = spark.createDataFrame(df)
        sdf = sdf.dropna()
        sdf.write.format("delta").mode("overwrite").saveAsTable(table_name)
        row_count = sdf.count()
        return (
            f"Loaded {row_count} rows into Delta table '{table_name}'.",
            f"Next step: query with spark.sql('SELECT * FROM {table_name} LIMIT 10').",
        )
    except Exception as e:
        return f"ETL failed: {e}", "Check CSV format and table permissions."


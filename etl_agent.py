import sqlite3
import pandas as pd
import streamlit as st


def load_data_dictionary():
    """Load data dictionary from the SQLite database."""
    conn = sqlite3.connect('app.db')
    df = pd.read_sql_query('SELECT * FROM data_dictionary', conn)
    conn.close()
    return df


def find_relevant_fields(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """Return rows in the data dictionary matching the user's query."""
    query_lower = query.lower()
    mask = (
        df['column_name'].str.contains(query_lower, case=False, na=False)
        | df['description'].str.contains(query_lower, case=False, na=False)
        | df['table_name'].str.contains(query_lower, case=False, na=False)
    )
    return df[mask]


def parse_relationships(rel_str: str):
    """Parse relationship strings of the form 'table1.col -> table2.col'."""
    relationships = []
    if pd.isna(rel_str) or not rel_str:
        return relationships
    parts = [p.strip() for p in rel_str.split(';') if '->' in p]
    for part in parts:
        left, right = part.split('->')
        relationships.append({'left': left.strip(), 'right': right.strip()})
    return relationships


def build_etl_plan(df: pd.DataFrame, tables: list) -> list:
    """Create a basic ETL plan using relationships between tables."""
    steps = []
    if not tables:
        return steps

    base_table = tables[0]
    steps.append(f"Load table `{base_table}`")
    used_tables = {base_table}

    table_rels = df[['table_name', 'relationships']].drop_duplicates()
    for table in tables[1:]:
        row = table_rels[table_rels['table_name'] == table]
        rels = []
        if not row.empty:
            rels = parse_relationships(row.iloc[0]['relationships'])
        join_step = None
        for rel in rels:
            left_table = rel['left'].split('.')[0]
            right_table = rel['right'].split('.')[0]
            if left_table in used_tables:
                join_step = f"Join `{table}` on {rel['left']} = {rel['right']}"
                break
            if right_table in used_tables:
                join_step = f"Join `{table}` on {rel['right']} = {rel['left']}"
                break
        if join_step:
            steps.append(join_step)
            used_tables.add(table)
        else:
            steps.append(f"Consider joining `{table}`; relationship not found in dictionary")
    steps.append("Select necessary columns and apply transformations")
    return steps


def run_etl_agent():
    """Streamlit UI for the ETL agent."""
    st.subheader("ETL Agent")
    query = st.text_input("Describe your analysis goal or the data you need")
    if not query:
        return

    df = load_data_dictionary()
    results = find_relevant_fields(df, query)
    if results.empty:
        st.info("No matching fields found in data dictionary")
        return

    st.write("Suggested fields:")
    st.dataframe(
        results[['database_name', 'table_name', 'column_name', 'description']]
    )

    tables = results['table_name'].unique().tolist()
    steps = build_etl_plan(df, tables)
    if steps:
        st.write("Proposed ETL pipeline:")
        for i, step in enumerate(steps, start=1):
            st.write(f"{i}. {step}")


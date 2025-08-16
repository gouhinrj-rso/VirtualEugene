import streamlit as st
import pandas as pd
from io import BytesIO, StringIO


def clean_data():
    """Clean uploaded or pasted CSV data and generate Databricks-ready code."""

    input_mode = st.radio("Provide data via", ["Upload CSV", "Paste CSV"])
    df = None
    source_code = ""

    if input_mode == "Upload CSV":
        uploaded_file = st.file_uploader("Upload CSV for Cleaning", type="csv")
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                source_code = "df = pd.read_csv('/dbfs/path/to/your.csv')"
            except Exception as e:
                st.error(f"Error processing CSV: {str(e)}")
    else:
        pasted = st.text_area("Paste CSV data")
        if pasted:
            try:
                df = pd.read_csv(StringIO(pasted))
                source_code = (
                    "from io import StringIO\n"
                    "csv_data = '''\n" + pasted + "\n'''\n"
                    "df = pd.read_csv(StringIO(csv_data))"
                )
            except Exception as e:
                st.error(f"Error processing pasted CSV: {str(e)}")

    if df is not None:
        try:
            code_lines = ["import pandas as pd"]
            if source_code:
                code_lines.append(source_code)

            col1, col2 = st.columns(2)
            with col1:
                st.write("Original Data Preview:", df.head(10))
            with col2:
                st.subheader("Cleaning Steps")
                if df.isnull().sum().sum() > 0:
                    st.write("Missing Values Detected:", df.isnull().sum())
                    missing_action = st.selectbox(
                        "Handle missing values",
                        ["Drop", "Fill with Mean", "Fill with Median", "Fill with Mode"],
                    )
                    if missing_action == "Drop":
                        df = df.dropna()
                        code_lines.append("df = df.dropna()")
                    elif missing_action == "Fill with Mean":
                        df = df.fillna(df.mean(numeric_only=True))
                        code_lines.append("df = df.fillna(df.mean(numeric_only=True))")
                    elif missing_action == "Fill with Median":
                        df = df.fillna(df.median(numeric_only=True))
                        code_lines.append("df = df.fillna(df.median(numeric_only=True))")
                    elif missing_action == "Fill with Mode":
                        df = df.fillna(df.mode().iloc[0])
                        code_lines.append("df = df.fillna(df.mode().iloc[0])")
                if df.duplicated().sum() > 0:
                    st.write(f"Duplicates Detected: {df.duplicated().sum()}")
                    if st.button("Remove Duplicates"):
                        df = df.drop_duplicates()
                        code_lines.append("df = df.drop_duplicates()")
                st.write("Current Data Types:", df.dtypes)
                for col in df.columns:
                    if st.checkbox(f"Convert {col} to datetime"):
                        try:
                            df[col] = pd.to_datetime(df[col])
                            code_lines.append(
                                f"df['{col}'] = pd.to_datetime(df['{col}'])"
                            )
                        except Exception:
                            st.warning(f"Cannot convert {col} to datetime")

            st.session_state.cleaned_df = df
            st.write("Cleaned Data Preview:", df.head(10))
            st.download_button(
                label="Download Cleaned Data as CSV",
                data=df.to_csv(index=False),
                file_name="cleaned_data.csv",
                mime="text/csv",
            )
            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False)
            st.download_button(
                label="Download Cleaned Data as Excel",
                data=output.getvalue(),
                file_name="cleaned_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

            st.subheader("Code for Databricks")
            st.code("\n".join(code_lines), language="python")
        except Exception as e:

            st.error(f"Error processing data: {str(e)}")



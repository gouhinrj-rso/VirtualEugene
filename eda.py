#1548

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

def perform_eda():
    st.info("Exploratory Data Analysis: Upload data or use sample datasets to explore patterns, create visualizations, and gain insights.")
    
    # Sample data options
    st.subheader("🎯 Try Sample Data")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Load Employee Sample", help="Employee data with salary, performance, and demographics", key="eda_load_employee"):
            try:
                df = pd.read_csv('sample_data.csv')
                st.session_state.cleaned_df = df
                st.success(f"Loaded {len(df)} employee records!")
                st.rerun()
            except FileNotFoundError:
                st.error("Sample employee data file not found.")
    
    with col2:
        if st.button("Load Sales Sample", help="Product sales data with revenue, discounts, and categories", key="eda_load_sales"):
            try:
                df = pd.read_csv('sample_sales_data.csv')
                st.session_state.cleaned_df = df
                st.success(f"Loaded {len(df)} sales records!")
                st.rerun()
            except FileNotFoundError:
                st.error("Sample sales data file not found.")
    
    with col3:
        if st.button("Clear Data", help="Remove current dataset", key="eda_clear_data"):
            st.session_state.cleaned_df = None
            st.success("Data cleared!")
            st.rerun()

    if st.session_state.cleaned_df is not None:
        df = st.session_state.cleaned_df
        st.success(f"✅ Using dataset with {len(df)} rows and {len(df.columns)} columns")
        with st.expander("Data Preview", expanded=False):
            st.dataframe(df.head(10))
    else:
        uploaded_file = st.file_uploader("Upload CSV for EDA", type="csv", help="Upload your own CSV file for analysis")
        if uploaded_file:
            # Check file size (limit to 10MB)
            if uploaded_file.size > 10 * 1024 * 1024:
                st.warning("File is larger than 10MB. This may slow down processing. Consider uploading a smaller dataset.")
                return
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8', encoding_errors='ignore')
                st.session_state.cleaned_df = df
                st.success(f"Uploaded {len(df)} rows successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error uploading CSV: {str(e)}")
                return
        else:
            st.info("💡 **Get Started**: Load sample data above or upload your own CSV file to begin exploring!")
            st.markdown("""
            **Sample datasets include:**
            - **Employee Data**: Demographics, salaries, performance scores, departments
            - **Sales Data**: Product sales, revenue, discounts, customer segments
            
            **Or upload your own data** to explore patterns, create visualizations, and gain insights.
            """)
            return

    # Validate DataFrame
    if df.empty:
        st.error("The DataFrame is empty. Please upload a valid dataset.")
        return
    if len(df) > 100000:
        st.warning("Large dataset detected (>100,000 rows). Visualizations and exports may be slow.")

    # Enhanced Ask questions section with examples
    st.subheader("🔍 Ask About Your Data")
    
    # Show example questions based on data
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    with st.expander("💡 Example Questions You Can Ask", expanded=False):
        if numeric_cols and cat_cols:
            st.markdown(f"""
            **Distribution Questions:**
            - "Show distribution of {numeric_cols[0]}"
            - "Show histogram of {numeric_cols[0]}"
            
            **Comparison Questions:**
            - "Compare {numeric_cols[0]} by {cat_cols[0]}"
            - "Show {numeric_cols[0]} by category"
            
            **Statistical Questions:**
            - "Show correlation matrix"
            - "Show mean {numeric_cols[0]} by {cat_cols[0]}"
            - "Find outliers in {numeric_cols[0]}"
            
            **Visualization Questions:**
            - "Create scatter plot of {numeric_cols[0] if len(numeric_cols) > 0 else 'col1'} vs {numeric_cols[1] if len(numeric_cols) > 1 else 'col2'}"
            - "Show trends over time" (if you have date columns)
            """)
        else:
            st.markdown("""
            **Try these examples:**
            - "Show distribution of [column_name]"
            - "Show correlation matrix"
            - "Compare values by category"
            - "Find data summary"
            """)
    
    question = st.text_input("Ask a question about your data:", 
                           placeholder="e.g., 'Show distribution of salary' or 'Compare revenue by category'",
                           help="Type your question in natural language. The system will interpret and create appropriate visualizations.")
    
    if question:
        try:
            st.markdown("---")
            st.subheader(f"📊 Analysis: {question}")
            
            # Enhanced question parsing with more options
            question_lower = question.lower()
            
            if "distribution" in question_lower or "histogram" in question_lower:
                if not numeric_cols:
                    st.warning("No numeric columns available for distribution plot.")
                else:
                    # Auto-detect column from question or let user select
                    detected_col = None
                    for col in numeric_cols:
                        if col.lower() in question_lower:
                            detected_col = col
                            break
                    
                    if detected_col:
                        selected_col = detected_col
                        st.info(f"Auto-detected column: {selected_col}")
                    else:
                        selected_col = st.selectbox("Select column for distribution:", numeric_cols)
                    
                    # Create enhanced distribution plot
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
                    
                    # Histogram with KDE
                    sns.histplot(df[selected_col].dropna(), kde=True, ax=ax1)
                    ax1.set_title(f'Distribution of {selected_col}')
                    ax1.axvline(df[selected_col].mean(), color='red', linestyle='--', label='Mean')
                    ax1.axvline(df[selected_col].median(), color='green', linestyle='--', label='Median')
                    ax1.legend()
                    
                    # Box plot
                    sns.boxplot(y=df[selected_col], ax=ax2)
                    ax2.set_title(f'Box Plot of {selected_col}')
                    
                    st.pyplot(fig)
                    plt.clf()
                    
                    # Statistics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Mean", f"{df[selected_col].mean():.2f}")
                    with col2:
                        st.metric("Median", f"{df[selected_col].median():.2f}")
                    with col3:
                        st.metric("Std Dev", f"{df[selected_col].std():.2f}")
                    
                    st.write("**Next Steps:**")
                    st.code(f"df['{selected_col}'].describe()", language='python')
            
            elif "correlation" in question_lower:
                if len(numeric_cols) < 2:
                    st.warning("Need at least two numeric columns for correlation analysis.")
                else:
                    plt.figure(figsize=(10, 8))
                    corr_matrix = df[numeric_cols].corr()
                    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                               square=True, fmt='.2f')
                    plt.title('Correlation Matrix')
                    st.pyplot(plt)
                    plt.clf()
                    
                    # Show strongest correlations
                    st.write("**Strongest Correlations:**")
                    corr_pairs = []
                    for i in range(len(corr_matrix.columns)):
                        for j in range(i+1, len(corr_matrix.columns)):
                            corr_pairs.append({
                                'Variable 1': corr_matrix.columns[i],
                                'Variable 2': corr_matrix.columns[j],
                                'Correlation': corr_matrix.iloc[i, j]
                            })
                    corr_df = pd.DataFrame(corr_pairs)
                    corr_df = corr_df.reindex(corr_df['Correlation'].abs().sort_values(ascending=False).index)
                    st.dataframe(corr_df.head())
            
            elif "compare" in question_lower or "by" in question_lower:
                if not cat_cols or not numeric_cols:
                    st.warning("Need both categorical and numeric columns for comparison.")
                else:
                    # Auto-detect columns
                    detected_numeric = None
                    detected_cat = None
                    
                    for col in numeric_cols:
                        if col.lower() in question_lower:
                            detected_numeric = col
                            break
                    
                    for col in cat_cols:
                        if col.lower() in question_lower:
                            detected_cat = col
                            break
                    
                    numeric_col = detected_numeric if detected_numeric else st.selectbox("Select numeric column:", numeric_cols)
                    cat_col = detected_cat if detected_cat else st.selectbox("Select categorical column:", cat_cols)
                    
                    # Create comparison visualizations
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
                    
                    # Box plot
                    sns.boxplot(data=df, x=cat_col, y=numeric_col, ax=ax1)
                    ax1.set_title(f'{numeric_col} by {cat_col}')
                    ax1.tick_params(axis='x', rotation=45)
                    
                    # Bar plot of means
                    means = df.groupby(cat_col)[numeric_col].mean()
                    means.plot(kind='bar', ax=ax2)
                    ax2.set_title(f'Average {numeric_col} by {cat_col}')
                    ax2.tick_params(axis='x', rotation=45)
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.clf()
                    
                    # Summary statistics
                    summary = df.groupby(cat_col)[numeric_col].agg(['count', 'mean', 'median', 'std']).round(2)
                    st.write("**Summary Statistics:**")
                    st.dataframe(summary)
            
            elif "scatter" in question_lower:
                if len(numeric_cols) < 2:
                    st.warning("Need at least two numeric columns for scatter plot.")
                else:
                    col1 = st.selectbox("Select X column:", numeric_cols)
                    col2 = st.selectbox("Select Y column:", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
                    
                    plt.figure(figsize=(10, 6))
                    if cat_cols:
                        color_col = st.selectbox("Color by (optional):", ["None"] + cat_cols)
                        if color_col != "None":
                            sns.scatterplot(data=df, x=col1, y=col2, hue=color_col)
                        else:
                            sns.scatterplot(data=df, x=col1, y=col2)
                    else:
                        sns.scatterplot(data=df, x=col1, y=col2)
                    
                    plt.title(f'{col1} vs {col2}')
                    st.pyplot(plt)
                    plt.clf()
                    
                    # Show correlation
                    correlation = df[col1].corr(df[col2])
                    st.metric("Correlation Coefficient", f"{correlation:.3f}")
            
            elif "outlier" in question_lower:
                if not numeric_cols:
                    st.warning("No numeric columns available for outlier detection.")
                else:
                    col = st.selectbox("Select column for outlier detection:", numeric_cols)
                    
                    # IQR method for outlier detection
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
                    
                    st.write(f"**Outliers in {col}:**")
                    st.write(f"Found {len(outliers)} outliers out of {len(df)} records ({len(outliers)/len(df)*100:.1f}%)")
                    
                    if len(outliers) > 0:
                        st.dataframe(outliers)
                        
                        # Visualization
                        plt.figure(figsize=(12, 5))
                        plt.subplot(1, 2, 1)
                        sns.boxplot(y=df[col])
                        plt.title(f'Box Plot - {col}')
                        
                        plt.subplot(1, 2, 2)
                        plt.scatter(df.index, df[col], alpha=0.6)
                        plt.scatter(outliers.index, outliers[col], color='red', label='Outliers')
                        plt.axhline(upper_bound, color='red', linestyle='--', alpha=0.7)
                        plt.axhline(lower_bound, color='red', linestyle='--', alpha=0.7)
                        plt.title(f'Outlier Detection - {col}')
                        plt.legend()
                        
                        st.pyplot(plt)
                        plt.clf()
            
            elif "summary" in question_lower or "overview" in question_lower:
                st.write("**Dataset Overview:**")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Rows", len(df))
                with col2:
                    st.metric("Total Columns", len(df.columns))
                with col3:
                    st.metric("Missing Values", df.isnull().sum().sum())
                
                st.write("**Column Information:**")
                info_df = pd.DataFrame({
                    'Column': df.columns,
                    'Type': df.dtypes,
                    'Non-Null Count': df.count(),
                    'Null Count': df.isnull().sum(),
                    'Unique Values': [df[col].nunique() for col in df.columns]
                })
                st.dataframe(info_df)
                
                if numeric_cols:
                    st.write("**Numeric Summary:**")
                    st.dataframe(df[numeric_cols].describe())
            
            else:
                st.info("Question not recognized. Here's a general overview of your data:")
                
                # General analysis
                col1, col2 = st.columns(2)
                
                with col1:
                    if numeric_cols:
                        st.write("**Numeric Columns Summary:**")
                        st.dataframe(df[numeric_cols].describe())
                
                with col2:
                    if cat_cols:
                        st.write("**Categorical Columns:**")
                        for col in cat_cols[:3]:  # Show first 3 categorical columns
                            st.write(f"**{col}:**")
                            st.write(df[col].value_counts().head())
                
                st.write("**Try asking more specific questions like:**")
                st.code("Show distribution of [column_name]", language='text')
                st.code("Compare [numeric_column] by [category]", language='text')
                st.code("Show correlation matrix", language='text')
                    plt.clf()
                    st.write("Suggested next step: Check correlation between these columns")
                    st.code(f"df[['{col1}', '{col2}']].corr()", language='python')
                else:
                    st.warning("Need at least two numeric columns for scatter plot.")
            
            else:
                st.info("Question not recognized. Try 'distribution', 'correlation', 'mean', or 'scatter'.")
                st.write("Suggested next step: View summary statistics")
                st.code("df.describe()", language='python')
                st.write(df.describe())
            
            # Export DataFrame
            st.subheader("Export Data")
            st.download_button(
                label="Download Data as CSV",
                data=df.to_csv(index=False),
                file_name="eda_data.csv",
                mime="text/csv"
            )
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            st.download_button(
                label="Download Data as Excel",
                data=output.getvalue(),
                file_name="eda_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"Error processing question: {str(e)}")

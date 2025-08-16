# VirtualEugene

## Solution Overview

### Tech Stack: Streamlit (frontend and backend), pandas (data processing), Matplotlib/Seaborn (visualizations), PySpark (Databricks-like functionality), openpyxl/xlsxwriter (Excel exports), SQLite (lightweight database for data dictionary and knowledge base). All free or built-in, except Streamlit hosting (free on Community Cloud).
### Deployment: Push to a public GitHub repo, then deploy to Streamlit Community Cloud with one-click setup.
Features:

### Resource Hub: Searchable knowledge base with guides for pandas, Python, Matplotlib, Data Analytics, PySpark, Databricks, and Excel.
#### Prompt Builder: Interactive chatbot-style interface to create custom prompts with examples.
#### Notebook Module: Jupyter-like environment for running Python/PySpark code, mimicking Databricks.
#### Data Dictionary Upload: Upload CSV with Databricks cluster metadata (databases, tables, fields, relationships) for field/table searches and recommendations.
#### Data Cleaning Module: Upload CSV, guided cleaning with pandas/PySpark, output a clean table.
#### EDA Module: Use cleaned table to ask questions, auto-generate Python code for visualizations, and get analysis suggestions.

#### ETL Agent: Query the data dictionary and receive step-by-step joins and transformations for optimized datasets.
 ###Export: Any rendered DataFrame/table can be exported as CSV or Excel.




## Code Structure
The app will be split into modular Python files for clarity, with a main app.py to tie everything together. Here's the structure:

##### app.py: Main Streamlit app, orchestrates UI and navigation.
##### knowledge_base.py: Manages the searchable resource hub.
##### prompt_builder.py: Handles interactive prompt creation.
##### notebook.py: Implements the Databricks/Jupyter-like code execution.
##### data_dictionary.py: Processes CSV data dictionary uploads and searches.
##### data_cleaning.py: Guides CSV cleaning and transformation.
##### eda.py: Handles exploratory data analysis and visualization.
##### agents.py: Provides an OpenAI-powered assistant.
##### requirements.txt: Lists dependencies for deployment.
##### SQLite database (app.db) for storing knowledge base and data dictionary.

## Implementation
Below is the complete code for the app. Each module is designed to be modular and reusable, with Streamlit providing the interactive UI. I'll include comments for clarity and instructions for deployment at the end.


## OpenAI API Key Setup
Some features use OpenAI's API. Install requirements and provide an API key through an environment variable.

### Using shell environment
```bash
export OPENAI_API_KEY=sk-...
```

### Using a `.env` file
Create a `.env` file (use `.env.example` as a template) with the following line:

```
OPENAI_API_KEY=sk-...
```

The application will raise an error at startup if this key is not supplied.


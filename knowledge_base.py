# Databricks notebook source
import sqlite3
import streamlit as st

def init_knowledge_base():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS knowledge_base 
                 (id INTEGER PRIMARY KEY, title TEXT, content TEXT, code TEXT, tags TEXT)''')
    # Original sample data
    sample_data = [
        ('Pandas GroupBy', 'Group data by columns', 'df.groupby("column").sum()', 'pandas,groupby'),
        ('Matplotlib Bar Plot', 'Create a bar plot', 'plt.bar(df["x"], df["y"])', 'matplotlib,plot'),
        ('PySpark Join', 'Join two DataFrames', 'df1.join(df2, "id", "inner")', 'pyspark,join')
    ]
    # Scraped data for Databricks
    sample_data.extend([
        ('Create a New Notebook', 'Learn how to create a new notebook in your Databricks workspace by clicking New in the sidebar and then selecting Notebook. A blank notebook opens in the workspace.', '', 'databricks'),
        ('Query a Table Using SQL', 'Query the samples.nyctaxi.trips table in Unity Catalog using SQL by copying and pasting the provided code into a new notebook cell and running it.', 'SELECT * FROM samples.nyctaxi.trips', 'databricks,sql'),
        ('Visualize Query Results', 'Display the average fare amount by trip distance, grouped by pickup zip code, using the visualization editor in the notebook. Select Bar chart type, set fare_amount for X column, trip_distance for Y column, Average as aggregation, and pickup_zip as Group by column, then save.', '', 'databricks')
    ])
    # Scraped data for Python
    sample_data.extend([
        ('Introduction to Python', 'This tutorial is designed for programmers new to Python, not beginners new to programming. It introduces basic concepts and features of Python, expecting a basic understanding of programming. Python is easy to learn, powerful, with efficient high-level data structures, simple object-oriented programming, elegant syntax, dynamic typing, and is ideal for scripting and rapid application development. The Python interpreter and standard library are freely available in source or binary form for all major platforms, and can be extended with new functions and data types implemented in C or C++. The tutorial is not comprehensive but covers many noteworthy features, preparing readers to write Python modules and programs.', '', 'python,basics,introduction')
    ])
    # Scraped data for SQL (using search snippets since browse had issues; formatted as examples)
    sample_data.extend([
        ('SQL SELECT', 'Select all records from a table.', 'SELECT * FROM Customers;', 'sql,select'),
        ('SQL SELECT DISTINCT', 'Select distinct values.', 'SELECT DISTINCT Country FROM Customers;', 'sql,distinct'),
        ('SQL WHERE', 'Filter records.', 'SELECT * FROM Customers WHERE Country="Mexico";', 'sql,where'),
        ('SQL AND/OR', 'Combine conditions.', 'SELECT * FROM Customers WHERE Country="Germany" AND City="Berlin";', 'sql,and,or'),
        ('SQL ORDER BY', 'Sort results.', 'SELECT * FROM Customers ORDER BY Country;', 'sql,order by'),
        ('SQL INSERT INTO', 'Insert new records.', 'INSERT INTO Customers (CustomerName, ContactName) VALUES ("Cardinal", "Tom B. Erichsen");', 'sql,insert'),
        ('SQL UPDATE', 'Update records.', 'UPDATE Customers SET ContactName="Alfred Schmidt" WHERE CustomerID=1;', 'sql,update'),
        ('SQL DELETE', 'Delete records.', 'DELETE FROM Customers WHERE CustomerName="Alfreds Futterkiste";', 'sql,delete'),
        ('SQL LIMIT', 'Limit results.', 'SELECT * FROM Customers LIMIT 3;', 'sql,limit'),
        ('SQL MIN/MAX', 'Find min/max values.', 'SELECT MIN(Price) AS SmallestPrice FROM Products;', 'sql,min,max'),
        ('SQL COUNT', 'Count records.', 'SELECT COUNT(*) FROM Products;', 'sql,count'),
        ('SQL AVG', 'Average value.', 'SELECT AVG(Price) FROM Products;', 'sql,avg'),
        ('SQL SUM', 'Sum values.', 'SELECT SUM(Quantity) FROM OrderDetails;', 'sql,sum'),
        ('SQL LIKE', 'Pattern matching.', 'SELECT * FROM Customers WHERE CustomerName LIKE "a%";', 'sql,like'),
        ('SQL IN', 'Multiple values.', 'SELECT * FROM Customers WHERE Country IN ("Germany", "France");', 'sql,in'),
        ('SQL BETWEEN', 'Range values.', 'SELECT * FROM Products WHERE Price BETWEEN 10 AND 20;', 'sql,between'),
        ('SQL ALIAS', 'Rename columns/tables.', 'SELECT CustomerName AS Customer FROM Customers;', 'sql,alias'),
        ('SQL JOIN', 'Join tables.', 'SELECT Orders.OrderID, Customers.CustomerName FROM Orders INNER JOIN Customers ON Orders.CustomerID = Customers.CustomerID;', 'sql,join'),
        ('SQL UNION', 'Combine results.', 'SELECT City FROM Customers UNION SELECT City FROM Suppliers;', 'sql,union'),
        ('SQL GROUP BY', 'Group results.', 'SELECT COUNT(CustomerID), Country FROM Customers GROUP BY Country;', 'sql,group by'),
        ('SQL HAVING', 'Filter groups.', 'SELECT COUNT(CustomerID), Country FROM Customers GROUP BY Country HAVING COUNT(CustomerID) > 5;', 'sql,having')
    ])
    # Scraped data for VS Code
    sample_data.extend([
        ('Set Up Anaconda Environment', 'Create an Anaconda environment for the data science tutorial with necessary packages.', 'conda create -n myenv python=3.10 pandas jupyter seaborn scikit-learn keras tensorflow', 'vscode,data analysis'),
        ('Create VS Code Workspace', 'Create a folder for the VS Code workspace and open it in VS Code.', 'No specific code; use File > Open Folder in VS Code to open the "hello_ds" folder.', 'vscode,data analysis'),
        ('Create Jupyter Notebook', 'Create a new Jupyter notebook in VS Code for the tutorial.', 'Use Command Palette (Ctrl+Shift+P) and select "Create: New Jupyter Notebook" or create a file named "hello.ipynb".', 'vscode,data analysis'),
        ('Select Jupyter Notebook Kernel', 'Choose the Python environment created earlier as the kernel for the Jupyter notebook.', 'Select "Select Kernel" in the notebook and choose the created environment.', 'vscode,data analysis'),
        ('Load Titanic Dataset', 'Import pandas and numpy libraries and load the Titanic dataset into a pandas DataFrame.', 'import pandas as pd\nimport numpy as np\ndata = pd.read_csv("titanic3.csv")', 'vscode,data analysis'),
        ('Clean Data by Handling Missing Values', 'Replace question marks with NaN and update data types for age and fare columns.', 'data.replace("?", np.nan, inplace= True)\ndata = data.astype({"age": np.float64, "fare": np.float64})', 'vscode,data analysis'),
        ('Visualize Data with Seaborn and Matplotlib', 'Use seaborn and matplotlib to create plots showing relationships between variables and survival.', 'import seaborn as sns\nimport matplotlib.pyplot as plt\nfig, axs = plt.subplots(ncols=5, figsize=(30,5))\nsns.violinplot(x="survived", y="age", hue="sex", data=data, ax=axs[0])\nsns.pointplot(x="sibsp", y="survived", hue="sex", data=data, ax=axs[1])\nsns.pointplot(x="parch", y="survived", hue="sex", data=data, ax=axs[2])\nsns.pointplot(x="pclass", y="survived", hue="sex", data=data, ax=axs[3])\nsns.violinplot(x="survived", y="fare", hue="sex", data=data, ax=axs[4])', 'vscode,data analysis'),
        ('Convert Categorical Data to Numeric', 'Replace string values (male/female) with numeric values for correlation analysis.', 'data.replace({"male": 1, "female": 0}, inplace= True)', 'vscode,data analysis'),
        ('Calculate Correlations and Create New Variables', 'Analyze correlations and create a new "relatives" column based on sibsp and parch.', 'data.corr(numeric_only=True).abs()[["survived"]]\ndata["relatives"] = data.apply (lambda row: int((row["sibsp"] + row["parch"]) > 0), axis=1)\ndata.corr(numeric_only=True).abs()[["survived"]]', 'vscode,data analysis'),
        ('Prepare Data for Machine Learning', 'Drop unnecessary columns and rows with NaN values to prepare the dataset for training.', 'data = data[["sex", "pclass","age","relatives","fare","survived"]].dropna()', 'vscode,data analysis')
    ])
    # Scraped data for Data Analytics (using search snippets and general examples)
    sample_data.extend([
        ('SQL for Data Analysis Introduction', 'SQL is a standard language for accessing and manipulating databases, essential for data analysts.', '', 'data analytics,sql'),
        ('Python for Data Analytics', 'Use Python with pandas for data manipulation and analysis.', 'import pandas as pd\ndf = pd.read_csv("data.csv")', 'data analytics,python'),
        ('Integrating SQL with Python', 'Combine SQL queries in Python for efficient data analysis.', 'import pandas as pd\nimport sqlite3\nconn = sqlite3.connect("database.db")\ndf = pd.read_sql_query("SELECT * FROM table", conn)', 'data analytics,sql,python')
    ])
    c.executemany('INSERT OR IGNORE INTO knowledge_base (title, content, code, tags) VALUES (?, ?, ?, ?)', sample_data)
    conn.commit()
    conn.close()

def search_knowledge_base(query):
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("SELECT title, content, code FROM knowledge_base WHERE tags LIKE ? OR title LIKE ? OR content LIKE ?", 
              (f'%{query}%', f'%{query}%', f'%{query}%'))
    results = [{'title': row[0], 'content': row[1], 'code': row[2]} for row in c.fetchall()]
    conn.close()
    return results
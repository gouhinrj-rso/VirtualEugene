import sqlite3
import streamlit as st
import requests
from bs4 import BeautifulSoup


def init_knowledge_base(db_path: str = "app.db"):
    """Initialize the knowledge base SQLite database.

    Parameters
    ----------
    db_path:
        Path to the SQLite database file. Defaults to ``"app.db"``.

    The table uses a UNIQUE constraint on ``title`` so that calling this
    function multiple times does not insert duplicate rows.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS knowledge_base
                 (id INTEGER PRIMARY KEY, title TEXT UNIQUE, content TEXT, code TEXT, tags TEXT)"""
    )
    sample_data = [
        ('Query and visualize data', 'Use a Databricks notebook to query sample data stored in Unity Catalog using SQL, Python, Scala, and R, and then visualize the query results in the notebook.', '', 'databricks,querying data,visualizations,notebooks'),
        ('Import and visualize CSV data from a notebook', 'Use a Databricks notebook to import data from a CSV file containing baby name data from https://health.data.ny.gov into your Unity Catalog volume using Python, Scala, and R. You also learn to modify a column name, visualize the data, and save to a table.', '', 'databricks,querying data,visualizations,notebooks,data analytics'),
        ('Create a table', 'Create a table and grant privileges in Databricks using the Unity Catalog data governance model.', '', 'databricks,data analytics'),
        ('Build an ETL pipeline using Lakeflow Declarative Pipelines', 'Create and deploy an ETL (extract, transform, and load) pipeline for data orchestration using Lakeflow Declarative Pipelines and Auto Loader.', '', 'databricks,pyspark,data analytics'),
        ('Build an ETL pipeline using Apache Spark', 'Develop and deploy your first ETL (extract, transform, and load) pipeline for data orchestration with Apache Spark™.', '', 'databricks,pyspark,data analytics'),
        ('Train and deploy an ML model', 'Build a machine learning classification model using the scikit-learn library on Databricks to predict whether a wine is considered “high-quality”. This tutorial also illustrates the use of MLflow to track the model development process, and Hyperopt to automate hyperparameter tuning.', '', 'databricks,data analytics,pyspark'),
        ('Query LLMs and prototype AI agents with no-code', 'Use the AI Playground to query large language models (LLMs) and compare results side-by-side, prototype a tool-calling AI agent, and export your agent to code.', '', 'databricks,data analytics'),
        ('Introduction to Python', 'This tutorial introduces the reader informally to the basic concepts and features of the Python language and system.', '', 'python,basics,introduction'),
        ('An Informal Introduction to Python', 'The interpreter acts as a simple calculator: you can type an expression at it and it will write the value. Expression syntax is straightforward.', '3 + 5', 'python,basics'),
        ('Python Tutorial - W3Schools', 'Learn by examples! This tutorial supplements all explanations with clarifying examples.', 'print("Hello, World!")', 'python,basics'),
        ('Documenting Python Code: A Complete Guide', 'In this guide, you\'ll learn from the ground up how to properly document your Python code from the smallest of scripts to the largest of Python projects.', 'def hello_world():\n    """Print \'Hello, World!\'"""\n    print("Hello, World!")', 'python,documentation'),
        ('Python Tutorial - GeeksforGeeks', 'In this section, we\'ll cover the basics of Python programming, including installing Python, writing first program, understanding comments and working with variables.', 'x = 5\nprint(x)', 'python,basics,variables'),
        ('Python Tutorial - Tutorialspoint', 'This Python tutorial gives a complete understanding of Python programming language, starting from basic concepts to advanced concepts.', 'def add(a, b):\n    return a + b', 'python,functions'),
        ('Beginner\'s Guide to Python', 'New to programming? Python is free and easy to learn if you know where to start! This guide will help you to get started quickly.', '', 'python,basics'),
        ('The Hitchhiker\'s Guide to Python', 'This handcrafted guide exists to provide both novice and expert Python developers a best practice handbook for the installation, configuration, and usage of Python.', '', 'python,best practices'),
        ('SQL SELECT Command', 'The SELECT statement is used to select data from a database. The example shows how to select all columns from the Customers table.', 'SELECT * FROM Customers;', 'sql,command'),
        ('SQL WHERE Clause', 'The WHERE clause is used to filter records.', 'SELECT * FROM Customers WHERE Country=\'USA\';', 'sql,command'),
        ('SQL JOIN Operations', 'JOIN is used to combine rows from two or more tables based on a related column.', 'SELECT Customers.CustomerName, Orders.OrderID FROM Customers INNER JOIN Orders ON Customers.CustomerID=Orders.CustomerID;', 'sql,command'),
        ('SQL GROUP BY Clause', 'GROUP BY is used to arrange identical data into groups.', 'SELECT Country, COUNT(*) FROM Customers GROUP BY Country;', 'sql,command'),
        ('SQL Introduction', 'SQL is a standard language for accessing and manipulating databases.', '', 'sql,basics'),
        ('MySQL SQL Commands', 'Some of The Most Important SQL Commands like SELECT, UPDATE, DELETE.', 'UPDATE Customers SET ContactName=\'Alfred Schmidt\' WHERE CustomerID=1;', 'sql,command'),
        ('SQL Exercises', 'Practice SQL with exercises on various commands.', '', 'sql,exercises'),
        ('Set Up a Data Science Environment', 'Create an Anaconda environment for the data science tutorial, set up a VS Code workspace, and create a Jupyter notebook.', 'conda create -n myenv python=3.10 pandas jupyter seaborn scikit-learn keras tensorflow', 'vscode,data science'),
        ('Prepare the Data', 'Download and load the Titanic dataset, STS', 'import pandas as pd\nimport numpy as np\ndata = pd.read_csv(\'titanic3.csv\')\ndata.replace(\'?\', np.nan, inplace=True)\ndata = data.astype({"age": np.float64, "fare": np.float64})\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nfig, axs = plt.subplots(ncols=5, figsize=(30,5))\nsns.violinplot(x="survived", y="age", hue="sex", data=data, ax=axs[0])\ndata.replace({\'male\': 1, \'female\': 0}, inplace=True)\ndata.corr(numeric_only=True).abs()[["survived"]]\ndata[\'relatives\'] = data.apply(lambda row: int((row[\'sibsp\'] + row[\'parch\']) > 0), axis=1)\ndata = data[[\'sex\', \'pclass\',\'age\',\'relatives\',\'fare\',\'survived\']].dropna()', 'vscode,data science'),
        ('Train and Evaluate a Model', 'Use scikit-learn to split the dataset, normalize inputs, train a Naive Bayes model, and evaluate its accuracy.', 'from sklearn.model_selection import train_test_split\nx_train, x_test, y_train, y_test = train_test_split(data[[\'sex\',\'pclass\',\'age\',\'relatives\',\'fare\']], data.survived, test_size=0.2, random_state=0)', 'vscode,data science'),
        ('What is Data Analytics?', 'Data analytics is a process to uncover patterns and extract insights from raw data, helping organizations understand customers, create relevant content, strategize ad campaigns, develop products, and boost business performance.', '', 'data analytics'),
        ('Types of Data Analytics', 'Qualitative vs. Quantitative Research: Two methods used by data analysts, with differences in objectives, applications, and techniques.', '', 'data analytics'),
        ('Tools for Data Analytics', 'Python: Popular for data analytics due to libraries like NumPy. SQL: Essential for data analysis. Business Intelligence Tools: Top tools for insights.', '', 'data analytics,python,sql'),
        ('Best Practices for Data Analytics', 'Prerequisites include ability to work with numbers, some programming experience, willingness to learn statistical concepts, and passion for problem-solving. Applications include improved decision making, effective marketing, better customer service.', '', 'data analytics,best practices'),
        ('Walmart Case Study', 'Case study on Walmart using modern tools and technologies for deriving business insights and improving customer satisfaction.', '', 'data analytics')
    ]
    c.executemany(
        "INSERT OR IGNORE INTO knowledge_base (title, content, code, tags) VALUES (?, ?, ?, ?)",
        sample_data,
    )
    conn.commit()
    conn.close()


    fetch_web_docs(db_path)


def fetch_web_docs(db_path="app.db"):
    """Populate the knowledge base with documentation snippets fetched from the web."""
    docs = [
        (
            "Databricks Documentation",
            "https://docs.databricks.com/en/index.html",
            "databricks",
        ),
        ("SQL Documentation", "https://www.w3schools.com/sql/", "sql"),
        ("Python Documentation", "https://docs.python.org/3/", "python"),
        ("Pandas Documentation", "https://pandas.pydata.org/docs/", "pandas"),
        ("NumPy Documentation", "https://numpy.org/doc/stable/", "numpy"),
        (
            "Matplotlib Documentation",
            "https://matplotlib.org/stable/index.html",
            "matplotlib",
        ),
    ]

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    for title, url, tag in docs:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            content = " ".join(p.get_text() for p in soup.find_all("p")[:5])
            code = "\n".join(code.get_text() for code in soup.find_all("code")[:3])
            c.execute(
                "INSERT OR IGNORE INTO knowledge_base (title, content, code, tags) VALUES (?, ?, ?, ?)",
                (title, content, code, f"{tag},documentation"),
            )
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")

    conn.commit()
    conn.close()

def search_knowledge_base(query, db_path="app.db"):
    conn = sqlite3.connect(db_path)

    c = conn.cursor()
    c.execute(
        "SELECT title, content, code FROM knowledge_base WHERE tags LIKE ? OR title LIKE ? OR content LIKE ?",
        (f"%{query}%", f"%{query}%", f"%{query}%"),
    )
    results = [
        {"title": row[0], "content": row[1], "code": row[2]} for row in c.fetchall()
    ]
    conn.close()
    return results

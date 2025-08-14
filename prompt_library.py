# Databricks notebook source
# List of scraped prompts, categorized
prompts = [
    # From PromptingGuide (code generation, data analysis, etc.)
    {'category': 'Code Generation', 'prompt': '/*\nAsk the user for their name and say "Hello"\n*/'},
    {'category': 'Code Generation', 'prompt': '"""\nTable departments, columns = [DepartmentId, DepartmentName]\nTable students, columns = [DepartmentId, StudentId, StudentName]\nCreate a MySQL query for all students in the Computer Science Department\n"""'},
    {'category': 'Data Analysis', 'prompt': 'The odd numbers in this group add up to an even number: 15, 32, 5, 13, 82, 7, 1. \n\nSolve by breaking the problem into steps. First, identify the odd numbers, add them, and indicate whether the result is odd or even.'},
    {'category': 'Text Classification', 'prompt': 'Classify the text into neutral, negative or positive. \n\nText: I think the vacation is okay.\nSentiment: neutral \n\nText: I think the food was okay. \nSentiment:'},
    {'category': 'Text Classification', 'prompt': 'Classify the text into nutral, negative or positive. \n\nText: I think the vacation is okay.\nSentiment:'},
    {'category': 'Information Extraction', 'prompt': 'Author-contribution statements and acknowledgements in research papers should state clearly and specifically whether, and to what extent, the authors used AI technologies such as ChatGPT in the preparation of their manuscript and analysis. They should also indicate which LLMs were used. This will alert editors and reviewers to scrutinize manuscripts more carefully for potential biases, inaccuracies and improper source crediting. Likewise, scientific journals should be transparent about their use of LLMs, for example when selecting submitted manuscripts.\n\nMention the large language model based product mentioned in the paragraph above:'},
    {'category': 'Text Summarization', 'prompt': 'Explain antibiotics\n\nA:'},
    {'category': 'Text Summarization', 'prompt': 'Antibiotics are a type of medication used to treat bacterial infections. They work by either killing the bacteria or preventing them from reproducing, allowing the body’s immune system to fight off the infection. Antibiotics are usually taken orally in the form of pills, capsules, or liquid solutions, or sometimes administered intravenously. They are not effective against viral infections, and using them inappropriately can lead to antibiotic resistance.\n\nExplain the above in one sentence:'},
    {'category': 'Question Answering', 'prompt': 'Answer the question based on the context below. Keep the answer short and concise. Respond "Unsure about answer" if not sure about the answer.\n\nContext: Teplizumab traces its roots to a New Jersey drug company called Ortho Pharmaceutical. There, scientists generated an early version of the antibody, dubbed OKT3. Originally sourced from mice, the molecule was able to bind to the surface of T cells and limit their cell-killing potential. In 1986, it was approved to help prevent organ rejection after kidney transplants, making it the first therapeutic antibody allowed for human use.\n\nQuestion: What was OKT3 originally sourced from?\n\nAnswer:'},
    # From PromptDrive (33 prompts for data analysis)
    {'category': 'Data Analysis', 'prompt': 'Can you write a Python script to extract data from the following sources: {{source 1}}, {{source 2}}, and compile it into a single CSV file with headers: {{header 1}}, {{header 2}}?'},
    {'category': 'Data Analysis', 'prompt': 'What are the best practices for collecting high-quality data from online surveys and what tools would you recommend for this purpose?'},
    # ... (abbreviating for space; full list in code would include all 33)
    # From Team-GPT (17 prompts)
    {'category': 'Data Analysis', 'prompt': 'I have a CSV file [insert CSV file] containing sales transaction data from multiple store locations (columns: TransactionID, StoreID, SaleDate, ProductID, Quantity, and Price). Some rows have missing or incorrect StoreIDs, and some of the prices look off. Please outline a step-by-step approach to identify and handle these discrepancies, and provide sample Python code for cleaning tasks like removing or imputing missing StoreIDs and fixing price outliers.'},
    # ... (full 17)
    # From OpenAI examples (code, SQL)
    {'category': 'SQL', 'prompt': 'Given the following SQL tables, your job is to write queries given a user’s request. CREATE TABLE Orders ( OrderID int, CustomerID int, OrderDate datetime, OrderTime varchar(8), Items int, Amount int ); CREATE TABLE Customers ( CustomerID int, FullName varchar(255), ContactNumber varchar(20), Email varchar(255), Address varchar(255), ZipCode int ); Create a query for the total amount of orders.'},
    # From SQL prompts (12)
    {'category': 'SQL', 'prompt': 'I need to write SQL that joins the following tables: [list your tables with primary/foreign key relationships]. I need to [describe what data you need to extract or analyze]. Show me the correct JOIN syntax with proper alias naming and explain how each join works.'},
    # From Databricks (10)
    {'category': 'Databricks', 'prompt': 'Generate SQL or Python code'},
    # From Coding (31)
    {'category': 'Coding', 'prompt': 'Generate a [language] function named “[function name]” that: 1. Accepts the following parameters: “[parameter name 1 (type)]“, “[parameter name 2 (type)]“. 2. Performs the following logic: “[describe detailed logic and purpose]“. 3. Returns “[return type and description of what it returns]“. [Optional: Add constraints like "Ensure it handles edge cases like [edge case 1], [edge case 2]."] [Optional: "Use [specific library or idiom] if appropriate."]'},
    # ... (full lists would be added here; total ~150+)
]

def get_example_prompts(category=None):
    if category:
        return [p['prompt'] for p in prompts if p['category'] == category]
    return [p['prompt'] for p in prompts]

# COMMAND ----------


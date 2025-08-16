import streamlit as st
from prompt_library import get_example_prompts, prompts

def build_prompt():
    st.write("Let's build a custom prompt!")
    # Category filter for prompts
    categories = list(set(p['category'] for p in prompts)) + ["All"]
    category = st.selectbox("Select prompt category", categories)
    prompt_list = get_example_prompts(category if category != "All" else None)
    example_prompt = st.selectbox("Select an example prompt to start with", ["None"] + prompt_list)
    if example_prompt != "None":
        initial_prompt = example_prompt
    else:
        initial_prompt = ""
    goal = st.text_input("What's your goal? (e.g., 'Analyze sales data')", value=initial_prompt)
    tool = st.selectbox("Preferred tool", ["pandas", "PySpark", "Matplotlib", "Excel", "SQL", "VS Code"])
    details = st.text_area("Any specific details or constraints?")
    
    if st.button("Generate Prompt"):
        prompt = f"Create a {tool} solution to {goal}. Details: {details}"
        st.write("Generated Prompt:", prompt)
        # Sample example based on tool
        if tool == "pandas":
            st.code("df = pd.read_csv('data.csv')\ndf.groupby('category').sum()", language='python')
        elif tool == "PySpark":
            st.code("df = spark.read.csv('data.csv')\ndf.groupBy('category').sum()", language='python')
        st.write("You can refine this prompt or copy it to the Notebook module!")

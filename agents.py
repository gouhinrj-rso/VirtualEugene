import os
import streamlit as st
from openai import OpenAI

def run_agent():
    if not os.getenv("OPENAI_API_KEY"):
        st.warning("Set the OPENAI_API_KEY environment variable to use the agent.")
        return
    client = OpenAI()
    st.write("Interact with the OpenAI-powered data science agent.")
    prompt = st.text_area("Ask a question or describe a task:")
    if st.button("Run Agent") and prompt:
        with st.spinner("Contacting OpenAI..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                )
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"OpenAI API error: {e}")

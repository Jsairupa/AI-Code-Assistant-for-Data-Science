import os
import streamlit as st
import pandas as pd
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from langchain_community.llms.ollama import Ollama
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# ---------------------------
# Sidebar config
# ---------------------------
st.sidebar.title("Model Settings")

use_openai = st.sidebar.checkbox("Use OpenAI", value=True)

if use_openai:
    api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    model = st.sidebar.selectbox("OpenAI Model", ["gpt-4", "gpt-3.5-turbo"])
else:
    model = st.sidebar.selectbox("Ollama Model", ["mistral", "gemma", "llama2"])

temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 100, 1000, 500)

# ---------------------------
# Prompt Template
# ---------------------------
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a Python data science assistant. Based on the user's input, suggest data cleaning steps, write code, and explain it."),
    ("user", "Dataset preview:\n{preview}\n\nUser task: {task}")
])

# ---------------------------
# Function to generate LLM response
# ---------------------------
def generate_response(preview, task, use_openai, model, api_key, temperature):
    if use_openai:
        llm = ChatOpenAI(openai_api_key=api_key, temperature=temperature, model=model)
    else:
        llm = Ollama(model=model)

    parser = StrOutputParser()
    chain: Runnable = prompt_template | llm | parser
    return chain.invoke({"preview": preview, "task": task})

# ---------------------------
# Main App Interface
# ---------------------------
st.title("🧠 AI Code Assistant for Data Science")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
user_task = st.text_area("Describe your task (e.g., 'Clean the data and create a model to predict churn')")

if uploaded_file and user_task:
    try:
        df = pd.read_csv(uploaded_file)
        st.subheader("📊 Data Preview")
        st.write(df.head())

        # Create sample preview for the LLM
        sample_preview = df.head(3).to_csv(index=False)

        with st.spinner("🧠 Generating response from the assistant..."):
            response = generate_response(sample_preview, user_task, use_openai, model, api_key, temperature)

        st.subheader("🧹 Suggested Cleaning + Code + Explanation")
        st.markdown(response)

    except Exception as e:
        st.error(f"❌ Failed to read CSV: {e}")

elif uploaded_file and not user_task:
    st.info("✏️ Please describe your data task.")
elif user_task and not uploaded_file:
    st.info("📁 Please upload a CSV file to analyze.")

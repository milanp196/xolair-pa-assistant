import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

import streamlit as st

st.title("PA Assistant for Xolair Admins")

uploaded_file = st.file_uploader("Upload a denial letter or fax (PDF or image)")
if uploaded_file:
    st.write("File received:", uploaded_file.name)
    st.success("This is where we’ll process the document.") 

def summarize_prior_auth(text):
    prompt = f"""
You are a medical admin assistant AI.

A clinic staff member just received this document. Your job is to:
1. Determine the type of document (denial, approval, or request for info)
2. Summarize the key message in plain English
3. Suggest the next steps they should take to move the prior auth forward
4. Output as clearly formatted bullet points

Here’s the document content:
{text}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

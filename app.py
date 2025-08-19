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
        import pdfplumber

    # Extract text from PDF
    with pdfplumber.open(uploaded_file) as pdf:
        text = "\n".join([page.extract_text() or "" for page in pdf.pages])

    st.markdown("### 🧾 Extracted Document Text")
    st.text_area("Raw Text", text, height=250)

    # Button to trigger GPT-4
    if st.button("Analyze with AI"):
        with st.spinner("Analyzing..."):
            summary = summarize_prior_auth(text)
        st.markdown("### 🧠 AI Summary & Next Steps")
        st.write(summary)

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

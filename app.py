import streamlit as st
import pdfplumber
from openai import OpenAI

# --- Secure API Key from Streamlit Secrets ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Streamlit App Title ---
st.title("PA Assistant for Xolair Admins")

# --- Summarization Function ---
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
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- File Upload ---
uploaded_file = st.file_uploader("Upload a denial letter or fax (PDF only)")

if uploaded_file:
    st.write("📎 File received:", uploaded_file.name)

    # Extract text using pdfplumber
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    except Exception as e:
        st.error(f"Error reading file: {e}")
        text = ""

    if text.strip() == "":
        st.warning("⚠️ No readable text found in the uploaded PDF.")
    else:
        st.markdown("### 🧾 Extracted Document Text")
        st.text_area("Raw Text", text, height=250)

        # --- Analyze with AI ---
        if st.button("Analyze with AI"):
            with st.spinner("Analyzing with GPT-4..."):
                summary = summarize_prior_auth(text)
            st.markdown("### 🧠 AI Summary & Next Steps")
            st.write(summary)

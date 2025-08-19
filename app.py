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

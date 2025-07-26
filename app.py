import streamlit as st

st.title("PA Assistant for Xolair Admins")

uploaded_file = st.file_uploader("Upload a denial letter or fax (PDF or image)")
if uploaded_file:
    st.write("File received:", uploaded_file.name)
    st.success("This is where we’ll process the document.")

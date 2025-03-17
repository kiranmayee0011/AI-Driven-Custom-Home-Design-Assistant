import streamlit as st
import pandas as pd
import PyPDF2
from docx import Document
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("AIzaSyCJGCaLxcVcakWgE6qOlyrw6G3VIiScN0U")

genai.configure(api_key=AIzaSyCJGCaLxcVcakWgE6qOlyrw6G3VIiScN0UPI_KEY)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# Function to get AI-generated response
def get_ai_response(prompt, context):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"{context}\n\nUser: {prompt}\nAI:")
    return response.text if response else "Error generating response."

# Process Research Paper with Gemini AI
def process_research_paper(uploaded_file):
    if uploaded_file.name.endswith('.pdf'):
        text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith('.docx'):
        text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file format")
        return
    
    st.write("### Extracted Text (Preview)")
    st.text_area("", text[:1000] + "...", height=200)
    
    user_query = st.text_input("Ask a question about the document:")
    if user_query:
        with st.spinner("Generating AI response..."):
            response = get_ai_response(user_query, text)
            st.write("### AI Response:")
            st.success(response)

# Main Function
def main():
    st.title("Advanced Document Analyzer with Google Gemini AI")
    option = st.sidebar.selectbox("Choose a scenario", ["Price List Analyzer", "Research Paper Simplifier", "Resume Matcher for Hiring"])
    
    if option == "Price List Analyzer":
        uploaded_files = st.file_uploader("Upload price lists (CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=True)
        if uploaded_files:
            st.write("### Uploaded Price Lists")
            for file in uploaded_files:
                st.write(file.name)
    
    elif option == "Research Paper Simplifier":
        uploaded_file = st.file_uploader("Upload research paper (PDF or DOCX)", type=["pdf", "docx"])
        if uploaded_file:
            process_research_paper(uploaded_file)
    
    elif option == "Resume Matcher for Hiring":
        st.write("Resume Matching functionality is under development.")
    
if _name_ == "_main_":
    main()

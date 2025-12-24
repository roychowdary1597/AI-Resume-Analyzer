import streamlit as st
import zipfile
import os
import io
import json
import pandas as pd
from typing import TypedDict, List

from PyPDF2 import PdfReader
from docx import Document
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# --------------------------------------------------
# ENV SETUP
# --------------------------------------------------
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("gemini")

# --------------------------------------------------
# STREAMLIT CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

st.title("AI-Powered Resume Analyzer & CSV Generator")
st.caption("Upload a ZIP file containing resumes (PDF / DOCX)")

# --------------------------------------------------
# TYPEDDICT SCHEMA (TYPE SAFETY ONLY)
# --------------------------------------------------
class ResumeSchema(TypedDict):
    name: str
    email: str
    phone: str
    skills: List[str]
    experience_summary: str
    education: str
    linkedin: str
    github: str

# --------------------------------------------------
# JSON OUTPUT PARSER
# --------------------------------------------------
parser = JsonOutputParser()

# --------------------------------------------------
# PROMPT TEMPLATE
# --------------------------------------------------
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an AI resume analyzer.

Extract the following fields from the resume text and return ONLY valid JSON.
If a field is missing, return an empty string.
Skills must be a list of strings.

JSON format:
{{
  "name": "",
  "email": "",
  "phone": "",
  "skills": [],
  "experience_summary": "",
  "education": "",
  "linkedin": "",
  "github": ""
}}
"""
        ),
        ("human", "{resume_text}")
    ]
)

# --------------------------------------------------
# LLM
# --------------------------------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

chain = prompt | llm | parser

# --------------------------------------------------
# FILE TEXT EXTRACTION
# --------------------------------------------------
def extract_pdf_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def extract_docx_text(file):
    doc = Document(file)
    return "\n".join(p.text for p in doc.paragraphs)

# --------------------------------------------------
# ZIP PROCESSOR
# --------------------------------------------------
def process_zip(zip_file):
    extracted_data: List[ResumeSchema] = []

    with zipfile.ZipFile(zip_file) as z:
        for file_name in z.namelist():
            if file_name.lower().endswith((".pdf", ".docx")):
                with z.open(file_name) as f:

                    if file_name.lower().endswith(".pdf"):
                        text = extract_pdf_text(f)
                    else:
                        text = extract_docx_text(io.BytesIO(f.read()))

                    if not text.strip():
                        continue

                    try:
                        result = chain.invoke({"resume_text": text})

                        # Ensure keys exist (TypedDict safety)
                        structured: ResumeSchema = {
                            "name": result.get("name", ""),
                            "email": result.get("email", ""),
                            "phone": result.get("phone", ""),
                            "skills": result.get("skills", []),
                            "experience_summary": result.get("experience_summary", ""),
                            "education": result.get("education", ""),
                            "linkedin": result.get("linkedin", ""),
                            "github": result.get("github", "")
                        }

                        extracted_data.append(structured)

                    except Exception as e:
                        st.warning(f"Failed to parse {file_name}: {e}")

    return extracted_data

# --------------------------------------------------
# UI
# --------------------------------------------------
uploaded_zip = st.file_uploader(
    "Upload ZIP file containing resumes",
    type=["zip"]
)

if uploaded_zip:
    if st.button("Analyze Resumes"):
        with st.spinner("Processing resumes..."):
            results = process_zip(uploaded_zip)

        if results:
            df = pd.DataFrame(results)

            st.success("Resume analysis completed successfully")
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="resume_analysis.csv",
                mime="text/csv"
            )
        else:
            st.warning("No valid resumes found in the ZIP file")

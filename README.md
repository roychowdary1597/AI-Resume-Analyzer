# AI-Powered Resume Analyzer & CSV Generator

An end-to-end **LLM-powered resume analysis system** that automatically processes bulk resumes (PDF/DOCX) from a ZIP file, extracts structured candidate information, and generates a downloadable CSV file using **LangChain**, **Google Gemini**, and **Streamlit**.

---

## 🚀 Project Overview

Recruiters and HR teams often receive resumes in bulk, typically as compressed ZIP files containing multiple PDF or DOCX resumes. Manually reviewing and extracting key information from each resume is:

- Time-consuming  
- Repetitive  
- Error-prone  
- Inconsistent due to varied formats  

This project automates resume understanding and structured information extraction using **Large Language Models (LLMs)** and enforces a consistent schema for CSV-based analysis.

---

## ✨ Key Features

- Upload a ZIP file containing multiple resumes  
- Supports **PDF** and **DOCX** formats  
- Automatic resume text extraction  
- LLM-based structured data extraction  
- Uses **TypedDict + JsonOutputParser** (no Pydantic)  
- Aggregates all resumes into a single CSV file  
- Download CSV directly from the Streamlit UI  

---

## 🧩 Extracted Fields

Each resume is converted into structured data with the following fields:

- `name`
- `email`
- `phone`
- `skills` (list of strings)
- `experience_summary`
- `education`
- `linkedin`
- `github`

---

## 🏗️ System Architecture

ZIP Upload (Streamlit)
↓
PDF / DOCX Text Extraction
↓
Prompt-Driven LLM Processing (LangChain)
↓
Structured JSON Output
↓
CSV Aggregation
↓
Download via Streamlit UI

markdown
Copy code

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** – UI & file handling
- **LangChain (LCEL)** – LLM orchestration
- **Google Gemini (gemini-1.0-pro)** – Resume understanding
- **JsonOutputParser** – Structured output enforcement
- **TypedDict** – Static schema typing
- **PyPDF2** – PDF text extraction
- **python-docx** – DOCX text extraction
- **Pandas** – CSV generation

---













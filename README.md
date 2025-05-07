# 📄 ATS Resume Analyzer

A smart, AI-powered web application that evaluates resumes against job descriptions using both cloud-based (Google Gemini API) and local (Ollama LLMs) models. This tool helps job seekers assess how well their resume aligns with a target role and receive actionable insights to improve their chances in Applicant Tracking Systems (ATS).

---

## 🔍 Features

✅ Analyze resume content against a job description  
✅ Suggest missing skills, tools, or certifications  
✅ Provide a match percentage score with reasoning  
✅ Supports both cloud-based (Gemini 1.5/2.0) and local LLM (Ollama) options  
✅ Extracts and cleans resume content from PDF uploads  

---

## 🧱 Project Versions

### 1. **Gemini Vision Resume Analyzer**
- Uses **Gemini 1.5 Pro with Vision API**.
- Converts PDF resumes into images.
- Sends visual content to Gemini for semantic analysis.
- Supports three AI prompts for:
  - Resume Strengths & Gaps
  - Skill Recommendations
  - Match Score Estimation

### 2. **Local LLM with Ollama**
- Uses local models like `qwen2.5-coder:7b` via the `ollama` CLI.
- Extracts text from PDFs using PyPDF2.
- Fully offline and cost-effective.
- Ideal for developers who prefer privacy or open-source solutions.

### 3. **Gemini 2.0 Flash Text Analyzer**
- Lightweight and fast version.
- Purely text-based using Gemini 2.0 Flash (or other Gemini models).
- Extracts resume text and combines with job description in prompt.
- Simple, scalable, and minimal dependencies.

---


import streamlit as st
import subprocess
import PyPDF2
import re

# --- Helper: Clean non-ASCII characters (optional, prevents emoji issues) ---
def clean_text(text):
    return re.sub(r'[^\x00-\x7F]+', ' ', text)

# --- PDF text extraction ---
def extract_pdf_text(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return clean_text(text)
    except Exception as e:
        st.error(f"❌ Error reading PDF: {e}")
        return None

# --- Run prompt through Ollama locally ---
def query_ollama(prompt):
    try:
        result = subprocess.run(
            ['ollama', 'run', 'qwen2.5-coder:7b'],
            input=prompt,
            text=True,
            capture_output=True,
            encoding='utf-8',   # ✅ Force UTF-8 to fix Unicode errors
            errors='replace'    # ✅ Avoid crash if any bad char
        )
        return result.stdout
    except Exception as e:
        return f"❌ Error running Ollama: {e}"

# --- Prompts ---
prompt_analysis = """
You are an experienced technical human resources recruiter. 
Your job is to analyze resumes and compare them to job descriptions. 
Evaluate how well the resume matches the job description provided. 
Highlight the strengths, relevant experiences, and technical skills that align with the job. 
Also, mention any noticeable gaps or missing skills.
"""

prompt_improve = """
You are a career development advisor and resume expert. 
Analyze the candidate's resume against the provided job description and suggest how they can improve their skill set. 
Highlight missing technical skills, certifications, tools, or relevant experience that would strengthen their resume. 
Offer practical, targeted recommendations for improvement in bullet-point format.
"""

prompt_match = """
You are an AI assistant used in an Applicant Tracking System (ATS). 
Compare the resume to the job description and provide a percentage match score (0% to 100%) based on skills, experience, and keyword relevance. 
Then briefly explain the reasoning behind the score, including what matched well and what was missing.
"""

# --- Streamlit App UI ---
st.set_page_config(page_title="ATS Resume Expert")
st.title("📄 ATS Resume Analyzer")
st.markdown("Upload your resume and paste a job description to analyze how well they match.")

job_description = st.text_area("📝 Job Description:")
upload_file = st.file_uploader("📤 Upload Your Resume (PDF)", type=["pdf"])

submit1 = st.button("🧠 Analyze Resume")
submit2 = st.button("💡 Suggest Skill Improvements")
submit3 = st.button("📊 Get Match Percentage")

# --- Main Logic ---
if upload_file:
    resume_text = extract_pdf_text(upload_file)

    if resume_text:
        if submit1:
            prompt = f"{prompt_analysis}\n\nJob Description:\n{job_description}\n\nResume:\n{resume_text}"
            st.info("Analyzing resume...")
            response = query_ollama(prompt)
            st.subheader("📄 Resume Analysis")
            st.write(response)

        elif submit2:
            prompt = f"{prompt_improve}\n\nJob Description:\n{job_description}\n\nResume:\n{resume_text}"
            st.info("Suggesting improvements...")
            response = query_ollama(prompt)
            st.subheader("🛠️ Skill Improvement Suggestions")
            st.write(response)

        elif submit3:
            prompt = f"{prompt_match}\n\nJob Description:\n{job_description}\n\nResume:\n{resume_text}"
            st.info("Calculating match percentage...")
            response = query_ollama(prompt)
            st.subheader("📊 Match Percentage")
            st.write(response)
else:
    st.info("📌 Upload your resume to begin.")

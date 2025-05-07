import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Extract text from PDF ---
def extract_text_from_pdf(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# --- Gemini Call ---
def get_gemini_response(prompt: str):
    try:
        model = genai.GenerativeModel("models/gemini-2.0-flash")  # Use available model like text-bison
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- Prompt Templates ---
input_prompt1 = "You are a professional ATS system. Analyze this resume:\n"
input_prompt2 = "Act as a career advisor. Suggest skills based on this job description:\n"
input_prompt3 = "Rate the resume match percentage against the job role. Return in %.\n"

# --- Streamlit UI ---
st.title("🧠 Smart Resume Evaluator")
input_text = st.text_area("📌 Paste the Job Description")
upload_file = st.file_uploader("📄 Upload Your Resume (PDF)", type="pdf")

submit1 = st.button("📄 Resume Analysis")
submit2 = st.button("🛠️ Skill Suggestions")
submit3 = st.button("📊 Match Percentage")

# --- Logic ---
if upload_file is not None:
    resume_text = extract_text_from_pdf(upload_file)

    if resume_text:
        if submit1:
            prompt = input_prompt1 + f"\n\nJob Description:\n{input_text}\n\nResume:\n{resume_text}"
            st.subheader("📄 Resume Analysis")
            st.write(get_gemini_response(prompt))

        elif submit2:
            prompt = input_prompt2 + f"\n\nJob Description:\n{input_text}\n\nResume:\n{resume_text}"
            st.subheader("🛠️ Skill Suggestions")
            st.write(get_gemini_response(prompt))

        elif submit3:
            prompt = input_prompt3 + f"\n\nJob Description:\n{input_text}\n\nResume:\n{resume_text}"
            st.subheader("📊 Match Percentage")
            st.write(get_gemini_response(prompt))
    else:
        st.warning("❗ Couldn't extract text from the uploaded PDF.")
else:
    st.info("Please upload a resume and enter the job description.")

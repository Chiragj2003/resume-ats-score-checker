import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import base64
import io
from PIL import Image
from pdf2image import convert_from_bytes

# --- Load API key ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Convert PDF (first page) to image bytes ---
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            images = convert_from_bytes(uploaded_file.read())
            first_page = images[0]
            img_byte_arr = io.BytesIO()
            first_page.save(img_byte_arr, format='JPEG')
            img_bytes = img_byte_arr.getvalue()
            return [{
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_bytes).decode("utf-8")
            }]
        except Exception as e:
            st.error(f"❌ Error processing PDF: {e}")
            return None
    else:
        st.warning("No file uploaded.")
        return None

# --- Gemini Vision Function ---
def get_gemini_responses(pdf_content, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content([pdf_content[0], prompt])
        return response.text
    except Exception as e:
        st.error(f"❌ Gemini API error: {e}")
        return None

# --- Prompts ---
input_prompt1 = """
You are an experienced technical human resources recruiter. 
Your job is to analyze resumes and compare them to job descriptions. 
Evaluate how well the resume matches the job description provided. 
Highlight the strengths, relevant experiences, and technical skills that align with the job. 
Also, mention any noticeable gaps or missing skills.
"""

input_prompt2 = """
You are a career development advisor and resume expert. 
Analyze the candidate's resume against the provided job description and suggest how they can improve their skill set. 
Highlight missing technical skills, certifications, tools, or relevant experience that would strengthen their resume. 
Offer practical, targeted recommendations for improvement in bullet-point format.
"""

input_prompt3 = """
You are an AI assistant used in an Applicant Tracking System (ATS). 
Compare the resume to the job description and provide a percentage match score (0% to 100%) based on skills, experience, and keyword relevance. 
Then briefly explain the reasoning behind the score, including what matched well and what was missing.
"""

# --- Streamlit App UI ---
st.set_page_config(page_title="ATS Resume Expert")
st.title("📄 ATS Resume Analyzer")
st.markdown("Upload your resume (PDF) and provide a job description to analyze its match.")

input_text = st.text_area("📝 Job Description:")
upload_file = st.file_uploader("📤 Upload Your Resume (PDF)", type=["pdf"])

if upload_file is not None:
    st.success("✅ PDF uploaded successfully")

submit1 = st.button("🧠 Analyze Resume")
submit2 = st.button("💡 Suggest Skill Improvements")
submit3 = st.button("📊 Get Match Percentage")

# --- Button Logic ---
if upload_file is not None:
    pdf_content = input_pdf_setup(upload_file)

    if pdf_content:
        if submit1:
            response = get_gemini_responses(pdf_content, input_prompt1 + "\n\nJob Description:\n" + input_text)
            st.subheader("📄 Resume Analysis")
            st.write(response)

        elif submit2:
            response = get_gemini_responses(pdf_content, input_prompt2 + "\n\nJob Description:\n" + input_text)
            st.subheader("🛠️ Skill Improvement Suggestions")
            st.write(response)

        elif submit3:
            response = get_gemini_responses(pdf_content, input_prompt3 + "\n\nJob Description:\n" + input_text)
            st.subheader("📊 Match Percentage")
            st.write(response)

else:
    st.info("📌 Upload a PDF resume to get started.")

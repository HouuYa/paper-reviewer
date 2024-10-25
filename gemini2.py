import streamlit as st
import google.generativeai as genai
import os
from PyPDF2 import PdfReader
import io

def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

st.title('AI Research Paper Review Team')

st.header('Team Structure')
st.write("1. Sam (AI PhD): Explains paper content in simple terms")
st.write("2. Jenny (AI & Education PhD): Simplifies and expands on Sam's draft")
st.write("3. Will (Team Leader): Finalizes the report")

# PDF 파일 업로드
uploaded_file = st.file_uploader("PDF 파일을 선택하거나 여기에 드래그하세요", type="pdf")

# Gemini API 키 입력
api_key = st.text_input('Gemini API 키를 입력하세요:', type='password')

if uploaded_file is not None and api_key:
    # API 키 설정
    os.environ['GOOGLE_API_KEY'] = api_key
    genai.configure(api_key=api_key)

    # PDF에서 텍스트 추출
    pdf_text = extract_text_from_pdf(uploaded_file)

    # Gemini 모델 설정
    model = genai.GenerativeModel('gemini-pro')

    # Sam의 분석
    st.subheader("Sam's Initial Analysis")
    sam_prompt = f"""You are Sam, an AI PhD graduate. Analyze the following research paper:

    {pdf_text}

    Provide an initial draft explaining the paper's content in simpler terms. Focus on key points, methodologies, and findings."""

    sam_response = model.generate_content(sam_prompt)
    st.write(sam_response.text)

    # Jenny의 리뷰
    st.subheader("Jenny's Review and Enhancement")
    jenny_prompt = f"""You are Jenny, with PhDs in AI and Education. Review Sam's analysis:

    {sam_response.text}

    Simplify the language further, add educational context, and expand on areas needing more explanation."""

    jenny_response = model.generate_content(jenny_prompt)
    st.write(jenny_response.text)

    # Will의 최종 리뷰
    st.subheader("Will's Final Review and Compilation")
    will_prompt = f"""You are Will, the team leader. Review both Sam and Jenny's contributions:

    Sam's analysis: {sam_response.text}

    Jenny's review: {jenny_response.text}

    Create a final report covering all key points, ensuring accuracy and readability. Structure the report as follows:
    1. Executive Summary
    2. Introduction to the Research Topic
    3. Key Findings and Methodologies
    4. Simplified Explanation of Complex Concepts
    5. Real-world Applications and Implications
    6. Conclusion and Future Research Directions"""

    will_response = model.generate_content(will_prompt)
    st.write(will_response.text)

elif uploaded_file is None:
    st.write('PDF 파일을 업로드해주세요.')
elif not api_key:
    st.write('API 키를 입력해주세요.')

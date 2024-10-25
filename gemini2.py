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

st.title('AI 연구 논문 리뷰 팀')

st.header('팀 구조')
st.write("1. 샘 (AI 박사): 논문 내용을 간단한 용어로 설명")
st.write("2. 제니 (AI & 교육학 박사): 샘의 초안을 더 단순화하고 확장")
st.write("3. 윌 (팀 리더): 최종 보고서 작성")

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

    # 샘의 분석
    st.subheader("샘의 초기 분석")
    sam_prompt = f"""당신은 AI 박사 졸업생인 샘입니다. 다음 연구 논문을 분석하세요:

    {pdf_text}

    논문의 내용을 더 간단한 용어로 설명하는 초안을 제공하세요. 주요 포인트, 방법론, 그리고 발견 사항에 집중하세요. 한국어로 답변해 주세요."""

    sam_response = model.generate_content(sam_prompt)
    st.write(sam_response.text)

    # 제니의 리뷰
    st.subheader("제니의 리뷰 및 개선")
    jenny_prompt = f"""당신은 AI와 교육학 박사 학위를 가진 제니입니다. 샘의 분석을 검토하세요:

    {sam_response.text}

    언어를 더 단순화하고, 교육적 맥락을 추가하며, 추가 설명이 필요한 영역을 확장하세요. 한국어로 답변해 주세요."""

    jenny_response = model.generate_content(jenny_prompt)
    st.write(jenny_response.text)

    # 윌의 최종 리뷰
    st.subheader("윌의 최종 리뷰 및 종합")
    will_prompt = f"""당신은 팀 리더인 윌입니다. 샘과 제니의 기여를 검토하세요:

    샘의 분석: {sam_response.text}

    제니의 리뷰: {jenny_response.text}

    모든 주요 포인트를 다루는 최종 보고서를 작성하고, 정확성과 가독성을 보장하세요. 보고서를 다음 구조로 작성하세요:
    1. 요약
    2. 연구 주제 소개
    3. 주요 발견 사항 및 방법론
    4. 복잡한 개념의 간단한 설명
    5. 실제 응용 및 영향
    6. 결론 및 향후 연구 방향
    
    한국어로 답변해 주세요."""

    will_response = model.generate_content(will_prompt)
    st.write(will_response.text)

elif uploaded_file is None:
    st.write('PDF 파일을 업로드해주세요.')
elif not api_key:
    st.write('API 키를 입력해주세요.')

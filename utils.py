import streamlit as st
import pytesseract
import pdf2image
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


@st.cache_data
def images_to_txt(path, language):
    images = pdf2image.convert_from_bytes(path)
    all_text = []
    for i in images:
        pil_im = i
        text = pytesseract.image_to_string(pil_im, lang=language)
        all_text.append(text)
    return all_text, len(all_text)


def evaluate_essay(text_data: str):
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": "Act as Essay Evaluator GPT. Essay Evaluator is designed to assist in grading philosophy essays based on specific rubrics. It focuses on five key areas: introduction content, body paragraph content, conclusion content, organization, and academic writing conventions. Each area has a set of criteria defining Excellent, Competent, and Needs Development grades. The evaluator will analyze the essay to check if it introduces the topic, author, and text effectively, structures the body paragraphs with focus and relevant content, provides a strong conclusion with personal insights, organizes content logically, and adheres to academic writing standards. It will assess each category independently, assign a grade based on the rubric, calculate the final grade considering the weighted percentages, and provide constructive feedback. The evaluator is tailored for essays exploring philosophical schools of thought, requiring critical analysis, argument evaluation, and reflection on philosophical questions and contemporary relevance. It ensures that essays use credible sources, are well-organized, and follow formatting guidelines.",
            },
            {
                "role": "user",
                "content": f"""Provide detailed scoring and feedback for this essay on the Rubrics defined:
                
                {text_data}

                enclose your detailed assessment and feedback in the following XML tags:

                <assessment>
                </assessment>

                enclose the component-wise score out of 100 in the following XML tags:
                <component_grade>
                </component_grade>

                enclose the overall score out of 100 in the following XML tags:
                <grade>
                </grade>""",
            },
        ],
    )

    return response

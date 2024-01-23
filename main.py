import streamlit as st
from openai import OpenAI
from utils import images_to_txt
import re

st.title("Essay Evaluator")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

file = st.file_uploader("Upload your essay")
if file:
    path = file.read()
    texts, numPages = images_to_txt(path, "eng")
    text_data = "\n\n".join(texts)
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

    full_response = response.choices[0].message.content.replace("\n", "")  # type: ignore

    feedback = None
    score = None
    question = None

    m = re.search(r"<assessment>(.*)</assessment>", full_response)
    if m:
        feedback = m.group(1)
    m = re.search(r"<component_grade>(.*)</component_grade>", full_response)
    if m:
        score = m.group(1)
    m = re.search(r"<grade>(.*)</grade>", full_response)
    if m:
        question = m.group(1)

    if feedback is not None and score is not None:
        st.markdown("# Score - \n\n " + score)
        st.markdown("## Feedback - \n\n " + feedback)
        if question:
            st.markdown("## Next Question - \n\n " + question)
    else:
        st.write(full_response)
        st.write("Gpt produced incorrect response structure")

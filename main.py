import streamlit as st
from utils import images_to_txt, evaluate_essay
import re

st.title("Essay Evaluator")


file = st.file_uploader("Upload your essay")
if file:
    path = file.read()
    texts, numPages = images_to_txt(path, "eng")
    text_data = "\n\n".join(texts)

    response = evaluate_essay(text_data)
    full_response = response.choices[0].message.content.replace("\n", "")  # type: ignore

    assessment = None
    c_grade = None
    grade = None

    m = re.search(r"<assessment>(.*)</assessment>", full_response)
    if m:
        assessment = m.group(1)
    m = re.search(r"<component_grade>(.*)</component_grade>", full_response)
    if m:
        c_score = m.group(1)
    m = re.search(r"<grade>(.*)</grade>", full_response)
    if m:
        grade = m.group(1)

    if assessment is not None and grade is not None:
        st.markdown("# Grade - \n\n " + grade)
        st.markdown("## Assessment- \n\n " + assessment)
        if c_grade is not None:
            st.markdown("## component_grade- \n\n " + c_grade)
    else:
        st.write(full_response)
        st.write("Gpt produced incorrect response structure")

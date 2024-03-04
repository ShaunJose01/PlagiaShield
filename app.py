import streamlit as st
import streamlit as st
from PIL import Image as pl
import matplotlib.pyplot as plt
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import docx2txt
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import json



# Load Lottie animation
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

head, mid, anim = st.columns([40, 20, 40])

with head:
    st.title("PlagiaShield ")

with anim:
    with open(r"C:\Users\shaun\OneDrive\Desktop\NLP\anima.json") as f:
        animation_data = json.load(f)
        st_lottie(animation_data)

with st.sidebar:
    sel = option_menu(
        menu_title='Main Menu',
        options=['Login', 'Home'],
        icons=['check', 'check']
    )

uploaded_file1 = st.file_uploader("Select document 1", type="docx")
uploaded_file2 = st.file_uploader("Select document 2", type="docx")

if uploaded_file1 and uploaded_file2:  # Check if files are uploaded
    doc1_text = docx2txt.process(uploaded_file1)
    doc2_text = docx2txt.process(uploaded_file2)

    # Combine the text into a list
    content = [doc1_text, doc2_text]

    # Initialize CountVectorizer and transform the content
    cv = CountVectorizer()
    matrix = cv.fit_transform(content)

    # Compute cosine similarity
    similarity_scores = cosine_similarity(matrix)
    res = similarity_scores[0][1]

    if res > 0.8:
        st.error(f"Similarity between the documents: {round(res, 3)}")
        st.warning("High level of similarity detected. Potential plagiarism.")
        st.write('NOTE:')
        st.write("Tips to improve: Try paraphrasing the content or citing sources properly.")
        st.write("Educational message: Plagiarism can have serious consequences. Practice academic integrity.")

    elif res < 0.5:
        st.success(f"Similarity between the documents: {round(res, 3)}")
        st.info("Low level of similarity detected. Likely no plagiarism.")
        st.write('NOTE:')
        st.write("Educational message: Understanding proper citation and paraphrasing is crucial for academic honesty.")

    elif res >= 0.5 and res <= 0.8:
        st.info(f"Similarity between the documents: {round(res, 3)}")
        st.info("Moderate level of similarity detected. Check for potential plagiarism.")
        st.write('NOTE:')
        st.write("Tips to improve: Double-check the sources and ensure proper citation.")

else:
    st.warning("Please upload both documents to check for similarity.")

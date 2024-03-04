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

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Predefined user dictionary (for demonstration purposes)
users = {
    'user1': '1',
    'Shaun01': 'password2'
}

def login(username, password):
    if username in users and users[username] == password:
        return True
    return False

def login_section():
    st.header("Login")
    login_username = st.text_input("Username")
    login_password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(login_username, login_password):
            st.success("Login successful!")
            # Proceed to your main app or display content after login
        else:
            st.error("Invalid username or password. Please try again.")
            # Check if user exists, if not, register
            if login_username not in users:
                st.warning("New user! You've been registered.")
                users[login_username] = login_password

def resume_checker():
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

# Your Streamlit app
def main():
    head, mid, anim = st.columns([40, 10, 50])
    with head:
        st.title("PlagiaShield")
    with anim:
        with open(r"C:\Users\shaun\OneDrive\Desktop\NLP\anima.json") as f:
            animation_data = json.load(f)
            st_lottie(animation_data) 
    
    with st.sidebar:
        selected_menu = st.selectbox(
            "Main Menu",
            options=['Login', 'Home']
        )
    
    if selected_menu == 'Login':
        login_section()  # Display login section
    elif selected_menu == 'Home':
        resume_checker()  # Display resume checker section

if __name__ == "__main__":
    main()  # Run the Streamlit app

import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@st.cache_data
def load_data():
    df = pd.read_csv("mon_cours.csv", sep=";", encoding="utf-8")
    df.dropna(inplace=True)
    return df

def get_best_answer(question, df):
    vectorizer = TfidfVectorizer()
    corpus = df["question"].tolist() + [question]
    tfidf = vectorizer.fit_transform(corpus)
    scores = cosine_similarity(tfidf[-1], tfidf[:-1])
    best_idx = scores.argmax()
    return df["reponse"].iloc[best_idx]

st.set_page_config(page_title="Chatbot 1MCVA", layout="centered")

# ✅ Correction : remplacer 'body' par '.stApp' pour Streamlit
st.markdown(
    """
    <style>
        .stApp {
            background-color: #3374ff;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='color:white;'>🤖 Explorez le Commerce avec BotPro</h1>", unsafe_allow_html=True)
st.write("Pose ta question sur le cours 👇")

df = load_data()
user_question = st.text_input("Ta question ici :")

# ➕ À commenter si tu ne veux plus afficher le tableau brut
# st.write(df.head())

if user_question:
    answer = get_best_answer(user_question, df)
    st.success(f"Réponse : {answer}")# Ajout de commentaire pour test de commit

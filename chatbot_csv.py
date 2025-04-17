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

from PIL import Image

# Charger le logo
logo = Image.open("robot.png")

# Afficher le logo à gauche
st.columns([0.2, 0.8])[0].image(logo, width=100)

st.markdown("""
    <style>
        .stApp {
            background-color: #f0f2f6;
        }
        .main-title {
            color: #1f4e79;
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            padding: 20px;
        }
        .sub-title {
            color: #444;
            font-size: 1.2em;
            text-align: center;
            margin-bottom: 30px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🤖 Bienvenue sur BotPro – Le chatbot du cours de commerce</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Pose une question sur le cours et reçois une réponse instantanée !</div>", unsafe_allow_html=True)

# 🎬 Page d'accueil : bouton pour démarrer
if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    if st.button("🚀 Commencer le chatbot"):
        st.session_state.started = True
    st.stop()
    
# ✅ Correction : remplacer 'body' par '.stApp' pour Streamlit
st.markdown(
    """
    <style>
        .stApp {
            background-color: #4f5355;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='color:white;'>🤖 Explorez le Commerce avec BotPro</h1>", unsafe_allow_html=True)
st.write("Pose ta question 👇")

df = load_data()
user_question = st.text_input("Ta question ici :")

# ➕ À commenter si tu ne veux plus afficher le tableau brut
# st.write(df.head())

if user_question:
    answer = get_best_answer(user_question, df)
    st.success(f"Réponse : {answer}")# Ajout de commentaire pour test de commit
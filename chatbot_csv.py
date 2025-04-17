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
            color: #121213;
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            padding: 20px;
        }
        .sub-title {
            color: #e8f60b;
            font-size: 1.2em;
            text-align: center;
            margin-bottom: 30px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🤖 Bienvenue sur BotPro – Le chatbot des cours de commerce</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'> </div>", unsafe_allow_html=True)

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

st.markdown("<h1 style='color:white;'> Explorez le Commerce avec BotPro</h1>", unsafe_allow_html=True)
st.write("BotPro est un chatbot conçu pour répondre à vos questions sur les cours des Métiers du Commerce et de la Vente. Posez votre question ci-dessous et obtenez une réponse instantanée !")

df = load_data()
MOTS_INDECENTS = [
    "merde", "putain", "con", "connard", "salop", "enculé", "bordel", "nique", "ta mère", "fdp"
]

def contient_mot_indescent(texte: str) -> bool:
    texte = texte.lower()
    return any(mot in texte for mot in MOTS_INDECENTS)

def masquer_insultes(texte: str) -> str:
    for mot in MOTS_INDECENTS:
        if mot in texte.lower():
            texte = texte.replace(mot, mot[0] + '*' * (len(mot) - 1))
    return texte

user_question = st.text_input("Ta question ici 👇:")

if user_question:
    if contient_mot_indescent(user_question):
        question_masquee = masquer_insultes(user_question)
        reponse = (
            f"🤖🚫 <strong>Ce langage n’est pas approprié</strong> dans : “{question_masquee}”.<br>"
            f"Merci de rester respectueux 🙏."
        )
    else:
        reponse = get_best_answer(user_question, df)
        reponse = f"🤖😊 <strong>Réponse :</strong> {reponse}"
else:
    reponse = "🤖🤔 J’attends ta question avec impatience !"

st.markdown(
    f'<div class="response-box">{reponse}</div>',
    unsafe_allow_html=True
)

# Footer avec message + lien Digipad
st.markdown(
    """
    <div style='text-align: center; font-size: 1em; color: white; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ccc;'>
        ✨ Crois en toi, révise avec le sourire 😄 et donne le meilleur de toi-même !<br>
        💪 Bon courage pour tes révisions !<br><br>
        👉 <a href="https://digipad.app/p/847630/15248ba9144b5" target="_blank" style="color:white; font-weight:bold;">
        Accède ici à ton Digipad 📚</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Signature personnalisée en bas à droite
st.markdown(
    """
    <div style='text-align: right; font-size: 0.9em; color: white; margin-top: 30px;'>
        Réalisé par <strong>Sarah Ouziel</strong> © 2025
    </div>
    """,
    unsafe_allow_html=True
)
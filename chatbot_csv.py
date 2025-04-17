import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import random

st.set_page_config(page_title="Chatbot 1MCVA", layout="centered")

# Chargement du logo
logo = Image.open("robot.png")
st.columns([0.2, 0.8])[0].image(logo, width=100)

# Styles
st.markdown("""
    <style>
        .stApp {
            background-color: #4f5355;
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
        .response-box {
            background-color: #ffffff;
            color: #000000;
            padding: 10px;
            border-radius: 10px;
            border: 2px solid #3374ff;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🤖 Bienvenue sur BotPro – Le chatbot des cours de commerce</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Pose une question ou fais un jeu pédagogique 🎨</div>", unsafe_allow_html=True)

# Étape 1 : bouton de démarrage
if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.markdown("## 👋 Bienvenue sur BotPro !")
    st.markdown("Clique ci-dessous pour accéder aux activités 👇")
    if st.button("🚀 Commencer le chatbot"):
        st.session_state.started = True
    st.stop()

# Menu déroulant aligné à droite après démarrage
with st.container():
    st.markdown(
        """
        <div style='display: flex; justify-content: flex-end;'>
            <div style='width: 250px;'>
        """,
        unsafe_allow_html=True
    )
    choix = st.selectbox("📌", [
        "🤖 Chatbot",
        "🎯 Quiz de révision",
        "🎮 Jeu des 5 mots",
    ])
    st.markdown("</div></div>", unsafe_allow_html=True)

# Data et fonctions
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

MOTS_INDECENTS = ["merde", "putain", "con", "connard", "salop", "enculé", "bordel", "nique", "ta mère", "fdp"]

def contient_mot_indescent(texte: str) -> bool:
    return any(mot in texte.lower() for mot in MOTS_INDECENTS)

def masquer_insultes(texte: str) -> str:
    for mot in MOTS_INDECENTS:
        if mot in texte.lower():
            texte = texte.replace(mot, mot[0] + '*' * (len(mot) - 1))
    return texte

# 🤖 Chatbot
if choix == "🤖 Chatbot":
    st.markdown("<h1 style='color:white;'> Explorez le Commerce avec BotPro</h1>", unsafe_allow_html=True)
    st.write("Pose ta question sur le cours 👇")
    df = load_data()
    user_question = st.text_input("Ta question ici :")
    if user_question:
        if contient_mot_indescent(user_question):
            question_masquee = masquer_insultes(user_question)
            reponse = f"🤖🚫 <strong>Ce langage n’est pas approprié</strong> dans : “{question_masquee}”.<br>Merci de rester respectueux 🙏."
        else:
            reponse = get_best_answer(user_question, df)
            reponse = f"🤖😊 <strong>Réponse :</strong> {reponse}"
    else:
        reponse = "🤖🤔 J’attends ta question avec impatience !"
    st.markdown(f'<div class="response-box">{reponse}</div>', unsafe_allow_html=True)

# 🎯 Quiz (placeholder à compléter)
elif choix == "🎯 Quiz de révision":
    st.markdown("### 📘 Prochainement : Quiz pédagogique à choix multiples !")

# 🎮 Jeu des 5 mots
elif choix == "🎮 Jeu des 5 mots":
    st.header("🎯 Débloque les 5 mots du commerce")
    quiz_mots = [
        {"mot": "client", "question": "Qui achète un produit ou un service ?", "reponse": "client"},
        {"mot": "vendeur", "question": "Qui propose un produit ou un service au client ?", "reponse": "vendeur"},
        {"mot": "produit", "question": "Quel mot désigne un bien que l'on peut acheter ?", "reponse": "produit"},
        {"mot": "fidelité", "question": "Comment appelle-t-on le fait qu'un client revienne souvent ?", "reponse": "fidelité"},
        {"mot": "besoin", "question": "Que cherche à satisfaire un client avec un achat ?", "reponse": "besoin"},
    ]
    if "deverrouilles" not in st.session_state:
        st.session_state.deverrouilles = []
    for mot in quiz_mots:
        if mot["mot"] in st.session_state.deverrouilles:
            st.success(f"✅ {mot['mot'].capitalize()} débloqué !")
        else:
            reponse = st.text_input(mot["question"], key=mot["mot"])
            if reponse and reponse.lower().strip() == mot["reponse"]:
                st.session_state.deverrouilles.append(mot["mot"])
                st.success(f"🎉 Bravo, tu as débloqué : {mot['mot'].capitalize()} !")
                st.rerun()
    if len(st.session_state.deverrouilles) == len(quiz_mots):
        st.balloons()
        st.info("🎉 Tu as débloqué tous les mots du commerce ! Tu connais déjà bien le vocabulaire 👏")

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

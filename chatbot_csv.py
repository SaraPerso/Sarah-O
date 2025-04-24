import random
import io
import base64
import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import time
import os
import csv
from datetime import datetime

import os
import csv
from datetime import datetime
import streamlit as st

st.set_page_config(page_title="Chatbot LycéePro", layout="centered")

def init_fichier_visites():
    """Crée le fichier visites.csv s’il n’existe pas"""
    if not os.path.exists("visites.csv"):
        with open("visites.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date"])
        print("✅ Fichier visites.csv créé")

def enregistrer_visite():
    """Enregistre une nouvelle visite dans le fichier CSV"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("visites.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([now])
    print(f"✅ Visite enregistrée à {now}")

def total_visites():
    """Retourne le nombre total de visites enregistrées"""
    if not os.path.exists("visites.csv"):
        return 0
    with open("visites.csv", "r") as f:
        reader = csv.reader(f)
        return sum(1 for _ in reader) - 1  # -1 pour l’en-tête

# Initialisation du fichier
init_fichier_visites()

# Enregistrement de la visite
from datetime import timedelta

now = datetime.now()
if "last_visit" not in st.session_state:
    enregistrer_visite()
    st.session_state.last_visit = now
else:
    if now - st.session_state.last_visit > timedelta(hours=24):
        enregistrer_visite()
        st.session_state.last_visit = now

# Affichage du total
total = total_visites()

if total >= 300:
    st.toast("🥳 Déjà plus de 300 visites ! Merci !")

# Affichage du robot flottant sur la page d'accueil
def afficher_robot_flotant():
    with open("robot3.png", "rb") as img:
        encoded_robot = base64.b64encode(img.read()).decode()
    st.markdown("""
        <style>
            .floating-robot {
                position: fixed;
                bottom: 20px;
                right: 30px;
                width: 180px;
                animation: float 3s ease-in-out infinite;
                z-index: 100;
            }
            @keyframes float {
                0% { transform: translateY(0px); }
                50% { transform: translateY(-20px); }
                100% { transform: translateY(0px); }
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown(f"<img src='data:image/png;base64,{encoded_robot}' class='floating-robot'>", unsafe_allow_html=True)

# Utilisation dans chaque page
    afficher_robot_flotant()
    
# 🖼️ Logo et titre agrandi + aligné
col1, col2 = st.columns([0.15, 0.85])
with col1:
    st.image("robot-assistant.png", width=200)  # ← augmente ici
with col2:
    st.markdown("<h1 style='color:#121213; padding-top:40px;'> Bienvenue sur BotPro</h1>", unsafe_allow_html=True)

# Styles
st.markdown("""
    <style>
        .stApp {
            background-color: #a1a1a1; /* plus clair */
            transition: background 0.5s ease-in-out;
        }

        div.block-container {
            padding: 2rem 2rem 4rem 2rem;
        }

        h1, h2, h3, h4 {
            margin-top: 2rem;
            margin-bottom: 1rem;
        }

        .main-title {
            color: #121213;
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            padding: 15px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'> L’assistant virtuel pour les cours des Métiers du commerce et de la vente</div>", unsafe_allow_html=True)

# Étape 1 : bouton de démarrage     
if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.markdown("## 👋 Bienvenue sur BotPro !")
    st.markdown("Clique ci-dessous pour accéder aux activités 👇")
    afficher_robot_flotant()
    if st.button("🚀 C'est parti !"):
        st.session_state.started = True
        st.rerun()
    st.stop()

st.markdown("""
    <style>
    /* Agrandir la police et les zones des onglets */
    .stTabs [role="tab"] {
        font-size: 1.4rem !important;  /* Taille du texte : augmente la valeur pour encore plus grand */
        padding: 18px 36px !important; /* Taille de la zone cliquable */
        font-weight: bold !important;
        color: #222 !important;        /* Couleur du texte */
        border-radius: 10px 10px 0 0 !important;  /* Arrondi */
        background: #f4f4f4 !important; /* Couleur de fond des onglets */
        margin-right: 8px !important;
        min-width: 160px !important;   /* Largeur minimale pour chaque onglet */
    }
    .stTabs [role="tab"][aria-selected="true"] {
        background: #000000 !important; /* Onglet actif, couleur */
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Onglets de navigation
onglets = st.tabs(["🤖 Chatbot", "🎯 Quiz de révision", "🎮 Jeu des 5 mots", "📚 Digipad"])

# Data et fonctions
@st.cache_data(show_spinner="📦 Chargement des questions...")
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

MOTS_INDECENTS = ["merde", "putain", "con", "connard", "salop", "enculé", "bordel", "nique", "pute", "ta mère", "fdp"]

import re

def contient_mot_indescent(texte: str) -> bool:
    pattern = r'\b(?:' + '|'.join(re.escape(mot) for mot in MOTS_INDECENTS) + r')\b'
    return re.search(pattern, texte.lower(), re.IGNORECASE) is not None

def masquer_insultes(texte: str) -> str:
    for mot in MOTS_INDECENTS:
        pattern = fr'\b{re.escape(mot)}\b'
        remplacement = mot[0] + '*' * (len(mot) - 1)
        texte = re.sub(pattern, remplacement, texte, flags=re.IGNORECASE)
    return texte

# 🤖 Chatbot
with onglets[0]:
    st.markdown("<h1 style='color:white;'> Explorez le Commerce avec BotPro</h1>", unsafe_allow_html=True)
    st.write("Pose ta question sur le cours 👇")
    df = load_data()
    user_question = st.text_input("Ta question ici :")
    if user_question:
        if contient_mot_indescent(user_question):
            question_masquee = masquer_insultes(user_question)
            reponse = f"🚫 <strong>Ce langage n’est pas approprié</strong> dans : “{question_masquee}”.<br>Merci de rester respectueux 🙏."
        else:
            reponse = get_best_answer(user_question, df)
            reponse = f"😊 <strong>Réponse :</strong> {reponse}"
    else:
        reponse = "🤔 J’attends ta question avec impatience !"
    st.markdown(f'<div class="response-box">{reponse}</div>', unsafe_allow_html=True)

# 🎯 Quiz basé sur mon_cours.csv
with onglets[1]:
    st.header("📚 Quiz de révision")

    if "quiz_q" not in st.session_state:
        st.session_state.quiz_q = None
    if "quiz_done" not in st.session_state:
        st.session_state.quiz_done = False
    if "reponse_libre" not in st.session_state:
        st.session_state.reponse_libre = ""
    if "selected_qcm" not in st.session_state:
        st.session_state.selected_qcm = None
    if "next_question" not in st.session_state:
        st.session_state.next_question = False
    if "propositions" not in st.session_state:
        st.session_state.propositions = None

    if st.button("🔄 Recharger les questions"):
        st.cache_data.clear()

    df = load_data()

    if st.session_state.quiz_q is None:
        st.session_state.quiz_q = random.choice(df.to_dict("records"))

    if st.session_state.next_question:
        st.session_state.quiz_q = random.choice(df.to_dict("records"))
        st.session_state.quiz_done = False
        st.session_state.reponse_libre = ""
        st.session_state.selected_qcm = None
        st.session_state.propositions = None
        st.session_state.next_question = False

    question = st.session_state.quiz_q["question"]
    reponse_attendue = st.session_state.quiz_q["reponse"]

    st.subheader(f"🤔 {question}")

    reponse_libre = st.text_input(
        "💬 Ta réponse :",
        value=st.session_state.reponse_libre,
        key="reponse_libre",
        placeholder="Appuie sur Entrée pour valider..."
    )

    if st.session_state.propositions is None or st.session_state.quiz_done:
        propositions = [reponse_attendue]
        while len(propositions) < 4:
            r = random.choice(df["reponse"].tolist())
            if r not in propositions:
                propositions.append(r)
        random.shuffle(propositions)
        st.session_state.propositions = propositions

    container_qcm = st.container()
    choix_qcm = container_qcm.radio(
        "☑️ Ou choisis une réponse:",
        st.session_state.propositions,
        key="choix_qcm",
        index=None
    )

    if st.button("✅ Valider la réponse"):
        if reponse_libre.strip() and choix_qcm:
            st.warning("❗Merci de répondre soit à la question libre, soit au QCM, pas les deux.")
        elif reponse_libre.strip():
            from difflib import SequenceMatcher
            ratio = SequenceMatcher(None, reponse_attendue.lower(), reponse_libre.lower()).ratio()
            if ratio > 0.6:
                st.success("✅ Bonne réponse !")
                st.session_state.quiz_done = True
            else:
                st.error(f"❌ Mauvaise réponse. Réponse attendue : {reponse_attendue}")
        elif choix_qcm:
            if choix_qcm == reponse_attendue:
                st.success("✅ Bonne réponse !")
                st.session_state.quiz_done = True
            else:
                st.error(f"❌ Mauvaise réponse. Réponse attendue : {reponse_attendue}")
        else:
            st.warning("❗Merci de répondre à la question ou de choisir une réponse dans le QCM.")

    if st.session_state.quiz_done:
        if st.button("🔁 Question suivante"):
            st.session_state.next_question = True
            st.rerun()
            
# 🎮 Jeu des 5 mots
with onglets[2]:
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
        time.sleep(1.5)
        st.balloons()
        time.sleep(2.0)
        st.info("🎉 Tu as débloqué tous les mots du commerce ! Tu connais déjà bien le vocabulaire 👏")
        
# 📚 Digipad
with onglets[3]:
    st.header("📚 Accès au Digipad")
    st.markdown("""
    <h2 style="text-align: center; color: #000000; margin-top: 40px;">
        Ton espace de révision sur Digipad
    </h2>
    <div style="margin: 0 auto; max-width: 1200px; padding: 20px; background-color: #f9f9fc;
                border: 2px solid #61dafb; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        <iframe src="https://digipad.app/p/847630/15248ba9144b5"
                width="100%" height="850px"
                style="border: none; border-radius: 12px;">
        </iframe>
    </div>
""", unsafe_allow_html=True)
    
# Footer avec message + lien Digipad
st.markdown(
    f"""
    <div style='text-align: center; font-size: 1em; color: white; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ccc;'>
        ✨ Crois en toi, révise avec le sourire 😄 et donne le meilleur de toi-même !<br>
        💪 Bon courage pour tes révisions !<br><br>
        👉 <a href="https://digipad.app/p/847630/15248ba9144b5" target="_blank" style="color:white; font-weight:bold;">
        Accède ici à ton Digipad 📚</a><br><br>
        👥 <strong>Nombre total de visiteurs :</strong> {total}
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

# 📆 Badge de mise à jour
from datetime import datetime
date_maj = datetime.now().strftime("%d/%m/%Y à %Hh%M")
st.markdown(
    f"""
    <div style='text-align: center; font-size: 0.9em; color: white; margin-top: 10px;'>
        📆 Dernière mise à jour : <strong>{date_maj}</strong>
    </div>
    """,
    unsafe_allow_html=True
)

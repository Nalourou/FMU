import streamlit as st
import json
import re
import datetime
from langdetect import detect  # Pour la détection automatique de la langue

# --- Configuration de la page ---
st.set_page_config(page_title="FMU Éditeur ", layout="wide")
st.title("🛠️ FMU Éditeur ")

# --- Gestion du thème clair/sombre avec persistance ---
if "theme" not in st.session_state:
    st.session_state["theme"] = "Clair"

st.session_state["theme"] = st.radio(
    "Thème :", ["Clair", "Sombre"],
    index=0 if st.session_state["theme"] == "Clair" else 1,
    horizontal=True
)

# --- Application du thème via CSS ---
if st.session_state["theme"] == "Sombre":
    st.markdown("""
        <style>
            body, .stApp { background-color: #0e1117; color: white; }
            input, textarea, .stTextArea textarea {
                background-color: #262730; color: white; border: 1px solid #40444b;
            }
            .stDownloadButton { background-color: green; color: white; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            body, .stApp { background-color: #ffffff; color: black; }
            input, textarea, .stTextArea textarea {
                background-color: #f5f5f5; color: black; border: 1px solid #ccc;
            }
            .stDownloadButton { background-color: #007bff; color: white; }
        </style>
    """, unsafe_allow_html=True)

# --- Fonctions utilitaires ---
def valider_balises(fmu_text):
    """Vérifie que chaque balise ouvrante a une balise fermante correspondante."""
    erreurs = []
    balises_ouvertes = re.findall(r"<(\w+)>", fmu_text)
    balises_fermees = re.findall(r"</(\w+)>", fmu_text)
    for b in set(balises_ouvertes):
        if balises_ouvertes.count(b) != balises_fermees.count(b):
            erreurs.append(f"Balise non fermée : <{b}>")
    return erreurs

def parse_fmu_to_json(fmu_text):
    """Convertit le texte FMU en structure JSON."""
    lang_blocks = re.findall(r"<(\w{2})>(.*?)</\1>", fmu_text, re.DOTALL)
    result = {"lang": {}}
    for lang, content in lang_blocks:
        section = {}
        for tag in ["contents", "title", "header", "body", "info"]:
            match = re.search(rf"<{tag}>(.*?)</{tag}>", content, re.DOTALL)
            if match:
                section[tag] = match.group(1).strip()
        result["lang"][lang] = section
    return result

def json_to_html(data):
    """Génère du HTML à partir d’un JSON FMU."""
    html = ""
    for lang, bloc in data["lang"].items():
        html += f"<h2>{bloc.get('title','')}</h2>"
        html += f"<h3>{bloc.get('header','')}</h3>"
        html += f"<p><strong>Résumé :</strong> {bloc.get('contents','')}</p>"
        html += f"<p>{bloc.get('body','')}</p>"
        html += f"<pre>{bloc.get('info','')}</pre><hr>"
    return html

def json_to_txt(data):
    """Génère un texte brut à partir du JSON FMU."""
    texte = ""
    for lang, bloc in data["lang"].items():
        texte += f"{bloc.get('title','')}\n{bloc.get('header','')}\n\n"
        texte += f"{bloc.get('contents','')}\n\n{bloc.get('body','')}\n\n"
        texte += f"[INFO] {bloc.get('info','')}\n\n---\n"
    return texte

# --- Modèles prédéfinis ---
modeles = {
    "Exemple de base (FR)": """<fr>
  <title>Bienvenue</title>
  <header>Introduction</header>
  <contents>Résumé rapide du document FMU.</contents>
  <body>Ceci est le corps principal du contenu en français.</body>
  <info>Auteur : Moi | Date : 2025</info>
</fr>""",
    "Vide": ""
}

# --- Choix et chargement d’un modèle de base ---
modele = st.selectbox("Choisir un modèle :", list(modeles.keys()))
if st.button("Charger le modèle"):
    st.session_state["autosave"] = modeles[modele]
    st.toast("Modèle chargé !")

# --- Initialisation de la session pour sauvegarde ---
if "autosave" not in st.session_state:
    st.session_state["autosave"] = ""
if "versions" not in st.session_state:
    st.session_state["versions"] = []

# --- Interface avec onglets ---
tabs = st.tabs(["1. Édition", "2. Validation & JSON", "3. Prévisualisation", "4. Export"])

# === Onglet 1 : Édition ===
with tabs[0]:
    fmu_input = st.text_area("Éditez le contenu FMU :", value=st.session_state["autosave"], height=400)
    st.session_state["autosave"] = fmu_input

    if st.button("💾 Sauvegarder cette version"):
        st.session_state["versions"].append((datetime.datetime.now().strftime("%H:%M:%S"), fmu_input))
        st.toast("Version enregistrée")

    if st.session_state["versions"]:
        st.markdown("### Dernières versions")
        for horodatage, contenu in st.session_state["versions"][-3:][::-1]:
            with st.expander(f"Version {horodatage}"):
                st.code(contenu, language="xml")

# === Onglet 2 : Validation & JSON ===
with tabs[1]:
    erreurs = valider_balises(fmu_input)
    if erreurs:
        st.warning("Erreurs détectées :")
        for err in erreurs:
            st.markdown(f"- {err}")
        json_output = {}
    else:
        try:
            json_output = parse_fmu_to_json(fmu_input)
            st.success("✅ JSON généré automatiquement")
        except Exception as e:
            st.error(f"Erreur de parsing : {e}")
            json_output = {}

    if json_output and st.checkbox("Afficher JSON brut"):
        st.json(json_output)

# === Onglet 3 : Prévisualisation avec sélection de langue ===
with tabs[2]:
    if json_output:
        taille = st.slider("Taille du texte (prévisualisation)", 12, 32, 16)

        langues_disponibles = list(json_output["lang"].keys())
        langue_selectionnee = st.selectbox("Choisissez la langue à prévisualiser :", langues_disponibles)

        bloc = json_output["lang"].get(langue_selectionnee)
        if bloc:
            st.markdown(
                f"<div style='font-size:{taille}px'><strong>{bloc.get('title','')}</strong><br>{bloc.get('header','')}</div>",
                unsafe_allow_html=True
            )
            st.markdown(f"Résumé : {bloc.get('contents','')}")
            st.markdown(bloc.get("body", ""))
            st.code(bloc.get("info", ""), language="markdown")
        else:
            st.warning("Aucun contenu disponible pour la langue sélectionnée.")

# === Onglet 4 : Export ===
with tabs[3]:
    if json_output:
        nom = st.text_input("Nom de fichier", "mon_fmu.fmu.json")

        st.download_button(
            "Télécharger JSON",
            data=json.dumps(json_output, indent=4),
            file_name=nom,
            mime="application/json"
        )

        html = json_to_html(json_output)
        st.download_button(
            "Télécharger en HTML",
            data=html,
            file_name="mon_fmu.html",
            mime="text/html"
        )

        texte = json_to_txt(json_output)
        st.download_button(
            "Télécharger en texte",
            data=texte,
            file_name="mon_fmu.txt",
            mime="text/plain"
  )

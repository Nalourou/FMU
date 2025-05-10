import streamlit as st
import json

st.set_page_config(page_title="Lecteur FMU", layout="wide")
st.title("Lecteur FMU Multilingue")

uploaded_file = st.file_uploader("Téléversez un fichier FMU.JSON", type=["json"])

if uploaded_file:
    try:
        data = json.load(uploaded_file)

        if "lang" not in data:
            st.error("Fichier FMU invalide : la clé 'lang' est manquante.")
        else:
            langues = list(data["lang"].keys())
            selected_lang = st.selectbox("Choisissez une langue :", langues)

            if selected_lang in data["lang"]:
                contenu = data["lang"][selected_lang]
                st.success(f"Langue sélectionnée : `{selected_lang}`")

                with st.container():
                    st.subheader(contenu.get("title", ""))
                    st.markdown(f"### {contenu.get('header', '')}")
                    st.markdown(f"**Résumé :**\n{contenu.get('contents', '')}")
                    st.markdown("---")
                    st.markdown(f"**Détails :**\n{contenu.get('body', '')}")
                    st.markdown("---")
                    st.markdown("**Informations Supplémentaires :**")
                    st.code(contenu.get("info", ""), language="markdown")
            else:
                st.warning("Langue sélectionnée non disponible.")
    except Exception as e:
        st.error(f"Erreur de lecture : {e}")
else:
    st.info("Veuillez importer un fichier FMU.JSON pour commencer.")
    

st.write("Recharger votre fichier pour une manipulation complète.")

st.header("Manipulation ")

# Initialiser l'état du mode
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "fmu_data" not in st.session_state:
    st.session_state.fmu_data = None

# Upload du fichier
uploaded_file = st.file_uploader("Chargez un fichier FMU (.fmu.json)", type="json")

if uploaded_file and st.session_state.fmu_data is None:
    try:
        st.session_state.fmu_data = json.load(uploaded_file)
    except json.JSONDecodeError:
        st.error("Le fichier JSON est invalide.")

fmu_data = st.session_state.fmu_data

if fmu_data:
    if "lang" in fmu_data:
        langues_dispo = list(fmu_data["lang"].keys())
        langue_choisie = st.selectbox("Choisissez la langue :", langues_dispo)
        contenu = fmu_data["lang"].get(langue_choisie, {})

        # Bouton pour basculer entre lecture et édition
        if st.button("Lecteur / Modifier"):
            st.session_state.edit_mode = not st.session_state.edit_mode

        st.markdown("---")

        if not st.session_state.edit_mode:
            # Mode lecture seule
            st.text(f"Titre : {contenu.get('title', '')}")
            st.text(f"Header : {contenu.get('header', '')}")
            st.text_area("Corps du texte", value=contenu.get("body", ""), height=100, disabled=True)
            st.text_area("Résumé / Contents", value=contenu.get("contents", ""), height=80, disabled=True)
            st.text_area("Infos", value=contenu.get("info", ""), height=80, disabled=True)
        else:
            # Mode édition
            titre = st.text_input("Titre", value=contenu.get("title", ""))
            header = st.text_input("Header", value=contenu.get("header", ""))
            body = st.text_area("Corps du texte", value=contenu.get("body", ""), height=150)
            contents = st.text_area("Résumé / Contents", value=contenu.get("contents", ""), height=100)
            info = st.text_area("Infos", value=contenu.get("info", ""), height=80)

            # Sauvegarde
            fmu_data["lang"][langue_choisie] = {
                "title": titre,
                "header": header,
                "body": body,
                "contents": contents,
                "info": info
            }

            filename = st.text_input("Nom du fichier à sauvegarder :", value="fmu_modifié.fmu.json")
            st.download_button(
                label="Télécharger la version modifiée",
                data=json.dumps(fmu_data, indent=4, ensure_ascii=False),
                file_name=filename,
                mime="application/json"
            )
    else:
        st.error("Le fichier ne contient pas de clé 'lang'.")
      

import streamlit as st


st.set_page_config(page_title="FMU App", layout="centered")
st.title("Bienvenue dans l'application FMU")

st.markdown("Utilisez le menu à gauche pour :")
st.markdown("- Éditer un fichier FMU")
st.markdown("- Lire un fichier FMU multilingue")

# Documentation 
st.header("Documentation")

# Bouton pour lire la documentation
if st.button("Lire Documentation"):
    try:
        # Lecture du fichier Document.txt
        with open("Document.txt", "r", encoding="utf-8") as file:
            content = file.read()
        
        # Affichage du contenu dans une zone de texte en lecture seule
        st.text_area("Contenu de la documentation", 
                    value=content, 
                    height=400,
                    key="doc_content",
                    disabled=True)  # disabled=True empêche la modification
        
    except FileNotFoundError:
        st.error("Le fichier Document.txt n'a pas été trouvé.")
    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")
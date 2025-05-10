
# FMU Éditeur Multilingue – Streamlit App

**FMU (Fichier Multilingue Universel)** est un format de document conçu pour structurer du contenu dans plusieurs langues grâce à des balises intelligentes (`<title>`, `<header>`, `<body>`, etc.).  
Cette application Streamlit te permet de **créer, éditer, visualiser et exporter** facilement des fichiers `.fmu`.

## Fonctionnalités principales

- **Édition de contenu FMU** avec auto-sauvegarde  
- **Validation des balises FMU**  
- **Conversion automatique vers JSON (FMJ)**  
- **Prévisualisation dynamique par langue**  
- **Thèmes clair / sombre personnalisés**  
- **Export vers `.json`, `.html` ou `.txt`**  
- **Lecture de fichier `.fmu.json` dans un lecteur dédié**  

## À propos du format FMU

FMU permet d'organiser du contenu multilingue avec la structure suivante :

```xml
<lang>
  <fr>
    <title>Bienvenue</title>
    <header>Introduction</header>
    <contents>Résumé en français...</contents>
    <body>Contenu du document...</body>
    <info>Auteur : Nalourou, 2025</info>
  </fr>
  <en>
    <title>Welcome</title>
    <header>Introduction</header>
    <contents>Summary in English...</contents>
    <body>Document content...</body>
    <info>Author: Nalourou, 2025</info>
  </en>
</lang>

Lors de l'export, ce format est transformé automatiquement en JSON :
```json
{
  "lang": {
    "fr": {
      "title": "...",
      "header": "...",
      "contents": "...",
      "body": "...",
      "info": "..."
    },
    "en": {
      ...
    }
  }
}

🚀 ##Comment lancer l’application

Installation :

Assurez-vous d’avoir Python 3 et Streamlit installés :

pip install -r requirements.txt

Exécution :

streamlit run Home.py

🗂 ##Structure du projet

FMU/
├── Home.py              ← Point d’entrée Streamlit
├── requirements.txt     ← Dépendances Python
├── document.txt         ← Documentation officielle FMU
├── pages/               ← Composants internes
│   ├── FMU.py
│   └── Lectur_FMU.py


👤 ##Auteur

Nalourou – Visionnaire technologique et architecte
de la communication multilingue du futur.

> "Unifier les langues, structurer le savoir."


# FMU
# FMU
# FMU
# FMU

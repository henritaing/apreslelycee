import pandas as pd
import streamlit as st

# Charger les données
df = pd.read_csv("fr-esr-parcoursup.csv", sep=";", encoding="utf-8-sig")

# Liste des domaines (avec "Autres")
domaines = list([
    "Art / Audiovisuel / Animation / Design",
    "Droit et sciences politiques",
    "Philosophie, lettres et langues",
    "Sciences humaines et sociales",
    "Sciences",
    "Psychologie",
    "Santé",
    "Enseignement",
    "Architecture",
    "Commerce, économie et gestion",
    "Communication",
    "écoles de la Défense",
    "écoles de gendarmerie",
    "écoles du jeu vidéo",
    "Ingénierie",
    "écoles de journalisme",
    "écoles de police",
    "Paramédical",
    "écoles du social",
    "ENS (écoles normales supérieures)",
    "écoles vétérinaires",
    "formations en sport",
    "Agriculture",
    "Services",
    "Mode",
    "Musique",
    "Artisanat",
    "Technique / Production",
    "Autres"
])

# Créer la colonne Domaine si elle n'existe pas
if 'Domaine' not in df.columns:
    df['Domaine'] = ''

# Nouveau mapping domaine -> mots-clés
domaine_mapping = {
    "Art / Audiovisuel / Animation / Design": ["art", "arts plastiques", "design", "beaux-arts", "école d'art", "arts appliqués", "audiovisuel", "cinéma", "télévision", "animation", "3d", "cinéma d’animation", "illustration", "graphisme"],
    "Droit et sciences politiques": ["droit", "science politique", "juridique", "Instituts d'études politiques", "iep", "institut d'études politiques", "sciences po"],
    "Commerce, économie et gestion": ["économie", "gestion", "commerce", "finance", "management", "economie", "economique", "économique", "administration", "école de commerce", "business school", "commerce", "vente", "ECG", "commercialisation", "comptabilité", "expertise comptable", "dgc"],
    "Philosophie, lettres et langues": ["lettres", "langues", "littérature", "linguistique", "anglais", "espagnol", "langage", "philosophie", "littéraire", "littéraires"],
    "Sciences humaines et sociales": ["sociologie", "anthropologie", "sciences sociales", "histoire", "géographie"],
    "Agriculture": ["agricole", "nature", "agricoles"],
    "Sciences": ["math", "physique", "chimie", "informatique", "biologie", "sciences de la vie", "sciences de la terre", "electronique", "électronique", "MP2I", "PCSI", "MPSI", "PTSI", "CPGE - TB", "TSI", "BCPST", "science des données", "réseaux et télécommunications"],
    "Psychologie": ["psychologie", "psycho"],
    "Santé": ["médecine", "infirmier", "kiné", "orthophoniste", "orthoptiste", "sage-femme", "ergothérapeute", "santé", "Imagerie médicale et radiologie thérapeutique"],
    "Enseignement": ["professeur", "enseignement", "éducation", "pppe", "éducateur", "Educateur", "professorat", "Sciences de l'éducation et de la formation", "éducation"],
    "Architecture": ["architecture", "architecte"],
    "Communication": ["communication", "publicité", "relations publiques"],
    "écoles de la Défense": ["défense", "armée"],
    "écoles de gendarmerie": ["gendarmerie"],
    "écoles du jeu vidéo": ["jeu vidéo", "game", "gaming"],
    "Ingénierie": ["ingénierie", "école d'ingénieur", "ingénieur", "génie"],
    "écoles de journalisme": ["journalisme", "journaliste"],
    "écoles de police": ["police"],
    "Paramédical": ["audioprothésiste", "manipulateur", "podologue", "laboratoire médical", "secrétariat médical", "Diététique"],
    "écoles du social": ["assistant de service social", "éducateur", "animation sociale", "assistance sociale", "Economie sociale familiale"],
    "ENS (écoles normales supérieures)": ["ens"],
    "écoles vétérinaires": ["vétérinaire"],
    "formations en sport": ["staps", "sport", "activité physique", "éducateur sportif", "sportif"],
    "Mode": ["mode"],
    "Services": ["tourisme", "hôtellerie", "restauration", "hospitalité", "événement", "accueil"],
    "Musique": ["musicologie", "musique"],
    "Artisanat": ["matériaux", "bois", "métal"],
    "Technique / Production": ["conception", "maintenance", "production", "processus"]
}

# Fonction pour prédire le domaine
def predire_domaine(filiere):
    filiere_lower = filiere.lower()
    for domaine, mots in domaine_mapping.items():
        for mot in mots:
            if mot.lower() in filiere_lower:
                return domaine
    return "Autres"

# Pré-remplir les domaines inconnus
df.loc[df['Domaine'] == '', 'Domaine'] = df.loc[df['Domaine'] == '', 'Filière de formation'].apply(predire_domaine)

# Afficher le tableau pour validation ou modification
edited_df = st.data_editor(
    df[['Filière de formation', 'Domaine']],
    column_config={
        "Domaine": st.column_config.SelectboxColumn(
            "Choisir le domaine",
            options=domaines,
        )
    },
    key="editeur_final",
    hide_index=True
)

# Bouton pour sauvegarder
if st.button("Sauvegarder les modifications"):
    for idx, row in edited_df.iterrows():
        df.loc[df['Filière de formation'] == row['Filière de formation'], 'Domaine'] = row['Domaine']

    df.to_csv("fr-esr-parcoursup-mis-a-jour.csv", sep=";", index=False, encoding="utf-8-sig")
    st.success("Toutes les modifications ont été sauvegardées !")

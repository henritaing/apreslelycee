import streamlit as st
from db import SessionLocal
from models import Formation, Metier, Domaine

st.set_page_config(page_title="Orientation", layout="wide")

st.title("🎓 Explorer les parcours Formations ↔ Métiers")

session = SessionLocal()

# Choix utilisateur
# app.py (nouveau mode)
mode = st.radio("Explorer par :", ["Métier → Formations", "Domaine → Formations → Métiers"])

if mode == "Domaine → Formations → Métiers":
    domaines = session.query(Domaine).all()
    choix_domaine = st.selectbox("Choisissez un domaine :", [f"{d.id} - {d.libelle}" for d in domaines])
    domaine_id = choix_domaine.split(" - ")[0]
    domaine = session.get(Domaine, domaine_id)

    formations = domaine.formations
    choix_formation = st.selectbox("Choisissez une formation :", [f"{f.id} - {f.libelle}" for f in formations])
    formation_id = choix_formation.split(" - ")[0]
    formation = session.get(Formation, formation_id)

    st.subheader(f"📚 {formation.libelle} ({formation.niveau})")
    if formation.url:
        st.markdown(f"[📖 Plus d'infos]({formation.url})")

    st.write("👉 Métiers accessibles :")
    for metier in formation.metiers:
        st.markdown(f"- **{metier.nom}** ({metier.libelle_masculin} / {metier.libelle_feminin})")

elif mode == "Métier → Formations":
    metiers = session.query(Metier).all()
    choix = st.selectbox("Choisissez un métier :", [f"{m.id} - {m.nom}" for m in metiers])
    metier_id = choix.split(" - ")[0]
    metier = session.get(Metier, metier_id)

    st.subheader(f"👩‍💼 {metier.nom}")
    st.write("👉 Formations possibles :")
    for formation in metier.formations:
        st.markdown(f"- **{formation.libelle}** ({formation.niveau}) [🔗]({formation.url})")

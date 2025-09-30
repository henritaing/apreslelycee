import streamlit as st
from db import SessionLocal
from models import Formation, Metier

st.set_page_config(page_title="Orientation", layout="wide")

st.title("🎓 Explorer les parcours Formations ↔ Métiers")

session = SessionLocal()

# Choix utilisateur
mode = st.radio("Voulez-vous partir d’une formation ou d’un métier ?", ["Formation → Métiers", "Métier → Formations"])

if mode == "Formation → Métiers":
    formations = session.query(Formation).all()
    choix = st.selectbox("Choisissez une formation :", [f"{f.id} - {f.libelle}" for f in formations])
    formation_id = choix.split(" - ")[0]
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

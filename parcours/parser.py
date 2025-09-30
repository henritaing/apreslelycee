import xml.etree.ElementTree as ET
from db import init_db, SessionLocal
from models import Formation, Metier

def parse_and_insert(xml_path="data/formations.xml"):
    init_db()
    tree = ET.parse(xml_path)
    root = tree.getroot()

    session = SessionLocal()

    for formation in root.findall("formation"):
        f = Formation(
            id=formation.findtext("identifiant"),
            libelle=formation.findtext("libelle_complet"),
            niveau=formation.findtext("niveau_etudes/libelle"),
            url=formation.findtext("url")
        )

        for metier_xml in formation.findall("metiers_formation/metier"):
            m_id = metier_xml.findtext("id")
            metier = session.get(Metier, m_id)
            if not metier:
                metier = Metier(
                    id=m_id,
                    nom=metier_xml.findtext("nom_metier"),
                    libelle_feminin=metier_xml.findtext("libelle_feminin"),
                    libelle_masculin=metier_xml.findtext("libelle_masculin"),
                )
            f.metiers.append(metier)

        session.add(f)

    session.commit()
    session.close()

if __name__ == "__main__":
    parse_and_insert()
    print("✅ Base de données remplie avec succès")

from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

formations_metiers = Table(
    "formations_metiers", Base.metadata,
    Column("formation_id", ForeignKey("formations.id"), primary_key=True),
    Column("metier_id", ForeignKey("metiers.id"), primary_key=True)
)

class Formation(Base):
    __tablename__ = "formations"
    id = Column(String, primary_key=True)
    libelle = Column(String)
    niveau = Column(String)
    url = Column(String)
    metiers = relationship("Metier", secondary=formations_metiers, back_populates="formations")

class Metier(Base):
    __tablename__ = "metiers"
    id = Column(String, primary_key=True)
    nom = Column(String)
    libelle_feminin = Column(String)
    libelle_masculin = Column(String)
    formations = relationship("Formation", secondary=formations_metiers, back_populates="metiers")

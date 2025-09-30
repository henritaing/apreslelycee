from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

formations_metiers = Table(
    "formations_metiers", Base.metadata,
    Column("formation_id", ForeignKey("formations.id"), primary_key=True),
    Column("metier_id", ForeignKey("metiers.id"), primary_key=True)
)

formations_domaines = Table(
    "formations_domaines",
    Base.metadata,
    Column("formation_id", String, ForeignKey("formations.id"), primary_key=True),
    Column("domaine_id", String, ForeignKey("domaines.id"), primary_key=True),
    extend_existing=True
)

class Formation(Base):
    __tablename__ = "formations"
    id = Column(String, primary_key=True)
    libelle = Column(String)
    niveau = Column(String)
    url = Column(String)
    
    # Relation vers les métiers
    metiers = relationship("Metier", secondary=formations_metiers, back_populates="formations")
    
    # Relation vers les domaines
    domaines = relationship("Domaine", secondary=formations_domaines, back_populates="formations")


class Metier(Base):
    __tablename__ = "metiers"
    id = Column(String, primary_key=True)
    nom = Column(String)
    libelle_feminin = Column(String)
    libelle_masculin = Column(String)
    formations = relationship("Formation", secondary=formations_metiers, back_populates="metiers")

class Domaine(Base):
    __tablename__ = "domaines"
    id = Column(String, primary_key=True)
    libelle = Column(String)
    formations = relationship("Formation", secondary="formations_domaines", back_populates="domaines")


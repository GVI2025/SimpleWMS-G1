from sqlalchemy import Column, String, Float, Date, Enum, Integer, Boolean
from uuid import uuid4
import enum

from app.database.database import Base

class Salle(Base):
    __tablename__ = "salles"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    nom = Column(String, unique=True, nullable=False)
    capacite = Column(Integer, nullable=False)
    localisation = Column(String, nullable=False)
    disponible = Column(Boolean, nullable=False, default=True)

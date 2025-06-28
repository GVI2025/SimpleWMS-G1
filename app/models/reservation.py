from sqlalchemy import Column, String, Date, Time, ForeignKey
from uuid import uuid4
import enum

from app.database.database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    salle_id = Column(String, ForeignKey("salles.id"), nullable=False)
    date = Column(Date, nullable=False)
    heure = Column(Time, nullable=False)
    utilisateur = Column(String, nullable=False)

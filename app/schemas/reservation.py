from pydantic import BaseModel
from datetime import time, date

class ReservationBase(BaseModel):
    salle_id: str
    date: date
    heure: time
    utilisateur: str
    commentaire: str

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(ReservationBase):
    pass

class ReservationRead(ReservationBase):
    id: str

    class Config:
        orm_mode = True

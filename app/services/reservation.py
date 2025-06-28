from sqlalchemy.orm import Session
from app.models import Reservation as ReservationModel
from app.schemas.reservation import ReservationCreate, ReservationUpdate

def get_reservation(db: Session, reservation_id: str):
    return db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()

def list_reservations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ReservationModel).offset(skip).limit(limit).all()

def create_reservation(db: Session, reservation: ReservationCreate):
    db_reservation = ReservationModel(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation
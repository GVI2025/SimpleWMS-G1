from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.models import Reservation as ReservationModel
from app.schemas.reservation import ReservationCreate

from datetime import datetime, timedelta

def get_reservation(db: Session, reservation_id: str):
    return db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()

def list_reservations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ReservationModel).offset(skip).limit(limit).all()

def create_reservation(db: Session, reservation: ReservationCreate):
    db_reservation = ReservationModel(**reservation.dict())

    time = datetime.combine(datetime.today(), db_reservation.heure)
    next_hour = (time+timedelta(hours=1)).time()
    previous_hour = (time-timedelta(hours=1)).time()

    check = db.query(ReservationModel).filter(ReservationModel.salle_id == db_reservation.salle_id)
    check = check.filter(ReservationModel.date == db_reservation.date)
    result = check.filter(or_(
      and_(ReservationModel.heure >= db_reservation.heure, ReservationModel.heure <= next_hour),
      and_(ReservationModel.heure <= db_reservation.heure, ReservationModel.heure >= previous_hour)
    )).first()

    if result:
      return    
    
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def delete_reservation(db: Session, reservation_id: str):
    db_reservation = get_reservation(db, reservation_id)
    if db_reservation:
        db.delete(db_reservation)
        db.commit()
    return db_reservation

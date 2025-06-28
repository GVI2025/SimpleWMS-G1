from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.reservation import ReservationRead, ReservationCreate, ReservationUpdate
from app.services import reservation as reservation_service
from app.database.database import get_db

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.get("/", response_model=List[ReservationRead])
def list_reservations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return reservation_service.list_reservations(db, skip, limit)

@router.post("/", response_model=ReservationRead, status_code=201)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    reservation = reservation_service.create_reservation(db, reservation)
    if not reservation:
      raise HTTPException(status_code=400, detail="Créneau déjà réservé")
    return reservation

@router.get("/{reservation_id}", response_model=ReservationRead)
def get_reservation(reservation_id: str, db: Session = Depends(get_db)):
    reservation = reservation_service.get_reservation(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@router.delete("/{reservation_id}", response_model=ReservationRead)
def delete_reservation(reservation_id: str, db: Session = Depends(get_db)):
    deleted = reservation_service.delete_reservation(db, reservation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return deleted

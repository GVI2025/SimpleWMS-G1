from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.reception import ReceptionRead, ReceptionCreate, ReceptionUpdate
from app.services import reception as reception_service
from app.database.database import get_db

router = APIRouter(prefix="/receptions", tags=["Réceptions"])

@router.get("/", response_model=List[ReceptionRead])
def list_receptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return reception_service.list_receptions(db, skip, limit)

@router.post("/", response_model=ReceptionRead, status_code=201)
def create_reception(reception: ReceptionCreate, db: Session = Depends(get_db)):
    return reception_service.create_reception(db, reception)

@router.get("/{reception_id}", response_model=ReceptionRead)
def get_reception(reception_id: str, db: Session = Depends(get_db)):
    reception = reception_service.get_reception(db, reception_id)
    if not reception:
        raise HTTPException(status_code=404, detail="Reception not found")
    return reception

@router.put("/{reception_id}", response_model=ReceptionRead)
def update_reception(reception_id: str, reception: ReceptionUpdate, db: Session = Depends(get_db)):
    updated = reception_service.update_reception(db, reception_id, reception)
    if not updated:
        raise HTTPException(status_code=404, detail="Reception not found")
    return updated

@router.delete("/{reception_id}", response_model=ReceptionRead)
def delete_reception(reception_id: str, db: Session = Depends(get_db)):
    deleted = reception_service.delete_reception(db, reception_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Reception not found")
    return deleted

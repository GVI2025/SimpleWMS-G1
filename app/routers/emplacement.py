from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.emplacement import EmplacementRead, EmplacementCreate, EmplacementUpdate
from app.services import emplacement as emplacement_service
from app.database.database import get_db

router = APIRouter(prefix="/emplacements", tags=["Emplacements"])

@router.get("/", response_model=List[EmplacementRead])
def list_emplacements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return emplacement_service.list_emplacements(db, skip, limit)

@router.post("/", response_model=EmplacementRead, status_code=201)
def create_emplacement(emplacement: EmplacementCreate, db: Session = Depends(get_db)):
    existing = emplacement_service.get_emplacement_by_code(db, emplacement.code)
    if existing:
        raise HTTPException(status_code=400, detail="Emplacement with this code already exists.")
    return emplacement_service.create_emplacement(db, emplacement)

@router.get("/{emplacement_id}", response_model=EmplacementRead)
def get_emplacement(emplacement_id: str, db: Session = Depends(get_db)):
    emplacement = emplacement_service.get_emplacement(db, emplacement_id)
    if not emplacement:
        raise HTTPException(status_code=404, detail="Emplacement not found")
    return emplacement

@router.put("/{emplacement_id}", response_model=EmplacementRead)
def update_emplacement(emplacement_id: str, emplacement: EmplacementUpdate, db: Session = Depends(get_db)):
    updated = emplacement_service.update_emplacement(db, emplacement_id, emplacement)
    if not updated:
        raise HTTPException(status_code=404, detail="Emplacement not found")
    return updated

@router.delete("/{emplacement_id}", response_model=EmplacementRead)
def delete_emplacement(emplacement_id: str, db: Session = Depends(get_db)):
    deleted = emplacement_service.delete_emplacement(db, emplacement_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Emplacement not found")
    return deleted

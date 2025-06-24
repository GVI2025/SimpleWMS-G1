from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.implantation import ImplantationRead, ImplantationCreate, ImplantationUpdate
from app.services import implantation as implantation_service
from app.database.database import get_db

router = APIRouter(prefix="/implantations", tags=["Implantations"])

@router.get("/", response_model=List[ImplantationRead])
def list_implantations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return implantation_service.list_implantations(db, skip, limit)

@router.post("/", response_model=ImplantationRead, status_code=201)
def create_implantation(implantation: ImplantationCreate, db: Session = Depends(get_db)):
    return implantation_service.create_implantation(db, implantation)

@router.get("/{implantation_id}", response_model=ImplantationRead)
def get_implantation(implantation_id: str, db: Session = Depends(get_db)):
    implantation = implantation_service.get_implantation(db, implantation_id)
    if not implantation:
        raise HTTPException(status_code=404, detail="Implantation not found")
    return implantation

@router.put("/{implantation_id}", response_model=ImplantationRead)
def update_implantation(implantation_id: str, implantation: ImplantationUpdate, db: Session = Depends(get_db)):
    updated = implantation_service.update_implantation(db, implantation_id, implantation)
    if not updated:
        raise HTTPException(status_code=404, detail="Implantation not found")
    return updated

@router.delete("/{implantation_id}", response_model=ImplantationRead)
def delete_implantation(implantation_id: str, db: Session = Depends(get_db)):
    deleted = implantation_service.delete_implantation(db, implantation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Implantation not found")
    return deleted

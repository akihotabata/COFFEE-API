from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud.certification as certification_crud
import schemas
from database import SessionLocal

router = APIRouter(prefix="/certifications", tags=["certifications"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.Certification])
def read_certifications(page: int = 1, per_page: int = 50, db: Session = Depends(get_db)):
    skip = (page - 1) * per_page
    return certification_crud.get_multi(db, skip=skip, limit=per_page)


@router.get("/{certification_id}", response_model=schemas.Certification)
def read_certification(certification_id: int, db: Session = Depends(get_db)):
    db_cert = certification_crud.get(db, certification_id)
    if not db_cert:
        raise HTTPException(status_code=404, detail="Certification not found")
    return db_cert


@router.post("/", response_model=schemas.Certification, status_code=201)
def create_certification(certification: schemas.CertificationCreate, db: Session = Depends(get_db)):
    return certification_crud.create(db, certification)


@router.put("/{certification_id}", response_model=schemas.Certification)
def update_certification(
    certification_id: int, certification: schemas.CertificationUpdate, db: Session = Depends(get_db)
):
    db_cert = certification_crud.get(db, certification_id)
    if not db_cert:
        raise HTTPException(status_code=404, detail="Certification not found")
    return certification_crud.update(db, db_cert, certification)


@router.delete("/{certification_id}", response_model=schemas.Certification)
def delete_certification(certification_id: int, db: Session = Depends(get_db)):
    db_cert = certification_crud.get(db, certification_id)
    if not db_cert:
        raise HTTPException(status_code=404, detail="Certification not found")
    return certification_crud.remove(db, db_cert)

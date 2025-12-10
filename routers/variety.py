from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud.variety as variety_crud
import schemas
from database import SessionLocal

router = APIRouter(prefix="/varieties", tags=["varieties"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.Variety])
def read_varieties(page: int = 1, per_page: int = 50, db: Session = Depends(get_db)):
    skip = (page - 1) * per_page
    return variety_crud.get_multi(db, skip=skip, limit=per_page)


@router.get("/{variety_id}", response_model=schemas.Variety)
def read_variety(variety_id: int, db: Session = Depends(get_db)):
    db_variety = variety_crud.get(db, variety_id)
    if not db_variety:
        raise HTTPException(status_code=404, detail="Variety not found")
    return db_variety


@router.post("/", response_model=schemas.Variety, status_code=201)
def create_variety(variety: schemas.VarietyCreate, db: Session = Depends(get_db)):
    return variety_crud.create(db, variety)


@router.put("/{variety_id}", response_model=schemas.Variety)
def update_variety(variety_id: int, variety: schemas.VarietyUpdate, db: Session = Depends(get_db)):
    db_variety = variety_crud.get(db, variety_id)
    if not db_variety:
        raise HTTPException(status_code=404, detail="Variety not found")
    return variety_crud.update(db, db_variety, variety)


@router.delete("/{variety_id}", response_model=schemas.Variety)
def delete_variety(variety_id: int, db: Session = Depends(get_db)):
    db_variety = variety_crud.get(db, variety_id)
    if not db_variety:
        raise HTTPException(status_code=404, detail="Variety not found")
    return variety_crud.remove(db, db_variety)

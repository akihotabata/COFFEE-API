from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud.subregion as subregion_crud
import schemas
from database import SessionLocal

router = APIRouter(prefix="/subregions", tags=["subregions"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.Subregion])
def read_subregions(page: int = 1, per_page: int = 50, db: Session = Depends(get_db)):
    skip = (page - 1) * per_page
    return subregion_crud.get_multi(db, skip=skip, limit=per_page)


@router.get("/{subregion_id}", response_model=schemas.Subregion)
def read_subregion(subregion_id: int, db: Session = Depends(get_db)):
    db_subregion = subregion_crud.get(db, subregion_id)
    if not db_subregion:
        raise HTTPException(status_code=404, detail="Subregion not found")
    return db_subregion


@router.post("/", response_model=schemas.Subregion, status_code=201)
def create_subregion(subregion: schemas.SubregionCreate, db: Session = Depends(get_db)):
    return subregion_crud.create(db, subregion)


@router.put("/{subregion_id}", response_model=schemas.Subregion)
def update_subregion(subregion_id: int, subregion: schemas.SubregionUpdate, db: Session = Depends(get_db)):
    db_subregion = subregion_crud.get(db, subregion_id)
    if not db_subregion:
        raise HTTPException(status_code=404, detail="Subregion not found")
    return subregion_crud.update(db, db_subregion, subregion)


@router.delete("/{subregion_id}", response_model=schemas.Subregion)
def delete_subregion(subregion_id: int, db: Session = Depends(get_db)):
    db_subregion = subregion_crud.get(db, subregion_id)
    if not db_subregion:
        raise HTTPException(status_code=404, detail="Subregion not found")
    return subregion_crud.remove(db, db_subregion)

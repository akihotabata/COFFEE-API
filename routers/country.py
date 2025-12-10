from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud.country as country_crud
import schemas
from database import SessionLocal

router = APIRouter(prefix="/countries", tags=["countries"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.Country])
def read_countries(page: int = 1, per_page: int = 50, db: Session = Depends(get_db)):
    skip = (page - 1) * per_page
    return country_crud.get_multi(db, skip=skip, limit=per_page)


@router.get("/{country_id}", response_model=schemas.Country)
def read_country(country_id: int, db: Session = Depends(get_db)):
    db_country = country_crud.get(db, country_id)
    if not db_country:
        raise HTTPException(status_code=404, detail="Country not found")
    return db_country


@router.post("/", response_model=schemas.Country, status_code=201)
def create_country(country: schemas.CountryCreate, db: Session = Depends(get_db)):
    return country_crud.create(db, country)


@router.put("/{country_id}", response_model=schemas.Country)
def update_country(country_id: int, country: schemas.CountryUpdate, db: Session = Depends(get_db)):
    db_country = country_crud.get(db, country_id)
    if not db_country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country_crud.update(db, db_country, country)


@router.delete("/{country_id}", response_model=schemas.Country)
def delete_country(country_id: int, db: Session = Depends(get_db)):
    db_country = country_crud.get(db, country_id)
    if not db_country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country_crud.remove(db, db_country)

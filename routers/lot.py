from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud.lot as lot_crud
import schemas
from database import SessionLocal
from filters import filter_lots

router = APIRouter(prefix="/lots", tags=["lots"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=schemas.PaginatedResponse)
def search_lots(
    country_code: str = None,
    farm_id: int = None,
    variety_id: int = None,
    process_id: int = None,
    harvest_year: int = None,
    min_score: float = None,
    max_score: float = None,
    tasting: str = None,
    min_altitude: int = None,
    max_altitude: int = None,
    page: int = 1,
    per_page: int = 50,
    db: Session = Depends(get_db),
):
    params = schemas.LotSearchParams(
        country_code=country_code,
        farm_id=farm_id,
        variety_id=variety_id,
        process_id=process_id,
        harvest_year=harvest_year,
        min_score=min_score,
        max_score=max_score,
        tasting=tasting,
        min_altitude=min_altitude,
        max_altitude=max_altitude,
        page=page,
        per_page=per_page,
    )
    total, items = filter_lots(db, params)
    return schemas.PaginatedResponse(total=total, page=page, per_page=per_page, items=items)


@router.get("/{lot_id}", response_model=schemas.Lot)
def read_lot(lot_id: int, db: Session = Depends(get_db)):
    db_lot = lot_crud.get(db, lot_id)
    if not db_lot:
        raise HTTPException(status_code=404, detail="Lot not found")
    return db_lot


@router.post("/", response_model=schemas.Lot, status_code=201)
def create_lot(lot: schemas.LotCreate, db: Session = Depends(get_db)):
    return lot_crud.create(db, lot)


@router.put("/{lot_id}", response_model=schemas.Lot)
def update_lot(lot_id: int, lot: schemas.LotUpdate, db: Session = Depends(get_db)):
    db_lot = lot_crud.get(db, lot_id)
    if not db_lot:
        raise HTTPException(status_code=404, detail="Lot not found")
    return lot_crud.update(db, db_lot, lot)


@router.delete("/{lot_id}", response_model=schemas.Lot)
def delete_lot(lot_id: int, db: Session = Depends(get_db)):
    db_lot = lot_crud.get(db, lot_id)
    if not db_lot:
        raise HTTPException(status_code=404, detail="Lot not found")
    return lot_crud.remove(db, db_lot)

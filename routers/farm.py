from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud.farm as farm_crud
import schemas
from database import SessionLocal
from filters import filter_farms

router = APIRouter(prefix="/farms", tags=["farms"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=schemas.PaginatedResponse)
def search_farms(
    country_code: str = None,
    region_id: int = None,
    subregion_id: int = None,
    min_altitude: int = None,
    max_altitude: int = None,
    q: str = None,
    page: int = 1,
    per_page: int = 50,
    db: Session = Depends(get_db),
):
    params = schemas.FarmSearchParams(
        country_code=country_code,
        region_id=region_id,
        subregion_id=subregion_id,
        min_altitude=min_altitude,
        max_altitude=max_altitude,
        q=q,
        page=page,
        per_page=per_page,
    )
    total, items = filter_farms(db, params)
    return schemas.PaginatedResponse(total=total, page=page, per_page=per_page, items=items)


@router.get("/{farm_id}", response_model=schemas.Farm)
def read_farm(farm_id: int, db: Session = Depends(get_db)):
    db_farm = farm_crud.get(db, farm_id)
    if not db_farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    return db_farm


@router.post("/", response_model=schemas.Farm, status_code=201)
def create_farm(farm: schemas.FarmCreate, db: Session = Depends(get_db)):
    return farm_crud.create(db, farm)


@router.put("/{farm_id}", response_model=schemas.Farm)
def update_farm(farm_id: int, farm: schemas.FarmUpdate, db: Session = Depends(get_db)):
    db_farm = farm_crud.get(db, farm_id)
    if not db_farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farm_crud.update(db, db_farm, farm)


@router.delete("/{farm_id}", response_model=schemas.Farm)
def delete_farm(farm_id: int, db: Session = Depends(get_db)):
    db_farm = farm_crud.get(db, farm_id)
    if not db_farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farm_crud.remove(db, db_farm)

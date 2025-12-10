from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud.region as region_crud
import schemas
from database import SessionLocal

router = APIRouter(prefix="/regions", tags=["regions"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.Region])
def read_regions(page: int = 1, per_page: int = 50, db: Session = Depends(get_db)):
    skip = (page - 1) * per_page
    return region_crud.get_multi(db, skip=skip, limit=per_page)


@router.get("/{region_id}", response_model=schemas.Region)
def read_region(region_id: int, db: Session = Depends(get_db)):
    db_region = region_crud.get(db, region_id)
    if not db_region:
        raise HTTPException(status_code=404, detail="Region not found")
    return db_region


@router.post("/", response_model=schemas.Region, status_code=201)
def create_region(region: schemas.RegionCreate, db: Session = Depends(get_db)):
    return region_crud.create(db, region)


@router.put("/{region_id}", response_model=schemas.Region)
def update_region(region_id: int, region: schemas.RegionUpdate, db: Session = Depends(get_db)):
    db_region = region_crud.get(db, region_id)
    if not db_region:
        raise HTTPException(status_code=404, detail="Region not found")
    return region_crud.update(db, db_region, region)


@router.delete("/{region_id}", response_model=schemas.Region)
def delete_region(region_id: int, db: Session = Depends(get_db)):
    db_region = region_crud.get(db, region_id)
    if not db_region:
        raise HTTPException(status_code=404, detail="Region not found")
    return region_crud.remove(db, db_region)

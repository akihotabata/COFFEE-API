from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud.producer as producer_crud
import schemas
from database import SessionLocal

router = APIRouter(prefix="/producers", tags=["producers"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.Producer])
def read_producers(page: int = 1, per_page: int = 50, db: Session = Depends(get_db)):
    skip = (page - 1) * per_page
    return producer_crud.get_multi(db, skip=skip, limit=per_page)


@router.get("/{producer_id}", response_model=schemas.Producer)
def read_producer(producer_id: int, db: Session = Depends(get_db)):
    db_producer = producer_crud.get(db, producer_id)
    if not db_producer:
        raise HTTPException(status_code=404, detail="Producer not found")
    return db_producer


@router.post("/", response_model=schemas.Producer, status_code=201)
def create_producer(producer: schemas.ProducerCreate, db: Session = Depends(get_db)):
    return producer_crud.create(db, producer)


@router.put("/{producer_id}", response_model=schemas.Producer)
def update_producer(producer_id: int, producer: schemas.ProducerUpdate, db: Session = Depends(get_db)):
    db_producer = producer_crud.get(db, producer_id)
    if not db_producer:
        raise HTTPException(status_code=404, detail="Producer not found")
    return producer_crud.update(db, db_producer, producer)


@router.delete("/{producer_id}", response_model=schemas.Producer)
def delete_producer(producer_id: int, db: Session = Depends(get_db)):
    db_producer = producer_crud.get(db, producer_id)
    if not db_producer:
        raise HTTPException(status_code=404, detail="Producer not found")
    return producer_crud.remove(db, db_producer)

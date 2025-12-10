from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud.process as process_crud
import schemas
from database import SessionLocal

router = APIRouter(prefix="/processes", tags=["processes"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.Process])
def read_processes(page: int = 1, per_page: int = 50, db: Session = Depends(get_db)):
    skip = (page - 1) * per_page
    return process_crud.get_multi(db, skip=skip, limit=per_page)


@router.get("/{process_id}", response_model=schemas.Process)
def read_process(process_id: int, db: Session = Depends(get_db)):
    db_process = process_crud.get(db, process_id)
    if not db_process:
        raise HTTPException(status_code=404, detail="Process not found")
    return db_process


@router.post("/", response_model=schemas.Process, status_code=201)
def create_process(process: schemas.ProcessCreate, db: Session = Depends(get_db)):
    return process_crud.create(db, process)


@router.put("/{process_id}", response_model=schemas.Process)
def update_process(process_id: int, process: schemas.ProcessUpdate, db: Session = Depends(get_db)):
    db_process = process_crud.get(db, process_id)
    if not db_process:
        raise HTTPException(status_code=404, detail="Process not found")
    return process_crud.update(db, db_process, process)


@router.delete("/{process_id}", response_model=schemas.Process)
def delete_process(process_id: int, db: Session = Depends(get_db)):
    db_process = process_crud.get(db, process_id)
    if not db_process:
        raise HTTPException(status_code=404, detail="Process not found")
    return process_crud.remove(db, db_process)

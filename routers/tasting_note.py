from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud.tasting_note as tasting_note_crud
import schemas
from database import SessionLocal

router = APIRouter(prefix="/tasting-notes", tags=["tasting_notes"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.TastingNote])
def read_tasting_notes(page: int = 1, per_page: int = 50, db: Session = Depends(get_db)):
    skip = (page - 1) * per_page
    return tasting_note_crud.get_multi(db, skip=skip, limit=per_page)


@router.get("/{note_id}", response_model=schemas.TastingNote)
def read_tasting_note(note_id: int, db: Session = Depends(get_db)):
    db_note = tasting_note_crud.get(db, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Tasting note not found")
    return db_note


@router.post("/", response_model=schemas.TastingNote, status_code=201)
def create_tasting_note(note: schemas.TastingNoteCreate, db: Session = Depends(get_db)):
    return tasting_note_crud.create(db, note)


@router.put("/{note_id}", response_model=schemas.TastingNote)
def update_tasting_note(note_id: int, note: schemas.TastingNoteUpdate, db: Session = Depends(get_db)):
    db_note = tasting_note_crud.get(db, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Tasting note not found")
    return tasting_note_crud.update(db, db_note, note)


@router.delete("/{note_id}", response_model=schemas.TastingNote)
def delete_tasting_note(note_id: int, db: Session = Depends(get_db)):
    db_note = tasting_note_crud.get(db, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Tasting note not found")
    return tasting_note_crud.remove(db, db_note)

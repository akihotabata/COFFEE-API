from typing import List, Optional

from sqlalchemy.orm import Session

from crud import base
from models import TastingNote
from schemas import TastingNoteCreate, TastingNoteUpdate


def get(db: Session, note_id: int) -> Optional[TastingNote]:
    return base.get(db, TastingNote, note_id)


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[TastingNote]:
    return base.get_multi(db, TastingNote, skip, limit)


def create(db: Session, obj_in: TastingNoteCreate) -> TastingNote:
    return base.create(db, TastingNote, obj_in)


def update(db: Session, db_obj: TastingNote, obj_in: TastingNoteUpdate) -> TastingNote:
    return base.update(db, db_obj, obj_in)


def remove(db: Session, db_obj: TastingNote) -> TastingNote:
    return base.remove(db, db_obj)

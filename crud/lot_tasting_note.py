from typing import List

from sqlalchemy.orm import Session

from crud import base
from models import LotTastingNote
from schemas import LotTastingNoteCreate


def get(db: Session, lot_id: int, tasting_note_id: int) -> LotTastingNote:
    return (
        db.query(LotTastingNote)
        .filter(
            LotTastingNote.lot_id == lot_id,
            LotTastingNote.tasting_note_id == tasting_note_id,
        )
        .first()
    )


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[LotTastingNote]:
    return base.get_multi(db, LotTastingNote, skip, limit)


def create(db: Session, obj_in: LotTastingNoteCreate) -> LotTastingNote:
    return base.create(db, LotTastingNote, obj_in)


def remove(db: Session, db_obj: LotTastingNote) -> LotTastingNote:
    return base.remove(db, db_obj)

from typing import List

from sqlalchemy.orm import Session

from crud import base
from models import LotVariety
from schemas import LotVarietyCreate


def get(db: Session, lot_id: int, variety_id: int) -> LotVariety:
    return (
        db.query(LotVariety)
        .filter(LotVariety.lot_id == lot_id, LotVariety.variety_id == variety_id)
        .first()
    )


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[LotVariety]:
    return base.get_multi(db, LotVariety, skip, limit)


def create(db: Session, obj_in: LotVarietyCreate) -> LotVariety:
    return base.create(db, LotVariety, obj_in)


def remove(db: Session, db_obj: LotVariety) -> LotVariety:
    return base.remove(db, db_obj)

from typing import List, Optional

from sqlalchemy.orm import Session

from crud import base
from models import Variety
from schemas import VarietyCreate, VarietyUpdate


def get(db: Session, variety_id: int) -> Optional[Variety]:
    return base.get(db, Variety, variety_id)


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Variety]:
    return base.get_multi(db, Variety, skip, limit)


def create(db: Session, obj_in: VarietyCreate) -> Variety:
    return base.create(db, Variety, obj_in)


def update(db: Session, db_obj: Variety, obj_in: VarietyUpdate) -> Variety:
    return base.update(db, db_obj, obj_in)


def remove(db: Session, db_obj: Variety) -> Variety:
    return base.remove(db, db_obj)

from typing import List, Optional

from sqlalchemy.orm import Session

from crud import base
from models import Subregion
from schemas import SubregionCreate, SubregionUpdate


def get(db: Session, subregion_id: int) -> Optional[Subregion]:
    return base.get(db, Subregion, subregion_id)


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Subregion]:
    return base.get_multi(db, Subregion, skip, limit)


def create(db: Session, obj_in: SubregionCreate) -> Subregion:
    return base.create(db, Subregion, obj_in)


def update(db: Session, db_obj: Subregion, obj_in: SubregionUpdate) -> Subregion:
    return base.update(db, db_obj, obj_in)


def remove(db: Session, db_obj: Subregion) -> Subregion:
    return base.remove(db, db_obj)

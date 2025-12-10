from typing import List, Optional

from sqlalchemy.orm import Session

from crud import base
from models import Farm
from schemas import FarmCreate, FarmUpdate


def get(db: Session, farm_id: int) -> Optional[Farm]:
    return base.get(db, Farm, farm_id)


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Farm]:
    return base.get_multi(db, Farm, skip, limit)


def create(db: Session, obj_in: FarmCreate) -> Farm:
    return base.create(db, Farm, obj_in)


def update(db: Session, db_obj: Farm, obj_in: FarmUpdate) -> Farm:
    return base.update(db, db_obj, obj_in)


def remove(db: Session, db_obj: Farm) -> Farm:
    return base.remove(db, db_obj)

from typing import List, Optional

from sqlalchemy.orm import Session

from crud import base
from models import Lot
from schemas import LotCreate, LotUpdate


def get(db: Session, lot_id: int) -> Optional[Lot]:
    return base.get(db, Lot, lot_id)


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Lot]:
    return base.get_multi(db, Lot, skip, limit)


def create(db: Session, obj_in: LotCreate) -> Lot:
    return base.create(db, Lot, obj_in)


def update(db: Session, db_obj: Lot, obj_in: LotUpdate) -> Lot:
    return base.update(db, db_obj, obj_in)


def remove(db: Session, db_obj: Lot) -> Lot:
    return base.remove(db, db_obj)

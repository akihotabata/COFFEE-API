from typing import List, Optional

from sqlalchemy.orm import Session

from crud import base
from models import Region
from schemas import RegionCreate, RegionUpdate


def get(db: Session, region_id: int) -> Optional[Region]:
    return base.get(db, Region, region_id)


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Region]:
    return base.get_multi(db, Region, skip, limit)


def create(db: Session, obj_in: RegionCreate) -> Region:
    return base.create(db, Region, obj_in)


def update(db: Session, db_obj: Region, obj_in: RegionUpdate) -> Region:
    return base.update(db, db_obj, obj_in)


def remove(db: Session, db_obj: Region) -> Region:
    return base.remove(db, db_obj)

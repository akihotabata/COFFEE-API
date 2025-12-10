from typing import List, Optional

from sqlalchemy.orm import Session

from crud import base
from models import Country
from schemas import CountryCreate, CountryUpdate


def get(db: Session, country_id: int) -> Optional[Country]:
    return base.get(db, Country, country_id)


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Country]:
    return base.get_multi(db, Country, skip, limit)


def create(db: Session, obj_in: CountryCreate) -> Country:
    return base.create(db, Country, obj_in)


def update(db: Session, db_obj: Country, obj_in: CountryUpdate) -> Country:
    return base.update(db, db_obj, obj_in)


def remove(db: Session, db_obj: Country) -> Country:
    return base.remove(db, db_obj)

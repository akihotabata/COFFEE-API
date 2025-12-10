from typing import List, Optional

from sqlalchemy.orm import Session

from crud import base
from models import CuppingScore
from schemas import CuppingScoreCreate, CuppingScoreUpdate


def get(db: Session, score_id: int) -> Optional[CuppingScore]:
    return base.get(db, CuppingScore, score_id)


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[CuppingScore]:
    return base.get_multi(db, CuppingScore, skip, limit)


def create(db: Session, obj_in: CuppingScoreCreate) -> CuppingScore:
    return base.create(db, CuppingScore, obj_in)


def update(db: Session, db_obj: CuppingScore, obj_in: CuppingScoreUpdate) -> CuppingScore:
    return base.update(db, db_obj, obj_in)


def remove(db: Session, db_obj: CuppingScore) -> CuppingScore:
    return base.remove(db, db_obj)

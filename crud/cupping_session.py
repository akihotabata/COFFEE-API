from typing import List, Optional

from sqlalchemy.orm import Session

from crud import base
from models import CuppingSession
from schemas import CuppingSessionCreate, CuppingSessionUpdate


def get(db: Session, session_id: int) -> Optional[CuppingSession]:
    return base.get(db, CuppingSession, session_id)


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[CuppingSession]:
    return base.get_multi(db, CuppingSession, skip, limit)


def create(db: Session, obj_in: CuppingSessionCreate) -> CuppingSession:
    return base.create(db, CuppingSession, obj_in)


def update(db: Session, db_obj: CuppingSession, obj_in: CuppingSessionUpdate) -> CuppingSession:
    return base.update(db, db_obj, obj_in)


def remove(db: Session, db_obj: CuppingSession) -> CuppingSession:
    return base.remove(db, db_obj)

from typing import List, Optional

from sqlalchemy.orm import Session

from crud import base
from models import Process
from schemas import ProcessCreate, ProcessUpdate


def get(db: Session, process_id: int) -> Optional[Process]:
    return base.get(db, Process, process_id)


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Process]:
    return base.get_multi(db, Process, skip, limit)


def create(db: Session, obj_in: ProcessCreate) -> Process:
    return base.create(db, Process, obj_in)


def update(db: Session, db_obj: Process, obj_in: ProcessUpdate) -> Process:
    return base.update(db, db_obj, obj_in)


def remove(db: Session, db_obj: Process) -> Process:
    return base.remove(db, db_obj)

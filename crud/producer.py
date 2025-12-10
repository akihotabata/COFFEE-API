from typing import List, Optional

from sqlalchemy.orm import Session

from crud import base
from models import Producer
from schemas import ProducerCreate, ProducerUpdate


def get(db: Session, producer_id: int) -> Optional[Producer]:
    return base.get(db, Producer, producer_id)


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Producer]:
    return base.get_multi(db, Producer, skip, limit)


def create(db: Session, obj_in: ProducerCreate) -> Producer:
    return base.create(db, Producer, obj_in)


def update(db: Session, db_obj: Producer, obj_in: ProducerUpdate) -> Producer:
    return base.update(db, db_obj, obj_in)


def remove(db: Session, db_obj: Producer) -> Producer:
    return base.remove(db, db_obj)

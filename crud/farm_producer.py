from typing import List

from sqlalchemy.orm import Session

from crud import base
from models import FarmProducer
from schemas import FarmProducerCreate


def get(db: Session, farm_id: int, producer_id: int) -> FarmProducer:
    return (
        db.query(FarmProducer)
        .filter(FarmProducer.farm_id == farm_id, FarmProducer.producer_id == producer_id)
        .first()
    )


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[FarmProducer]:
    return base.get_multi(db, FarmProducer, skip, limit)


def create(db: Session, obj_in: FarmProducerCreate) -> FarmProducer:
    return base.create(db, FarmProducer, obj_in)


def remove(db: Session, db_obj: FarmProducer) -> FarmProducer:
    return base.remove(db, db_obj)

from typing import List

from sqlalchemy.orm import Session

from crud import base
from models import FarmCertification
from schemas import FarmCertificationCreate


def get(db: Session, farm_id: int, certification_id: int) -> FarmCertification:
    return (
        db.query(FarmCertification)
        .filter(
            FarmCertification.farm_id == farm_id,
            FarmCertification.certification_id == certification_id,
        )
        .first()
    )


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[FarmCertification]:
    return base.get_multi(db, FarmCertification, skip, limit)


def create(db: Session, obj_in: FarmCertificationCreate) -> FarmCertification:
    return base.create(db, FarmCertification, obj_in)


def remove(db: Session, db_obj: FarmCertification) -> FarmCertification:
    return base.remove(db, db_obj)

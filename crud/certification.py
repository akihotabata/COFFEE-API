from typing import List, Optional

from sqlalchemy.orm import Session

from crud import base
from models import Certification
from schemas import CertificationCreate, CertificationUpdate


def get(db: Session, certification_id: int) -> Optional[Certification]:
    return base.get(db, Certification, certification_id)


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Certification]:
    return base.get_multi(db, Certification, skip, limit)


def create(db: Session, obj_in: CertificationCreate) -> Certification:
    return base.create(db, Certification, obj_in)


def update(db: Session, db_obj: Certification, obj_in: CertificationUpdate) -> Certification:
    return base.update(db, db_obj, obj_in)


def remove(db: Session, db_obj: Certification) -> Certification:
    return base.remove(db, db_obj)

from typing import Any, Dict, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=Any)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=Any)


def get(db: Session, model: Type[ModelType], entity_id: int) -> Optional[ModelType]:
    return db.query(model).get(entity_id)


def get_multi(db: Session, model: Type[ModelType], skip: int = 0, limit: int = 100) -> List[ModelType]:
    return db.query(model).offset(skip).limit(limit).all()


def create(db: Session, model: Type[ModelType], obj_in: CreateSchemaType) -> ModelType:
    db_obj = model(**obj_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
    obj_data = obj_in.dict(exclude_unset=True)
    for field, value in obj_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, db_obj: ModelType) -> ModelType:
    db.delete(db_obj)
    db.commit()
    return db_obj

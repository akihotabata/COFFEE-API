from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud.cupping_score as score_crud
import schemas
from database import SessionLocal

router = APIRouter(prefix="/cupping-scores", tags=["cupping_scores"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.CuppingScore])
def read_scores(page: int = 1, per_page: int = 50, db: Session = Depends(get_db)):
    skip = (page - 1) * per_page
    return score_crud.get_multi(db, skip=skip, limit=per_page)


@router.get("/{score_id}", response_model=schemas.CuppingScore)
def read_score(score_id: int, db: Session = Depends(get_db)):
    db_score = score_crud.get(db, score_id)
    if not db_score:
        raise HTTPException(status_code=404, detail="Score not found")
    return db_score


@router.post("/", response_model=schemas.CuppingScore, status_code=201)
def create_score(score: schemas.CuppingScoreCreate, db: Session = Depends(get_db)):
    return score_crud.create(db, score)


@router.put("/{score_id}", response_model=schemas.CuppingScore)
def update_score(score_id: int, score: schemas.CuppingScoreUpdate, db: Session = Depends(get_db)):
    db_score = score_crud.get(db, score_id)
    if not db_score:
        raise HTTPException(status_code=404, detail="Score not found")
    return score_crud.update(db, db_score, score)


@router.delete("/{score_id}", response_model=schemas.CuppingScore)
def delete_score(score_id: int, db: Session = Depends(get_db)):
    db_score = score_crud.get(db, score_id)
    if not db_score:
        raise HTTPException(status_code=404, detail="Score not found")
    return score_crud.remove(db, db_score)

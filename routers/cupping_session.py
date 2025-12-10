from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud.cupping_session as session_crud
import schemas
from database import SessionLocal

router = APIRouter(prefix="/cupping-sessions", tags=["cupping_sessions"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.CuppingSession])
def read_sessions(page: int = 1, per_page: int = 50, db: Session = Depends(get_db)):
    skip = (page - 1) * per_page
    return session_crud.get_multi(db, skip=skip, limit=per_page)


@router.get("/{session_id}", response_model=schemas.CuppingSession)
def read_session(session_id: int, db: Session = Depends(get_db)):
    db_session = session_crud.get(db, session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return db_session


@router.post("/", response_model=schemas.CuppingSession, status_code=201)
def create_session(session: schemas.CuppingSessionCreate, db: Session = Depends(get_db)):
    return session_crud.create(db, session)


@router.put("/{session_id}", response_model=schemas.CuppingSession)
def update_session(session_id: int, session: schemas.CuppingSessionUpdate, db: Session = Depends(get_db)):
    db_session = session_crud.get(db, session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session_crud.update(db, db_session, session)


@router.delete("/{session_id}", response_model=schemas.CuppingSession)
def delete_session(session_id: int, db: Session = Depends(get_db)):
    db_session = session_crud.get(db, session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session_crud.remove(db, db_session)

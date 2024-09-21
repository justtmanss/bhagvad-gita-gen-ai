# routes.py
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from model import Chapter, Sloka
from database import SessionLocal

router = APIRouter()

@router.get("/chapters/")
def get_chapters():
    db: Session = SessionLocal()
    chapters = db.query(Chapter).all()
    return chapters

@router.get("/slokas/{chapter_id}")
def get_slokas(chapter_id: int):
    db: Session = SessionLocal()
    slokas = db.query(Sloka).filter(Sloka.chapter_id == chapter_id).all()
    if not slokas:
        raise HTTPException(status_code=404, detail="No slokas found for this chapter")
    return slokas

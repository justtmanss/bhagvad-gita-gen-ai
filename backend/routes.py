# routes.py
from fastapi import APIRouter
from models import Chapter, Sloka
from database import SessionLocal

router = APIRouter()

@router.get("/chapters/")
def get_chapters():
    db = SessionLocal()
    chapters = db.query(Chapter).all()
    return chapters

@router.get("/slokas/{chapter_id}")
def get_slokas(chapter_id: int):
    db = SessionLocal()
    slokas = db.query(Sloka).filter(Sloka.chapter_id == chapter_id).all()
    return slokas

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from model import Chapter, Sloka  # Adjust according to your models
import re

DATABASE_URI = 'postgresql://aakash:chootu@localhost/bhagavad_gita_explorer'
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def search_database(db: Session, query: str):
    results = []

    # Search chapters based on the query
    chapters = db.query(Chapter).filter(Chapter.title.ilike(f"%{query}%")).all()

    # If relevant chapters are found, look for related slokas
    for chapter in chapters:
        # Search for slokas in the found chapter
        slokas = db.query(Sloka).filter(Sloka.chapter_id == chapter.id, Sloka.sloka_text.ilike(f"%{query}%")).all()
        
        if slokas:
            for sloka in slokas:
                results.append((chapter, sloka))  # Append chapter with the relevant sloka
        else:
            results.append((chapter, None))  # Append chapter with None for sloka if none found

    return results

    # Search for chapters that match the query
    chapters = db.query(Chapter).filter(Chapter.title.ilike(f"%{query}%")).all()

    for chapter in chapters:
        results.append((chapter, None))  # Append chapter with None for sloka
        
        # Search for slokas in the found chapter
        slokas = db.query(Sloka).filter(Sloka.chapter_id == chapter.id, Sloka.sloka_text.ilike(f"%{query}%")).all()
        for sloka in slokas:
            results.append((chapter, sloka))  # Append chapter with the relevant sloka

    return results

Base = declarative_base()

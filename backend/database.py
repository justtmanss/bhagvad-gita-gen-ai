from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session
from model import Chapter, Sloka  # Adjust according to your models

DATABASE_URI = 'postgresql://aakash:chootu@localhost/bhagavad_gita_explorer'
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def search_database(db: Session, query: str):
    # Example logic to search chapters and slokas based on the query
    results = []
    
    # Search chapters based on the query
    chapters = db.query(Chapter).filter(Chapter.title.ilike(f"%{query}%")).all()
    
    for chapter in chapters:
        # If relevant chapters are found, look for related slokas
        slokas = db.query(Sloka).filter(Sloka.chapter_id == chapter.id).all()
        for sloka in slokas:
            results.append((chapter, sloka))

    return results


Base = declarative_base()

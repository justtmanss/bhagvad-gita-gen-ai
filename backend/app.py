# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router  # Import API routes
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Chapter, Sloka, Session  # Import the models and Session


app = FastAPI()

# Middleware to allow frontend (React) to access backend API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity; you can restrict this later.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Bhagavad Gita Explorer"}

# Include API routes from routes.py
app.include_router(router)

# Set up the SQLAlchemy database connection
DATABASE_URI = 'postgresql://aakash:chootu@localhost/bhagavad_gita_explorer'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

@app.route('/chapters', methods=['GET'])
def get_chapters():
    session = Session()
    chapters = session.query(Chapter).all()
    session.close()
    
    # Convert chapters to a list of dictionaries
    return jsonify([{
        'id': chapter.id,
        'title': chapter.title,
        'chapter_number': chapter.chapter_number,
        'verse_count': chapter.verse_count,
        'language': chapter.language,
        'yoga_name': chapter.yoga_name,
        'meaning': chapter.meaning,
        'summary': chapter.summary
    } for chapter in chapters])

@app.route('/slokas/<int:chapter_number>', methods=['GET'])
def get_slokas_by_chapter(chapter_number):
    session = Session()
    chapter = session.query(Chapter).filter_by(chapter_number=chapter_number).first()
    if not chapter:
        return jsonify({'error': 'Chapter not found'}), 404
    
    slokas = session.query(Sloka).filter_by(chapter_id=chapter.id).all()
    session.close()

    return jsonify([{
        'id': sloka.id,
        'sloka_text': sloka.sloka_text,
        'meaning': sloka.meaning,
        'speaker': sloka.speaker,
        'language': sloka.language
    } for sloka in slokas])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

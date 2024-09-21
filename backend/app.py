# app.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from routes import router  # Import API routes
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Chapter, Sloka, Session  # Import the models and Session
from sqlalchemy.orm import Session
from database import SessionLocal, search_database  # Import your functions
import openai


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

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/ask/")
async def ask_question(query: str, db: Session = Depends(get_db)):
    # Search the database for relevant content
    results = search_database(db, query)

    if results:
        # Format the results to send to OpenAI
        formatted_results = format_results(results)

        # Call OpenAI API for further processing
        openai_response = call_openai_api(formatted_results)
        return {"answer": openai_response}
    else:
        raise HTTPException(status_code=404, detail="No relevant information found.")

def format_results(results):
    # Format your results from the database for OpenAI
    return " ".join([f"{chapter.title}: {sloka.sloka_text}" for chapter, sloka in results])

def call_openai_api(formatted_results):
    # Make a call to OpenAI's API
    openai.api_key = "sk-jBF7Zi4kRM8VCc0xU25UbCGAuP4fipWe8jAVRiHzTQT3BlbkFJrxFL5I-o3gJn6H-B4ineZnsJ7C-MXvR_0oZyRMUV0A"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": formatted_results}
        ]
    )
    return response['choices'][0]['message']['content']

@app.post("/ask/")
async def ask_question(query: str):
    answer = handle_user_query(query)
    return {"answer": answer}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

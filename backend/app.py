from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session  # Ensure Session is imported here
from model import Chapter, Sloka  # Ensure models are correctly imported
from database import SessionLocal, search_database  # Import your functions
import openai
from pydantic import BaseModel  # Add this import


app = FastAPI()

# Middleware to allow frontend (React) to access backend API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity; you can restrict this later.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Bhagavad Gita Explorer"}

# Define a Pydantic model for the query
class Query(BaseModel):
    query: str
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
    openai.api_key = "YOUR_API_KEY"  # Replace with your actual API key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": formatted_results}
        ]
    )
    return response['choices'][0]['message']['content']

# SQLAlchemy database setup
DATABASE_URI = 'postgresql://aakash:chootu@localhost/bhagavad_gita_explorer'
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

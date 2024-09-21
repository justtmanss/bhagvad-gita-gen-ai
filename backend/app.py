from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from model import Chapter, Sloka
from database import SessionLocal, search_database
import openai
from pydantic import BaseModel

app = FastAPI()

# Middleware to allow frontend to access backend API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
async def ask_question(query: Query, db: Session = Depends(get_db)):
    # Search the database for relevant content
    results = search_database(db, query.query)

    if results:
        # Format the results to send to OpenAI
        formatted_results = format_results(results)

        # Call OpenAI API for further processing
        openai_response = call_openai_api(formatted_results)
        return {"answer": openai_response}
    else:
        raise HTTPException(status_code=404, detail="No relevant information found.")

def format_results(results):
    if not results:
        return "No relevant content found."

    response_lines = []
    for item in results:
        if isinstance(item, tuple) and len(item) == 2:  # Ensure item is a tuple with two elements
            chapter, sloka = item
            if sloka:  # If there's a sloka
                response_lines.append(f"In Chapter {chapter.title}, Sloka: {sloka.sloka_text}")
            else:  # If only a chapter is found without a sloka
                response_lines.append(f"In Chapter {chapter.title}, no specific sloka matches the query.")
        else:
            response_lines.append("Unexpected result format.")

    return "\n".join(response_lines)


def call_openai_api(formatted_results):
    # Make a call to OpenAI's API
    openai.api_key = "sk-jBF7Zi4kRM8VCc0xU25UbCGAuP4fipWe8jAVRiHzTQT3BlbkFJrxFL5I-o3gJn6H-B4ineZnsJ7C-MXvR_0oZyRMUV0A"  # Replace with your actual API key
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

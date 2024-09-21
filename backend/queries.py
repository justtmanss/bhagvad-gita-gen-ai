# queries.py or services.py
from openai_api import ask_openai
from langsmith_api import ask_langsmith
from database import search_database, get_db
from sqlalchemy.orm import Session

def handle_user_query(query: str, db: Session):
    # Search the local database for relevant information
    results = search_database(db, query)

    if results:
        return format_results(results)
    else:
        # Fallback to external APIs if no local results found
        response = ask_openai(query)
        if not response:
            response = ask_langsmith(query)
        return response

def format_results(results):
    # Format the results from the database search to return as an answer
    formatted_answer = ""
    for chapter, sloka in results:
        formatted_answer += f"Chapter {chapter.chapter_number} - {chapter.title}: {sloka.text}\n"
    return formatted_answer

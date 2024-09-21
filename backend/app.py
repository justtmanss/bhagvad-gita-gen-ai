# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router  # Import API routes

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

import json
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

# Set up the SQLAlchemy database connection to the bhagavad_gita_explorer database
DATABASE_URI = 'postgresql://aakash:chootu@localhost/bhagavad_gita_explorer'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Define the base model
Base = declarative_base()

# Define the Chapter model
class Chapter(Base):
    __tablename__ = 'chapters'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    chapter_number = Column(Integer, unique=True, nullable=False)
    verse_count = Column(Integer, nullable=False)
    language = Column(String, nullable=False)
    yoga_name = Column(String, nullable=False)
    meaning = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)

# Define the Sloka model
class Sloka(Base):
    __tablename__ = 'slokas'

    id = Column(Integer, primary_key=True)
    chapter_id = Column(Integer, ForeignKey('chapters.id'), nullable=False)
    sloka_text = Column(Text, nullable=False)
    meaning = Column(Text, nullable=True)
    speaker = Column(String, nullable=False)
    language = Column(String, nullable=False)

# Create tables in the database
Base.metadata.create_all(engine)

# Close the session
session.close()

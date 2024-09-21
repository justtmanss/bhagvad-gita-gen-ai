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

# Load chapters data from JSON file
with open('/Users/aakashvenkatraman/Documents/GitHub/bahgvad-gita-gen-ai/backend/database/data/genai.chapter.json', 'r', encoding='utf-8') as chapter_file:
    chapters_data = json.load(chapter_file)

# Insert chapters
for chapter in chapters_data:
    existing_chapter = session.query(Chapter).filter_by(chapter_number=chapter['chapterNumber']).first()
    if not existing_chapter:  # Check if chapter already exists
        new_chapter = Chapter(
            title=chapter['chapterName'],
            chapter_number=chapter['chapterNumber'],
            verse_count=chapter['verseCount'],
            language=chapter['language'],
            yoga_name=chapter['yogaName'],
            meaning=chapter['meaning'],
            summary=chapter['summary']
        )
        session.add(new_chapter)
    else:
        print(f"Chapter {chapter['chapterNumber']} already exists, skipping.")

session.commit()  # Commit to get chapter IDs

# Load slokas data from JSON file
with open('/Users/aakashvenkatraman/Documents/GitHub/bahgvad-gita-gen-ai/backend/database/data/genai.sloka.json', 'r', encoding='utf-8') as sloka_file:
    slokas_data = json.load(sloka_file)

# Insert slokas related to the chapters
for sloka in slokas_data:
    chapter_id = session.query(Chapter.id).filter_by(chapter_number=sloka['chapterNumber']).first()
    if chapter_id:
        new_sloka = Sloka(
            chapter_id=chapter_id[0],
            sloka_text=sloka['sloka'],
            meaning=sloka['meaning'],
            speaker=sloka['speaker'],
            language=sloka['language']
        )
        session.add(new_sloka)

# Commit all changes for slokas
session.commit()

# Close the session
session.close()

print("Data loaded successfully into bhagavad_gita_explorer database.")

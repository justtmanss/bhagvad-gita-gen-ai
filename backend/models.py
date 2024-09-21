# models.py
from sqlalchemy import Column, Integer, String, Text
from database import Base

class Chapter(Base):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    summary = Column(Text)

class Sloka(Base):
    __tablename__ = "slokas"
    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, index=True)
    sloka_text = Column(Text)
    meaning = Column(Text)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slokas = db.relationship('Sloka', backref='chapter', lazy=True)

class Sloka(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)

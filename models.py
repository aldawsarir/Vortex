from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    uploads = db.relationship('Upload', backref='user', lazy=True)
    quiz_results = db.relationship('QuizResult', backref='user', lazy=True)
    battle_participations = db.relationship('BattleParticipant', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    is_shared = db.Column(db.Boolean, default=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    reviews = db.relationship('Review', backref='upload', lazy=True)

class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class DailyChallenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    points = db.Column(db.Integer, default=50)
    date = db.Column(db.Date, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)

class QuizBattle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='active')
    winner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    participants = db.relationship('BattleParticipant', backref='battle', lazy=True)

class BattleParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    battle_id = db.Column(db.Integer, db.ForeignKey('quiz_battle.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    upload_id = db.Column(db.Integer, db.ForeignKey('upload.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PuzzleGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    scrambled_words = db.Column(db.Text, nullable=False)
    score = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import ENUM
import json
db = SQLAlchemy()


# Student Model
class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    std = db.Column(db.String(10), nullable=False)
    age = db.Column(db.String(10), nullable=False)

    # Relationship with Profile and Marks
    profile = db.relationship('Profile', backref='student', uselist=False)
    marks = db.relationship('Marks', backref='student', lazy=True)

    def __init__(self, name, gender, std, age):
        self.name = name
        self.gender = gender
        self.std = std
        self.age = age

# Profile Model
class Profile(db.Model):
    __tablename__ = 'profile'
    profile_id = db.Column(db.Integer, primary_key=True, nullable=False)
    st_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    overall_percentage = db.Column(db.Float, nullable=False)
    type_of_learner = db.Column(db.String(50), nullable=True)
    # Using TEXT to store JSON data
    hobbies = db.Column(db.Text, nullable=True)
    # Using TEXT to store JSON data
    favorite_subjects = db.Column(db.Text, nullable=True)
    # Using TEXT to store JSON data
    recommended_subjects = db.Column(db.Text, nullable=True)
    carrier_interest = db.Column(db.String(100), nullable=True)
    predicted_career = db.Column(db.String(100), nullable=True)

    def __init__(self, st_id, overall_percentage, type_of_learner, hobbies, favorite_subjects, carrier_interest, recommended_subjects, predicted_career):
        self.st_id = st_id
        self.overall_percentage = overall_percentage
        self.type_of_learner = type_of_learner
        self.hobbies = json.dumps(hobbies)  # Converting list to JSON string
        self.favorite_subjects = json.dumps(
            favorite_subjects)  # Converting list to JSON string
        self.recommended_subjects = json.dumps(
            recommended_subjects)  # Converting list to JSON string
        self.carrier_interest = carrier_interest
        self.predicted_career = predicted_career

# Marks Model
class Marks(db.Model):
    __tablename__ = 'marks'
    mark_id = db.Column(db.Integer, primary_key=True, nullable=False)
    st_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject = db.Column(ENUM('math', 'science', 'english',
                        'socialScience', 'hindi'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __init__(self, st_id, subject, score):
        self.st_id = st_id
        self.subject = subject
        self.score = score

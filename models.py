from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()

class Participant(db.Model):
    __tablename__ = 'participants'
    
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.String(64), unique=True, nullable=False, index=True) # Reg No / Student ID
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, index=True)
    college = db.Column(db.String(256), nullable=False, index=True)
    department = db.Column(db.String(128), nullable=False)
    year = db.Column(db.String(32), nullable=False)
    team_name = db.Column(db.String(128), nullable=True)
    session_token = db.Column(db.String(128), nullable=True)
    
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    r1_started_at = db.Column(db.DateTime, nullable=True)
    r1_completed_at = db.Column(db.DateTime, nullable=True)
    r1_score = db.Column(db.Float, default=0.0)
    
    r2_started_at = db.Column(db.DateTime, nullable=True)
    r2_completed_at = db.Column(db.DateTime, nullable=True)
    r2_score = db.Column(db.Float, default=0.0)
    
    total_score = db.Column(db.Float, default=0.0)
    total_time_seconds = db.Column(db.Integer, default=0)
    status = db.Column(db.String(32), default='registered') # registered, round1_active, round1_completed, round2_active, completed
    
    submissions = db.relationship('Submission', backref='participant', lazy='dynamic', cascade='all, delete-orphan')
    activities = db.relationship('SuspiciousActivity', backref='participant', lazy='dynamic', cascade='all, delete-orphan')
    
    def update_totals(self):
        self.total_score = round((self.r1_score or 0.0) + (self.r2_score or 0.0), 2)
        r1_time = 0
        if self.r1_started_at and self.r1_completed_at:
            r1_time = max(0, int((self.r1_completed_at - self.r1_started_at).total_seconds()))
        r2_time = 0
        if self.r2_started_at and self.r2_completed_at:
            r2_time = max(0, int((self.r2_completed_at - self.r2_started_at).total_seconds()))
        self.total_time_seconds = r1_time + r2_time

    @property
    def formatted_time(self):
        mins = self.total_time_seconds // 60
        secs = self.total_time_seconds % 60
        return f"{mins:02d}:{secs:02d}"


class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    round = db.Column(db.Integer, nullable=False, index=True) # 1 or 2
    language = db.Column(db.String(32), nullable=False) # 'python' or 'java'
    difficulty = db.Column(db.String(32), default='Medium') # Medium, Hard
    order_num = db.Column(db.Integer, default=1)
    title = db.Column(db.String(256), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    buggy_code = db.Column(db.Text, nullable=False)
    correct_code = db.Column(db.Text, nullable=False)
    error_type = db.Column(db.String(128), nullable=True) # e.g. "Logical Error", "Runtime Error"
    explanation = db.Column(db.Text, nullable=True)
    test_cases_json = db.Column(db.Text, default='[]')
    points = db.Column(db.Float, default=5.0)
    
    java_errors = db.relationship('JavaError', backref='question', lazy='joined', cascade='all, delete-orphan', order_by='JavaError.error_number')
    submissions = db.relationship('Submission', backref='question', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def test_cases(self):
        try:
            return json.loads(self.test_cases_json or '[]')
        except Exception:
            return []

    @test_cases.setter
    def test_cases(self, val):
        self.test_cases_json = json.dumps(val)


class JavaError(db.Model):
    __tablename__ = 'java_errors'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    error_number = db.Column(db.Integer, nullable=False) # 1 to 7
    error_category = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    buggy_snippet = db.Column(db.Text, nullable=False)
    fixed_snippet = db.Column(db.Text, nullable=False)
    detection_rule = db.Column(db.Text, nullable=True) # Check rule key/regex
    points = db.Column(db.Float, default=2.0)


class Submission(db.Model):
    __tablename__ = 'submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id', ondelete='CASCADE'), nullable=False, index=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False, index=True)
    round = db.Column(db.Integer, nullable=False)
    submitted_code = db.Column(db.Text, nullable=False)
    score = db.Column(db.Float, default=0.0)
    errors_fixed_count = db.Column(db.Integer, default=0) # For Java Round (0 to 7)
    status = db.Column(db.String(32), default='failed') # passed, failed, partial
    test_results_json = db.Column(db.Text, default='{}')
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def test_results(self):
        try:
            return json.loads(self.test_results_json or '{}')
        except Exception:
            return {}

    @test_results.setter
    def test_results(self, val):
        self.test_results_json = json.dumps(val)


class Competition(db.Model):
    __tablename__ = 'competition'
    
    id = db.Column(db.Integer, primary_key=True)
    r1_duration_minutes = db.Column(db.Integer, default=30)
    r2_duration_minutes = db.Column(db.Integer, default=30)
    r1_enabled = db.Column(db.Boolean, default=True)
    r2_enabled = db.Column(db.Boolean, default=True)
    r1_points_per_question = db.Column(db.Float, default=5.0)
    r2_points_per_question = db.Column(db.Float, default=14.0)
    r2_points_per_error = db.Column(db.Float, default=2.0)
    allow_answer_review = db.Column(db.Boolean, default=False)
    anti_cheat_enabled = db.Column(db.Boolean, default=True)


class SuspiciousActivity(db.Model):
    __tablename__ = 'suspicious_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id', ondelete='CASCADE'), nullable=False, index=True)
    event = db.Column(db.String(128), nullable=False)
    details = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

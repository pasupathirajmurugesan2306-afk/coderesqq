import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'coderesq-super-secret-key-2026-prod-dbg')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'coderesq.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Competition Defaults
    R1_DURATION_MINUTES = 30
    R2_DURATION_MINUTES = 30
    R1_POINTS_PER_QUESTION = 5.0  # 20 questions * 5 = 100 marks
    R2_POINTS_PER_QUESTION = 14.0 # 5 questions * 14 = 70 marks (2 marks per error)
    R2_POINTS_PER_ERROR = 2.0
    
    # Execution timeouts
    CODE_EXECUTION_TIMEOUT = 5 # seconds

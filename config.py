import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY environment variable is not set")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'coderesq.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Competition Defaults
    R1_DURATION_MINUTES = 30
    R2_DURATION_MINUTES = 30
    R1_POINTS_PER_QUESTION = 5.0
    R2_POINTS_PER_QUESTION = 14.0
    R2_POINTS_PER_ERROR = 2.0

    # Execution timeouts
    CODE_EXECUTION_TIMEOUT = 5

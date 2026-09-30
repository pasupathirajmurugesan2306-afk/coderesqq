from app import app
from seed_data import seed_database

with app.app_context():
    seed_database()
    print("Seeding applied.")

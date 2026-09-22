import os
from flask import Flask
from config import Config
from models import db
from seed_data import seed_database

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure instance folder exists
    instance_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
    os.makedirs(instance_dir, exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.participant import participant_bp
    from routes.competition import competition_bp
    from routes.admin import admin_bp
    from routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(participant_bp)
    app.register_blueprint(competition_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # Context processors for templates
    @app.context_processor
    def inject_global_vars():
        from models import Competition
        comp = Competition.query.first()
        return dict(global_comp=comp)

    # Initialize Database & Seed
    with app.app_context():
        db.create_all()
        seed_database()

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

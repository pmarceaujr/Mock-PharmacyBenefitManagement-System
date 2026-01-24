from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
from pathlib import Path
import os

# -----------------------------
# Point to .env file and verify its existence
# -----------------------------
env_path = Path("Config") / ".env"

if env_path.exists():   # check if file exists
    load_dotenv(dotenv_path=env_path)
else:
    print(f"Warning: {env_path} does not exist, skipping env load")


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def create_app(config_name='development'):
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True if config_name == 'development' else False
    
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    CORS(app)
    
    with app.app_context():
        from app.routes import claims, members, drugs, pharmacies, analytics, reports
        
        app.register_blueprint(claims.bp)
        app.register_blueprint(members.bp)
        app.register_blueprint(drugs.bp)
        app.register_blueprint(pharmacies.bp)
        app.register_blueprint(analytics.bp)
        app.register_blueprint(reports.bp)
    
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'message': 'the Mock-PBM System API is healthy, maybe not wealthy, but very wise'}, 200
    
    @app.route('/')
    def index():
        return {
            'message': 'Welcome to the Mock-PBM System API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/health',
                'claims': '/api/claims',
                'members': '/api/members',
                'drugs': '/api/drugs',
                'pharmacies': '/api/pharmacies',
                'analytics': '/api/analytics',
                'reports': '/api/reports'
            }
        }, 200
    
    return app

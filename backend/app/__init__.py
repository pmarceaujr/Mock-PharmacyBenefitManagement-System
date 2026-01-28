from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
from pathlib import Path
from app.config import *
import os

# -----------------------------
# Point to .env file and verify its existence
# -----------------------------
env_path = Path("local_config") / ".env"
print(f"Current Dir:{os.getcwd()}")

if env_path.exists():   # check if file exists
    load_dotenv(dotenv_path=env_path)
else:
    print(f"Warning: {env_path} does not exist, skipping env load")


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def create_app(config_name='development'):
    # Create app with instance folder support
    app = Flask(__name__, instance_relative_config=True)

    # Read environment variable (default to "development")
    env = os.getenv("FLASK_ENV", "development")
    print(f"Starting app in {env} mode...")
    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    app.config.from_pyfile('config.py', silent=True)

    if env == "production":
        app.config.update({'DATABASE_URL': app.config.get('DATABASE_URL')})

    # Heroku PostgreSQL URLs start with postgres:// but SQLAlchemy needs postgresql://
    if app.config['SQLALCHEMY_DATABASE_URI'] and app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)
            

    app.config.update({
        # Security / Auth
        'SECRET_KEY': os.environ.get('SECRET_KEY') or app.config.get('SECRET_KEY'),
        'JWT_SECRET_KEY': os.environ.get('JWT_SECRET_KEY') or app.config.get('JWT_SECRET_KEY'),
        'JWT_ALGORITHM': os.environ.get('JWT_ALGORITHM') or app.config.get('JWT_ALGORITHM'), 
        'JWT_ACCESS_TOKEN_EXPIRES': int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600)) or app.config.get('JWT_ACCESS_TOKEN_EXPIRES'),

        # SQL ALchemy
        'SQLALCHEMY_DATABASE_URI': os.getenv('DATABASE_URL'),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ECHO': True if config_name == 'development' else False,

        # Server / Flask
        'PORT': os.environ.get('PORT')  or app.config.get('PORT'),

        # Database (most important on Heroku!)
        'DATABASE_URL': os.environ.get('DATABASE_URL') or app.config.get('DATABASE_URL'),
        # Very important: Heroku forces SSL on Postgres
        # 'SQLALCHEMY_ENGINE_OPTIONS': {'connect_args': {'sslmode': 'require'}} if 'DATABASE_URL' in os.environ else None,
    })

    # ───────────────────────────────────────────────
    print("┌──────────── Loaded config from────────────┐")
    for key, value in sorted(app.config.items()):
        if not key.isupper(): continue           # skip Flask internal stuff
        if key in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_DEFAULT_REGION', 'JWT_SECRET_KEY', 'DATABASE_URL_PROD', 'OPENAI_API_KEY', 'SECRET_KEY', 'SQLALCHEMY_DATABASE_URI','DATABASE_URL']:
             print(f"│ {key: <28} : {'*' * 8} (hidden)")
        else:
            print(f"│ {key: <28} : {value!r}")
    print("└────────────────────────────────────────────────────────────┘")   
    print(f"database url: {app.config.get('DATABASE_URL')[-10:]} (last 10 chars shown)")     
    print(f"SQLALCHEMY_DATABASE_URI: {app.config.get('SQLALCHEMY_DATABASE_URI')[-10:]} (last 10 chars shown)")

 # Use Postgres on Heroku, SQLite locally
    DATABASE_URL = app.config.get('DATABASE_URL')

    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        # Heroku provides "postgres://" but SQLAlchemy wants "postgresql://"
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
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
        return {'status': 'running', 'message': 'the Mock-PBM System API is healthy, maybe not wealthy, but very wise'}, 200
    
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

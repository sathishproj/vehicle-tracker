import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///vehicle_tracking.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    login_manager.init_app(app)
    from app.auth.routes import auth_bp
    from app.dashboard.routes import dashboard_bp
    from app.tracking.routes import tracking_bp
    from app.geofence.routes import geofence_bp
    from app.reports.routes import reports_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(tracking_bp, url_prefix='/tracking')
    app.register_blueprint(geofence_bp, url_prefix='/geofence')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    return app

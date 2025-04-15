import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# Setup database base class
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with the base class
db = SQLAlchemy(model_class=Base)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # Needed for url_for to generate with https

# Configure the database
# Use PostgreSQL from environment or fallback to SQLite
database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    # Adjust postgresql URLs for SQLAlchemy 1.4+
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url or "sqlite:///kogabe.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Log the database connection type (without credentials)
logging.info(f"Database type: {'PostgreSQL' if database_url else 'SQLite'}")

# Initialize the app with the extension
db.init_app(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

# Import this here to avoid circular imports
import models
import routes
import auth

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(models.User, int(user_id))

# Create all database tables
with app.app_context():
    try:
        db.create_all()
        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Database initialization error: {str(e)}")
        raise
    
    # Create default admin user if not exists
    admin = models.User.query.filter_by(username="Dinesh").first()
    if not admin:
        from werkzeug.security import generate_password_hash
        admin = models.User(
            username="Dinesh",
            email="admin@kogabe.com",
            password_hash=generate_password_hash("!@#$%^&*")
        )
        db.session.add(admin)
        db.session.commit()
        logging.info("Default admin user created")

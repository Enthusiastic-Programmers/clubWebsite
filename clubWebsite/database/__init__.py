"""SQLAlchemy and Migrate instance"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()   #: flask-SQLAlchemy instance. db.session can be used to access the current session
migrate = Migrate() #: Alembic database migration integration

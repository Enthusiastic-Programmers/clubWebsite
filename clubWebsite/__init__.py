from flask import Flask
from clubWebsite.routes import views_blueprint
from clubWebsite.database import db, migrate
from clubWebsite.database.models import Member

def create_instance(configClass):
    """
    Creates a Flask application instance, loads configuration from the given config obj, 
    and initializes the database ORMs, blueprints, and other flask plugins. 
    """
    instance = Flask(__name__)
    instance.config.from_object(configClass)

    db.init_app(instance)
    migrate.init_app(instance, db)

    instance.register_blueprint(views_blueprint)
    return instance

def add_context(instance):
    """Adds shell context to the given Flask instance"""
    def make_context():
        return {'db':db, 'migrate':migrate, 'Member':Member}
    instance.shell_context_processor(make_context)
    return instance
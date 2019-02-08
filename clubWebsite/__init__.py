from flask import Flask
from clubWebsite.routes import views_blueprint
from clubWebsite.database import db, migrate
from clubWebsite.database.models import Member

def create_instance(configClass):
    instance = Flask(__name__)
    instance.config.from_object(configClass)

    db.init_app(instance)
    migrate.init_app(instance, db)

    instance.register_blueprint(views_blueprint)
    return instance

def add_context(instance):
    def make_context():
        return {'db':db, 'migrate':migrate, 'Member':Member}
    instance.shell_context_processor(make_context)
    return instance
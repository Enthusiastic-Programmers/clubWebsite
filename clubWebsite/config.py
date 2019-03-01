"""Configuration defaults; overloaded from environment variables and .env"""
import os
import pathlib
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(str(pathlib.Path('.env')))

SQLALCHEMY_DEFAULT_URI = 'sqlite:///' +  os.path.join(os.getcwd(), 'students.db')

class BaseConfig:
    """Default configurations"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False #: Disable for better performance
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or SQLALCHEMY_DEFAULT_URI #: Connection URI for SQL database
                              
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ChangeMeInProd!' #: Unique key for session and CSRF protection

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

    SECRET_KEY = os.environ.get('SECRET_KEY') #: Unique key for session and CSRF protection
    if SECRET_KEY is None:
        print("Warning: SECRET_KEY not found in environment. Using default.")
        SECRET_KEY = 'ChangeMeInProd!'

    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    if SENDGRID_API_KEY is None:
        print("Warning: SENDGRID_API_KEY not found in environment. Confirmation emails will not work.")


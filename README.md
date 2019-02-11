# clubWebsite
Moorpark Enthusiastic Programmers Club website

The purpose is to have a website for the club for easy sign up, and easy access to more club information and announcments.
We.Love.Hackathons.


Link to website: https://enthusiastic-programmers.github.io/clubWebsite/

## Setting up a development environment

1) Clone this repository

2) Create a python virtual environment

   `python -m venv venv`

3) Activate the virtual environment

    Linux: `source venv/bin/activate`

    Windows: `venv/Scripts/activate.bat`

4) Install dependencies

   `pip install -r requirements.txt`

5) Initialize the database tables:
   
   `flask db upgrade`

6) Run flask development server

   `python wsgi.py`
   
   Note: The development server will automatically reload source files when it detects an
   updated file on the disk. 

7) Or, run the flask server with debug mode disabled

   `flask run`
   
   Note: This command is not sufficient for running the website in production.
    
## Making changes to the database models

This project uses SQLAlchemy to manage database ORMs (Object-Relational Models).
Each model in `clubWebsite/database/models.py` is mapped to at least one table, where 
properties of that model represent database columns. SQLAlchemy generates SQL statements,
and handles creating/destroying sessions.

The database also uses Alembic (provided by flask-migrate) for generating database migrations.
Migrations are effectively scripts that describe the changes in database tables/columns over time,
providing version control for database layouts. 

When changing or adding database models, in order to use them in your application run

`flask db migrate -m "<migration descriptive name here>"`

to generate a new migration script. This behaves similarly to a git commit in that the
generated script will look at the current database structure, and compare it to the structure
described by the ORM models. It will automatically generate a migration script in `migrations/versions/`
with the generated `upgrade()` and `downgrade()` functions. It is often necessary to manually edit
or add extra code to facilitate with data migration. Examples of code that needs to be edited manually
include transforming types from one form to another (E.G. converting a string to an int, and vice versa). 

After generating the migration script, you need to run 

`flask db upgrade`

 to apply the database migrations. 
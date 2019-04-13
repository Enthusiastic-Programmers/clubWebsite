# clubWebsite
Moorpark Enthusiastic Programmers Club website

The purpose is to have a website for the club for easy sign up, and easy access to more club information and announcments.
We.Love.Hackathons.


Link to website: https://epclub.pythonanywhere.com/

## Setting up a development environment

1) Clone this repository

2) Create a python virtual environment

   `python -m venv venv`

3) Activate the virtual environment

    Linux: `source venv/bin/activate`

    Windows: `venv\Scripts\activate.bat`

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

 # Deploying on PythonAnywhere

 ## PythonAnywhere Flask Code Setup

 1) Create a PythonAnywhere account and login

 2) Under the Dashboard tab -> Consoles start a new bash console

 3) Clone the clubWebsite repo: 

    `git clone https://github.com/Enthusiastic-Programmers/clubWebsite`

    `cd clubWebsite/`

 4) Switch to the flask-server branch

     `git checkout flask-server`

 5) Create a virtual environment

    `python3 -m venv prod_venv`

 6) Enter the virtual environment
    
    `source prod_venv/bin/activate`

 7) Install python dependencies in the virtual environment

    `pip install -r requirements.txt`

 8) Create the database
    
    `flask db upgrade`

 9) Close the console

    `exit`


 ## PythonAnywhere Flask App Setup

 1) Go to the `Web Apps` tab in your PythonAnywhere account

 3) Click `Add a new web app`

 4) Set the domain name (or leave it as the default of <username>.pythonanywhere.com)

 5) On the `Select a Python Web Framework` select `Manual configuration`

 6) Select the python version `3.7`

 7) Click `Next` to generate a sample WSGI configuration file (we will edit this later)

 8) Under the `Code` section of the web app, se the `Source Code` directory and the `Working Directory` to `/home/<username>/clubWebsite` 


 9) Under the `Virtualenv` tab, set the virtualenv directory to `/home/<username>/clubWebsite/prod_venv`

 10) Under `Static files`, add a static location with the url `/static` and the path `/home/<username>/clubWebsite/clubWebsite/static`

 11) Under `Security`, set `Force HTTPS` to Enabled

 12) Under the `Code` section, click the `WSGI Configuration File` to edit it

 13) Delete the existing contents of the WSGI Configuration File and replace it with:
 
    
    import sys
    path = '/home/<username>/clubWebsite'
    if path not in sys.path:
        sys.path.append(path)

    from wsgi import app as application  
    
    
 14) Save the WSGI Configuration File, and click the Reload button to reload the site configuration

 ## Updating an already configured site

 1) Under the Dashboard tab -> Consoles start a new bash console (or click on an existing one)

 2) CD into the git repo:

    `cd /home/<username>/clubWebsite`

 3) Pull changes

    `git pull`

 4) Run database migrations (Important!)
    
    `flask db upgrade`

 4) Close the console

    `exit`

 5) Reload the web app

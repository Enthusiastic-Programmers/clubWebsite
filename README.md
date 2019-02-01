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

5) Run flask development server

   `python wsgi.py`
   
   Note: The development server will automatically reload source files when it detects an
   updated file on the disk. 

6) Or, run the flask server with debug mode disabled

   `flask run`
   
   Note: This command is not sufficient for running the website in production.
    

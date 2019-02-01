from string import Template
import os
import sqlite3

database_path = os.path.normpath('./data/members.sqlite')

with open('./template.html', 'r', encoding='utf-8') as f:
    basic_template = Template(f.read())

def error_page(environ, start_response, message, code='400 Bad Request'):
    start_response(code, [('Content-Type', 'text/html')])
    yield basic_template.substitute(title='Error', main='Error: ' + message).encode('utf-8')

def open_database():
    database_directory = os.path.dirname(database_path)
    if not os.path.exists(database_directory):
        os.makedirs(database_directory)
    return sqlite3.connect(database_path)

def check_database(connection):
    cursor = connection.cursor()
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    if 'members' not in (row[0] for row in tables):
        cursor.execute('''CREATE TABLE members (
                                email text PRIMARY KEY NOT NULL,
                                student_id text NOT NULL,
                                first_name text NOT NULL,
                                last_name text NOT NULL,
                                time_added real,
                                confirmation_token text,
                                confirmed boolean
                                )''')

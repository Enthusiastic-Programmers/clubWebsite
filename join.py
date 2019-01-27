import urllib
import re
from email.utils import parseaddr
import os
import html
import time
import sqlite3
import secrets
import common, email_confirmation

# https://stackabuse.com/a-sqlite-tutorial-with-python/


def _check_database(connection):
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

def iterlength(iterable):
    ''' Return length of finite iterable '''
    return sum(1 for i in iterable)

def _add_member(email, student_id, first_name, last_name, time_added, confirmation_token, confirmed):
    connection = sqlite3.connect(common.database_path)
    try:
        _check_database(connection)
        email_confirmation.prune_expired_members(connection)

        cursor = connection.cursor()
        # Check if this email address is already in database
        if iterlength(cursor.execute("SELECT * FROM members WHERE email= ? ", (email,) )) > 0:
            # Update member info
            cursor.execute("""UPDATE members
                              SET student_id = ?, first_name = ?, last_name = ?, time_added = ?, confirmation_token = ?, confirmed = ? 
                            WHERE email = ?""", (student_id, first_name, last_name, time_added, confirmation_token, confirmed, email))
        else:
            cursor.execute('''INSERT INTO members (email, student_id, first_name, last_name, time_added, confirmation_token, confirmed) 
                            VALUES (?, ?, ?, ?, ?, ?, ?)''', (email, student_id, first_name, last_name, time_added, confirmation_token, confirmed))
        connection.commit()
    except:
        connection.rollback()
        raise
    finally:
        connection.close()

def _remove_member(email):
    connection = sqlite3.connect(common.database_path)
    try:
        _check_database(connection)
        email_confirmation.prune_expired_members(connection)

        cursor = connection.cursor()
        cursor.execute("DELETE FROM members WHERE email= ?", (email, ))
        connection.commit()
    except:
        connection.rollback()
        raise
    finally:
        connection.close()



# https://docs.python.org/3/tutorial/datastructures.html#sets
# https://docs.python.org/3/library/stdtypes.html#set
required_params = {'email', 'student_id', 'first_name', 'last_name'}

def application(environ, start_response):
    method = environ['REQUEST_METHOD']
    if method != "POST":
        yield from common.error_page(environ, start_response, "Bad request", code="405 Method Not Allowed")
        return

    # Read POST data
    parameters = urllib.parse.parse_qs(environ['wsgi.input'].read().decode())

    # Check that all the required information is present
    if not required_params.issubset(parameters.keys()):
        message = "Bad request, missing parameters: " + ','.join(required_params - parameters.keys())
        yield from common.error_page(environ, start_response, message)
        return

    email = parameters['email'][0]
    student_id = parameters['student_id'][0]
    first_name = parameters['first_name'][0]
    last_name = parameters['last_name'][0]


    # Check that 900 number is valid
    if not re.fullmatch(r'900\d{6}', student_id):
        yield from common.error_page(environ, start_response, 'Invalid student_id')
        return

    # Check that email is valid
    # https://stackoverflow.com/a/14485817/8146866
    name, address = parseaddr(email)
    if address == '' or not address.endswith('@my.vcccd.edu'):
        yield from common.error_page(environ, start_response, 'Invalid email address')
        return


    time_added = time.time()

    # Confirmation code to be used in email confirmation link
    confirmation_token = str(time_added) + '_' + secrets.token_urlsafe(nbytes=32)

    # Now add the person to the members table
    _add_member(email, student_id, first_name, last_name, time_added, confirmation_token, False)

    start_response('200 OK', [('Content-Type', 'text/html')] )
    yield common.basic_template.substitute(title='Success', main='An email has been sent to ' + html.escape(email) + ' to confirm your membership').encode('utf-8')

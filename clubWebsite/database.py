"""
Existing database code, mix of functions from join.py and common.py

"""
import time
from string import Template
import os
import sqlite3

database_path = os.path.normpath('./data/members.sqlite')
confirmation_expire_time = 24*60*60     # 24 hours

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


def iterlength(iterable):
    ''' Return length of finite iterable '''
    return sum(1 for i in iterable)

def _add_member(email, student_id, first_name, last_name, time_added, confirmation_token, confirmed):
    connection = open_database()
    try:
        check_database(connection)
        prune_expired_members(connection)

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
    connection = open_database()
    try:
        check_database(connection)
        email_confirmation.prune_expired_members(connection)

        cursor = connection.cursor()
        cursor.execute("DELETE FROM members WHERE email= ?", (email, ))
        connection.commit()
    except:
        connection.rollback()
        raise
    finally:
        connection.close()

def prune_expired_members(connection):
    ''' Removes members from database who haven't confirmed their email within confirmation_expire_time '''
    expires_before = time.time() - confirmation_expire_time     # Anything before this time has expired

    cursor = connection.cursor()
    cursor.execute("""DELETE FROM members WHERE confirmed=0 AND time_added < ?""", (expires_before,))

def _confirm_member(token):
    ''' Returns string indicating whether confirmation was successful or not '''
    connection = open_database()
    try:
        check_database(connection)
        prune_expired_members(connection)
        cursor = connection.cursor()
        results = list( cursor.execute("""SELECT confirmed FROM members WHERE confirmation_token = ?""", (token,)) )
        if len(results) == 0:
            message = "Confirmation link expired, please try again."
        else:
            row = results[0]
            if row[0] == 1:
                message = "Your membership has already been confirmed."
            else:
                cursor.execute("""UPDATE members SET confirmed = 1 WHERE confirmation_token = ?""", (token,))
                message = "Your membership has been confirmed."

        connection.commit()
        return message
    except:
        connection.rollback()
        raise
    finally:
        connection.close()
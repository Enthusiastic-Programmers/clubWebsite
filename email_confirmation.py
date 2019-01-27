import sqlite3
import time
import urllib
import common

confirmation_expire_time = 24*60*60     # 24 hours

def prune_expired_members(connection):
    ''' Removes members from database who haven't confirmed their email within confirmation_expire_time '''
    expires_before = time.time() - confirmation_expire_time     # Anything before this time has expired

    cursor = connection.cursor()
    cursor.execute("""DELETE FROM members WHERE confirmed=0 AND time_added < ?""", (expires_before,))

def _confirm_member(token):
    ''' Returns string indicating whether confirmation was successful or not '''
    connection = sqlite3.connect(common.database_path)
    try:
        prune_expired_members(connection)
        cursor = connection.cursor()
        results = list( cursor.execute("""SELECT confirmed FROM members WHERE confirmation_code = ?""", (token,)) )
        if len(results) == 0:
            message = "Confirmation link expired, please try again."
        else:
            row = results[0]
            if row[0] == 1:
                message = "Your membership has already been confirmed."
            else:
                cursor.execute("""UPDATE members SET confirmed = 1 WHERE confirmation_code = ?""", (token,))
                message = "Your membership has been confirmed."

        connection.commit()
        return message
    except:
        connection.rollback()
        raise
    finally:
        connection.close()

def confirm(environ, start_response):
    parameters = urllib.parse.parse_qs(environ['QUERY_STRING'])
    if 'confirmation_token' not in parameters:
        yield from common.error_code(environ, start_response, 'Missing confirmation_token', code='400 Bad Request')
        return
    token = parameters['confirmation_token'][0]
    message = _confirm_member(token)
    start_response('200 OK', [('Content-Type', 'text/html')] )
    yield common.basic_template.substitute(title="Membership Confirmation", main=message).encode('utf-8')

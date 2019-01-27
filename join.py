import urllib
import re
from email.utils import parseaddr
import os
from string import Template
import html
import time

members_csv = os.path.normpath('./data/members.csv')
members_directory = os.path.dirname(members_csv)
# just completely remove commas, newlines, and quotes from field instead of dealing with stupid csv escaping
# we don't need those characters in data anyway
def sanitize_field(field):
    for character in ('"', ',', '\r', '\n'):
        field = field.replace(character, '')
    return field


def add_member(email, student_id, first_name, last_name): #, time_added, confirmation_code, confirmed):
    line_to_add = ','.join(sanitize_field(field) for field in (email, student_id, first_name, last_name))

    # check that directory with members.csv exists
    if not os.path.exists(members_directory):
        os.makedirs(members_directory)
    try:
        with open(members_csv, 'r', encoding='utf-8') as f:
            members = f.read()
    except FileNotFoundError:
        with open(members_csv, 'a+', encoding='utf-8') as f:
            f.write('email,student_id,first_name,last_name,time_added,confirmation_code,confirmed\n' + line_to_add + '\n')
    else:
        start_position = members.find('\n' + email)
        if start_position == -1:
            members += line_to_add + '\n'
        else:   # member already exists, update line
            end_position = members.find('\n', start_position+1)
            members = members[0:start_position+1] + line_to_add + members[end_position:]
        with open(members_csv, 'w', encoding='utf-8') as f:
            f.write(members)

with open('./template.html', 'r', encoding='utf-8') as f:
    basic_template = Template(f.read())
def error_page(environ, start_response, message, code='400 Bad Request'):
    start_response(code, [('Content-Type', 'text/html')])
    yield basic_template.substitute(title='Error', main='Error: ' + message).encode('utf-8')



# https://docs.python.org/3/tutorial/datastructures.html#sets
# https://docs.python.org/3/library/stdtypes.html#set
required_params = {'email', 'student_id', 'first_name', 'last_name'}

def application(environ, start_response):
    method = environ['REQUEST_METHOD']
    if method != "POST":
        yield from error_page(environ, start_response, "Bad request", code="405 Method Not Allowed")
        return

    # Read POST data
    parameters = urllib.parse.parse_qs(environ['wsgi.input'].read().decode())

    # Check that all the required information is present
    if not required_params.issubset(parameters.keys()):
        message = "Bad request, missing parameters: " + ','.join(required_params - parameters.keys())
        yield from error_page(environ, start_response, message)
        return

    email = parameters['email'][0]
    student_id = parameters['student_id'][0]
    first_name = parameters['first_name'][0]
    last_name = parameters['last_name'][0]


    # Check that 900 number is valid
    if not re.fullmatch(r'900\d{6}', student_id):
        yield from error_page(environ, start_response, 'Invalid student_id')
        return

    # Check that email is valid
    # https://stackoverflow.com/a/14485817/8146866
    name, address = parseaddr(email)
    if address == '' or not address.endswith('@my.vcccd.edu'):
        yield from error_page(environ, start_response, 'Invalid email address')
        return

    add_member(email, student_id, first_name, last_name)
    start_response('200 OK', [('Content-Type', 'text/html')] )
    yield basic_template.substitute(title='Success', main='An email has been sent to ' + html.escape(email) + ' to confirm your membership').encode('utf-8')

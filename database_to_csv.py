import sqlite3
import os

# just completely remove commas, newlines, and quotes from field instead of dealing with stupid csv escaping
# we don't need those characters in data anyway
def sanitize_field(field):
    for character in ('"', ',', '\r', '\n'):
        field = field.replace(character, '')
    return field


csv_path = os.path.normpath('./data/members.csv')
database_path = os.path.normpath('./data/members.sqlite')

connection = sqlite3.connect(database_path)
try:
    cursor = connection.cursor()
    rows = cursor.execute("SELECT * FROM members")

    members_csv = 'email,student_id,first_name,last_name,time_added,confirmation_token,confirmed\n'
    for row in rows:
        members_csv += ','.join(sanitize_field(str(field)) for field in row) + '\n'
finally:
    connection.close()

with open(csv_path, 'w', encoding='utf-8') as f:
    f.write(members_csv)

input('Success. Press enter to quit')

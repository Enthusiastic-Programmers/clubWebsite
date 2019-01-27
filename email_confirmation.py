import sqlite3
import time

confirmation_expire_time = 24*60*60     # 24 hours

def prune_expired_members(connection):
    expires_before = time.time() - confirmation_expire_time     # Anything before this time has expired

    cursor = connection.cursor()
    cursor.execute("""DELETE FROM members WHERE confirmed=0 AND time_added < ?""", (expires_before,))

import sqlite3
conn = sqlite3.connect('rex.db')
c = conn.cursor()
c.execute("CREATE TABLE messages (id text, user text, message text)")
conn.commit()
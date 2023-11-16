from flask import Blueprint, request,session
import json
import sqlite3
import logging
import mqttudp.engine as me

messages = Blueprint('messages', __name__)

@messages.route('/', methods=['POST'])
def message():
    print(request.form)
    data = request.form
    logging.info("relaying message: %s", data["message"])
    conn = sqlite3.connect('rex.db')
    c = conn.cursor()
    last_id = c.execute("SELECT * FROM messages WHERE user=? ORDER BY id DESC LIMIT 1", (session["name"],)).fetchone()
    if last_id is None or len(last_id) == 0:
        last_id =[ 0]
    c.execute("INSERT INTO messages VALUES (?,?,?)",(int(last_id[0])+1,session["name"],data["message"]))
    conn.commit()
    conn.close()
    me.send_publish("message", json.dumps({"id":int(last_id[0])+1,"name":session["name"],"message":data["message"]}).encode())
    return "OK"

def fns():
    def previous():
        conn = sqlite3.connect('rex.db')
        c = conn.cursor()
        c.execute("SELECT * FROM messages")
        l = c.fetchall()
        conn.close()
        return json.dumps(l)
    return dict(previous=previous)
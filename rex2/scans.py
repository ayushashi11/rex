import json
import logging
import colorama
import sqlite3
import time
from flask import session
from flask_sse import sse
from mqttudp import engine as me

colorama.init()
logging.basicConfig(level=logging.INFO , format=f'{colorama.Fore.LIGHTBLACK_EX}[{colorama.Fore.LIGHTBLUE_EX}%(name)s{colorama.Fore.LIGHTBLACK_EX}:{colorama.Fore.LIGHTYELLOW_EX}%(lineno)s{colorama.Fore.LIGHTBLACK_EX} {colorama.Fore.LIGHTBLACK_EX}- {colorama.Fore.LIGHTRED_EX}%(levelname)s{colorama.Fore.LIGHTBLACK_EX}] {colorama.Fore.LIGHTWHITE_EX}%(message)s {colorama.Fore.LIGHTBLACK_EX}at %(asctime)s{colorama.Fore.RESET}')

def a():
    me.send_ping()
    while True:
        me.send_publish("ping", session["name"].encode())
        time.sleep(0.5)


def recv(type:str,topic:str,message:str,something:int,ip:str):
    time.sleep(0.5)
    if topic=="ping":
        if message == session["name"]:
            return
        logging.info("Received ping: %s from %s", message, ip)
        sse.publish({"ip":ip,"name":message}, type='ping')
    if topic=="message":
        logging.info("Received message: %s from %s", message, ip)
        data = json.loads(message)
        logging.info("sql loaded")
        conn = sqlite3.connect('rex.db')
        c = conn.cursor()
        c.execute("SELECT * FROM messages WHERE id=? and user=?",(data["id"],data["name"]))
        if len(c.fetchall()) != 0:
            return
        c.execute("INSERT INTO messages VALUES (?,?,?)",(data["id"],data["name"],data["message"]))
        conn.commit()
        conn.close()
        sse.publish(data, type='message')

task = lambda: me.listen(recv)

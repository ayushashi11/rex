from flask import Flask
from .routes import mainbp, people, messages, fns
from flask_sse import sse
import sqlite3, logging
from flask_executor import Executor
app = Flask(__name__, template_folder="templates")
executor = Executor(app)
app.config["REDIS_URL"] = "redis://localhost:6379"
app.config["SECRET_KEY"] = "abcdefg"
app.register_blueprint(sse, url_prefix='/stream')
app.register_blueprint(mainbp)
app.register_blueprint(people, url_prefix='/people')
app.register_blueprint(messages, url_prefix='/message')
app.context_processor(fns)
conn = sqlite3.connect('rex.db')
def main():
    for route in app.url_map.iter_rules():
        logging.info(route)
    app.run()
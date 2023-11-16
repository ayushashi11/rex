from .people import people #type:ignore 
from .messages import messages, fns #type:ignore
from flask import Blueprint, render_template, session
from ..scans import task, a

mainbp = Blueprint('main', __name__)  
@mainbp.route('/')
def index():
    from .. import executor
    if len(executor.futures) == 0:
        session["name"] = "pbk"
        executor.submit(task)
        executor.submit(a)
    return render_template('index.html')
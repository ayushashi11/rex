from flask import Blueprint, request
from flask_sse import sse

people = Blueprint('people', __name__)

@people.route('/publish_internal', methods=['POST'])
def publish_internal():
    name = request.form.get("name")
    strength = request.form.get("strength")
    address = request.form.get("address")
    sse.publish({"name":name,"ip":address+"     "+strength}, type='ping')
    return "OK"

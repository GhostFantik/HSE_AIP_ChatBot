from flask import Flask, request
from BotLogic import message_handle
import db


app = Flask(__name__)
db.connect()


@app.route('/message', methods=['POST'])
def hello():
    user = request.form.get('user')
    source = request.form.get('source')
    message = request.form.get('message')
    return message_handle(user, source, message)


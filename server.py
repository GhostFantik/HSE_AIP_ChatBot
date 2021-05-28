from flask import Flask, request
from loguru import logger
from BotLogic import message_handle
import db


app = Flask(__name__)
db.connect()

logger.add('logs.txt')


@app.route('/message', methods=['POST'])
def hello():
    user = request.form.get('user')
    source = request.form.get('source')
    message = request.form.get('message')
    logger.info(f'New message from {source}-client {user} - {message}')
    return message_handle(user, source, message)


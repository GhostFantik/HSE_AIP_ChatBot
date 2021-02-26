# token 1536002137:AAEW6IhEfsvKx_F42KeFQt_tlkXWIVlYoVo

import os
import dotenv
import telebot
import requests
import json

dotenv.load_dotenv()

url = os.getenv('server_message_url')

bot = telebot.TeleBot("1536002137:AAEW6IhEfsvKx_F42KeFQt_tlkXWIVlYoVo")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    response = requests.post(url, data = {
        "user": message.chat.id,
        "source": "tg",
        "message": message.text,
    })
    bot.send_message(message.chat.id, response.text)
bot.polling()

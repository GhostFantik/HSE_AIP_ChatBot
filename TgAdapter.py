import os
import dotenv
import telebot
import requests

dotenv.load_dotenv()

url = os.getenv('server_message_url')

bot = telebot.TeleBot(os.getenv('tg_token'))


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    response = requests.post(url, data = {
        "user": message.chat.id,
        "source": "tg",
        "message": message.text,
    })
    bot.send_message(message.chat.id, response.text)
bot.polling()

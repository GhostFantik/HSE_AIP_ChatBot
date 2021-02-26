# token 1536002137:AAEW6IhEfsvKx_F42KeFQt_tlkXWIVlYoVo

import telebot
import requests
import json

bot = telebot.TeleBot("1536002137:AAEW6IhEfsvKx_F42KeFQt_tlkXWIVlYoVo")

@bot.message_handler(func=lambda message: True)
payload = {'mes': 'message', 'id': 'message.chat.id'}
r = requests.post(" ", data = payload, json = )
def echo_all(message):
    bot.send_message(message.chat.id, message.text)
bot.polling()

payload = {'mes': 'value1', 'key2': 'value2'}
r = requests.post("https://github.com/GhostFantik/HSE_AIP_ChatBot.git", data=payload)
print(r.text)
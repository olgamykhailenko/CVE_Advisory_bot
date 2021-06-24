#!/usr/bin/env python
# coding: utf-8
pip install pycvesearch && pip install pyTelegramBotAPI

import telebot
import json
from telebot import types
from pycvesearch import CVESearch

TOKEN = '1838881014:AAGp9qp9cs_HwKBCNELRtfwdX-JO0lWOSPA'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler()
def start(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, 'Hi, {0.first_name}! Please enter the vendor you are searching for!'.format(message.from_user))
    if message.chat.type == 'private':
        if message.text != '/start':
            vendor = message.text
            url = "https://nvd.nist.gov/vuln/search/results?form_type=Basic&results_type=overview&query?={vendor}&search_type=last3months".format(vendor=vendor)
            bot.send_message(message.chat.id, url)
    
bot.polling(none_stop=True)

import telebot
from telebot import types

TOKEN = '1891713169:AAE2kaM1l6evpd09rYxLoYlFCaz8ehuIhio'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton('PC')
    item2 = types.KeyboardButton('Laptop')
    item3 = types.KeyboardButton('Smartphone')
    item4 = types.KeyboardButton('Tablet')

    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id, 'Hi, {0.first_name}! Please select a device type'.format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text in ('PC', 'Laptop'):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Windows')
            item2 = types.KeyboardButton('Linux')
            item3 = types.KeyboardButton('MacOS')
            back = types.KeyboardButton('⬅️ Back')
            markup.add(item1, item2, item3, back)

            bot.send_message(message.chat.id, 'Please select OS', reply_markup=markup)

        elif message.text == 'Smartphone':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Android')
            item2 = types.KeyboardButton('iOS')
            back = types.KeyboardButton('⬅️ Back')
            markup.add(item1, item2, back)

            bot.send_message(message.chat.id, 'Please select OS', reply_markup=markup)

        elif message.text == '⬅️ Back':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('PC')
            item2 = types.KeyboardButton('Laptop')
            item3 = types.KeyboardButton('Smartphone')
            item4 = types.KeyboardButton('Tablet')

            markup.add(item1, item2, item3, item4)

            bot.send_message(message.chat.id, '⬅️ Back', reply_markup=markup)


bot.polling(none_stop=True)
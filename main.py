import telebot
import re
from telebot import types
from pycvesearch import CVESearch

TOKEN = '1891713169:AAE2kaM1l6evpd09rYxLoYlFCaz8ehuIhio'

bot = telebot.TeleBot(TOKEN)
cve = CVESearch("https://cve.circl.lu")
MESSAGE_STATE = 0 # Global message state handler, can be used to figure out where the user is in the bot workflow
STATE_CONSTS = {
    "start": 0,
    "waiting_cve_input": 1,
    "waiting" : 2
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton('PC')
    item2 = types.KeyboardButton('Laptop')
    item3 = types.KeyboardButton('Smartphone')
    item4 = types.KeyboardButton('Tablet')
    item5 = types.KeyboardButton('Search By CVE Number Directly')

    markup.add(item1, item2, item3, item4, item5)

    MESSAGE_STATE = STATE_CONSTS["start"]
    bot.send_message(message.chat.id, 'Hi, {0.first_name}! Please select a use case!'.format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    global MESSAGE_STATE
    print(MESSAGE_STATE)
    if message.chat.type == 'private':
        if MESSAGE_STATE == STATE_CONSTS["waiting_cve_input"]:
            print("got here!")
            print(message.text)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            message_text = ""
            if(len(re.findall(r"CVE-\d{4}-\d{4,7}", message.text)) < 1):
                print("got to invalid cve")
                print(len(re.findall("/CVE-\d{4}-\d{4,7}/ig", message.text)))
                message_text = "Error, your CVE Number is invalid!"
            else:
                vuln = cve.id(message.text)
                message_text += message.text
                message_text += "\nComplexity: " + vuln['access']['complexity']
                message_text += "\nAuthentication: " + vuln['access']['authentication']
                message_text += "\nAccess Vector: " + vuln['access']['vector']
                message_text += "\nDescription:" + vuln['summary']
                message_text += "\n\nYou can find more about this vulnerability on the following URL: https://nvd.nist.gov/vuln/detail/" + message.text
            MESSAGE_STATE = STATE_CONSTS["start"]
            bot.send_message(message.chat.id, message_text, reply_markup=markup)
        
        if MESSAGE_STATE == STATE_CONSTS["waiting"]:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            vendor = message.text
            url = "https://nvd.nist.gov/vuln/search/results?form_type=Basic&results_type=overview&query?={vendor}&search_type=last3months".format(vendor=vendor)
            bot.send_message(message.chat.id, url, reply_markup=markup)
            MESSAGE_STATE = STATE_CONSTS["start"]
                
            

        elif (message.text in ('Search By CVE Number Directly')) and MESSAGE_STATE == STATE_CONSTS["start"]:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            exampleRequestData = cve.id('CVE-2010-3333')
            message_text = "Please enter the CVE number directly. Use the format of CVE-<year>-<no>"
            bot.send_message(message.chat.id, message_text, reply_markup=markup)
            MESSAGE_STATE = STATE_CONSTS["waiting_cve_input"]

        elif (message.text in ('Search by Vendor Name')) and MESSAGE_STATE == STATE_CONSTS["start"]:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            message_text = "Please Enter the vendor, you are searching for!"
            bot.send_message(message.chat.id, message_text, reply_markup=markup)
            MESSAGE_STATE = STATE_CONSTS["waiting"]
            
        elif message.text in ('PC', 'Laptop'):
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

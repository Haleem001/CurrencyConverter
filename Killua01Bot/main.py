
from email import header
from urllib import request
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import os
import requests
import json
import time 
from datetime import datetime
import pytz 


PORT = int(os.environ.get('PORT', 5000))
TOKEN = ''
updater = Updater (token = TOKEN , use_context = True)
dispatcher = updater.dispatcher

def help(update, context):
    context.bot.send_message(
    chat_id = update.effective_chat.id, 
    text =  '/start - Start bot\n'+
        '/help - Show currency list\n'+
        '\n'+
        '/usd - Get current Dollar (USD) rate\n' +
        '/ngnusd - Naira (NGN) to Dollar (USD)\n' +
        '/usdngn - Dollar (USD) to Naira (NGN)\n' 
    )


def get_rate_new():
    global float_rate
    response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=USDTNGN')
    data = response.text
    parse_json = json.loads(data)
    rate = parse_json['price']
    float_rate = float(rate)
    tz_NG = pytz.timezone('Africa/Lagos')
    now = datetime.now(tz_NG)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    

    clean_rate =  '$1  is ₦{:.2f} as at {}.'.format(float_rate , dt_string)
    return clean_rate

def start(update, context):
    context.bot.send_message(
        chat_id = update.effective_chat.id, text="Hello, welcome to dollar to naira rates bot \n "
        'Use /help to show commands list'
        )

def get_usd(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_rate_new())

def ngnusd(update , context):
    real = update.message.text.replace('/ngnusd','')
    real = real.replace(',','.')

    real = float(real)
    convert = real/float_rate

    update.message.reply_text('₦{} is ${:.2f}' .format(real, convert))

def usdngn(update , context):
    real = update.message.text.replace('/usdngn','')
    real = real.replace(',','.')

    real = float(real)
    convert = real*float_rate

    update.message.reply_text('${} is ₦{:.2f}' .format(real , convert))





dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler("usd", get_usd)) 
dispatcher.add_handler(CommandHandler('ngnusd' , ngnusd))
dispatcher.add_handler(CommandHandler('usdngn', usdngn))

# updater.start_polling()
# updater.idle()


updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
updater.bot.setWebhook('https://arcane-scrubland-67404.herokuapp.com/' + TOKEN)

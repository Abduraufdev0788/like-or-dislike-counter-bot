from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext, MessageHandler, CommandHandler
import telegram
from pprint import pprint

from dotenv import load_dotenv
import os
import time
load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')


# bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN)

counter = {
    "mydata":0,
    "mydata2":0
}    

def start0(update, context):
    key1 = InlineKeyboardButton(text='👍', callback_data='mydata')

    key12 = InlineKeyboardButton(text='👎', callback_data='mydata2')
    reply_markup = InlineKeyboardMarkup([
        [key1, key12]
    ])

    update.message.reply_text('Hello', reply_markup=reply_markup)

def start1(update, context):
    key1 = InlineKeyboardButton(text=f'👍 {counter["mydata"]}', callback_data='mydata')

    key12 = InlineKeyboardButton(text=f'👎 {counter["mydata2"]}', callback_data='mydata2')
    reply_markup = InlineKeyboardMarkup([
        [key1, key12]
    ])

    update.message.reply_text('Hello', reply_markup=reply_markup)


def button_handler(update, context):
    query = update.callback_query
    query.answer()

    user_id = query.from_user.id
    new_vote = query.data

    old_vote = counter.get(user_id) 

    if old_vote == "mydata":
        counter["mydata"] -= 1

    elif old_vote == "mydata2":
        counter["mydata2"] -= 1


    if old_vote == new_vote:
        del counter[user_id]

    else:
        counter[user_id] = new_vote

        if new_vote == "mydata":
            counter["mydata"] += 1

        elif new_vote == "mydata2":
            counter["mydata2"] += 1


    query.edit_message_text(
        text="Hello",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    f'👍 {counter["mydata"]}',
                    callback_data="mydata"
                ),
                InlineKeyboardButton(
                    f'👎 {counter["mydata2"]}',
                    callback_data="mydata2"
                )
            ]
        ])
    )

def likewatch(update, context):
    if counter['mydata2'] == 0 and counter['mydata'] == 0:
        start0(update, context)

    else:
        start1(update, context)


    

    

dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", likewatch))
dispatcher.add_handler(CallbackQueryHandler(button_handler))


updater.start_polling()
updater.idle()

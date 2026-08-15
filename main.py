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
    "like" : 0,
    "dislike": 0
}

# Bir foydalanuvchi faqat bir marta ovoz berishi mumkin.
voted_users = set()
def start0(update, context):
    key1 = InlineKeyboardButton(text='👍', callback_data='mydata')

    key12 = InlineKeyboardButton(text='👎', callback_data='mydata2')
    reply_markup = InlineKeyboardMarkup([
        [key1, key12]
    ])

    update.message.reply_text('Hello', reply_markup=reply_markup)

def start1(update, context):
    key1 = InlineKeyboardButton(text=f'👍 {counter["like"]}', callback_data='mydata')

    key12 = InlineKeyboardButton(text=f'👎 {counter["dislike"]}', callback_data='mydata2')
    reply_markup = InlineKeyboardMarkup([
        [key1, key12]
    ])

    update.message.reply_text('Hello', reply_markup=reply_markup)


def button_handler(update, context):
    query = update.callback_query
    user_id = query.from_user.id

    if user_id in voted_users:
        query.answer("Siz allaqachon ovoz bergansiz.", show_alert=True)
        return

    voted_users.add(user_id)
    query.answer("Ovozingiz qabul qilindi.")

    if query.data == "mydata":
        counter["like"] += 1

    elif query.data == "mydata2":
        counter["dislike"] += 1

    query.edit_message_text(
        text="Hello",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    f'👍 {counter["like"]}',
                    callback_data="mydata"
                ),
                InlineKeyboardButton(
                    f'👎 {counter["dislike"]}',
                    callback_data="mydata2"
                )
            ]
        ])
    )

def likewatch(update, context):
    if counter['dislike'] == 0 and counter['like'] == 0:
        start0(update, context)

    else:
        start1(update, context)


    

    

dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", likewatch))
dispatcher.add_handler(CallbackQueryHandler(button_handler))


updater.start_polling()
updater.idle()

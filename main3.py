from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

updater = Updater(token=TOKEN)

counter = {
    "like": 0,
    "dislike": 0
}

voted_users = set()


def start(update, context):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                f"👍 {counter['like']}",
                callback_data="like"
            ),
            InlineKeyboardButton(
                f"👎 {counter['dislike']}",
                callback_data="dislike"
            )
        ]
    ])

    update.message.reply_text(
        "Ovoz bering:",
        reply_markup=keyboard
    )


def button_handler(update, context):
    query = update.callback_query
    user_id = query.from_user.id


    if user_id in voted_users:
        query.answer(
            "Siz allaqachon ovoz bergansiz. O'zgartira olmaysiz!",
            show_alert=True
        )
        return

    voted_users.add(user_id)

    if query.data == "like":
        counter["like"] += 1
        message = "Siz 👍 Like ovoz berdingiz!"

    elif query.data == "dislike":
        counter["dislike"] += 1
        message = "Siz 👎 Dislike ovoz berdingiz!"


    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                f"👍 {counter['like']}",
                callback_data="like"
            ),
            InlineKeyboardButton(
                f"👎 {counter['dislike']}",
                callback_data="dislike"
            )
        ]
    ])

    query.answer(message)

    query.edit_message_text(
        text="Ovoz berish yakunlandi",
             
        reply_markup=keyboard
    )


dispatcher = updater.dispatcher

dispatcher.add_handler(
    CommandHandler("start", start)
)

dispatcher.add_handler(
    CallbackQueryHandler(button_handler)
)

updater.start_polling()
updater.idle()
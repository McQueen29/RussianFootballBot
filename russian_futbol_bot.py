from flask import Flask, render_template
import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
reply_keyboard = [['/news', '/statistic'],
                  ['/developers', '/info'],
                  ['/social_media']]

TOKEN = '5193054775:AAHmmNiMl5903TX_C8Wk9Xp6fJ2REQVvdyE'

app = Flask(__name__)

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def start(update, context):
    update.message.reply_text(
        "Привет! От меня ты можешь узнать много о нашем футболе. С чего хочешь начать?",
        reply_markup=markup
    )


def close_keyboard(update, context):
    update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def news(update, context):
    keyboard = [
        [
            InlineKeyboardButton('Матч Премьер', callback_data='Матч Премьер'),
            InlineKeyboardButton("tg2", callback_data='2'),
        ],
        [InlineKeyboardButton("tg 3", callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        'Итак тут ты можешь узнать последние новости о нашем футболе. Выбери Телеграм канал, '
        'а я 10 последних новостей)', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query

    query.answer()

    query.edit_message_text(text=f"выбранный канал: {query.data} \n"
                                 f"пререйдите по ссылке: http://127.0.0.1:5000/")

    @app.route('/')
    def news():
        if query.data == 'Матч Премьер':
            url = 'matchpremier'
            return render_template('news.html', title=f'Новости: {query.data}', url=url)

    app.run()


def developers(update, context):
    update.message.reply_text("will be soon")


def statistic(update, context):
    update.message.reply_text(
        "will be soon")


def social_media(update, context):
    update.message.reply_text(
        "will be soon")


def info(update, context):
    update.message.reply_text(
        "will be soon")


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text & ~Filters.command, start)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("news", news))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("developers", developers))
    dp.add_handler(CommandHandler("statistic", statistic))
    dp.add_handler(CommandHandler("social_media", social_media))
    dp.add_handler(CommandHandler("close", close_keyboard))
    dp.add_handler(text_handler)
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

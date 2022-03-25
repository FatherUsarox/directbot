from socket import timeout
import time
import logging
import pyshorteners
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
)




# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
INPU = range(4)


def start(update, context):

    update.message.reply_text(
        text="Hola, bienvenido. ¿Qué deseas hacer?",
        reply_markup = InlineKeyboardMarkup([
            
            [InlineKeyboardButton(text="Acortar enlace /url:", callback_data="url")],
            [InlineKeyboardButton(text="Google", url="https://www.google.com/")]
        ])
    )
    

def url_command_handler(update, context):
    update.message.reply_text("Envía un enlace para acortarlo:\n")
    return INPU

def url_callback_handler (update, context):

    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text = "Envía un enlace para acortarlo:\n"
    )
    return INPU

def input_url(update,context):
    #bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
    url = update.message.text #here because we want to retrieve the text from the original message and send the same thing back
    chat = update.message.chat
    
    # acortar url

    short = ''

    s = pyshorteners.Shortener()

    short = s.chilpit.short('url')
    #s.chilpit.expand('http://chilp.it/TEST')

    chat.send_action(
        action = ChatAction.TYPING,
        timeout=None
    )

    chat.send_message(
        text = short
    
    )

    return ConversationHandler.END

def main() -> None:

    updater = Updater("5202799890:AAESmZj4AR7SsTo6UlJUQYnR5Mbnq-bBWEM")
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start",start))

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('url', url_command_handler),
            CallbackQueryHandler(pattern="url", callback=url_callback_handler)
        ],
        states={
            INPU: [MessageHandler(Filters.text & ~Filters.command, input_url)],
        },
        fallbacks=[],
    )

    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()


    updater.idle()
if __name__ == '__main__':
    main()
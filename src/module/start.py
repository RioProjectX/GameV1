import logging, datetime

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackQueryHandler, Filters

from ..helper.constant import Constant

logging.basicConfig(
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", level = logging.INFO
)
logger = logging.getLogger(__name__)

def init(dispatcher):
    dispatcher.add_handler( CommandHandler("start", start, filters = Filters.chat_type.private) )
    dispatcher.add_handler( CallbackQueryHandler(home, pattern = "^home$") )

def start(update, context):
    msg = update.effective_message
    keyboard = [
        [
            InlineKeyboardButton( text = "Petunjuk", callback_data = "help" ),
            InlineKeyboardButton( text = "Tentangku", callback_data = "about" )
        ],[
            InlineKeyboardButton( text = "Channel", url = "t.me/tokai" )
        ]
    ]
    
    context.user_data["time"] = datetime.datetime.now()
    msg.reply_text(
        Constant.START,
        allow_sending_without_reply = True,
        reply_markup = InlineKeyboardMarkup(keyboard)
    )

def home(update, context):
    callback = update.callback_query
    keyboard = [
        [
            InlineKeyboardButton( text = "Petunjuk", callback_data = "help" ),
            InlineKeyboardButton( text = "Tentangku", callback_data = "about" )
        ],[
            InlineKeyboardButton( text = "Channel", url = "t.me/tokai" )
        ]
    ]
    
    context.user_data["time"] = datetime.datetime.now()
    callback.edit_message_text(
        Constant.START,
        parse_mode = "HTML",
        reply_markup = InlineKeyboardMarkup(keyboard)
    )
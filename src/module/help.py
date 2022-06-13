import logging, datetime

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, Filters

from ..helper.constant import Constant

logging.basicConfig(
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", level = logging.INFO
)
logger = logging.getLogger(__name__)

def init(dispatcher):
    dispatcher.add_handler( CallbackQueryHandler(about, pattern = "^help$") )

def about(update, context):
    callback = update.callback_query
    keyboard = [
        [
            InlineKeyboardButton( text = "Menu", callback_data = "home" ),
            InlineKeyboardButton( text = "Tentangku", callback_data = "about" )
        ]
    ]
    
    context.user_data["time"] = datetime.datetime.now()
    callback.edit_message_text(
        Constant.HELP,
        parse_mode = "HTML",
        reply_markup = InlineKeyboardMarkup(keyboard)
    )
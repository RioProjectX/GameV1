import logging, datetime

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, Filters

from ..helper.constant import Constant

logging.basicConfig(
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", level = logging.INFO
)
logger = logging.getLogger(__name__)

def init(dispatcher):
    dispatcher.add_handler( CallbackQueryHandler(about, pattern = "^about$") )

def about(update, context):
    callback = update.callback_query
    keyboard = [
            [
                InlineKeyboardButton( text = "Petunjuk", callback_data = "help" ),
                InlineKeyboardButton( text = "Menu", callback_data = "home" )
            ]
    ]

    context.user_data["time"] = datetime.datetime.now()
    callback.edit_message_text(
            Constant.ABOUT,
            parse_mode = "HTML",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(keyboard)
    )

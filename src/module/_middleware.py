import logging, datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import TypeHandler, DispatcherHandlerStop

from ..helper.limiter import limiter
from ..helper.constant import Constant

logging.basicConfig(
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", level = logging.INFO
)
logger = logging.getLogger(__name__)

def init(dispatcher):
    dispatcher.add_handler(TypeHandler(Update, middleware), group = -1)

def middleware(update, context):
    msg = update.effective_message
    if not msg:
        return

    if msg.chat.type == "private":
        is_flooding = limiter.is_limited(context, "private")
        if is_flooding:
            if update.callback_query:
                update.callback_query.answer("Tunggu... jangan melakukan spam!!")

            raise DispatcherHandlerStop

        if update.callback_query:
            update.callback_query.answer("")

    else:
        is_flooding = limiter.is_limited(context, "group")
        if is_flooding:
            raise DispatcherHandlerStop

        is_admin = limiter.is_admin(context, msg.chat.id)
        if not is_admin:
            msg.reply_text(Constant.NOT_ADMIN_ALERT, parse_mode = "HTML")
            context.chat_data["time"] = datetime.datetime.now()

            raise DispatcherHandlerStop

        if msg.chat.type == "group":
            msg.reply_text(
                    Constant.GROUP_ALERT,
                    parse_mode = "HTML",
                    reply_markup = InlineKeyboardMarkup(
                        [[ InlineKeyboardButton(text = "Tutorial", url = "t.me/tokai") ]]
                    )
            )

            context.chat_data["time"] = datetime.datetime.now()
            raise DispatcherHandlerStop

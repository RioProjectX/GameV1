import logging, datetime

from telegram.ext import CommandHandler, Filters
from ..helper.game import game

logging.basicConfig(
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", level = logging.INFO
)
logger = logging.getLogger(__name__)

def init(dispatcher):
    dispatcher.add_handler( CommandHandler("play", play, filters = Filters.chat_type.supergroup) )

def play(update, context):
    msg = update.effective_message
    chat_data = context.chat_data

    if "cache_game" in chat_data:
        try:
            message_id = chat_data["cache_game"]["quest_id"]
            context.bot.delete_message(msg.chat.id, message_id)
        except Exception as _:
            pass
    
    quest = game.get_quest(context)
    photo = context.bot.send_photo(msg.chat.id, quest["soal"])
    
    chat_data["time"] = datetime.datetime.now()
    chat_data["cache_game"] = {
        "answer": quest["jawaban"].lower(),
        "quest_id": photo.message_id
    }

import logging, datetime, random

from telegram.ext import MessageHandler, Filters
from ..helper.game import game
from ..helper.database import database

logging.basicConfig(
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", level = logging.INFO
)
logger = logging.getLogger(__name__)

def init(dispatcher):
    my_filter = ( Filters.reply & Filters.text & Filters.chat_type.supergroup )
    dispatcher.add_handler(
        MessageHandler(filters = my_filter, callback = track_answer)
    )

def track_answer(update, context):
    msg = update.effective_message
    reply = msg.reply_to_message
    
    chat_data = context.chat_data
    if (
        "cache_game" not in chat_data or
        reply.message_id != chat_data["cache_game"]["quest_id"]
    ):
        return
    
    text = "<b><i>Salah</i></b> ❌" + "\n"
    text += f"<b>{ msg.text }</b> <i>bukanlah jawaban yang benar, cobalah kembali!!</i>"
    
    if msg.text.lower() == chat_data["cache_game"]["answer"]:
        context.bot.delete_message(msg.chat.id, reply.message_id)
        del chat_data["cache_game"]
        
        score = random.randint(5, 50)
        is_exists = database.get_score(msg.from_user.id)
        old_score = is_exists if is_exists else 0
        updated_score = old_score + score
        
        if not is_exists:
            database.add_user(( msg.from_user.id, msg.from_user.first_name, updated_score ))
        else:
            database.update_score(( updated_score, msg.from_user.id ))
        
        text = "<b><i>Benar</i></b> 🎉" + "\n"
        text += f"<i>Jawaban kamu benar!! kamu mendapat</i> <b>{ score }</b> <i>skor dan "
        text += f"total skor kamu menjadi</i> <b>{ updated_score }</b>"
    
    chat_data["time"] = datetime.datetime.now()
    msg.reply_text(text, parse_mode = "HTML")



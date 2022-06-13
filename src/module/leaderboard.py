import logging, datetime, html

from telegram.ext import CommandHandler, Filters
from ..helper.database import database

logging.basicConfig(
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", level = logging.INFO
)
logger = logging.getLogger(__name__)

def init(dispatcher):
    dispatcher.add_handler( CommandHandler("top", leaderboard, filters = Filters.chat_type.supergroup) )

def leaderboard(update, context):
    msg = update.effective_message

    all_data = database.get_leaderboard()
    if not all_data:
        return msg.reply_text(
                "<b>Leaderboard</b> <i>masih dalam keadaan kosong!!</i>",
                parse_mode = "HTML"
        )

    text = "🔸 <b><i>TOP 10 PEMAIN BULAN INI</i></b> 🔸" + "\n\n"
    medals = ["🥇", "🥈", "🥉"]

    for index, data in enumerate(all_data, start = 1):
        user_id = data["id"]
        user_name = html.escape(data["name"])
        score = data["score"]
        mention = f"<a href=\"tg://user?id={ user_id }\">{ user_name }</a>"

        medal = ""
        if ( (index - 1) <= 2 ):
            medal = medals[index - 1]

        text += f"<b>{ index }. <i>{ mention }</i></b> { medal }" + "\n"
        text += f"<b>└</b> <code>{ score } pts</code> <b>-</b> <code>{ user_id }</code>" + "\n"

    context.chat_data["time"] = datetime.datetime.now()
    msg.reply_text(text, parse_mode = "HTML")

import logging, os

from importlib import import_module
from telegram.ext import Updater, CallbackContext

from src.helper.game import game

logging.basicConfig(
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", level = logging.INFO
)
logger = logging.getLogger(__name__)

def load_handlers(dispatcher):
    base_path = os.path.join(os.path.dirname(__file__), "src/module")
    files = os.listdir(base_path)
    index = 0

    for file_name in files:
        if file_name != "__pycache__":
            index += 1
            print(f"{ index }.", file_name, "berhasil diimport")

            handler_module, _ = os.path.splitext(file_name)
            module = import_module(f".{handler_module}", "src.module")

            module.init(dispatcher)

def main():
    updater = Updater("PUT-YOUR-BOT-TOKEN-HERE", use_context = True)
    dispatcher = updater.dispatcher

    load_handlers(dispatcher)

    context = CallbackContext(dispatcher)
    game.get_quest(context)

    updater.start_polling(drop_pending_updates = True)
    updater.idle()
if __name__ == "__main__":
    main()

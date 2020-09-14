from telegram.ext import Updater

from . import handlers


class Bot:
    def __init__(self, token: str):
        self.updater = Updater(token=token, use_context=True)
        dp = self.updater.dispatcher

        # https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/nestedconversationbot.py

        dp.add_error_handler(handlers.error)

    def run(self):
        self.updater.start_polling()

    def forever_run(self):
        self.run()
        self.updater.idle()

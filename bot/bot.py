import traceback
from telegram.ext import Updater, MessageHandler, Filters

from bot.user import User


class Bot:
    def __init__(self, token, dispatcher):
        self.updater = Updater(token=token)
        self.dispatcher = dispatcher

        handler = MessageHandler(Filters.text | Filters.command, self.__onMessage)
        self.updater.dispatcher.add_handler(handler)

    def start(self):
        self.updater.start_polling()

    def __onMessage(self, bot, update):
        try:
            user = User.fromMessage(update.message)
            responses = self.dispatcher.process(user, update.message.text)
            for response in responses:
                bot.send_message(
                    chat_id=response.chatId,
                    parse_mode=response.parseMode,
                    text=response.msg)
        except Exception as e:
            print(e)
            traceback.print_exc()

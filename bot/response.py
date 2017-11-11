from telegram import ParseMode


class Response:
    MARKDOWN = ParseMode.MARKDOWN

    def __init__(self, chatId, msg, parseMode=None):
        self.chatId = chatId
        self.msg = msg
        self.parseMode = parseMode

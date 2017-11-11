from tinydb import where

from bot.command.command import Command
from bot.response import Response


class StartCommand(Command):
    def __init__(self, db):
        Command.__init__(self, 'start', [])
        self.db = db

    def process(self, user, args):
        existed = self.db.users.contains(where('userId') == user.userId)
        if existed:
            return [Response(user.chatId, 'You are already Secret Santa!')]

        self.db.users.insert(user.toDatabase())
        return [Response(user.chatId, 'Now you are Secret Santa!')]

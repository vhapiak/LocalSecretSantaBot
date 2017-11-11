from tinydb import where

from bot.command.command import Command
from bot.response import Response


class JoinCommand(Command):
    def __init__(self, db):
        Command.__init__(self, 'join', ['group_name'])
        self.db = db

    def process(self, user, args):
        assert len(args) == 1

        name = args[0]
        group = self.db.groups.get(where('name') == name)
        if group is None:
            return [Response(user.chatId, 'Group not found!')]

        if group['launched']:
            return [Response(user.chatId, 'Group already launched!')]

        if user.userId in group['users']:
            return [Response(user.chatId, 'You are already in this group!')]

        group['users'].append(user.userId)
        self.db.groups.update(group)
        return [Response(user.chatId, 'You are joined to group!')]

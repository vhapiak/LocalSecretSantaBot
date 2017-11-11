from tinydb import where

from bot.command.command import Command
from bot.response import Response


class CreateCommand(Command):
    def __init__(self, db, joinCommand):
        Command.__init__(self, 'create', ['group_name'])
        self.db = db
        self.joinCommand = joinCommand;

    def process(self, user, args):
        assert len(args) == 1

        name = args[0]
        if len(name) < 3:
            return [Response(user.chatId, 'Group name must has at least 3 letters!')]

        groups_number = self.db.groups.count(where('ownerId') == user.userId)
        if groups_number >= 10:
            return [Response(user.chatId, 'You cannot create more than 10 groups!')]

        existed = self.db.groups.contains(where('name') == name)
        if existed:
            return [Response(user.chatId, 'Group with such name already exists!')]

        self.db.groups.insert({
            'name': name,
            'ownerId': user.userId,
            'launched': False,
            'users': []
        })
        return [Response(user.chatId, 'Group created!')] + self.joinCommand.process(user, args)

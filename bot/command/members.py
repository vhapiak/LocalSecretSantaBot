from tinydb import where

from bot.command.command import Command
from bot.response import Response
from bot.user import User


class MembersCommand(Command):
    def __init__(self, db):
        Command.__init__(self, 'members', ['group_name'])
        self.db = db

    def process(self, user, args):
        assert len(args) == 1

        name = args[0]
        group = self.db.groups.get(where('name') == name)
        if group is None:
            return [Response(user.chatId, 'Group not found!')]

        if user.userId not in group['users']:
            return [Response(user.chatId, 'You are not member of this group!')]

        users = self.db.users.search(where('userId').test(lambda x: x in group['users']))
        mentions = map(User.makeMention, map(User.fromDatabase, users))

        return [Response(user.chatId, 'Group members:\n\n' + '\n'.join(mentions), Response.MARKDOWN)]

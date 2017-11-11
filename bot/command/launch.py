import random
from tinydb import where

from bot.command.command import Command
from bot.response import Response
from bot.user import User


class LaunchCommand(Command):
    def __init__(self, db):
        Command.__init__(self, 'launch', ['group_name'])
        self.db = db

    def process(self, user, args):
        assert len(args) == 1

        name = args[0]
        group = self.db.groups.get(where('name') == name)
        if group is None:
            return [Response(user.chatId, 'Group not found!')]

        if group['ownerId'] != user.userId:
            return [Response(user.chatId, 'You are not owner of the group!')]

        if group['launched']:
            return [Response(user.chatId, 'Group already launched!')]

        if len(group['users']) < 2:
            return [Response(user.chatId, 'Group must contains at least 2 members')]

        dbUsers = self.db.users.search(where('userId').test(lambda x: x in group['users']))
        users = list(map(User.fromDatabase, dbUsers))

        appointments = _makeAppointments(users)
        responses = map(lambda appointment: _makeResponse(name, appointment), appointments)

        group['launched'] = True
        self.db.groups.update(group)

        return responses


class _Appointment:
    def __init__(self, santa, target):
        self.santa = santa
        self.target = target


def _makeAppointments(users):
    random.shuffle(users)
    appointments = list()
    for index, current in enumerate(users):
        targetIndex = (index + 1) % len(users)
        appointments.append(_Appointment(current, users[targetIndex]))
    return appointments


def _makeResponse(name, appointment):
    return Response(
        appointment.santa.chatId,
        'Your target in group "' + name + '" is ' + User.makeMention(appointment.target),
        Response.MARKDOWN)
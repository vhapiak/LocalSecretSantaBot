from bot.response import Response


class Dispatcher:
    def __init__(self):
        self.commands = {}

    def registerCommand(self, command):
        self.commands[command.name] = command

    def process(self, user, message):
        if message.startswith('/'):
            return self.__processCommand(user, message)
        else:
            return [Response(user.chatId, 'I\'m waiting for a command')]

    def __processCommand(self, user, message):
        parts = message.split()
        commandName = parts[0][1:]
        args = parts[1:]

        if commandName in self.commands:
            command = self.commands[commandName]
            if len(args) == len(command.args):
                return command.process(user, args)
            else:
                return [Response(user.chatId, 'Usage: ' + command.getUsage())]
        else:
            return [Response(user.chatId, 'Command not found')]
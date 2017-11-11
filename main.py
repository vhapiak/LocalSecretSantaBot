#!/usr/bin/python

import sys

from bot.database import Database
from bot.bot import Bot
from bot.dispatcher import Dispatcher

from bot.command.start import StartCommand
from bot.command.create import CreateCommand
from bot.command.join import JoinCommand
from bot.command.members import MembersCommand
from bot.command.launch import LaunchCommand

if len(sys.argv) != 3:
    print("Usage: main.py db.json token")
    sys.exit(1)

dbPath = sys.argv[1]
botToken = sys.argv[2]

database = Database(dbPath)

joinCommand = JoinCommand(database)

dispatcher = Dispatcher()
dispatcher.registerCommand(StartCommand(database))
dispatcher.registerCommand(joinCommand)
dispatcher.registerCommand(CreateCommand(database, joinCommand))
dispatcher.registerCommand(MembersCommand(database))
dispatcher.registerCommand(LaunchCommand(database))

bot = Bot(botToken, dispatcher)
bot.start()

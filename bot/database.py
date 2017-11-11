import tinydb


class Database:
    def __init__(self, path):
        connection = tinydb.TinyDB(path)
        self.users = connection.table('users')
        self.groups = connection.table('groups')

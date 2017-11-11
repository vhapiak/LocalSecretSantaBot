

class User:
    @staticmethod
    def fromMessage(msg):
        return User(
            msg.from_user.id,
            msg.chat.id,
            msg.from_user.first_name,
            msg.from_user.last_name)

    @staticmethod
    def fromDatabase(record):
        return User(
            record['userId'],
            record['chatId'],
            record['firstName'],
            record['lastName'])

    @staticmethod
    def makeMention(user):
        firstName = user.firstName
        lastName = user.lastName
        fullName = '[' + firstName + ' ' + lastName + ']'
        mention = '(tg://user?id=' + str(user.userId) + ')'
        return fullName + mention

    def __init__(self, userId, chatId, firstName, lastName):
        self.userId = userId
        self.chatId = chatId
        self.firstName = str(firstName) if firstName is not None else ''
        self.lastName = str(lastName) if lastName is not None else ''

    def toDatabase(self):
        return {
            'userId': self.userId,
            'chatId': self.chatId,
            'firstName': self.firstName,
            'lastName': self.lastName
        }
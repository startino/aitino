class ChatBotException(Exception):
    pass


class WrongCreds(ChatBotException):
    pass


class HookException(ChatBotException):
    pass


class APIException(ChatBotException):
    pass


class BotNotRunning(ChatBotException):
    pass

from Bot.BotApi import Vk
from Bot.Config import Config
from Bot.Forwarded import ForwardedMessages


class NewMessage:
    def __init__(self, obj):
        self.vk = Vk()
        from_id = obj.message['peer_id']
        if from_id <= 2000000001:
            User(obj)
        elif from_id == Config.CONSOLE:
            Console(obj)
        else:
            Conference(obj)


class User:
    def __init__(self, obj):
        print(ForwardedMessages(obj).find_quote())


class Console:
    def __init__(self, obj):
        pass


class Conference:
    def __init__(self, obj):
        pass
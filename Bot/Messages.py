from os import remove

from BotApi import Vk
from Config import Config
from MessagesQuotes import MessagesQuotes, single_quote
from QuotesGen import SingleQuote


class NewMessage:
    def __init__(self, obj):
        from_id = obj.message['peer_id']
        if from_id < 2000000000:
            User(obj)
        elif from_id == Config.CONSOLE:
            Console(obj)
        else:
            Conference(obj)


def by_forwarded_message(obj):
    VK = Vk()
    peer = obj.message['peer_id']
    msg = obj.message['text'].lower()
    quote = MessagesQuotes(obj).find_quote()
    if quote:
        reg = False
        if 'регистр' in msg or 'reg' in msg or 'рег' in msg:
            reg = True

        if single_quote(quote):
            if quote[0] > 0:
                quoted = SingleQuote(quote, reg).assembly()
                if quoted:
                    q = VK.UploadAttachmentPhoto(quoted)
                    VK.MessageSend(peer, 'Мемчик...\nСамые смешные мемы кидайте в предложку группы!', attachment=q)
                    VK.MessageSend(Config.CONSOLE, f'От: @id{obj.message["from_id"]}', attachment=q)
                    remove(quoted)
                else:
                    VK.MessageSend(peer, 'При создании цитаты произошла ошибка!\nВозможно, цитата имела слишком много строк и символов!\nКраткость - сестра таланта!')
            else:
                VK.MessageSend(peer, 'Невозможно сгенерировать цитату паблика...')
        else:
            VK.MessageSend(peer, 'Пока что не научлся генерировать диалоги...\nНо когда-нибудь все будет!')
    else:
        VK.MessageSend(peer, 'Не получилось сгенерировать цитату!\nВозможно, пересланные сообщения не содержат текста, либо произошла внутренняя ошибка')


class User:
    def __init__(self, obj):
        if obj.message.fwd_messages:
            by_forwarded_message(obj)


class Console:
    def __init__(self):
        pass


class Conference:
    def __init__(self, obj):
        if obj.message.fwd_messages:
            by_forwarded_message(obj)
        elif 'reply_message' in obj.message.keys():
            VK = Vk()
            reply = obj.message['reply_message']
            peer = obj.message['peer_id']
            msg = obj.message['text'].lower()
            reg = False
            if 'регистр' in msg or 'reg' in msg or 'рег' in msg:
                reg = True

            quote = [reply['from_id'], reply['text']]
            if quote[0] > 0:
                quoted = SingleQuote(quote, reg).assembly()
                if quoted:
                    q = VK.UploadAttachmentPhoto(quoted)
                    VK.MessageSend(peer, 'Мемчик...\nСамые смешные мемы кидайте в предложку группы!', attachment=q)
                    VK.MessageSend(Config.CONSOLE, f'От: @id{obj.message["from_id"]}', attachment=q)
                    remove(quoted)
                else:
                    VK.MessageSend(peer,
                                   'При создании цитаты произошла ошибка!\nВозможно, цитата имела слишком много строк и символов!\nКраткость - сестра таланта!')
            else:
                VK.MessageSend(peer, 'Невозможно сгенерировать цитату паблика...')
from time import sleep

import requests
from vk_api.bot_longpoll import VkBotEventType

from BotApi import Vk
from Messages import NewMessage

VK = Vk()


def MainBot():
    print('LongPooling started!')
    while True:
        try:
            for event in VK.LongPool.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    try:
                        NewMessage(event)
                    except Exception as e:
                        print(e)
                        VK.ConsoleMessage(f'Ошибка: {e} caused by {event.obj.message}')
        except requests.exceptions.ReadTimeout:
            VK.ConsoleMessage('LongPool перезапущен!')


if __name__ == '__main__':
    MainBot()


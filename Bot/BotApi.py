import vk_api.vk_api
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.utils import get_random_id

from Config import Config


class Vk:
    def __init__(self):
        self.VkSession = vk_api.VkApi(token=Config.TOKEN)
        self.VkApi = self.VkSession.get_api()
        self.LongPool = VkBotLongPoll(self.VkSession, group_id=Config.GROUP_ID)

    def MessageSend(self, send_id, message=None, attachment=None, keyboard=None):
        self.VkApi.messages.send(peer_id=send_id,
                                 message=message,
                                 random_id=get_random_id(),
                                 attachment=attachment,
                                 keyboard=keyboard)

    def CheckOnline(self, user_id):
        info = self.VkApi.users.get(user_ids=user_id, fields=['online'])
        return info

    def ConsoleMessage(self, message):
        self.MessageSend(Config.CONSOLE, message)

    def UploadAttachmentPhoto(self, photo):
        upload = VkUpload(self.VkSession)
        response = upload.photo_messages(photo)[0]
        return f'photo{response["owner_id"]}_{response["id"]}_{response["access_key"]}'

    def UserNameGet(self, user_id):
        info = self.VkApi.users.get(user_ids=user_id)[0]
        return info['first_name'], info['last_name']

    def UserPhotoGet(self, user_id):
        info = self.VkApi.users.get(user_ids=user_id, fields=['photo_max_orig'])[0]
        if 'photo_max_orig' in info.keys():
            return info['photo_max_orig']
        return 'https://vk.com/images/camera_400.png?ava=1'

    def SetActivity(self, peer_id):
        self.VkApi.messages.setActivity(type='typing',
                                        peer_id=peer_id,
                                        group_id=Config.GROUP_ID)

    def ManyMessagesSend(self, user_ids, message=None, attachment=None, keyboard=None):
        if len(user_ids) > 100:
            for i in range(len(user_ids) // 100 + 1):
                self.VkApi.messages.send(user_ids=user_ids[i * 100: 100 * (i + 1)],
                                         message=message,
                                         random_id=get_random_id(),
                                         attachment=attachment,
                                         keyboard=keyboard)
        else:
            self.VkApi.messages.send(user_ids=user_ids,
                                     message=message,
                                     random_id=get_random_id(),
                                     attachment=attachment,
                                     keyboard=keyboard)

from vk_api import VkUpload, vk_api
from vk_api.utils import get_random_id

TOKEN = 'f8f998d833e721e098709fafbfff96c42dc1021f183eb8a961730d6120a6f9a7373bef4ec318b4f5482f8'
GROUP_ID = '172694092'
CONSOLE = 2000000001

api = vk_api.VkApi(token=TOKEN)


def get_user_photo(uid):
    info = api.get_api().users.get(user_ids=uid, fields=['photo_max_orig'])[0]
    if 'photo_max_orig' in info.keys():
        return info['photo_max_orig']
    return 'https://vk.com/images/camera_400.png?ava=1'


def get_user_name(uid):
    info = api.get_api().users.get(user_ids=uid)[0]
    return info['first_name'], info['last_name']


def send_message(send_id, message=None, attachment=None, keyboard=None):
    api.get_api().messages.send(peer_id=send_id,
                                message=message,
                                random_id=get_random_id(),
                                attachment=attachment,
                                keyboard=keyboard)


def upload_message_photo(photo):
    upload = VkUpload(api)
    response = upload.photo_messages(photo)[0]
    return f'photo{response["owner_id"]}_{response["id"]}_{response["access_key"]}'

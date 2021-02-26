from vk_api import VkApi
from vk_api.longpoll import  VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import os
import dotenv
import requests

dotenv.load_dotenv()

vk_session = VkApi(token=os.getenv('vk_token'))
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


def start_longpoll():
    print('Start VkAdapter...')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user:
            user = event.user_id
            message = event.message
            source = 'vk'
            response = requests.post(url=os.getenv('server_message_url'), data={
                'user': user,
                'source': source,
                'message': message,
            })
            send_message(user, response.text)


def send_message(user_id, message):
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=get_random_id()
    )


if __name__ == '__main__':
    start_longpoll()

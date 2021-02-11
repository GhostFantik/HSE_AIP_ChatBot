from vk_api import VkApi
from vk_api.longpoll import  VkLongPoll, VkEventType
from vk_api.utils import get_random_id


vk_session = VkApi(token='82f73784e78cc8b4b4be15dbcdd94fe096a0adf0cd48de804fc28ced6fa2bfbe279b9e9a215f19ad675a1')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


def start_longpoll(handler):
    print('Start VkAdapter...')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user:
            handler(event.message + ' Курсач')


def send_message(user_id, message):
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=get_random_id()
    )


#
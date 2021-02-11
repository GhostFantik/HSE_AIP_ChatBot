from vk_api import VkApi
from vk_api.longpoll import  VkLongPoll, VkEventType
from vk_api.utils import get_random_id


vk_session = VkApi(token='8039baae4648d1345d8419312db53bc9954b0a39822f3fb79926583a0b08b8a0d05b9bdc768ff0155127f')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


def start_longpoll(handler):
    print('Start TestAdapter...')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user:
            handler(event.message + ' SarDelivery')


def send_message(user_id, message):
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=get_random_id()
    )
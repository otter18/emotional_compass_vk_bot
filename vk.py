# -*- coding: utf-8 -*-
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from chat_vk import Chat
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api import VkUpload
from pd import *
import os

# Chat object for each unique user
users = {}


def main():
    if os.environ.get('RELOAD_IMG'):
        # img dowloading
        print('-' * 30, 'downloading imgs', '-' * 30)
        get_imgs()
    # auth
    # vk_session = vk_api.VkApi(token=open('config/token.txt', 'r').read())
    vk_session = vk_api.VkApi(token=os.environ.get('VK_TOKEN', open('config/token.txt', 'r').read()))
    server = VkBotLongPoll(vk_session, 183487105)

    vk = vk_session.get_api()
    upload = VkUpload(vk_session)

    print('-' * 30, 'bot started', '-' * 30)
    
    # main loop
    for event in server.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            id = event.object.from_id
            msg = event.obj.text
            if id in users.keys():
                txt, bnt, url = users[id].answer(msg, id)
            else:
                users[id] = Chat()
                txt, bnt, url = users[id].answer(msg, id)
            # keyboard
            keyboard = VkKeyboard(one_time=True)

            if bnt:
                for row in bnt[:-1]:
                    for button in row:
                        keyboard.add_button(button['txt'], color=button['color'])  # NEGATIVE VkKeyboardColor.DEFAULT
                    keyboard.add_line()

                for button in bnt[-1]:
                    keyboard.add_button(button['txt'], color=button['color'])
            if url:
                try:
                    photo = upload.photo_messages(photos='img/%s.jpg' % url)[0]
                except:
                    try:
                        photo = upload.photo_messages(photos='img/%s.png' % url)[0]
                    except:
                        photo = upload.photo_messages(photos='img/error.jpg')[0]
            vk.messages.send(
                random_id=get_random_id(),
                user_id=id,
                keyboard=keyboard.get_keyboard() if bnt else keyboard.get_empty_keyboard(),
                attachment='photo{}_{}'.format(photo['owner_id'], photo['id']) if url else None,
                message=txt
            )

            print('Username:', get_user_name_from_vk_id(id))
            print('User msg:', msg)
            print('Bot msg:', txt, url)
            print('-' * 30)


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from chat_vk import Chat
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api import VkUpload
from pd import *

# Chat object for each unique user
users = {}


def main():
    # img dowloading
    get_imgs()
    # auth
    vk_session = vk_api.VkApi(token=open('config/token.txt', 'r').read())
    server = VkBotLongPoll(vk_session, 183487105)

    vk = vk_session.get_api()
    upload = VkUpload(vk_session)


    print('\033[01m', 'bot started...', '\033[0m')
    print('-' * 30)
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
                        keyboard.add_button(button['txt'], color=button['color']) #NEGATIVE VkKeyboardColor.DEFAULT
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
                attachment= 'photo{}_{}'.format(photo['owner_id'], photo['id']) if url else None,
                message=txt
            )

            print('\033[01m', 'Username:', '\033[0m', get_user_name_from_vk_id(id))
            print('\033[01m', 'User msg:','\033[0m', msg)
            print('\033[01m', 'Bot msg:', '\033[0m', txt, url)
            print('-' * 30)


if __name__ == '__main__':
    main()

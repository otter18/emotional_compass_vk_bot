# -*- coding: utf-8 -*-
import vk_api
from chat_vk import Chat
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api import VkUpload
from pd import *
import os
from flask import Flask, request
import json

# Chat object for each unique user
users = {}
server = Flask(__name__)
vk_session = vk_api.VkApi(token=os.environ['VK_TOKEN'])
vk = vk_session.get_api()
upload = VkUpload(vk_session)

# img dowloading
print('-' * 30, 'downloading imgs', '-' * 30)
get_imgs()
print('-' * 30, 'bot started', '-' * 30)


def main(data):
    id = data['object']['from_id']
    msg = data['object']['text']

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
                keyboard.add_button(button['txt'], color=button['color'])
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


@server.route('/vk-bot', methods=['POST'])
def getMessage():
    data = json.loads(request.stream.read().decode("utf-8"))
    if data['secret'] == os.environ.get('secret'):
        if data['type'] == 'confirmation':
            return os.environ.get('confirmation_token'), 200
        if data['type'] == 'message_new':
            main(data)
            return "ok", 200
    return "!", 403


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

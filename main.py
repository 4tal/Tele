from pyrogram import api, Client
from pyrogram.api import functions

import time

with Client(
    "TestApp",
    api_id=4324323,
    api_hash="sadasdadsaasdfafasddfas"
) as app:

    #user_name_to_search = app.get_users(['Dove420'])[0].username
    user_name_to_search = app.get_users([613073508])[0].username
    chat_id = None

    for dialog in app.iter_dialogs(0, 100):
        if dialog.chat.username == user_name_to_search:
            chat_id = dialog.chat.id
            break

    relevant_chat = app.get_chat(chat_id)
    chat_name = None
    time_offset = int(time.time())

    while True:
        time.sleep(2)
        messages_history = app.get_history(chat_id).messages

        for message in messages_history:
            if message.text != None and time_offset < message.date:
                validation_array = message.text.split()
                if "OpenGroup" in message.text and "OpenGroup" == validation_array[0] and len(validation_array) == 2:
                    chat_name = validation_array[1]
                    message_id = message.message_id
                    break

                print("Not a valid call")
                time_offset = int(time.time())  # Alternative date offset.

        if chat_name is not None:
            time_offset = int(time.time())
            print(chat_name)
            print(time_offset)

            channel_obj = (app.send(
                functions.channels.CreateChannel(chat_name, 'Description', True, True)).chats[0]
            )

            chat_name = None
            invite_link = app.send(api.functions.channels.ExportInvite(api.types.InputChannel(channel_obj.id, channel_obj.access_hash))).link
            app.send_message(chat_id, invite_link, reply_to_message_id=message_id)
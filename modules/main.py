import asyncio
import time
import sys
import hashlib
import uuid

sys.path.append("./../")    #allows python interpreter to find modules

from nio import (AsyncClient, AsyncClientConfig, RoomMessageText,
    InviteEvent, RoomMessageImage, RoomMessageMedia)
from models.database import create_tables
from services.database_service import (check_if_room_is_existing,
    check_if_student_is_existing, create_new_room, create_new_student,
    create_new_message, get_number_of_links_to_be_shown, get_salt_value,
    add_salt_value, check_if_room_is_existing, get_all_modules_original,
    get_room_ids)
from nlp import language_processing
from response_management import generate_response
from message_evaluation import evaluate_message
from organisational_document import add_organisation_document
from config import Config

#from aiofiles import *

#set filepath of config file
config_filepath = "config.yaml"
config = Config(config_filepath)

#AsyncClient configuration options
client_config = AsyncClientConfig(
    max_limit_exceeded=0,
    max_timeouts=0,
    store_sync_tokens=True,
    encryption_enabled=True,
)

#initialize matrix client
client = AsyncClient(
    config.homeserver_url,
    config.user_id,
    config=client_config,
)

async def main():
    #client login
    await client.login(password=config.user_password)
    print("after login")

    #add event callbacks
    client.add_event_callback(message_cb, RoomMessageText)
    client.add_event_callback(auto_join_room_cb, InviteEvent)

    #sync encryption keys with the server, for encrypted rooms
    if client.should_upload_keys:
        await client.keys_upload()

    await client.sync_forever(timeout=30000, full_state=True)

    #close client connection on disconnect
    await client.close()

async def sendMessage(room_id, response):

    await client.room_send(
        room_id=room_id,
        message_type="m.room.message",
        content={
            "msgtype": "m.text",
            "body": str(response)
        }
    )

async def message_cb(room, event):

    room_id = str(room.room_id)
    room_display_name = room.display_name
    student_name = room.user_name(event.sender)

    #ignore own messages
    if event.sender == client.user:
        return

    else:

        #hasing of the user name with salt
        salt_value = get_salt_value()
        salt_value = salt_value[0]
        salt_value = salt_value.encode('utf-8')
        student_name = student_name.encode('utf-8')
        hashed_user_name = hashlib.sha512(student_name + salt_value).hexdigest()
        student_name = hashed_user_name

        message_body = event.body

        event_timestamp = event.server_timestamp #tiestamp in ms (unix time)
        current_timestamp = int(round(time.time() * 1000))
        timestamp_difference = current_timestamp - event_timestamp

        #print("timestamp difference: " + str(timestamp_difference))
        #ignore old events
        if timestamp_difference > 10000:
            print("old")
        else:
            print("NEW MESSAGE")
            if check_if_student_is_existing(student_name) == False:
                create_new_student(student_name, "operating systems (os)")   #default: show 2 links

            if check_if_room_is_existing(room_id) == False:
                create_new_room(room_id, room_display_name, student_name)

            #process message
            processed_message = language_processing(message_body)
            evaluation = evaluate_message(student_name, processed_message)
            response = generate_response(student_name, evaluation, message_body)

            if response != "":
                #send response
                await sendMessage(room_id, response)

#auto join rooms
async def auto_join_room_cb(room, event):

    room_id = room.room_id

    room_ids = get_room_ids()
    all_room_ids = []
    for i in range(0, len(room_ids)):
        all_room_ids.append(room_ids[i][0])

    #check if room was already joined
    if room_id in all_room_ids:
        return

    await client.join(room_id)
    salt_value = get_salt_value()
    if salt_value == None:
        salt_value = uuid.uuid4().hex
        add_salt_value(salt_value)

        all_modules = get_all_modules_original()
        string_with_modules = ""
        for i in range(0, len(all_modules)):
            current = all_modules[i][0]
            if current != "General":
                if string_with_modules == "":
                    string_with_modules = string_with_modules + current
                else:
                    string_with_modules = string_with_modules + ", " + current

        standard_first_message = "Hi, I'm your chatbot helping you with whatever you need! I've information about the following modules: " + string_with_modules + "\nCall 'help' to see all my options."
        #await sendMessage(room_id, standard_first_message)

        #file_stat = await aiofiles.stat("topics.png")
        #async with aiofiles.open("topics.png", "r+b") as f:
        #    resp, maybe_keys = await client.upload(
        #        f,
        #        content_type="image/png",
        #        filename="topics.png",
        #        filesize=file_stat.st_size()
        #    )
        print("AUTO JOIN")
        await client.room_send(
            room_id=room_id,
            message_type="m.room.message",
            content = {
                "msgtype": "m.file",
                "url": "https://uni-muenster.sciebo.de/s/MnwAt06uUNUBijh",
                "body": standard_first_message
            }
        )

asyncio.get_event_loop().run_until_complete(main())

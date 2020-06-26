import asyncio
import time
from nio import AsyncClient
from nio import Api
#from nio import register

import sys

#sys.path.append("/home/jonathan/Studium/Semester6/Bachelorarbeit/Chatbot/chatbot/")
sys.path.append("./../")    #allows python interpreter to find modules


from nio import (SyncResponse, RoomMessageText, FullyReadEvent,
    ToDeviceMessage, RoomMessagesResponse, RoomRedactResponse, InviteEvent)

from models.database import create_tables
from services.database_service import check_if_room_is_existing, check_if_student_is_existing, create_new_room, create_new_student, create_new_message, get_number_of_links_to_be_shown
from services.database_service import get_salt_value, add_salt_value, check_if_room_is_existing
from nlp import language_processing
from response_management import generate_response
from message_evaluation import evaluate_message
from index_evaluation import add_data_basis
from organisational_document import add_organisation_document

#for hashing
import hashlib, uuid

lastResponse = ""   #global variables
lastSender = ""

joined_room = ""

client = AsyncClient("https://matrix.org", "@neo-wwu:matrix.org")


async def sendMessage(room_id, response):

    await client.room_send(
        room_id=room_id,
        message_type="m.room.message",
        content={
            "msgtype": "m.text",
            "body": str(response)
        }
    )

    global lastResponse
    global lastSender
    lastResponse = response
    lastSender = "neo-wwu"
    salt_value = get_salt_value()[0]
    salt_value = salt_value.encode('utf-8')
    lastSender = lastSender.encode('utf-8')
    lastSender = hashlib.sha512(lastSender + salt_value).hexdigest()

async def message_cb(room, event):
    room_id = str(room.room_id)
    room_display_name = room.display_name
    student_name = room.user_name(event.sender)

    if student_name != "neo-wwu":

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
        if timestamp_difference > 10000: #10s difference = new message
            print("old")
        else:
            print("NEW MESSAGE")
            if check_if_student_is_existing(student_name) == False:
                create_new_student(student_name, "operating systems (os)")   #default: show 2 links

            if check_if_room_is_existing(room_id) == False:
                create_new_room(room_id, room_display_name, student_name)

            global lastSender
            global lastResponse

            if str(lastSender) != str(student_name) or str(lastResponse) != str(message_body):

                processed_message = language_processing(message_body)
                evaluation = evaluate_message(student_name, processed_message)
                response = generate_response(student_name, evaluation, message_body)

                if response != "":
                    await sendMessage(room_id, response)

#auto join rooms
async def auto_join_room_cb(room, event):
    room_id = room.room_id
    await client.join(room_id)
    salt_value = get_salt_value()
    if salt_value == None:
        salt_value = uuid.uuid4().hex
        add_salt_value(salt_value)
    global joined_room
    if joined_room != str(room_id):
        standard_first_message = "Hi, I'm your chatbot helping you with whatever you need! Call 'help' to see all my options."
        await sendMessage(room_id, standard_first_message)
        joined_room = room_id

async def main():
    #create_tables()
    #add_data_basis()
    #add_organisation_document()
    await client.login("johaiva123thaype")
    print("after login")

    client.add_event_callback(message_cb, RoomMessageText)
    client.add_event_callback(auto_join_room_cb, InviteEvent)

    await client.sync_forever(timeout=30000) #always sync with server


asyncio.get_event_loop().run_until_complete(main())

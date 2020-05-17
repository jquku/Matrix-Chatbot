import asyncio
import time
from nio import AsyncClient
from nio import Api
#from nio import Api
#from nio import register

import sys

#sys.path.append("/home/jonathan/Studium/Semester6/Bachelorarbeit/Chatbot/chatbot/")
sys.path.append("./../")    #allows python interpreter to find modules


from nio import (SyncResponse, RoomMessageText, FullyReadEvent,
    ToDeviceMessage, RoomMessagesResponse, RoomRedactResponse)

from models.database import create_tables
from services.database_service import check_if_room_is_existing, check_if_student_is_existing, create_new_room, create_new_student, create_new_message, get_number_of_links_to_be_shown
from nlp import language_processing
from response_generation import generate_response
from message_evaluation import evaluate_message
from index_evaluation import add_data_basis

lastResponse = ""   #global variables
lastSender = ""

client = AsyncClient("https://matrix.org", "@riot_chatbot:matrix.org")


async def sendMessage(room_id, response, student_name):
    print("RESPONSE: " + str(response))


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
    lastSender = "riot_chatbot"

async def message_cb(room, event):
    room_id = str(room.room_id)
    room_display_name = room.display_name
    student_name = room.user_name(event.sender)
    message_body = event.body

    event_timestamp = event.server_timestamp #tiestamp in ms (unix time)
    current_timestamp = int(round(time.time() * 1000))
    timestamp_difference = current_timestamp - event_timestamp

    #print("timestamp difference: " + str(timestamp_difference))
    if timestamp_difference > 20000: #5s difference = new message
        print("old")
    else:
        print("NEW MESSAGE")

        if check_if_room_is_existing(room_id) == False:
            create_new_room(room_id, room_display_name, student_name)

        if check_if_student_is_existing(student_name) == False:
            create_new_student(student_name, "OS", 2)   #default: show 2 links

        global lastSender
        global lastResponse

        if str(lastSender) != str(student_name) or str(lastResponse) != str(message_body):

            processed_message = language_processing(message_body)
            evaluation = evaluate_message(student_name, processed_message)
            response = generate_response(student_name, evaluation, message_body)

            if response != "":
                await sendMessage(room_id, response, student_name)

async def main():
    create_tables()
    await client.login("chatbot123")
    print("after login")

    client.add_event_callback(message_cb, RoomMessageText)
    await client.sync_forever(timeout=30000) #always sync with server

asyncio.get_event_loop().run_until_complete(main())

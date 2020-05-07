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
from nlp import strategy
from data_basis import add_data_basis
#from register_user import register_new_user

lastResponse = ""   #global variables
lastSender = ""

#client = AsyncClient("http://localhost:8008", "@chatbot:quade.org")
#client = AsyncClient("https://matrix.org", "@jquku:matrix.org")
client = AsyncClient("https://matrix.org", "@riot_chatbot:matrix.org")


async def sendMessage(room_id, response, student_name):
    print("RESPONSE: " + str(response))

    #response_string = ""    #response comes as a list, build a string
    #for i in range(0, len(response)):
    #    response_string = response_string + response[i] + " "

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

    #print("lastSender after sending: " + str(lastSender))
    #print("lastResponse after sending: " + str(lastResponse))

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
        #print("room id: " + str(room_id))
        #print(
        #    "Message received for room {} | {}: {}".format(
        #        room.display_name, room.user_name(event.sender), event.body
        #    )    + str("room timestamp: " + str(event.server_timestamp)) + " type: " + str(type(event))
        #)
        #print("                     ")
        #new message
        if check_if_room_is_existing(room_id) == False:
            create_new_room(room_id, room_display_name, student_name)
            #print("New room added")
        if check_if_student_is_existing(student_name) == False:
            create_new_student(student_name, "OS", "default")
            #print("New student added")
        #print("new message added")
        global lastSender
        global lastResponse
        #print("LAST SENDER: " + str(lastSender))
        #print("CURRENT SENDER: " + str(student_name))
        #print("LAST RESPONSE: " + str(lastResponse))
        #print("CURRENT RESPONSE: " + str(message_body))
        #print("lastSender before sending: " + str(lastSender) + " CURRENT: " + str(student_name))
        #print("lastResponse before sending: " + str(lastResponse) + " CURRENT: " + str(message_body))
        if str(lastSender) != str(student_name) or str(lastResponse) != str(message_body):
            #if lastSender != student_name:
                #print("Sender ungleich")
            #if lastResponse != message_body:
                #print("Response ungleich")
            response = strategy(message_body, student_name)
            #print("RESPONSE " + str(len(response[2])) + " TYPE: " + str(type(response[2])))
            create_new_message(student_name, message_body, response[0], response[1], response[2])
            if len(response[2]) > 0:
                await sendMessage(room_id, response[2], student_name)

        #await client.close()
        #sys.exit(0)

async def main():
    create_tables()
    #add_data_basis()
    #print('\n'.join(sys.path))
    #await client.register("chatbot:matrix.org", "test123", "")
    await client.login("chatbot123")
    #await client.login("chatbot")
    print("after login")
    #await register_new_user()
    #user = "chatbot:matrix.org"
    #password = "chatbot123454321"
    #device_name = ""
    #device_id = ""
    #nio = Api()
    #await Api.register(user, password, device_name, device_id)
    #await self.regiter(user, password, device_name, device_id)

    #client.register(user, password)
    #await Api.register(user, password, device_name)

    #strategy("Hello guys,    this is a testmessage about virtual clock memory. We also have ---...,,,:::::89")
    #await client.sync(timeout=5000)
    client.add_event_callback(message_cb, RoomMessageText)
    await client.sync_forever(timeout=30000) #always sync with server

asyncio.get_event_loop().run_until_complete(main())

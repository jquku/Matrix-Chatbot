import sys

sys.path.append("./../")

from services.database_service import get_number_of_links_to_be_shown, set_number_of_links_to_be_shown, get_concerning_links, get_next_links
from services.database_service import create_new_message

def generate_response(user, message, original_message):

    lowercase_only = message[0]
    standardized_message = message[1]
    help = message[2]
    number_of_links = message[3]
    show_more = message[4]
    show_all = message[5]
    greetings = message[6]
    goodbyes = message[7]
    links = message[8]

    response = ""
    number_of_links_found = len(links)

    #step 1: check if help called
    if help == True:
        response = "Use 'links = X' to return X links by default. \n" + "Use 'show more' to display more links fitting the query. \n" + "Use 'show all' to display all links fitting the query."
        #create_new_message params = user, original message; information_extracted, all_links, response
        create_new_message(user, original_message, lowercase_only, "", response)
        return response

    #step 2: check if number of links called
    if number_of_links == True:
        #new number of links already set in message_evaluation module
        response = ""
        create_new_message(user, original_message, lowercase_only, "", response)
        return response

    #step 3: add greeting if necessary
    if greetings == True:
        response = "Hi! "

    #step 4: check if show more or show all is called
    if show_more == True:
        links_last_message_more = get_next_links(user)
        #print("SHOW MORE TYPE: " + str(type(links_last_message_more)))
        response = response + links_last_message_more

    if show_all == True:
        links_last_message_all = get_concerning_links(user)
        #TUPLE
        #print("SHOW ALL TYPE: " + str(type(links_last_message_all)))
        response = response + links_last_message_all[0]

    #step 5: add links if necessary
    if number_of_links_found > 0:
        how_many_links_to_show = get_number_of_links_to_be_shown(user)
        #print("how many links to show: " + how_many_links_to_show)
        how_many_links_to_show = int(how_many_links_to_show)
        response = response + "I've found " + str(number_of_links_found) + " results. "
        for i in range(0, number_of_links_found):
            if i < how_many_links_to_show:
                response = response + links[i] +  "\n" +  "\n"
            else:
                break
    #print("CURRENT RESPONSE: " + str(response))
    #step 6: add goodbye if necessary
    if goodbyes == True:
        response = response + "Bye!"

    #step 7: check if default answer is necessary
    if response == "":
        default_answer = "I'm a chatbot serving as your digital learning assistant. Tell me which topic you want to know more about."
        response = default_answer
    #print("LINKS TYPE: " + str(type(links)))

    all_links_db = list_to_string(links)
    if all_links_db == "":
        if show_more == True:
            all_links_db = get_concerning_links(user)  #wrong
        if show_all == True:
            all_links_db = links_last_message_all[0]
    create_new_message(user, original_message, lowercase_only, all_links_db, response)
    return response

def list_to_string(links):
    final = ""
    for i in range(0, len(links)):
        final = final + links[i] +  "\n" +  "\n"
    return final

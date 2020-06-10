import sys

sys.path.append("./../")

from services.database_service import get_number_of_links_to_be_shown, set_number_of_links_to_be_shown, get_concerning_links, get_next_links, get_stats, increment_links_counter_for_helpful, get_links_counter_for_helpful, update_modul_satisfaction, get_last_module_of_user
from services.database_service import create_new_message, update_last_module_of_user, get_module_name, get_last_message, get_organisation_text
from services.database_service import get_stats_preferred, get_student_language

def generate_response(user, message, original_message):

    lowercase_only = message[0]
    standardized_message = message[1]
    help = message[2]
    number_of_links = message[3]
    show_more = message[4]
    show_all = message[5]
    greetings = message[6]
    goodbyes = message[7]
    stats_called = message[8]
    message_contains_yes_or_no = message[9]
    changed_number_of_stats = message[10]
    change_language = message[11]
    links_from_multiple_modules = message[12]
    links = message[13]

    response = ""
    number_of_links_found = len(links)
    language_of_user = get_student_language(user)[0]

    #step 1: check if help called
    if help == True:
        if language_of_user == "english":
            response = "Use 'links = X' to return X links by default. \n" + "Use 'show more' to display more links fitting the query. \n" + "Use 'show all' to display all links fitting the query. \n" + "Use 'stats' and add your module to receive the statistics. \n" + "Use 'stats = X' to return X stats by default. \n" + "Use 'language = english/german' to change my bot language."
        else:
            response = "Schreibe 'links = X' um standardmäßig X links zurückzugeben. \n" + "Mit 'zeig mehr' bekommst du mehr Links angezeigt. \n" + "Mit 'zeig alles' werden alle passenden Links zurückgegeben. \n" + "Tippe 'stats' und füge deinen Modulnamen hinzu, um die Statistiken abzurufen. \n" + "Mit 'stats = X' werden dir X Statistiken angezeigt.. \n" + "Mit 'language = englisch/deutsch' kannst du die Bot Sprache abändern."
        #create_new_message params = user, original message; information_extracted, all_links, response
        create_new_message(user, original_message, lowercase_only, "", response)
        return response

    #step 2: check if number of links called, if number of stats changed or user language changed
    if number_of_links == True or changed_number_of_stats == True or change_language == True:
        #new number of links already set in message_evaluation module
        if language_of_user == "english":
            response = "I saved the changes."
        else:
            response = "Ich habe die Änderungen abgespeichert."
        create_new_message(user, original_message, lowercase_only, "", response)
        return response

    #step 3: add greeting if necessary
    if greetings == True:
        response = "Hi! "

    #step 4: return statistics if called
    if stats_called != False:
        output_stats = get_stats(stats_called)  #returns sorted list of topics + questions
        if language_of_user == "english":
            response = response + "Here are the most requested topics. \n \n"
        else:
            response = response + "Hier sind die am häufigsten angefragten Themen. \n \n"
        number_of_stats_to_return = get_stats_preferred(user)[0]
        if number_of_stats_to_return > len(output_stats):
            number_of_stats_to_return = len(output_stats)
        for j in range(0, number_of_stats_to_return):
            if language_of_user == "english":
                response = response + str(output_stats[j][0]) + " was requested " + str(output_stats[j][1]) + " times. \n"
            else:
                response = response + str(output_stats[j][0]) + " wurde " + str(output_stats[j][1]) + "-mal angefragt. \n"
        #print("STATS STATS STATS: " + str(output_stats) + str(output_stats[0][0]) + str(type(output_stats)) + str(len(output_stats[0])))
        create_new_message(user, original_message, lowercase_only, "", response)
        return response

    #step 5: check if show more or show all is called
    if show_more == True:
        links_last_message_more = get_next_links(user)
        response = response + links_last_message_more

    if show_all == True:
        links_last_message_all = get_concerning_links(user)
        #TUPLE
        response = response + links_last_message_all[0]

    #step 6: add links if necessary
    if number_of_links_found > 0:

        if links_from_multiple_modules != False:
            if language_of_user == "english":
                response = response + "I've found fitting results from the following modules: \n" + links_from_multiple_modules + "Which module are you interested in?"
            else:
                response = response + "Ich habe zu den folgenden Modulen passende Resultate erhalten: \n" + links_from_multiple_modules + "Welches Modul interessiert dich??"
            all_links_db = list_to_string(links)
            create_new_message(user, original_message, lowercase_only, all_links_db, response)
            return response

        how_many_links_to_show = get_number_of_links_to_be_shown(user)
        increment_links_counter_for_helpful(user)
        #print("how many links to show: " + how_many_links_to_show)
        how_many_links_to_show = int(how_many_links_to_show)
        if language_of_user == "english":
            response = response + "I've found " + str(number_of_links_found) + " results. "
        else:
            response = response + "Ich habe " + str(number_of_links_found) + " Resultate gefunden. "
        #print("RESPONSE: " + str(response))
        for i in range(0, number_of_links_found):
            if i == 0:
                #print("LINKS[i]: " + str(links[i]))
                #get module name of best fitting link
                module = get_module_name(links[i])[0]
                #print("MODULE NAME: " + str(module))
                update_last_module_of_user(user, module)
            if i < how_many_links_to_show:
                response = response + links[i] +  "\n" +  "\n"
            else:
                break
        #step 7: add "is my answer helpful" after every 5th link interaction
        counter = get_links_counter_for_helpful(user)
        #print("COUNTER TYPE: " + str(type(counter)) + str(counter[0]))
        if counter[0] % 5 == 0:    #every 5th link interaction added by "is my answer helpful"
            if language_of_user == "english":
                response = response + "Is my answer helpful?"
            else:
                response = response + "War meine Antwort hilfreich?"

    #step 8: check if student answered with yes or no if answer was helpful
    else:
        if message_contains_yes_or_no != False:
            counter = get_links_counter_for_helpful(user)
            if counter[0] % 5 == 0:
                last_message = get_last_message(user)[0]
                print("LAST MESSAGE: " + str(last_message))
                helpful_string_english = "Is my answer helpful?"
                helpful_string_german = "War meine Antwort hilfreich?"
                if helpful_string_english in last_message or helpful_string_german in last_message:
                    if language_of_user == "english":
                        response = response + "Thanks for your feedback!"
                    else:
                        response = response + "Danke für dein Feedback!"
                    last_module = get_last_module_of_user(user)[0]
                    #print("LAST MODULE: " + str(last_module))
                    #print("SATISFACTION COUNTER: " + str(message_contains_yes_or_no))
                    update_modul_satisfaction(last_module, message_contains_yes_or_no)
                    create_new_message(user, original_message, lowercase_only, "", response)
                    return response


    #step 9: check if user wants to access the document with organisation infos
    if message_contains_yes_or_no == 1:
        last_message = get_last_message(user)[0]
        if language_of_user == "english":
            organisation_string = "Do you want to access the organisation infos?"
        else:
            organisation_string = "Willst du die organisatorischen Infos abrufen?"
        if organisation_string in last_message:
            last_module = get_last_module_of_user(user)[0]
            organisation_text = get_organisation_text(last_module)
            if organisation_text != None:
                organisation_text = organisation_text[0]
                response = response + organisation_text.rstrip()

    #step 10: add goodbye if necessary
    if goodbyes == True:
        response = response + "Bye!"

    #step 11: check if default answer is necessary
    if response == "":
        #print("MESSAGE CONTAINS CONTAINS: " + str(message_contains_yes_or_no))
        if message_contains_yes_or_no != False:
            return response
        #    helpful_string_english = "Is my answer helpful?"
        #    helpful_string_german = "War meine Antwort hilfreich?"
        #    if helpful_string_english in last_message or helpful_string_german in last_message:
        #        return response
        if language_of_user == "english":
            default_answer = "I'm a chatbot serving as your digital learning assistant. Tell me which topic you want to know more about. Do you want to access the organisation infos?"
        else:
            default_answer = "Ich bin ein Chatbot, dein digitaler Lernassistent. Über welches Vorlesungsthema willst du Bescheid wissen? Willst du die organisatorischen Infos abrufen?"
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

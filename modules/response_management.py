import sys
import random

sys.path.append("./../")

from services.database_service import (get_number_of_links_to_be_shown, set_number_of_links_to_be_shown,
    get_concerning_links, get_next_links, get_stats, increment_links_counter_for_helpful,
    get_links_counter_for_helpful, update_modul_satisfaction, get_last_module_of_user,
    create_new_message, update_last_module_of_user, get_domain_name, get_last_message, get_organisation_text,
    get_stats_preferred, get_user_language)

def generate_response(user, message, original_message):

    lowercase_only = message[0]
    standardized_message = message[1]
    help = message[2]
    number_of_links = message[3]
    show_more = message[4]
    show_all = message[5]
    stats_called = message[6]
    message_contains_yes_or_no = message[7]
    message_contains_thank_you = message[8]
    changed_number_of_stats = message[9]
    change_language = message[10]
    links_from_multiple_modules = message[11]
    links = message[12]
    small_talk = message[13]
    organisational = message[14]

    response = ""
    number_of_links_found = len(links)
    language_of_user = get_user_language(user)[0]

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

    #step 3: small talk
    if len(small_talk) > 0:
        response = response + small_talk[0] + " "

    if len(organisational) > 0:
        response = response + organisational[0] + "\n"

    #step 4: add you're welcome if user thanked chatbot
    if message_contains_thank_you == True:
        if language_of_user == "english":
            response = response + "You're welcome. "
        else:
            response = response + "Bitte. "

    #step 5: return statistics if called
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
        create_new_message(user, original_message, lowercase_only, "", response)
        return response

    #step 6: check if show more or show all is called
    if show_more == True:
        links_last_message_more = get_next_links(user)
        response = response + links_last_message_more

    if show_all == True:
        links_last_message_all = get_concerning_links(user)
        response = response + links_last_message_all[0]

    #step 7: add links if necessary
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
        how_many_links_to_show = int(how_many_links_to_show)
        if language_of_user == "english":
            response = response + "I've found " + str(number_of_links_found) + " results. "
        else:
            response = response + "Ich habe " + str(number_of_links_found) + " Resultate gefunden. "
        for i in range(0, number_of_links_found):
            if i == 0:
                #get domain name of best fitting response
                module = get_domain_name(links[i])[0]
                update_last_module_of_user(user, module)
            if i < how_many_links_to_show:
                response = response + links[i] +  "\n" +  "\n"
            else:
                break

        #step 8: add "is my answer helpful" after every 5th link interaction
        counter = get_links_counter_for_helpful(user)
        if counter[0] % 5 == 0:    #every 5th link interaction added by "is my answer helpful"
            if language_of_user == "english":
                response = response + "Is my answer helpful?"
            else:
                response = response + "War meine Antwort hilfreich?"

    #step 9: check if user answered with yes or no if answer was helpful
    else:
        if message_contains_yes_or_no != False:
            counter = get_links_counter_for_helpful(user)
            if counter[0] % 5 == 0:
                last_message = get_last_message(user)[0]
                helpful_string_english = "Is my answer helpful?"
                helpful_string_german = "War meine Antwort hilfreich?"
                if helpful_string_english in last_message or helpful_string_german in last_message:
                    if language_of_user == "english":
                        response = response + "Thanks for your feedback!"
                    else:
                        response = response + "Danke für dein Feedback!"
                    last_module = get_last_module_of_user(user)[0]
                    update_modul_satisfaction(last_module, message_contains_yes_or_no)
                    create_new_message(user, original_message, lowercase_only, "", response)
                    return response

    #step 10: check if default answer is necessary
    if response == "":
        if message_contains_yes_or_no != False:
            return response
    
        if language_of_user == "english":
            default_1 = "Can you please specify your question?"
            default_2 = "I haven't found anything fitting."
            default_3 = "I've found no match to your question."
            default_4 = "I can't answer that."
        else:
            default_1 = "Kannst du deine Frage bitte spezifizieren?"
            default_2 = "Ich kenne keine passende Antwort."
            default_3 = "Ich habe keine Übereinstimmung gefunden."
            default_4 = "Das kann ich nicht beantworten."
        default_answer = [default_1, default_2, default_3, default_4]
        response = random.choice(default_answer)

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

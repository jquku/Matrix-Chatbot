import sys
import re

sys.path.append("./../")

from services.database_service import data_basis_query, get_number_of_links_to_be_shown, set_number_of_links_to_be_shown, get_concerning_links, get_next_links, get_all_modules
from services.database_service import get_original_topic, check_if_topic_already_in_statistic, create_new_statistic_entry, increment_statistic_topic_counter, get_stats
from services.database_service import change_stats_preferred, links_from_multiple_modules, get_last_message, get_all_modules, get_all_links_of_last_response
from services.database_service import check_if_link_belongs_to_module, change_student_language

def evaluate_message(user, message):

    lowercase_only = message[0]
    standardized_message = message[1]
    only_tokens = message[2]

    help = help_called(lowercase_only)
    number_of_links = change_standard_number_of_links_called(user, lowercase_only)
    changed_number_of_stats = change_number_of_stats_to_return(user, lowercase_only)
    show_more = show_more_called(lowercase_only)
    show_all = show_all_called(lowercase_only)
    greetings = greetings_involved(standardized_message)
    goodbyes = goodbyes_involved(standardized_message)
    stats_called_result = stats_called(only_tokens)
    message_contains_yes_or_no = check_if_message_contains_yes_or_no(only_tokens)
    change_language = change_user_language(user, lowercase_only)

    #print("HELP: " + str(help))
    #print("CHANGE NUMBER OF LINKS: " + str(number_of_links))
    #print("SHOW MORE: " + str(show_more))
    #print("SHOW ALL: " + str(show_all))
    #print("GREETINGS: " + str(greetings))
    #print("GOODBYES: " + str(goodbyes))

    links = compare_message_with_data_basis(standardized_message)
    #print("LINKS BEFORE BEFORE BEFORE: " + str(type(links)) + str(links) + str(len(links)))
    links = sort_links_by_matching(links, standardized_message)

    #print("LINKS AFTER AFTERAFTER AFTER: " + str(type(links)) + str(links) + str(len(links)))

    links_from_multiple_modules = check_if_links_from_multiple_modules(links)
    answer_given_for_multiple_modules = check_if_answer_for_results_from_multiple_modules_given(user, only_tokens)
    if answer_given_for_multiple_modules != False:
        links = answer_given_for_multiple_modules
        links_from_multiple_modules = False
    print("LINKS FROM MULTIPLE MODULES: " + str(links_from_multiple_modules))
    print("LINKS: " + str(links))
    evaluation = (lowercase_only, standardized_message, help, number_of_links, show_more, show_all, greetings, goodbyes, stats_called_result, message_contains_yes_or_no, changed_number_of_stats, change_language, links_from_multiple_modules, links)
    return evaluation

def help_called(message):

    help_phrases = ['help', 'i need help', 'help me', 'hilf mir', 'hilfe', 'options', 'optionen']
    for i in range(0, len(help_phrases)):
        current = help_phrases[i]
        if current in message:
            return True
    return False

def change_standard_number_of_links_called(user, message):

    if "links = " in message or "link = " in message or "links= " in message or "link=" in message:

        number = re.findall(r'\d+', message)

        if len(number) == 1:
            number = number[0]
            set_number_of_links_to_be_shown(user, number)
            return True
    else:
        return False

def change_number_of_stats_to_return(user, message):
    if "stats = " in message or "stat = " in message or "stats= " in message or "stat=" in message:

        number_of_stats = re.findall(r'\d+', message)
        number_of_stats = number_of_stats[0]
        change_stats_preferred(user, number_of_stats)
        return True
    else:
        return False

def change_user_language(user, message):
    if "language = " in message or "language=" in message or "lang =" in message or "lang=" in message or "sprache=" in message or "sprache =" in message:

        if "en" in message or "american" in message:
            change_student_language(user, 'english')
            return True

        if "ger" in message or "de" in message:
            print("DEUTSCH")
            change_student_language(user, 'german')
            return True

        else:
            return False

    else:
        return False

def show_more_called(message):

    if "show more" in message or "zeig mehr" in message:
        return True
    else:
        return False

def show_all_called(message):

    if "show all" in message or "zeig alles" in message:
        return True
    else:
        return False



def greetings_involved(tokens):  #greeting forms found on the internet
    phrases = ["hi", "hello", "hey", "helloo", "hellooo", "g morining",
        "gmorning","good morning", "morning", "good day", "good afternoon",
        "good evening","greetings", "greeting", "good to see you",
        "its good seeing you","how are you", "how're you", "how are you doing",
        "how ya doin'","how ya doin", "how is everything",
        "how is everything going","how's everything going", "how is you",
        "how's you", "how are things","how're things", "how is it going",
        "how's it going", "how's it goin'", "how's it goin",
        "how is life been treating you", "how's life been treating you",
        "how have you been", "how've you been", "what is up", "what's up",
        "what is cracking", "what's cracking", "what is good", "what's good",
        "what is happening", "what's happening", "what is new", "what's new",
        "what is neww", "g’day", "howdy", "hallo", "bonjour"]
    for i in range(0, len(tokens)):
        if tokens[i] in phrases:
            return True
    return False

def goodbyes_involved(tokens):
    phrases = ["goodbye", "au revoir", "bye", "tschüß", "tschau", "see you",
        "bye bye", "see you soon", "auf wiedersehen", "bis bald",
        "take it easy", "have a nice day", "take care", "goodnight",
        "catch you later", "peace", "peace out"]
    for i in range(0, len(tokens)):
        if tokens[i] in phrases:
            return True
    return False

def stats_called(tokens):
    stats_called = False
    phrases = ["statistics", "stat", "stats", "analytics", "statistik","analytik", "statistiken"]
    modules = get_all_modules()
    new_modules = []
    for j in range(0, len(modules)):
        new_modules.append(modules[j][0])
    modules = new_modules
    module = ""
    for i in range(0, len(tokens)):
        if tokens[i] in phrases:
            stats_called = True
        #module_found = any(tokens[i] in string for string in modules)
        module_found = [string for string in modules if tokens[i] in string]
        if len(module_found) > 0:
            module = module_found[0]
    if stats_called == True and module != "":
        return module
    else:
        return False

def check_if_message_contains_yes_or_no(tokens):
    phrases_yes = ["yes", "yeah", "jo", "ja", "klar", "for sure"]
    phrases_no = ["no", "not at all", "nah", "ne", "nein"]
    for i in range(0, len(tokens)):
        if tokens[i] in phrases_yes:
            #print("PHRASES YES")
            return 1
        if tokens[i] in phrases_no:
            #print("PHRASES NO")
            return -1
    return False


def compare_message_with_data_basis(message):
    link = data_basis_query(message)
    return link

def sort_links_by_matching(links, keywords):

    links = list(dict.fromkeys(links)) #remove doubles by transforming into dict
    only_topic = []
    for i in range(0, len(links)):
        only_topic.append(links[i][0])

    listA = list(only_topic)

    list_with_matching_coefficients = []
    new_links_list = []
    for m in range(0, len(listA)):
        current = []
        element = listA[m]
        #print("current element: " + str(element))
        current.append(element)
        current_list_a = " ".join(current).split()
        #print("current_list_a: " + str(current_list_a))
        #print("listB: " + str(keywords))
        setA = set(current_list_a)
        setB = set(keywords)

        overlap = setA & setB

        matching = float(len(overlap)) / len(setB) * 100

        if matching > 0:

            #print("current coefficient: " + str(matching))
            list_with_matching_coefficients.append(matching)
            new_links_list.append(links[m])

            if matching > 50:
                #print("matching: " + str(matching))
                query_result = get_original_topic(element)  #returns tuple
                original = query_result[0]
                module = query_result[1]
                #print("original: " + str(type(original)) + str(original))
                #original = str(original[0])
                module_in_statistic = check_if_topic_already_in_statistic(original)
                #print("topic_in_statistic: " + str(module) + str(type(module)))
                #topic_in_statistic = str(topic_in_statistic[0])
                #print("topic_in_statistic: " + str(topic_in_statistic))
                if module_in_statistic is None:
                    create_new_statistic_entry(module, original)
                else:
                    increment_statistic_topic_counter(module, original)
                #if len(topic_in_statistic) == "":
                #    create_new_statistic_entry()
                #if topic_in_statistic == True:
                #    increment_statistic_topic_counter
                #else:
                #    create_new_statistic_entry

    #print("list with matching coefficients: " + str(list_with_matching_coefficients))
    #print("new links list: " + str(new_links_list))
    #sort list based on list with matching coefficients

    sorted_list = [x for _,x in sorted(zip(list_with_matching_coefficients, new_links_list))]
    sorted_list.reverse()
    #print("sorted_list: " + str(sorted_list))

    #each list element contains topic + link
    all_links = []
    if len(sorted_list) > 0:
        for j in range(0, len(sorted_list)):
            #print("current element: " + str(sorted_list[j][1]))
            all_links.append(sorted_list[j][1])   #only return link, not whole tuple
    #print("all links: " + str(all_links))
    all_links = list(dict.fromkeys(all_links)) #potentially two topics have same link; remove from list
    return all_links

def check_if_links_from_multiple_modules(links):
    list_of_moduls_with_links = []
    for i in range(0, len(links)):
        current = links[i]
        module = links_from_multiple_modules(current)
        if module not in list_of_moduls_with_links:
            list_of_moduls_with_links.append(module)
    #print("LISTE: " + str(list_of_moduls_with_links))
    if len(list_of_moduls_with_links) == 1:
        #print("RETURN FALSE")
        return False#
    else:
        all_modules_string = ""
        for j in range(0, len(list_of_moduls_with_links)):
            current_module = list_of_moduls_with_links[j]
            all_modules_string = all_modules_string + "- " + current_module + "\n"
        #print("ALL MODULES STRING: " + str(all_modules_string))
        return all_modules_string

def check_if_answer_for_results_from_multiple_modules_given(user, tokens):
    modules_to_show_links_of = []
    last_message = get_last_message(user)
    if last_message == None:
        return False
    last_message = last_message[0]
    #print("LAST MESSAGES LAST MESSAGE LAST MESSAGES: \n" + str(last_message))
    links_from_multiple_modules_string = "Which module are you interested in?"
    if links_from_multiple_modules_string in last_message:
        last_message = last_message.lower()
        #check if current message contains module that was also in last message
        all_modules = get_all_modules()
        new_list_of_all_modules = []
        for j in range(0, len(all_modules)):
            new_list_of_all_modules.append(all_modules[j][0])
        #print("ALL MODULES: " + str(new_list_of_all_modules) + str(type(new_list_of_all_modules)) + str(len(new_list_of_all_modules)))
        for i in range(0, len(new_list_of_all_modules)):
            current_module = new_list_of_all_modules[i]
            print("Tokens: " + str(tokens))
            for t in range(0, len(tokens)):
                current_token = tokens[t]
                if current_token in current_module:
                    modules_to_show_links_of.append(current_module)
            #if current_module in message:
            #    modules_to_show_links_of.append(current_module)
    if len(modules_to_show_links_of) == 0:
        return False
    print("modules to show links of: " + str(modules_to_show_links_of))
    #get links of last response
    all_links  = get_all_links_of_last_response(user)
    if all_links != None:
        all_links = all_links[0]
    all_links_string = all_links
    all_links = all_links.split()
    print("ALL LINKS: " + str(all_links))
    new_links = []
    for k in range(0, len(all_links)):
        current_link = all_links[k]
        print("CURRENT LINK: " + str(current_link))
        module = check_if_link_belongs_to_module(current_link)[0]
        print("Belonging module: " + str(module))
        if module in modules_to_show_links_of:
            new_links.append(current_link)
            print("should be in")
    print("NEW LINKS: " + str(new_links))
    return new_links

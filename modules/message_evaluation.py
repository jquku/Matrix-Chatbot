import sys
import re

sys.path.append("./../")

from services.database_service import data_basis_query, get_number_of_links_to_be_shown, set_number_of_links_to_be_shown, get_concerning_links, get_next_links, get_all_modules
from services.database_service import get_original_topic, check_if_topic_already_in_statistic, create_new_statistic_entry, increment_statistic_topic_counter, get_stats


def evaluate_message(user, message):

    lowercase_only = message[0]
    standardized_message = message[1]
    only_tokens = message[2]

    help = help_called(lowercase_only)
    number_of_links = change_standard_number_of_links_called(user, lowercase_only)
    show_more = show_more_called(lowercase_only)
    show_all = show_all_called(lowercase_only)
    greetings = greetings_involved(standardized_message)
    goodbyes = goodbyes_involved(standardized_message)
    stats_called_result = stats_called(only_tokens)
    message_contains_yes_or_no = check_if_message_contains_yes_or_no(standardized_message)

    print("HELP: " + str(help))
    print("CHANGE NUMBER OF LINKS: " + str(number_of_links))
    print("SHOW MORE: " + str(show_more))
    print("SHOW ALL: " + str(show_all))
    print("GREETINGS: " + str(greetings))
    print("GOODBYES: " + str(goodbyes))

    links = compare_message_with_data_basis(standardized_message)
    print("LINKS BEFORE BEFORE BEFORE: " + str(type(links)) + str(links) + str(len(links)))
    links = sort_links_by_matching(links, standardized_message)

    print("LINKS AFTER AFTERAFTER AFTER: " + str(type(links)) + str(links) + str(len(links)))
    evaluation = (lowercase_only, standardized_message, help, number_of_links, show_more, show_all, greetings, goodbyes, stats_called_result, message_contains_yes_or_no, links)
    return evaluation

def help_called(message):

    help_phrases = ['help', 'i need help', 'help me', 'hilf mir', 'hilfe']
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
    module = ""
    for i in range(0, len(tokens)):
        if tokens[i] in phrases:
            stats_called = True
        #module_found = any(tokens[i] in string for string in modules)
        module_found = [string for string in modules if tokens[i] in string]
        if len(module_found) > 0:
            module = module_found[0]
    print(str(stats_called) + str(module))
    if stats_called == True and module != "":
        return module
    else:
        return False

def check_if_message_contains_yes_or_no(tokens):
    phrases_yes = ["yes", "yeah", "jo", "ja", "klar", "for sure"]
    phrases_no = ["no", "not at all", "nah", "ne", "nein"]
    for i in range(0, len(tokens)):
        if tokens[i] in phrases_yes:
            return 1
        if tokens[i] in phrases_no:
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
        print("current element: " + str(element))
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

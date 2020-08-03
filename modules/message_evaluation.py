import sys
import re

sys.path.append("./../")

from services.database_service import (data_basis_query,
    get_number_of_links_to_be_shown, set_number_of_links_to_be_shown,
    get_concerning_links, get_next_links,
    get_original_topic, check_if_topic_already_in_statistic,
    create_new_statistic_entry, increment_statistic_topic_counter, get_stats,
    change_stats_preferred, links_from_multiple_domains, get_last_message,
    get_all_domains, get_all_links_of_last_response,
    check_if_link_belongs_to_module, change_user_language,
    get_domain_name_based_on_id, data_basis_query, data_basis_query_small_talk,
    data_basis_query_organisational)

'''
complete evaluation of the message, also checks if there is an entry
from the knowledge domain in the db fitting the user query
'''

def evaluate_message(user, message):
    '''controls the evaluation'''
    lowercase_only = message[0]
    standardized_message = message[1]
    only_tokens = message[2]
    after_lemmitation = message[3]

    #kick off evaluation process
    help = help_called(lowercase_only)
    number_of_links = change_standard_number_of_links_called(user,
        lowercase_only)
    changed_number_of_stats = change_number_of_stats_to_return(user,
        lowercase_only)
    show_more = show_more_called(lowercase_only)
    show_all = show_all_called(lowercase_only)
    stats_called_result = stats_called(only_tokens)
    message_contains_yes_or_no = check_if_message_contains_yes_or_no(only_tokens)
    message_contains_thank_you = check_if_message_contains_thank_you(only_tokens)
    change_language = change_user_language(user, lowercase_only)


    links = data_basis_query(standardized_message)
    links = sort_links_by_matching(links, standardized_message)
    small_talk = data_basis_query_small_talk(after_lemmitation)
    small_talk = sort_links_by_matching_general(small_talk, after_lemmitation,
        65)
    if len(small_talk) > 0:
        small_talk = [small_talk[0]]

    organisational = data_basis_query_organisational(after_lemmitation)
    organisational = sort_links_by_matching_general(organisational,
        after_lemmitation, 75)

    links_from_multiple_domains = check_if_links_from_multiple_domains(links)
    answer_given_for_multiple_modules = check_if_answer_for_results_from_multiple_domains_given(user, only_tokens)
    if answer_given_for_multiple_modules != False:
        links = answer_given_for_multiple_modules
        links_from_multiple_domains = False

    #collect evaluation results and store them into one
    evaluation = (lowercase_only, standardized_message, help, number_of_links,
        show_more, show_all, stats_called_result, message_contains_yes_or_no,
        message_contains_thank_you, changed_number_of_stats, change_language,
        links_from_multiple_domains, links, small_talk, organisational)
    return evaluation

def help_called(message):
    '''checks if user has called help/options'''
    help_phrases = ['help', 'i need help', 'help me', 'hilf mir', 'hilfe',
        'options', 'optionen']
    for i in range(0, len(help_phrases)):
        current = help_phrases[i]
        if current in message:
            return True
    return False

def change_standard_number_of_links_called(user, message):
    '''checks if user wants to change the output's number of links'''
    if "links" in message or "link" in message or "Links" in message or "Link" in message:
        if "=" in message:
            number = re.findall(r'\d+', message)
            if len(number) == 1:
                number = number[0]
                set_number_of_links_to_be_shown(user, number)
                return True
    return False

def change_number_of_stats_to_return(user, message):
    '''checks if user wants to increase or reduce the stats scope'''
    if "stats" in message or "stat" in message or "Stats" in message or "Stat" in message:
        if "=" in message:
            number_of_stats = re.findall(r'\d+', message)
            if number_of_stats != None and len(number_of_stats)>0:
                number_of_stats = number_of_stats[0]
                change_stats_preferred(user, number_of_stats)
                return True
    return False

def change_user_language(user, message):
    '''checks if a language change was requested'''
    if "language" in message or "Language" in message or "sprache" in message or "Sprache" in message:

        if "=" in message:

            if "en" in message or "american" in message:
                change_user_language(user, 'english')
                return True

            if "ger" in message or "de" in message:
                change_user_language(user, 'german')
                return True
    return False

def show_more_called(message):
    '''checks if keywords show more called'''
    if "show" in message or "zeig" in message:
        if "more" in message or "mehr" in message:
            return True
    else:
        return False

def show_all_called(message):
    '''checks if keywords show all called?'''
    if "show" in message or "zeig" in message:
        if "all" in message or "alles" in message:
            return True
    else:
        return False

def stats_called(tokens):
    '''checks if user wants to receive stats'''
    stats_called = False
    phrases = ["statistics", "stat", "stats", "analytics", "statistik",
        "analytik", "statistiken"]
    modules = get_all_domains()
    new_modules = []
    for j in range(0, len(modules)):
        new_modules.append(modules[j][0])
    modules = new_modules
    module = ""
    for i in range(0, len(tokens)):
        if tokens[i] in phrases:
            stats_called = True
        module_found = [string for string in modules if tokens[i] in string]
        if len(module_found) > 0:
            module = module_found[0]
    if stats_called == True and module != "":
        return module
    else:
        return False

def check_if_message_contains_yes_or_no(tokens):
    '''checks if the user's message contains a yes or no'''
    phrases_yes = ["yes", "yeah", "jo", "ja", "klar", "for sure"]
    phrases_no = ["no", "not at all", "nah", "ne", "nein"]
    for i in range(0, len(tokens)):
        if tokens[i] in phrases_yes:
            return 1    #1 means yes
        if tokens[i] in phrases_no:
            return -1   #-1 means no
    return False

def check_if_message_contains_thank_you(tokens):
    '''checks if the user's message contains a thank you'''
    phrases = ['thank you', 'thanks', 'danke', 'dankeschön', 'vielen dank',
        'lieben dank', 'thank you very much', 'thx', 'merci']
    for i in range(0, len(tokens)):
        if tokens[i] in phrases:
            return True
    return False

def sort_links_by_matching(links, keywords):
    '''sort fitting responses based on matching coefficient'''
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
        current.append(element)
        current_list_a = " ".join(current).split()
        setA = set(current_list_a)
        setB = set(keywords)
        overlap = setA & setB

        matching = float(len(overlap)) / len(setB) * 100    #calculate matching

        if matching > 0:

            list_with_matching_coefficients.append(matching)
            new_links_list.append(links[m])

            if matching > 50: #increase stats counter for fitting links
                query_result = get_original_topic(element)
                original = query_result[0]
                module_id = query_result[1]
                module = get_domain_name_based_on_id(module_id)
                module_in_statistic = check_if_topic_already_in_statistic(original)
                if module_in_statistic is None:
                    create_new_statistic_entry(module, original)
                else:
                    increment_statistic_topic_counter(module, original)

    sorted_list = [x for _,x in sorted(zip(list_with_matching_coefficients,
        new_links_list))]
    sorted_list.reverse()

    #each list element contains topic + response
    all_links = []
    if len(sorted_list) > 0:
        for j in range(0, len(sorted_list)):
            all_links.append(sorted_list[j][1])   #only return link
    all_links = list(dict.fromkeys(all_links)) #remove doubles
    return all_links

def sort_links_by_matching_general(links, keywords, value):
    '''sort fitting responses from small talk based on matching coefficient'''
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
        current.append(element)
        current_list_a = " ".join(current).split()
        setA = set(keywords)
        setB = set(current_list_a)
        overlap = setA & setB

        matching = float(len(overlap)) / len(setB) * 100
        if matching >= value:

            list_with_matching_coefficients.append(matching)
            new_links_list.append(links[m])

    sorted_list = [x for _,x in sorted(zip(list_with_matching_coefficients,
        new_links_list))]
    sorted_list.reverse()

    #each list element contains topic + response
    all_links = []
    if len(sorted_list) > 0:
        for j in range(0, len(sorted_list)):
            all_links.append(sorted_list[j][1])
    all_links = list(dict.fromkeys(all_links)) #remove topics with same response
    return all_links

def check_if_links_from_multiple_domains(links):
    '''fitting responses can also come from multiple knowledge domains'''
    list_of_moduls_with_links = []
    for i in range(0, len(links)):
        current = links[i]
        module = links_from_multiple_domains(current)
        if module not in list_of_moduls_with_links:
            list_of_moduls_with_links.append(module)
    if len(list_of_moduls_with_links) == 1:
        return False#
    else:
        all_domains_string = ""
        for j in range(0, len(list_of_moduls_with_links)):
            current_domain = list_of_moduls_with_links[j]
            all_domains_string = all_domains_string + "- " + current_domain + "\n"
        return all_domains_string

def check_if_answer_for_results_from_multiple_domains_given(user, tokens):
    '''in case multiple fitting responses from different domains found'''
    modules_to_show_links_of = []
    last_message = get_last_message(user)
    if last_message == None:
        return False
    last_message = last_message[0]
    links_from_multiple_domains_string = "Which module are you interested in?"
    if links_from_multiple_domains_string in last_message:
        last_message = last_message.lower()
        #check if current message contains module that was also in last message
        all_domains = get_all_domains()
        new_list_of_all_domains = []
        for j in range(0, len(all_domains)):
            new_list_of_all_domains.append(all_domains[j][0])
        for i in range(0, len(new_list_of_all_domains)):
            current_domain = new_list_of_all_domains[i]
            for t in range(0, len(tokens)):
                current_token = tokens[t]
                if current_token in current_domain:
                    modules_to_show_links_of.append(current_domain)
    if len(modules_to_show_links_of) == 0:
        return False
    all_links  = get_all_links_of_last_response(user)
    if all_links != None:
        all_links = all_links[0]
    all_links_string = all_links
    all_links = all_links.split()
    new_links = []
    for k in range(0, len(all_links)):
        current_link = all_links[k]
        module = check_if_link_belongs_to_module(current_link)[0]
        if module in modules_to_show_links_of:
            new_links.append(current_link)
    return new_links

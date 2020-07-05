import sys
import re
import psycopg2

from config import Config

config_filepath = "config.yaml"
config = Config(config_filepath)

def connect_to_database():
    connection = psycopg2.connect(
        database = config.name,
        user = config.user,
        password = config.password,
        host = config.host,
        port = config.port)
    return connection

def check_if_room_is_existing(room_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM room WHERE room_id = %s", [room_id])
    query_result = cursor.fetchall()
    cursor.close()
    connection.close()
    if len(query_result) == 0:
        return False
    return True

def check_if_student_is_existing(name):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_chatbot WHERE name = %s", [name])
    query_result = cursor.fetchall()
    cursor.close()
    connection.close()
    if len(query_result) == 0:
        return False
    return True

def get_user_chatbot_id(user_name):
    #print("USER NAME: " + str(user_name))
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM user_chatbot WHERE name = %s", [user_name])
    query_result = cursor.fetchone()
    #print("USER CHATBOT ID RESULT: " + str(query_result))
    query_result = query_result[0]
    return query_result

def get_module_id(module):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM module WHERE name = %s", [module])
    query_result = cursor.fetchone()
    query_result = query_result[0]
    return query_result

def create_new_room(room_id, room_name, user_name):
    user_chatbot_id = get_user_chatbot_id(user_name)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO room(room_id, room_name, user_chatbot_id) VALUES (%s, %s, %s)", [room_id, room_name, user_chatbot_id])
    connection.commit()
    cursor.close()
    connection.close()

def create_new_student(name, last_module):
    last_module = get_module_id(last_module)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO user_chatbot(name, last_module, links_preferred, stats_preferred, links_counter, language) VALUES (%s, %s, %s, %s, %s, %s)", [name, last_module, 2, 5, 0, "english"])
    connection.commit()
    cursor.close()
    connection.close()

def create_new_message(student_name, body, information_extracted, all_links, response):
    user_chatbot_id = get_user_chatbot_id(student_name)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO message(user_chatbot_id, body, information_extracted, all_links, response) VALUES (%s, %s, %s, %s, %s)", [user_chatbot_id, body, information_extracted, all_links, response])
    connection.commit()
    cursor.close()
    connection.close()

def add_data_basis_entry(module_id, original, topic, url):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO data_basis(module_id, original, topic, link) VALUES (%s, %s, %s, %s)", [module_id, original, topic, url])
    connection.commit()
    cursor.close()
    connection.close()

def add_new_module(name, original, source):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO module(name, original, source, satisfaction, feedback_given) VALUES (%s, %s, %s, %s, %s) RETURNING id", [name, original, source, 0, 0])
    connection.commit()
    module_id = cursor.fetchone()
    module_id = module_id[0]
    cursor.close()
    connection.close()
    return module_id

def data_basis_query(keywords):
    if len(keywords) == 0:
        return []
    module_general_id = get_module_general_id()
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT topic, link FROM data_basis WHERE module_id != " + str(module_general_id) + " AND original != 'Organisational'"
    query = query + " AND topic LIKE '%" + keywords[0] + "%'"
    for i in range(1, len(keywords)):
        query = query + " OR module_id != " + str(module_general_id) + "  AND original != 'Organisational' AND topic LIKE '%" + keywords[i] + "%'"
    cursor.execute(query)
    links = cursor.fetchall()    #returns tuple
    cursor.close()
    connection.close()
    return links

def data_basis_query_small_talk(keywords):
    print("keyowrds:" + str(keywords))
    print("calling the method")
    if len(keywords) == 0:
        return []
    module_general_id = get_module_general_id()
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT topic, link FROM data_basis WHERE module_id = " + str(module_general_id)
    query = query + " AND topic LIKE '%" + keywords[0] + "%'"
    for i in range(1, len(keywords)):
        query = query + " OR module_id = " + str(module_general_id) + " AND topic LIKE '%" + keywords[i] + "%'"
    cursor.execute(query)
    links = cursor.fetchall()    #returns tuple
    print("links: " + str(links))
    cursor.close()
    connection.close()
    return links

def data_basis_query_organisational(keywords):
    if len(keywords) == 0:
        return []
    module_general_id = get_module_general_id()
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT topic, link FROM data_basis WHERE module_id != " + str(module_general_id) + " AND original = 'Organisational'"
    query = query + " AND topic LIKE '%" + keywords[0] + "%'"
    for i in range(1, len(keywords)):
        query = query + " OR module_id != " + str(module_general_id) + "  AND original = 'Organisational' AND topic LIKE '%" + keywords[i] + "%'"
    cursor.execute(query)
    links = cursor.fetchall()    #returns tuple
    cursor.close()
    connection.close()
    return links

def get_module_general_id():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM module WHERE name = 'general'")
    result = cursor.fetchall()
    print("result:" + str(result))
    result = str(result[0][0])
    #result = str(result[0])
    cursor.close()
    connection.close()
    return result

def get_number_of_links_to_be_shown(user):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT links_preferred FROM user_chatbot WHERE name = %s", [user])
    result = cursor.fetchall()
    result = str(result[0][0])
    #result = str(result[0])
    cursor.close()
    connection.close()
    return result

def set_number_of_links_to_be_shown(user, number):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("UPDATE user_chatbot SET links_preferred = %s WHERE name = %s", [number, user])
    connection.commit()
    cursor.close()
    connection.close()

#method for 'show all'; returns all links
def get_concerning_links(user):
    user_chatbot_id = get_user_chatbot_id(user)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT all_links FROM message WHERE user_chatbot_id = %s and all_links != '' order by id desc limit 1", [user_chatbot_id])
    fitting_links = cursor.fetchall()
    number_of_links = len(fitting_links)
    result = fitting_links[number_of_links-1] #get all_links from last message
    cursor.close()
    connection.close()
    return result

def get_next_links(user):
    user_chatbot_id = get_user_chatbot_id(user)
    connection = connect_to_database()
    cursor = connection.cursor()
    all_links = get_concerning_links(user)
    #print("all_links: " + str(all_links))
    number_of_links_to_be_shown = get_number_of_links_to_be_shown(user)
    #print("NUMBER OF LINKS TO SHOW: " + str(number_of_links_to_be_shown))
    cursor.execute("SELECT response FROM message WHERE user_chatbot_id = %s and all_links != '' order by id desc limit 1", [user_chatbot_id])
    last_message = cursor.fetchone()
    #print("QUERY RESULT RESULT RESULT: " + str(last_message) + str(type(last_message)) + str(len(last_message)))
    last_message = str(last_message[0])
    last_message = last_message.replace("\n\n", " ")
    #print("2222222222222222: " + str(last_message))
    last_message = last_message.split()
    #last_message = [x.strip() for x in last_message.split('\n\n')]
    #last_message = last_message.split()
    #print("QUERY RESULT RESULT RESULT NEW NEW NEW: " + str(last_message))
    all_links = list(all_links)
    links_in_list = all_links[0].split()
    #print("LINKS IN LIST LINKS IN LIST LINKS IN LIST: " + str(links_in_list))
    highest_index = 0
    #print("len(links_in_list:) " + str(len(links_in_list)))
    for i in range(0, len(links_in_list)):
        #print("i: " + str(i))
        current = links_in_list[i]
        #print("current: " + str(current))
        #if current in last_message:
        element_found = False
        for k in range(0, len(last_message)):
            #print("LAST MESSAGE[k]: " + str(last_message[k]) + " CURRENT: " + str(current))
            if str(last_message[k]) == str(current):
                element_found = True
        if element_found == True:
            #print("current in message")
            if i >= highest_index:
                highest_index = i + 1
                #highest_index = i
    #print("new highest index: " + str(highest_index))
    #print("PRE CUTTING: " + str(links_in_list) + str(len(links_in_list)))
    links_in_list = links_in_list[highest_index:]
    #print("LINKS IN LIST LINKS IN LIST LINKS IN LIST 2: " + str(links_in_list))
    if int(number_of_links_to_be_shown) > len(links_in_list):
        number_of_links_to_be_shown = len(links_in_list)
    output = ""

    for j in range(0, int(number_of_links_to_be_shown)):
        output = output + links_in_list[j] + "\n" + "\n"
    return output

def get_original_topic(topic):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT original, module_id FROM data_basis WHERE topic = %s", [topic])
    original = cursor.fetchone()
    cursor.close()
    connection.close()
    return original

def check_if_topic_already_in_statistic(topic):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT module_id FROM statistics WHERE topic = %s", [topic])
    module = cursor.fetchone()
    cursor.close()
    connection.close()
    return module

def create_new_statistic_entry(module, topic):
    module_id = get_module_id(module)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO statistics(module_id, topic, questioned) VALUES (%s, %s, %s)", [module_id, topic, 1])
    connection.commit()
    cursor.close()
    connection.close()

def increment_statistic_topic_counter(module, topic):
    module_id = get_module_id(module)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("UPDATE statistics SET questioned = questioned + 1 WHERE module_id = %s and topic = %s", [module_id, topic])
    connection.commit()
    cursor.close()
    connection.close()

def get_module_id_for_stats(module):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM module WHERE name LIKE '%" + module + "%'")
    module_id = cursor.fetchone()
    module_id = module_id[0] #vorher [0][0]
    cursor.close()
    connection.close()
    return module_id


def get_stats(module):
    module_id = get_module_id_for_stats(module)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT topic, questioned FROM statistics WHERE module_id = %s order by questioned desc", [module_id])
    output = cursor.fetchall()
    cursor.close()
    connection.close()
    return output

def increment_links_counter_for_helpful(student):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("UPDATE user_chatbot SET links_counter = links_counter + 1 WHERE name = %s", [student])
    connection.commit()
    cursor.close()
    connection.close()

def get_links_counter_for_helpful(student):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT links_counter FROM user_chatbot WHERE name = %s", [student])
    counter = cursor.fetchone()
    cursor.close()
    connection.close()
    return counter

#method for 'show all'; returns all links
def get_last_message(user):
    user_chatbot_id = get_user_chatbot_id(user)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT response FROM message WHERE user_chatbot_id = %s order by id desc limit 1", [user_chatbot_id])
    last_response = cursor.fetchone()
    cursor.close()
    connection.close()
    return last_response

def update_modul_satisfaction(module, factor):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("UPDATE module SET satisfaction = satisfaction + %s, feedback_given = feedback_given + 1 WHERE name = %s", [factor, module])
    connection.commit()
    cursor.close()
    connection.close()

def update_last_module_of_user(user, last_module):
    last_module = get_module_id(last_module)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("UPDATE user_chatbot SET last_module = %s WHERE name = %s", [last_module, user])
    connection.commit()
    cursor.close()
    connection.close()

def get_last_module_of_user(user):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM module join (SELECT last_module FROM user_chatbot WHERE name = %s) m on m.last_module=module.id",[user])
    last_module = cursor.fetchone()
    cursor.close()
    connection.close()
    return last_module

def get_module_name(link):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM module join (SELECT module_id FROM data_basis WHERE link = %s) m on m.module_id=module.id", [link])
    module = cursor.fetchone()
    cursor.close()
    connection.close()
    return module

def get_module_name_based_on_id(module_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM module WHERE id = %s", [module_id])
    module = cursor.fetchone()
    cursor.close()
    connection.close()
    return module

def add_organisation_entry(module, original, topic, response):
    module_id = get_module_id(module)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO data_basis(module_id, original, topic, link) VALUES (%s, %s, %s, %s)", [module_id, original, topic, response])
    connection.commit()
    cursor.close()
    connection.close()

def get_organisation_text(module):
    module_id = get_module_id(module)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT original FROM data_basis WHERE module_id = %s and topic = 'Organisation'", [module_id])
    module = cursor.fetchone()
    cursor.close()
    connection.close()
    return module

def check_if_module_already_in_data_basis(module):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT module_id FROM data_basis join (SELECT id FROM module WHERE name = %s) i on i.id=module_id", [module])
    module = cursor.fetchone()
    cursor.close()
    connection.close()
    return module

def delete_existing_data_basis(module):
    module_id = get_module_id(module)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM data_basis WHERE module_id = %s", [module_id])
    cursor.close()
    connection.close()

def get_stats_preferred(user):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT stats_preferred FROM user_chatbot WHERE name = %s", [user])
    number_of_stats_to_return = cursor.fetchone()
    cursor.close()
    connection.close()
    return number_of_stats_to_return

def change_stats_preferred(user, stats_preferred):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("UPDATE user_chatbot SET stats_preferred = %s WHERE name = %s", [stats_preferred, user])
    connection.commit()
    cursor.close()
    connection.close()

def links_from_multiple_modules(link):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT module_id FROM data_basis WHERE link = %s", [link])
    module_id = cursor.fetchone()
    module_id = module_id[0]
    cursor.execute("SELECT original FROM module WHERE id = %s", [module_id])
    original_module_name = cursor.fetchone()
    original_module_name = original_module_name[0]
    cursor.close()
    connection.close()
    return original_module_name

def get_all_modules():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM module")
    all_modules = cursor.fetchall()
    cursor.close()
    connection.close()
    return all_modules

def get_all_modules_original():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT original FROM module")
    all_modules = cursor.fetchall()
    cursor.close()
    connection.close()
    return all_modules

def get_all_links_of_last_response(user):
    user_id = get_user_chatbot_id(user)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT all_links FROM message WHERE user_chatbot_id = %s order by id desc limit 1", [user_id])
    all_links = cursor.fetchone()
    cursor.close()
    connection.close()
    return all_links

def check_if_link_belongs_to_module(link):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM module join (SELECT module_id FROM data_basis WHERE link = %s) m on m.module_id=module.id", [link])
    module = cursor.fetchone()
    cursor.close()
    connection.close()
    return module

def add_salt_value(value):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO salt(value) VALUES (%s)", [value])
    connection.commit()
    cursor.close()
    connection.close()

def get_salt_value():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT value FROM salt")
    value = cursor.fetchone()
    cursor.close()
    connection.close()
    return value

def change_student_language(user, language):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("UPDATE user_chatbot SET language = %s WHERE name = %s", [language, user])
    connection.commit()
    cursor.close()
    connection.close()

def get_student_language(user):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT language FROM user_chatbot WHERE name = %s", [user])
    language = cursor.fetchone()
    cursor.close()
    connection.close()
    return language

def check_if_general_module_existing():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM module WHERE name = 'general'")
    existing = cursor.fetchone()
    cursor.close()
    connection.close()
    return existing

def add_small_talk_document_to_data_basis(module_id, original, topic, link):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO data_basis(module_id, original, topic, link) VALUES (%s, %s, %s, %s)", [module_id, original, topic, link])
    connection.commit()
    cursor.close()
    connection.close()

def get_room_ids():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT room_id FROM room")
    ids = cursor.fetchall()
    cursor.close()
    connection.close()
    return ids

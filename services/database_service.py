import sys
import re
import psycopg2

from config import Config

config_filepath = "../config.yaml"
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

def check_if_user_is_existing(name):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_client WHERE name = %s", [name])
    query_result = cursor.fetchall()
    cursor.close()
    connection.close()
    if len(query_result) == 0:
        return False
    return True

def get_user_client_id(user_name):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM user_client WHERE name = %s", [user_name])
    query_result = cursor.fetchone()
    print("query result: " + str(query_result))
    if query_result != None:
        query_result = query_result[0]
    return query_result

def get_domain_description_id(domain_description):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM domain_description WHERE name = %s", [domain_description])
    query_result = cursor.fetchone()
    query_result = query_result[0]
    return query_result

def create_new_room(room_id, user_name):
    user_client_id = get_user_client_id(user_name)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO room(room_id, user_client_id) VALUES (%s, %s)", [room_id, user_client_id])
    connection.commit()
    cursor.close()
    connection.close()

def create_new_user(name, last_module):
    last_module = get_domain_description_id(last_module)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO user_client(name, last_module, links_preferred, stats_preferred, links_counter, language) VALUES (%s, %s, %s, %s, %s, %s)", [name, last_module, 2, 5, 0, "english"])
    connection.commit()
    cursor.close()
    connection.close()

def create_new_message(user_name, body, information_extracted, all_links, response):
    user_client_id = get_user_client_id(user_name)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO message(user_client_id, body, information_extracted, all_links, response) VALUES (%s, %s, %s, %s, %s)", [user_client_id, body, information_extracted, all_links, response])
    connection.commit()
    cursor.close()
    connection.close()

def add_data_basis_entry(domain_description_id, original, topic, response):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO data_basis(domain_description_id, original, topic, response) VALUES (%s, %s, %s, %s)", [domain_description_id, original, topic, response])
    connection.commit()
    cursor.close()
    connection.close()

def add_new_domain(name, original, source):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO domain_description(name, original, source, satisfaction, feedback_given) VALUES (%s, %s, %s, %s, %s) RETURNING id", [name, original, source, 0, 0])
    connection.commit()
    domain_id = cursor.fetchone()
    domain_id = domain_id[0]
    cursor.close()
    connection.close()
    return domain_id

def data_basis_query(keywords):
    if len(keywords) == 0:
        return []
    domain_general_id = get_domain_general_id()
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT topic, response FROM data_basis WHERE domain_description_id != " + str(domain_general_id) + " AND original != 'Organisational'"
    query = query + " AND topic LIKE '%" + keywords[0] + "%'"
    for i in range(1, len(keywords)):
        query = query + " OR domain_description_id != " + str(domain_general_id) + "  AND original != 'Organisational' AND topic LIKE '%" + keywords[i] + "%'"
    cursor.execute(query)
    response = cursor.fetchall()    #returns tuple
    cursor.close()
    connection.close()
    return response

def data_basis_query_small_talk(keywords):
    if len(keywords) == 0:
        return []
    domain_general_id = get_domain_general_id()
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT topic, response FROM data_basis WHERE domain_description_id = " + str(domain_general_id)
    query = query + " AND topic LIKE '%" + keywords[0] + "%'"
    for i in range(1, len(keywords)):
        query = query + " OR domain_description_id = " + str(domain_general_id) + " AND topic LIKE '%" + keywords[i] + "%'"
    cursor.execute(query)
    response = cursor.fetchall()    #returns tuple
    cursor.close()
    connection.close()
    return response

def data_basis_query_organisational(keywords):
    if len(keywords) == 0:
        return []
    domain_general_id = get_domain_general_id()
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT topic, response FROM data_basis WHERE domain_description_id != " + str(domain_general_id) + " AND original = 'Organisational'"
    query = query + " AND topic LIKE '%" + keywords[0] + "%'"
    for i in range(1, len(keywords)):
        query = query + " OR domain_description_id != " + str(domain_general_id) + "  AND original = 'Organisational' AND topic LIKE '%" + keywords[i] + "%'"
    cursor.execute(query)
    response = cursor.fetchall()    #returns tuple
    cursor.close()
    connection.close()
    return response

def get_domain_general_id():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM domain_description WHERE name = 'general'")
    result = cursor.fetchall()
    result = str(result[0][0])
    cursor.close()
    connection.close()
    return result

def get_number_of_links_to_be_shown(user):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT links_preferred FROM user_client WHERE name = %s", [user])
    result = cursor.fetchall()
    result = str(result[0][0])
    cursor.close()
    connection.close()
    return result

def set_number_of_links_to_be_shown(user, number):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("UPDATE user_client SET links_preferred = %s WHERE name = %s", [number, user])
    connection.commit()
    cursor.close()
    connection.close()

#method for 'show all'; returns all links
def get_concerning_links(user):
    user_client_id = get_user_client_id(user)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT all_links FROM message WHERE user_client_id = %s and all_links != '' order by id desc limit 1", [user_client_id])
    fitting_links = cursor.fetchall()
    number_of_links = len(fitting_links)
    result = fitting_links[number_of_links-1] #get all_links from last message
    cursor.close()
    connection.close()
    return result

def get_next_links(user):
    user_client_id = get_user_client_id(user)
    connection = connect_to_database()
    cursor = connection.cursor()
    all_links = get_concerning_links(user)
    number_of_links_to_be_shown = get_number_of_links_to_be_shown(user)
    cursor.execute("SELECT response FROM message WHERE user_client_id = %s and all_links != '' order by id desc limit 1", [user_client_id])
    last_message = cursor.fetchone()
    last_message = str(last_message[0])
    last_message = last_message.replace("\n\n", " ")
    last_message = last_message.split()
    all_links = list(all_links)
    links_in_list = all_links[0].split()
    highest_index = 0
    for i in range(0, len(links_in_list)):
        current = links_in_list[i]
        element_found = False
        for k in range(0, len(last_message)):
            if str(last_message[k]) == str(current):
                element_found = True
        if element_found == True:
            if i >= highest_index:
                highest_index = i + 1
    links_in_list = links_in_list[highest_index:]
    if int(number_of_links_to_be_shown) > len(links_in_list):
        number_of_links_to_be_shown = len(links_in_list)
    output = ""

    for j in range(0, int(number_of_links_to_be_shown)):
        output = output + links_in_list[j] + "\n" + "\n"
    return output

def get_original_topic(topic):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT original, domain_description_id FROM data_basis WHERE topic = %s", [topic])
    original = cursor.fetchone()
    cursor.close()
    connection.close()
    return original

def check_if_topic_already_in_statistic(topic):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT domain_description_id FROM statistics WHERE topic = %s", [topic])
    module = cursor.fetchone()
    cursor.close()
    connection.close()
    return module

def create_new_statistic_entry(module, topic):
    domain_description_id = get_domain_description_id(module)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO statistics(domain_description_id, topic, questioned) VALUES (%s, %s, %s)", [domain_description_id, topic, 1])
    connection.commit()
    cursor.close()
    connection.close()

def increment_statistic_topic_counter(module, topic):
    domain_description_id_id = get_domain_description_id_id(module)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("UPDATE statistics SET questioned = questioned + 1 WHERE domain_description_id = %s and topic = %s", [domain_description_id, topic])
    connection.commit()
    cursor.close()
    connection.close()

def get_domain_description_id_id_for_stats(module):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM domain_description WHERE name LIKE '%" + module + "%'")
    modudomain_idle_id = cursor.fetchone()
    domain_id = domain_id[0]
    cursor.close()
    connection.close()
    return domain_id


def get_stats(module):
    domain_description_id = get_domain_description_id_id_for_stats(module)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT topic, questioned FROM statistics WHERE domain_description_id = %s order by questioned desc", [domain_description_id])
    output = cursor.fetchall()
    cursor.close()
    connection.close()
    return output

def increment_links_counter_for_helpful(user):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("UPDATE user_client SET links_counter = links_counter + 1 WHERE name = %s", [user])
    connection.commit()
    cursor.close()
    connection.close()

def get_links_counter_for_helpful(user):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT links_counter FROM user_client WHERE name = %s", [user])
    counter = cursor.fetchone()
    cursor.close()
    connection.close()
    return counter

#method for 'show all'; returns all links
def get_last_message(user):
    user_client_id = get_user_client_id(user)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT response FROM message WHERE user_client_id = %s order by id desc limit 1", [user_client_id])
    last_response = cursor.fetchone()
    cursor.close()
    connection.close()
    return last_response

def update_modul_satisfaction(module, factor):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("UPDATE domain_description SET satisfaction = satisfaction + %s, feedback_given = feedback_given + 1 WHERE name = %s", [factor, module])
    connection.commit()
    cursor.close()
    connection.close()

def update_last_module_of_user(user, last_module):
    last_module = get_domain_description_id_id(last_module)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("UPDATE user_client SET last_module = %s WHERE name = %s", [last_module, user])
    connection.commit()
    cursor.close()
    connection.close()

def get_last_module_of_user(user):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM domain_description join (SELECT last_module FROM user_client WHERE name = %s) m on m.last_module=domain_description.id",[user])
    last_module = cursor.fetchone()
    cursor.close()
    connection.close()
    return last_module

def get_domain_name(response):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM domain_description join (SELECT domain_description_id FROM data_basis WHERE response = %s) m on m.domain_description_id=domain_description.id", [response])
    module = cursor.fetchone()
    cursor.close()
    connection.close()
    return module

def get_domain_name_based_on_id(domain_description_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM domain_description WHERE id = %s", [domain_description_id])
    module = cursor.fetchone()
    cursor.close()
    connection.close()
    return module

def add_organisation_entry(module, original, topic, response):
    domain_description_id = get_domain_description_id(module)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO data_basis(domain_description_id, original, topic, response) VALUES (%s, %s, %s, %s)", [domain_description_id, original, topic, response])
    connection.commit()
    cursor.close()
    connection.close()

def get_organisation_text(module):
    domain_description_id = get_domain_description_id_id(module)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT original FROM data_basis WHERE domain_description_id = %s and topic = 'Organisation'", [domain_description_id])
    module = cursor.fetchone()
    cursor.close()
    connection.close()
    return module

def check_if_domain_already_in_data_basis(module):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT domain_description_id FROM data_basis join (SELECT id FROM domain_description WHERE name = %s) i on i.id=domain_description_id", [module])
    module = cursor.fetchone()
    cursor.close()
    connection.close()
    return module

def delete_existing_data_basis(module):
    domain_description_id = get_domain_description_id(module)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM data_basis WHERE domain_description_id = %s", [domain_description_id])
    cursor.close()
    connection.close()

def get_stats_preferred(user):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT stats_preferred FROM user_client WHERE name = %s", [user])
    number_of_stats_to_return = cursor.fetchone()
    cursor.close()
    connection.close()
    return number_of_stats_to_return

def change_stats_preferred(user, stats_preferred):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("UPDATE user_client SET stats_preferred = %s WHERE name = %s", [stats_preferred, user])
    connection.commit()
    cursor.close()
    connection.close()

def links_from_multiple_domains(response):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT domain_description_id FROM data_basis WHERE response = %s", [response])
    domain_id = cursor.fetchone()
    domain_id = domain_id[0]
    cursor.execute("SELECT original FROM domain_description WHERE id = %s", [domain_id])
    original_module_name = cursor.fetchone()
    original_module_name = original_module_name[0]
    cursor.close()
    connection.close()
    return original_module_name

def get_all_domains():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM domain_description")
    all_domains = cursor.fetchall()
    cursor.close()
    connection.close()
    return all_domains

def get_all_domains_original():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT original FROM domain_description")
    all_domains = cursor.fetchall()
    cursor.close()
    connection.close()
    return all_domains

def get_all_links_of_last_response(user):
    user_id = get_user_client_id(user)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT all_links FROM message WHERE user_client_id = %s order by id desc limit 1", [user_id])
    all_links = cursor.fetchone()
    cursor.close()
    connection.close()
    return all_links

def check_if_link_belongs_to_module(response):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM domain_description join (SELECT domain_description_id FROM data_basis WHERE response = %s) m on m.domain_description_id=domain_description.id", [response])
    module = cursor.fetchone()
    cursor.close()
    connection.close()
    return module

def add_salt_value(user_name, value):
    connection = connect_to_database()
    cursor = connection.cursor()
    user_client_id = get_user_client_id(user_name)
    cursor.execute("INSERT INTO salt(user_client_id, value) VALUES (%s, %s)", [user_client_id, value])
    connection.commit()
    cursor.close()
    connection.close()

def get_salt_value(user_name):
    connection = connect_to_database()
    cursor = connection.cursor()
    user_client_id = get_user_client_id(user_name)
    cursor.execute("SELECT value FROM salt WHERE user_client_id = %s", [user_client_id])
    value = cursor.fetchone()
    cursor.close()
    connection.close()
    return value

def change_user_language(user, language):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("UPDATE user_client SET language = %s WHERE name = %s", [language, user])
    connection.commit()
    cursor.close()
    connection.close()

def get_user_language(user):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT language FROM user_client WHERE name = %s", [user])
    language = cursor.fetchone()
    cursor.close()
    connection.close()
    return language

def check_if_general_domain_existing():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM domain_description WHERE name = 'general'")
    existing = cursor.fetchone()
    cursor.close()
    connection.close()
    return existing

def add_small_talk_document_to_data_basis(domain_description_id, original, topic, response):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO data_basis(domain_description_id, original, topic, response) VALUES (%s, %s, %s, %s)", [domain_description_id, original, topic, response])
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

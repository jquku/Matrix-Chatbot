import sys

import psycopg2


def connect_to_database():
    connection = psycopg2.connect(
        database = "postgres",
        user = "postgres",
        password = "postgres",
        host = "localhost",
        port = "5432")
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
    cursor.execute("SELECT * FROM student WHERE name = %s", [name])
    query_result = cursor.fetchall()
    cursor.close()
    connection.close()
    if len(query_result) == 0:
        return False
    return True

def create_new_room(room_id, room_name, students):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO room(room_id, room_name, students) VALUES (%s, %s, %s)", [room_id, room_name, students])
    connection.commit()
    cursor.close()
    connection.close()

def create_new_student(name, last_module, links_preferred):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO student(name, last_module, links_preferred) VALUES (%s, %s, %s)", [name, last_module, links_preferred])
    connection.commit()
    cursor.close()
    connection.close()

def create_new_message(student_name, body, information_extracted, all_links, response):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO message(student_name, body, information_extracted, all_links, response) VALUES (%s, %s, %s, %s, %s)", [student_name, body, information_extracted, all_links, response])
    connection.commit()
    cursor.close()
    connection.close()

def add_data_basis_entry(module, original, topic, url):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO data_basis(module, original, topic, link) VALUES (%s, %s, %s, %s)", [module, original, topic, url])
    connection.commit()
    cursor.close()
    connection.close()

def data_basis_query(keywords):
    if len(keywords) == 0:
        return []
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT topic, link FROM data_basis WHERE topic LIKE '%" + keywords[0] + "%'"
    for i in range(1, len(keywords)):
        query = query + " OR topic LIKE '%" + keywords[i] + "%'"
    cursor.execute(query)
    links = cursor.fetchall()    #returns tuple
    cursor.close()
    connection.close()
    return links

def get_number_of_links_to_be_shown(user):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT links_preferred FROM student WHERE name = %s", [user])
    result = cursor.fetchall()
    result = str(result[0][0])
    cursor.close()
    connection.close()
    return result

def set_number_of_links_to_be_shown(user, number):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("UPDATE student SET links_preferred = %s WHERE name = %s", [number, user])
    connection.commit()
    cursor.close()
    connection.close()

#method for 'show all'; returns all links
def get_concerning_links(user):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT all_links FROM message WHERE student_name = %s and all_links != '' order by id desc limit 1", [user])
    fitting_links = cursor.fetchall()
    number_of_links = len(fitting_links)
    result = fitting_links[number_of_links-1] #get all_links from last message
    cursor.close()
    connection.close()
    return result

def get_next_links(user):
    connection = connect_to_database()
    cursor = connection.cursor()
    all_links = get_concerning_links(user)
    number_of_links_to_be_shown = get_number_of_links_to_be_shown(user)
    cursor.execute("SELECT response FROM message WHERE student_name = %s and all_links != '' order by id desc limit 1", [user])
    last_message = cursor.fetchall()
    last_message = str(last_message)
    all_links = list(all_links)
    links_in_list = all_links[0].split()
    highest_index = 0
    for i in range(0, len(links_in_list)):
        current = links_in_list[i]
        if current in last_message:
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
    cursor.execute("SELECT original, module FROM data_basis WHERE topic = %s", [topic])
    original = cursor.fetchone()
    cursor.close()
    connection.close()
    return original

def check_if_topic_already_in_statistic(topic):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT module FROM statistics WHERE topic = %s", [topic])
    module = cursor.fetchone()
    cursor.close()
    connection.close()
    return module

def create_new_statistic_entry(module, topic):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO statistics(module, topic, questioned) VALUES (%s, %s, %s)", [module, topic, 1])
    connection.commit()
    cursor.close()
    connection.close()

def increment_statistic_topic_counter(module, topic):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("UPDATE statistics SET questioned = questioned + 1 WHERE module = %s and topic = %s", [module, topic])
    connection.commit()
    cursor.close()
    connection.close()

def get_stats(module):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT topic FROM statistics WHERE module LIKE '%" + module + "%'" + "order by questioned desc")
    output = cursor.fetchall()
    cursor.close()
    connection.close()
    return output

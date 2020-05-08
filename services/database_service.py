import sys

from .sort_links import sort_links_by_matching

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
    connection.commit() #commit changes
    cursor.close()
    connection.close()

def create_new_student(name, last_module, links_preferred):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO student(name, last_module, links_preferred) VALUES (%s, %s, %s)", [name, last_module, links_preferred])
    connection.commit() #commit changes
    cursor.close()
    connection.close()

def create_new_message(student_name, body, information_extracted, all_links, response):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO message(student_name, body, information_extracted, all_links, response) VALUES (%s, %s, %s, %s, %s)", [student_name, body, information_extracted, all_links, response])
    connection.commit() #commit changes
    cursor.close()
    connection.close()

def add_data_basis_entry(module, topic, url):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO data_basis(module, topic, link) VALUES (%s, %s, %s)", [module, topic, url])
    connection.commit() #commit changes
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
    return sort_links_by_matching(links, keywords)

def get_number_of_links_to_be_shown(user):
    print("user: " + str(user))
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT links_preferred FROM student WHERE name = %s", [user])
    result = cursor.fetchall()
    result = str(result[0][0])
    cursor.close()
    connection.close()
    return result

def set_number_of_links_to_be_shown(user, number):
    print("user: " + user)
    print("number: " + number)
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
    cursor.execute("SELECT all_links FROM message WHERE student_name = %s", [user])
    fitting_links = cursor.fetchall()
    #print("fitting links: " + str(fitting_links))
    number_of_links = len(fitting_links)
    result = fitting_links[number_of_links-1] #get all_links from last message
    cursor.close()
    connection.close()
    return result

def get_next_links(user, message):
    connection = connect_to_database()
    cursor = connection.cursor()
    all_links = get_concerning_links(user)
    number_of_links_to_be_shown = get_number_of_links_to_be_shown(user)
    cursor.execute("SELECT response FROM message WHERE student_name = %s order by id desc limit 1", [user])
    last_message = cursor.fetchall()
    last_message = str(last_message)
    print("all_links: " + str(all_links) + str(type(all_links)))
    all_links = list(all_links)
    links_in_list = all_links[0].split()
    print("links_in_list: " + str(links_in_list))
    print("LAST MESSAGE: " + str(last_message) + str(type(last_message)))
    highest_index = 0
    for i in range(0, len(links_in_list)):
        current = links_in_list[i]
        if current in last_message:
            if i >= highest_index:
                highest_index = i + 1
    print("highest index: " + str(highest_index))
    print("links_in_list BEFORE: " + str(links_in_list))
    links_in_list = links_in_list[highest_index:]
    print("links_in_list AFTER: " + str(links_in_list))
    if int(number_of_links_to_be_shown) > len(links_in_list):
        number_of_links_to_be_shown = len(links_in_list)
    print("number_of_links_to_be_shown: " + str(number_of_links_to_be_shown))
    output = ""

    for j in range(0, int(number_of_links_to_be_shown)):
        print("current elemnt: " + str(links_in_list[j]))
        output = output + "\n" + "\n" + links_in_list[j]
    print("output: " + str(output))
    return output

import psycopg2

import sys
sys.path.append("./../")

from services.database_service import connect_to_database

def create_tables():

    #initialize db connection
    connection = connect_to_database()

    #create tables via sql commands
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS room (id SERIAL PRIMARY KEY, room_id text, room_name VARCHAR(255) NOT NULL, students text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS student (id SERIAL PRIMARY KEY, name VARCHAR(255), last_module VARCHAR(255), links_preferred integer, links_counter integer)")
    cursor.execute("CREATE TABLE IF NOT EXISTS statistics (id SERIAL PRIMARY KEY, module VARCHAR(255), topic VARCHAR(255), questioned integer)")
    cursor.execute("CREATE TABLE IF NOT EXISTS message (id SERIAL PRIMARY KEY, student_name VARCHAR(255), body text, information_extracted text, all_links text, response text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS data_basis (id SERIAL PRIMARY KEY, module VARCHAR(255), original VARCHAR(255), topic VARCHAR(255), link VARCHAR(255))")
    cursor.execute("CREATE TABLE IF NOT EXISTS module (id SERIAL PRIMARY KEY, name VARCHAR(255), source VARCHAR(255), satisfaction integer, feedback_given integer)")
    #cursor.execute("CREATE TABLE IF NOT EXISTS data_basis (id SERIAL PRIMARY KEY, module VARCHAR(255), original text, topic text, link VARCHAR(255))")
    connection.commit() #commit changes
    cursor.close()
    connection.close()

#python interpreter calls create_tables function
if __name__ == '__main__':
    create_tables()

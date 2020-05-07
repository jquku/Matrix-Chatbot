import psycopg2

import sys
sys.path.append("./../")

from services.database_service import connect_to_database

def create_tables():

    #initialize db connection
    connection = connect_to_database()

    #create tables via sql commands
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS room (room_id text, room_name VARCHAR(255) NOT NULL, students text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS student (name VARCHAR(255), last_module VARCHAR(255), links_preferred text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS statistics (module VARCHAR(255), topic VARCHAR(255), questioned integer)")
    cursor.execute("CREATE TABLE IF NOT EXISTS message (id SERIAL PRIMARY KEY, student_name VARCHAR(255), body text, information_extracted text, all_links text, response text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS data_basis (module VARCHAR(255), topic VARCHAR(255), link VARCHAR(255))")
    connection.commit() #commit changes
    cursor.close()
    connection.close()

#python interpreter calls create_tables function
if __name__ == '__main__':
    create_tables()

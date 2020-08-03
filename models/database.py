import psycopg2

import sys
sys.path.append("./../")

from services.database_service import connect_to_database

'''creating all the database tables based on sql commands'''

def create_tables():
    '''creates all the database tables'''
    connection = connect_to_database()      #initialize db connection

    #create tables via sql commands
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS domain_description (id SERIAL PRIMARY KEY, name VARCHAR(255), original VARCHAR(255), source VARCHAR(255), satisfaction integer, feedback_given integer)")
    cursor.execute("CREATE TABLE IF NOT EXISTS user_client (id SERIAL PRIMARY KEY, name text, last_module integer, links_preferred integer, stats_preferred integer, links_counter integer, language VARCHAR(255), FOREIGN KEY (last_module) REFERENCES domain_description(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS statistics (id SERIAL PRIMARY KEY, domain_description_id integer, topic VARCHAR(255), questioned integer, FOREIGN KEY (domain_description_id) REFERENCES domain_description(id) )")
    cursor.execute("CREATE TABLE IF NOT EXISTS message (id SERIAL PRIMARY KEY, user_client_id integer, body text, information_extracted text, all_links text, response text, FOREIGN KEY (user_client_id) REFERENCES user_client(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS data_basis (id SERIAL PRIMARY KEY, domain_description_id integer, original text, topic VARCHAR(255), response VARCHAR(255), FOREIGN KEY (domain_description_id) REFERENCES domain_description(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS salt (id SERIAL PRIMARY KEY, value text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS room (id SERIAL PRIMARY KEY, room_id text, user_client_id integer, FOREIGN KEY (user_client_id) REFERENCES user_client(id) )")
    connection.commit() #commit changes
    cursor.close()
    connection.close()

#python interpreter calls create_tables function
if __name__ == '__main__':
    create_tables()

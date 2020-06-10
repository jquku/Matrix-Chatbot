import psycopg2

import sys
sys.path.append("./../")

from services.database_service import connect_to_database

def create_tables():

    #initialize db connection
    connection = connect_to_database()

    #create tables via sql commands
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS module (id SERIAL PRIMARY KEY, name VARCHAR(255), original VARCHAR(255), source VARCHAR(255), satisfaction integer, feedback_given integer)")
    cursor.execute("CREATE TABLE IF NOT EXISTS user_chatbot (id SERIAL PRIMARY KEY, name text, last_module integer, links_preferred integer, stats_preferred integer, links_counter integer, language VARCHAR(255), FOREIGN KEY (last_module) REFERENCES module(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS statistics (id SERIAL PRIMARY KEY, module_id integer, topic VARCHAR(255), questioned integer, FOREIGN KEY (module_id) REFERENCES module(id) )")
    cursor.execute("CREATE TABLE IF NOT EXISTS message (id SERIAL PRIMARY KEY, user_chatbot_id integer, body text, information_extracted text, all_links text, response text, FOREIGN KEY (user_chatbot_id) REFERENCES user_chatbot(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS data_basis (id SERIAL PRIMARY KEY, module_id integer, original text, topic VARCHAR(255), link VARCHAR(255), FOREIGN KEY (module_id) REFERENCES module(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS salt (id SERIAL PRIMARY KEY, value text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS room (id SERIAL PRIMARY KEY, room_id text, room_name VARCHAR(255) NOT NULL, user_chatbot_id integer, FOREIGN KEY (user_chatbot_id) REFERENCES user_chatbot(id) )")
    connection.commit() #commit changes
    cursor.close()
    connection.close()

#python interpreter calls create_tables function
if __name__ == '__main__':
    create_tables()

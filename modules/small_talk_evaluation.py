import sys
sys.path.append("./../")

from services.database_service import add_small_talk_document_to_data_basis, add_new_module, check_if_general_module_existing
from nlp import language_processing

def add_small_talk_document():
    #add general module if not existing
    module_id = check_if_general_module_existing()
    if module_id == None:
        module_id = add_new_module("general", "General", "")    #name, original, source
    else:
        module_id = module_id[0]
    with open("general.txt", "r") as file:
        for line in file:
            line = line.rstrip("\n")
            elements = line.split('-')
            topic = elements[0]
            message = language_processing(topic)
            standardized_message = message[1]
            after_lemmitation = message[3]  #take nlp result of after lemmitation, since small talk contains stop words
            after_lemmitation = list_to_string(after_lemmitation)
            response = elements[1]
            add_small_talk_document_to_data_basis(module_id, topic, after_lemmitation, response) #original, topic, link

def list_to_string(message):
    final = ""
    for i in range(0, len(message)):
        final = final + message[i] +  " "
    return final

if __name__ == '__main__':
    add_small_talk_document()

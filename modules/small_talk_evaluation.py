import sys
sys.path.append("./../")

from services.database_service import (add_small_talk_document_to_data_basis,
    add_new_domain, check_if_general_domain_existing)
from nlp import language_processing

'''
add small talk document to data basis
document consists of topic + response entries
'''

def add_small_talk_document():
    '''adds small talk document into data basis, adjust filepath accordingly'''
    module_id = check_if_general_domain_existing()
    if module_id == None:
        module_id = add_new_domain("general", "General", "")    #name, original, source
    else:
        module_id = module_id[0]
    document_name = "../knowledge_domains/small_talk.txt"   #filepath
    with open(document_name, "r") as file:
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
    '''delete existing data basis based on domain/module name'''
    final = ""
    for i in range(0, len(message)):
        final = final + message[i] +  " "
    return final

if __name__ == '__main__':
    add_small_talk_document()

from bs4 import BeautifulSoup   #scraping by using the BeautifulSoup package

import requests

import sys

sys.path.append("./../")

from services.database_service import (add_data_basis_entry, add_new_domain,
    check_if_domain_already_in_data_basis, delete_existing_data_basis)
from nlp import language_processing

''''
index are being used as knowledge for the chatbot's data basis;
analyze html code via python module BeautifulSoup (web scraping)
topics need to be transfered into db
topics are identified by the 'li' tag or the 'a' tag
'''

def list_to_string(topic):
    '''method that transforms a list into a string'''
    output = ""
    for i in range(0, len(topic)):
        output = output + str(topic[i]) + " "
    return output

def add_data_basis():
    '''analyze web index and store into db'''
    module = "<module name>"    #add module name here
    module_original = module
    module = module.lower()
    module_in_db = check_if_domain_already_in_data_basis(module)

    if module_in_db == None:

        url = "<web index path>"  #add path of web index here
        url_prefix = "<url prefix>" #add url prefix here if necessary, prefix can also be ""
        response = requests.get(url)
        soup = BeautifulSoup(response.text)
        links = soup.findAll('li')
        numberOfLinks = len(links)
        module_id = add_new_domain(module, module_original, url)
        for link in links:

            ul = link.find('ul')

            if ul != None:    #this is a topic within the index without a link, get fist upcoming link then

                topic = ul.find_previous('li').text
                topic_original = topic.partition('\n')[0]
                topic = language_processing(topic_original)[1]
                topic = list_to_string(topic)

                url = ul.find('a').get('href')    #first link is taken
                url = url_prefix + url

            else:

                topic_original = link.find('a').text
                print("Added topic: " + str(topic_original))
                topic = language_processing(topic_original)[1]   #get final message of nlp module
                topic = list_to_string(topic)
                url = link.find('a').get('href')
                url = url_prefix + url

            add_data_basis_entry(module_id, topic_original, topic, url)

def delete_existing_data_basis(module):
    '''delete existing data basis based on domain/module name'''
    module = module.lower()
    delete_existing_data_basis(module)


if __name__ == '__main__':
    add_data_basis()

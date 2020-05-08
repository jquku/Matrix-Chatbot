from bs4 import BeautifulSoup   #scraping by using the BeautifulSoup package

import requests

import sys

sys.path.append("./../")

from services.database_service import add_data_basis_entry
from nlp import noise_removal, tokenization, lemmatization_topic

#index is used for the data basis; topics need to be transfered into db
#topics are identified by the 'li' tag or the 'a' tag

#later method with parameter url
#def add_data_basis(module, url, url_prefix):

def add_data_basis():

    module = "Operating Systems (OS)"
    url = "https://oer.gitlab.io/OS/index-terms.html"
    url_prefix = "https://oer.gitlab.io/OS/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    links = soup.findAll('li')
    numberOfLinks = len(links)
    for link in links:

        ul = link.find('ul')

        if ul != None:    #this is a topic within the index without a link, get fist upcoming link then

            topic = ul.find_previous('li').text
            topic = topic.partition('\n')[0]
            topic = topic.lower()
            topic = noise_removal(topic)
            #print("TOKEN pre: " + str(topic))
            topic = lemmatization_topic(topic)
            #print("TOKEN post: " + str(topic))

            url = ul.find('a').get('href')    #first link is taken
            url = url_prefix + url

        else:
            
            topic = link.find('a').text
            topic = topic.lower()
            topic = noise_removal(topic)
            #print("TOKEN pre: " + str(topic))
            topic = lemmatization_topic(topic)
            #print("TOKEN post: " + str(topic))
            #topic = tokenization(topic)
            url = link.find('a').get('href')
            url = url_prefix + url

        add_data_basis_entry(module, topic, url)


if __name__ == '__main__':
    add_data_basis()

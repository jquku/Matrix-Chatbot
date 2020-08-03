import sys
import nltk
import re
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.corpus import brown
from autocorrect import Speller

sys.path.append("./../")

from services.database_service import (data_basis_query, get_number_of_links_to_be_shown,
    set_number_of_links_to_be_shown, get_concerning_links, get_next_links)

'''
Natural Language Processing Strategy
1. Conversion to lowercase letters
2. Remove special characters
3. Tokenization
4. Remove spelling errors
5. Lemmatization
6. Remove stop words
'''

def language_processing(message):
    '''method is called first'''
    lowercased = lowercase(message)
    remove_noises = noise_removal(lowercased)
    tokens = tokenization(remove_noises)
    after_spell_checking = remove_spelling_errors(tokens)
    after_lemmatization = lemmatization(after_spell_checking)
    final_message = remove_stop_words(after_lemmatization)
    return lowercased, final_message, tokens, after_lemmatization    #returns tuple

def lowercase(text):
    '''lowercasing every letter in string'''
    message = text.lower()
    return message

def noise_removal(text):
    '''remove special char, every character besieds letters and numbers'''
    text = re.sub(r'([^a-zA-Z0-9\s]+?)', '', text)
    return text

def tokenization(message):
    '''tokenize message, also whitespaces deleted'''
    tokens = nltk.word_tokenize(message)
    return tokens

def lemmatization(tokens):
    '''lemmatization of tokens'''
    lemmatizer = WordNetLemmatizer()
    lemmatization_list = []
    for token in tokens:
        lemmatized = lemmatizer.lemmatize(token)
        lemmatization_list.append(lemmatized)
    return lemmatization_list

def remove_stop_words(list):
    '''removal of german and english stop words'''
    stop_words_english = set(stopwords.words('english'))
    stop_words_german = set(stopwords.words('german'))
    filtered_list = [w for w in list if not w in stop_words_english]
    filtered_list = [w for w in filtered_list if not w in stop_words_german]
    return filtered_list

def remove_spelling_errors(list):
    '''remove spelling errors via speller module'''
    spell = Speller()
    new_list = []
    for word in list:
        word_new = spell(word)
        new_list.append(word_new)
    return new_list

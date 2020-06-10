import sys
import nltk
import re
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from autocorrect import Speller

sys.path.append("./../")
#nltk.download()

from services.database_service import data_basis_query, get_number_of_links_to_be_shown, set_number_of_links_to_be_shown, get_concerning_links, get_next_links

#Natural Language Processing Strategy
#1. Conversion to lowercase letters
#2. Remove special characters
#3. Tokenization
#4. Lemmatization
#5. Remove stop words
#6. Remove spelling errors

def language_processing(message):
    lowercased = lowercase(message)

    remove_noises = noise_removal(lowercased)

    tokens = tokenization(remove_noises)

    after_lemmitation = lemmatization(tokens)

    without_stop_words = remove_stop_words(after_lemmitation)

    final_message = remove_spelling_errors(without_stop_words)

    #print("lowercased: " + str(lowercased))
    #print("final FINAL FINAL FINAL message: " + str(final_message) + str(type(final_message)))
    return lowercased, final_message, tokens    #returns tuple

#lowercasing every letter in string
def lowercase(text):
    message = text.lower()
    return message

#remove special characters
def noise_removal(text):
    #every character besieds letters (a-z) and numbers
    text = re.sub(r'([^a-zA-Z0-9\s]+?)', '', text)
    return text

#tokenize text, also whitespaces deleted
def tokenization(message):
    tokens = nltk.word_tokenize(message)
    return tokens

def lemmatization(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatization_list = []
    for token in tokens:
        lemmatized = lemmatizer.lemmatize(token)
        lemmatization_list.append(lemmatized)
    return lemmatization_list

def remove_stop_words(list):
    stop_words_english = set(stopwords.words('english'))
    stop_words_german = set(stopwords.words('german'))
    filtered_list = [w for w in list if not w in stop_words_english
        and stop_words_german]
    return filtered_list

def remove_spelling_errors(list):
    spell_english = Speller(lang='en')
    new_list = []
    for i in range(0, len(list)):
        current_element = list[i]
        autocorrect = spell_english(current_element)
        new_list.append(autocorrect)
    return new_list

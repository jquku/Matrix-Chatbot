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

def strategy(message, user):
    lowercased = lowercase(message)

    help = check_if_help_called(message)

    if help != "":
        final_response = []
        final_response.append(lowercased)
        final_response.append("")
        final_response.append(help)
        return final_response

    options_called = check_if_options_called(lowercased, user)
    if options_called == True:
        final_response = []
        final_response.append(lowercased)
        final_response.append("")
        final_response.append("")
        return final_response

    if type(options_called) is tuple:
        final_response = []
        final_response.append(lowercased)
        final_response.append(options_called[0])
        final_response.append(options_called[0])
        return final_response

    if type(options_called) == str:
        final_response = []
        final_response.append(lowercased)
        final_response.append(get_concerning_links(user)[0])
        final_response.append(options_called)
        return final_response
#    print("lowercase message " + lowercased)
    remove_noises = noise_removal(lowercased)
#    print("no special characters: " + remove_noises)
    tokens = tokenization(remove_noises)

    after_lemmitation = lemmatization(tokens)

    greeting_involved = greetings(after_lemmitation)
    #print("GREETING INVOLVED: " + str(greeting_involved))

    goodbyes_involved = goodbyes(after_lemmitation)
    #print("GOODBYES INVOLVED: " + str(goodbyes_involved))

#    print("after lemmitation: " + str(after_lemmitation))
    without_stop_words = remove_stop_words(after_lemmitation)
#    print("without stop words: " + str(without_stop_words))
    final_message = remove_spelling_errors(without_stop_words)
#    print("final message: " + str(final_message))
    links = compare_message_with_data_basis(final_message)
    #print("LINKS BEFORE BEFORE BEFORE: " + str(type(links)) + str(links) + str(len(links)))

    #print("LINKS BEFORE BEFORE BEFORE: " + str(type(links)) + str(links) + str(len(links)))
    response = build_response(greeting_involved, links, goodbyes_involved, user)
    final_response = []
    final_response.append(final_message)
    final_response.append(list_to_string(links))
    final_response.append(response)
    return final_response

def list_to_string(links):
    final = ""
    for i in range(0, len(links)):
        final = final + links[i] +  "\n" +  "\n"
    return final

def check_if_options_called(message, user):
    #get more links
    #set number of links to be shown
    if "links = " in message or "link = " in message or "links= " in message or "link=" in message:

        number = re.findall(r'\d+', message)

        if len(number) == 1:
            number = str(number[0])
            set_number_of_links_to_be_shown(user, number)
            return True

    if "show more" in message or "zeig mehr" in message:
        links_last_message = get_next_links(user, message)
        return links_last_message

    if "show all" in message or "zeig alles" in message:
        links_last_message = get_concerning_links(user)
        return links_last_message

    return False

def check_if_help_called(message):

    help_phrases = ['help', 'i need help', 'help me', 'hilf mir', 'hilfe']
    standard = "Use 'links = X' to return X links by default. \n" + "Use 'show more' to display more links fitting the query. \n" + "Use 'show all' to display all links fitting the query."
    for i in range(0, len(help_phrases)):
        current = help_phrases[i]
        if current in message:
            return standard
    return ""

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

def greetings(tokens):  #greeting forms found on the internet
    greeting_involved = False
    phrases = ["hi", "hello", "hey", "helloo", "hellooo", "g morining",
        "gmorning","good morning", "morning", "good day", "good afternoon",
        "good evening","greetings", "greeting", "good to see you",
        "its good seeing you","how are you", "how're you", "how are you doing",
        "how ya doin'","how ya doin", "how is everything",
        "how is everything going","how's everything going", "how is you",
        "how's you", "how are things","how're things", "how is it going",
        "how's it going", "how's it goin'", "how's it goin",
        "how is life been treating you", "how's life been treating you",
        "how have you been", "how've you been", "what is up", "what's up",
        "what is cracking", "what's cracking", "what is good", "what's good",
        "what is happening", "what's happening", "what is new", "what's new",
        "what is neww", "g’day", "howdy", "hallo", "bonjour"]
    for i in range(0, len(tokens)):
        if tokens[i] in phrases:
            greeting_involved = True
    return greeting_involved

def goodbyes(tokens):
    goodbyes_involved = False
    phrases = ["goodbye", "au revoir", "bye", "tschüß", "tschau", "see you",
        "bye bye", "see you soon", "auf wiedersehen", "bis bald",
        "take it easy", "have a nice day", "take care", "goodnight",
        "catch you later", "peace", "peace out"]
    for i in range(0, len(tokens)):
        if tokens[i] in phrases:
            goodbyes_involved = True
    return goodbyes_involved

def lemmatization_topic(topic):
    final_topic_string = ""
    list_of_words = topic.split() #split topic into words
    lemmatizer = WordNetLemmatizer()
    for i in range(0, len(list_of_words)):
        current = list_of_words[i]
        lemmatized = lemmatizer.lemmatize(current)
        final_topic_string = final_topic_string + str(lemmatized) + " "
    return final_topic_string

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

def compare_message_with_data_basis(message):
    link = data_basis_query(message)
    return link

def build_response(greeting_involved, links, goodbyes_involved, user):
    response = ""
    default_answer = "I'm a chatbot serving as your digital learning assistant. Tell me which topic you want to know more about."
    number_of_links = len(links)
    if greeting_involved == True:
        response = "Hi "
    if number_of_links > 0:
        how_many_links_to_show = get_number_of_links_to_be_shown(user)
        print("how many links to show: " + how_many_links_to_show)
        if how_many_links_to_show == "default":
            how_many_links_to_show = 3
        how_many_links_to_show = int(how_many_links_to_show)
        response = response + "I've found " + str(number_of_links) + " results. "
        for i in range(0, number_of_links):
            if i < how_many_links_to_show:
                response = response + links[i] +  "\n" +  "\n"
            else:
                break
    if goodbyes_involved == True:
        response = response + "Bye"
    if response == "":
        response = default_answer
    return response

    #first 4 steps: Natural Language Understanding, #5 Natural Language Generation
    #1. Tokenize: Text wird in token unterteilt (z.B Punkte)
    #2. Normalisierung: Rechtschreibfehler werden bereinigt
    #3. Recognising Entities: Worüber wird im Text gesprochen?
    #4. Dependency Parsing: Sätze werden unterteilt in Nomen, Verben, Objekte etc..
    #5. Generation: Generierung einer Antwort

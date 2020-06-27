# Matrix-Chatbot

This natural language processing matrix-chatbot is designed for Riot.im and is based on the matrix.nio client libary. The chatbot can be used as a digital learning assistant for students. 
Knowledge extension is achieved by simply adding new rules in predetermined files that serve as a data basis for the chatbot. The application offers a statistical overview of frequently asked topics, which can be queried directly via the chatbot.

## Perequisites
- python3
- pip3
- docker.io
- docker-compose

## Configuration
- Create a new Riot.im user account manually and edit the user variable in [main.py](https://github.com/jquku/Matrix-Chatbot/blob/master/modules/main.py) appropiately.
- To expand the chatbot's data basis, add new rules to [small_talk_evaluation.py](https://github.com/jquku/Matrix-Chatbot/blob/master/modules/small_talk_evaluation.py) and [organisational_document.py](https://github.com/jquku/Matrix-Chatbot/blob/master/modules/organisational_document.py).

## Setup
1. Install the latest version of python-olm
   For e2e support, installing the [libolm](https://gitlab.matrix.org/matrix-org/olm) C libary is recommended
   ```console
   git clone https://gitlab.matrix.org/matrix-org/olm.git
   sudo make
   sudo make install
   sudo ldcfongig
2. Install [matrix-nio](https://github.com/poljar/matrix-nio), if you want e2e support call
   ```console
   pip3 install "matrix-nio[e2e]"
3. Clone this repository and navigate into the repoistory folder
4. Install all the requirements
   ```console
   pip3 install -r requirements.txt
5. Add all the nltk data    
   ```console
   python3 -m nltk.downloader all
6. Start the docker container
   ```console
   docker-compose up -d
7. Navgiate into folder models and create all the tables
   ```console
   python3 database.py
8. Add data basis by entering the folder modules and call the following scripts
   ```console
   python3 index_evaluation.py
   python3 organisational_document.py
   python3 small_talk_evaluation.py
9. Start the chatbot 
   ```console
   python3 main.py

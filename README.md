# Matrix-Chatbot

This matrix-chatbot is designed for the Riot messenger and is based on the matrix nio client libary. The chatbot can be used as a digital learning assistant for students and offers an anonymized, analytical processing of behavioral data.

## Setup

Make sure python3 is installed, check via python3 -V
sudo apt-get install python3-pip

sudo apt install docker.io docker-compose
user should be in group docker

git clone https://gitlab.matrix.org/matrix-org/olm.git
sudo su
make
make install
ldcfongig

pip3 install "matrix-nio[e2e]"


1. Clone this repository
2. navigate into Matrix-Chatbot folder
2. pip3 install -r requirements.txt
python3 -m nltk.downloader all
3. docker-compose up -d to create
5. Navgiate into folder models
3. python3 database.py to create
7. navigate into folder modules
8. python3 index_evaluation.py
9. python3 organisational_document.py
10. python3 small_talk_evaluation.py

Prerequisites
- make sure all the requirements are installed

 Run the database docker container by using the command
 docker-compose up -d.

 Create tables by running
 Add data basis
 Run main.py

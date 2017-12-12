#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import os

# URL of the codingbat website
URL = "http://codingbat.com"


# This will connect to the website and return the webpage
# This function might create an overhead incase the website is down
# or the path is broken
def get_webpage(url):
    r = requests.get(url)
    while r.status_code != 200:
        print("Connecting \n")
        r = requests.get(url)
    return r.text


# Get the all categories of questins available
def get_categories(text):
    soup = BeautifulSoup(text, 'lxml')
    categories = []
    for i in soup.find_all('div', class_='summ'):
        categories.append(i.find('a')['href'].split('/')[2])
    return categories


# Get all the questions in a specific category
def get_questions(category, topic):
    url = URL + "/" + topic + "/" + category
    soup = BeautifulSoup(get_webpage(url), 'lxml')
    question_names = []
    question_path = []
    for i in soup.find('div', class_='indent').find_all('td'):
        link = i.find('a')
        question_names.append(link.text)
        question_path.append(link['href'])
    return zip(question_names, question_path)


# Extract the question from it's webpage
def extract_question(text):
    soup = BeautifulSoup(text, 'lxml')
    question_td = soup.find('div', class_='indent').find('td')
    question = []

    # To get the question Text
    question.append(question_td.p.text)

    # get the contents of the table data containing quesiton
    # checks for the break element to add the use cases
    for i in range(len(question_td.contents)):
        # Possible area of improvement
        if str(question_td.contents[i]) == '<br/>':
            question.append(question_td.contents[i + 1])
    return question


# The Main function
def main(if_python=False):
    # To get the categories of questions
    if if_python:
        TOPIC = "python"
    else:
        TOPIC = "java"

    print ('Fetching the questions of the {} topic'.format(TOPIC))
    topic_page = get_webpage(URL + "/" + TOPIC)
    categories = get_categories(topic_page)

    os.mkdir('./{}'.format(TOPIC))
    os.chdir('./{}/'.format(TOPIC))

    for category in categories:
        # Creates a new directory for the category
        os.mkdir("./{}".format(category))
        os.chdir('./{}/'.format(category))

        questions = get_questions(category, TOPIC)

        for ques_name, ques_path in questions:
            ques_url = URL + ques_path
            print (ques_url)

            quest_page = get_webpage(ques_url)
            ques = extract_question(quest_page)

            with open('./{}'.format(ques_name), 'w') as f:
                f.writelines('Question:\n')
                f.writelines(ques[0])
                f.writelines('\n\nUse Cases:\n')
                for i in range(len(ques) - 1):
                    f.writelines(ques[i + 1] + "\n")

        # To get back in the main topic directory
        os.chdir('./../')

    # To get to the main codingbat directory
    os.chdir('./../')


if __name__ == "__main__":
    # Creating the main codingbat directory
    os.mkdir('./codingbat')
    os.chdir('./codingbat/')
    # For the java questions
    main()
    # For the python questions
    main(True)

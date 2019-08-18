import json
import requests
import time
import sys
import os

DIRECTORY_URL = "http://directory.pythonanywhere.com"
FAILURE_MESSAGE = "The server responded with an unsuccessful code: "
ACTIVE_URL = []


class Agency:
      def __init__(self, name, url, code):
        self.name = name
        self.url = url
        self.code = code


def run():
    with requests.session() as session:
        while True:
            user_input = input("""\nEnter one of the following commands:
            login \'url\' 
            logout 
            post 
            news [agency_id] [category] [region] [yyyy/mm/dd]
            list 
            delete \'story_key\'\n""")

            user_inputs = user_input.split(" ")
            command = user_inputs[0]

            # login case.
            if command == "login":
                try:
                    url = user_inputs[1]
                except:
                    print("Missing parameters")
                    continue

                login(session, url)
                continue

            # logout case.
            elif command == "logout":
                logout(session)
                break

            # post case.
            elif command == "post":
                post(session)

            # news case.
            elif command == "news":
                try:
                    id = user_inputs[1]
                    category = user_inputs[2]
                    region = user_inputs[3]
                    date = user_inputs[4]
                except:
                    print("Missing parameters")
                    continue
                news(session, id, category, region, date)

            # list case.
            elif command == "list":
                list_services(session)

            # delete case
            elif command == "delete":
                story_key = user_inputs[1]
                delete(session, story_key)

            # default case
            else:
                print("Incorrect command!")

            time.sleep(2)


def login(session, url):
    url ='http://127.0.0.1:8000'#'http://ll14tac.pythonanywhere.com'

    username = input("Hello author, Please enter your username for the service: \n")
    password = input("Enter your password: \n")
    response = session.post(url + "/api/login/", data={'username': username, 'password': password})

    # If any response but success notify user.
    if response.status_code != 201:
        print(FAILURE_MESSAGE + str(response.status_code))
        return False
    else:
        print("Successfully logged in!")
        ACTIVE_URL.append(url)
        return True


def logout(session):
    if session_is_active():
        headers = {'X-CSRFToken': session.cookies['csrftoken']}
        response = session.post(ACTIVE_URL[0] + "/api/logout/", headers=headers)
        print(response.text)
    print("\nThe session has been ended \n")


def post(session):
    headline = input("What is the headline?: ")
    category = input("\nWhat is the category? Please type one of the following: pol, art, tech or trivia: ")
    region = input("\nWhat is the region? Please type one of the following: uk, eu or w: ")
    details = input("Please type the story's details: ")

    data = {'headline': headline, 'category': category, 'region': region, 'details': details}

    headers = {'X-CSRFToken': session.cookies['csrftoken']}

    if not session_is_active():
        print("You aren't logged into any services")
        return
    else:
        response = session.post(ACTIVE_URL[0] + "/api/poststory/", json=data, headers=headers)
        if response.status_code != 201:
            print(FAILURE_MESSAGE + str(response.status_code) + " " + str(response.text))
            return

        print("Post was successful")


def news(session, agency_id, category, region, date):
    if category == '[]':
        category = '*'
    else:
        category = category.strip(']')
        category = category.strip('[')
    if region == '[]':
        region = '*'
    else:
        region = region.strip(']')
        region = region.strip('[')
    if date == '[]':
        date = '*'
    else:
        date = date.strip(']')
        date = date.strip('[')

    agency_id = agency_id.strip(']')
    agency_id = agency_id.strip('[')

    data = {'story_cat': category, 'story_region': region, 'story_date': date}
    agency_list = retrieve_list_response(session)

    if agency_id == '':
        for agency in agency_list:
            print("Agency - " + agency["agency_name"])
            stories = retrieve_stories(session, agency["agency_url"], data)
            print_stories(stories)
    else:
        for agency in agency_list:
            if agency['agency_code'] == agency_id:
                stories = retrieve_stories(session, agency["agency_url"], data)
                print_stories(stories)


def list_services(session):
    response = retrieve_list_response(session)
# if response.status_code == 200:
    print("\nSuccessfully retrieved all news agencies : ")
    #json_data = json.loads(response.json)
    services = []
    for agency in response:
        print("Name : " + agency["agency_name"])
        print("URL  : " + agency["agency_url"])
        print("Code : " + agency["agency_code"]+ "\n")

    for agency in services:
        print(agency.name + '\n')
        print(agency.url + '\n')
        print(agency.code + '\n')
    return
# else:
    print(FAILURE_MESSAGE + str(response.status_code))
    return


def delete(session, story_key):
    data = {'story_key': story_key}
    headers = {'X-CSRFToken': session.cookies['csrftoken']}
    response = session.post(ACTIVE_URL[0] + "/api/deletestory/", json=data, headers=headers)

    if response.status_code != 201:
        print(FAILURE_MESSAGE + str(response.status_code) + " " + str(response.text))
        return
    else:
        print("Successfully deleted!")
        return


def retrieve_list_response(session):
    #response = session.get(DIRECTORY_URL + "/api/list")
    #json_data = json.loads(response.text)
    json_data = json.loads('''{ "agency_list": [{ "agency_name": "ll14tac", "agency_url": "http://127.0.0.1:8000", "agency_code": "TAC" }]}''')

    agencies = []
    for agency in json_data["agency_list"]:
        agencies.append({'agency_name': agency['agency_name'], 'agency_url': agency['agency_url'], 'agency_code': agency['agency_code'] })
    return agencies


def retrieve_stories(session, url, data):
    response = session.get(url + "/api/getstories/", params=data)
    json_data = json.loads(response.text)
    stories = []

    for story in json_data["stories"]:
        stories.append(story)
    return stories

def print_stories(stories):
    for story in stories:
        print("Story Key : " + story["key"])
        print("Headline  : " + story["headline"])
        print("Category  : " + story["story_cat"])
        print("Region    : " + story["story_region"])
        print("Author    : " + story["author"])
        print("Date      : " + story["story_date"])
        print("Details   : " + story["story_details"] + "\n")

def session_is_active():
    return len(ACTIVE_URL) > 0

try:
    run()
    sys.exit(0)
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
